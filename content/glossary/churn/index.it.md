---
title: "Churn"
description: "Misura di quanto una tabella database cambia dopo l'inserimento iniziale dei dati, in termini di UPDATE e DELETE. Determina il costo di manutenzione degli indici."
translationKey: "glossary_churn"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

Il **churn** di una tabella è la misura di quanto i suoi dati cambiano dopo l'inserimento. Una tabella con alto churn subisce frequenti UPDATE e DELETE; una tabella con basso churn è prevalentemente append-only (solo INSERT).

## Come funziona

In PostgreSQL, ogni UPDATE crea una nuova versione della riga (a causa del modello MVCC) e la vecchia versione diventa una dead tuple. Le DELETE creano anch'esse dead tuples. Più alto è il churn, più lavoro devono fare VACUUM e gli indici per mantenere le performance. Un indice GIN su una tabella ad alto churn può degradare significativamente le performance di scrittura.

## A cosa serve

Valutare il churn prima di creare un indice è essenziale per evitare di risolvere un problema di lettura creandone uno di scrittura. Su una tabella append-only (zero UPDATE, zero DELETE, zero dead tuples), un indice GIN ha un impatto minimo sulle scritture. Su una tabella ad alto churn, lo stesso indice potrebbe diventare un collo di bottiglia.

## Quando si usa

Il churn si analizza verificando le statistiche della tabella: numero di UPDATE e DELETE giornalieri, dead tuples, frequenza di VACUUM. In PostgreSQL, `pg_stat_user_tables` fornisce queste metriche. La decisione di aggiungere un indice GIN o trigram dovrebbe sempre partire da questa analisi.
