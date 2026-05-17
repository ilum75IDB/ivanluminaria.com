---
title: "VALIDATE / NOVALIDATE"
description: "Modalità Oracle di applicazione di un vincolo al momento della creazione o modifica: VALIDATE controlla tutte le righe esistenti, NOVALIDATE salta il controllo."
translationKey: "glossary_oracle_validate_novalidate"
aka: "Constraint validation modes (Oracle)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**`VALIDATE`** e **`NOVALIDATE`** sono le due modalità con cui Oracle Database applica un vincolo (CHECK, FK, UNIQUE, NOT NULL, e dalla 23ai anche `SQL DOMAIN`) al momento della **creazione o modifica del vincolo stesso**. La differenza riguarda solo le **righe già presenti** nella tabella: tutto quello che viene inserito o aggiornato dopo è sempre controllato dal motore.

## Come funziona

Si specifica come opzione di clausola al `CREATE TABLE`, `ALTER TABLE ADD CONSTRAINT`, `ALTER TABLE MODIFY` o `ALTER DOMAIN`. `VALIDATE` (default) fa una **scansione completa** della tabella per verificare che ogni riga rispetti il vincolo; se anche una sola viola, l'operazione fallisce con `ORA-02293`. `NOVALIDATE` salta la scansione e accetta lo stato attuale "così com'è": il vincolo è marcato come applicato in avanti, ma il dizionario dati lo segnala come **non validato** (`STATUS = ENABLED NOVALIDATE` in `DBA_CONSTRAINTS`).

## Quando si usa NOVALIDATE

Tipicamente su **tabelle molto grandi** in finestre di manutenzione strette, dove la scansione di validazione costerebbe ore di blocco. Si applica `NOVALIDATE`, si garantisce l'integrità in avanti, e si fa un cleanup successivo via script batch in background. Comune in:

- Migrazione schema su tabelle storiche da centinaia di milioni di righe
- Aggiunta di un CHECK su una colonna `status` di un fact table DWH
- Conversione di vecchi `CHECK` inline a `SQL DOMAIN` su molte tabelle (Oracle 23ai+)

## Cosa controllare dopo

Una volta che il vincolo è `ENABLED NOVALIDATE`, l'ottimizzatore **non lo usa per ottimizzare query** (es. per eliminare condizioni impossibili), perché non ha garanzia che le righe storiche lo rispettino. Per recuperare il piano ottimale, dopo aver pulito i dati storici, conviene fare un `ALTER TABLE ... ENABLE VALIDATE CONSTRAINT` che riporta il vincolo in stato pienamente valido.
