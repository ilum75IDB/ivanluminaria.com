---
title: "MVCC"
description: "Multi-Version Concurrency Control — modello di concorrenza di PostgreSQL che mantiene più versioni delle righe per garantire isolamento transazionale senza lock esclusivi sulle letture."
translationKey: "glossary_mvcc"
aka: "Multi-Version Concurrency Control"
articles:
  - "/posts/postgresql/vacuum-autovacuum-postgresql"
---

**MVCC** (Multi-Version Concurrency Control) è il modello di concorrenza usato da PostgreSQL per gestire l'accesso simultaneo ai dati. Ogni UPDATE crea una nuova versione della riga e segna la vecchia come "morta"; ogni DELETE marca la riga come non più visibile. Le letture non bloccano le scritture e viceversa.

## Come funziona

Ogni transazione vede uno snapshot consistente del database al momento del suo inizio. Le righe modificate da altre transazioni non ancora committate sono invisibili. Questo elimina la necessità di lock esclusivi sulle letture, permettendo alta concorrenza — ma genera "spazzatura" sotto forma di dead tuples che devono essere puliti dal VACUUM.

## A cosa serve

MVCC è il compromesso architetturale di PostgreSQL: concorrenza elevata senza lock, al prezzo di dover gestire la pulizia delle versioni obsolete. È un prezzo ragionevole — a patto che l'autovacuum sia configurato correttamente per tenere il passo con il ritmo di modifica delle tabelle.

## Perché è critico

Se il VACUUM non riesce a tenere il passo con la velocità di generazione dei dead tuples, le tabelle si gonfiano (bloat), le scansioni sequenziali rallentano e gli indici diventano inefficienti. Il pattern classico: lunedì il database va bene, venerdì è un disastro.
