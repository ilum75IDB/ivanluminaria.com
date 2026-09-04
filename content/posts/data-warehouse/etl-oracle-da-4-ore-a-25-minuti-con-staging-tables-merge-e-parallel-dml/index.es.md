---
categories:
- data-warehouse
date: 2099-12-31
description: 'Cómo diagnosticamos y reescribimos un ETL PL/SQL legacy en Oracle 19c:
  row-by-row, lookups sin índice, COMMIT frecuente. Números reales antes y después.'
draft: true
image: etl-oracle-da-4-ore-a-25-minuti-con-staging-tables-merge-e-parallel-dml.cover.jpg
seoTitle: 'ETL Oracle 19c: de 4 horas a 24 minutos con MERGE y Parallel DML'
tags:
- oracle
- etl
- performance-tuning
- parallel-dml
- data-warehouse
title: 'La ventana que se cerraba: ETL Oracle de 4 horas a 24 minutos con staging,
  MERGE y parallel DML'
translationKey: etl_oracle_da_4_ore_a_25_minuti_con_staging_tables_merge_e_parallel_dml
webo_generated_at: 2026-09-04
webo_status: da_tradurre
---

## La ventana que se cerraba

El DBA del cliente nos mandó un mensaje lacónico: "El batch de anoche terminó a las 7:12. Los informes de las 7:00 estaban vacíos."

No era la primera vez. Desde hacía algunas semanas la carga nocturna iba retrasándose — primero tres horas y media, luego casi cuatro, luego más. La ventana batch estaba fijada entre las 23:00 y las 6:30, y el sistema empezaba a sobrepasarla con regularidad. Al día siguiente nos sentamos frente a los logs con el DBA del cliente y empezamos a ver qué estaba pasando de verdad.

El contexto: un Data Warehouse Oracle 19c, un proceso ETL legacy escrito en PL/SQL, 15 millones de filas que cargar cada noche desde fuentes operacionales. El volumen no había cambiado de forma significativa respecto al año anterior — había crecido un 12%, nada dramático. La lentitud no era un problema de escala: era un problema de cómo estaba escrito el código.

## Lo que contaban los logs

La primera herramienta que usamos fue AWR [1]. Un informe AWR sobre la ventana nocturna mostraba enseguida dónde iba el tiempo: el top SQL por elapsed time era un bloque PL/SQL con un cursor que iteraba fila a fila sobre 15 millones de registros.

```sql
-- patrón original (simplificado) — el problema era exactamente este
FOR rec IN (SELECT * FROM stg_source_data WHERE process_flag = 'N') LOOP
    -- lookup sobre tabla de referencia sin índice
    SELECT dim_id INTO v_dim_id
    FROM dim_customer
    WHERE ext_code = rec.customer_code;

    INSERT INTO fact_sales (
        dim_customer_id, sale_date, amount, product_id
    ) VALUES (
        v_dim_id, rec.sale_date, rec.amount, rec.product_id
    );

    v_count := v_count + 1;
    IF MOD(v_count, 100) = 0 THEN
        COMMIT;
    END IF;
END LOOP;
```

Tres líneas de código, tres causas de lentitud. Vamos por partes.

## Las cuatro causas de un ETL que no llega

**1. INSERT fila a fila (row-by-row = slow-by-slow)**

Es una de las frases más citadas en los cursos Oracle, pero sigue apareciendo en producción. Cada `INSERT` individual genera un round-trip hacia el buffer cache, actualiza los segmentos de undo, escribe en el redo log. Multiplicado por 15 millones de filas, el coste de contexto por cada operación individual acaba dominando sobre el coste del dato en sí.

La comparación que hicimos internamente: un `INSERT ... SELECT` bulk sobre 15 millones de filas tarda una fracción del tiempo respecto a 15 millones de `INSERT` individuales, con los mismos datos. No es una cuestión de IO — es una cuestión de overhead por operación.

**2. Lookup sin índice sobre `dim_customer`**

La tabla `dim_customer` tenía unos 2,8 millones de filas. La columna `ext_code` — la usada para el join con la fuente — no tenía ningún índice. Cada lookup era un full table scan de 2,8 millones de filas, repetido 15 millones de veces.

AWR mostraba `dim_customer` como la tabla con mayor número de logical reads en toda la ventana nocturna. No era casualidad.

