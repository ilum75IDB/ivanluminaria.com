---
title: "REPEATABLE READ"
description: "Nivel de aislamiento predeterminado de MySQL/InnoDB: garantiza un snapshot coherente durante toda la transacción mediante MVCC y next-key locks."
translationKey: "glossary_repeatable_read"
aka: "Nivel de aislamiento Repeatable Read"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

REPEATABLE READ es el nivel de aislamiento predeterminado de MySQL/InnoDB. Una transacción que opera a este nivel siempre ve el mismo snapshot de los datos desde el momento de su primer SELECT, sin importar cuántos cambios hayan hecho COMMIT otros clientes mientras tanto.

## Cómo funciona

InnoDB implementa REPEATABLE READ sobre dos mecanismos distintos:

- **Lecturas no bloqueantes (consistent read):** gestionadas por MVCC. Cada fila mantiene una cadena de versiones; la transacción lee la versión válida en el momento del snapshot, ignorando las escrituras posteriores.
- **Lecturas bloqueantes y escrituras:** utilizan locks físicos. InnoDB aplica **next-key locks** (record lock + gap lock) para evitar que filas fantasma aparezcan entre un `SELECT ... FOR UPDATE` y el siguiente dentro de la misma transacción.

```sql
-- La transacción siempre ve el mismo snapshot
START TRANSACTION;
SELECT * FROM pedidos WHERE estado = 'abierto';  -- snapshot fijado aquí
-- ... otras operaciones ...
SELECT * FROM pedidos WHERE estado = 'abierto';  -- mismo resultado
COMMIT;
```

## Cuándo usarlo y limitaciones

REPEATABLE READ es adecuado para la mayoría de las cargas OLTP: cierres de balance, informes dentro de una transacción, operaciones multi-paso que requieren datos estables. El coste principal son los next-key locks, que amplían la superficie de bloqueo respecto a READ COMMITTED y aumentan el riesgo de deadlocks en INSERTs concurrentes. Si la aplicación no necesita protección contra phantom reads, bajar a READ COMMITTED reduce la contención.
