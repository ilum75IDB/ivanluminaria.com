---
title: "Predicado universal"
description: "Expresión lógica SQL que verifica que una condición se cumple para todas las filas de un conjunto, usando NOT EXISTS (... WHERE NOT condición)."
translationKey: "glossary_predicato_universal"
aka: "Cuantificador universal SQL"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un predicado universal afirma que una condición se cumple para **cada** fila de un conjunto. En lógica formal corresponde al cuantificador ∀ (para todo). SQL no expone este cuantificador de forma directa, por lo que se construye mediante doble negación.

## Cómo funciona

La equivalencia fundamental es:

> "∀ x: P(x)" ≡ "¬∃ x: ¬P(x)"

En SQL:

```sql
-- "todos los pedidos de este cliente tienen importe > 0"
SELECT c.id
FROM clientes c
WHERE NOT EXISTS (
    SELECT 1
    FROM pedidos p
    WHERE p.cliente_id = c.id
      AND NOT (p.importe > 0)
);
```

El motor recorre el subconjunto correlacionado y devuelve la fila padre solo cuando no encuentra ninguna que viole la condición. Si el conjunto interno está vacío, el predicado se satisface por verdad vacua (vacuous truth).

## Cuándo se usa

El predicado universal aparece en escenarios de **restricción relacional**:

- verificar que todas las líneas de un encabezado cumplen una regla de negocio (por ejemplo, todas las líneas de factura tienen código de impuesto informado);
- implementar **assertions** lógicas en bases de datos que no soportan `CREATE ASSERTION` de forma nativa (Oracle 23ai incluido);
- expresar división relacional ("clientes que han comprado *todos* los productos de una categoría").

Hay que tener cuidado con la verdad vacua: si la subconsulta no devuelve filas, `NOT EXISTS` evalúa a `TRUE` por definición, lo que puede generar falsos positivos cuando el conjunto de referencia está vacío.
