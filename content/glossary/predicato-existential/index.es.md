---
title: "Predicado Existencial"
description: "Expresión lógica SQL que comprueba si existe al menos una fila que cumple una condición, base de los patrones EXISTS y NOT EXISTS."
translationKey: "glossary_predicato_existential"
aka: "Existential predicate, predicado de existencia"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un **predicado existencial** es una expresión lógica que devuelve `TRUE` si existe al menos una fila que satisface una condición dada. En SQL es el mecanismo que sustenta los operadores `EXISTS` y `NOT EXISTS`, utilizados habitualmente en subconsultas correlacionadas para verificar la presencia o ausencia de datos relacionados sin recuperarlos explícitamente.

## Cómo funciona

El motor evalúa la subconsulta correlacionada fila a fila respecto a la consulta externa. En cuanto encuentra la primera fila que cumple la condición, devuelve `TRUE` y detiene el recorrido (evaluación en cortocircuito). Esto lo hace frecuentemente más eficiente que un `JOIN` o un `IN` sobre conjuntos de datos grandes.

```sql
-- Verificar que existe al menos un pedido activo por cada cliente
SELECT c.id, c.nombre
FROM clientes c
WHERE EXISTS (
    SELECT 1
    FROM pedidos p
    WHERE p.cliente_id = c.id
      AND p.estado = 'ACTIVO'
);
```

El `SELECT 1` en la subconsulta es convencional: el valor proyectado es irrelevante, solo importa la existencia de la fila.

## Cuándo se usa

El predicado existencial es el patrón natural para implementar **Assertions de tipo "al menos uno"**: restricciones o comprobaciones que exigen la presencia garantizada de al menos un registro relacionado. En Oracle 23ai, donde las Assertions declarativas aún no están disponibles como objetos DDL nativos, `EXISTS` dentro de triggers o check constraints es el sustituto operativo estándar.

`NOT EXISTS` cubre el caso complementario — ninguna fila debe satisfacer la condición — útil para restricciones de exclusión o para detectar huecos en series temporales.

Un aspecto a tener en cuenta: en subconsultas no correlacionadas o sobre columnas sin índice, el coste puede degradarse a un recorrido completo. Revisar el plan de ejecución (`EXPLAIN PLAN`) antes de llevar a producción consultas con `EXISTS` sobre tablas de gran tamaño es siempre recomendable.
