---
title: "Next-key lock"
description: "Mecanismo de bloqueo de InnoDB que combina record lock y gap lock para prevenir phantom reads en escaneos de índice con REPEATABLE READ."
translationKey: "glossary_next_key_lock"
aka: "Next-key locking"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

El **next-key lock** es la estrategia de bloqueo predeterminada de InnoDB durante los escaneos de índice en modo `REPEATABLE READ`. Combina un **record lock** sobre el registro actual con un **gap lock** sobre el intervalo abierto que lo precede, formando el rango semiabierto `(valor_anterior, valor_actual]`.

## Cómo funciona

Cuando una consulta adquiere un next-key lock sobre un registro con valor `42`, bloquea tanto el registro `42` como el intervalo `(x, 42]`, donde `x` es el valor inmediatamente anterior en el índice. Ninguna otra transacción puede insertar un valor en ese intervalo hasta que el lock sea liberado.

```sql
-- Este SELECT en REPEATABLE READ adquiere next-key locks
-- sobre cada registro devuelto y sobre los intervalos entre ellos
SELECT * FROM pedidos WHERE estado = 'abierto' FOR SHARE;
```

Para el registro con el valor más alto del índice, InnoDB extiende el next-key lock hasta el centinela interno `supremum`, cubriendo todos los valores futuros que podrían insertarse más allá del máximo actual.

## Cuándo se aplica

Los next-key locks están activos por defecto en `REPEATABLE READ` y garantizan que releer la misma consulta dentro de la misma transacción devuelva siempre los mismos resultados, previniendo los **phantom reads**. En `READ COMMITTED`, los gap locks se liberan tras la evaluación del predicado, reduciendo la contención a costa de exponer la transacción a phantom reads.

Los next-key locks son la causa más frecuente de deadlocks en aplicaciones que ejecutan operaciones concurrentes de INSERT y SELECT sobre el mismo índice: dos transacciones pueden mantener gap locks solapados y bloquearse mutuamente cuando ambas intentan un INSERT en el mismo intervalo.
