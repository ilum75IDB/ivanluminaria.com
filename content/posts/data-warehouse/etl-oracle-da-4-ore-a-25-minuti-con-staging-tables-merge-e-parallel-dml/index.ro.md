---
title: "Fereastra care se închidea: cum am rescris un ETL Oracle de la 4 ore la 24 de minute"
seoTitle: "ETL Oracle 19c: de la 4 ore la 24 minute cu bulk load și MERGE"
description: "Un batch nocturn care depășea fereastra de încărcare. Diagnostic AWR, rescrierea cu direct path insert, MERGE paralel și un singur COMMIT. Cifre reale."
date: 2099-12-31
draft: true
translationKey: "etl_oracle_da_4_ore_a_25_minuti_con_staging_tables_merge_e_parallel_dml"
tags: ["oracle-19c", "etl", "performance-tuning", "parallel-dml", "data-warehouse"]
categories: ["data-warehouse"]
image: "etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml.cover.jpg"
webo_status: da_tradurre
webo_generated_at: 2026-08-12
---

## Fereastra care se închidea

DBA-ul clientului ne trimisese un mesaj laconic: „Batch-ul de ieri noapte a terminat la 7:12. Rapoartele de la 7:00 erau goale."

Nu era prima dată. De câteva săptămâni, încărcarea nocturnă tot aluneca — mai întâi 3 ore și jumătate, apoi aproape 4, apoi peste. Fereastra batch era fixată între 23:00 și 6:30, iar sistemul începuse să o depășească regulat. A doua zi ne-am așezat în fața log-urilor împreună cu DBA-ul clientului și am început să vedem ce se întâmpla cu adevărat.

Contextul: un Data Warehouse Oracle 19c, un proces ETL legacy scris în PL/SQL, 15 milioane de rânduri de încărcat în fiecare noapte din surse operaționale. Volumul nu crescuse semnificativ față de anul precedent — 12%, nimic dramatic. Lentoarea nu era o problemă de scală: era o problemă legată de modul în care era scris codul.

## Ce povesteau log-urile

Primul instrument pe care l-am folosit a fost AWR [1]. Un raport AWR pe fereastra nocturnă arăta imediat unde se ducea timpul: top SQL după elapsed time era un bloc PL/SQL cu un cursor care itera rând cu rând peste 15 milioane de înregistrări.

```sql
-- pattern original (simplificat) — problema era exact aceasta
FOR rec IN (SELECT * FROM stg_source_data WHERE process_flag = 'N') LOOP
    -- lookup pe tabel de referință fără index
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

Trei rânduri de cod, trei cauze de lentoare. Să le luăm pe rând.

## Cele patru cauze ale unui ETL care nu mai ține pasul

**1. INSERT rând cu rând (row-by-row = slow-by-slow)**

E una dintre frazele cele mai citate în cursurile Oracle, dar continuă să apară în producție. Fiecare `INSERT` individual generează un round-trip către buffer cache, actualizează segmentele de undo, scrie în redo log. Înmulțit cu 15 milioane de rânduri, costul de context per operație devine dominant față de costul datei în sine.

Comparația pe care am făcut-o intern: un `INSERT ... SELECT` bulk pe 15 milioane de rânduri durează o fracțiune din timp față de 15 milioane de `INSERT`-uri individuale, chiar la volum identic de date. Nu e o chestiune de IO — e o chestiune de overhead per operație.

**2. Lookup fără index pe `dim_customer`**

Tabelul `dim_customer` avea circa 2,8 milioane de rânduri. Coloana `ext_code` — cea folosită pentru join cu sursa — nu avea niciun index. Fiecare lookup era un full table scan de 2,8 milioane de rânduri, repetat de 15 milioane de ori.

AWR arăta `dim_customer` ca tabelul cu cel mai mare număr de logical reads din întreaga fereastră nocturnă. Nu era o coincidență.

**3. COMMIT la fiecare 100 de rânduri**

COMMIT-ul frecvent e introdus adesea cu intenții bune: „dacă ceva merge prost, nu pierdem totul". În realitate, pe Oracle, fiecare COMMIT are un cost deloc neglijabil: flush al redo log buffer, actualizarea SCN-urilor, sincronizare cu procesele de background. Făcut de 150.000 de ori pe noapte (15M / 100), adaugă un overhead măsurabil și, mai ales, împiedică baza de date să optimizeze operațiile în batch.

**4. Niciun paralelism**

Procesul era complet serial: un singur proces PL/SQL, un cursor, un loop. Oracle 19c pe acel server avea 16 core disponibile, dar încărcarea folosea unul singur toată noaptea.

## Rescrierea: staging, MERGE, bulk și parallel

Strategia adoptată împreună cu echipa se articula în patru mișcări, în ordinea în care le-am implementat.

### Staging table cu bulk load

Primul pas a fost separarea încărcării de transformare. Datele din sursă sunt mai întâi încărcate într-un staging table cu un `INSERT /*+ APPEND */ ... SELECT` — o singură operație bulk care ocolește buffer cache și scrie direct în datafile-uri (direct path insert) [2].

```sql
-- încărcare staging: direct path insert, nologging
INSERT /*+ APPEND PARALLEL(stg_sales_load, 8) */ INTO stg_sales_load
    NOLOGGING
