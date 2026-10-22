---
title: "PgBouncer"
description: "Connection pooler ușor pentru PostgreSQL care reduce costul conexiunilor menținând un pool restrâns de conexiuni reale partajate între mulți clienți."
translationKey: "glossary_pgbouncer"
aka: "PgBouncer (PostgreSQL Connection Pooler)"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

PgBouncer este un connection pooler ușor pentru PostgreSQL, scris în C cu I/O asincron. Se plasează între clienți și baza de date, menținând un pool restrâns de conexiuni reale către PostgreSQL și reutilizându-le între mulți clienți concurenți, eliminând costul de fork și autentificare pentru fiecare conexiune nouă.

## Cum funcționează

PgBouncer interceptează conexiunile primite și le mapează pe un subset de conexiuni reale deja deschise către PostgreSQL. Suportă trei moduri de pooling:

- **Session pooling**: o conexiune reală este alocată clientului pe toată durata sesiunii.
- **Transaction pooling**: conexiunea reală este returnată în pool după fiecare COMMIT sau ROLLBACK. Este modul cel mai eficient, dar incompatibil cu anumite funcționalități cu stare (prepared statements pe server, `SET LOCAL`, advisory locks).
- **Statement pooling**: eliberare după fiecare instrucțiune individuală. Rar utilizat în producție.

Configurarea minimă se realizează printr-un fișier `.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

## Când se folosește

PgBouncer este potrivit când numărul de conexiuni client depășește pragul sustenabil de PostgreSQL (tipic peste 200-300 conexiuni active), sau când sarcini de lucru fără stare precum workeri sau microservicii deschid și închid conexiuni cu frecvență ridicată. Nu înlocuiește o gestionare corectă a conexiunilor la nivelul aplicației, dar atenuează efectele acesteia sub sarcină ridicată.

În modul transaction pooling, parametri precum `server_reset_query` și gestionarea prepared statements necesită atenție specifică pentru a evita comportamente neașteptate.
