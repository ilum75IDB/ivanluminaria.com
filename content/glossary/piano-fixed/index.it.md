---
title: "Piano fixed"
description: "Piano di esecuzione Oracle con attributo FIXED=YES nella SQL Plan Baseline: l'optimizer lo seleziona sempre, ignorando piani alternativi."
translationKey: "glossary_piano_fixed"
aka: "Fixed Plan (SQL Plan Baseline)"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

Un **piano fixed** è un piano di esecuzione all'interno di una SQL Plan Baseline marcato con l'attributo `FIXED = YES`. A differenza dei piani semplicemente "accettati" (`ACCEPTED = YES`), un piano fixed ha precedenza assoluta: l'optimizer Oracle lo seleziona sempre per quella SQL, anche se durante la compilazione trova piani alternativi con costo stimato inferiore.

## Come funziona

Quando l'optimizer elabora una query, controlla se esiste una SQL Plan Baseline associata alla sua SQL signature. Se nella baseline è presente almeno un piano con `FIXED = YES`, l'optimizer ignora qualsiasi altro piano — accettato o non accettato — e usa esclusivamente quello fixed.

Per marcare un piano come fixed si usa `DBMS_SPM`:

```sql
DECLARE
  v_result PLS_INTEGER;
BEGIN
  v_result := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
    sql_handle      => 'SQL_abc123def456',
    plan_name       => 'SQL_PLAN_abc123def456_1',
    attribute_name  => 'fixed',
    attribute_value => 'YES'
  );
END;
/
```

## Quando si usa

Il piano fixed è lo strumento corretto in scenari dove la stabilità del piano è più critica delle ottimizzazioni automatiche dell'optimizer:

- **Regressioni post-upgrade**: dopo un aggiornamento di Oracle o delle statistiche, si fissa il piano noto come buono per evitare che l'optimizer scelga percorsi peggiori.
- **Query critiche in produzione**: per statement con SLA stringenti, si elimina qualsiasi variabilità nel piano di esecuzione.
- **Ambienti con statistiche instabili**: tabelle con dati molto variabili possono generare piani diversi a ogni raccolta di statistiche; il piano fixed neutralizza questa variabilità.

Il limite principale è la rigidità: se i dati cambiano strutturalmente (nuovi indici, partizioni, volumi molto diversi), un piano fixed può diventare subottimale senza che l'optimizer possa intervenire. Va quindi monitorato e revisionato periodicamente.
