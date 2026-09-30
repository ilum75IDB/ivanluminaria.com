---
title: "Plan de execuție"
description: "Secvența de operații aleasă de optimizatorul SQL pentru a executa o interogare: scanări, join-uri, sortări. Statisticile învechite îl degradează fără semnal vizibil."
translationKey: "glossary_piano_di_esecuzione"
aka: "Query execution plan, Query plan"
articles:
  - "/posts/project-management/il-preventivo-dell-upgrade-e-la-domanda-che-non-e-istintiva"
---

Planul de execuție este rețeta pe care motorul bazei de date o urmează pentru a răspunde la o interogare SQL. Optimizatorul evaluează mai multe strategii posibile — ce indecși să folosească, în ce ordine să unească tabelele, dacă să sorteze înainte sau după join — și o alege pe cea cu costul estimat cel mai mic. Rezultatul este un arbore de operatori executați în secvență.

## Cum funcționează

Optimizatorul se bazează pe **statistici** (distribuția valorilor, cardinalitatea tabelelor, selectivitatea indecșilor) pentru a estima costul fiecărui plan candidat. În PostgreSQL punctul de plecare este `EXPLAIN` sau `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending';
```

Rezultatul afișează fiecare nod (Seq Scan, Index Scan, Hash Join, Sort…), costul estimat și — cu `ANALYZE` — timpul real și rândurile efectiv procesate. Diferența dintre rândurile estimate și cele reale este primul semnal al unor statistici învechite.

## Când devine o problemă

Un plan degradat apare de obicei după:

- **încărcări masive** care modifică distribuția datelor fără un `ANALYZE` ulterior;
- **upgrade-uri de versiune** ale motorului, unde optimizatorul își schimbă euristicile;
- **creșterea organică** a tabelelor peste pragurile pentru care planul fusese calibrat.

Simptomul clasic este o interogare care rula în milisecunde și dintr-o dată durează zeci de secunde, fără nicio modificare în codul aplicației. Adăugarea de hardware nu rezolvă problema: un Full Table Scan peste 500 de milioane de rânduri rămâne costisitor indiferent de RAM-ul disponibil. Remediul este actualizarea statisticilor (`ANALYZE`, `UPDATE STATISTICS`, `DBMS_STATS`) și verificarea că optimizatorul alege planul așteptat.
