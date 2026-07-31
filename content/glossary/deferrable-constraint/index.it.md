---
title: "DEFERRABLE constraint"
description: "Vincolo di integrità che può essere verificato alla fine della transazione anziché a ogni DML. Utile per operazioni multi-step in Oracle e altri RDBMS."
translationKey: "glossary_deferrable_constraint"
aka: "vincolo differibile"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un DEFERRABLE constraint è un vincolo di integrità referenziale o di dominio la cui verifica può essere posticipata al momento del COMMIT, invece di essere eseguita immediatamente dopo ogni singola istruzione DML. Questo consente di attraversare stati intermedi temporaneamente inconsistenti all'interno di una transazione, purché la consistenza sia ripristinata prima della chiusura.

## Come funziona

Un vincolo dichiarato `DEFERRABLE` può operare in due modalità:

- `INITIALLY IMMEDIATE` — verificato dopo ogni DML (comportamento default); può essere posticipato esplicitamente con `SET CONSTRAINT`.
- `INITIALLY DEFERRED` — verificato solo al COMMIT per default.

```sql
ALTER TABLE ordini
  ADD CONSTRAINT fk_cliente
  FOREIGN KEY (cliente_id) REFERENCES clienti(id)
  DEFERRABLE INITIALLY DEFERRED;

-- All'interno della transazione:
SET CONSTRAINT fk_cliente DEFERRED;
INSERT INTO ordini (id, cliente_id) VALUES (1, 999); -- cliente 999 non esiste ancora
INSERT INTO clienti (id) VALUES (999);               -- ora esiste
COMMIT;                                              -- verifica superata
```

## Quando si usa

Il caso d'uso classico è il caricamento di dati con dipendenze circolari o l'inserimento in ordine non deterministico di righe collegate da foreign key. È comune anche nella replica e nei processi ETL dove l'ordine di arrivo dei record non è garantito.

**Limite fondamentale**: un DEFERRABLE constraint non è un'Assertion. Agisce su singole righe o relazioni tra tabelle già definite nello schema, ma non può esprimere predicati arbitrari cross-tabella come `CHECK (SELECT COUNT(*) FROM ...)`. Per vincoli di questo tipo Oracle 23ai introduce le SQL Assertions native.
