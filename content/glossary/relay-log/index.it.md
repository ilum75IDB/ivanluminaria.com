---
title: "Relay log"
description: "Il relay log è la copia locale del binlog del master sullo slave MySQL: l'IO thread lo scrive, lo SQL thread lo legge per applicare le transazioni."
translationKey: "glossary_relay_log"
aka: null
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

Il relay log è il file binario che lo slave MySQL mantiene localmente come copia degli eventi ricevuti dal master. Funziona da buffer tra la ricezione degli eventi di replica e la loro applicazione effettiva sul database: due thread distinti si occupano delle due fasi, e il relay log è il punto di contatto tra loro.

## Come funziona

La replica MySQL si articola su due thread separati sullo slave:

- **IO thread**: si connette al master, legge il binlog e scrive gli eventi nel relay log locale.
- **SQL thread**: legge il relay log e applica gli eventi (INSERT, UPDATE, DELETE, DDL) sul database slave.

Questo disaccoppiamento permette allo slave di ricevere eventi anche quando l'SQL thread è in ritardo. I file del relay log seguono una naming convention del tipo `hostname-relay-bin.000001` e vengono ruotati automaticamente.

```sql
-- Verificare lo stato del relay log sullo slave
SHOW SLAVE STATUS\G
-- Campi rilevanti:
-- Relay_Log_File: file corrente letto dall'SQL thread
-- Relay_Log_Pos: posizione corrente
-- Relay_Master_Log_File: file del binlog master corrispondente
-- Exec_Master_Log_Pos: posizione applicata sul master
```

## Contesto operativo

Il relay log è centrale nella diagnosi del lag di replica. Se `Seconds_Behind_Master` cresce, il relay log accumula eventi non ancora applicati: l'IO thread è avanti rispetto all'SQL thread. Monitorare la dimensione dei file di relay log e la differenza tra `Read_Master_Log_Pos` e `Exec_Master_Log_Pos` permette di capire dove si trova il collo di bottiglia.

In caso di crash dello slave, MySQL usa il file `relay-log.info` per riprendere dall'ultima posizione applicata. Con `relay_log_recovery = ON` il relay log viene rigenerato dal master alla ripartenza, riducendo il rischio di corruzione.
