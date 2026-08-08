---
title: "CATSEARCH Index"
description: "Oracle Text index type for mixed archives: resolves SQL predicates on structured attributes and full-text search together inside a single index structure."
translationKey: "glossary_indice_catsearch"
aka: "CATSEARCH index, Oracle Text CATSEARCH"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

The CATSEARCH index is a specialized Oracle Text index type designed for domains where each document carries structured attributes — sender, date, category, status — alongside free text that must be searched simultaneously. Rather than combining a B-tree index on structured columns with a separate full-text index, CATSEARCH merges both dimensions into a single structure.

## How it works

The index is created using `CTXSYS.CTXCAT` as the index type and accepts a list of structured columns to include in the sub-index. Oracle Text internally builds a catalog that indexes both text tokens and the values of the additional columns.

```sql
CREATE INDEX idx_doc_catsearch
ON documents(body)
INDEXTYPE IS CTXSYS.CTXCAT
PARAMETERS ('CTXCAT_INDEX_SET myindexset');
```

Queries use the `CATSEARCH` operator instead of the standard `CONTAINS`:

```sql
SELECT id, title
FROM documents
WHERE CATSEARCH(body, 'invoice AND overdue', 'category = ''accounting''') > 0;
```

The structural predicate (`category = 'accounting'`) is resolved inside the index, not as a post-scan filter.

## When to use it

CATSEARCH suits document archives with medium-to-high cardinality on structured columns and queries that systematically combine attribute filters with text search: ticketing systems, email archives, contract repositories. It is not the right fit for pure full-text search without structural predicates, where `CONTEXT` (with `CONTAINS`) provides richer linguistic capabilities. Index synchronization requires attention: like all Oracle Text indexes, CATSEARCH does not update in real time without an explicit sync policy.
