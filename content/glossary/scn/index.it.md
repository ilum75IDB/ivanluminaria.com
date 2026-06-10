---
title: "SCN"
description: "System Change Number: il numero sequenziale monotono crescente con cui Oracle marca ogni COMMIT e garantisce consistenza e recovery point-in-time."
translationKey: "glossary_scn"
aka: "System Change Number"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

L'SCN (System Change Number) è il contatore interno con cui Oracle ordina ogni modifica avvenuta nel database. Cresce in modo strettamente monotono: ogni COMMIT ottiene un SCN più alto del precedente, rendendo possibile ricostruire con precisione lo stato del database in qualsiasi momento passato.

## Come funziona

Ogni volta che una transazione esegue un COMMIT, Oracle assegna un SCN univoco e lo registra nel redo log, nel control file e negli header dei datafile. Questo valore è il punto di riferimento per tutte le operazioni di consistenza.

```sql
-- Lettura dell'SCN corrente del database
SELECT CURRENT_SCN FROM V$DATABASE;

-- SCN registrato nell'header di un datafile
SELECT NAME, CHECKPOINT_CHANGE# FROM V$DATAFILE;
```

Durante un'istanza recovery, Oracle confronta l'SCN del control file con quello degli header dei datafile per determinare quali blocchi necessitano di redo e quali sono già consistenti.

## Contesto operativo

L'SCN è centrale in tre scenari principali:

- **Point-in-time recovery (PITR)**: si specifica un SCN target e Oracle riapplica il redo fino a quel punto esatto.
- **Flashback**: le funzionalità Flashback Query e Flashback Database usano l'SCN per navigare nella storia dei dati.
- **Data Guard e replication**: lo standby applica l'archived redo fino all'SCN trasmesso dal primary, garantendo la sincronizzazione.

L'SCN ha un limite teorico massimo (legato all'architettura a 48 bit nelle versioni recenti), ma in condizioni normali non rappresenta un vincolo operativo. Situazioni anomale di SCN headroom ridotto sono monitorabili tramite `V$DATABASE_INCARNATION` e le note MOS correlate.
