---
title: "GxP"
description: "Término colectivo para las directrices regulatorias Good Practice en la industria farmacéutica: exige change control, pruebas documentadas y aprobación formal de Calidad en sistemas informatizados."
translationKey: "glossary_gxp"
aka: "Good Practice (GMP, GLP, GCP, GDP)"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

GxP es un acrónimo colectivo que agrupa las directrices regulatorias "Good Practice" aplicables a las industrias farmacéutica, biotecnológica y de dispositivos médicos. La "x" es un comodín para la disciplina específica: GMP (Manufacturing), GLP (Laboratory), GCP (Clinical), GDP (Distribution). Cualquier sistema informatizado que entre en el ámbito GxP está sujeto a requisitos estrictos de validación, integridad de datos y control de cambios.

## Alcance normativo

Las dos referencias principales para sistemas informatizados son **EU GMP Annex 11** (Europa) y **21 CFR Part 11** (FDA, EE. UU.). Ambas exigen que cada sistema informatizado GxP esté validado, que la integridad de los datos esté garantizada y que los cambios queden registrados mediante un audit trail. A nivel de base de datos, esto implica control de versiones de esquemas, logs inmutables y procedimientos de backup verificados con frecuencia documentada.

## Impacto operativo en el change control

Cualquier modificación a un sistema GxP — actualización del DBMS, migración de esquema, cambio de parámetros de configuración — debe seguir un proceso formal de change control:

1. **Impact Assessment**: evaluación del riesgo sobre el estado validado existente.
2. **Pruebas documentadas**: IQ (Installation Qualification), OQ (Operational Qualification), PQ (Performance Qualification).
3. **Aprobación de Calidad**: firma formal antes del despliegue en producción.

Un lift-and-shift de una base de datos Oracle hacia la nube, por ejemplo, nunca es transparente en un entorno GxP: cambia la infraestructura subyacente, y eso reabre el ciclo de validación. Los plazos del change control — habitualmente entre 4 y 12 semanas — son el coste oculto que los planes de migración tienden a subestimar sistemáticamente.

## Cuando el DBA forma parte del proceso regulatorio

En entornos GxP el DBA no gestiona únicamente rendimiento y disponibilidad: es un actor dentro del sistema de calidad. Las sentencias DDL ejecutadas en producción deben estar pre-aprobadas, los backups deben probarse con frecuencia documentada y cualquier anomalía debe generar un deviation report. La latencia WAN o un failover no planificado no son solo incidentes técnicos — pueden ser eventos regulatorios que requieren una investigación formal.
