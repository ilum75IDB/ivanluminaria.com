---
title: "Query Rewriting"
description: "Funcționalitate Oracle care redirecționează automat interogările pe tabelele de bază către o Materialized View echivalentă, fără modificări în codul aplicației."
translationKey: "glossary_query_rewriting"
aka: "Automatic Query Rewriting"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Query Rewriting este o capabilitate a optimizatorului de interogări Oracle care interceptează instrucțiuni SQL adresate tabelelor de bază și le redirecționează transparent către o Materialized View (MV) ce conține deja rezultatul pre-calculat. Aplicația nu știe nimic despre această substituție: trimite aceeași interogare ca întotdeauna și primește datele mai rapid.

## Cum funcționează

Când o MV este creată sau modificată cu `ENABLE QUERY REWRITE`, optimizatorul este autorizat să o folosească drept sursă alternativă de date. Oracle verifică că MV este semantic echivalentă cu interogarea primită — aceleași agregări, aceleași coloane, aceeași logică de filtrare — și, dacă potrivirea este validă, înlocuiește planul de execuție.

```sql
CREATE MATERIALIZED VIEW mv_trafic_zilnic
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT data_apel, id_celula, SUM(durata_sec) AS total_durata
FROM fapt_apeluri
GROUP BY data_apel, id_celula;
```

După această definiție, o interogare de tipul `SELECT data_apel, SUM(durata_sec) FROM fapt_apeluri GROUP BY data_apel` poate fi rezolvată citind MV în loc de tabela de bază, ori de câte ori optimizatorul consideră că este avantajos.

## Când se folosește

Query Rewriting este cel mai eficient în Data Warehouse-uri cu interogări analitice grele și repetitive pe aceleași agregări. Condiția esențială este că MV să fie **proaspătă**: dacă datele sunt depășite față de tabela de bază, Oracle poate alege să nu o folosească — comportament controlabil prin parametrul `QUERY_REWRITE_INTEGRITY`. Parametrul de sesiune sau sistem `QUERY_REWRITE_ENABLED` trebuie de asemenea activat. În medii cu refresh-uri frecvente sau near-real-time, beneficiul scade și trebuie cântărit costul refresh-ului față de câștigul la citire.
