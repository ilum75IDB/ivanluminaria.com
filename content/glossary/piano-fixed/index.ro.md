---
title: "Plan fixed"
description: "Plan de execuție Oracle marcat cu FIXED=YES într-o SQL Plan Baseline: optimizatorul îl selectează întotdeauna, indiferent de planurile alternative găsite."
translationKey: "glossary_piano_fixed"
aka: "Fixed Plan (SQL Plan Baseline)"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

Un **plan fixed** este un plan de execuție stocat într-o SQL Plan Baseline și marcat cu atributul `FIXED = YES`. Spre deosebire de planurile pur și simplu acceptate (`ACCEPTED = YES`), un plan fixed are prioritate absolută: optimizatorul Oracle îl selectează întotdeauna pentru acea instrucțiune SQL, chiar dacă în timpul compilării găsește planuri alternative cu un cost estimat mai mic.

## Cum funcționează

Când optimizatorul procesează o interogare, verifică dacă există o SQL Plan Baseline asociată cu SQL signature-ul acesteia. Dacă baseline-ul conține cel puțin un plan cu `FIXED = YES`, optimizatorul ignoră orice alt plan — acceptat sau nu — și folosește exclusiv planul fixed.

Marcarea unui plan ca fixed se realizează prin `DBMS_SPM`:

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

## Când se folosește

Planul fixed este instrumentul potrivit atunci când stabilitatea planului este mai critică decât optimizările automate ale optimizatorului:

- **Regresii post-upgrade**: după o actualizare Oracle sau o reîmprospătare a statisticilor, fixarea unui plan cunoscut ca bun împiedică optimizatorul să aleagă rute mai slabe.
- **Interogări critice în producție**: pentru instrucțiuni cu SLA-uri stricte, orice variabilitate în planul de execuție este inacceptabilă.
- **Medii cu statistici instabile**: tabelele cu date foarte volatile pot genera planuri diferite după fiecare colectare de statistici; planul fixed elimină această variabilitate.

Principalul dezavantaj este rigiditatea: dacă caracteristicile datelor se schimbă semnificativ (indecși noi, partiționare, volume foarte diferite), planul fixed poate deveni suboptimal fără ca optimizatorul să poată interveni. Trebuie monitorizat și revizuit periodic.
