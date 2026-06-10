---
title: "Online Redo Log"
description: "Fișiere circulare Oracle care înregistrează fiecare modificare a bazei de date înainte de scrierea pe datafile-uri: baza mecanismului de recovery după crash."
translationKey: "glossary_online_redo_log"
aka: "Redo Log, Online Redo Log Files"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

Online Redo Log este structura pe care Oracle o folosește pentru a garanta durabilitatea tranzacțiilor. Fiecare modificare — INSERT, UPDATE, DELETE, DDL — generează o **redo entry** scrisă în redo log *înainte* de a fi aplicată pe datafile-uri. După un crash, Oracle recitește aceste intrări pentru a readuce baza de date la o stare consistentă.

## Cum funcționează

Redo log-urile sunt organizate în **grupuri** (minimum două; trei sau mai multe recomandate în producție). Oracle scrie circular: umple grupul activ, execută un **log switch** și trece la următorul. Fiecare grup poate conține mai mulți **membri** — copii fizice identice pe discuri separate — pentru redundanță.

Procesul de fundal **LGWR** (Log Writer) descarcă redo buffer-ul din memorie în log-ul curent în patru situații: la fiecare COMMIT, când buffer-ul atinge 30% din capacitate, la fiecare 3 secunde sau înainte ca **DBWR** să scrie blocurile murdare.

```sql
-- Verificarea stării grupurilor de redo log
SELECT group#, members, bytes/1024/1024 AS mb, status
FROM v$log
ORDER BY group#;

-- Verificarea membrilor fizici
SELECT group#, member, status
FROM v$logfile
ORDER BY group#;
```

## Context operațional

Dimensionarea corectă a grupurilor de redo log este critică: grupurile prea mici provoacă log switch-uri frecvente, degradând performanța și crescând sarcina pe ARCH (procesul de arhivare, când baza de date rulează în modul **ARCHIVELOG**). Grupurile prea mari prelungesc timpii de recovery.

Un log switch la fiecare 15–30 de minute este un punct de plecare uzual. În medii cu scrieri intense — încărcări masive, pipeline-uri ETL — switch-urile mai frecvente sunt de așteptat; răspunsul obișnuit este creșterea dimensiunii grupurilor sau adăugarea de grupuri noi.

Dacă un grup nu poate fi suprascris deoarece ARCH nu a arhivat încă log-ul anterior, baza de date se blochează în așteptare. Acesta este unul dintre cele mai frecvente blocaje în producție legate de configurarea redo log-ului.
