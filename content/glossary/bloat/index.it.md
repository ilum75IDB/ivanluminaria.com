---
title: "Bloat"
description: "Spazio morto accumulato in una tabella o indice PostgreSQL a causa di dead tuples non rimossi, che gonfia la dimensione su disco e degrada le performance delle query."
translationKey: "glossary_bloat"
aka: "Table Bloat / Index Bloat"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

Il **Bloat** è l'accumulo di spazio morto all'interno di una tabella o di un indice PostgreSQL, causato da dead tuples non ancora rimossi dal VACUUM. Una tabella con il 50% di bloat occupa il doppio dello spazio necessario e costringe le scansioni sequenziali a leggere il doppio delle pagine.

## Come funziona

Il bloat si misura confrontando la dimensione effettiva della tabella con la dimensione attesa basata sulle righe vive. L'estensione `pgstattuple` fornisce il campo `dead_tuple_percent`. Un bloat sopra il 20-30% è un segnale di allarme; sopra il 50% è un'emergenza.

## A cosa serve

Monitorare il bloat è essenziale per capire se l'autovacuum sta tenendo il passo. La query `pg_stat_user_tables` con `n_dead_tup` e `last_autovacuum` è il primo strumento diagnostico. Se il bloat è fuori controllo, `pg_repack` ricostruisce la tabella online senza lock esclusivi prolungati — al contrario di `VACUUM FULL`.

## Cosa può andare storto

VACUUM normale recupera lo spazio dei dead tuples ma non compatta la tabella — lo spazio frammentato resta. Se il bloat raggiunge il 50-70%, il VACUUM non basta più. Le opzioni sono `VACUUM FULL` (lock esclusivo, blocca tutto) o `pg_repack` (online, ma richiede installazione). La vera soluzione è non arrivarci, con un autovacuum ben configurato.
