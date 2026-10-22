---
title: "SPM Baseline"
description: "SQL Plan Management baseline: meccanismo Oracle che congela un piano di esecuzione approvato, proteggendo le query da regressioni dopo upgrade o modifiche statistiche."
translationKey: "glossary_spm_baseline"
aka: "SQL Plan Management Baseline"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

La SPM Baseline è la funzionalità di Oracle SQL Plan Management che permette di ancorare un piano di esecuzione specifico a una query, rendendolo l'unico piano accettabile per il Cost-Based Optimizer (CBO). Anche se il CBO scopre un piano alternativo con costo stimato inferiore, non lo userà finché non viene esplicitamente accettato come baseline.

## Come funziona

Ogni piano viene identificato da un `SQL_HANDLE` (legato al testo della query) e un `PLAN_NAME` (legato al piano specifico). Oracle mantiene una SQL Plan History: i piani nuovi entrano in history ma non diventano automaticamente baseline. Solo i piani marcati come `ACCEPTED` vengono usati a runtime.

```sql
-- Carica una baseline dal cursor cache per una query specifica
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/

-- Verifica le baseline attive
SELECT sql_handle, plan_name, accepted, enabled, fixed
FROM   dba_sql_plan_baselines
WHERE  sql_text LIKE '%nome_tabella%';
```

Il flag `FIXED = YES` blocca ulteriormente il piano: il CBO non può nemmeno considerare alternative, indipendentemente da nuove statistiche o hint.

## Quando si usa

Lo scenario più comune è l'upgrade di database (es. da 11g R2 a 19c): i piani validati in staging vengono catturati e caricati come baseline prima del go-live in produzione, così il CBO del nuovo motore non può introdurre regressioni. È utile anche dopo un aggiornamento massivo di statistiche o una modifica strutturale (aggiunta di indice, partitioning) che potrebbe destabilizzare query critiche.

Il limite principale è la manutenzione: le baseline vanno riviste periodicamente. Un piano congelato su una tabella che cresce di un ordine di grandezza può diventare subottimale nel tempo.
