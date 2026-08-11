---
title: "Binlog"
description: "El Binary Log de MySQL registra secuencialmente cada cambio en los datos del master: es la base de la replicación master-slave y de los pipelines CDC."
translationKey: "glossary_binlog"
aka: "Binary Log"
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

El Binlog (Binary Log) es el registro secuencial que MySQL mantiene en el master para rastrear cada operación que modifica datos. El slave lo lee para saber exactamente qué replicar y en qué orden. Sin Binlog no existe replicación, y sin replicación no existe alta disponibilidad ni recuperación ante desastres en MySQL.

## Cómo funciona

Cada COMMIT escribe uno o más eventos en el Binlog, según el formato configurado:

- **ROW**: registra las filas efectivamente modificadas (imagen before/after). Más verboso, pero completamente determinista.
- **STATEMENT**: registra la consulta SQL como texto. Compacto, pero funciones no deterministas (`NOW()`, `UUID()`) pueden provocar divergencias entre master y slave.
- **MIXED**: MySQL elige automáticamente ROW o STATEMENT para cada instrucción.

```sql
-- Verificar el formato activo
SHOW VARIABLES LIKE 'binlog_format';

-- Inspeccionar eventos en un archivo binlog
SHOW BINLOG EVENTS IN 'mysql-bin.000042' LIMIT 20;
```

El slave mantiene su posición actual en el Binlog mediante nombre de archivo y offset (replicación clásica) o mediante GTID (Global Transaction Identifier), lo que simplifica considerablemente el failover.

## Cuándo es relevante

El Binlog está activo siempre que la replicación está habilitada, pero también lo consumen herramientas de CDC como Debezium para capturar cambios y alimentar pipelines de streaming. Requiere monitorización: un Binlog que crece sin ser consumido por el slave es un indicador directo de retraso en la replicación. La retención se controla con `binlog_expire_logs_seconds` (MySQL 8) o `expire_logs_days` (versiones anteriores).
