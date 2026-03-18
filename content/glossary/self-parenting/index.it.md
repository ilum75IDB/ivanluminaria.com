---
title: "Self-parenting"
description: "Tecnica di bilanciamento delle gerarchie sbilanciate: chi non ha un padre diventa padre di sé stesso."
translationKey: "glossary_self_parenting"
aka: "Auto-riferimento gerarchico"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

Il **self-parenting** è una tecnica di dimensional modeling usata per bilanciare le gerarchie sbilanciate (ragged hierarchies). Il principio è semplice: un'entità che non ha un livello gerarchico superiore diventa il proprio genitore a quel livello.

## Come funziona

In una gerarchia a tre livelli Top Group → Group → Client:

- Un Client senza Group usa il proprio nome/ID come Group
- Un Group senza Top Group usa il proprio nome/ID come Top Group

Il risultato è una tabella dimensionale senza NULL nelle colonne gerarchiche, con tutti i livelli sempre popolati.

## I flag di distinzione

Per non perdere l'informazione su quali entità sono state bilanciate artificialmente, si aggiungono flag alla dimensione:

- `is_direct_client = 'Y'`: il client non aveva un Group nella sorgente
- `is_standalone_group = 'Y'`: il Group non aveva un Top Group nella sorgente

Questi flag permettono al business di filtrare i "veri" top group dai clienti promossi.

## Perché nell'ETL e non nel report

Il self-parenting si applica una volta nell'ETL, non in ogni singolo report. Un report dovrebbe fare GROUP BY e JOIN, non decidere come gestire i livelli mancanti. Se la logica di bilanciamento è nel modello, tutti i report ne beneficiano automaticamente.
