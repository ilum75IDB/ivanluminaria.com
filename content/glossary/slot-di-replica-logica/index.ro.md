---
title: "Slot de replicare logică"
description: "Structură PostgreSQL persistentă pe publisher care urmărește poziția de consum a WAL-urilor per subscriber. Protejează împotriva pierderii de date la deconectare."
translationKey: "glossary_slot_di_replica_logica"
aka: "Logical Replication Slot"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**Slot-ul de replicare logică** este o structură persistentă pe publisher-ul PostgreSQL care memorează poziția de consum a WAL-urilor pentru fiecare subscriber. Garantează că nicio modificare nu se pierde chiar dacă subscriber-ul se deconectează temporar: segmentele WAL sunt reținute până când au fost consumate și confirmate.

## De ce există

Fără un slot, PostgreSQL reciclează segmentele WAL imediat ce devin de prisos pentru crash recovery — tipic în câteva minute pe sisteme active. Un subscriber deconectat timp de o oră s-ar trezi cu un gol nerecuperabil și singura ieșire ar fi reinițializarea subscription-ului din snapshot. Slot-ul rezolvă această problemă păstrând WAL-urile disponibile.

## Riscul slot-ului orfan

Un slot care nu mai consumă (subscriber crash-uit, dropped fără să fi eliminat înainte slot-ul, migrare întreruptă) **continuă să rețină WAL la infinit**, umplând discul publisher-ului. Este cauza numărul unu de outage din replicarea logică în producție.

## Monitorizare esențială

View-ul `pg_replication_slots` expune `active` (este în uz?), `restart_lsn` (de unde ar relua), iar calculând delta-ul între `pg_current_wal_lsn()` și `restart_lsn` se obține volumul de WAL reținut. Pe sisteme critice este obligatoriu un alert când delta-ul depășește un prag (de exemplu 10 GB) sau când un slot rămâne `active = false` prea mult timp. Din PostgreSQL 13 există și `max_slot_wal_keep_size` ca limită de siguranță.
