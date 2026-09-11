---
title: "Data Quality"
description: "Misura in cui i dati sono accurati, completi, coerenti, validi e tempestivi. Processo continuo di monitoraggio e remediation, non un controllo una-tantum."
translationKey: "glossary_data_quality"
aka: "Qualità del dato"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

La Data Quality misura quanto i dati di un sistema siano affidabili per supportare decisioni e analisi. Cinque dimensioni la definiscono: accuratezza, completezza, coerenza, validità e tempestività. Nessuna di esse è garantita per sempre: degradano nel tempo per effetto di integrazioni difettose, errori umani, cambi di schema o sorgenti esterne fuori controllo.

## Come funziona

Un processo di Data Quality si articola in tre fasi ricorrenti: **profiling**, **monitoring** e **remediation**.

Il profiling analizza la distribuzione dei dati per individuare anomalie strutturali (valori nulli, duplicati, formati inconsistenti). Il monitoring applica regole continue sulle pipeline — soglie di nullità, range attesi, cardinalità — e genera alert quando una metrica scende sotto la soglia accettabile. La remediation corregge i dati a monte (fix sulla sorgente) o a valle (trasformazioni di pulizia nella pipeline ETL/ELT).

```sql
-- Esempio: controllo completezza su colonna critica
SELECT
  COUNT(*) AS totale,
  COUNT(customer_id) AS non_nulli,
  ROUND(COUNT(customer_id) * 100.0 / COUNT(*), 2) AS pct_completezza
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days';
```

## Contesto operativo

Nei data warehouse la Data Quality è un prerequisito della governance: senza di essa, report e modelli ML producono output inaffidabili indipendentemente dalla qualità dell'architettura sottostante. Gli strumenti dedicati (Great Expectations, dbt tests, Soda Core) integrano i controlli direttamente nelle pipeline, bloccando i dati non conformi prima che raggiungano i layer analitici. Il trade-off principale è tra latenza e rigore: controlli più granulari aumentano la copertura ma rallentano i job di caricamento.
