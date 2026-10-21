---
title: "Phantom Read"
description: "Anomalía de concurrencia en la que una transacción lee un rango dos veces y obtiene resultados distintos porque otra transacción insertó o eliminó filas entre medias."
translationKey: "glossary_phantom_read"
aka: "Lectura fantasma"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un **Phantom Read** ocurre cuando una transacción ejecuta la misma consulta sobre un rango de filas en dos momentos distintos y obtiene conjuntos de resultados diferentes, porque otra transacción ha insertado o eliminado filas en ese rango mientras tanto. El término "fantasma" describe bien el fenómeno: filas que aparecen o desaparecen sin que la transacción actual las haya modificado.

## Cómo funciona

La secuencia clásica implica dos transacciones concurrentes:

```sql
-- Transacción A
BEGIN;
SELECT * FROM pedidos WHERE importe > 1000;
-- devuelve 5 filas

-- Transacción B (mientras tanto)
INSERT INTO pedidos (importe) VALUES (1500);
COMMIT;

-- Transacción A, misma consulta
SELECT * FROM pedidos WHERE importe > 1000;
-- ahora devuelve 6 filas → phantom read
COMMIT;
```

La transacción A no modificó nada, pero el resultado cambia. Esto se diferencia del **Non-Repeatable Read**, que afecta a filas ya leídas que son modificadas, no a la aparición o desaparición de filas dentro del rango analizado.

## Niveles de aislamiento y prevención

`READ COMMITTED` permite los phantom reads: cada SELECT ve un snapshot actualizado en el momento de su propia ejecución. `REPEATABLE READ` — nivel por defecto en InnoDB — los previene mediante **gap locks** y **next-key locks**, que bloquean intervalos de índice e impiden INSERT concurrentes dentro del rango leído. `SERIALIZABLE` ofrece la garantía más fuerte, convirtiendo las SELECT implícitas en lecturas bloqueantes.

Optar por `READ COMMITTED` en entornos de alta concurrencia reduce el riesgo de deadlocks por gap lock, pero expone la aplicación a phantom reads: un trade-off que debe evaluarse según la lógica de negocio.
