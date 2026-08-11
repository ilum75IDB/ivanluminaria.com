---
title: "Relay log"
description: "Relay log-ul este copia locală a binlog-ului masterului pe slave-ul MySQL: IO thread-ul îl scrie, SQL thread-ul îl citește pentru a aplica tranzacțiile."
translationKey: "glossary_relay_log"
aka: null
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

Relay log-ul este fișierul binar pe care slave-ul MySQL îl menține local ca o copie a evenimentelor primite de la master. Funcționează ca un buffer între recepția evenimentelor de replicare și aplicarea lor efectivă în baza de date: două thread-uri distincte gestionează fiecare fază, iar relay log-ul reprezintă punctul de legătură dintre ele.

## Cum funcționează

Replicarea MySQL pe slave se bazează pe două thread-uri independente:

- **IO thread**: se conectează la master, citește binlog-ul și scrie evenimentele în relay log-ul local.
- **SQL thread**: citește relay log-ul și aplică evenimentele (INSERT, UPDATE, DELETE, DDL) pe baza de date slave.

Această separare permite slave-ului să primească în continuare evenimente chiar și atunci când SQL thread-ul rămâne în urmă. Fișierele relay log urmează o convenție de denumire de tipul `hostname-relay-bin.000001` și sunt rotite automat.

```sql
-- Verificarea stării relay log-ului pe slave
SHOW SLAVE STATUS\G
-- Câmpuri relevante:
-- Relay_Log_File: fișierul curent citit de SQL thread
-- Relay_Log_Pos: poziția curentă
-- Relay_Master_Log_File: fișierul binlog al masterului corespunzător
-- Exec_Master_Log_Pos: poziția aplicată pe master
```

## Context operațional

Relay log-ul este esențial pentru diagnosticarea lag-ului de replicare. Când `Seconds_Behind_Master` crește, relay log-ul acumulează evenimente neaplicare încă: IO thread-ul este înaintea SQL thread-ului. Monitorizarea dimensiunii fișierelor relay log și a diferenței dintre `Read_Master_Log_Pos` și `Exec_Master_Log_Pos` permite identificarea blocajului.

După un crash al slave-ului, MySQL folosește fișierul `relay-log.info` pentru a relua de la ultima poziție aplicată. Cu `relay_log_recovery = ON`, relay log-ul este regenerat de la master la repornire, reducând riscul de corupție.