SELECT
    s.customer_code,
    s.sale_date,
    s.amount,
    s.product_id
FROM source_sales_ext s  -- external table sau db link
WHERE s.load_date = TRUNC(SYSDATE);

COMMIT;  -- un singur commit după bulk
```

Hint-ul `APPEND` activează direct path insert. `NOLOGGING` reduce scrierea în redo log (acceptabil pentru un staging table recreat în fiecare noapte). `PARALLEL` distribuie lucrul pe 8 procese paralele.

### Index pe `dim_customer.ext_code`

Simplu, dar necesar. Înainte de orice transformare:

```sql
CREATE INDEX idx_dim_customer_ext_code
    ON dim_customer (ext_code)
    PARALLEL 4
    NOLOGGING;
```

După creare, lookup-urile pe 2,8 milioane de rânduri au devenit index range scan pe o coloană cu selectivitate ridicată. Costul per lookup a scăzut dramatic.

### MERGE în loc de INSERT + UPDATE separate

Procesul original avea și o logică implicită de „upsert": dacă rândul exista deja în `fact_sales` (pentru reprelucrări parțiale), trebuia actualizat; altfel, inserat. Codul original gestiona asta cu un `SELECT COUNT(*)` înainte de fiecare `INSERT`, adăugând un round-trip suplimentar per rând.

Rescrierea folosește `MERGE` [3]:

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

COMMIT;  -- un singur commit pentru întregul MERGE
```

O singură operație, un singur commit, join-ul cu `dim_customer` executat o dată pe întregul dataset în loc de 15 milioane de ori.

### Parallel DML activat la nivel de sesiune

Pentru ca paralelismul să funcționeze pe `MERGE`, trebuie activat explicit [4]:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Fără această instrucțiune, hint-urile `PARALLEL` pe operațiile DML sunt ignorate în tăcere — un detaliu care ne-a costat timp și nouă prima dată când am testat rescrierea și nu vedeam îmbunătățiri semnificative.

## Cifrele, înainte și după

Am rulat trei teste pe un mediu de staging cu un dataset real anonimizat (aceeași cardinalitate, aceeași distribuție a valorilor).

| Metrică | Înainte | După |
|---|---|---|
| Timp total ETL | 4h 03m | 24m 38s |
| Logical reads (AWR) | ~2,1 miliarde | ~48 milioane |
| COMMIT-uri totale | ~150.000 | 2 (staging + MERGE) |
| Procese paralele active | 1 | 8 |
| Redo generat | ~18 GB | ~3,2 GB |

