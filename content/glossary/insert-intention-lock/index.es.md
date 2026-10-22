---
title: "Insert Intention Lock"
description: "Lock de intención adquirido por INSERT antes de escribir en un gap. Compatible con otros insert intention locks, bloqueado por gap locks existentes."
translationKey: "glossary_insert_intention_lock"
aka: "Insert Intention Gap Lock"
articles:
  - "/posts/mysql/mysql-gap-lock-e-next-key-lock-diagnosi-dei-deadlock-con-show-engine-innodb"
---

Un **Insert Intention Lock** es un tipo especial de gap lock que InnoDB adquiere cada vez que una transacción ejecuta una `INSERT` dentro de un gap entre dos valores de índice. Varios insert intention locks sobre el mismo gap son mutuamente compatibles — inserciones concurrentes en el mismo intervalo pueden avanzar en paralelo — pero cualquier gap lock o next-key lock existente sobre ese gap los bloqueará.

## Cómo funciona

Antes de escribir el nuevo registro, InnoDB coloca un insert intention lock sobre el gap de destino. Si otra transacción ya mantiene un gap lock sobre el mismo rango (por ejemplo, a partir de un `SELECT ... FOR UPDATE` con predicado de rango), la `INSERT` queda en espera hasta que ese lock se libere.

```sql
-- Transacción A: adquiere un gap lock sobre el intervalo (10, 20)
SELECT * FROM pedidos WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- Transacción B: intenta insertar en el mismo intervalo, espera el gap lock de A
INSERT INTO pedidos (id, estado) VALUES (15, 'nuevo');
```

La compatibilidad entre insert intention locks es deliberada: permite inserciones de alta concurrencia en el mismo gap sin serialización innecesaria, siempre que las filas insertadas no colisionen en la misma clave.

## Deadlocks por INSERTs concurrentes

El patrón de deadlock más frecuente con insert intention locks ocurre cuando dos transacciones adquieren cada una un gap lock — habitualmente mediante un `SELECT ... FOR UPDATE` que no devuelve filas — y luego ambas intentan insertar en el mismo gap. Cada una espera que la otra libere su gap lock, formando un ciclo que InnoDB detecta y resuelve haciendo ROLLBACK de una de las dos transacciones.

```sql
-- Secuencia típica de deadlock
-- T1: SELECT ... FOR UPDATE sobre gap → gap lock adquirido
-- T2: SELECT ... FOR UPDATE sobre mismo gap → gap lock adquirido
-- T1: INSERT en el gap → espera el gap lock de T2
-- T2: INSERT en el gap → espera el gap lock de T1 → DEADLOCK
```

Para diagnosticar este escenario, analiza la salida de `SHOW ENGINE INNODB STATUS`: los modos de lock relevantes aparecen como `LOCK_MODE: X,GAP` y `LOCK_MODE: X,INSERT_INTENTION`.
