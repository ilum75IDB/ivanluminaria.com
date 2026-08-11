---
title: "Invalid view"
description: "A MySQL view whose SQL body references objects that no longer exist or are inaccessible: renamed tables, dropped columns, revoked privileges."
translationKey: "glossary_view_invalida"
aka: "Broken view, Stale view"
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

An **invalid view** is a view whose SQL body references objects that no longer exist or are no longer accessible: renamed tables, dropped columns, revoked privileges. MySQL does not automatically invalidate views when the underlying table is modified, so the error stays silent until the view is first queried or until a `mysqldump` attempts to export it.

## How it works

MySQL stores the view's SQL text in `information_schema.VIEWS` at creation time but does not track runtime dependencies. If a referenced table is renamed or a column is dropped via `ALTER TABLE ... DROP COLUMN`, the view continues to exist in the catalog with no warning.

```sql
-- Quick status check for all views in the current database
SELECT table_name, is_updatable
FROM information_schema.VIEWS
WHERE table_schema = DATABASE();

-- Accessing the view exposes the broken state
SELECT * FROM view_name;
-- ERROR 1356 (HY000): View 'db.view_name' references invalid table(s) or column(s)
```

## Operational context

The issue typically surfaces in three scenarios: during a **patching** cycle or schema migration, after a `RENAME TABLE` executed without updating dependent views, or during a dump with `mysqldump --routines` that tries to export the view definition. In the last case the dump may complete but the restore fails or produces warnings that are hard to trace. Before any maintenance operation, a systematic check using `CHECK TABLE view_name` or querying `information_schema` is the standard safeguard.
