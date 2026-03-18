---
title: "COALESCE"
description: "Funcție SQL care returnează prima valoare non-NULL dintr-o listă de expresii."
translationKey: "glossary_coalesce"
aka: "NVL (Oracle), IFNULL (MySQL)"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**COALESCE** este o funcție SQL standard care acceptă o listă de expresii și returnează prima care nu este NULL. Dacă toate expresiile sunt NULL, returnează NULL.

## Sintaxă

``` sql
COALESCE(expresie1, expresie2, expresie3, ...)
```

Echivalent cu un lanț de CASE WHEN:

``` sql
CASE WHEN expresie1 IS NOT NULL THEN expresie1
     WHEN expresie2 IS NOT NULL THEN expresie2
     WHEN expresie3 IS NOT NULL THEN expresie3
     ELSE NULL END
```

## Utilizare în ierarhii

În contextul ragged hierarchies, COALESCE este adesea folosită pentru a completa nivelurile lipsă:

``` sql
COALESCE(top_group_name, group_name, client_name) AS top_group_name
```

Aceasta funcționează ca workaround în rapoarte, dar are limitări importante: trebuie repetată în fiecare interogare, nu distinge valorile originale de cele de fallback, și complică codul.

## Alternative pe baze de date

- **Oracle**: `NVL(a, b)` pentru două valori, `COALESCE` pentru mai mult de două
- **MySQL**: `IFNULL(a, b)` pentru două valori, `COALESCE` pentru mai mult de două
- **PostgreSQL**: doar `COALESCE` (SQL standard)

## Abordare recomandată în DWH

Într-un data warehouse, este preferabil să folosești COALESCE în ETL pentru a popula tabela dimensională cu valori NOT NULL (self-parenting), în loc să o folosești repetat în rapoarte. Logica de gestionare a NULL-urilor trebuie să fie în model, nu în stratul de prezentare.
