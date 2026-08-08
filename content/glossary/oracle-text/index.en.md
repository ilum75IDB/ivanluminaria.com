---
title: "Oracle Text"
description: "Oracle Database built-in component for full-text indexing and search on CLOB, BLOB, and VARCHAR2 columns, no separate license required."
translationKey: "glossary_oracle_text"
aka: "Oracle Text (Oracle interMedia Text, ConText)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Oracle Text is the full-text search engine built into Oracle Database. It allows indexing and querying large volumes of structured and unstructured text directly inside the database, with no external dependencies and no additional license beyond the Standard or Enterprise Edition.

## How it works

Oracle Text builds specialized indexes (`CONTEXT`, `CTXCAT`, `CTXRULE`, or `CTXPATH`) on text columns. The `CONTEXT` index is the most common: it tokenizes the text, applies stemming and stoplists, and stores token positions in internal structures optimized for search.

Queries use the `CONTAINS` operator in the `WHERE` clause:

```sql
SELECT doc_id, title
FROM documents
WHERE CONTAINS(body, 'database AND performance', 1) > 0
ORDER BY SCORE(1) DESC;
```

The index must be synchronized manually or on a schedule using `CTX_DDL.SYNC_INDEX` after DML operations, because it is not updated in real time within the transaction.

## When to use it

Oracle Text is the right choice when:

- text volume makes `LIKE` or `REGEXP_LIKE` impractical due to performance degradation;
- advanced features are needed, such as proximity search, fuzzy matching, thematic expansion, or result highlighting;
- documents already live in Oracle Database and moving data to an external engine (Elasticsearch, Solr) would introduce unjustified architectural complexity.

The main limitation is index synchronization: in high-write scenarios, the lag between DML and index update must be explicitly planned and scheduled.
