---
categories:
- oracle
date: '2026-11-24'
description: 'Flashback Query, Table, Drop e Database in Oracle: come recuperare dati
  persi per errori logici in minuti, senza restore da backup e senza downtime.'
draft: false
image: oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database.cover.jpg
seoTitle: 'Oracle Flashback: recupero dati logici senza downtime'
tags:
- oracle
- flashback
- recovery
- undo
- rto
title: 'Oracle Flashback: recupero dati logici senza downtime, da Query a Database'
translationKey: oracle_flashback_recupero_dati_logici_senza_downtime_da_query_a_database
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La riunione del martedì mattina

La segnalazione è arrivata durante una riunione settimanale su Teams, non come alert di monitoraggio, non come ticket urgente. Uno dei responsabili di area ha condiviso lo schermo e ha detto, con tono più perplesso che allarmato: "I numeri di ieri non tornano. E quelli dell'altro ieri nemmeno."

La dashboard direzionale di un grande gruppo assicurativo italiano — quella che ogni mattina alimenta le decisioni operative sui premi e sui sinistri — mostrava dati incongruenti. Non un crash, non una pagina bianca. I dati c'erano, ma erano sbagliati. O meglio: erano incompleti, e nessuno aveva ricevuto un alert perché tecnicamente il sistema funzionava. La pipeline girava, le tabelle erano accessibili, le query rispondevano. Semplicemente, alcune righe erano sparite da circa quarantotto ore.

Trenta minuti di riunione per raccogliere le osservazioni dei colleghi, restringere la finestra temporale del problema, capire che non si trattava di un'interruzione di servizio ma di un errore logico silenzioso. Poi la domanda inevitabile: come si recuperano quei dati?

La risposta, in quel contesto, non era "ripristiniamo dal backup".

## Perché il backup completo non era la prima mossa

Un restore da backup su una tabella da circa 500 GB e 2 miliardi di righe non è un'operazione che si fa in un'ora. Richiede una finestra di manutenzione, un ambiente di staging dove ripristinare selettivamente, la gestione delle dipendenze con le altre tabelle, e quasi certamente un'interruzione del servizio per gli utenti. In un contesto assicurativo dove la dashboard alimenta decisioni quotidiane su portafogli attivi, questo ha un costo reale.

Oracle, però, offre da anni una suite di funzionalità che permette di fare qualcosa di molto più chirurgico: tornare indietro nel tempo a livello di singola query, di tabella, o persino dell'intero database, sfruttando dati che il motore conserva già per altri scopi — gli undo segments e i flashback logs. Collettivamente, queste tecnologie si chiamano **Oracle Flashback** [1].

Il principio è semplice: Oracle mantiene versioni precedenti dei blocchi dati per gestire la consistenza delle letture (MVCC) e il rollback delle transazioni. Le funzionalità Flashback sfruttano questa infrastruttura per permettere operazioni di recovery mirate, senza toccare i backup.

## Flashback Query: quindici minuti per trovare l'ago

La prima cosa da fare era capire esattamente cosa mancava. Flashback Query permette di eseguire una `SELECT` come se il database fosse in uno stato precedente, specificando un timestamp o un SCN (System Change Number) [2].

L'SCN è un contatore interno di Oracle che avanza monotonicamente a ogni commit: identifica un punto preciso nella storia del database. Ogni riga ha un SCN associato all'ultima modifica. Flashback Query usa gli undo segments per ricostruire la versione di una riga a un SCN passato.

La prima query è stata un conteggio semplice, per verificare quante righe erano presenti due giorni fa rispetto a oggi:

```sql
-- Conteggio righe presenti 48 ore fa
SELECT COUNT(*)
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' DAY);
```

Il risultato ha confermato l'ipotesi: la tabella conteneva circa 340.000 righe in più rispetto allo stato attuale. Qualcosa le aveva rimosse, e il sistema non aveva generato alert perché la rimozione era avvenuta tramite una transazione apparentemente normale.

La seconda query ha isolato le righe mancanti per una data specifica:

