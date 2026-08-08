---
title: "Index CTXXPATH"
description: "Tip de index Oracle Text pentru documente XML sau JSON stocate în CLOB/BLOB: păstrează ierarhia path-urilor și permite interogări pe noduri specifice."
translationKey: "glossary_indice_ctxxpath"
aka: "CTXXPATH index (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Indexul CTXXPATH este un tip specializat de Oracle Text conceput pentru documente XML sau JSON stocate în coloane `CLOB` sau `BLOB`. Spre deosebire de indexurile full-text generice, CTXXPATH păstrează structura ierarhică a documentului în timpul indexării, permițând limitarea căutărilor la path-uri sau noduri specifice în loc să parcurgă întregul conținut textual.

## Cum funcționează

Indexul se creează cu `CREATE INDEX ... INDEXTYPE IS CTXSYS.CTXXPATH`. Oracle Text analizează documentul, construiește o hartă a path-urilor XML/JSON și indexează atât conținutul textual, cât și poziția structurală a fiecărui nod.

```sql
CREATE INDEX idx_doc_xml
ON documente(continut_xml)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

Interogările folosesc apoi `existsNode` sau operatorul `CONTAINS` cu sintaxă path-aware pentru a delimita căutarea:

```sql
SELECT id
FROM documente
WHERE existsNode(continut_xml, '/factura/client[nume="Popescu"]') = 1;
```

## Când se utilizează

CTXXPATH este alegerea potrivită atunci când documentele au o structură XML sau JSON semnificativă și interogările trebuie să distingă noduri cu același conținut textual aflate în poziții diferite în document. Scenarii tipice: arhive de facturi electronice, cataloage de produse în XML, payload-uri JSON eterogene.

Principala limitare este dependența de format: documentul trebuie să fie XML sau JSON bine format. Pentru text nestructurat, `CTXSYS.CONTEXT` este mai potrivit; pentru căutări pur structurale fără cerințe full-text, indexurile relaționale standard pe coloane extrase cu `XMLTable` sau `JSON_TABLE` sunt suficiente.
