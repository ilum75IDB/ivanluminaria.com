---
title: "Direct-path insert"
description: "Modo de carga de datos de Oracle que omite el buffer cache y escribe directamente en los datafiles mediante el hint /*+ APPEND */."
translationKey: "glossary_direct_path_insert"
aka: "Direct-path insert (hint APPEND de Oracle)"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

El Direct-path insert es un modo de escritura de Oracle que omite el buffer cache e inserta los datos directamente en los datafiles, por encima del high-water mark del segmento. Se activa mediante el hint `/*+ APPEND */` en una instrucción `INSERT` y se utiliza habitualmente en operaciones de carga masiva para reducir la sobrecarga de I/O y el volumen de redo generado.

## Cómo funciona

Durante un Direct-path insert, Oracle no busca bloques libres en el segmento existente: asigna nuevo espacio más allá del high-water mark y escribe directamente en disco, saltando el buffer pool. La generación de redo es mínima (o nula en modo `NOLOGGING`), lo que hace que la operación sea considerablemente más rápida que un conventional insert sobre grandes volúmenes de datos.

```sql
INSERT /*+ APPEND */ INTO target_table
SELECT * FROM source_table;
COMMIT;
```

Hasta el COMMIT, la tabla queda bloqueada en escritura para otras sesiones: ningún otro proceso puede insertar filas en la misma tabla durante la transacción.

## Cuándo usarlo y limitaciones

El Direct-path insert es adecuado para pipelines ETL, cargas masivas y poblado de tablas de staging. Presenta algunas restricciones operativas relevantes:

- **Restricciones de integridad**: las restricciones `CHECK` y `NOT NULL` se evalúan, pero las claves foráneas pueden necesitar deshabilitarse o diferirse para mantener el rendimiento.
- **Triggers**: los triggers `BEFORE/AFTER INSERT ROW` no se ejecutan en modo direct-path.
- **Assertions (Oracle 23ai+)**: el comportamiento con las Assertions debe verificarse caso por caso, ya que el mecanismo de validación difiere del conventional insert.

En entornos con Assertions activas, es necesario realizar pruebas explícitas antes de adoptar el Direct-path insert en producción.
