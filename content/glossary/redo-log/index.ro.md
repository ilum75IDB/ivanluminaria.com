---
title: "Redo Log"
description: "Fisiere de log in care Oracle inregistreaza fiecare modificare a datelor inainte de a o scrie in datafile-uri, asigurand recuperarea in caz de defectiune."
translationKey: "glossary_redo_log"
aka: "Online Redo Log, Archived Redo Log"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**Redo Log** este mecanismul prin care Oracle inregistreaza fiecare modificare a datelor (INSERT, UPDATE, DELETE, DDL) inainte ca aceasta sa fie scrisa definitiv in datafile-uri. Este garantia fundamentala a durabilitatii tranzactiilor.

## Cum functioneaza

Oracle scrie modificarile in redo log-urile online secvential si continuu. Redo log-urile sunt organizate in grupuri circulare: cand un grup se umple, Oracle trece la urmatorul. Cand toate grupurile au fost folosite, Oracle revine la primul (log switch).

## Online vs Archived

- **Online redo log**: fisierele active unde Oracle scrie in timp real. Sunt circulare si se suprascriu
- **Archived redo log**: copii ale redo log-urilor online salvate inainte de suprascriere. Necesare pentru recuperarea point-in-time si pentru Data Guard

Modul `ARCHIVELOG` al bazei de date activeaza crearea automata a archived log-urilor. Fara acesta, redo log-urile sunt suprascrise si recuperarea este limitata la ultimul backup complet.

## De ce sunt importante

Redo log-urile sunt inima recuperarii si replicarii in Oracle. Fara redo:

- Recuperarea dupa un crash nu este posibila (instance recovery)
- Recuperarea point-in-time nu este posibila (media recovery)
- Data Guard nu poate functiona (replicarea se bazeaza in intregime pe redo)
- Flashback database nu este posibil
