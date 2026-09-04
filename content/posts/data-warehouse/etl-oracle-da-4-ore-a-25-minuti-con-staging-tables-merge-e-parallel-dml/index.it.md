---
categories:
- data-warehouse
date: '2026-09-01'
description: 'Un ETL notturno su DWH Oracle: 15 milioni di righe, finestra batch in
  esaurimento. Diagnosi, riscrittura con staging tables, MERGE e parallel DML. Numeri
  prima e dopo.'
draft: false
image: etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml.cover.jpg
seoTitle: 'ETL Oracle: da 4 ore a 25 minuti con bulk loading e MERGE'
tags:
- etl
- oracle
- bulk-loading
- data-warehouse
- performance
title: 'ETL Oracle: da 4 ore a 25 minuti con staging tables, MERGE e parallel DML'
translationKey: etl_oracle_da_4_ore_a_25_minuti_con_staging_tables_merge_e_parallel_dml
webo_generated_at: 2026-08-12
webo_status: scheduled
---

## La finestra che si chiudeva

Il DBA del cliente ci aveva mandato un messaggio laconico: "Il batch di ieri notte ha finito alle 7:12. I report delle 7:00 erano vuoti."

Non era la prima volta. Da qualche settimana il caricamento notturno stava slittando — prima 3 ore e mezza, poi quasi 4, poi oltre. La finestra batch era fissata tra le 23:00 e le 6:30, e il sistema stava iniziando a sforare regolarmente. Il giorno dopo ci siamo seduti davanti ai log con il DBA del cliente e abbiamo cominciato a guardare cosa stava succedendo davvero.

Il contesto: un Data Warehouse Oracle 19c, un processo ETL legacy scritto in PL/SQL, 15 milioni di righe da caricare ogni notte da sorgenti operative. Il volume non era cambiato in modo significativo rispetto all'anno precedente — era cresciuto del 12%, niente di drammatico. La lentezza non era un problema di scala: era un problema di come il codice era scritto.

## Quello che i log raccontavano

Il primo strumento che abbiamo usato è stato AWR [1]. Un report AWR sulla finestra notturna mostrava subito dove andava il tempo: il top SQL per elapsed time era un blocco PL/SQL con un cursore che iterava riga per riga su 15 milioni di record.

```sql
-- pattern originale (semplificato) — il problema era esattamente questo
FOR rec IN (SELECT * FROM stg_source_data WHERE process_flag = 'N') LOOP
    -- lookup su tabella di riferimento senza indice
    SELECT dim_id INTO v_dim_id
    FROM dim_customer
    WHERE ext_code = rec.customer_code;

    INSERT INTO fact_sales (
        dim_customer_id, sale_date, amount, product_id
    ) VALUES (
        v_dim_id, rec.sale_date, rec.amount, rec.product_id
    );

    v_count := v_count + 1;
    IF MOD(v_count, 100) = 0 THEN
        COMMIT;
    END IF;
END LOOP;
```

Tre righe di codice, tre cause di lentezza. Andiamo per ordine.

## Le quattro cause di un ETL che non ce la fa

**1. INSERT riga per riga (row-by-row = slow-by-slow)**

È una delle frasi più citate nei corsi Oracle, ma continua a comparire in produzione. Ogni `INSERT` singolo genera un round-trip verso il buffer cache, aggiorna i segmenti di undo, scrive nel redo log. Moltiplicato per 15 milioni di righe, il costo di contesto per ogni singola operazione diventa dominante rispetto al costo del dato stesso.

Il confronto che abbiamo fatto internamente: un `INSERT ... SELECT` bulk su 15 milioni di righe impiega una frazione del tempo rispetto a 15 milioni di `INSERT` singoli, anche a parità di dati. Non è una questione di IO — è una questione di overhead per operazione.

**2. Lookup senza indice su `dim_customer`**

La tabella `dim_customer` aveva circa 2,8 milioni di righe. La colonna `ext_code` — quella usata per il join con la sorgente — non aveva nessun indice. Ogni lookup era un full table scan da 2,8 milioni di righe, ripetuto 15 milioni di volte.

AWR mostrava `dim_customer` come la tabella con il maggior numero di logical reads nell'intera finestra notturna. Non era un caso.

**3. COMMIT ogni 100 righe**

