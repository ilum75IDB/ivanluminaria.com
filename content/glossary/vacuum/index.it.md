---
title: "VACUUM"
description: "Comando PostgreSQL che recupera lo spazio occupato dai dead tuples, rendendolo riutilizzabile per nuovi inserimenti senza restituirlo al sistema operativo."
translationKey: "glossary_vacuum"
aka: "PostgreSQL VACUUM"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**VACUUM** è il comando PostgreSQL che recupera lo spazio occupato dai dead tuples (righe morte) e lo rende disponibile per nuovi inserimenti. Non restituisce spazio al sistema operativo, non riorganizza la tabella e non compatta nulla — segna le pagine come riscrivibili.

## Come funziona

`VACUUM tabella` scansiona la tabella, identifica i dead tuples non più visibili a nessuna transazione e ne marca lo spazio come riutilizzabile. È un'operazione leggera che non blocca le scritture e può girare in parallelo con le query normali. `VACUUM FULL` invece riscrive fisicamente l'intera tabella con lock esclusivo — da usare rarissimamente e solo in emergenza.

## A cosa serve

Senza VACUUM, le tabelle con alto traffico di UPDATE e DELETE accumulano dead tuples che occupano spazio su disco e rallentano le scansioni sequenziali. Il VACUUM è il meccanismo di pulizia essenziale che bilancia il costo del modello MVCC di PostgreSQL.

## Perché è critico

L'autovacuum esegue VACUUM automaticamente, ma con i default di PostgreSQL può attivarsi troppo raramente su tabelle ad alto traffico. Su una tabella con 10 milioni di righe, il default aspetta 2 milioni di dead tuples prima di intervenire — abbastanza per degradare visibilmente le performance.
