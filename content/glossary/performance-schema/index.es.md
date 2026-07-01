---
title: "performance_schema"
description: "Esquema de sistema de MySQL que recopila métricas de ejecución en tiempo real: digest de consultas, wait events y memoria por hilo. Base para el diagnóstico de rendimiento."
translationKey: "glossary_performance_schema"
aka: "P_S (abreviatura común)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`performance_schema` es una base de datos de sistema disponible en MySQL desde la versión 5.5, diseñada para exponer métricas internas de ejecución del servidor sin necesidad de herramientas externas. Los datos se recopilan en memoria mediante estructuras de instrumentación de bajo overhead y se actualizan en tiempo real.

## Cómo funciona

El motor de instrumentación intercepta eventos internos (consultas, locks, I/O, asignaciones de memoria) y los agrega en tablas consultables mediante SQL estándar. Las principales áreas cubiertas son:

- **Statement digests**: estadísticas agregadas por consulta normalizada (`events_statements_summary_by_digest`)
- **Wait events**: esperas en mutexes, I/O, locks (`events_waits_summary_global_by_event_name`)
- **Memoria**: asignaciones por hilo y por componente (`memory_summary_by_thread_by_event_name`)

```sql
-- Top 10 consultas por latencia media
SELECT
    digest_text,
    count_star,
    ROUND(avg_timer_wait / 1e9, 2) AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

La habilitación granular de los instrumentos se controla mediante las tablas `setup_instruments` y `setup_consumers`: es posible activar únicamente las categorías necesarias para minimizar el impacto en el workload.

## Cuándo se usa

`performance_schema` es el punto de partida para cualquier análisis de rendimiento en MySQL cuando no se dispone de herramientas APM externas. Escenarios típicos:

- Identificar consultas lentas cuando el slow query log no está habilitado
- Diagnosticar contención en el InnoDB buffer pool o locks a nivel de fila
- Monitorizar el uso de memoria por hilo en entornos con muchas conexiones concurrentes (relevante en configuraciones de InnoDB Cluster)

**Limitaciones a considerar**: los datos son volátiles (se reinician al reiniciar el servidor), las tablas no se persisten en disco, y el overhead — aunque bajo — es medible en workloads con altísima frecuencia de statements cortos.
