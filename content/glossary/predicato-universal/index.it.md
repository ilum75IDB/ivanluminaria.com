---
title: "Predicato universale"
description: "Espressione logica SQL che verifica una condizione su tutte le righe di un insieme, espressa con NOT EXISTS (... WHERE NOT condizione)."
translationKey: "glossary_predicato_universal"
aka: "Quantificatore universale SQL"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un predicato universale afferma che una certa condizione vale per **ogni** riga di un insieme. In logica formale corrisponde al quantificatore ∀ (per ogni). SQL non espone questo quantificatore direttamente, quindi lo si costruisce per negazione doppia.

## Come funziona

L'equivalenza fondamentale è:

> "∀ x: P(x)" ≡ "¬∃ x: ¬P(x)"

In SQL si traduce così:

```sql
-- "tutti gli ordini di questo cliente hanno importo > 0"
SELECT c.id
FROM clienti c
WHERE NOT EXISTS (
    SELECT 1
    FROM ordini o
    WHERE o.cliente_id = c.id
      AND NOT (o.importo > 0)
);
```

Il motore scansiona il sottoinsieme di righe correlate e restituisce il padre solo se non ne trova nemmeno una che violi la condizione. Se l'insieme interno è vuoto, il predicato è soddisfatto per vacuità (vacuous truth).

## Quando si usa

Il predicato universale ricorre tipicamente in scenari di **vincolo relazionale**:

- verificare che tutti i dettagli di una testata rispettino una regola di business (es. tutte le righe di una fattura hanno IVA valorizzata);
- implementare **assertions** logiche in database che non supportano `CREATE ASSERTION` nativa (Oracle 23ai incluso);
- esprimere divisione relazionale ("clienti che hanno acquistato *tutti* i prodotti di una categoria").

Attenzione alla vacuous truth: se la sottoquery non restituisce righe, `NOT EXISTS` è `TRUE` per definizione, il che può produrre falsi positivi se l'insieme di riferimento è vuoto.
