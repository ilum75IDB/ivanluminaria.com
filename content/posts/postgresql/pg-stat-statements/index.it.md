---
title: "pg_stat_statements: la prima cosa da installare su qualsiasi PostgreSQL"
description: "Un PostgreSQL in produzione da due anni senza pg_stat_statements. Quando l'abbiamo attivato, tre query consumavano l'80% delle risorse — e ognuna si risolveva con un indice. Come installare, interrogare e leggere i risultati dell'estensione più importante per la diagnostica PostgreSQL."
date: "2026-04-21T08:03:00+01:00"
draft: false
translationKey: "pg_stat_statements"
tags: ["monitoring", "performance", "pg_stat_statements", "diagnostics", "tuning"]
categories: ["postgresql"]
image: "pg-stat-statements.cover.jpg"
---

Il ticket diceva: "Il database è lento da qualche giorno, ma non sappiamo quale query sia il problema."

PostgreSQL 15 in produzione, un gestionale per un'azienda manifatturiera con circa quattrocento utenti. Il server aveva 64 GB di RAM, 16 core, dischi NVMe — hardware più che adeguato per il carico. Eppure i tempi di risposta dell'applicazione erano saliti da 200 millisecondi a 2-3 secondi, e il trend era in peggioramento.

La prima cosa che ho chiesto al DBA è stata: "Fammi vedere l'output di pg_stat_statements."

Silenzio. Poi: "Non ce l'abbiamo attivo."

Due anni di produzione. Quattrocento utenti. Nessuno strumento di diagnostica delle query installato. È come guidare di notte senza fari — finché la strada è dritta non ti accorgi di nulla, ma alla prima curva finisci nel fosso.

---

## Cosa fa pg_stat_statements

{{< glossary term="pg-stat-statements" >}}pg_stat_statements{{< /glossary >}} è un'estensione di PostgreSQL — inclusa nella distribuzione ufficiale ma non attiva di default — che tiene traccia delle statistiche di esecuzione di tutte le query SQL che passano dal server.

Per ogni query, registra:

- Quante volte è stata eseguita (`calls`)
- Quanto tempo totale ha consumato (`total_exec_time`)
- Quanto tempo in media per esecuzione (`mean_exec_time`)
- Quante righe ha restituito (`rows`)
- Quanti blocchi ha letto da disco (`shared_blks_read`) e dalla cache (`shared_blks_hit`)

Le query vengono normalizzate: i valori letterali vengono sostituiti con `$1`, `$2`, ecc. Questo significa che `SELECT * FROM users WHERE id = 42` e `SELECT * FROM users WHERE id = 99` sono la stessa query per pg_stat_statements. È esattamente quello che vuoi — ti interessa il pattern, non i singoli valori.

---

## Installazione: cinque minuti che cambiano tutto

L'installazione richiede una modifica al file `postgresql.conf` e un restart del servizio. Non c'è modo di evitare il restart — l'estensione deve essere caricata come shared library all'avvio del processo.

