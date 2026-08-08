---
title: "CTXXPATH Index"
description: "Oracle Text index type for XML or JSON documents stored in CLOB/BLOB: preserves path hierarchy and enables node-specific queries."
translationKey: "glossary_indice_ctxxpath"
aka: "CTXXPATH index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

The CTXXPATH index is a specialized Oracle Text index type designed for XML or JSON documents stored in `CLOB` or `BLOB` columns. Unlike generic full-text indexes, CTXXPATH retains the hierarchical structure of the document during indexing, making it possible to scope searches to specific paths or nodes rather than scanning the entire text content.

## How it works

The index is created using `CREATE INDEX ... INDEXTYPE IS CTXSYS.CTXXPATH`. Oracle Text parses the document, builds a map of XML/JSON paths, and indexes both the textual content and the structural position of each node.

```sql
CREATE INDEX idx_doc_xml
ON documents(xml_content)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

Queries then use `existsNode` or the `CONTAINS` operator with path-aware syntax to narrow the search:

```sql
SELECT id
FROM documents
WHERE existsNode(xml_content, '/invoice/customer[name="Smith"]') = 1;
```

## When to use it

CTXXPATH is the right choice when documents have meaningful XML or JSON structure and queries need to distinguish between nodes that share the same text value but sit at different positions in the document. Typical scenarios: electronic invoice archives, XML product catalogs, heterogeneous JSON payloads.

The main limitation is format dependency: the document must be well-formed XML or JSON. For unstructured text, `CTXSYS.CONTEXT` is more appropriate; for purely structural searches without full-text requirements, standard relational indexes on columns extracted via `XMLTable` or `JSON_TABLE` are sufficient.
