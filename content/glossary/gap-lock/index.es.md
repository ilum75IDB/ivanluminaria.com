---
title: "Gap Lock"
description: "El Gap Lock de InnoDB bloquea un intervalo entre valores de índice para impedir INSERT en ese rango. Activo en REPEATABLE READ, ausente en READ COMMITTED."
translationKey: "glossary_gap_lock"
aka: "Gap Lock (InnoDB)"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un Gap Lock es un mecanismo de bloqueo de InnoDB que protege un **intervalo** entre dos valores de un índice, sin bloquear los registros que delimitan ese intervalo. Su objetivo principal es impedir que otras transacciones inserten filas en el rango protegido, garantizando la consistencia de lectura.

## Cómo funciona

Cuando una transacción lee un rango con `SELECT ... FOR UPDATE` o `SELECT ... LOCK IN SHARE MODE`, InnoDB puede adquirir un Gap Lock sobre el intervalo entre los valores del índice involucrados. Ningún registro físico queda bloqueado: el lock existe únicamente en el "espacio" entre los valores.

```sql
-- Transacción A: lee filas con id entre 10 y 20
SELECT * FROM pedidos WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transacción B: intenta insertar id = 15 → bloqueada por el Gap Lock
INSERT INTO pedidos (id, estado) VALUES (15, 'nuevo');
```

Dos Gap Locks sobre el mismo intervalo son **compatibles entre sí**: el conflicto ocurre únicamente con los intentos de INSERT dentro del rango protegido.

## Contexto operativo

El Gap Lock está activo exclusivamente con el nivel de aislamiento `REPEATABLE READ` (valor por defecto de InnoDB). Al cambiar a `READ COMMITTED`, InnoDB libera los Gap Locks tras cada sentencia, reduciendo la contención pero exponiendo la transacción a lecturas no repetibles y phantom reads.

En sistemas de alta concurrencia con muchos INSERT, los Gap Locks son una causa frecuente de deadlocks: dos transacciones pueden adquirir Gap Locks solapados y bloquearse mutuamente al intentar insertar. Diagnosticar estos escenarios requiere analizar la salida de `SHOW ENGINE INNODB STATUS`.
