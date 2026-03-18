---
title: "Redo Log"
description: "File di log in cui Oracle registra ogni modifica ai dati prima di scriverla nei datafile, garantendo il recovery in caso di guasto."
translationKey: "glossary_redo_log"
aka: "Online Redo Log, Archived Redo Log"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**Redo Log** è il meccanismo con cui Oracle registra ogni modifica ai dati del database (INSERT, UPDATE, DELETE, DDL) prima che venga scritta definitivamente nei datafile. È la garanzia fondamentale di durabilità delle transazioni.

## Come funziona

Oracle scrive le modifiche nei redo log online in modo sequenziale e continuo. I redo log sono organizzati in gruppi circolari: quando un gruppo si riempie, Oracle passa al successivo. Quando tutti i gruppi sono stati usati, Oracle torna al primo (log switch).

## Online vs Archived

- **Online redo log**: i file attivi dove Oracle scrive in tempo reale. Sono circolari e si sovrascrivono
- **Archived redo log**: copie dei redo log online salvate prima della sovrascrittura. Necessari per il recovery point-in-time e per Data Guard

La modalità `ARCHIVELOG` del database attiva la creazione automatica degli archived log. Senza di essa, i redo vengono sovrascritti e il recovery è limitato all'ultimo backup completo.

## Perché sono importanti

I redo log sono il cuore del recovery e della replica Oracle. Senza redo:

- Non è possibile il recovery dopo un crash (instance recovery)
- Non è possibile il recovery point-in-time (media recovery)
- Data Guard non può funzionare (la replica si basa interamente sui redo)
- Non è possibile il flashback database
