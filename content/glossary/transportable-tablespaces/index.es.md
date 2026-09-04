---
title: "Transportable Tablespaces (TTS)"
description: "Funcionalidad Oracle para mover tablespaces entre bases de datos copiando los datafiles físicos e importando solo los metadatos con Data Pump. Mucho más rápido que un export completo."
translationKey: "glossary_transportable_tablespaces"
aka: "Transportable Tablespaces (Oracle TTS)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Los Transportable Tablespaces (TTS) son una funcionalidad de Oracle que permite mover uno o más tablespaces entre bases de datos — incluso entre plataformas distintas — copiando físicamente los datafiles y transportando únicamente los metadatos mediante Data Pump. En volúmenes del orden de los terabytes, el ahorro de tiempo respecto a un export/import convencional es considerable.

## Cómo funciona

El proceso se divide en tres fases principales:

1. **Poner el tablespace origen en modo read-only.**
2. **Exportar los metadatos** con Data Pump (`TRANSPORT_TABLESPACES`).
3. **Copiar los datafiles** al sistema destino e importar los metadatos.

```sql
-- Poner el tablespace en read-only
ALTER TABLESPACE sales_data READ ONLY;

-- Export de metadatos (Data Pump)
-- expdp system/pwd TRANSPORT_TABLESPACES=sales_data \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_sales.log

-- Tras copiar los datafiles al destino:
-- impdp system/pwd TRANSPORT_DATAFILES='/u02/oradata/sales_data01.dbf' \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_import.log
```

Cuando la migración es entre plataformas con diferente endianness, se requiere un paso de conversión RMAN (`CONVERT TABLESPACE`) antes del import. La compatibilidad de character set entre origen y destino también es obligatoria.

## Cuándo se usa

TTS es la opción natural cuando:

- se migran grandes volúmenes de datos históricos o tablespaces de data warehouse entre entornos Oracle;
- el tiempo de inactividad tolerable es reducido y un export/import completo llevaría horas o días;
- se consolidan varias bases de datos en un único destino (p. ej., upgrade a 21c en Exadata).

La principal restricción es que el tablespace origen debe permanecer en `READ ONLY` durante toda la copia de los datafiles. En escenarios con requisitos de alta disponibilidad, TTS se combina habitualmente con RMAN Incremental Backup para reducir la ventana de read-only al mínimo imprescindible.