Il COMMIT frequente è spesso introdotto con buone intenzioni: "se qualcosa va storto, non perdiamo tutto". In realtà, su Oracle, ogni COMMIT ha un costo non banale: flush del redo log buffer, aggiornamento degli SCN, sincronizzazione con i processi di background. Farlo 150.000 volte per notte (15M / 100) aggiunge un overhead misurabile e, soprattutto, impedisce al database di ottimizzare le operazioni in batch.

**4. Nessun parallelismo**

Il processo era completamente seriale: un singolo processo PL/SQL, un cursore, un loop. Oracle 19c su quel server aveva 16 core disponibili, ma il caricamento ne usava uno solo per tutta la notte.

## La riscrittura: staging, MERGE, bulk e parallel

La strategia che abbiamo adottato con il team si articolava in quattro mosse, nell'ordine in cui le abbiamo implementate.

### Staging table con bulk load

Il primo passo è stato separare il caricamento dalla trasformazione. I dati dalla sorgente vengono prima caricati in una staging table con un `INSERT /*+ APPEND */ ... SELECT` — una singola operazione bulk che bypassa il buffer cache e scrive direttamente nei datafile (direct path insert) [2].

```sql
-- caricamento staging: direct path insert, nologging
INSERT /*+ APPEND PARALLEL(stg_sales_load, 8) */ INTO stg_sales_load
    NOLOGGING
SELECT
    s.customer_code,
    s.sale_date,
    s.amount,
    s.product_id
FROM source_sales_ext s  -- external table o db link
WHERE s.load_date = TRUNC(SYSDATE);

COMMIT;  -- un solo commit dopo il bulk
```

L'hint `APPEND` attiva il direct path insert. `NOLOGGING` riduce la scrittura sul redo log (accettabile per una staging table ricreata ogni notte). `PARALLEL` distribuisce il lavoro su 8 processi paralleli.

### Indice su `dim_customer.ext_code`

Semplice, ma necessario. Prima di procedere con qualsiasi trasformazione:

```sql
CREATE INDEX idx_dim_customer_ext_code
    ON dim_customer (ext_code)
    PARALLEL 4
    NOLOGGING;
```

Dopo la creazione, i lookup da 2,8 milioni di righe sono diventati index range scan su una colonna con alta selettività. Il costo per lookup è crollato.

### MERGE invece di INSERT + UPDATE separati

Il processo originale aveva anche una logica di "upsert" implicita: se la riga esisteva già in `fact_sales` (per riprocessamenti parziali), andava aggiornata; altrimenti inserita. Il codice originale gestiva questo con un `SELECT COUNT(*)` prima di ogni `INSERT`, aggiungendo un ulteriore round-trip per riga.

La riscrittura usa `MERGE` [3]:

```sql
MERGE /*+ PARALLEL(f, 8) */ INTO fact_sales f
USING (
    SELECT
        dc.dim_id AS dim_customer_id,
        stg.sale_date,
        stg.amount,
        stg.product_id
    FROM stg_sales_load stg
    JOIN dim_customer dc ON dc.ext_code = stg.customer_code
) src
ON (
    f.dim_customer_id = src.dim_customer_id
    AND f.sale_date    = src.sale_date
    AND f.product_id   = src.product_id
)
WHEN MATCHED THEN
    UPDATE SET f.amount = src.amount
WHEN NOT MATCHED THEN
    INSERT (dim_customer_id, sale_date, amount, product_id)
    VALUES (src.dim_customer_id, src.sale_date, src.amount, src.product_id);

COMMIT;  -- un solo commit per tutto il MERGE
```

Un'operazione sola, un commit solo, il join con `dim_customer` eseguito una volta sola sull'intero dataset invece di 15 milioni di volte.

### Parallel DML abilitato a livello di sessione

Per far funzionare il parallelismo sul `MERGE`, occorre abilitarlo esplicitamente [4]:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Senza questa istruzione, gli hint `PARALLEL` sulle operazioni DML vengono ignorati silenziosamente — un dettaglio che ha fatto perdere tempo anche a noi la prima volta che abbiamo testato la riscrittura e non vedevamo miglioramenti significativi.

## I numeri, prima e dopo

Abbiamo eseguito tre run di test su un ambiente di staging con un dataset reale anonimizzato (stessa cardinalità, stessa distribuzione dei valori).

| Metrica | Prima | Dopo |
|---|---|---|
| Tempo totale ETL | 4h 03m | 24m 38s |
| Logical reads (AWR) | ~2,1 miliardi | ~48 milioni |
| COMMIT totali | ~150.000 | 2 (staging + MERGE) |
| Processi paralleli attivi | 1 | 8 |
| Redo generato | ~18 GB | ~3,2 GB |

