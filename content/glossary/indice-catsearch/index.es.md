---
title: "Índice CATSEARCH"
description: "Tipo de índice Oracle Text para archivos mixtos: resuelve predicados SQL sobre atributos estructurados y búsqueda de texto libre en una sola operación dentro del índice."
translationKey: "glossary_indice_catsearch"
aka: "CATSEARCH index, Oracle Text CATSEARCH"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

El índice CATSEARCH es un tipo especializado de Oracle Text diseñado para dominios en los que cada documento lleva atributos estructurados — remitente, fecha, categoría, estado — junto con texto libre que debe buscarse de forma simultánea. En lugar de combinar un índice B-tree sobre columnas estructuradas con un índice full-text separado, CATSEARCH fusiona ambas dimensiones en una única estructura.

## Cómo funciona

El índice se crea usando `CTXSYS.CTXCAT` como tipo de índice y acepta una lista de columnas estructuradas para incluir en el sub-índice. Oracle Text construye internamente un catálogo que indexa tanto los tokens textuales como los valores de las columnas adicionales.

```sql
CREATE INDEX idx_doc_catsearch
ON documentos(cuerpo)
INDEXTYPE IS CTXSYS.CTXCAT
PARAMETERS ('CTXCAT_INDEX_SET myindexset');
```

Las consultas usan el operador `CATSEARCH` en lugar del clásico `CONTAINS`:

```sql
SELECT id, titulo
FROM documentos
WHERE CATSEARCH(cuerpo, 'factura AND vencida', 'categoria = ''contabilidad''') > 0;
```

El predicado estructural (`categoria = 'contabilidad'`) se resuelve dentro del índice, no como filtro posterior al escaneo.

## Cuándo se usa

CATSEARCH es adecuado para archivos documentales con cardinalidad media-alta en las columnas estructuradas y consultas que combinan sistemáticamente filtros de atributos con búsqueda textual: sistemas de ticketing, archivos de correo electrónico, repositorios de contratos. No es la opción correcta para búsqueda full-text pura sin predicados estructurales, donde `CONTEXT` (con `CONTAINS`) ofrece capacidades lingüísticas más ricas. La sincronización del índice requiere atención: como todos los índices Oracle Text, CATSEARCH no se actualiza en tiempo real sin una política de sync explícita.
