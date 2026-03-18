---
title: "Local Index"
description: "Indice Oracle partizionato con la stessa chiave della tabella, dove ogni partizione della tabella ha la sua partizione di indice corrispondente. Più manutenibile di un indice globale."
translationKey: "glossary_local-index"
articles:
  - "/posts/oracle/oracle-partitioning"
---

Un **Local Index** è un indice Oracle creato su una tabella partizionata, che viene automaticamente partizionato con la stessa chiave e gli stessi limiti della tabella. Ogni partizione della tabella ha una corrispondente partizione di indice.

## Come funziona

Quando si crea un indice con la clausola `LOCAL`, Oracle crea una partizione di indice per ogni partizione della tabella. Se la tabella ha 100 partizioni mensili, l'indice avrà 100 partizioni corrispondenti. Le operazioni DDL su una partizione (DROP, TRUNCATE, SPLIT) invalidano solo la partizione di indice corrispondente, non l'intero indice.

## A cosa serve

Il Local Index è la scelta preferita per indici su tabelle partizionate perché mantiene l'indipendenza delle partizioni. Un `DROP PARTITION` richiede meno di un secondo e non invalida nessun altro indice. Con un indice globale, la stessa operazione invaliderebbe l'intero indice, richiedendo ore di rebuild.

## Quando si usa

Si usa quando l'indice include la chiave di partizione o quando le query filtrano sempre sulla colonna di partizione. Per lookup puntuali su colonne non-partition (es. primary key), serve invece un indice globale. La regola: local dove possibile, global solo dove necessario.