Il redo generato è sceso anche grazie al `NOLOGGING` sulla staging table — che però va usato con consapevolezza: una staging table `NOLOGGING` non è recuperabile da un backup incrementale preso durante il caricamento. Nel nostro caso era accettabile perché la staging viene ricreata da zero ogni notte dalla sorgente.

Il caricamento ora finisce alle 00:24. La finestra batch è di nuovo abbondante.

## Quello che vale la pena portarsi a casa

Qualche settimana dopo la messa in produzione, il DBA del cliente ci ha mandato un altro messaggio — questa volta meno laconico: "Funziona. Grazie."

Quello che abbiamo imparato (o meglio, confermato) in questo progetto non è nuovo, ma vale la pena scriverlo esplicitamente perché continua a presentarsi:

**Il row-by-row è il killer silenzioso degli ETL legacy.** Non è ovvio finché non si guarda AWR o un trace 10046. Il codice sembra ragionevole — un loop, un insert, un commit. Il problema è che "ragionevole" non significa "efficiente" quando si scala a milioni di righe.

**Il COMMIT frequente non protegge: rallenta.** Se il processo deve essere riprendibile in caso di errore, la strategia giusta è la staging table con un flag di stato — non il commit ogni N righe sulla tabella di destinazione.

**Il parallelismo Oracle richiede configurazione esplicita.** `ALTER SESSION ENABLE PARALLEL DML` non è opzionale se si vogliono operazioni DML parallele. E i gradi di parallelismo vanno calibrati sul server reale, non scelti a caso.

**Il MERGE è sottoutilizzato.** Molti ETL legacy gestiscono l'upsert con SELECT + INSERT/UPDATE separati. Il MERGE fa la stessa cosa in un'operazione sola, con un solo accesso alla tabella di destinazione.

Il pattern — staging table → trasformazione con join indicizzati → MERGE bulk con parallel DML → commit singolo — è riutilizzabile su qualsiasi ETL Oracle con caratteristiche simili. Non è una soluzione magica: richiede di capire il profilo del dato (cardinalità, distribuzione, frequenza di aggiornamento) e di testare i gradi di parallelismo sull'hardware reale. Ma come punto di partenza per una riscrittura, funziona.

## Fonti ufficiali

1. Oracle Database — [Automatic Workload Repository (AWR)](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/gathering-database-statistics.html)
2. Oracle Database — [Direct Path INSERT](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/INSERT.html#GUID-903F8043-0254-4EE9-ACC1-CB8AC0AF3423)
3. Oracle Database SQL Language Reference 19c — [MERGE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/MERGE.html)
4. Oracle Database — [Parallel DML](https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/using-parallel-dml.html)

## Glossario
- **[AWR](/it/glossary/awr/)** (Oracle Automatic Workload Repository) — Repository di snapshot periodici di metriche di workload Oracle. Base per i report AWR e per ADDM. Fondamentale per diagnosticare colli di bottiglia su finestre temporali specifiche come una notte di batch.

- **[Direct Path Insert](/it/glossary/direct-path-insert/)** — Modalità di INSERT Oracle (attivata dall'hint `APPEND`) che bypassa il buffer cache e scrive direttamente nei datafile. Riduce drasticamente il costo di caricamento bulk ma richiede attenzione alla strategia di backup e recovery.

- **[MERGE](/it/glossary/merge/)** (SQL) — Istruzione SQL che combina INSERT e UPDATE in un'unica operazione atomica (upsert). Esegue un singolo accesso alla tabella di destinazione, eliminando il pattern SELECT + INSERT/UPDATE separati tipico degli ETL legacy.

- **[Parallel DML](/it/glossary/awr/)** (Oracle) — Esecuzione parallela di operazioni DML (INSERT, UPDATE, DELETE, MERGE) su più processi Oracle. Richiede `ALTER SESSION ENABLE PARALLEL DML` e hint espliciti. Senza l'abilitazione a livello di sessione, gli hint vengono ignorati silenziosamente.

- **[Staging table](/it/glossary/direct-path-insert/)** — Tabella temporanea usata come area di atterraggio dei dati grezzi prima della trasformazione e del caricamento nella destinazione finale. Permette di separare le fasi dell'ETL, gestire la riprendibilità e applicare trasformazioni in bulk invece che riga per riga.
