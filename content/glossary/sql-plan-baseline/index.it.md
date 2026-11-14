---
title: "SQL Plan Baseline"
description: "Set di piani di esecuzione accettati per uno SQL statement, memorizzato nel repository SPM di Oracle per garantire stabilità delle performance."
translationKey: "glossary_sql_plan_baseline"
aka: "SPM Baseline, Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

Una SQL Plan Baseline è un insieme di uno o più piani di esecuzione approvati per uno specifico SQL statement, gestito dal componente Oracle **SQL Plan Management (SPM)**. Quando una baseline è attiva, l'optimizer sceglie esclusivamente tra i piani in essa contenuti, anche se durante la compilazione individua alternative apparentemente più efficienti.

## Come funziona

L'optimizer confronta il piano generato a runtime con quelli presenti nella baseline. Se il piano corrente è già accettato (`ACCEPTED = YES`), viene usato direttamente. Se è nuovo, viene aggiunto alla baseline con stato `NOT ACCEPTED` e rimane in quarantena finché un DBA — o il processo automatico di evoluzione — non lo verifica e promuove.

```sql
-- Caricamento manuale di una baseline dalla Cursor Cache
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/
```

## Quando si usa

Le baseline sono lo strumento principale per **bloccare regressioni di piano** dopo upgrade del database, raccolta di nuove statistiche o modifiche strutturali agli indici. Sono preferibili agli hint inline perché non richiedono modifiche al codice applicativo e si gestiscono interamente lato DBA. Il limite principale è che ogni baseline è legata all'`SQL_ID` esatto: variazioni nel testo della query (anche spazi o maiuscole) generano un `SQL_ID` diverso e richiedono una baseline separata.
