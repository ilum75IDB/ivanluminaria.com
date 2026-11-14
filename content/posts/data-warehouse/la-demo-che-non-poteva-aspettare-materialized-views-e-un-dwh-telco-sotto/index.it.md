---
categories:
- data-warehouse
date: '2026-12-09'
description: Come le Materialized Views hanno trasformato un prototipo DWH lento in
  un sistema di reportistica credibile per un grande operatore telco. Criteri di scelta,
  strategie di refresh e risultati misurabili.
draft: false
image: la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto.cover.jpg
seoTitle: 'Materialized Views nel DWH: performance analitiche in ambiente Telco'
tags:
- materialized-views
- data-warehouse
- performance-tuning
- oracle
- postgresql
title: 'La demo che non poteva aspettare: Materialized Views e un DWH Telco sotto
  pressione'
translationKey: la_demo_che_non_poteva_aspettare_materialized_views_e_un_dwh_telco_sotto
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La demo che non poteva aspettare

Era un progetto che non avremmo dovuto fare. Non nel senso che fosse sbagliato farlo — era esattamente il tipo di lavoro che ci piaceva — ma nel senso che nessuno ce lo aveva commissionato. Il team di consulenza aveva deciso di costruire un prototipo di Data Warehouse per un grande operatore telco mobile con cui lavoravamo da mesi, convinti che la reportistica dettagliata su clienti e traffico telefonico potesse sbloccare conversazioni commerciali nuove. Una scommessa interna, finanziata con ore non fatturate e un po' di entusiasmo.

L'idea era semplice: portare al team marketing del cliente una dashboard che mostrasse pattern di traffico, distribuzione geografica delle chiamate, segmentazione per tipo di contratto. Dati che loro avevano, ma che non riuscivano a leggere in modo aggregato. Noi avevamo l'accesso ai sistemi sorgente, avevamo l'esperienza, avevamo voglia di dimostrare qualcosa.

Quello che non avevamo calcolato bene era la scala.

I record di dettaglio delle chiamate — i CDR, *Call Detail Records* — si accumulavano a un ritmo di circa 500 GB al mese. Anni di dati storici, decine di milioni di righe per ogni periodo mensile. Quando abbiamo cominciato a costruire i report sopra queste tabelle, la realtà si è fatta sentire in modo piuttosto diretto: i colleghi che testevano le query tornavano con facce lunghe e numeri poco incoraggianti. Un'ora e quarantacinque minuti per un'aggregazione mensile. Tre minuti per caricare la dashboard principale. Il PM, che aveva creduto nel progetto fin dall'inizio, aveva smesso di fare domande entusiaste e aveva cominciato a fare domande preoccupate.

La demo era fissata. Non si poteva spostare.

## Quando il motore si inceppa sui volumi

Il problema non era un bug. Era strutturale, e vale la pena capire perché, perché è lo stesso problema che si incontra in qualunque ambiente analitico che cresce senza una strategia di pre-aggregazione.

Le query di reportistica su un DWH hanno una caratteristica precisa: aggregano grandi volumi di dati storici per produrre risultati sintetici. Una query che calcola il traffico mensile per cliente, per esempio, deve leggere potenzialmente milioni di righe, applicare funzioni di aggregazione, fare join con la tabella anagrafica. Il database esegue questo lavoro ogni volta che qualcuno apre il report.

Una query tipica sul nostro schema aveva questa forma:

```sql
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    SUM(cdr.CALL_DURATION_SEC) / 60.0  AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                  AS TOTAL_CALLS,
    AVG(cdr.COST)                      AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
WHERE
    cdr.CALL_DATE >= TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
    AND cdr.CALL_DATE <  TRUNC(SYSDATE, 'MM')
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME
ORDER BY
    cm.REGION,
    TOTAL_DURATION_MIN DESC;
```

Il piano di esecuzione mostrava quello che ci aspettavamo: una full scan su `call_detail_records` per il mese selezionato, un hash join con `customer_master`, poi l'aggregazione. Con 500 GB mensili di CDR e indici che aiutavano poco su query di range temporale così ampie, il tempo di risposta era quello che era.

