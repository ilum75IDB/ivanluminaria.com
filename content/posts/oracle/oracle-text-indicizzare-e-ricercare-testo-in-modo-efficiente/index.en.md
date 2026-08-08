---
categories:
- oracle
date: 2099-12-31
draft: true
image: oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente.cover.jpg
tags: []
title: 'Research on millions of legal documents: how Oracle Text changed response
  times'
translationKey: oracle_text_indicizzare_e_ricercare_testo_in_modo_efficiente
webo_generated_at: 2026-08-08
webo_status: da_tradurre
---

```
---
title: "Alberto's frustration: Oracle Text full-text search on a 30-year legal archive"
seoTitle: "Oracle Text: CONTEXT, CATSEARCH, CTXXPATH on CLOB columns"
description: "How three Oracle Text indexes cut legal archive search times from 90 seconds to under 700ms. A real case with CONTEXT, CATSEARCH, and CTXXPATH."
tags: ["oracle-text", "full-text-search", "oracle-19c", "clob", "performance-tuning"]
---
```

## Alberto's frustration

Alberto didn't open a ticket. He called directly, in the middle of an afternoon, and the first thing he said was: "Search times are unacceptable. I can't wait a minute every time I look up a contract."

Thirty years of documents layered into an Oracle archive. Contracts, legal opinions, court filings, correspondence with clients and counterparties. The `LEGAL_ARCHIVE` schema on `oracle-legal-prod-01` held two main tables: `DOCUMENTS`, with a `DOC_CONTENT` column of type CLOB collecting hundreds of gigabytes of text, and `EMAILS`, with `SENDER`, `SUBJECT`, and `BODY`. Millions of rows in both.

The bottleneck wasn't generic system slowness. It was text search: `LIKE '%term%'` queries on CLOB columns, with no indexes suited to that kind of workload. Thirty seconds to find a contract, forty-five to search an email by subject and body content. Ninety in the worst moments.

The first thing we did, before touching any configuration, was sit down with Alberto and two of his most hands-on colleagues and ask them how they actually search. Not "what do you search for," but *how*: free-text fragments? Combinations of sender plus keyword in the body? Specific clauses in structured XML documents? The answer completely changed the approach.

Nobody had ever asked that question before.

## Oracle Text: not an add-on, a built-in component

Oracle Text is included in Oracle Database with no additional license [1]. It's not an external engine to integrate, not an Elasticsearch instance to maintain in parallel: it's a full-text indexing system that lives inside the database, with direct access to the data, transactions, and access controls already in place.

The distinction from a standard B-tree index is substantial. A B-tree on a `VARCHAR2` column works for equality and prefix matches (`LIKE 'term%'`), and at the same time it's useless for mid-string searches (`LIKE '%term%'`) on CLOB columns spanning hundreds of gigabytes — in that case Oracle performs a full column scan, row by row. Oracle Text instead builds an inverted structure: for each token (word) it maintains the list of documents containing it, along with position information. The query doesn't scan the data; it consults the index.

Three index types cover different scenarios:

- **CONTEXT** — free text, documents, articles
- **CATSEARCH** — mixed archives with structured attributes and free text
- **CTXXPATH** — XML or JSON documents stored in CLOB/BLOB

The choice among the three isn't arbitrary: it depends precisely on how users search. That's why the conversation with Alberto came before the code.

## CONTEXT index: the foundation for unstructured documents

For `LEGAL_ARCHIVE.DOCUMENTS` the case was clear: full-text search on unstructured text. Contracts in plain text format, legal opinions, court filings. The CONTEXT index is the natural choice [1].

```sql
-- Create the CONTEXT index on the DOC_CONTENT column
BEGIN
  CTX_DDL.CREATE_PREFERENCE('legal_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'MIXED_CASE', 'NO');

  CTX_DDL.CREATE_STOPLIST('legal_stoplist', 'BASIC_STOPLIST');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'il');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'la');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'di');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'che');
END;
/

CREATE INDEX legal_doc_ctx_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CONTEXT
PARAMETERS ('LEXER legal_lexer STOPLIST legal_stoplist MEMORY 256M');
```

The `BASIC_LEXER` with `BASE_LETTER YES` handles accent normalization — essential for Italian, where "è" and "e" shouldn't be treated as distinct tokens in a search. The `STOPLIST` excludes from the index the function words that carry no semantic weight in legal queries.

Queries use the `CONTAINS` operator [1]:

