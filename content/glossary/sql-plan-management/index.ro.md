---
title: "SQL Plan Management (SPM)"
description: "Funcționalitate Oracle care stabilizează planurile de execuție prin baseline-uri aprobate, prevenind regresiile de performanță cauzate de optimizer."
translationKey: "glossary_sql_plan_management"
aka: "SPM, SQL Plan Baseline"
articles:
  - "/posts/oracle/oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire"
---

SQL Plan Management (SPM) este o funcționalitate Oracle Database care oferă DBA-ilor control explicit asupra planurilor de execuție pe care optimizer-ul le poate folosi pentru o anumită instrucțiune SQL. Mecanismul central este **SQL Plan Baseline**: un repository de planuri verificate și acceptate, pe care optimizer-ul îl consultă înainte de a adopta orice plan nou generat.

## Cum funcționează

Cu SPM activ, optimizer-ul poate genera planuri alternative, însă le marchează ca neacceptate. Un plan nou intră în producție doar după o acceptare explicită — manuală sau prin evoluție automată — și numai dacă demonstrează performanțe cel puțin egale cu planul din baseline-ul existent.

```sql
-- Încărcarea manuală a unui plan din Cursor Cache în baseline
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

Fiecare intrare din baseline este identificată prin perechea `SQL_HANDLE` + `PLAN_NAME` și este stocată în tablespace-ul `SYSAUX`, persistând independent de modificările statisticilor sau ale parametrilor de sistem.

## Când se folosește

SPM este instrumentul de referință atunci când:

- o actualizare de statistici, un patch al optimizer-ului sau un upgrade Oracle introduce regresii de plan pe interogări critice;
- comportamentul unei interogări specifice trebuie înghețat în medii cu SLA-uri stricte;
- se migrează între versiuni Oracle și stabilitatea planului trebuie garantată pe durata perioadei de tranziție.

Principala limitare operațională este gestionarea ciclului de viață al baseline-urilor: baseline-urile acumulate trebuie revizuite periodic, altfel optimizările legitime pe care optimizer-ul le-ar putea exploata riscă să fie blocate pe termen nedefinit.
