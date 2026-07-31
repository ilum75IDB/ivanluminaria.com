---
title: "Predicat universal"
description: "Expresie logică SQL care verifică dacă o condiție este îndeplinită pentru toate rândurile unui set, exprimată cu NOT EXISTS (... WHERE NOT condiție)."
translationKey: "glossary_predicato_universal"
aka: "Cuantificator universal SQL"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un predicat universal afirmă că o anumită condiție este valabilă pentru **fiecare** rând dintr-un set. În logica formală corespunde cuantificatorului ∀ (pentru orice). SQL nu expune acest cuantificator în mod direct, astfel că se construiește prin dublă negație.

## Cum funcționează

Echivalența de bază este:

> "∀ x: P(x)" ≡ "¬∃ x: ¬P(x)"

În SQL:

```sql
-- "toate comenzile acestui client au suma > 0"
SELECT c.id
FROM clienti c
WHERE NOT EXISTS (
    SELECT 1
    FROM comenzi o
    WHERE o.client_id = c.id
      AND NOT (o.suma > 0)
);
```

Motorul parcurge subsetul corelat și returnează rândul părinte doar atunci când nu găsește niciun rând care să violeze condiția. Dacă setul intern este gol, predicatul este satisfăcut prin adevăr vacuu (vacuous truth).

## Când se folosește

Predicatul universal apare în scenarii de **constrângere relațională**:

- verificarea că toate rândurile de detaliu ale unui antet respectă o regulă de business (de exemplu, toate liniile unei facturi au codul de taxă completat);
- implementarea de **assertions** logice în baze de date care nu suportă nativ `CREATE ASSERTION` (Oracle 23ai inclus);
- exprimarea diviziunii relaționale ("clienți care au cumpărat *toate* produsele dintr-o categorie").

Atenție la adevărul vacuu: dacă subinterogarea nu returnează rânduri, `NOT EXISTS` evaluează la `TRUE` prin definiție, ceea ce poate produce rezultate fals pozitive atunci când setul de referință este gol.
