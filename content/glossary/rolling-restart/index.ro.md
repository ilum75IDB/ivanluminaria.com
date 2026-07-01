---
title: "Rolling Restart"
description: "Procedură de repornire secvențială a nodurilor unui cluster care menține serviciul activ și aplică modificări de configurare fără downtime."
translationKey: "glossary_rolling_restart"
aka: "Repornire secvențială, repornire rotativă"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

**Rolling restart** este tehnica prin care nodurile unui cluster sunt repornite pe rând, câte unul, lăsând celelalte active astfel încât serviciul să rămână disponibil pentru clienți pe toată durata operațiunii. Clusterul trebuie să mențină quorum-ul la fiecare pas pentru a continua să gestioneze scrierile și să aleagă un primary.

## Cum funcționează

Pe un InnoDB Cluster cu 3 noduri, secvența tipică este:

1. Identificarea nodului de repornit (de preferință un secondary).
2. Verificarea că întregul cluster este `ONLINE` și că toți membrii sunt sincronizați.
3. Repornirea nodului (`systemctl restart mysqld` sau echivalent).
4. Așteptarea ca nodul să reintre în grup înainte de a continua cu următorul.

```bash
# Verifică starea clusterului înainte de fiecare pas
mysqlsh -- cluster status
```

Nodul repornit se reconectează la grup prin Group Replication și recuperează tranzacțiile lipsă prin distributed recovery. Doar după ce starea sa revine la `ONLINE` se trece la repornirea nodului următor.

## Când se folosește

Rolling restart este procedura standard ori de câte ori este necesară aplicarea unor modificări la parametrii de configurare MySQL din `my.cnf` care impun repornirea procesului — de exemplu modificări ale `innodb_buffer_pool_size`, `innodb_log_file_size` sau parametri Group Replication. Este, de asemenea, metoda preferată pentru aplicarea patch-urilor de sistem de operare sau a actualizărilor de versiune minore fără a programa o fereastră de mentenanță formală.

Principala limitare este timpul: dacă nodul repornit are un backlog semnificativ de tranzacții de recuperat, faza de distributed recovery poate dura câteva minute, prelungind fereastra operațională totală.