```ini
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

Il parametro `pg_stat_statements.max` definisce quante query distinte vengono tracciate. Il default è 5000, ma su database con molte query diverse conviene alzarlo. `pg_stat_statements.track` impostato a `all` traccia anche le query eseguite dentro funzioni PL/pgSQL — senza questo parametro, le query nelle stored procedure non vengono registrate.

Dopo il restart:

```sql
CREATE EXTENSION pg_stat_statements;
```

Da questo momento, ogni query che passa dal server viene tracciata. Non serve toccare l'applicazione, non serve modificare le query, non serve nulla. È completamente trasparente.

L'overhead? Trascurabile. Ho fatto benchmark su diversi ambienti e l'impatto è nell'ordine dell'1-2% di CPU in più. Su qualsiasi database di produzione è un costo che si ripaga al primo problema diagnosticato.

---

## Le tre query che mangiavano il server

Torniamo al cliente. Dopo il restart con l'estensione attiva, ho aspettato 24 ore per raccogliere un campione rappresentativo del carico. Poi ho lanciato la query che lancio sempre per prima:

```sql
SELECT
    substring(query, 1, 80) AS query_troncata,
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    rows,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percentuale
FROM pg_stat_statements
WHERE userid != (SELECT usesysid FROM pg_user WHERE usename = 'postgres')
ORDER BY total_exec_time DESC
LIMIT 20;
```

Questa query ordina tutte le query tracciate per tempo totale consumato e mostra la percentuale sul totale. È il punto di partenza — ti dice subito dove va il tempo del database.

Il risultato era impressionante:

| # | Query (troncata) | Calls | Total time | Mean time | % |
|---|-----------------|-------|------------|-----------|---|
| 1 | `SELECT o.*, c.name FROM orders o JOIN customers c ON...` | 847.000 | 1.240.000 ms | 1,46 ms | 42% |
| 2 | `SELECT p.*, s.qty FROM products p LEFT JOIN stock s...` | 312.000 | 680.000 ms | 2,18 ms | 23% |
| 3 | `SELECT * FROM audit_log WHERE created_at > $1 AND...` | 28.000 | 440.000 ms | 15,71 ms | 15% |

Tre query. L'80% del tempo totale del database.

La prima veniva eseguita 847.000 volte in 24 ore — circa dieci volte al secondo. Il tempo medio era basso (1,46 ms) ma il volume la rendeva la più costosa in assoluto. Mancava un indice sul campo di join della tabella `customers`.

La seconda aveva un LEFT JOIN che faceva un sequential scan sulla tabella `stock` — 2 milioni di righe, ogni volta. Un indice sulla colonna di join ha portato il mean_time da 2,18 ms a 0,12 ms.

La terza era quella che mi preoccupava di più. 15 millisecondi di media su una tabella di audit con 50 milioni di righe. La query filtrava per `created_at` e `action_type`, ma l'indice esistente era solo su `created_at`. Un indice composto `(created_at, action_type)` ha risolto il problema.

Tre indici. Venti minuti di lavoro. Il tempo medio di risposta dell'applicazione è sceso da 2,3 secondi a 180 millisecondi.

---

## Le query diagnostiche che uso sempre

Dopo anni di utilizzo, ho un set di query che lancio regolarmente. Le condivido perché sono quelle che avrei voluto avere quando ho iniziato con PostgreSQL.

### Top query per tempo totale

È la query che ho mostrato sopra. Ti dice dove va il tempo del database. La uso come primo passo in qualsiasi sessione diagnostica.

### Top query per tempo medio

```sql
SELECT
    substring(query, 1, 80) AS query_troncata,
    calls,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;
```

Questa è complementare alla prima. Trova le query singolarmente lente — quelle che magari vengono eseguite poche volte ma ciascuna impiega secondi. Il filtro `calls > 100` evita di pescare query una tantum che non sono rappresentative.

### Query con più I/O su disco

```sql
SELECT
    substring(query, 1, 80) AS query_troncata,
    calls,
    shared_blks_read AS blocchi_disco,
    shared_blks_hit AS blocchi_cache,
    round(
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2
    ) AS cache_hit_ratio
FROM pg_stat_statements
WHERE shared_blks_read > 1000
ORDER BY shared_blks_read DESC
LIMIT 20;
```

Questa è fondamentale per capire quali query stanno martellando il disco. Un `cache_hit_ratio` sotto il 90% su una query frequente è un segnale d'allarme — significa che i dati non stanno in `shared_buffers` e ogni esecuzione va a leggere dal filesystem.

### Query con il peggior rapporto righe restituite / righe lette

```sql
SELECT
    substring(query, 1, 80) AS query_troncata,
    calls,
    rows AS righe_restituite,
    shared_blks_hit + shared_blks_read AS blocchi_totali,
    round(rows::numeric / nullif(shared_blks_hit + shared_blks_read, 0), 4) AS efficienza
FROM pg_stat_statements
WHERE calls > 50
  AND (shared_blks_hit + shared_blks_read) > 0
ORDER BY efficienza ASC
LIMIT 20;
```

Questa trova le query che leggono moltissimi blocchi per restituire poche righe — il segnale classico di un sequential scan dove servirebbe un index scan. Un'efficienza vicina a zero su una query frequente è quasi sempre un indice mancante.

---

## Reset delle statistiche: quando e perché

Le statistiche di pg_stat_statements sono cumulative dall'ultimo reset. Se il server è in piedi da sei mesi, stai guardando la media di sei mesi — che potrebbe nascondere un problema recente.

```sql
SELECT pg_stat_statements_reset();
```

Quando fare il reset? Dipende dalla situazione:

- **Dopo un deploy applicativo**: le query cambiano, i vecchi dati non servono più
- **Dopo un intervento di tuning**: vuoi vedere l'effetto degli indici creati, non la media con il "prima"
- **Periodicamente**: alcuni team fanno un reset settimanale o mensile e salvano i dati in una tabella storica prima del reset

Un approccio che uso spesso è salvare uno snapshot prima del reset:

```sql
CREATE TABLE pgss_snapshot AS
SELECT now() AS snapshot_time, *
FROM pg_stat_statements;

