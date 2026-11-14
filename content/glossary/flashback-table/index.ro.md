---
title: "Flashback Table"
description: "Comandă Oracle care restaurează o tabelă întreagă la un moment anterior în timp folosind datele de undo, fără a întrerupe sesiunile active pe alte tabele."
translationKey: "glossary_flashback_table"
aka: "Oracle Flashback Table"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

`FLASHBACK TABLE` este o comandă DDL/DML Oracle care readuce o tabelă întreagă — inclusiv datele din rânduri — la un snapshot anterior, folosind segmentele de undo încă disponibile în instanță. Spre deosebire de o restaurare tradițională, operează la nivel logic și nu necesită downtime al bazei de date.

## Cum funcționează

Comanda citește blocurile de undo generate de tranzacțiile ulterioare punctului țintă și le aplică în ordine inversă asupra tabelei. Sunt necesare două condiții: tabela trebuie să aibă `ROW MOVEMENT` activat (necesar pentru reasignarea ROWID-urilor în timpul restaurării) și datele de undo trebuie să fie încă prezente în tablespace-ul UNDO — nesuprascrise de tranzacții mai recente.

```sql
-- Condiție prealabilă: activarea ROW MOVEMENT
ALTER TABLE comenzi ENABLE ROW MOVEMENT;

-- Restaurare la un timestamp specific
FLASHBACK TABLE comenzi TO TIMESTAMP
  TO_TIMESTAMP('2025-06-10 14:30:00', 'YYYY-MM-DD HH24:MI:SS');

-- Restaurare la un SCN specific
FLASHBACK TABLE comenzi TO SCN 9823741;
```

## Când se folosește

Scenariul tipic este recuperarea după o eroare aplicativă sau umană: un `DELETE` sau `UPDATE` executat fără clauza `WHERE` corectă, sau un `TRUNCATE` accidental (acesta din urmă este recuperabil doar dacă tabela a fost ștearsă cu DROP și se folosește `FLASHBACK DROP`). Comanda este potrivită când:

- fereastra de timp este redusă (limitată de valoarea configurată pentru `UNDO_RETENTION`);
- trebuie restaurată o singură tabelă fără a afecta celelalte;
- sesiunile active pe alte tabele nu trebuie întrerupte.

Două limitări principale: operațiunea eșuează dacă datele de undo au fost deja suprascrise, și nu gestionează dependențele referențiale — dacă tabela are foreign key-uri către alte tabele modificate în intervalul respectiv, restaurarea poate genera violări de integritate care trebuie rezolvate manual.
