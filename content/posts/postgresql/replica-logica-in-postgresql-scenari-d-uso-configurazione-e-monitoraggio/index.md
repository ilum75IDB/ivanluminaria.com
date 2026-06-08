---
title: "Replica logica in PostgreSQL: le domande di un collega che chiariscono l'argomento"
date: 2099-12-31
draft: true
section: postgresql
webo_status: da_approvare
webo_generated_at: 2026-06-08
---

## Un affiancamento che non era una lezione

Claudio era lì per osservare, non per imparare in senso formale. L'affiancamento era lavoro reale: un sistema di gestione sinistri e polizze in produzione, un grande gruppo assicurativo italiano, e la necessità concreta di migrare da PostgreSQL 13 a PostgreSQL 15 senza interrompere le operazioni. In parallelo, il team di analisi frodi attendeva un flusso di dati verso il data warehouse per alimentare i propri modelli.

Non era il contesto ideale per spiegare la replica logica da zero. Eppure Claudio ha fatto esattamente le domande che chiunque farebbe la prima volta — e rispondere a quelle domande ad alta voce, in modo che reggesse, ha reso più solida ogni scelta che avevo già fatto in silenzio.

Questo articolo segue quella sequenza: prima le domande, poi i concetti, poi la configurazione concreta.

---

## Replica fisica e replica logica: il dilemma iniziale

La prima domanda di Claudio è arrivata prima ancora di aprire un terminale: «Perché non usiamo la replica fisica? Non è quella che si usa di solito?»

È la domanda giusta. La replica fisica — streaming replication — è la scelta consolidata per alta disponibilità e disaster recovery. Funziona a livello di blocco: il server primario trasmette i WAL (Write-Ahead Log) al replica, che li applica identicamente. Il risultato è una copia byte per byte del cluster. Semplice da configurare, affidabile, ben documentata [1].

Il limite è esattamente la sua forza: replica *tutto*, nello stesso formato, alla stessa versione di PostgreSQL. Non si può replicare solo alcune tabelle. Non si può replicare verso una versione diversa del motore. Non si può usare il replica come sorgente per un sistema esterno che parla un protocollo diverso.

La replica logica opera a livello di riga, non di blocco. Il publisher decodifica le modifiche dai WAL e le trasmette come operazioni logiche — `INSERT`, `UPDATE`, `DELETE` — verso uno o più subscriber. Questo apre tre possibilità che la replica fisica non offre:

- replicare un sottoinsieme di tabelle o righe
- replicare tra versioni diverse di PostgreSQL (dalla 10 in poi, con limitazioni)
- alimentare sistemi eterogenei come data warehouse o message broker tramite Change Data Capture (CDC)

Nel nostro caso, tutte e tre le necessità erano presenti contemporaneamente.

---

## I tre scenari e le domande di Claudio

### Migrazione cross-versione senza downtime

«Ma non posso fare un `pg_upgrade`?» ha chiesto Claudio, guardando la documentazione sul monitor accanto.

Sì, `pg_upgrade` funziona. Ma richiede di portare il sistema offline, eseguire l'upgrade, verificare, e solo allora riaprire il traffico. Con 100 milioni di righe in `claim_events.claims` e 300 milioni in `claim_events.claim_details`, il tempo di inattività sarebbe stato nell'ordine delle ore — inaccettabile per un sistema che gestisce liquidazioni attive.

La replica logica permette un approccio diverso: si prepara il nuovo cluster PostgreSQL 15 (`pg-claims-new-01`), lo si alimenta tramite subscription, e quando il lag di replica è ridotto a secondi si esegue lo switchover. Il downtime si riduce al tempo necessario per reindirizzare le connessioni — minuti, non ore.

### Integrazione CDC verso il data warehouse

«È come un trigger distribuito?» ha chiesto Claudio, con una certa soddisfazione per l'analogia.

No — e la differenza è sostanziale. Un trigger viene eseguito in transazione, aggiunge latenza, e scala male su volumi elevati. La replica logica legge i WAL *dopo* che la transazione è già stata confermata: nessun impatto sul percorso critico delle scritture, nessun lock aggiuntivo, nessun overhead sul publisher oltre alla decodifica WAL.

