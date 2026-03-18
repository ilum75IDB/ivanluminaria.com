---
title: "B-Tree"
description: "Struttura dati ad albero bilanciato, tipo di indice predefinito nella maggior parte dei database relazionali. Efficiente per ricerche di uguaglianza e range, ma inadatto per LIKE con wildcard iniziale."
translationKey: "glossary_b-tree"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

Il **B-Tree** (Balanced Tree) è la struttura dati più comune per gli indici nei database relazionali ed è il tipo di indice predefinito in PostgreSQL, MySQL e Oracle. Mantiene i dati ordinati in una struttura ad albero bilanciato che garantisce tempi di ricerca logaritmici.

## Come funziona

Un B-Tree organizza le chiavi in nodi ordinati, con ogni nodo che contiene puntatori ai nodi figli. La ricerca parte dalla radice e scende verso le foglie, dimezzando lo spazio di ricerca ad ogni livello. Per una tabella di 6 milioni di righe, un B-Tree richiede tipicamente 3-4 livelli di profondità, quindi 3-4 letture di pagina per trovare un valore.

## A cosa serve

I B-Tree sono ottimali per ricerche di uguaglianza (`WHERE col = 'valore'`), range (`WHERE col BETWEEN x AND y`), ordinamento e ricerche con prefisso (`LIKE 'ABC%'`). Non possono però essere usati per ricerche con wildcard iniziale (`LIKE '%ABC%'`), perché l'ordinamento del B-Tree non aiuta a trovare sottostringhe in posizioni arbitrarie.

## Quando si usa

Il B-Tree è la scelta giusta per la maggior parte degli indici. Quando serve una ricerca "contiene" su testo, bisogna passare a un indice GIN con l'estensione pg_trgm. La scelta tra B-Tree e GIN dipende dal tipo di query e dal profilo di carico della tabella.
