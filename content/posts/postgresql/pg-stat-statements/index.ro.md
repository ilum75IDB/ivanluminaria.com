---
title: "pg_stat_statements: primul lucru de instalat pe orice PostgreSQL"
description: "Un PostgreSQL în producție de doi ani fără pg_stat_statements. Când l-am activat, trei query-uri consumau 80% din resurse — fiecare se rezolva cu un singur index. Cum să instalezi, să interoghezi și să citești rezultatele celei mai importante extensii de diagnosticare PostgreSQL."
date: "2026-04-21T08:03:00+01:00"
draft: false
translationKey: "pg_stat_statements"
tags: ["monitoring", "performance", "pg_stat_statements", "diagnostics", "tuning"]
categories: ["postgresql"]
image: "pg-stat-statements.cover.jpg"
---

Ticket-ul spunea: "Baza de date e lentă de câteva zile, dar nu știm care query e problema."

PostgreSQL 15 în producție, un gestional pentru o companie din sectorul manufacturier cu aproximativ patru sute de utilizatori. Serverul avea 64 GB de RAM, 16 core-uri, discuri NVMe — hardware mai mult decât adecvat pentru sarcină. Totuși, timpii de răspuns ai aplicației crescuseră de la 200 de milisecunde la 2-3 secunde, iar trendul era în agravare.

Primul lucru pe care l-am întrebat pe DBA a fost: "Arată-mi output-ul de la pg_stat_statements."

Liniște. Apoi: "Nu-l avem activat."

Doi ani de producție. Patru sute de utilizatori. Niciun instrument de diagnosticare a query-urilor instalat. E ca și cum ai conduce noaptea fără faruri — cât timp drumul e drept nu observi nimic, dar la prima curbă ajungi în șanț.

---

## Ce face pg_stat_statements

{{< glossary term="pg-stat-statements" >}}pg_stat_statements{{< /glossary >}} este o extensie PostgreSQL — inclusă în distribuția oficială dar neactivă implicit — care ține evidența statisticilor de execuție pentru toate query-urile SQL care trec prin server.

Pentru fiecare query, înregistrează:

- De câte ori a fost executată (`calls`)
- Cât timp total a consumat (`total_exec_time`)
- Cât timp în medie per execuție (`mean_exec_time`)
- Câte rânduri a returnat (`rows`)
- Câte blocuri a citit de pe disc (`shared_blks_read`) și din cache (`shared_blks_hit`)

Query-urile sunt normalizate: valorile literale sunt înlocuite cu `$1`, `$2`, etc. Asta înseamnă că `SELECT * FROM users WHERE id = 42` și `SELECT * FROM users WHERE id = 99` sunt același query pentru pg_stat_statements. E exact ce vrei — te interesează pattern-ul, nu valorile individuale.

---

## Instalare: cinci minute care schimbă totul

Instalarea necesită o modificare în `postgresql.conf` și un restart al serviciului. Nu există modalitate de a evita restart-ul — extensia trebuie încărcată ca shared library la pornirea procesului.

```ini
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

Parametrul `pg_stat_statements.max` definește câte query-uri distincte sunt urmărite. Valoarea implicită este 5000, dar pe baze de date cu multe query-uri diferite merită crescut. `pg_stat_statements.track` setat pe `all` urmărește și query-urile executate în funcții PL/pgSQL — fără acest parametru, query-urile din procedurile stocate nu sunt înregistrate.

După restart:

```sql
CREATE EXTENSION pg_stat_statements;
```

Din acest moment, fiecare query care trece prin server este urmărită. Nu trebuie să atingi aplicația, nu trebuie să modifici query-uri, nimic. Este complet transparent.

Overhead-ul? Neglijabil. Am făcut benchmark-uri pe diverse medii și impactul este în ordinul a 1-2% CPU în plus. Pe orice bază de date de producție, este un cost care se recuperează la prima problemă diagnosticată.

---

## Cele trei query-uri care mâncau serverul

Să ne întoarcem la client. După restart-ul cu extensia activă, am așteptat 24 de ore pentru a colecta un eșantion reprezentativ al sarcinii. Apoi am lansat query-ul pe care îl lansez întotdeauna primul:

```sql
SELECT
    substring(query, 1, 80) AS query_trunchiat,
    calls,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    rows,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS procent
