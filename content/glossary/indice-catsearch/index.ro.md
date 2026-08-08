---
title: "Index CATSEARCH"
description: "Tip de index Oracle Text pentru arhive mixte: rezolvă predicatele SQL pe atribute structurate și căutarea full-text împreună, într-o singură structură de index."
translationKey: "glossary_indice_catsearch"
aka: "CATSEARCH index, Oracle Text CATSEARCH"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Indexul CATSEARCH este un tip specializat de Oracle Text conceput pentru domenii în care fiecare document conține atribute structurate — expeditor, dată, categorie, stare — alături de text liber care trebuie căutat simultan. În loc să combine un index B-tree pe coloane structurate cu un index full-text separat, CATSEARCH fuzionează ambele dimensiuni într-o singură structură.

## Cum funcționează

Indexul se creează folosind `CTXSYS.CTXCAT` ca tip de index și acceptă o listă de coloane structurate de inclus în sub-index. Oracle Text construiește intern un catalog care indexează atât token-urile textuale, cât și valorile coloanelor suplimentare.

```sql
CREATE INDEX idx_doc_catsearch
ON documente(continut)
INDEXTYPE IS CTXSYS.CTXCAT
PARAMETERS ('CTXCAT_INDEX_SET myindexset');
```

Interogările folosesc operatorul `CATSEARCH` în locul clasicului `CONTAINS`:

```sql
SELECT id, titlu
FROM documente
WHERE CATSEARCH(continut, 'factura AND scadenta', 'categorie = ''contabilitate''') > 0;
```

Predicatul structural (`categorie = 'contabilitate'`) este rezolvat în interiorul indexului, nu ca filtru aplicat după scanare.

## Când se folosește

CATSEARCH este potrivit pentru arhive documentare cu cardinalitate medie-ridicată pe coloanele structurate și interogări care combină sistematic filtre pe atribute cu căutare textuală: sisteme de ticketing, arhive de email, depozite de contracte. Nu este alegerea potrivită pentru căutare full-text pură fără predicate structurale, unde `CONTEXT` (cu `CONTAINS`) oferă capabilități lingvistice mai bogate. Sincronizarea indexului necesită atenție: ca toți indexii Oracle Text, CATSEARCH nu se actualizează în timp real fără o politică de sync explicită.