SELECT pg_stat_statements_reset();
```

Così hai lo storico e le statistiche fresche.

---

## pg_stat_statements + EXPLAIN: il workflow completo

pg_stat_statements ti dice *quale* query è il problema. EXPLAIN ti dice *perché* è un problema. Usarli insieme è il workflow diagnostico più potente che PostgreSQL offre.

Il processo che seguo è sempre lo stesso:

1. **Identifico le top query** con pg_stat_statements (per tempo totale, per tempo medio, o per I/O)
2. **Copio la query normalizzata** e sostituisco i `$1`, `$2` con valori reali
3. **Lancio EXPLAIN (ANALYZE, BUFFERS)** per vedere il piano di esecuzione
4. **Cerco i segnali d'allarme**: sequential scan su tabelle grandi, nested loop con molte righe, sort su disco
5. **Intervengo**: creo un indice, riscrivo la query, aggiorno le statistiche con ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > '2026-01-01';
```

La cosa importante è il ciclo: dopo l'intervento, fai un reset di pg_stat_statements, aspetti qualche ora, e verifichi che la query sia effettivamente migliorata nei numeri reali — non solo nell'EXPLAIN.

---

## Perché non è attivo di default

Una domanda che mi fanno spesso: se pg_stat_statements è così utile, perché PostgreSQL non lo attiva di default?

La risposta è filosofica più che tecnica. PostgreSQL ha una cultura di minimalismo — il core fa il database, tutto il resto è estensione. L'overhead di pg_stat_statements è trascurabile, ma il progetto preferisce non imporre nulla. È lo stesso motivo per cui `shared_buffers` ha un default di 128 MB — un valore ridicolo per qualsiasi produzione, ma il progetto non vuole presumere quanto hardware hai.

La conseguenza pratica è che ogni installazione PostgreSQL andrebbe configurata esplicitamente. E pg_stat_statements dovrebbe essere la prima riga della checklist post-installazione — prima di tuning di shared_buffers, prima di configurare l'autovacuum, prima di tutto il resto.

Senza pg_stat_statements stai volando alla cieca. Puoi fare tuning quanto vuoi, ma stai indovinando dove intervenire.

---

## Il giorno dopo

Il giorno dopo aver creato i tre indici, ho controllato di nuovo pg_stat_statements. La distribuzione del carico era cambiata completamente. Le tre query che prima consumavano l'80% del tempo ora erano al 12% — e la query più costosa era diventata un report che girava una volta al giorno e che nessuno si era mai lamentato fosse lento.

Il DBA mi ha chiesto: "Ma perché nessuno ci aveva detto di installare questa estensione?"

La risposta è che pg_stat_statements non è un segreto. È nella documentazione ufficiale, è in ogni tutorial di performance tuning, è raccomandata da ogni DBA PostgreSQL che conosco. Ma se non la installi, non sai cosa non sai. E se non sai cosa non sai, tutto sembra funzionare — finché non funziona più.

Cinque minuti di installazione. Venti minuti di analisi. Tre indici. Un database che è passato da "lento da qualche giorno" a "il più veloce che abbiamo mai avuto" — che poi significa semplicemente "veloce come avrebbe dovuto essere dall'inizio".

------------------------------------------------------------------------

## Glossario

**[pg_stat_statements](/it/glossary/pg-stat-statements/)** — Estensione PostgreSQL che raccoglie statistiche di esecuzione per tutte le query SQL: tempi, conteggi, righe restituite e blocchi letti. Strumento fondamentale per la diagnostica delle performance.

**[shared_buffers](/it/glossary/shared-buffers/)** — Area di memoria condivisa di PostgreSQL che funge da cache per i blocchi dati letti dal disco. Il parametro più importante per il tuning della memoria, con un default di 128 MB quasi sempre inadeguato per la produzione.

**[Execution Plan](/it/glossary/execution-plan/)** — Sequenza di operazioni (scan, join, sort) che il database sceglie per risolvere una query SQL. Si visualizza con EXPLAIN e EXPLAIN ANALYZE.

**[Sequential Scan](/it/glossary/sequential-scan/)** — Operazione di lettura in cui PostgreSQL legge tutti i blocchi di una tabella dall'inizio alla fine senza utilizzare indici. Efficiente su tabelle piccole, problematica su tabelle grandi quando serve solo un sottoinsieme delle righe.

**[ANALYZE](/it/glossary/postgresql-analyze/)** — Comando PostgreSQL che raccoglie statistiche sulla distribuzione dei dati nelle tabelle, usate dall'optimizer per scegliere il piano di esecuzione.
