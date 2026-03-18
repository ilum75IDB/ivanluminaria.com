---
title: "Churn"
description: "Medida de cuánto cambia una tabla de base de datos después de la inserción inicial de datos, en términos de UPDATE y DELETE. Determina el coste de mantenimiento de los índices."
translationKey: "glossary_churn"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

El **churn** de una tabla es la medida de cuánto cambian sus datos después de la inserción. Una tabla con alto churn sufre frecuentes UPDATE y DELETE; una tabla con bajo churn es predominantemente append-only (solo INSERT).

## Cómo funciona

En PostgreSQL, cada UPDATE crea una nueva versión de la fila (debido al modelo MVCC) y la versión antigua se convierte en una dead tuple. Los DELETE también crean dead tuples. Cuanto mayor es el churn, más trabajo deben hacer VACUUM y los índices para mantener el rendimiento. Un índice GIN en una tabla de alto churn puede degradar significativamente el rendimiento de escritura.

## Para qué sirve

Evaluar el churn antes de crear un índice es esencial para evitar resolver un problema de lectura creando uno de escritura. En una tabla append-only (cero UPDATE, cero DELETE, cero dead tuples), un índice GIN tiene impacto mínimo en las escrituras. En una tabla de alto churn, el mismo índice podría convertirse en un cuello de botella.

## Cuándo se usa

El churn se analiza verificando las estadísticas de la tabla: número de UPDATE y DELETE diarios, dead tuples, frecuencia de VACUUM. En PostgreSQL, `pg_stat_user_tables` proporciona estas métricas. La decisión de añadir un índice GIN o trigram debería siempre partir de este análisis.
