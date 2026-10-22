---
title: "max_connections"
description: "Parametru PostgreSQL care stabilește numărul maxim de conexiuni simultane acceptate. Fiecare conexiune are un cost real în memorie și în planificarea proceselor OS."
translationKey: "glossary_max_connections"
aka: "max_connections (limită conexiuni PostgreSQL)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`max_connections` este parametrul din `postgresql.conf` care definește câte conexiuni client poate accepta PostgreSQL în același timp. Nu este o limită arbitrară: fiecare conexiune activă pornește un proces backend dedicat, cu un cost fix în memoria partajată și în planificarea proceselor la nivelul sistemului de operare.

## Cum funcționează

PostgreSQL folosește un model process-per-connection: fiecare client care se conectează generează un proces backend separat prin fork. `max_connections` stabilește plafonul maxim al acestor procese. Odată atins limita, serverul respinge conexiunile noi cu o eroare explicită.

```sql
-- Verificarea valorii curente
SHOW max_connections;

-- Conexiuni active în acest moment
SELECT count(*) FROM pg_stat_activity;
```

Modificarea parametrului necesită repornirea serverului, deoarece determină alocarea inițială a memoriei partajate — în special pentru tabelele de lock-uri și buffer-ele per proces.

## Context operațional

O valoare ridicată a `max_connections` nu este gratuită: fiecare slot rezervă aproximativ 5–10 MB de memorie partajată chiar și atunci când conexiunea este inactivă. La 500 de conexiuni, vorbim de câțiva gigabytes rezervați înainte ca o singură interogare să fie executată.

Modelul recomandat este să se mențină `max_connections` la un nivel scăzut (tipic 100–200 pentru workload-uri OLTP) și să se delege multiplexarea către un connection pooler precum PgBouncer în modul transaction pooling. Astfel, mii de clienți aplicativi partajează un număr redus de conexiuni reale către PostgreSQL.

## Note

Creșterea `max_connections` impune și revizuirea `work_mem` și `shared_buffers`: memoria disponibilă se împarte între toate procesele backend active. Ridicarea limitei fără a lua în calcul footprint-ul global poate duce la presiune pe memorie sau, în cazuri extreme, la un OOM kill din partea sistemului de operare.