Redo-ul generat a scăzut și datorită `NOLOGGING` pe staging table — care trebuie folosit cu discernământ: un staging table `NOLOGGING` nu poate fi recuperat dintr-un backup incremental luat în timpul încărcării. În cazul nostru era acceptabil, pentru că staging-ul este recreat de la zero în fiecare noapte din sursă.

Încărcarea se termină acum la 00:24. Fereastra batch e din nou confortabilă.

## Ce merită dus mai departe

La câteva săptămâni după punerea în producție, DBA-ul clientului ne-a trimis un alt mesaj — de data aceasta mai puțin laconic: „Funcționează. Mulțumim."

Ce am învățat (sau mai degrabă confirmat) în acest proiect nu e nou, dar merită scris explicit pentru că tot revine:

**Row-by-row este ucigașul tăcut al ETL-urilor legacy.** Nu e evident până nu te uiți în AWR sau într-un trace 10046. Codul pare rezonabil — un loop, un insert, un commit. Situația e că „rezonabil" nu înseamnă „eficient" când scalezi la milioane de rânduri.

**COMMIT-ul frecvent nu protejează: încetinește.** Dacă procesul trebuie să poată fi reluat în caz de eroare, strategia corectă este staging table cu un flag de stare — nu commit la fiecare N rânduri pe tabelul de destinație.

**Paralelismul Oracle necesită configurare explicită.** `ALTER SESSION ENABLE PARALLEL DML` nu e opțional dacă vrei operații DML paralele. Iar gradele de paralelism trebuie calibrate pe serverul real, nu alese la întâmplare.

**MERGE este subutilizat.** Multe ETL-uri legacy gestionează upsert-ul cu SELECT + INSERT/UPDATE separate. MERGE face același lucru într-o singură operație, cu un singur acces la tabelul de destinație.

Tiparul — staging table → transformare cu join-uri indexate → MERGE bulk cu parallel DML → commit unic — este reutilizabil pe orice ETL Oracle cu caracteristici similare. Nu e o soluție magică: necesită înțelegerea profilului datei (cardinalitate, distribuție, frecvență de actualizare) și testarea gradelor de paralelism pe hardware-ul real. Dar ca punct de plecare pentru o rescriere, funcționează.

## Surse oficiale

1. Oracle Database — [Automatic Workload Repository (AWR)](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/gathering-database-statistics.html)
2. Oracle Database — [Direct Path INSERT](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/INSERT.html#GUID-903F8043-0254-4EE9-ACC1-CB8AC0AF3423)
3. Oracle Database SQL Language Reference 19c — [MERGE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/MERGE.html)
4. Oracle Database — [Parallel DML](https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/using-parallel-dml.html)

## Glosar candidat

- **AWR** (Oracle Automatic Workload Repository) — Repository de snapshot-uri periodice ale metricilor de workload Oracle. Baza pentru rapoartele AWR și pentru ADDM. Esențial pentru diagnosticarea blocajelor pe ferestre temporale specifice, cum ar fi o noapte de batch.

- **Direct Path Insert** — Modalitate de INSERT Oracle (activată prin hint-ul `APPEND`) care ocolește buffer cache și scrie direct în datafile-uri. Reduce drastic costul încărcărilor bulk, dar necesită atenție la strategia de backup și recovery.

- **MERGE** (SQL) — Instrucțiune SQL care combină INSERT și UPDATE într-o singură operație atomică (upsert). Execută un singur acces la tabelul de destinație, eliminând tiparul SELECT + INSERT/UPDATE separate specific ETL-urilor legacy.

- **Parallel DML** (Oracle) — Execuție paralelă a operațiilor DML (INSERT, UPDATE, DELETE, MERGE) pe mai multe procese Oracle. Necesită `ALTER SESSION ENABLE PARALLEL DML` și hint-uri explicite. Fără activarea la nivel de sesiune, hint-urile sunt ignorate în tăcere.

- **Staging table** — Tabel temporar folosit ca zonă de aterizare a datelor brute înainte de transformare și încărcare în destinația finală. Permite separarea fazelor ETL, gestionarea reluării și aplicarea transformărilor în bulk în loc de rând cu rând.
