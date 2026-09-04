---
title: "Auto-Indexing"
description: "Funcionalidad Oracle (desde 19c) que analiza el workload SQL, crea índices invisibles y los promueve automáticamente si mejoran el rendimiento."
translationKey: "glossary_auto_indexing"
aka: "Automatic Indexing (Oracle)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Auto-Indexing es una funcionalidad introducida en Oracle 19c que delega al propio motor de base de datos la gestión del ciclo de vida de los índices: análisis del workload SQL, creación experimental, validación y promoción. En Oracle 21c el comportamiento se volvió configurable con mayor granularidad.

## Cómo funciona

El proceso se articula en tres fases automáticas:

1. **Análisis** — Oracle monitoriza el workload mediante el Automatic Workload Repository (AWR) e identifica las consultas candidatas a beneficiarse de nuevos índices.
2. **Creación invisible** — Los índices candidatos se crean como `INVISIBLE`, por lo que el optimizador los ignora en condiciones normales.
3. **Validación y promoción** — Oracle ejecuta pruebas internas comparando planes de ejecución. Si el índice reduce el coste, se promueve a `VISIBLE`; en caso contrario permanece invisible o se elimina.

```sql
-- Verificar la configuración de Auto-Indexing
SELECT * FROM DBA_AUTO_INDEX_CONFIG;

-- Habilitar / deshabilitar explícitamente
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'IMPLEMENT');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'OFF');
```

## Contexto operativo

Auto-Indexing está pensado para entornos OLTP con workloads variables o difíciles de perfilar manualmente. En bases de datos de producción con esquemas estables e índices ya optimizados, el riesgo es que se creen índices redundantes que incrementen el overhead de INSERT/UPDATE/DELETE y consuman espacio en tablespace.

**Recomendación práctica**: en entornos de producción críticos, ejecutar primero en modo `REPORT ONLY` antes de activar `IMPLEMENT`. Deshabilitar explícitamente con `OFF` cuando el DBA gestiona la estrategia de índices de forma manual.

```sql
-- Modo report: analiza pero no crea índices
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'REPORT ONLY');

-- Listar índices gestionados automáticamente
SELECT INDEX_NAME, STATUS, AUTO
FROM DBA_INDEXES
WHERE AUTO = 'YES';
```
