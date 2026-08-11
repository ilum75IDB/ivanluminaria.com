---
title: "Binlog"
description: "Il Binary Log di MySQL registra in sequenza ogni modifica ai dati: è il meccanismo su cui si fonda la replica master-slave e il CDC."
translationKey: "glossary_binlog"
aka: "Binary Log"
articles:
  - "/posts/mysql/mysql-slave-lag-parallel-replication"
---

Il Binlog (Binary Log) è il registro sequenziale che MySQL mantiene sul master per tracciare ogni operazione che modifica i dati. Lo slave lo legge per sapere esattamente cosa replicare, nell'ordine in cui è avvenuto. Senza Binlog non esiste replica, e senza replica non esiste alta disponibilità né disaster recovery su MySQL.

## Come funziona

Ogni COMMIT scrive nel Binlog uno o più eventi, a seconda del formato scelto:

- **ROW**: registra le righe effettivamente modificate (before/after image). Più verboso, ma deterministico.
- **STATEMENT**: registra la query SQL testuale. Compatto, ma alcune funzioni non deterministiche (`NOW()`, `UUID()`) possono causare divergenze.
- **MIXED**: MySQL sceglie automaticamente ROW o STATEMENT per ogni istruzione.

```sql
-- Verificare il formato attivo
SHOW VARIABLES LIKE 'binlog_format';

-- Ispezionare gli eventi di un file binlog
SHOW BINLOG EVENTS IN 'mysql-bin.000042' LIMIT 20;
```

Lo slave mantiene la posizione corrente nel Binlog tramite file e offset (replica classica) oppure tramite GTID (Global Transaction Identifier), che rende il failover molto più gestibile.

## Quando si usa

Il Binlog è attivo ogni volta che la replica è abilitata, ma viene sfruttato anche da strumenti di CDC come Debezium per catturare i cambiamenti e inviarli a pipeline di streaming. Va monitorato: un Binlog che cresce senza essere consumato dallo slave segnala un ritardo di replica. La retention si controlla con `binlog_expire_logs_seconds` (MySQL 8) o `expire_logs_days` (versioni precedenti).