Aggiungere indici avrebbe aiutato marginalmente. Partizionare per data avrebbe ridotto il volume scansionato, ma non avremmo avuto il tempo di riprogettare lo schema prima della demo. Serviva qualcosa che spostasse il lavoro fuori dalla query stessa.

## L'esperienza che trova il suo momento

Non è stata un'intuizione improvvisa. Ho proposto le Materialized Views perché le avevo già usate in altri contesti — su Oracle, in ambienti di reportistica finanziaria — e sapevo che il pattern si adattava bene a quello che stavamo cercando di fare.

Una Materialized View è, nella sostanza, una query i cui risultati vengono calcolati una volta e memorizzati fisicamente su disco come se fossero una tabella. Quando un'applicazione interroga la MV, non ricalcola nulla: legge dati già aggregati. La differenza con una view standard è esattamente questa: la view normale è una definizione di query che viene eseguita ogni volta, la MV è un risultato pre-calcolato che viene aggiornato periodicamente.

Oracle supporta le Materialized Views da molto tempo, con opzioni sofisticate di refresh e query rewriting automatico [1][2]. PostgreSQL le ha introdotte nella versione 9.3 con una sintassi più essenziale ma ugualmente efficace [3]. In entrambi i casi, il principio è lo stesso: sposta il costo computazionale dal momento della lettura al momento del refresh.

Nel nostro contesto, questo era esattamente il trade-off giusto. I dati storici non cambiavano. I report del mese precedente erano statici. Potevamo pre-calcolare tutto una volta sola, o al massimo una volta al giorno, e servire i risultati in millisecondi.

## Candidati ideali e scenari in cui non ha senso

Non tutte le query sono buone candidate per una Materialized View. Prima di implementare, abbiamo fatto una mappatura rapida dei pattern di accesso.

I candidati ideali condividono alcune caratteristiche:

**Aggregazioni frequenti su dati storici stabili.** Se la stessa aggregazione viene eseguita decine di volte al giorno su dati che cambiano poco o nulla, il costo del refresh periodico è ampiamente giustificato dal risparmio sulle letture. I report mensili sui CDR erano il caso perfetto: i dati del mese precedente non cambiano mai, quelli del mese corrente cambiano solo con i nuovi record in arrivo.

**Join complessi tra tabelle grandi.** Il join tra `call_detail_records` e `customer_master` era costoso perché coinvolgeva milioni di righe. Pre-calcolarlo nella MV significava che la dashboard non doveva mai eseguire quel join.

**Report con latenza tollerabile sui dati.** Se il marketing accetta report aggiornati ogni ora, o anche ogni notte, una MV con refresh schedulato è la soluzione naturale. Se invece serve consistenza in tempo reale — un saldo bancario, una disponibilità di magazzino live — le MV introducono complessità senza risolvere il problema.

I casi in cui **non** ha senso:

- Dati che cambiano continuamente e richiedono consistenza immediata
- Query eseguite raramente (il costo del refresh supera il beneficio)
- Tabelle sorgente piccole dove la query originale è già veloce
- Scenari OLTP dove la latenza di scrittura del refresh è inaccettabile

Nel nostro DWH, la distinzione era netta: i dati storici erano perfetti per le MV, i dati del giorno corrente potevano restare su query dirette.

## Refresh, coerenza e il costo nascosto

La parte che richiede più attenzione non è la creazione della MV, ma la gestione del refresh. È qui che si prendono le decisioni architetturali che contano.

Oracle offre due modalità principali [2]:

- **`REFRESH COMPLETE`**: ricalcola l'intera MV da zero. Semplice, affidabile, costoso su grandi volumi. Adatto quando i dati sorgente cambiano in modo non tracciabile.
- **`REFRESH FAST`**: aggiornamento incrementale basato sui *materialized view logs*, strutture che tracciano le modifiche alle tabelle sorgente. Molto più efficiente, ma richiede che le tabelle base abbiano i log abilitati e che la query della MV rispetti alcuni vincoli.

