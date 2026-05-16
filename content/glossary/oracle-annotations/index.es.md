---
title: "Annotations"
description: "Sistema de metadatos de Oracle 23ai que asocia pares clave/valor a objetos del esquema (columnas, domain, tablas), legibles vía USER_ANNOTATIONS_USAGE."
translationKey: "glossary_oracle_annotations"
aka: "Annotations (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

Las **Annotations** son un sistema de metadatos introducido en Oracle Database 23ai que permite asociar **pares clave/valor** a objetos del esquema: columnas, SQL Domain, tablas, vistas. Son legibles por el motor a través de las vistas `USER_ANNOTATIONS_USAGE`, `DBA_ANNOTATIONS_USAGE`, `ALL_ANNOTATIONS_USAGE`.

## Cómo funciona

Se declaran directamente en el `CREATE` (o `ALTER`) del objeto, dentro de la cláusula `ANNOTATIONS (...)`. Cada par tiene la forma `nombre 'valor'`. Ejemplo en un domain:

```sql
CREATE DOMAIN estado_poliza AS VARCHAR2(20)
  CONSTRAINT chk CHECK (VALUE IN ('EMITIDA','VIGENTE','SUSPENDIDA'))
  ANNOTATIONS (
    display 'Estado Póliza',
    description 'Ciclo de vida de una póliza',
    ordering 'EMITIDA<VIGENTE<SUSPENDIDA'
  );
```

Los valores se almacenan en el diccionario de datos sin ser interpretados por el motor — son semántica, no vínculo. Una consulta sobre `USER_ANNOTATIONS_USAGE` permite extraerlos en runtime.

## Para qué sirven

Centralizar en el diccionario del esquema los metadatos que hasta 23ai vivían en tablas aplicativas separadas o en archivos de configuración externos. Herramientas BI (Power BI, Tableau), frameworks de UI generation y procedimientos de reportería pueden leer directamente las anotaciones del database para derivar etiquetas de display, descripciones de campo, ordering lógico — sin requerir un mapping manual.

## Qué las distingue de COMMENT

`COMMENT ON COLUMN` (presente desde hace décadas en Oracle) permite asociar una sola cadena de texto libre a un objeto. Las `ANNOTATIONS` son **estructuradas**: claves distintas, valores consultables como campos tabulares, soporte a múltiples anotaciones por objeto. Un `COMMENT` sigue siendo útil para la documentación textual; las `ANNOTATIONS` son adecuadas para metadatos que las herramientas deben leer y usar automáticamente.
