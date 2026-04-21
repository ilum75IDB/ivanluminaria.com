---
title: "Bus Matrix"
description: "Matriz bidimensional de Ralph Kimball con los procesos de negocio en las filas y las dimensiones conformadas en las columnas. Herramienta de alineamiento organizativo previa al diseño físico del DWH."
translationKey: "glossary_bus_matrix"
aka: "Kimball Bus Matrix, Data Warehouse Bus Architecture"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Bus Matrix** es una herramienta de diseño introducida por Ralph Kimball para alinear de forma explícita los procesos de negocio de una organización con las dimensiones analíticas compartidas que los describirán en el data warehouse.

## Cómo es

Una matriz bidimensional:

- En las **filas**: los procesos de negocio (ventas, devoluciones, campañas, facturación, movimientos de almacén, emisión de pólizas, cobros, etc.)
- En las **columnas**: las dimensiones candidatas a ser conformadas (cliente, producto, tiempo, geografía, canal, empleado, etc.)
- En las **celdas**: una X si ese proceso usa esa dimensión

Leer la matriz en vertical indica cuántas fact tables tocan una dimensión dada: cuantas más X, más crítica es la conformidad para esa dimensión.

## Para qué sirve

El bus matrix no genera código, no crea tablas ni optimiza consultas. Sirve para una sola cosa: obligar a los interesados (IT, negocio, finance, marketing) a mirar la misma hoja y acordar de forma explícita qué entienden por "cliente", "producto", "fecha". Es un ejercicio de alineamiento organizativo que precede al diseño físico.

## Cuándo hacerlo

Al inicio del proyecto, antes de cualquier CREATE TABLE. Kimball lo recomienda como primer paso del ciclo de vida del DWH. Hacerlo después, cuando los data marts ya han sido construidos de forma autónoma por los departamentos, cuesta órdenes de magnitud más: hacen falta talleres de gobierno, procesos de matching a posteriori, tablas de mapeo (xref) y tiempo para renegociar las definiciones existentes.

## Relación con las dimensiones conformadas

El bus matrix es la herramienta de diagnóstico, las dimensiones conformadas son la solución. Donde dos procesos comparten una dimensión en la matriz, esa dimensión *debe* ser conformada — misma clave, misma estructura, misma semántica — si no, los análisis cross-proceso devolverán números incoherentes.
