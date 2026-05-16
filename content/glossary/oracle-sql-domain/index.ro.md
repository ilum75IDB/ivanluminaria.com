---
title: "SQL Domain"
description: "Construct introdus în Oracle Database 23ai care definește un domeniu reutilizabil (tip de bază + CHECK + DEFAULT + annotations) ca obiect al dicționarului de date."
translationKey: "glossary_oracle_sql_domain"
aka: "SQL Domain (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

**SQL Domain** este un construct introdus în Oracle Database 23ai care permite definirea unui **domeniu reutilizabil** pentru o coloană: un tip de bază (ex. `VARCHAR2(20)`), o constrângere `CHECK`, o valoare `DEFAULT`, și eventuale **annotations** de metadate, totul încapsulat într-un obiect al dicționarului de date care poate fi reutilizat pe multe coloane diferite.

## Cum funcționează

Se declară cu `CREATE DOMAIN nume AS tip_de_baza ... CONSTRAINT chk_X CHECK (...) DEFAULT ... ANNOTATIONS (...)`. Odată creat, domeniul este vizibil în `DBA_DOMAINS` și poate fi folosit ca tip de coloană în orice `CREATE TABLE`. Oracle validează `CHECK`-urile domeniului la fiecare INSERT/UPDATE la fel cum ar face cu o constrângere inline.

## La ce servește

Centralizarea într-un singur punct a domeniului unei coloane, evitând replicarea aceleiași liste de valori (sau aceleiași constrângeri) în zeci de tabele. Când setul evoluează, un singur `ALTER DOMAIN` propagă schimbarea la toate coloanele care folosesc domeniul — fără a fi nevoie să atingi `CREATE TABLE`-urile sau să execuți multiple `ALTER TABLE`.

## Ce îl distinge de DOMAIN-ul PostgreSQL

`DOMAIN`-ul PostgreSQL există de mult mai mult timp dar este mai esențial: tip de bază + constrângeri, fără sistem de annotations. Oracle a adăugat un nivel de metadate (`display`, `description`, ordering etc.) pe care instrumentele de BI, raportare și UI generation îl pot citi pentru a genera automat etichete, ordering vizual, descrieri de câmp.
