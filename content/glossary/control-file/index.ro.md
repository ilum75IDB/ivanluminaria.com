---
title: "Control File"
description: "Fișier binar Oracle care înregistrează structura fizică a bazei de date: căi datafile, redo log-uri, SCN curent și informații de checkpoint. Indispensabil pentru faza MOUNT."
translationKey: "glossary_control_file"
aka: null
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

Control File-ul este un fișier binar de dimensiuni reduse, menținut în permanență actualizat de Oracle. Conține metadatele structurale ale bazei de date: căile datafile-urilor, căile redo log group-urilor, SCN-ul curent și informațiile de checkpoint. Fără el, instanța nu poate depăși faza de MOUNT.

## Ce înregistrează

Ori de câte ori Oracle execută un CHECKPOINT sau adaugă un fișier la structura bazei de date, Control File-ul este actualizat sincron. Câmpurile principale includ:

- **Numele bazei de date și DBID**
- **Calea și starea fiecărui datafile** (online, offline, read-only)
- **Configurația redo log group-urilor**
- **SCN de checkpoint** — utilizat în timpul recovery-ului pentru a determina punctul de consistență
- **Metadatele backup-urilor RMAN** (când se folosește Recovery Manager)

## Multiplexare și riscul de pierdere

Oracle permite — și recomandă — păstrarea unor copii identice ale Control File-ului pe căi fizic separate. Configurarea se face prin parametrul `CONTROL_FILES`:

```sql
ALTER SYSTEM SET CONTROL_FILES =
  '/u01/oradata/orcl/control01.ctl',
  '/u02/fast_recovery_area/orcl/control02.ctl'
SCOPE=SPFILE;
```

Toate copiile sunt scrise în paralel la fiecare actualizare. Dacă o copie este coruptă sau lipsește, baza de date pornește în continuare folosind copiile valide. Pierderea **tuturor** copiilor fără un backup recent necesită un recovery manual complex.

## Context operațional

În timpul startup-ului, Oracle citește Control File-ul în faza MOUNT pentru a localiza datafile-urile înainte de a le deschide (faza OPEN). Într-un mediu Data Guard, Control File-ul standby-ului conține și metadatele de sincronizare cu primary-ul. În backup-urile RMAN, Control File-ul (sau un Catalog separat) funcționează ca registru central pentru toate backup set-urile și image copy-urile.
