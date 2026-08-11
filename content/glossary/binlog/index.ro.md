---
title: "Binlog"
description: "Binary Log-ul MySQL înregistrează secvențial fiecare modificare de date pe master: este fundamentul replicării master-slave și al pipeline-urilor CDC."
translationKey: "glossary_binlog"
aka: "Binary Log"
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

Binlog-ul (Binary Log) este registrul secvențial pe care MySQL îl menține pe master pentru a urmări fiecare operațiune care modifică date. Slave-ul îl citește pentru a ști exact ce să replice și în ce ordine. Fără Binlog nu există replicare, iar fără replicare nu există înaltă disponibilitate sau disaster recovery pe MySQL.

## Cum funcționează

Fiecare COMMIT scrie unul sau mai multe evenimente în Binlog, în funcție de formatul configurat:

- **ROW**: înregistrează rândurile efectiv modificate (imaginea before/after). Mai verbose, dar complet determinist.
- **STATEMENT**: înregistrează interogarea SQL ca text. Compact, dar funcțiile nedeterministe (`NOW()`, `UUID()`) pot provoca divergențe între master și slave.
- **MIXED**: MySQL alege automat ROW sau STATEMENT pentru fiecare instrucțiune.

```sql
-- Verificarea formatului activ
SHOW VARIABLES LIKE 'binlog_format';

-- Inspectarea evenimentelor dintr-un fișier binlog
SHOW BINLOG EVENTS IN 'mysql-bin.000042' LIMIT 20;
```

Slave-ul își urmărește poziția curentă în Binlog prin numele fișierului și offset (replicare clasică) sau prin GTID (Global Transaction Identifier), ceea ce simplifică semnificativ failover-ul.

## Când contează

Binlog-ul este activ ori de câte ori replicarea este activată, dar este consumat și de instrumente CDC precum Debezium pentru a captura modificările și a alimenta pipeline-uri de streaming. Necesită monitorizare: un Binlog care crește fără a fi consumat de slave este un indicator direct al întârzierii replicării. Retenția se controlează prin `binlog_expire_logs_seconds` (MySQL 8) sau `expire_logs_days` (versiuni anterioare).
