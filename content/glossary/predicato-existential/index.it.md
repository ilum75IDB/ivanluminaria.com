---
title: "Predicato Existential"
description: "Espressione logica SQL che verifica l'esistenza di almeno una riga in una subquery correlata, base dei pattern EXISTS e NOT EXISTS."
translationKey: "glossary_predicato_existential"
aka: "Existential predicate, predicato di esistenza"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un **predicato existential** è un'espressione logica che restituisce `TRUE` se esiste almeno una riga che soddisfa una condizione data. In SQL è il meccanismo alla base degli operatori `EXISTS` e `NOT EXISTS`, usati tipicamente in subquery correlate per verificare la presenza o l'assenza di dati correlati senza recuperarli esplicitamente.

## Come funziona

Il motore valuta la subquery correlata riga per riga rispetto alla query esterna. Non appena trova la prima riga che soddisfa la condizione, restituisce `TRUE` e interrompe la scansione (short-circuit evaluation). Questo lo rende spesso più efficiente di un `JOIN` o di un `IN` su grandi dataset.

```sql
-- Verifica che esista almeno un ordine attivo per ogni cliente
SELECT c.id, c.nome
FROM clienti c
WHERE EXISTS (
    SELECT 1
    FROM ordini o
    WHERE o.cliente_id = c.id
      AND o.stato = 'ATTIVO'
);
```

Il `SELECT 1` nella subquery è convenzionale: il valore proiettato è irrilevante, conta solo l'esistenza della riga.

## Quando si usa

Il predicato existential è il pattern naturale per implementare **Assertions di tipo "almeno uno"**: vincoli o controlli che richiedono la presenza garantita di almeno un record correlato. In Oracle 23ai, dove le Assertions dichiarative non sono ancora esposte come oggetti DDL nativi, `EXISTS` in trigger o check constraint è il sostituto operativo standard.

`NOT EXISTS` copre il caso complementare — nessuna riga deve soddisfare la condizione — utile per vincoli di esclusione o per rilevare gap in serie temporali.

Un limite da tenere presente: su subquery non correlate o su colonne non indicizzate, il costo può degradare a scansione completa. L'analisi del piano di esecuzione (`EXPLAIN PLAN`) è sempre consigliata prima di portare in produzione query con `EXISTS` su tabelle di grandi dimensioni.
