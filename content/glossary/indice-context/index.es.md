---
title: "Índice CONTEXT"
description: "Índice Oracle Text para búsqueda full-text sobre contenido no estructurado: construye una estructura invertida token→documento sobre columnas CLOB."
translationKey: "glossary_indice_context"
aka: "CONTEXT index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

El índice CONTEXT es el tipo de índice principal de Oracle Text, diseñado para la búsqueda full-text en columnas que contienen texto no estructurado: documentos, artículos, dictámenes legales, notas técnicas. A diferencia de un índice B-tree estándar, no indexa valores discretos sino tokens lingüísticos, construyendo una estructura invertida que mapea cada palabra a los documentos donde aparece.

## Cómo funciona

Durante la creación, Oracle Text tokeniza el contenido de la columna (típicamente `CLOB`), aplica filtros lingüísticos (stemming, stopwords, thesaurus opcional) y puebla una serie de tablas internas — `$I`, `$K`, `$R`, `$N` — que forman el índice invertido. Las consultas usan el operador `CONTAINS` en lugar de `LIKE`:

```sql
SELECT doc_id, SCORE(1) AS relevancia
FROM documentos
WHERE CONTAINS(texto, 'contrato AND (arrendamiento OR alquiler)', 1) > 0
ORDER BY relevancia DESC;
```

El índice evita el escaneo secuencial completo de la columna CLOB en cada consulta, reduciendo drásticamente los tiempos de respuesta en conjuntos de datos de gran volumen.

## Cuándo utilizarlo

El índice CONTEXT es adecuado cuando:

- la columna contiene texto largo y variable (documentos, PDFs convertidos, XML);
- las consultas requieren operadores booleanos, búsqueda por proximidad o recuperación por concepto;
- el volumen de datos hace inviable cualquier enfoque basado en `LIKE '%...%'`.

Una limitación operativa relevante: el índice CONTEXT **no se actualiza en tiempo real**. Las filas insertadas o modificadas tras la creación del índice solo se vuelven buscables después de una sincronización explícita (`CTX_DDL.SYNC_INDEX`) o mediante un job programado. En escenarios con escrituras frecuentes, es necesario planificar una estrategia de sincronización coherente con la latencia de búsqueda aceptable.
