---
title: "Indice Parziale"
description: "Indice PostgreSQL che copre solo un sottoinsieme delle righe della tabella, definito con WHERE nella CREATE INDEX. Riduce spazio e tempo di manutenzione."
translationKey: "glossary_indice_parziale"
aka: "Partial Index"
articles:
  - "/posts/postgresql/postgresql-indici-quando-fanno-male"
---

Un **indice parziale** (*partial index*) è un indice PostgreSQL che copre solo un sottoinsieme delle righe della tabella, definito con una clausola `WHERE` nella `CREATE INDEX`. Le righe che non soddisfano la condizione non vengono indicizzate e non occupano spazio nell'indice.

## Come funziona

La sintassi è semplice:

```sql
CREATE INDEX idx_attivi
ON ordini (data_creazione)
WHERE stato = 'attivo';
```

L'indice contiene solo le righe con `stato = 'attivo'`. Tutte le altre vengono ignorate. Il planner usa questo indice solo per query che includono la stessa condizione `WHERE stato = 'attivo'` (o una condizione più restrittiva).

## A cosa serve

Risolve uno scenario comunissimo: la maggior parte delle query operative filtra sempre per una condizione (es. `attivo = true`, `archiviato = false`, `data > x`), e le righe che non soddisfano quella condizione non vengono mai cercate. Indicizzarle è uno spreco.

I benefici concreti:

- **Spazio**: l'indice è più piccolo, a volte molto. Su una tabella dove il 35% delle righe è "attivo", l'indice parziale occupa il 35% dello spazio.
- **Manutenzione**: meno lavoro per il VACUUM, meno write-amplification su INSERT/UPDATE delle righe escluse.
- **Performance**: l'indice è più piccolo da scorrere e tende a stare più facilmente in cache.

## Quando si usa

Si usa quando:

- Le query operative filtrano sistematicamente per una condizione binaria
- Le righe che non soddisfano la condizione sono molte (>50%) e non rilevanti per il workload caldo
- Le query sull'altro sottoinsieme sono rare e vanno bene anche con un seq scan

Da non usare se le query filtrano per condizioni dinamiche o variabili: il planner non userà mai l'indice parziale.
