---
title: "Conformed Dimension"
description: "Dimensión compartida entre varios data marts con la misma estructura, semántica y clave. Permite análisis cross-proceso coherentes y sumables."
translationKey: "glossary_conformed_dimension"
aka: "Dimensión Conformada, Shared Dimension"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Conformed Dimension** (dimensión conformada) es una dimensión usada en más de una fact table o data mart con la misma estructura, la misma semántica y la misma clave. Es el pilar de la bus architecture de Kimball.

## Qué significa "conformar"

Conformar una dimensión significa acordar tres elementos:

- **Clave natural única**: qué identificador representa la entidad (código fiscal, código de cliente, código de producto, NIF)
- **Atributos compartidos**: qué columnas son comunes a todos los data marts que usan la dimensión (país, región, categoría, etc.)
- **Grano**: el nivel de detalle de la dimensión (una fila por cliente, no por segmento)

Los atributos específicos de un solo departamento pueden quedarse en tablas dimensionales locales, pero no deben entrar en la parte conformada de la dimensión.

## Para qué sirve

Sin dimensiones conformadas, las medidas procedentes de fact tables distintas no se pueden comparar de forma fiable. Con dimensiones conformadas, una consulta que cruza ventas y campañas de marketing sobre el mismo cliente devuelve un resultado coherente porque "cliente" significa lo mismo en los dos procesos.

## Implementación física

Una dimensión conformada no tiene por qué ser una única tabla física compartida. Puede ser:

- **Replicada** en varios esquemas (opción pragmática cuando los data marts viven en bases de datos distintas)
- **Centralizada** en un esquema dedicado (p. ej. `dim_conformed`) con vistas o sinónimos en los data marts
- **Virtualizada** mediante herramientas de data virtualization

Lo que importa es que las tres propiedades — estructura, semántica, clave — sean idénticas en cada copia.

## Cuándo hace falta gobierno

Mantener la conformidad en el tiempo requiere un comité de gobierno con representantes de los departamentos que usan la dimensión. Cada cambio (un atributo nuevo, una regla de deduplicación nueva, un canal de adquisición nuevo) se acuerda y se propaga de forma coordinada — si no, las dimensiones conformadas divergen y toda la construcción se derrumba.
