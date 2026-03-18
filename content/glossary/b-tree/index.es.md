---
title: "B-Tree"
description: "Estructura de datos de árbol balanceado, tipo de índice predeterminado en la mayoría de bases de datos relacionales. Eficiente para búsquedas de igualdad y rango, pero inadecuado para LIKE con wildcard inicial."
translationKey: "glossary_b-tree"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

El **B-Tree** (Balanced Tree) es la estructura de datos más común para índices en bases de datos relacionales y es el tipo de índice predeterminado en PostgreSQL, MySQL y Oracle. Mantiene los datos ordenados en una estructura de árbol balanceado que garantiza tiempos de búsqueda logarítmicos.

## Cómo funciona

Un B-Tree organiza las claves en nodos ordenados, con cada nodo conteniendo punteros a nodos hijos. La búsqueda parte de la raíz y desciende hacia las hojas, dividiendo a la mitad el espacio de búsqueda en cada nivel. Para una tabla de 6 millones de filas, un B-Tree requiere típicamente 3-4 niveles de profundidad, es decir 3-4 lecturas de página para encontrar un valor.

## Para qué sirve

Los B-Tree son óptimos para búsquedas de igualdad (`WHERE col = 'valor'`), rangos (`WHERE col BETWEEN x AND y`), ordenamiento y búsquedas con prefijo (`LIKE 'ABC%'`). Sin embargo, no pueden usarse para búsquedas con wildcard inicial (`LIKE '%ABC%'`), porque el ordenamiento del B-Tree no ayuda a encontrar subcadenas en posiciones arbitrarias.

## Cuándo se usa

El B-Tree es la elección correcta para la mayoría de los índices. Cuando se necesita una búsqueda "contiene" en texto, hay que pasar a un índice GIN con la extensión pg_trgm. La elección entre B-Tree y GIN depende del tipo de query y del perfil de carga de la tabla.
