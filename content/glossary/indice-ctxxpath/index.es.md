---
title: "Índice CTXXPATH"
description: "Tipo de índice Oracle Text para documentos XML o JSON en CLOB/BLOB: preserva la jerarquía de paths y permite consultas sobre nodos específicos."
translationKey: "glossary_indice_ctxxpath"
aka: "CTXXPATH index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

El índice CTXXPATH es un tipo especializado de Oracle Text diseñado para documentos XML o JSON almacenados en columnas `CLOB` o `BLOB`. A diferencia de los índices full-text genéricos, CTXXPATH conserva la estructura jerárquica del documento durante la indexación, lo que permite acotar las búsquedas a paths o nodos concretos en lugar de recorrer todo el contenido textual.

## Cómo funciona

El índice se crea con `CREATE INDEX ... INDEXTYPE IS CTXSYS.CTXXPATH`. Oracle Text analiza el documento, construye un mapa de los paths XML/JSON e indexa tanto el contenido textual como la posición estructural de cada nodo.

```sql
CREATE INDEX idx_doc_xml
ON documentos(contenido_xml)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

Las consultas utilizan `existsNode` o el operador `CONTAINS` con sintaxis path-aware para delimitar la búsqueda:

```sql
SELECT id
FROM documentos
WHERE existsNode(contenido_xml, '/factura/cliente[nombre="García"]') = 1;
```

## Cuándo utilizarlo

CTXXPATH es la opción adecuada cuando los documentos tienen una estructura XML o JSON relevante y las consultas deben diferenciar nodos con el mismo valor textual pero ubicados en posiciones distintas del documento. Escenarios habituales: archivos de facturas electrónicas, catálogos de productos en XML, payloads JSON heterogéneos.

La principal limitación es la dependencia del formato: el documento debe ser XML o JSON bien formado. Para texto no estructurado, `CTXSYS.CONTEXT` es más apropiado; para búsquedas puramente estructurales sin necesidad de full-text, bastan los índices relacionales estándar sobre columnas extraídas con `XMLTable` o `JSON_TABLE`.