Per il team antifrode, la necessità era ricevere in tempo quasi reale le nuove richieste di risarcimento (`fraud_detection_audit.new_claims_for_analysis`) su `pg-dw-subscriber-01`. La publication dedicata `fraud_audit_pub` ha risolto esattamente questo requisito, senza toccare la logica applicativa.

### Replica selettiva

«E se voglio solo i dati dei clienti attivi?» ha chiesto Claudio, pensando già a un caso d'uso futuro.

Qui la risposta è più articolata. La replica logica permette di selezionare le tabelle da includere in una publication. A partire da PostgreSQL 15, è possibile aggiungere anche una clausola `WHERE` per filtrare le righe [2]. La limitazione principale riguarda le DDL: le modifiche di schema non vengono replicate automaticamente — punto su cui torno nella sezione sul monitoraggio.

---

## Concetti chiave: publication, subscription e slot di replica

Prima di passare alla configurazione, tre concetti da tenere fermi.

**Publication** — definisce *cosa* viene replicato sul publisher. Può includere tabelle specifiche, tutte le tabelle di un database (`FOR ALL TABLES`), o — dalla versione 15 — sequenze. Ogni publication ha un nome e può essere referenziata da più subscriber.

**Subscription** — definisce *chi* riceve i dati e *da dove*. La subscription viene creata sul subscriber e specifica la stringa di connessione al publisher e il nome della publication a cui si iscrive. Al momento della creazione, PostgreSQL esegue una copia iniziale dei dati (initial snapshot) e poi applica le modifiche successive in streaming.

**Slot di replica logica** — è il meccanismo che garantisce la persistenza. Il publisher mantiene i segmenti WAL necessari finché il subscriber non li ha consumati. Questo è fondamentale per la consistenza, ma introduce un rischio: se un subscriber si disconnette a lungo, i WAL si accumulano e lo spazio su disco del publisher può esaurirsi. Il monitoraggio degli slot è obbligatorio in produzione.

---

## Configurazione pratica

### Publisher: `pg-claims-primary-01` (PostgreSQL 13.10)

Il parametro più importante è `wal_level`, che deve essere impostato a `logical`. Gli altri parametri dimensionano le risorse per gli slot e i worker.

```sql
-- Su pg-claims-primary-01
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = '10';
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();
```

`wal_level = 'logical'` richiede un riavvio del server per essere attivo. Gli altri parametri sono applicabili con `pg_reload_conf()`, ma è buona norma verificare i valori effettivi dopo il reload:

```sql
SHOW wal_level;
SHOW max_replication_slots;
```

Dopo il riavvio, si creano le publication. Per la migrazione, le tabelle principali:

```sql
CREATE PUBLICATION claims_pub
  FOR TABLE insurance_policies.policies,
             claim_events.claims;
```

Per l'integrazione con il data warehouse, una publication separata e dedicata:

```sql
CREATE PUBLICATION fraud_audit_pub
  FOR TABLE fraud_detection_audit.new_claims_for_analysis;
```

Separare le publication per caso d'uso è una scelta deliberata: permette di gestire permessi, monitoraggio e ciclo di vita in modo indipendente.

