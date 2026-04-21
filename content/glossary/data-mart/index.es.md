---
title: "Data Mart"
description: "Subconjunto del data warehouse enfocado en un único proceso de negocio o área funcional. A menudo construido de forma autónoma por un departamento."
translationKey: "glossary_data_mart"
aka: "Departmental Data Mart, Subject-Area Data Mart"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Data Mart** es un subconjunto de un data warehouse enfocado en un único proceso de negocio, un área funcional (ventas, marketing, finance) o un departamento. Contiene típicamente una o pocas fact tables y las dimensiones asociadas a ellas.

## Por qué existen los data marts

En la realidad empresarial, un DWH enterprise completo requiere años de proyecto. Los data marts nacen como compromiso pragmático: se construye primero la pieza que un departamento necesita ya (p. ej. un data mart de ventas para marketing) y se integra con las demás más adelante. Es el enfoque bottom-up de Kimball.

## Riesgo de divergencia

Cuando varios data marts se construyen de forma autónoma por cada departamento — a menudo con herramientas BI distintas, sobre sistemas fuente distintos, con tiempos distintos — el riesgo es que "cliente" acabe significando tres cosas diferentes en los tres data marts. Los totales no cuadran, los análisis cross-departamento se vuelven imposibles o lentos, y el CFO se encuentra con tres versiones de la verdad.

## Data mart conformado vs independiente

La diferencia crítica es si el data mart comparte dimensiones conformadas o no:

- **Data marts conformados** (Kimball): comparten dimensiones conformadas (cliente, producto, tiempo, geografía) y por lo tanto pueden consultarse en conjunto de forma coherente
- **Data marts independientes**: construidos sin gobierno común, divergen con el tiempo y generan los clásicos problemas de "tres versiones de la verdad"

El bus matrix es la herramienta de diseño que previene el segundo escenario.

## Cuándo tiene sentido

Un data mart tiene sentido cuando:

- El perímetro funcional está bien definido (un proceso, un departamento)
- Las dimensiones conformadas ya están disponibles o se van a construir en paralelo
- El coste de un DWH enterprise completo no está justificado
- Se necesita un time-to-value rápido para un caso de uso específico

No tiene sentido en cambio como "solución permanente aislada": o es la primera pieza de una estrategia integrada, o se convierte en deuda técnica en pocos años.
