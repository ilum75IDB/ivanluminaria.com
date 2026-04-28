---
title: "GiST Index"
description: "Generalized Search Tree — famiglia di indici PostgreSQL per dati con struttura geometrica, range o di similarità, indispensabile per query spaziali e su intervalli."
translationKey: "glossary_gist_index"
aka: "Generalized Search Tree"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

**GiST** (*Generalized Search Tree*) è una famiglia di indici PostgreSQL pensata per dati che non possono essere ordinati linearmente: geometrie, range, vettori di similarità, full-text. È un albero bilanciato che organizza i dati per *bounding box* gerarchici invece che per ordinamento lessicografico.

## Come funziona

Mentre un B-tree ordina i valori da "minimo" a "massimo" e fa ricerca dicotomica, GiST raggruppa i dati in regioni (bounding box) annidate. Ogni nodo dell'albero rappresenta una regione che contiene tutti i dati nei suoi figli. Quando si cerca un valore, GiST scarta intere regioni con un confronto di sovrapposizione — senza scendere nei nodi che non possono contenere il risultato.

Questa struttura permette di indicizzare:

- **Geometrie**: punti, poligoni, linee (con PostGIS)
- **Range**: `int4range`, `tsrange`, `daterange` e altri tipi range
- **Full-text**: vettori `tsvector` per ricerca testuale
- **Similarità**: con estensioni come `pg_trgm` per ricerche approssimate

## A cosa serve

Risolve il problema di query "spaziali" o di intervallo che un B-tree non sa gestire:

- Trova tutti i punti dentro un riquadro o un raggio
- Trova tutti i record con un range che si sovrappone a un altro range
- Trova testi simili a una query, anche con typo
- Cerca per containment: `range1 @> range2` o `geom1 && geom2`

## Quando si usa

Si usa con `CREATE INDEX ... USING GIST (colonna)`. È il complemento naturale di GIN: GIN per containment di array/JSONB, GiST per geometria/range/similarità. Su tabelle ad alto churn ha costo di scrittura simile a GIN — quindi va valutato contesto per contesto.
