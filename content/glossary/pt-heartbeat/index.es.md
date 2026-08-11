---
title: "pt-heartbeat"
description: "Herramienta de Percona Toolkit que mide el lag de replicación MySQL escribiendo timestamps en el master y comparándolos en el slave. Más fiable que Seconds_Behind_Master."
translationKey: "glossary_pt_heartbeat"
aka: "Percona Toolkit Heartbeat"
articles:
  - "/posts/mysql/mysql-slave-lag-parallel-replication"
---

`pt-heartbeat` es una utilidad de Percona Toolkit diseñada para medir el lag de replicación MySQL de forma directa y fiable. A diferencia de la métrica nativa `Seconds_Behind_Master` — que puede devolver valores engañosos ante errores de replicación o pérdida de conexión — `pt-heartbeat` mide el retraso real rastreando datos escritos en el master y leídos en el slave.

## Cómo funciona

La herramienta opera en dos modos distintos, habitualmente como procesos independientes de larga duración:

```bash
# En el master: escribe un timestamp en una tabla dedicada cada N segundos
pt-heartbeat --host=master-host --user=repl --password=secret \
  --database=percona --update --interval=1

# En el slave: lee la tabla y calcula el delta respecto a la hora actual
pt-heartbeat --host=slave-host --user=repl --password=secret \
  --database=percona --monitor --master-server-id=1
```

La tabla `heartbeat` (creada automáticamente en el primer arranque) almacena un timestamp mantenido al día por el proceso `--update`. El proceso `--monitor` en el slave lee ese valor y calcula la diferencia respecto a la hora local: el resultado es el lag real en segundos, con precisión de centésimas.

## Cuándo se usa

`pt-heartbeat` es la referencia para alerting en producción cuando `Seconds_Behind_Master` no es suficiente. Los escenarios habituales son:

- **Replicación interrumpida**: `Seconds_Behind_Master` devuelve `NULL`, mientras que `pt-heartbeat` sigue reportando el lag creciente.
- **Replicación multi-source o con filtros**: el cálculo nativo puede ser impreciso; el timestamp escrito en el master es una fuente de verdad.
- **Integración con sistemas de monitorización**: la salida de `--monitor` es parseable por Nagios, Prometheus (vía exporter) o cualquier script bash.

La limitación principal es la dependencia de un proceso activo en el master: si el proceso `--update` se detiene, el lag medido crece indefinidamente aunque la replicación en sí esté sana.
