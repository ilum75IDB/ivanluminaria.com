---
title: "COALESCE"
description: "Funzione SQL che restituisce il primo valore non NULL da una lista di espressioni."
translationKey: "glossary_coalesce"
aka: "NVL (Oracle), IFNULL (MySQL)"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**COALESCE** è una funzione SQL standard che accetta una lista di espressioni e restituisce la prima che non è NULL. Se tutte le espressioni sono NULL, restituisce NULL.

## Sintassi

``` sql
COALESCE(espressione1, espressione2, espressione3, ...)
```

Equivale a una catena di CASE WHEN:

``` sql
CASE WHEN espressione1 IS NOT NULL THEN espressione1
     WHEN espressione2 IS NOT NULL THEN espressione2
     WHEN espressione3 IS NOT NULL THEN espressione3
     ELSE NULL END
```

## Uso nelle gerarchie

Nel contesto delle ragged hierarchies, COALESCE viene spesso usata per riempire i livelli mancanti:

``` sql
COALESCE(top_group_name, group_name, client_name) AS top_group_name
```

Questa operazione funziona come workaround nei report, ma ha limiti importanti: va ripetuta in ogni query, non distingue i valori originali da quelli di fallback, e complica il codice.

## Alternative per database

- **Oracle**: `NVL(a, b)` per due valori, `COALESCE` per più di due
- **MySQL**: `IFNULL(a, b)` per due valori, `COALESCE` per più di due
- **PostgreSQL**: solo `COALESCE` (standard SQL)

## Approccio consigliato nel DWH

Nel data warehouse, è preferibile usare COALESCE nell'ETL per popolare la tabella dimensionale con valori NOT NULL (self-parenting), piuttosto che usarla ripetutamente nei report. La logica di gestione dei NULL deve stare nel modello, non nella presentazione.