**Utente di replica** — il subscriber si connette con un utente dedicato che deve avere il ruolo `REPLICATION` e i permessi `SELECT` sulle tabelle pubblicate:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '...';
GRANT SELECT ON insurance_policies.policies TO replicator;
GRANT SELECT ON claim_events.claims TO replicator;
GRANT SELECT ON fraud_detection_audit.new_claims_for_analysis TO replicator;
```

Verificare anche che `pg_hba.conf` permetta la connessione dall'IP del subscriber con il metodo di autenticazione appropriato (preferibilmente `scram-sha-256`).

### Subscriber per migrazione: `pg-claims-new-01` (PostgreSQL 15.3)

```sql
-- Su pg-claims-new-01
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION claims_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION claims_pub;
```

Al momento della `CREATE SUBSCRIPTION`, PostgreSQL avvia lo snapshot iniziale: copia tutte le righe esistenti nelle tabelle pubblicate, poi passa alla replica delle modifiche in streaming. Con 150 milioni di righe tra `policies` e `claims`, questo snapshot ha richiesto alcune ore — pianificato in un momento di bassa attività.

### Subscriber per il data warehouse: `pg-dw-subscriber-01` (PostgreSQL 15.3)

```sql
-- Su pg-dw-subscriber-01
ALTER SYSTEM SET max_worker_processes = '5';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION fraud_audit_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION fraud_audit_pub;
```

---

## Monitoraggio e troubleshooting

«Come faccio a sapere se sta funzionando?» — la domanda di Claudio più utile di tutte.

### Lag di replica

La vista `pg_replication_slots` sul publisher mostra lo stato degli slot attivi e il volume di WAL trattenuto:

```sql
SELECT
  slot_name,
  active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS replication_lag_bytes
FROM pg_replication_slots
WHERE slot_type = 'logical';
```

Un `replication_lag_bytes` in crescita costante segnala un subscriber in difficoltà. Se `active` è `false` e il lag continua ad aumentare, lo slot sta accumulando WAL senza consumarli: situazione da risolvere rapidamente.

Sul subscriber, `pg_stat_subscription` e `pg_stat_subscription_stats` mostrano lo stato dell'applicazione:

```sql
SELECT
  subname,
  subenabled,
  subconninfo,
  subslotname,
  substate,
  subbinary
FROM pg_subscription;

SELECT
  subid,
  relid,
  last_applied_lsn,
  last_received_lsn,
  pg_wal_lsn_diff(last_received_lsn, last_applied_lsn) AS apply_lag_bytes