```sql
-- Search for documents containing both terms
SELECT doc_id, doc_title, SCORE(1) AS relevance
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'responsabilità AND contrattuale', 1) > 0
ORDER BY SCORE(1) DESC;

-- Proximity search: the two terms within 5 words of each other
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'NEAR((inadempimento, risarcimento), 5)', 1) > 0;
```

The result after implementation: from 30–60 seconds down to under 500 ms. That's not an optimistic estimate — it's the measured figure on queries representative of the real workload.

## CATSEARCH index: when text mixes with metadata

Emails were a different case. Alberto and his colleagues don't search only in the message body: they search by sender, by subject, by date, and then filter by text content. A typical query was: "all emails from that external consultant, with 'perizia' in the subject or body, in the last two years."

This is exactly the scenario CATSEARCH was designed for [1]: searches that combine SQL predicates on structured columns with full-text search on text columns.

```sql
-- Define the set of structured columns included in the index
EXEC CTX_DDL.CREATE_INDEX_SET('legal_email_set');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SENDER');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SUBJECT');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'RECEIVED_DATE');

-- Create the CATSEARCH index on EMAILS
CREATE INDEX legal_email_cat_idx
ON LEGAL_ARCHIVE.EMAILS(BODY)
INDEXTYPE IS CTXSYS.CATSEARCH
PARAMETERS ('CTXCAT_INDEX_CLAUSE
  "CTXCAT_INDEX_SET legal_email_set"');
```

Order matters: define the structured column set first, then create the index that references it.

The query uses the `CATSEARCH` operator with a separate structured clause [1]:

```sql
-- Combined search: specific sender + term in body
SELECT email_id, sender, subject, received_date
FROM LEGAL_ARCHIVE.EMAILS
WHERE CATSEARCH(
  BODY,
  'perizia',
  'SENDER = ''consulente.esterno@example.com'' AND
   RECEIVED_DATE > DATE ''2024-01-01'''
) > 0
ORDER BY received_date DESC;
```

The difference from CONTEXT is that predicates on structured columns are evaluated inside the index, not as subsequent SQL filters. The optimizer doesn't have to find all documents containing "perizia" first and then filter by sender: both conditions are resolved together. From 45–90 seconds down to under 700 ms.

## CTXXPATH index: inside XML and JSON documents

Part of the archive held documents in XML format — structured filings with sections, statutory references, encoded metadata. Searching with `LIKE` on a CLOB containing XML is inefficient by definition: there's no way to limit the search to a specific node without parsing the document at runtime.

CTXXPATH addresses this [1]: it indexes XML content while preserving path structure, and enables queries that search for a term only within a specific node.

```sql
-- Create the CTXXPATH index on XML documents
CREATE INDEX legal_xml_xpath_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

The query uses `CTX_XPTH.CONTAINS` [1]:

```sql
-- Search for 'inadempimento' only within the <motivazione> section
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CTX_XPTH.CONTAINS(
  DOC_CONTENT,
  '/atto/motivazione[. contains("inadempimento")]'
) = 1;
```

Before: a `LIKE '%inadempimento%'` query on XML CLOB, over 120 seconds. After: under one second. The difference is structural: the index knows where tokens sit relative to the XML hierarchy, and doesn't need to re-read the entire document to answer.

## Advanced operators and relevance scoring

Once the indexes were live, we worked with the firm's staff to refine the queries. Oracle Text provides a set of operators that go well beyond simple boolean search [1][2].

`ACCUM` accumulates scores instead of requiring all terms to be present — useful when you want to rank by overall relevance without excluding documents that contain only some of the terms:

```sql
-- Most relevant documents for a combination of terms
SELECT doc_id, doc_title, SCORE(1) AS score
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(
  DOC_CONTENT,
  '(responsabilità ACCUM contrattuale ACCUM inadempimento)',
  1
) > 0
ORDER BY SCORE(1) DESC
FETCH FIRST 20 ROWS ONLY;
```

`FUZZY` handles spelling variations and typos — particularly useful on OCR-scanned texts, where recognition quality isn't uniform:

```sql
-- Fuzzy search to handle spelling variants
SELECT doc_id FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'FUZZY(risarcimanto, 70, 6)', 1) > 0;
```

The `70` parameter is the similarity threshold (0–100), `6` the maximum number of expansions. It needs calibration: thresholds too low produce noise, too high and you miss the relevant variants.

To present results to users, `CTX_DOC.HIGHLIGHT` returns the text with matched terms marked up [1]:

```sql
-- Highlight matched terms in the document
DECLARE
  v_highlight CLOB;
