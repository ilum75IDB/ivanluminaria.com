---
title: "SCD"
description: "Slowly Changing Dimension — tecnica de data warehouse para rastrear los cambios en el tiempo en las tablas dimensionales."
translationKey: "glossary_scd"
aka: "Slowly Changing Dimension"
articles:
  - "/posts/data-warehouse/scd-tipo-2"
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**SCD** (Slowly Changing Dimension) indica un conjunto de tecnicas usadas en data warehouse para gestionar los cambios en los datos de las tablas dimensionales a lo largo del tiempo.

## Tipos principales

- **Tipo 1**: sobreescritura del valor anterior. No se conserva historia
- **Tipo 2**: insercion de una nueva fila con fechas de validez (fecha inicio, fecha fin). Conserva toda la historia
- **Tipo 3**: adicion de una columna para el valor anterior. Conserva solo el ultimo cambio

## Por que es importante

En una base de datos transaccional, cuando un cliente cambia de direccion se actualiza el registro. En un data warehouse esto significaria perder la historia: todas las ventas anteriores aparecerian asociadas a la nueva direccion.

La SCD Tipo 2 resuelve este problema manteniendo una fila por cada version del dato, con fechas de validez que permiten reconstruir la situacion en cualquier punto en el tiempo.

## Cuando se usa

La eleccion del tipo depende del requisito de negocio. Si solo importa el dato actual, el Tipo 1 es suficiente. Si el negocio necesita analisis historicos precisos — y en la mayoria de los data warehouses reales asi es — el Tipo 2 es la eleccion estandar.
