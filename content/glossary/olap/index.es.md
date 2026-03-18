---
title: "OLAP"
description: "Online Analytical Processing — procesamiento orientado al análisis multidimensional de datos, típico de los data warehouses."
translationKey: "glossary_olap"
aka: "Online Analytical Processing"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**OLAP** (Online Analytical Processing) indica un enfoque de procesamiento de datos orientado al análisis multidimensional: agregaciones, drill-down, comparaciones temporales, slice-and-dice sobre grandes volúmenes de datos históricos.

## OLAP vs OLTP

| Característica | OLAP | OLTP |
|----------------|------|------|
| Propósito | Análisis y reporting | Transacciones operativas |
| Modelo de datos | Star schema, desnormalizado | 3NF, normalizado |
| Consulta típica | Agregaciones sobre millones de filas | Lectura/escritura de pocas filas |
| Usuarios | Analistas, management | Aplicaciones, operadores |
| Actualización | Batch (ETL periódico) | Tiempo real |

## Operaciones OLAP

Las operaciones fundamentales del análisis OLAP son:

- **Drill-down**: del nivel agregado al detalle
- **Drill-up** (roll-up): del detalle al agregado
- **Slice**: seleccionar una "rebanada" de datos fijando una dimensión (ej. solo año 2025)
- **Dice**: seleccionar un sub-cubo especificando múltiples dimensiones
- **Pivot**: rotar las dimensiones de análisis (filas ↔ columnas)

## Implementaciones

- **ROLAP** (Relational OLAP): los datos permanecen en tablas relacionales, las agregaciones se calculan con consultas SQL. Es el enfoque usado en los data warehouses con star schemas
- **MOLAP** (Multidimensional OLAP): los datos se pre-agregan en estructuras multidimensionales (cubos). Más rápido en consultas pero requiere más espacio y tiempo de construcción
- **HOLAP** (Hybrid): combinación de ambos enfoques
