---
title: "Data Quality"
description: "Măsura în care datele sunt precise, complete, coerente, valide și oportune. Proces continuu de monitorizare și remediere, nu o verificare punctuală."
translationKey: "glossary_data_quality"
aka: "Calitatea datelor"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Data Quality măsoară în ce măsură datele unui sistem sunt fiabile pentru a susține decizii și analize. Cinci dimensiuni o definesc: acuratețe, completitudine, coerență, validitate și oportunitate. Niciuna dintre ele nu este garantată permanent — se degradează în timp din cauza integrărilor defectuoase, erorilor umane, modificărilor de schemă sau surselor externe necontrolate.

## Cum funcționează

Un proces de Data Quality se desfășoară în trei faze recurente: **profiling**, **monitoring** și **remediation**.

Profilingul analizează distribuția datelor pentru a detecta anomalii structurale (valori nule, duplicate, formate inconsistente). Monitoringul aplică reguli continue pe pipeline-uri — praguri de nulitate, intervale așteptate, cardinalitate — și generează alerte când o metrică scade sub nivelul acceptabil. Remedierea corectează datele la sursă (fix pe sursă) sau în aval (transformări de curățare în pipeline-ul ETL/ELT).

```sql
-- Exemplu: verificarea completitudinii pe o coloană critică
SELECT
  COUNT(*) AS total,
  COUNT(customer_id) AS non_nule,
  ROUND(COUNT(customer_id) * 100.0 / COUNT(*), 2) AS pct_completitudine
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```

## Context operațional

În data warehouse-uri, Data Quality este o condiție prealabilă a governance-ului: fără ea, rapoartele și modelele ML produc rezultate nesigure indiferent de calitatea arhitecturii subiacente. Instrumentele dedicate (Great Expectations, dbt tests, Soda Core) integrează verificările direct în pipeline-uri, blocând datele neconforme înainte să ajungă la straturile analitice. Principalul trade-off este între latență și rigoare: verificările mai granulare cresc acoperirea, dar încetinesc job-urile de încărcare.