FROM pg_stat_statements
WHERE userid != (SELECT usesysid FROM pg_user WHERE usename = 'postgres')
ORDER BY total_exec_time DESC
LIMIT 20;
```

Acest query sortează toate query-urile urmărite după timpul total consumat și arată procentul din total. E punctul de pornire — îți spune imediat unde se duce timpul bazei de date.

Rezultatul era impresionant:

| # | Query (trunchiat) | Calls | Total time | Mean time | % |
|---|------------------|-------|------------|-----------|---|
| 1 | `SELECT o.*, c.name FROM orders o JOIN customers c ON...` | 847.000 | 1.240.000 ms | 1,46 ms | 42% |
| 2 | `SELECT p.*, s.qty FROM products p LEFT JOIN stock s...` | 312.000 | 680.000 ms | 2,18 ms | 23% |
| 3 | `SELECT * FROM audit_log WHERE created_at > $1 AND...` | 28.000 | 440.000 ms | 15,71 ms | 15% |

Trei query-uri. 80% din timpul total al bazei de date.

Primul se executa de 847.000 de ori în 24 de ore — aproximativ zece ori pe secundă. Timpul mediu era mic (1,46 ms) dar volumul îl făcea cel mai costisitor în termeni absoluți. Lipsea un index pe coloana de join a tabelei `customers`.

Al doilea avea un LEFT JOIN care făcea un sequential scan pe tabela `stock` — 2 milioane de rânduri, de fiecare dată. Un index pe coloana de join a adus mean_time de la 2,18 ms la 0,12 ms.

Al treilea era cel care mă îngrijora cel mai mult. 15 milisecunde în medie pe o tabelă de audit cu 50 de milioane de rânduri. Query-ul filtra după `created_at` și `action_type`, dar indexul existent era doar pe `created_at`. Un index compus `(created_at, action_type)` a rezolvat problema.

Trei indexuri. Douăzeci de minute de lucru. Timpul mediu de răspuns al aplicației a scăzut de la 2,3 secunde la 180 de milisecunde.

---

## Query-urile diagnostice pe care le folosesc mereu

După ani de utilizare, am un set de query-uri pe care le lansez regulat. Le împărtășesc pentru că sunt cele pe care mi-aș fi dorit să le am când am început cu PostgreSQL.

### Top query-uri după timp total

E query-ul pe care l-am arătat mai sus. Îți spune unde se duce timpul bazei de date. Îl folosesc ca prim pas în orice sesiune diagnostică.

### Top query-uri după timp mediu

```sql
SELECT
    substring(query, 1, 80) AS query_trunchiat,
    calls,
    round(mean_exec_time::numeric, 2) AS mean_time_ms,
    round(total_exec_time::numeric, 2) AS total_time_ms,
    rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;
```

Acesta este complementar primului. Găsește query-urile individual lente — cele care poate se execută de puține ori dar fiecare durează secunde. Filtrul `calls > 100` evită să prindă query-uri punctuale care nu sunt reprezentative.

### Query-uri cu cel mai mult I/O pe disc

```sql
SELECT
    substring(query, 1, 80) AS query_trunchiat,
    calls,
    shared_blks_read AS blocuri_disc,
    shared_blks_hit AS blocuri_cache,
    round(
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 2
    ) AS cache_hit_ratio
FROM pg_stat_statements
WHERE shared_blks_read > 1000
ORDER BY shared_blks_read DESC
LIMIT 20;
```

Acesta este fundamental pentru a înțelege care query-uri bat discul. Un `cache_hit_ratio` sub 90% pe un query frecvent este un semnal de alarmă — înseamnă că datele nu încap în `shared_buffers` și fiecare execuție citește din filesystem.

### Query-uri cu cel mai prost raport rânduri returnate / blocuri citite

```sql
SELECT
    substring(query, 1, 80) AS query_trunchiat,
    calls,
    rows AS randuri_returnate,
    shared_blks_hit + shared_blks_read AS blocuri_totale,
    round(rows::numeric / nullif(shared_blks_hit + shared_blks_read, 0), 4) AS eficienta
FROM pg_stat_statements
WHERE calls > 50
  AND (shared_blks_hit + shared_blks_read) > 0
ORDER BY eficienta ASC
LIMIT 20;
```

Acesta găsește query-urile care citesc foarte multe blocuri pentru a returna puține rânduri — semnalul clasic al unui sequential scan unde ar trebui un index scan. O eficiență aproape de zero pe un query frecvent este aproape întotdeauna un index lipsă.

---

## Resetarea statisticilor: când și de ce

Statisticile pg_stat_statements sunt cumulative de la ultimul reset. Dacă serverul e pornit de șase luni, te uiți la media pe șase luni — care ar putea ascunde o problemă recentă.

```sql
SELECT pg_stat_statements_reset();
```

Când să faci reset? Depinde de situație:

- **După un deploy aplicativ**: query-urile se schimbă, datele vechi nu mai servesc
- **După o intervenție de tuning**: vrei să vezi efectul indexurilor create, nu media cu "înainte"
- **Periodic**: unele echipe fac un reset săptămânal sau lunar și salvează datele într-o tabelă istorică înainte de reset

O abordare pe care o folosesc frecvent este să salvez un snapshot înainte de reset:

```sql
CREATE TABLE pgss_snapshot AS
SELECT now() AS snapshot_time, *
FROM pg_stat_statements;