PostgreSQL [3] supporta solo il refresh completo (`REFRESH MATERIALIZED VIEW`), con l'opzione `CONCURRENTLY` che permette di aggiornare la MV senza bloccare le letture — a patto che esista un indice univoco sulla MV stessa.

Nel nostro caso abbiamo scelto un approccio pragmatico: refresh completo notturno per le MV sui dati storici, eseguito tramite uno scheduler interno nelle ore di bassa attività. Il carico sul sistema sorgente durante il refresh era concentrato in una finestra temporale accettabile, e i report del mattino trovavano dati già pronti.

La configurazione Oracle per il refresh automatico aveva questa struttura:

```sql
-- Creazione del job di refresh (Oracle DBMS_SCHEDULER)
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'REFRESH_MV_MONTHLY_TRAFFIC',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN DBMS_MVIEW.REFRESH(''MV_MONTHLY_TRAFFIC_SUMMARY'', ''C''); END;',
        start_date      => TRUNC(SYSDATE + 1) + INTERVAL '2' HOUR,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Refresh notturno MV traffico mensile per reportistica marketing'
    );
END;
/
```

Un dettaglio che vale la pena sottolineare: il refresh completo su una MV grande blocca temporaneamente le query su quella MV (in Oracle, a meno di usare `ATOMIC_REFRESH => FALSE`). Pianificare il refresh nelle ore giuste non è un dettaglio operativo secondario — è parte del design.

## I report tornano a vivere

La MV che ha risolto il problema principale aggregava il traffico mensile per cliente e regione:

```sql
CREATE MATERIALIZED VIEW mv_monthly_traffic_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM')          AS CALL_MONTH,
    SUM(cdr.CALL_DURATION_SEC) / 60.0   AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                   AS TOTAL_CALLS,
    AVG(cdr.COST)                       AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM');

-- Indice per le query più frequenti della dashboard
CREATE INDEX idx_mv_monthly_region_month
    ON mv_monthly_traffic_summary (REGION, CALL_MONTH);
```

I numeri dopo il primo refresh erano quelli che speravamo. La query di aggregazione mensile che impiegava 45 secondi scendeva a 2 secondi — e quei 2 secondi erano quasi interamente latenza di rete e rendering dell'applicazione, non elaborazione del database. Il caricamento della dashboard marketing passava da 3 minuti a circa 10 secondi.

Il PM ha visto i risultati su uno schermo di test il pomeriggio prima della demo. Non ha detto molto. Ha annuito, ha chiesto se eravamo sicuri che i dati fossero corretti, e quando gli abbiamo confermato che sì, erano gli stessi dati di prima solo pre-aggregati, ha detto "bene" e ha chiuso il laptop.

Era il tipo di approvazione silenziosa che conta più di qualunque complimento.

## Oltre la demo: il valore che rimane

La demo è andata bene. Il team marketing del cliente ha interagito con i report, ha fatto domande sui dati, ha chiesto se fosse possibile aggiungere filtri per tipo di contratto e per area geografica. Nessuno ha commentato la velocità — e questo era esattamente il risultato corretto. Quando un sistema funziona come dovrebbe, gli utenti non pensano all'infrastruttura. Pensano ai dati.

L'obiezione implicita che aleggiava sul progetto — "abbiamo già i dati, perché dovremmo investire in un DWH separato?" — si è dissolta nel momento in cui il team marketing ha visto pattern che non riusciva a vedere prima. Non perché i dati fossero nuovi, ma perché erano accessibili in modo diverso. La reportistica aggregata e navigabile cambia il tipo di domande che si possono fare.

Le Materialized Views non erano la risposta a tutto. Il DWH aveva ancora bisogno di lavoro: la gestione degli aggiornamenti incrementali, la storicizzazione delle anagrafiche, la gestione delle eccezioni nei CDR. Ma avevano risolto il problema che bloccava il progetto in quel momento specifico, e avevano fissato un principio architetturale che avremmo usato come base per il resto dello sviluppo: pre-calcolare ciò che è stabile, lasciare dinamico solo ciò che deve esserlo.

