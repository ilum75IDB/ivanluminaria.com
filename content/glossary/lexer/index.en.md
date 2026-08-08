---
title: "Lexer"
description: "Oracle Text component that splits text into tokens during indexing, applying language- and format-specific normalization rules."
translationKey: "glossary_lexer"
aka: "Lexer (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

The Lexer is the Oracle Text component responsible for textual analysis during the indexing phase. It receives the raw text of a document or column and breaks it into tokens — the atomic units on which the inverted index is built — applying normalization rules that vary by language and content type.

## How it works

The Lexer runs before tokens are written to the inverted index. Its main responsibilities are tokenization (where to split the text), normalization (how to transform each token), and special character handling.

Oracle Text provides several Lexer types. The most common for natural-language text is `BASIC_LEXER`, configurable via `CTX_DDL.SET_ATTRIBUTE`:

```sql
BEGIN
  CTX_DDL.CREATE_PREFERENCE('my_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'MIXED_CASE', 'NO');
END;
/
```

The `BASE_LETTER YES` attribute instructs the Lexer to reduce accented characters to their base form (e.g. `è` → `e`, `ü` → `u`), making searches accent-insensitive — essential behavior for Italian and many other European languages.

## When to use it

The choice and configuration of the Lexer directly affects full-text search quality. A custom Lexer is needed when:

- the corpus contains text in languages with accents or non-ASCII characters (Italian, French, German, Spanish);
- URLs, product codes, or technical identifiers are being indexed and must not be split like ordinary words;
- token case-sensitivity needs explicit control.

The Lexer is associated with the index at creation time via the `LEXER` parameter in the `PARAMETERS` clause of `CREATE INDEX`. Once the index exists, changing the Lexer requires a full re-index.