```sql
-- Righe presenti ieri per una data di vendita specifica
SELECT *
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' DAY)
WHERE sales_date = TO_DATE('2024-11-22', 'YYYY-MM-DD');
```

Quindici minuti di analisi. Le righe c'erano, erano state cancellate, e il pattern della cancellazione suggeriva un job batch mal configurato che aveva eseguito un `DELETE` con una condizione più ampia del previsto. Nessun errore applicativo, nessun rollback: la transazione era andata a buon fine, ma aveva fatto più del necessario.

Il recovery è stato altrettanto diretto: un `INSERT ... SELECT ... AS OF TIMESTAMP` per reinserire le righe mancanti dalla versione storica della tabella. Cinque minuti, nessuna interruzione di servizio, nessuna finestra di manutenzione.

```sql
-- Reinserimento delle righe cancellate accidentalmente
INSERT INTO DASHBOARD_DATA.DAILY_SALES_METRICS
SELECT *
FROM DASHBOARD_DATA.DAILY_SALES_METRICS
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '2' DAY)
WHERE sales_date BETWEEN TO_DATE('2024-11-20', 'YYYY-MM-DD')
                     AND TO_DATE('2024-11-22', 'YYYY-MM-DD')
  AND metric_id NOT IN (
      SELECT metric_id FROM DASHBOARD_DATA.DAILY_SALES_METRICS
  );
```

Perché Flashback Query funzioni, è necessario che i dati di undo siano ancora disponibili — ovvero che il parametro `UNDO_RETENTION` sia configurato per un periodo sufficiente e che gli undo segments non siano stati sovrascritti per pressione di spazio. In questo caso, il sistema era configurato con un retention di 24 ore, sufficiente per coprire la finestra di quarantotto ore grazie alla combinazione con i flashback logs.

## Flashback Table e Flashback Drop: quando serve qualcosa di più

Flashback Query è lo strumento giusto quando si sa cosa cercare e si vogliono recuperare righe specifiche. Ma ci sono scenari dove serve un approccio diverso.

### Ripristinare una tabella intera

`FLASHBACK TABLE` riporta un'intera tabella — dati e struttura — a un punto nel tempo precedente [3]. È utile quando la corruzione è diffusa e non vale la pena identificare riga per riga cosa recuperare.

```sql
-- Ripristino di una tabella a un'ora fa
FLASHBACK TABLE DASHBOARD_DATA.DAILY_SALES_METRICS
TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' HOUR);
```

Due requisiti che vale la pena tenere a mente:

**ROW MOVEMENT** deve essere abilitato sulla tabella. Oracle, durante il flashback, può dover spostare fisicamente le righe (il ROWID cambia), e questo richiede che la tabella lo permetta esplicitamente:

```sql
ALTER TABLE DASHBOARD_DATA.DAILY_SALES_METRICS ENABLE ROW MOVEMENT;
```

**UNDO retention** deve coprire il punto nel tempo a cui si vuole tornare. Se gli undo segments sono stati sovrascritti, l'operazione fallisce con `ORA-01555: snapshot too old`.

A differenza di un restore da backup, `FLASHBACK TABLE` non richiede di portare il database in modalità mount, non interrompe le sessioni attive sulle altre tabelle, e non richiede una finestra di manutenzione. Il servizio resta disponibile.

### Recuperare una tabella eliminata

`FLASHBACK DROP` è il caso più drammatico e, paradossalmente, uno dei più semplici da gestire [3]. Quando si esegue un `DROP TABLE` senza `PURGE`, Oracle non elimina fisicamente la tabella: la sposta nel **Recycle Bin**, un'area logica dello spazio tablespace dove gli oggetti eliminati restano finché lo spazio non è necessario per altri scopi.

```sql
-- Recupero di una tabella eliminata per errore
FLASHBACK TABLE DASHBOARD_DATA.STAGING_METRICS TO BEFORE DROP;
```

Per vedere cosa c'è nel Recycle Bin:

```sql
SELECT object_name, original_name, droptime, space
FROM recyclebin
ORDER BY droptime DESC;
```