Il progetto non è rimasto un prototipo. Nei mesi successivi è diventato un contratto.

## Quello che resta sul quaderno

La lezione più utile di questa storia non riguarda le Materialized Views in sé. Riguarda il momento in cui uno strumento tecnico diventa rilevante.

Le MV non erano una novità per nessuno di noi. Erano uno strumento che conoscevamo, che avevamo usato in altri contesti, che sapevamo funzionare in determinati scenari. Il valore non era nell'invenzione, ma nel riconoscimento: questo problema, in questo momento, con questi vincoli di tempo, si risolve così.

Ci sono situazioni in cui la soluzione giusta è quella che conosci già, non quella che stai cercando di imparare. Sapere quando applicare ciò che si ha già in cassetta è una competenza che si costruisce con gli anni e con i progetti, non con i tutorial.

Il PM ha dato fiducia e spazio per implementare qualcosa che non era nel piano originale. Il team ha collaborato per verificare la correttezza dei dati dopo il refresh. Il DBA del cliente ha controllato l'impatto sul sistema sorgente durante la finestra di refresh notturna e ha dato il via libera. Nessuno ha salvato niente da solo — è andata bene perché le persone giuste hanno fatto le cose giuste al momento giusto.

Il quaderno tecnico si arricchisce così: non di soluzioni nuove, ma di contesti in cui le soluzioni vecchie funzionano ancora.

## Fonti ufficiali

1. Oracle Database SQL Language Reference 19c — [CREATE MATERIALIZED VIEW](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-MATERIALIZED-VIEW.html) — sintassi completa, opzioni `REFRESH FAST/COMPLETE`, `ON COMMIT`, `BUILD IMMEDIATE/DEFERRED`
2. Oracle Database Data Warehousing Guide 19c — [Basic Materialized Views](https://docs.oracle.com/en/database/oracle/oracle-database/19/dwhsg/basic-materialized-views.html) — concetti, strategie di utilizzo in DWH, query rewriting
3. PostgreSQL Documentation — [Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html) — `CREATE MATERIALIZED VIEW`, `REFRESH MATERIALIZED VIEW`, opzione `CONCURRENTLY`

## Glossario
- **[Materialized View (MV)](/it/glossary/materialized-view/)** — Vista pre-calcolata e memorizzata fisicamente su disco. Contiene il risultato di una query eseguita in anticipo; le letture successive leggono dati già aggregati senza ricalcolare. Supportata da Oracle, PostgreSQL, SQL Server e altri RDBMS.

- **[Refresh (MV)](/it/glossary/materialized-view/)** — Processo di aggiornamento dei dati di una Materialized View per riflettere le modifiche nelle tabelle base. Può essere completo (ricalcolo totale) o incrementale (solo le variazioni tracciate nei MV log). La frequenza e la modalità sono scelte architetturali con impatto diretto sulle performance.

- **[Call Detail Record (CDR)](/it/glossary/refresh/)** — Record che descrive una singola chiamata telefonica: identificativo cliente, data, durata, tipo di chiamata, costo. Nei sistemi telco i CDR sono il dato operativo primario e si accumulano in volumi molto elevati (centinaia di GB mensili per operatori di medie dimensioni).

- **[Query Rewriting](/it/glossary/materialized-view/)** — Funzionalità di Oracle che intercetta automaticamente una query sulle tabelle base e la redirige verso una Materialized View equivalente, senza modifiche al codice applicativo. Attivabile con `ENABLE QUERY REWRITE` nella definizione della MV.

- **[Data Warehouse (DWH)](/it/glossary/refresh/)** — Sistema di database ottimizzato per l'analisi dei dati storici, che aggrega informazioni da diverse sorgenti operative. A differenza dei sistemi OLTP, privilegia le letture massive e le aggregazioni rispetto alle scritture frequenti e puntuali.