**3. COMMIT cada 100 filas**

El COMMIT frecuente se introduce a menudo con buenas intenciones: "si algo falla, no lo perdemos todo". En realidad, en Oracle, cada COMMIT tiene un coste nada despreciable: flush del redo log buffer, actualización de los SCN, sincronización con los procesos de background. Hacerlo 150.000 veces por noche (15M / 100) añade un overhead medible y, sobre todo, impide que la base de datos optimice las operaciones en batch.

**4. Sin paralelismo**

El proceso era completamente serial: un único proceso PL/SQL, un cursor, un loop. Oracle 19c en ese servidor tenía 16 cores disponibles, pero la carga usaba solo uno durante toda la noche.

## La reescritura: staging, MERGE, bulk y parallel

La estrategia que adoptamos con el equipo se articulaba en cuatro movimientos, en el orden en que los implementamos.

### Staging table con bulk load

El primer paso fue separar la carga de la transformación. Los datos de la fuente se cargan primero en una staging table con un `INSERT /*+ APPEND */ ... SELECT` — una única operación bulk que bypasa el buffer cache y escribe directamente en los datafiles (direct path insert) [2].

```sql
-- carga staging: direct path insert, nologging
INSERT /*+ APPEND PARALLEL(stg_sales_load, 8) */ INTO stg_sales_load
    NOLOGGING
SELECT
    s.customer_code,
    s.sale_date,
    s.amount,
    s.product_id
FROM source_sales_ext s  -- external table o db link
WHERE s.load_date = TRUNC(SYSDATE);

COMMIT;  -- un solo commit tras el bulk
```

El hint `APPEND` activa el direct path insert. `NOLOGGING` reduce la escritura en el redo log (aceptable para una staging table que se recrea cada noche). `PARALLEL` distribuye el trabajo en 8 procesos paralelos.

### Índice sobre `dim_customer.ext_code`

Simple, pero necesario. Antes de proceder con cualquier transformación:

```sql
CREATE INDEX idx_dim_customer_ext_code
    ON dim_customer (ext_code)
    PARALLEL 4
    NOLOGGING;
```

Tras la creación, los lookups sobre 2,8 millones de filas pasaron a ser index range scans sobre una columna de alta selectividad. El coste por lookup se desplomó.

### MERGE en lugar de INSERT + UPDATE separados

El proceso original tenía también una lógica de "upsert" implícita: si la fila ya existía en `fact_sales` (por reprocesados parciales), había que actualizarla; si no, insertarla. El código original gestionaba esto con un `SELECT COUNT(*)` antes de cada `INSERT`, añadiendo un round-trip adicional por fila.

La reescritura usa `MERGE` [3]:

```sql
MERGE /*+ PARALLEL(f, 8) */ INTO fact_sales f
USING (
    SELECT
        dc.dim_id AS dim_customer_id,
        stg.sale_date,
        stg.amount,
        stg.product_id
    FROM stg_sales_load stg
    JOIN dim_customer dc ON dc.ext_code = stg.customer_code
) src
ON (
    f.dim_customer_id = src.dim_customer_id
    AND f.sale_date    = src.sale_date
    AND f.product_id   = src.product_id
)
WHEN MATCHED THEN
    UPDATE SET f.amount = src.amount
WHEN NOT MATCHED THEN
    INSERT (dim_customer_id, sale_date, amount, product_id)
    VALUES (src.dim_customer_id, src.sale_date, src.amount, src.product_id);

COMMIT;  -- un solo commit para todo el MERGE
```

Una sola operación, un solo commit, el join con `dim_customer` ejecutado una única vez sobre el dataset completo en lugar de 15 millones de veces.

### Parallel DML habilitado a nivel de sesión

Para que el paralelismo funcione en el `MERGE`, hay que habilitarlo explícitamente [4]:

```sql
ALTER SESSION ENABLE PARALLEL DML;
```

Sin esta instrucción, los hints `PARALLEL` en operaciones DML se ignoran en silencio — un detalle que también nos costó tiempo la primera vez que probamos la reescritura y no veíamos mejoras significativas.

## Los números, antes y después

Ejecutamos tres runs de prueba en un entorno de staging con un dataset real anonimizado (misma cardinalidad, misma distribución de valores).

