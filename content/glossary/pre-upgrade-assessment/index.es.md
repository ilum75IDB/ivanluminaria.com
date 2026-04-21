---
title: "Pre-upgrade Assessment"
description: "Medición estructurada del tamaño, crecimiento, tiempos de backup y tiempos de restore de una base de datos antes de un upgrade. Sirve para dimensionar la ventana de mantenimiento y definir un rollback realista."
translationKey: "glossary_pre_upgrade_assessment"
aka: "Upgrade Readiness Check, Database Sizing & Timing Assessment"
articles:
  - "/posts/mysql/mysql-pre-upgrade-assessment"
---

**Pre-upgrade Assessment** es un documento técnico, pero sobre todo una herramienta de gobernanza del riesgo. Traduce la pregunta operativa "¿llegamos a completar el upgrade dentro de la ventana de mantenimiento?" a números medidos, no estimados a ojo.

## Las cuatro cifras fundamentales

Un assessment completo responde a cuatro preguntas concretas:

1. **Tamaños actuales**: cuánto pesa hoy cada base de datos, por esquema, por tabla, en disco real vs. estimación de `information_schema`
2. **Tasa de crecimiento**: cuánto crecen los datos en el tiempo, medido mediante snapshots historizados y/o volumen del binary log
3. **Tiempos de backup**: cuánto dura un backup completo, medido sobre cada herramienta que podría usarse (`mysqldump`, `mydumper`, `xtrabackup`, `pg_dump`, `expdp`…)
4. **Tiempos de restore**: cuánto se tarda en reconstruir la base de datos desde cero — la cifra más importante y la más a menudo olvidada

## Por qué los tiempos de restore importan más que los de backup

Los backups se lanzan en segundo plano, a menudo fuera de la ventana de mantenimiento. Los restores en cambio están dentro de la ventana, dentro del plan de rollback, dentro del SLA de restauración del servicio. Un dataset que se guarda en 30 minutos puede requerir 4 horas de restore lógico: si el plan de rollback no lo tiene en cuenta, la ventana no basta.

## Cuándo hacerlo

- Antes de un **upgrade major** (MySQL 5.7→8.0, Oracle 12c→19c, PostgreSQL 14→16)
- Antes de una **migración de infraestructura** (nuevo storage, nuevo hypervisor, cloud migration)
- Antes de un **re-platforming** de on-premises a cloud
- Como **auditoría periódica** anual sobre bases de datos en producción, para verificar que los tiempos medidos siguen siendo válidos tras el crecimiento de los datos

## Qué entregar al PM

Una sola tabla, no treinta diapositivas. Columnas: servidor, tamaño actual, crecimiento estimado, tiempo de backup, tiempo de restore (herramienta principal), tiempo de restore peor caso (mysqldump o equivalente). El PM debe poder adjuntarla al plan de cutover sin adaptarla.