I limiti sono due: se la tabella è stata eliminata con `PURGE`, o se il Recycle Bin è stato svuotato (`PURGE RECYCLEBIN`), non c'è nulla da recuperare. E se lo spazio tablespace è sotto pressione, Oracle può riutilizzare automaticamente lo spazio del Recycle Bin senza preavviso.

## Flashback Database: il caso più serio

Le tre funzionalità precedenti operano a livello di oggetto o di riga. `FLASHBACK DATABASE` è un'altra categoria: riporta l'intero database a un punto nel tempo precedente, come se si premesse un tasto "annulla" globale [4].

Si usa in scenari dove l'errore è pervasivo: una patch applicativa che ha corrotto dati su decine di tabelle, un aggiornamento di schema andato storto, un errore logico che si è propagato attraverso procedure e trigger prima che qualcuno se ne accorgesse.

I requisiti sono più stringenti rispetto alle altre funzionalità:

- **Flashback Logging** deve essere abilitato (`ALTER DATABASE FLASHBACK ON`)
- Una **Fast Recovery Area (FRA)** deve essere configurata con spazio sufficiente
- Il parametro `DB_FLASHBACK_RETENTION_TARGET` definisce per quanti minuti il database mantiene i flashback logs (nel sistema del gruppo assicurativo era impostato a 4320 minuti, ovvero 3 giorni)

Il workflow di recovery richiede di portare il database in modalità mount:

```sql
-- Workflow Flashback Database
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP
    TO_TIMESTAMP('2024-11-22 08:00:00', 'YYYY-MM-DD HH24:MI:SS');
ALTER DATABASE OPEN RESETLOGS;
```

`RESETLOGS` è obbligatorio: dopo un Flashback Database, i redo logs vengono azzerati perché la storia del database è stata riscritta. Questo implica che i backup precedenti al `RESETLOGS` non sono più direttamente applicabili per un recovery incrementale — è necessario fare immediatamente un backup completo dopo l'operazione.

La differenza rispetto a un restore tradizionale è nel tempo: un Flashback Database su un sistema con FRA ben dimensionata può completarsi in minuti invece che in ore, perché lavora sui flashback logs (blocchi modificati) invece di dover ripristinare l'intera struttura fisica del database.

## I limiti che non si possono ignorare

Oracle Flashback non è un sostituto del backup. È un complemento per errori logici con una finestra temporale definita. Tre aspetti pratici da tenere presenti:

**Dipendenza dall'UNDO retention.** Flashback Query e Flashback Table dipendono dalla disponibilità dei dati di undo. Se il tablespace UNDO è sotto pressione, Oracle può sovrascrivere i dati di undo prima che scada il retention configurato. Il parametro `UNDO_RETENTION` è un obiettivo, non una garanzia assoluta — a meno di non abilitare `RETENTION GUARANTEE` sul tablespace UNDO, che impedisce la sovrascrittura anche a costo di fallire le transazioni che richiedono spazio.

**Impatto sullo spazio.** I flashback logs per `FLASHBACK DATABASE` occupano spazio nella FRA. Con `DB_FLASHBACK_RETENTION_TARGET` a 3 giorni su un database con workload intenso, la FRA può crescere rapidamente. Il monitoraggio dello spazio FRA è parte della routine operativa, non un'attività occasionale [5].

```sql
-- Monitoraggio spazio FRA
SELECT name, space_limit/1024/1024/1024 AS limit_gb,
       space_used/1024/1024/1024 AS used_gb,
       space_reclaimable/1024/1024/1024 AS reclaimable_gb
FROM v$recovery_file_dest;
```

**Errori fisici e media failure.** Flashback non aiuta in caso di corruzione fisica dei blocchi dati, perdita di datafile, o guasto hardware. Per questi scenari servono i backup tradizionali, la Data Guard, o entrambi. La suite Flashback copre la categoria degli errori logici — quelli che, statisticamente, sono la causa più frequente di perdita di dati in produzione, ma non l'unica.

## Quello che resta dopo la riunione

I dati sono stati recuperati. La dashboard era di nuovo affidabile entro mezzogiorno, senza che nessun utente avesse percepito un'interruzione. Il job batch responsabile della cancellazione è stato corretto e aggiunto alla lista delle verifiche del change management.

