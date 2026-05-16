---
title: "SQL Domain"
description: "Costrutto introdotto in Oracle Database 23ai che definisce un dominio riusabile (tipo base + CHECK + DEFAULT + annotations) come oggetto del dizionario dati."
translationKey: "glossary_oracle_sql_domain"
aka: "SQL Domain (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

Il **SQL Domain** è un costrutto introdotto in Oracle Database 23ai che permette di definire un **dominio riusabile** per una colonna: un tipo base (es. `VARCHAR2(20)`), un vincolo `CHECK`, un valore di `DEFAULT`, ed eventuali **annotations** di metadati, tutto incapsulato in un oggetto del dizionario dati che può essere riusato su molte colonne diverse.

## Come funziona

Si dichiara con `CREATE DOMAIN nome AS tipo_base ... CONSTRAINT chk_X CHECK (...) DEFAULT ... ANNOTATIONS (...)`. Una volta creato, il dominio è visibile in `DBA_DOMAINS` e può essere usato come tipo di colonna in qualsiasi `CREATE TABLE`. Oracle valida i `CHECK` del dominio ad ogni INSERT/UPDATE come farebbe con un constraint inline.

## A cosa serve

Centralizzare in un unico punto il dominio di una colonna, evitando di replicare la stessa lista di valori (o lo stesso vincolo) su decine di tabelle. Quando il set evolve, basta un `ALTER DOMAIN` e Oracle propaga il cambiamento a tutte le colonne che usano il dominio — senza dover toccare le `CREATE TABLE` né eseguire `ALTER TABLE` multipli.

## Cosa lo distingue dal DOMAIN di PostgreSQL

Il `DOMAIN` di PostgreSQL esiste da molto prima ma è più essenziale: tipo base + vincoli, niente sistema di annotations. Oracle ha aggiunto un livello di metadati (`display`, `description`, ordering ecc.) che strumenti di BI, reporting e UI generation possono leggere per generare automaticamente etichette, ordering visivo, descrizioni di campo.
