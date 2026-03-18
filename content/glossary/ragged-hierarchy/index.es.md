---
title: "Ragged hierarchy"
description: "Jerarquía en la que no todas las ramas alcanzan la misma profundidad: algunos niveles intermedios están ausentes."
translationKey: "glossary_ragged_hierarchy"
aka: "Jerarquía desequilibrada, Unbalanced hierarchy"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

Una **ragged hierarchy** (jerarquía desequilibrada) es una estructura jerárquica en la que no todas las ramas alcanzan la misma profundidad. Algunos niveles intermedios están ausentes para determinadas entidades.

## Ejemplo concreto

En una jerarquía de tres niveles Top Group → Group → Client:

- Algunos clientes tienen los tres niveles (jerarquía completa)
- Algunos clientes tienen un Group pero ningún Top Group
- Algunos clientes no tienen ni Group ni Top Group (clientes directos)

El resultado es una estructura con "huecos" que causa problemas en los reportes de agregación: filas con NULL, totales divididos, drill-downs incompletos.

## Por qué es un problema en el DWH

Las herramientas de BI y las consultas SQL esperan jerarquías completas para funcionar correctamente. Un GROUP BY sobre una columna con NULLs produce resultados inesperados: las filas con NULL se agrupan por separado, los totales no cuadran, y el mismo grupo puede aparecer en múltiples filas.

## Cómo se resuelve

La técnica estándar es el **self-parenting**: quien no tiene padre se convierte en padre de sí mismo. Esto balancea la jerarquía aguas arriba, en el ETL, eliminando los NULLs de la tabla dimensional. Flags adicionales (`is_direct_client`, `is_standalone_group`) permiten distinguir las entidades balanceadas artificialmente de las que tienen una jerarquía natural.
