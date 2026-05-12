---
title: "CHECK constraint"
description: "Vincolo SQL standard che limita i valori ammessi in una colonna tramite un'espressione booleana. In MySQL è realmente applicato solo dalla versione 8.0.16."
translationKey: "glossary_check_constraint"
aka: "CHECK constraint"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

Il **CHECK constraint** è un vincolo SQL standard che limita i valori ammessi in una colonna o in una tabella tramite un'espressione booleana. Quando una `INSERT` o `UPDATE` produrrebbe un valore che viola l'espressione, il database rifiuta l'operazione.

## Come funziona

Si dichiara a livello di colonna o di tabella nel `CREATE TABLE` o si aggiunge dopo con `ALTER TABLE ADD CONSTRAINT`. L'espressione può essere qualunque condizione booleana valida: `status IN ('NEW','ACTIVE','CLOSED')`, `prezzo > 0`, `data_fine >= data_inizio`. Il vincolo viene valutato ad ogni scrittura sulla colonna.

## A cosa serve

Garantire l'integrità del dato direttamente nello schema, senza dover validare a livello applicativo. Particolarmente utile per:

- Limitare un campo a un insieme di valori (alternativa a ENUM)
- Vincoli inter-colonna (es. coerenza di date, somme che devono corrispondere)
- Validazione di formato di base (es. email, codici fiscali)

## Quando si usa in MySQL

Attenzione alla versione: prima di **MySQL 8.0.16** i CHECK constraint venivano parsati e silenziosamente ignorati. Solo dalla 8.0.16 sono realmente applicati. È una cosa che ha sorpreso molti sviluppatori migrati da PostgreSQL o Oracle, dove i CHECK funzionano da sempre.

Rispetto ad ENUM, CHECK è più flessibile (rinominare un valore è solo un `ALTER CONSTRAINT`) ma più verboso. Va bene per insiemi di 5-15 valori che ogni tanto si toccano, senza necessità di attributi aggiuntivi.