FROM pg_stat_subscription_stats;
```

`apply_lag_bytes` misura il ritardo tra ciò che il subscriber ha ricevuto e ciò che ha effettivamente applicato. Un valore stabile e basso indica un sistema in salute.

### Conflitti e primary key

Il conflitto più comune in replica logica è la violazione di primary key: il subscriber riceve un `INSERT` per una riga che esiste già localmente. Questo accade tipicamente quando il subscriber ha dati preesistenti non allineati con il publisher.

PostgreSQL registra i conflitti nel log del subscriber con messaggi del tipo:

```
ERROR: duplicate key value violates unique constraint "claims_pkey"
```

La replica si interrompe fino alla risoluzione. Le opzioni sono: eliminare la riga conflittuale sul subscriber, o usare `ALTER SUBSCRIPTION ... SKIP` per saltare la transazione problematica (con consapevolezza delle implicazioni sulla consistenza).

### Gestione delle DDL

«Se aggiungo una colonna sul publisher, il subscriber la vede?» ha chiesto Claudio, e la risposta ha richiesto una pausa.

No — non automaticamente. La replica logica trasporta i dati, non le modifiche di schema. Se si aggiunge una colonna `NOT NULL` senza default sul publisher, la replica si interrompe perché il subscriber non sa dove mettere il valore.

La procedura corretta è:

1. Aggiungere la colonna sul subscriber prima che sul publisher (con un default o come `NULL`)
2. Aggiungere la colonna sul publisher
3. Verificare che la replica riprenda correttamente

Per modifiche di schema frequenti o complesse, strumenti come `pg_logical` o soluzioni CDC dedicate (Debezium, pgoutput con consumer esterni) offrono gestione più sofisticata. In questo progetto, le DDL erano rare e pianificate: la procedura manuale era sufficiente.

---

## Best practice e considerazioni operative

**Spazio WAL** — dimensionare `max_slot_wal_keep_size` (disponibile dalla versione 13) per limitare l'accumulo di WAL in caso di subscriber inattivi. Senza questo parametro, un subscriber disconnesso può esaurire lo spazio disco del publisher.

**Sicurezza** — usare sempre `scram-sha-256` in `pg_hba.conf` per le connessioni di replica. Valutare SSL obbligatorio aggiungendo `sslmode=require` nella stringa di connessione della subscription. Non usare l'utente `postgres` per la replica.

**Slot orfani** — uno slot di replica non più utilizzato ma non eliminato continua a trattenere WAL. Monitorare periodicamente `pg_replication_slots` e rimuovere gli slot obsoleti con `SELECT pg_drop_replication_slot('nome_slot')`.

**Tabelle senza primary key** — la replica logica in modalità `UPDATE` e `DELETE` richiede una primary key o una replica identity configurata (`REPLICA IDENTITY FULL` come alternativa, con impatto sulle performance). Verificare tutte le tabelle prima di creare la publication.

**Switchover finale** — nel caso della migrazione, il momento critico è il taglio: si disabilita la scrittura sul publisher (o si reindirizza il traffico), si attende che il lag scenda a zero, si verifica la consistenza, si promuove il nuovo cluster. Con il lag monitorato nei giorni precedenti e stabile sotto i 500ms, lo switchover ha richiesto meno di tre minuti.

---

## Chiusura

Il sistema è andato in produzione senza intoppi. Non c'è stato un problema dell'ultimo minuto, non c'è stato un momento di tensione da raccontare. Il nuovo cluster PostgreSQL 15 ha preso il traffico, il data warehouse ha continuato a ricevere i dati antifrode, e il gruppo assicurativo ha avuto il suo upgrade senza finestre di manutenzione visibili agli utenti.

Claudio ha una comprensione più concreta di quello che ha osservato. Io ho una comprensione più articolata di quello che so — perché ho dovuto trovare le parole giuste, non solo i comandi giusti. Spiegare la differenza tra replica fisica e logica a qualcuno che non la conosce significa doverla capire abbastanza bene da scegliere l'esempio corretto, non solo quello tecnicamente accurato.

Le domande di Claudio non hanno cambiato le scelte tecniche. Le hanno rese più solide.

---

## Fonti ufficiali

[1] PostgreSQL Documentation — [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — concetti generali, architettura, differenze con la replica fisica.

[2] PostgreSQL Documentation — [CREATE PUBLICATION](https://www.postgresql.org/docs/current/sql-create-publication.html) — sintassi completa, opzioni di filtro per riga (PostgreSQL 15+), gestione delle sequenze.

[3] PostgreSQL Documentation — [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/current/sql-create-subscription.html) — sintassi, opzioni di connessione, gestione dello snapshot iniziale.

[4] PostgreSQL Documentation — [Monitoring — pg_stat_replication_slots](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) — viste di sistema per il monitoraggio degli slot.

[5] PostgreSQL Documentation — [Replication Slots](https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS) — meccanismo degli slot, rischi di accumulo WAL, `max_slot_wal_keep_size`.

---

## Glossario candidato

**Publication** — oggetto PostgreSQL che definisce l'insieme di tabelle (e opzionalmente righe, dalla versione 15) i cui cambiamenti vengono resi disponibili per la replica logica. Creata sul publisher con `CREATE PUBLICATION`, può essere referenziata da più subscriber indipendenti.

**Subscription** — oggetto PostgreSQL creato sul subscriber che stabilisce la connessione al publisher, specifica la publication a cui iscriversi e gestisce il ciclo di vita della replica: snapshot iniziale, streaming delle modifiche, riconnessione automatica.

**Slot di replica logica** — struttura persistente sul publisher che traccia la posizione di consumo dei WAL per ogni subscriber. Garantisce che nessuna modifica venga persa in caso di disconnessione temporanea, al costo di trattenere i segmenti WAL fino al consumo.

**WAL (Write-Ahead Log)** — registro sequenziale di tutte le modifiche apportate al database PostgreSQL, scritto prima che le modifiche vengano applicate ai file di dati. È la sorgente da cui la replica logica estrae le operazioni da trasmettere ai subscriber tramite il processo di decodifica logica.

**CDC (Change Data Capture)** — tecnica che intercetta e trasmette in tempo quasi reale le modifiche ai dati di una sorgente verso sistemi destinatari (data warehouse, message broker, applicazioni). La replica logica di PostgreSQL implementa CDC nativamente tramite il protocollo `pgoutput`.
