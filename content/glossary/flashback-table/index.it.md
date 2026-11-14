---
title: "Flashback Table"
description: "Comando Oracle che ripristina un'intera tabella a un punto nel tempo precedente usando i dati di undo, senza interrompere le sessioni attive."
translationKey: "glossary_flashback_table"
aka: "Oracle Flashback Table"
articles:
  - "/posts/oracle/oracle-flashback-recupero-dati-logici-senza-downtime-da-query-a-database"
---

`FLASHBACK TABLE` è un comando DDL/DML di Oracle che riporta un'intera tabella — struttura dei dati inclusa — a uno snapshot precedente, sfruttando i segmenti di undo ancora disponibili nell'istanza. A differenza di un restore tradizionale, opera a livello logico e non richiede downtime del database.

## Come funziona

Il comando legge i blocchi di undo generati dalle transazioni successive al punto target e li applica in ordine inverso sulla tabella. Per funzionare, la tabella deve avere `ROW MOVEMENT` abilitato (necessario per aggiornare i ROWID durante il ripristino) e i dati di undo devono essere ancora presenti nel tablespace UNDO — non sovrascritti da transazioni più recenti.

```sql
-- Prerequisito: abilitare ROW MOVEMENT
ALTER TABLE ordini ENABLE ROW MOVEMENT;

-- Ripristino a un timestamp specifico
FLASHBACK TABLE ordini TO TIMESTAMP
  TO_TIMESTAMP('2025-06-10 14:30:00', 'YYYY-MM-DD HH24:MI:SS');

-- Ripristino a un SCN specifico
FLASHBACK TABLE ordini TO SCN 9823741;
```

## Quando si usa

Lo scenario tipico è il recupero da un errore applicativo o umano: una `DELETE` o `UPDATE` errata eseguita senza `WHERE` corretto, o un `TRUNCATE` accidentale (quest'ultimo recuperabile solo se la tabella è stata droppata e si usa `FLASHBACK DROP`, non `FLASHBACK TABLE`). Il comando è adatto quando:

- la finestra temporale è contenuta (dipende dalla `UNDO_RETENTION` configurata);
- si vuole ripristinare una singola tabella senza coinvolgere le altre;
- le sessioni attive sulle altre tabelle non devono essere interrotte.

I limiti principali sono due: non funziona se i dati di undo sono stati sovrascritti, e non gestisce le dipendenze referenziali — se la tabella ha foreign key verso altre tabelle modificate nel frattempo, il ripristino può generare violazioni di integrità che vanno risolte manualmente.
