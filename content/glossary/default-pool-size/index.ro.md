---
title: "default_pool_size"
description: "Parametru PgBouncer care definește numărul de conexiuni reale PostgreSQL menținute pentru fiecare pereche bază de date/utilizator, esențial pentru dimensionarea pool-ului."
translationKey: "glossary_default_pool_size"
aka: null
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`default_pool_size` este un parametru fundamental în PgBouncer, un pooler de conexiuni ușor și de înaltă performanță pentru PostgreSQL. Acest parametru determină numărul maxim de conexiuni *reale* pe care PgBouncer le menține deschise către serverul PostgreSQL pentru fiecare combinație unică de bază de date și utilizator. Este esențial pentru dimensionarea corectă a pool-ului de conexiuni și pentru asigurarea unei gestionări eficiente a resurselor.

## Ce face și cum funcționează

PgBouncer acționează ca un intermediar între aplicațiile client și serverul PostgreSQL. În loc ca PostgreSQL să deschidă o nouă conexiune pentru fiecare cerere a clientului, PgBouncer menține