| Métrica | Antes | Después |
|---|---|---|
| Tiempo total ETL | 4h 03m | 24m 38s |
| Logical reads (AWR) | ~2.100 millones | ~48 millones |
| COMMITs totales | ~150.000 | 2 (staging + MERGE) |
| Procesos paralelos activos | 1 | 8 |
| Redo generado | ~18 GB | ~3,2 GB |

El redo generado bajó también gracias al `NOLOGGING` en la staging table — que sin embargo hay que usar con criterio: una staging table `NOLOGGING` no es recuperable desde un backup incremental tomado durante la carga. En nuestro caso era aceptable porque la staging se recrea desde cero cada noche a partir de la fuente.

La carga ahora termina a las 00:24. La ventana batch vuelve a tener margen de sobra.

## Lo que vale la pena llevarse a casa

Algunas semanas después de la puesta en producción, el DBA del cliente nos mandó otro mensaje — esta vez menos lacónico: "Funciona. Gracias."

Lo que aprendimos (o más bien confirmamos) en este proyecto no es nuevo, pero merece escribirse de forma explícita porque sigue apareciendo:

**El row-by-row es el asesino silencioso de los ETL legacy.** No es obvio hasta que no se mira AWR o un trace 10046. El código parece razonable — un loop, un insert, un commit. La situación es que "razonable" no significa "eficiente" cuando se escala a millones de filas.

**El COMMIT frecuente no protege: ralentiza.** Si el proceso tiene que ser reanudable en caso de error, la estrategia correcta es la staging table con un flag de estado — no el commit cada N filas sobre la tabla de destino.

**El paralelismo Oracle requiere configuración explícita.** `ALTER SESSION ENABLE PARALLEL DML` no es opcional si se quieren operaciones DML paralelas. Y los grados de paralelismo hay que calibrarlos en el servidor real, no elegirlos al azar.

**El MERGE está infrautilizado.** Muchos ETL legacy gestionan el upsert con SELECT + INSERT/UPDATE separados. El MERGE hace lo mismo en una sola operación, con un único acceso a la tabla de destino.

El patrón — staging table → transformación con joins indexados → MERGE bulk con parallel DML → commit único — es reutilizable en cualquier ETL Oracle con características similares. No es una solución mágica: requiere entender el perfil del dato (cardinalidad, distribución, frecuencia de actualización) y probar los grados de paralelismo en el hardware real. Pero como punto de partida para una reescritura, funciona.

## Fuentes oficiales

1. Oracle Database — [Automatic Workload Repository (AWR)](https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/gathering-database-statistics.html)
2. Oracle Database — [Direct Path INSERT](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/INSERT.html#GUID-903F8043-0254-4EE9-ACC1-CB8AC0AF3423)
3. Oracle Database SQL Language Reference 19c — [MERGE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/MERGE.html)
4. Oracle Database — [Parallel DML](https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/using-parallel-dml.html)

## Glosario
- **[AWR](/es/glossary/awr/)** (Oracle Automatic Workload Repository) — Repositorio de snapshots periódicos de métricas de workload Oracle. Base para los informes AWR y para ADDM. Fundamental para diagnosticar cuellos de botella en ventanas temporales específicas como una noche de batch.

- **[Direct Path Insert](/es/glossary/direct-path-insert/)** — Modalidad de INSERT Oracle (activada por el hint `APPEND`) que bypasa el buffer cache y escribe directamente en los datafiles. Reduce drásticamente el coste de carga bulk pero requiere atención a la estrategia de backup y recovery.

- **[MERGE](/es/glossary/merge/)** (SQL) — Instrucción SQL que combina INSERT y UPDATE en una única operación atómica (upsert). Realiza un único acceso a la tabla de destino, eliminando el patrón SELECT + INSERT/UPDATE separados típico de los ETL legacy.

- **Parallel DML** (Oracle) — Ejecución paralela de operaciones DML (INSERT, UPDATE, DELETE, MERGE) en múltiples procesos Oracle. Requiere `ALTER SESSION ENABLE PARALLEL DML` y hints explícitos. Sin la habilitación a nivel de sesión, los hints se ignoran en silencio.

- **Staging table** — Tabla temporal usada como área de aterrizaje de los datos en bruto antes de la transformación y la carga en el destino final. Permite separar las fases del ETL, gestionar la reanudabilidad y aplicar transformaciones en bulk en lugar de fila a fila.