SELECT pg_stat_statements_reset();
```

Astfel ai istoricul și statisticile proaspete.

---

## pg_stat_statements + EXPLAIN: workflow-ul complet

pg_stat_statements îți spune *care* query e problema. EXPLAIN îți spune *de ce* e problemă. Să le folosești împreună este cel mai puternic workflow diagnostic pe care îl oferă PostgreSQL.

Procesul pe care îl urmez este mereu același:

1. **Identific top query-urile** cu pg_stat_statements (după timp total, timp mediu sau I/O)
2. **Copiez query-ul normalizat** și înlocuiesc `$1`, `$2` cu valori reale
3. **Lansez EXPLAIN (ANALYZE, BUFFERS)** pentru a vedea planul de execuție
4. **Caut semnalele de alarmă**: sequential scan pe tabele mari, nested loop cu multe rânduri, sort pe disc
5. **Intervin**: creez un index, rescriu query-ul, actualizez statisticile cu ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > '2026-01-01';
```

Lucrul important este ciclul: după intervenție, faci reset la pg_stat_statements, aștepți câteva ore și verifici că query-ul s-a îmbunătățit efectiv în numerele reale — nu doar în EXPLAIN.

---

## De ce nu e activat implicit

O întrebare pe care o primesc des: dacă pg_stat_statements e atât de util, de ce PostgreSQL nu îl activează implicit?

Răspunsul este mai degrabă filozofic decât tehnic. PostgreSQL are o cultură a minimalismului — core-ul face baza de date, tot restul e extensie. Overhead-ul pg_stat_statements este neglijabil, dar proiectul preferă să nu impună nimic. E același motiv pentru care `shared_buffers` are implicit 128 MB — o valoare ridicolă pentru orice producție, dar proiectul nu vrea să presupună cât hardware ai.

Consecința practică este că fiecare instalare PostgreSQL ar trebui configurată explicit. Iar pg_stat_statements ar trebui să fie prima linie din checklist-ul post-instalare — înainte de tuning-ul shared_buffers, înainte de configurarea autovacuum-ului, înainte de orice altceva.

Fără pg_stat_statements zbori pe orbește. Poți face tuning cât vrei, dar ghicești unde să intervii.

---

## Ziua următoare

A doua zi după crearea celor trei indexuri, am verificat din nou pg_stat_statements. Distribuția sarcinii se schimbase complet. Cele trei query-uri care consumau 80% din timp erau acum la 12% — iar cel mai costisitor query devenise un raport care rula o dată pe zi și de care nimeni nu se plânsese vreodată.

DBA-ul m-a întrebat: "Dar de ce nu ne-a spus nimeni să instalăm această extensie?"

Răspunsul este că pg_stat_statements nu e un secret. E în documentația oficială, e în fiecare tutorial de performance tuning, e recomandat de fiecare DBA PostgreSQL pe care îl cunosc. Dar dacă nu o instalezi, nu știi ce nu știi. Și dacă nu știi ce nu știi, totul pare să funcționeze — până când nu mai funcționează.

Cinci minute de instalare. Douăzeci de minute de analiză. Trei indexuri. O bază de date care a trecut de la "lentă de câteva zile" la "cea mai rapidă pe care am avut-o vreodată" — ceea ce de fapt înseamnă pur și simplu "la fel de rapidă cum ar fi trebuit să fie de la început."

------------------------------------------------------------------------

## Glosar

**[pg_stat_statements](/ro/glossary/pg-stat-statements/)** — Extensie PostgreSQL care colectează statistici de execuție pentru toate query-urile SQL: timpi, contoare, rânduri returnate și blocuri citite. Instrument fundamental pentru diagnosticarea performanței.

**[shared_buffers](/ro/glossary/shared-buffers/)** — Zona de memorie partajată a PostgreSQL care servește drept cache pentru blocurile de date citite de pe disc. Cel mai important parametru pentru tuning-ul memoriei, cu o valoare implicită de 128 MB aproape întotdeauna inadecvată pentru producție.

**[Execution Plan](/ro/glossary/execution-plan/)** — Secvența de operații (scan, join, sort) pe care baza de date o alege pentru a rezolva un query SQL. Se vizualizează cu EXPLAIN și EXPLAIN ANALYZE.

**[Sequential Scan](/ro/glossary/sequential-scan/)** — Operație de citire în care PostgreSQL citește toate blocurile unei tabele de la început până la sfârșit fără a folosi indexuri. Eficientă pe tabele mici, problematică pe tabele mari când e nevoie doar de un subset de rânduri.

**[ANALYZE](/ro/glossary/postgresql-analyze/)** — Comandă PostgreSQL care colectează statistici despre distribuția datelor în tabele, folosite de optimizer pentru a alege planul de execuție.