BEGIN
  CTX_DOC.HIGHLIGHT(
    index_name  => 'LEGAL_DOC_CTX_IDX',
    textkey     => '12345',
    query       => 'responsabilità contrattuale',
    restab      => v_highlight,
    starttag    => '<b>',
    endtag      => '</b>'
  );
  DBMS_OUTPUT.PUT_LINE(DBMS_LOB.SUBSTR(v_highlight, 500, 1));
END;
/
```

## Index synchronization and maintenance

One aspect that often gets underestimated: Oracle Text indexes don't update automatically in real time the way a B-tree does. When new rows are inserted, the index must be synchronized explicitly [1].

```sql
-- Manual index synchronization
EXEC CTX_DDL.SYNC_INDEX('LEGAL_DOC_CTX_IDX', '256M');

-- Periodic optimization to compact internal structures
EXEC CTX_DDL.OPTIMIZE_INDEX('LEGAL_DOC_CTX_IDX', 'FULL');
```

For a production archive with continuous inserts, synchronization needs to be scheduled. A `DBMS_SCHEDULER` job every 15–30 minutes is a reasonable starting point; the frequency depends on insert volume and tolerance for indexing lag. For `LEGAL_ARCHIVE`, where documents are loaded in nightly batches, a post-load synchronization was sufficient.

Monitoring goes through `CTX_USER_INDEXES` and `CTX_INDEX_ERRORS`:

```sql
-- Check Oracle Text index status
SELECT idx_name, idx_status, idx_docid_count
FROM CTX_USER_INDEXES;

-- Check for indexing errors
SELECT err_index_name, err_timestamp, err_text
FROM CTX_INDEX_ERRORS
ORDER BY err_timestamp DESC;
```

## Alberto's relief, not his surprise

When we showed Alberto the results, his reaction wasn't astonishment. It was relief. "Finally," he said. Not "incredible" — *finally*.

That word says everything about the approach that worked. There was no heroic moment where someone found the magic solution. There was a conversation where we stopped staring at logs and asked users how they actually work. From that conversation it emerged that three different indexes were needed for three different search patterns — not one generic index applied to everything.

Oracle Text was already available in the 19c instance. The features were documented. What was missing was the mapping between real search needs and the tool's capabilities.

The firm's team contributed in a decisive way: without their willingness to describe their actual workflows — not the theoretical ones, the daily ones — we would have configured indexes that looked reasonable on paper but weren't optimal for that specific context. The technology is a tool; understanding the problem is the real work.

Oracle Text indexes shouldn't be built from the documentation toward the data. They should be built from the needs of the people searching toward the data structure, and then the documentation helps identify the right index type and operators. In that order.

## Official sources

1. Oracle Text Reference 19c — [Oracle Text Indextype Reference (CONTEXT, CATSEARCH, CTXXPATH, CONTAINS, CATSEARCH operator, CTX_XPTH.CONTAINS, WORDLIST, STOPLIST, LEXER, CTX_DDL.SYNC_INDEX, CTX_DOC.HIGHLIGHT)](https://docs.oracle.com/en/database/oracle/oracle-database/19/textr/index.html)
2. Oracle Text Application Developer's Guide 19c — [Advanced concepts, tuning and best practices](https://docs.oracle.com/en/database/oracle/oracle-database/19/texta/toc.htm)
3. Oracle-Base (Tim Hall) — [Oracle Text Articles: practical examples](https://oracle-base.com/articles/misc/oracle-text)

## Glossary
- **[Oracle Text](/en/glossary/oracle-text/)** — Built-in Oracle Database component for indexing and full-text search on textual data. Requires no separate license and operates directly on database data structures, including CLOB, BLOB, and VARCHAR2 columns.

- **[CONTEXT index](/en/glossary/oracle-text/)** — Oracle Text index type for full-text search on unstructured text (documents, articles, legal opinions). Builds an inverted token→document structure that avoids full CLOB column scans on every query.

- **[CATSEARCH index](/en/glossary/indice-context/)** — Oracle Text index type optimized for archives that combine structured attributes (sender, date, category) with free text. SQL predicates and text search are resolved together inside the index, not in separate phases.

- **CTXXPATH index** — Oracle Text index type for XML or JSON documents stored in CLOB/BLOB. Preserves the hierarchical path structure during indexing, enabling queries that restrict search to specific nodes within the document.

- **Lexer** (Oracle Text) — Component that analyzes text during the indexing phase, breaking it into tokens and applying language- and format-specific normalization rules. The `BASIC_LEXER` with `BASE_LETTER YES` handles, for example, accent normalization for Italian text.
