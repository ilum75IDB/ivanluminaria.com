---
title: "Transportable Tablespaces (TTS)"
description: "Oracle feature to move tablespaces between databases by copying physical datafiles and importing only metadata via Data Pump. Far faster than a full export on large volumes."
translationKey: "glossary_transportable_tablespaces"
aka: "Transportable Tablespaces (Oracle TTS)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Transportable Tablespaces (TTS) is an Oracle feature that lets you move one or more tablespaces between databases — including across different platforms — by physically copying the datafiles and transporting only the metadata via Data Pump. On terabyte-scale datasets, the time savings over a conventional export/import are significant.

## How it works

The process has three main steps:

1. **Set the source tablespace to read-only.**
2. **Export the metadata** with Data Pump (`TRANSPORT_TABLESPACES`).
3. **Copy the datafiles** to the target system and import the metadata.

```sql
-- Set tablespace read-only
ALTER TABLESPACE sales_data READ ONLY;

-- Metadata export (Data Pump)
-- expdp system/pwd TRANSPORT_TABLESPACES=sales_data \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_sales.log

-- After copying datafiles to the target:
-- impdp system/pwd TRANSPORT_DATAFILES='/u02/oradata/sales_data01.dbf' \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_import.log
```

When moving across platforms with different endianness, an RMAN conversion step (`CONVERT TABLESPACE`) is required before the import. Character set compatibility between source and target is also mandatory.

## When to use it

TTS is the natural choice when:

- migrating large historical datasets or data warehouse tablespaces between Oracle environments;
- downtime tolerance is low and a full export/import would take hours or days;
- consolidating multiple databases into a single target (e.g., upgrading to 21c on Exadata).

The main constraint is that the source tablespace must remain `READ ONLY` for the entire duration of the datafile copy. In high-availability scenarios, TTS is often combined with RMAN Incremental Backup to shrink the read-only window to the bare minimum.
