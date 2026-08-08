---
title: "Oracle Text"
description: "Componentă integrată Oracle Database pentru indexarea și căutarea full-text pe coloane CLOB, BLOB și VARCHAR2, fără licență separată."
translationKey: "glossary_oracle_text"
aka: "Oracle Text (Oracle interMedia Text, ConText)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Oracle Text este motorul de căutare full-text integrat în Oracle Database. Permite indexarea și interogarea unor volume mari de text structurat și nestructurat direct în interiorul bazei de date, fără dependențe externe și fără licență suplimentară față de Standard sau Enterprise Edition.

## Cum funcționează

Oracle Text construiește indecși specializați (`CONTEXT`, `CTXCAT`, `CTXRULE` sau `CTXPATH`) pe coloanele de text. Indexul `CONTEXT` este cel mai utilizat: tokenizează textul, aplică stemming și stoplists, și stochează pozițiile token-urilor în structuri interne optimizate pentru căutare.

Interogările folosesc operatorul `CONTAINS` în clauza `WHERE`:

```sql
SELECT doc_id, title
FROM documents
WHERE CONTAINS(body, 'database AND performance', 1) > 0
ORDER BY SCORE(1) DESC;
```

Indexul trebuie sincronizat manual sau printr-un job programat cu `CTX_DDL.SYNC_INDEX` după operații DML, deoarece nu se actualizează în timp real în cadrul tranzacției.

## Când se utilizează

Oracle Text este alegerea potrivită atunci când:

- volumul de text face impracticabilă utilizarea `LIKE` sau `REGEXP_LIKE` fără degradarea performanței;
- sunt necesare funcționalități avansate precum căutarea prin proximitate, fuzzy matching, expansiunea tematică sau evidențierea rezultatelor;
- documentele se află deja în Oracle Database, iar mutarea datelor către un motor extern (Elasticsearch, Solr) ar introduce o complexitate arhitecturală nejustificată.

Principala limitare este sincronizarea indexului: în scenarii cu rată ridicată de scriere, decalajul dintre DML și actualizarea indexului trebuie planificat explicit.