Il punto che vale la pena sottolineare non è la velocità del recovery — cinquanta minuti dall'inizio della riunione alla dashboard ripristinata — ma la natura dello strumento. Flashback Query non ha richiesto di fermare nulla. Non ha richiesto di coinvolgere il team di infrastructure per un restore. Non ha richiesto una comunicazione agli utenti.

Ha richiesto di sapere che esisteva e come funzionava.

In molti ambienti Oracle, le funzionalità Flashback sono abilitate per default o con configurazione minima, ma non vengono mai usate perché non fanno parte del playbook operativo quotidiano. Finiscono nei manuali, non nelle runbook. E quando serve un recovery rapido, si tende a saltare direttamente al backup — che è la risposta giusta per molti scenari, ma non per tutti.

Investire qualche ora a capire la differenza tra `FLASHBACK TABLE` e un restore da RMAN, a testare `FLASHBACK DATABASE` in un ambiente di pre-produzione, a configurare correttamente `UNDO_RETENTION` e la FRA: è il tipo di lavoro preparatorio che non produce risultati visibili finché non serve. E quando serve, produce risultati molto visibili.

## Fonti ufficiali

1. Oracle Database — [Using Oracle Flashback Technology](https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/using-oracle-flashback-technology.html) — panoramica delle funzionalità Flashback, SCN, undo segments, architettura generale.
2. Oracle Database SQL Language Reference 19c — [SELECT (Flashback Queries)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/SELECT.html) — sintassi `AS OF TIMESTAMP` e `AS OF SCN`, clausole Flashback Version Query e Flashback Transaction Query.
3. Oracle Database SQL Language Reference 19c — [FLASHBACK TABLE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/FLASHBACK-TABLE.html) — sintassi `FLASHBACK TABLE ... TO TIMESTAMP`, `TO BEFORE DROP`, requisiti ROW MOVEMENT, Recycle Bin.
4. Oracle Database Backup and Recovery User's Guide 19c — [Performing Flashback Database and Database Point-in-Time Recovery](https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-performing-flashback-dbpitr.html) — workflow `FLASHBACK DATABASE`, requisiti FRA e Flashback Logging, `OPEN RESETLOGS`.
5. Oracle Database Reference 19c — [DB_FLASHBACK_RETENTION_TARGET](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/DB_FLASHBACK_RETENTION_TARGET.html) — parametro di configurazione, unità (minuti), interazione con la FRA.

## Glossario
- **[Flashback Query](/it/glossary/flashback-query/)** (Oracle) — Funzionalità che permette di eseguire una `SELECT` su uno stato passato del database, specificando un timestamp o un SCN. Sfrutta i dati di undo senza richiedere restore da backup. Utile per identificare e recuperare righe cancellate o modificate accidentalmente.

- **[Flashback Table](/it/glossary/scn/)** (Oracle) — Comando che ripristina un'intera tabella a un punto nel tempo precedente, inclusi i dati. Richiede `ROW MOVEMENT` abilitato sulla tabella e che i dati di undo siano ancora disponibili. Non interrompe le sessioni attive sulle altre tabelle del database.

- **[Flashback Database](/it/glossary/rto/)** (Oracle) — Tecnica di recovery che riporta l'intero database a un punto nel tempo precedente, usando i flashback logs nella Fast Recovery Area. Richiede `STARTUP MOUNT` e si chiude con `OPEN RESETLOGS`. Più rapido di un restore RMAN completo per errori logici pervasivi.

- **[SCN](/it/glossary/flashback-query/)** (System Change Number) — Contatore interno di Oracle che avanza monotonicamente a ogni commit. Identifica un punto preciso nella storia del database. Le operazioni Flashback usano l'SCN come riferimento temporale preciso, alternativo o complementare al timestamp.

- **[RTO](/it/glossary/flashback-table/)** (Recovery Time Objective) — Tempo massimo accettabile di indisponibilità di un sistema dopo un errore o un disastro. Le funzionalità Flashback riducono l'RTO per errori logici da ore (restore da backup) a minuti, senza richiedere finestre di manutenzione.
