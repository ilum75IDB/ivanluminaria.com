---
title: "join_buffer_size"
description: "MySQL buffer allocated per thread for each index-less join. Multiplied by active connections, it can exhaust server RAM."
translationKey: "glossary_join_buffer_size"
aka: "Join Buffer (MySQL)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`join_buffer_size` is a MySQL session-level parameter that controls the size of the buffer used to perform joins between tables when no suitable index is available. Unlike `innodb_buffer_pool_size`, which is a shared resource, this buffer is allocated **per active thread** executing such a join.

## How it works

When MySQL cannot use an index to join two tables, it falls back to a **Block Nested-Loop Join** (or, in newer versions, a Hash Join). In both cases, rows from the "outer" table are loaded into the `join_buffer` and compared against the "inner" table.

```sql
-- Check the current value at session level
SHOW VARIABLES LIKE 'join_buffer_size';

-- Override for the current session
SET SESSION join_buffer_size = 4 * 1024 * 1024; -- 4 MB
```

If the buffer cannot hold all the relevant rows, MySQL performs multiple passes over the inner table, increasing I/O.

## Operational context

The main risk is not the absolute value of the parameter but its **multiplicative effect**: with 500 concurrent connections and a `join_buffer_size` of 8 MB, the potential memory consumption exceeds 4 GB, regardless of how many joins are actually running at any given moment.

Practical guidelines:

- Keep the global value low (256 KB – 1 MB) and raise it at session level only for specific queries that benefit from it.
- Before increasing the buffer, check whether the missing index is intentional or an oversight: a proper index eliminates the problem at the source.
- Monitor `Select_full_join` and `Select_range_check` in `SHOW GLOBAL STATUS` to quantify how often index-less joins occur.
