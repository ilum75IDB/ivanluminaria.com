---
title: "Index CONTEXT"
description: "Index Oracle Text pentru căutare full-text pe conținut nestructurat: construiește o structură invertită token→document peste coloane CLOB."
translationKey: "glossary_indice_context"
aka: "CONTEXT index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Indexul CONTEXT este tipul principal de index din Oracle Text, proiectat pentru căutarea full-text în coloane care conțin text nestructurat: documente, articole, opinii juridice, note tehnice. Spre deosebire de un index B-tree clasic, nu indexează valori discrete, ci tokeni lingvistici, construind o structură invertită care mapează fiecare cuvânt la documentele în care apare.

## Cum funcționează

La creare, Oracle Text tokenizează conținutul coloanei (de obicei `CLOB`), aplică filtre lingvistice (stemming, stopwords, thesaurus opțional) și populează o serie de tabele interne — `$I`, `$K`, `$R`, `$N` — care formează indexul invertat. Interogările folosesc operatorul `CONTAINS` în locul lui `LIKE`:

```sql
SELECT doc_id, SCORE(1) AS relevanta
FROM documente
WHERE CONTAINS(text, 'contract AND (inchiriere OR arenda)', 1) > 0
ORDER BY relevanta DESC;
```

Indexul evită scanarea secvențială completă a coloanei CLOB la fiecare interogare, reducând drastic timpii de răspuns pe seturi de date de mari dimensiuni.

## Când se utilizează

Indexul CONTEXT este potrivit atunci când:

- coloana conține text lung și variabil (documente, PDF-uri convertite, XML);
- interogările necesită operatori booleeni, căutare prin proximitate sau recuperare bazată pe concept;
- volumul de date face impracticabil orice demers bazat pe `LIKE '%...%'`.

O limitare operațională semnificativă: indexul CONTEXT **nu se actualizează în timp real**. Rândurile inserate sau modificate după crearea indexului devin căutabile doar după o sincronizare explicită (`CTX_DDL.SYNC_INDEX`) sau printr-un job programat. Pentru scenarii cu scrieri frecvente, trebuie planificată o strategie de sincronizare aliniată cu latența de căutare acceptabilă.
