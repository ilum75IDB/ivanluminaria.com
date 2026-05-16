---
title: "Annotations"
description: "Oracle 23ai metadata system that attaches key/value pairs to schema objects (columns, domains, tables), readable via USER_ANNOTATIONS_USAGE."
translationKey: "glossary_oracle_annotations"
aka: "Annotations (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**Annotations** are a metadata system introduced in Oracle Database 23ai that lets you attach **key/value pairs** to schema objects: columns, SQL Domains, tables, views. They are readable by the engine via the `USER_ANNOTATIONS_USAGE`, `DBA_ANNOTATIONS_USAGE`, `ALL_ANNOTATIONS_USAGE` views.

## How it works

You declare them directly in the object's `CREATE` (or `ALTER`), inside the `ANNOTATIONS (...)` clause. Each pair has the form `name 'value'`. Example on a domain:

```sql
CREATE DOMAIN policy_status AS VARCHAR2(20)
  CONSTRAINT chk CHECK (VALUE IN ('ISSUED','ACTIVE','SUSPENDED'))
  ANNOTATIONS (
    display 'Policy Status',
    description 'Lifecycle of an insurance policy',
    ordering 'ISSUED<ACTIVE<SUSPENDED'
  );
```

Values are stored in the data dictionary without being interpreted by the engine — they are semantics, not a constraint. A query on `USER_ANNOTATIONS_USAGE` lets you extract them at runtime.

## What they're for

Centralizing in the schema dictionary the metadata that until 23ai lived in separate application tables or in external configuration files. BI tools (Power BI, Tableau), UI generation frameworks and reporting procedures can read database annotations directly to derive display labels, field descriptions, logical ordering — without requiring manual mapping.

## What sets them apart from COMMENT

`COMMENT ON COLUMN` (in Oracle for decades) lets you attach a single free-form text string to an object. `ANNOTATIONS` are **structured**: distinct keys, queryable values as table fields, support for multiple annotations per object. A `COMMENT` is still useful for textual documentation; `ANNOTATIONS` are suited for metadata that tools need to read and use automatically.
