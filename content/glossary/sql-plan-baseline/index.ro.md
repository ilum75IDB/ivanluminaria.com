---
title: "SQL Plan Baseline"
description: "Set de planuri de execuție acceptate pentru un SQL statement specific, stocat în repository-ul SPM Oracle pentru a garanta stabilitatea performanței."
translationKey: "glossary_sql_plan_baseline"
aka: "SPM Baseline, Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

O SQL Plan Baseline este o colecție de unul sau mai multe planuri de execuție aprobate pentru un SQL statement specific, gestionată de componenta Oracle **SQL Plan Management (SPM)**. Când o baseline este activă, optimizer-ul alege exclusiv dintre planurile pe care le conține, chiar dacă în timpul compilării identifică alternative aparent mai eficiente.

## Cum funcționează

La momentul parsării, optimizer-ul compară planul generat cu cele stocate în baseline. Dacă planul este deja marcat `ACCEPTED = YES`, este utilizat direct. Dacă este nou, este adăugat în baseline cu statusul `NOT ACCEPTED` și rămâne în carantină până când un DBA — sau procesul automat de evoluție a planurilor — îl verifică și îl promovează.

```sql
-- Încărcare manuală a unei baseline din Cursor Cache
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

## Când se utilizează

Baseline-urile sunt instrumentul principal pentru **blocarea regresiilor de plan** după upgrade-uri ale bazei de date, recolectarea de statistici sau modificări structurale ale indecșilor. Sunt preferabile hint-urilor inline deoarece nu necesită modificări în codul aplicației și sunt gestionate integral la nivelul DBA. Limitarea principală este că fiecare baseline este legată de un `SQL_ID` exact: orice variație în textul interogării — inclusiv spații sau majuscule — generează un `SQL_ID` diferit și necesită o baseline separată.
