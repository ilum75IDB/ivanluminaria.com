---
title: "CONTEXT Index"
description: "Oracle Text CONTEXT index for full-text search on unstructured content: builds an inverted token→document structure over CLOB columns."
translationKey: "glossary_indice_context"
aka: "CONTEXT index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

The CONTEXT index is Oracle Text's primary index type, designed for full-text search on columns containing unstructured text: documents, articles, legal opinions, technical notes. Unlike a standard B-tree index, it does not index discrete values but linguistic tokens, building an inverted structure that maps each word to the documents where it appears.

## How it works

At creation time, Oracle Text tokenizes the column content (typically a `CLOB`), applies linguistic filters (stemming, stopwords, optional thesaurus) and populates a set of internal tables — `$I`, `$K`, `$R`, `$N` — that form the inverted index. Queries use the `CONTAINS` operator instead of `LIKE`:

```sql
SELECT doc_id, SCORE(1) AS relevance
FROM documents
WHERE CONTAINS(body, 'contract AND (lease OR rental)', 1) > 0
ORDER BY relevance DESC;
```

The index avoids a full sequential scan of the CLOB column on every query, dramatically reducing response times on large datasets.

## When to use it

The CONTEXT index is the right choice when:

- the column holds long, variable text (documents, converted PDFs, XML);
- queries require boolean operators, proximity search, or concept-based retrieval;
- data volume makes any `LIKE '%...%'` approach impractical.

One significant operational constraint: the CONTEXT index **does not update in real time**. Rows inserted or modified after index creation become searchable only after an explicit synchronization (`CTX_DDL.SYNC_INDEX`) or via a scheduled job. For write-heavy workloads, a sync strategy aligned with the acceptable search latency must be planned upfront.
