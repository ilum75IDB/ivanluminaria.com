---
title: "PGA (Program Global Area)"
description: "La PGA è l'area di memoria privata allocata da Oracle per ogni sessione. Una configurazione errata degrada sort e hash join in modo difficile da tracciare."
translationKey: "glossary_pga"
aka: "Program Global Area"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

La PGA (Program Global Area) è un'area di memoria privata che Oracle alloca per ogni processo server o sessione. A differenza della SGA (System Global Area), condivisa tra tutte le sessioni, la PGA è esclusiva: contiene lo spazio di lavoro per operazioni di sort, hash join, bitmap merge e le variabili di sessione.

## Come funziona

Oracle gestisce la PGA in modalità automatica (`PGA_AGGREGATE_TARGET`) o manuale. In modalità automatica, il database stima la memoria disponibile e la distribuisce tra le sessioni attive. Quando la PGA allocata supera il target, Oracle riversa i dati su disco (temp tablespace), degradando le prestazioni.

```sql
-- Verifica configurazione PGA corrente
SELECT name, value
FROM v$pgastat
WHERE name IN (
  'aggregate PGA target parameter',
  'aggregate PGA auto target',
  'total PGA inuse',
  'cache hit percentage'
);
```

Il parametro `WORKAREA_SIZE_POLICY` controlla se la gestione è `AUTO` o `MANUAL`. In modalità manuale, parametri come `SORT_AREA_SIZE` e `HASH_AREA_SIZE` definiscono i limiti per sessione.

## Contesto operativo

Una PGA sottodimensionata produce spill su disco frequenti: le query con ORDER BY, GROUP BY o hash join diventano lente senza che gli alert standard (CPU, I/O aggregato) lo evidenzino chiaramente. Il degrado è spesso correlato a picchi di sessioni concorrenti, non a query singole.

Una PGA non documentata o modificata senza traccia nei change log è una delle cause più insidiose di regressioni prestazionali: il sintomo appare in produzione, ma la causa risale a una modifica di parametro avvenuta settimane prima.
