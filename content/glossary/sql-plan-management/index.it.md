---
title: "SQL Plan Management (SPM)"
description: "Funzionalità Oracle che stabilizza i piani di esecuzione tramite baseline approvate, prevenendo regressioni di performance causate dall'optimizer."
translationKey: "glossary_sql_plan_management"
aka: "SPM, SQL Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

SQL Plan Management (SPM) è una funzionalità di Oracle Database che consente di controllare quali piani di esecuzione l'optimizer può effettivamente usare per una determinata query. Il meccanismo centrale è il **SQL Plan Baseline**: un repository di piani verificati e approvati, che l'optimizer consulta prima di adottare qualsiasi nuovo piano generato.

## Come funziona

Quando SPM è attivo, l'optimizer può generare piani alternativi, ma li mette in uno stato di "non verificato" (unaccepted). Un piano nuovo viene usato in produzione solo dopo essere stato accettato esplicitamente — manualmente o tramite evoluzione automatica — e solo se dimostra prestazioni migliori rispetto al baseline esistente.

```sql
-- Caricamento manuale di un piano dalla Cursor Cache nel baseline
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

Il baseline è identificato dalla coppia `SQL_HANDLE` + `PLAN_NAME` e persiste nel `SYSAUX` tablespace, indipendentemente da statistiche o parametri di sistema.

## Quando si usa

SPM è lo strumento di riferimento quando:

- un aggiornamento di statistiche, un patch dell'optimizer o un upgrade di Oracle introduce regressioni di piano su query critiche;
- si vuole congelare il comportamento di una query specifica in ambienti con SLA stringenti;
- si migra da una versione Oracle a un'altra e si vuole garantire continuità di piano durante il periodo di transizione.

Il limite principale è la gestione nel tempo: i baseline accumulati vanno revisionati periodicamente, altrimenti si rischia di bloccare ottimizzazioni legittime che l'optimizer avrebbe potuto sfruttare.
