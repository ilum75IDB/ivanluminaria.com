---
title: "SPM Baseline"
description: "Baseline Oracle SQL Plan Management: îngheață un plan de execuție aprobat pentru o interogare, împiedicând optimizatorul să îl înlocuiască cu unul mai puțin eficient."
translationKey: "glossary_spm_baseline"
aka: "SQL Plan Management Baseline"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

O SPM Baseline este o construcție Oracle SQL Plan Management care ancorează un plan de execuție specific la o interogare. Odată ce un plan este marcat ca baseline acceptată, Cost-Based Optimizer (CBO) îl utilizează exclusiv — chiar dacă identifică un plan alternativ cu un cost estimat mai mic — până când alternativa respectivă este acceptată explicit.

## Cum funcționează

Fiecare plan este identificat printr-un `SQL_HANDLE` (legat de textul interogării) și un `PLAN_NAME` (legat de planul specific). Oracle menține o SQL Plan History: planurile noi intră automat în istoric, dar nu devin baseline până nu sunt acceptate explicit. Doar planurile marcate ca `ACCEPTED` sunt eligibile la runtime.

```sql
-- Încarcă o baseline din cursor cache pentru o interogare specifică
DECLARE
  l_plans PLS_INTEGER;
BEGIN
  l_plans := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
    sql_id => 'abc123xyz',
    plan_hash_value => 987654321
  );
END;
/

-- Verifică baseline-urile active
SELECT sql_handle, plan_name, accepted, enabled, fixed
FROM   dba_sql_plan_baselines
WHERE  sql_text LIKE '%nume_tabel%';
```

Setarea `FIXED = YES` adaugă un blocaj mai strict: CBO nu poate lua în considerare niciun plan alternativ, indiferent de statistici noi sau hints.

## Când se folosește

Scenariul cel mai frecvent este upgrade-ul de bază de date (ex. de la 11g R2 la 19c): planurile validate în staging sunt capturate și încărcate ca baseline înainte de go-live în producție, astfel încât noua versiune a optimizatorului să nu poată introduce regresii. Este util și după o actualizare masivă a statisticilor sau o modificare structurală (index nou, partiționare) care ar putea destabiliza interogări critice.

Principalul dezavantaj este costul de întreținere: baseline-urile trebuie revizuite periodic. Un plan înghețat pe o tabelă care crește cu un ordin de mărime poate deveni suboptimal în timp.
