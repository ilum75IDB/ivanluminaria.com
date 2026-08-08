---
title: "Oracle Text"
description: "Componente integrado de Oracle Database para indexación y búsqueda full-text sobre columnas CLOB, BLOB y VARCHAR2, sin licencia adicional."
translationKey: "glossary_oracle_text"
aka: "Oracle Text (Oracle interMedia Text, ConText)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Oracle Text es el motor de búsqueda full-text integrado en Oracle Database. Permite indexar y consultar grandes volúmenes de texto estructurado y no estructurado directamente dentro de la base de datos, sin dependencias externas y sin licencia adicional respecto a la Standard o Enterprise Edition.

## Cómo funciona

Oracle Text construye índices especializados (`CONTEXT`, `CTXCAT`, `CTXRULE` o `CTXPATH`) sobre columnas de texto. El índice `CONTEXT` es el más habitual: tokeniza el texto, aplica stemming y stoplists, y almacena las posiciones de los tokens en estructuras internas optimizadas para la búsqueda.

Las consultas se realizan mediante el operador `CONTAINS` en la cláusula `WHERE`:

```sql
SELECT doc_id, title
FROM documents
WHERE CONTAINS(body, 'database AND performance', 1) > 0
ORDER BY SCORE(1) DESC;
```

El índice debe sincronizarse manualmente o mediante una tarea programada con `CTX_DDL.SYNC_INDEX` tras operaciones DML, ya que no se actualiza en tiempo real dentro de la transacción.

## Cuándo utilizarlo

Oracle Text es la opción adecuada cuando:

- el volumen de texto hace inviable el uso de `LIKE` o `REGEXP_LIKE` sin degradación del rendimiento;
- se necesitan funcionalidades avanzadas como búsqueda por proximidad, fuzzy matching, expansión temática o resaltado de resultados;
- los documentos ya residen en Oracle Database y mover los datos a un motor externo (Elasticsearch, Solr) introduciría una complejidad arquitectónica no justificada.

La principal limitación es la sincronización del índice: en escenarios con alta tasa de escritura, el desfase entre el DML y la actualización del índice debe planificarse de forma explícita.
