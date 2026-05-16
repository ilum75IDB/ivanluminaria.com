---
title: "ASSERTION"
description: "Costrutto SQL standard per esprimere vincoli cross-tabella validati a livello transazionale dal motore del database. Annunciato in Oracle 26ai."
translationKey: "glossary_sql_assertion"
aka: "SQL ASSERTION (cross-table constraint)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

L'**`ASSERTION`** è un costrutto previsto dallo standard SQL — fin dagli anni '90 — per esprimere vincoli che **attraversano più tabelle**, validati direttamente dal motore del database a livello transazionale. Sulla carta è una soluzione elegante a problemi che oggi si risolvono con trigger o con check applicativi. Nella pratica, fino al 2026, nessun DBMS mainstream l'aveva implementata davvero. Oracle l'ha annunciata per la 26ai.

## Come funziona (sulla carta)

`CREATE ASSERTION nome CHECK (<condizione>)` definisce una condizione che il database garantisce sempre vera. A differenza di un `CHECK` di tabella (che valuta una singola riga al momento dell'INSERT/UPDATE), una `ASSERTION` può fare riferimento a **più tabelle**, fare aggregazioni, contare righe. Esempio: "almeno una riga in `stati_x` deve avere `attivo='Y'`", oppure "la somma di importi in `riga_ordine` non può superare il `totale` in `ordine`".

## Perché ha tardato tanto

Implementare le `ASSERTION` in modo efficiente è difficile. Ad ogni modifica delle tabelle coinvolte il motore deve rivalidare l'asserzione — e farlo senza serializzare tutte le transazioni richiede meccanismi sofisticati di incremental checking o di lock cross-tabella. Nessun vendor ha mai trovato la formula vincente. Oracle 26ai sarà il primo tentativo serio su un DBMS commerciale di rilievo.

## Cosa cambia per chi modella enumerazioni

Per le tassonomie gestite con lookup table, le `ASSERTION` aprono uno scenario nuovo: vincoli che oggi vivono come trigger applicativi (es. "la tassonomia non può restare senza stati attivi") diventeranno esprimibili in DDL, validati a livello transazionale, gestiti dal motore. È materia che si sviluppa quando l'implementazione 26ai sarà disponibile in test.
