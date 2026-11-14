---
title: "Call Detail Record (CDR)"
description: "Registro que documenta una única llamada telefónica: cliente, fecha, duración, tipo y coste. Dato operativo primario en sistemas de telecomunicaciones."
translationKey: "glossary_call_detail_record"
aka: "CDR, Call Data Record"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Un Call Detail Record (CDR) es la traza persistente que un sistema de telefonía genera al finalizar cada llamada. Contiene la información mínima necesaria para facturar el servicio y analizar el tráfico: quién llamó, cuándo, durante cuánto tiempo, con qué tipo de conexión y a qué coste. En los sistemas telco es el dato operativo de referencia, equivalente a una fila de transacción en un sistema bancario.

## Estructura típica

Un CDR incluye al menos los siguientes campos:

| Campo | Descripción |
|---|---|
| `caller_id` | Identificador del cliente que realiza la llamada |
| `callee_id` | Número o identificador del destinatario |
| `start_time` | Timestamp de inicio de la llamada |
| `duration_sec` | Duración en segundos |
| `call_type` | Voz, SMS, datos, roaming |
| `cost` | Coste calculado al finalizar la llamada |

La estructura varía entre operadores y estándares (3GPP, IPDR), pero estos campos son prácticamente universales.

## Contexto operativo

Los CDR se acumulan a gran velocidad: un operador de tamaño medio genera cientos de GB al mes. Esto los convierte en un caso de uso clásico para los Data Warehouses telco, donde se cargan en batch o mediante streaming y se agregan para facturación, análisis de tráfico y detección de fraude. Las consultas analíticas habituales — suma de duración por cliente, distribución por franja horaria, comparativa mes a mes — se benefician de técnicas como las Materialized Views para evitar recálculos costosos sobre tablas con miles de millones de filas.

## Consideraciones de volumen

Un CDR individual ocupa pocos bytes, pero la cardinalidad es muy elevada. Diseñar el esquema de almacenamiento — particionado por fecha, compresión columnar, índices parciales — es crítico desde la fase de modelado, antes incluso de definir los patrones de consulta.
