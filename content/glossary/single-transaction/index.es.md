---
title: "--single-transaction"
description: "Flag de mysqldump que abre una transacción REPEATABLE READ para exportar datos InnoDB de forma consistente, sin adquirir bloqueos a nivel de tabla."
translationKey: "glossary_single_transaction"
aka: null
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

`--single-transaction` es una opción de `mysqldump` que abre una transacción `REPEATABLE READ` antes de iniciar la exportación. El aislamiento proporcionado por InnoDB garantiza una lectura consistente de los datos sin bloquear las escrituras concurrentes.

## Cómo funciona

Al arrancar el dump, MySQL emite implícitamente `START TRANSACTION WITH CONSISTENT SNAPSHOT`. Todas las lecturas posteriores ocurren dentro de esa misma transacción, viendo los datos tal como estaban en el momento de abrir el snapshot. Las operaciones DML concurrentes (INSERT, UPDATE, DELETE) continúan sin interrupción gracias al aislamiento MVCC de InnoDB.

```bash
mysqldump --single-transaction --routines --events \
  -u root -p my_database > backup.sql
```

El archivo resultante contiene un dump lógicamente consistente, equivalente a un snapshot puntual en el tiempo.

## Cuándo usarlo y limitaciones

`--single-transaction` es la opción estándar para bases de datos InnoDB en producción: evita los bloqueos a nivel de tabla que paralizarían las aplicaciones. No es aplicable a tablas **MyISAM** o **MEMORY**, que no soportan transacciones. Para esos motores se recurre a `--lock-tables`, que adquiere un bloqueo compartido durante toda la duración del dump.

Cuando el esquema mezcla motores de almacenamiento, ambos flags son mutuamente excluyentes: `--single-transaction` deshabilita automáticamente `--lock-tables`. Las tablas no transaccionales incluidas en el dump pueden quedar inconsistentes respecto a las tablas InnoDB.

## Notas operativas

En dumps de gran tamaño, la transacción abierta puede acumular entradas significativas en el undo log de InnoDB. Monitorizar `innodb_history_list_length` durante operaciones de backup prolongadas es una práctica recomendable para evitar presión sobre el tablespace de undo.
