---
categories:
- oracle
date: '2026-12-01'
description: 'Cómo Oracle SPM transformó un informe financiero de 45 a 3 minutos:
  diagnóstico de un plan subóptimo, captura de baseline y prevención de regresiones.'
draft: false
image: oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire.cover.jpg
seoTitle: 'Oracle SQL Plan Management: estabilizar planes de ejecución'
tags:
- oracle
- sql-plan-management
- performance-tuning
- optimizer
- oracle-19c
title: La mañana de Pietro y el informe que 'siempre ha sido así'
translationKey: oracle_sql_plan_management_stabilizzare_i_piani_di_esecuzione_per_prevenire
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La mañana de Pietro y el informe que "siempre ha sido así"

Era una de esas mañanas raras en que el teléfono no suena. Sin alertas, sin escalaciones, sin el DBA del cliente en pánico. Pietro, un junior que trabaja conmigo desde hace unos meses en un proyecto para un gran grupo asegurador italiano, se había acercado a mi escritorio con esa curiosidad algo cautelosa que tienen los juniors cuando intuyen que el experto tiene tiempo.

"¿Puedo preguntarte algo sobre una query que me ha llamado la atención?"

La query en cuestión era el informe de facturación anual — uno de esos informes que el management board usa cada semana para monitorizar los ingresos. Llevaba años ejecutándose. Cuarenta y cinco minutos cada vez. El equipo de desarrollo lo sabía. El PM lo sabía. El management lo sabía. Se había convertido en parte del paisaje, como el ruido del aire acondicionado en la sala de servidores: presente, aceptado, ignorado.

Pietro había encontrado la query en el repositorio y había notado que no parecía especialmente compleja. Cuatro tablas, algunos joins, un agregado. ¿Por qué tardaba 45 minutos?

Respondí como respondo siempre en estos casos: "Abrimos el plan de ejecución y vemos qué está haciendo el optimizer."

No imaginaba que esa sesión didáctica se convertiría en un diagnóstico operativo.

## Lo que el optimizer estaba haciendo bajo el capó

La query era esta, simplificada para facilitar la lectura:

```sql
SELECT
    c.customer_name,
    SUM(il.amount) AS total_revenue
FROM
    FINANCE.CUSTOMERS c
JOIN
    SALES.INVOICES i ON c.customer_id = i.customer_id
JOIN
    SALES.INVOICE_LINES il ON i.invoice_id = il.invoice_id
WHERE
    i.invoice_date BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2025-12-31', 'YYYY-MM-DD')
GROUP BY
    c.customer_name
ORDER BY
    total_revenue DESC;
```

Las tablas involucradas no eran pequeñas: `SALES.INVOICES` tenía unos 150 millones de filas, `SALES.INVOICE_LINES` unos 750 millones, `FINANCE.CUSTOMERS` 5 millones. El filtro sobre `invoice_date` debería haber reducido drásticamente el dataset antes de los joins — pero solo si el optimizer hubiera elegido el camino correcto.

Extraje el plan actual desde la cursor cache:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => '<sql_id>', format => 'ALLSTATS LAST'));
```

El plan mostraba un Hash Join sobre `SALES.INVOICES` y `SALES.INVOICE_LINES` con Full Table Scan en ambas tablas — antes incluso de aplicar el filtro por fecha. El optimizer estaba leyendo 750 millones de filas para luego descartar la mayoría.

"¿Por qué hace eso?" preguntó Pietro.

Es una pregunta legítima. El optimizer no es tonto: eligió ese plan porque las estadísticas que tenía disponibles lo llevaban a creer que era el camino más eficiente. El problema es que las estadísticas habían cambiado — o más bien, habían sido actualizadas de forma no representativa tras una recolección masiva realizada durante una ventana de mantenimiento, probablemente con datos parciales. El resultado: el optimizer sobreestimaba la selectividad del filtro sobre `invoice_date` y subestimaba el coste del Full Table Scan en las tablas grandes.

Comparé con los snapshots AWR [1] de las semanas anteriores:

```sql
SELECT
    snap_id,
    plan_hash_value,
    elapsed_time_total / executions_total AS avg_elapsed_us
FROM
    DBA_HIST_SQLSTAT
WHERE
    sql_id = '<sql_id>'
ORDER BY
    snap_id DESC;
```

El plan había cambiado unas tres semanas antes. Antes de ese momento, la misma query se ejecutaba en menos de 4 minutos con un plan diferente — Nested Loops con Index Range Scan sobre `SALES.INVOICES` (índice sobre `invoice_date`) y posterior Index Scan sobre `SALES.INVOICE_LINES`. Un plan mucho más eficiente para este patrón de acceso.

Pietro miró los números en silencio durante unos segundos. "Entonces la query no es lenta. Es el plan el que está mal."

Exacto.

## SQL Plan Management: el concepto de baseline como ancla de estabilidad

En ese punto introduje SQL Plan Management [1], que es exactamente la herramienta pensada para situaciones como esta.

La idea de fondo es sencilla: Oracle mantiene un repositorio de planes de ejecución aprobados para cada SQL statement, denominado **SQL Plan Baseline**. Cuando el optimizer genera un nuevo plan para una query, lo compara con la baseline. Si el nuevo plan no está en la baseline, se marca como "no verificado" (*unaccepted*) y no se usa automáticamente — aunque el optimizer lo considere mejor. Solo los planes explícitamente aceptados en la baseline se utilizan en producción.

Este mecanismo crea una separación nítida entre "el optimizer encuentra un plan nuevo" y "el plan nuevo va a producción". Esa separación es valiosa: te da tiempo para evaluar, probar y decidir de forma consciente.

SPM opera sobre tres conceptos fundamentales:

- **SQL Plan Baseline**: el conjunto de planes aceptados para un SQL statement específico, identificado por su `sql_id` o por el texto normalizado.
- **Plan aceptado** (*accepted*): un plan en la baseline que el optimizer puede usar.
- **Plan candidato** (*unaccepted*): un plan que el optimizer ha encontrado pero que todavía no ha sido verificado ni aceptado.

El parámetro de sistema `OPTIMIZER_USE_SQL_PLAN_BASELINES` (por defecto `TRUE`) controla si el optimizer consulta las baselines. El parámetro `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES` [3] (por defecto `FALSE`) controla si Oracle captura automáticamente los planes de las queries repetidas.

## Capturar el plan bueno desde la cursor cache

El plan óptimo — el de Nested Loops con Index Scan — seguía en la cursor cache, asociado a un `plan_hash_value` distinto del actual. El objetivo era cargarlo en la baseline como plan aceptado.

El método más directo es `DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE` [2]:

```sql
DECLARE
    v_plans_loaded PLS_INTEGER;
BEGIN
    v_plans_loaded := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
        sql_id          => '<sql_id>',
        plan_hash_value => <plan_hash_value_buono>
    );
    DBMS_OUTPUT.PUT_LINE('Planes cargados: ' || v_plans_loaded);
END;
/
```

La función devuelve el número de planes cargados. El plan se inserta en la baseline con estado `ACCEPTED = YES` — listo para ser usado por el optimizer.

Para verificar qué hay en la baseline:

```sql
SELECT
    sql_handle,
    plan_name,
    accepted,
    enabled,
    fixed,
    created,
    last_modified
FROM
    DBA_SQL_PLAN_BASELINES
WHERE
    sql_text LIKE '%FINANCE.CUSTOMERS%'
ORDER BY
    created DESC;
```

En ese momento teníamos dos planes en la baseline: el bueno (recién cargado, `ACCEPTED = YES`) y el subóptimo que el optimizer estaba usando. El plan subóptimo no estaba todavía en la baseline — era simplemente el plan que el optimizer elegía libremente en ausencia de restricciones.

El siguiente paso era asegurarnos de que el optimizer usara el plan bueno y no volviera al malo en el futuro.

## El proceso de evolución: cómo SPM evalúa los nuevos planes

Antes de deshabilitar el plan subóptimo, vale la pena entender cómo funciona el mecanismo de evolución [1] — porque es aquí donde SPM muestra su verdadera utilidad a largo plazo.

Cuando el optimizer encuentra un plan que no está en la baseline, lo añade como plan candidato (*unaccepted*). Ese plan no se usa, pero se conserva para una evaluación posterior. El procedimiento `DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE` [2] realiza esa evaluación: ejecuta el plan candidato de forma controlada y lo compara con el plan aceptado actual. Si el candidato es significativamente más eficiente (por defecto, al menos un 1,5% más rápido), se promueve a *accepted*.

```sql
SET SERVEROUTPUT ON
DECLARE
    v_report CLOB;
BEGIN
    v_report := DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        time_limit  => 60,   -- segundos máximos para el test
        verify      => 'YES',
        commit      => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE(v_report);
END;
/
```

El parámetro `verify => 'YES'` hace que Oracle ejecute efectivamente el plan candidato para medir su rendimiento. Con `commit => 'YES'`, si el plan supera el umbral, se acepta automáticamente.

En este caso concreto no necesitábamos evolución automática — el plan bueno ya había sido cargado como aceptado. Pero es importante conocer el mecanismo para los casos en que se trabaja con captura automática (`OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE`), donde los planes candidatos se acumulan y deben evaluarse periódicamente.

## Estabilizar el plan óptimo y bloquear las regresiones futuras

Con el plan bueno en la baseline, dimos un paso más: marcarlo como `FIXED`. Un plan fixed tiene precedencia absoluta — el optimizer lo usa siempre, independientemente de cualquier otro plan en la baseline o de eventuales nuevos planes encontrados.

```sql
DECLARE
    v_plans_modified PLS_INTEGER;
BEGIN
    v_plans_modified := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        plan_name   => '<plan_name_buono>',
        attribute_name  => 'fixed',
        attribute_value => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE('Planes modificados: ' || v_plans_modified);
END;
/
```

Tras esta operación, ejecutamos la query en entorno de prueba. El plan elegido por el optimizer era el de Nested Loops con Index Range Scan sobre `invoice_date`. Tiempo de ejecución: poco menos de 3 minutos, frente a los 45 minutos anteriores.

El cambio en el plan era evidente: en lugar de leer la tabla completa `SALES.INVOICE_LINES` (750 millones de filas) con un Full Table Scan, el optimizer accedía primero a `SALES.INVOICES` a través del índice sobre `invoice_date` — reduciendo el dataset a unos pocos cientos de miles de filas para el año seleccionado — y luego ejecutaba el join con `SALES.INVOICE_LINES` mediante Index Scan sobre `invoice_id`. El filtro se aplicaba antes del join, no después.

Dejamos el plan subóptimo en la baseline con estado `ENABLED = NO` en lugar de eliminarlo, para conservar el historial y poder rehabilitarlo si fuera necesario. Una decisión conservadora, pero sensata en producción.

## Cuándo usar SPM: escenarios y trade-offs

Pietro hizo la pregunta correcta en ese momento: "Pero si funciona tan bien, ¿por qué no lo usamos en todas las queries?"

La respuesta honesta es que SPM tiene un coste de gestión que no es despreciable.

**Escenarios en los que SPM resulta especialmente útil**:

- **Antes y después de un upgrade de Oracle Database**: un upgrade puede cambiar el comportamiento del optimizer de forma significativa. Cargar las baselines antes del upgrade y verificarlas después es una práctica consolidada.
- **Tras la aplicación de parches**: los parches del optimizer (incluidos en las PSU/RU) pueden alterar los planes. SPM permite congelar los planes críticos antes del parcheo.
- **Después de una recolección masiva de estadísticas**: como en nuestro caso. Una recolección de estadísticas no representativa puede degradar decenas de queries simultáneamente.
- **Queries críticas con SLA estrictos**: informes financieros, batches nocturnos, queries de cierre mensual — cualquier query cuya regresión tenga impacto directo en el negocio.

**Trade-offs a considerar**:

- Las baselines requieren mantenimiento. Si la estructura de las tablas cambia (nuevos índices, particiones, columnas), los planes en la baseline podrían volverse subóptimos respecto a la nueva estructura. Es necesario un proceso de revisión periódica.
- Con `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE` a nivel de sistema, los planes candidatos se acumulan rápidamente. Sin un proceso de evolución regular, la baseline se convierte en un archivo inmanejable.
- SPM no es un sustituto de las estadísticas correctas. Es una herramienta de estabilización, no de optimización. El plan bueno debe existir y debe ser identificado: SPM lo conserva, no lo crea.

La estrategia que adoptamos es selectiva: baselines solo sobre las queries críticas identificadas, con revisión trimestral. Sin captura automática a nivel de sistema.

## El informe del lunes por la mañana

En los días siguientes, el informe de facturación empezó a ejecutarse en unos 3 minutos. Sin anuncios, sin comunicación previa al equipo de desarrollo.

El primero en notarlo fue uno de los analistas financieros, que escribió en el chat: "¿El informe de facturación ya está listo? Normalmente lo lanzo y me voy a por un café."

El equipo de desarrollo preguntó qué había cambiado. Explicamos el análisis, el plan subóptimo, el mecanismo de SPM. Fue una conversación útil — no porque el fix fuera complicado, sino porque abrió una discusión sobre cómo gestionar las queries críticas de forma proactiva, no solo reactiva.

El management board notó la mejora en el informe semanal siguiente. Sin intervenciones heroicas, sin emergencias resueltas en el último momento. Solo un análisis realizado en una mañana tranquila, gracias a la pregunta de un junior curioso.

Pietro, por su parte, entendió algo que los libros no enseñan fácilmente: que explicar un concepto a alguien te obliga a mirarlo con ojos distintos. Mientras le mostraba el plan de ejecución, vi la lentitud con la misma frescura con que la veía él. Sin esa pregunta, probablemente habría abierto otra pestaña y pasado a otra cosa.

## Lo que queda en el runbook del equipo

Tras esa mañana, añadimos tres prácticas al runbook del equipo:

1. **Revisión trimestral de las baselines SPM** sobre las queries críticas — verificación de que los planes aceptados siguen siendo óptimos respecto a la estructura actual de las tablas.
2. **Control de los planes AWR** antes y después de cada recolección masiva de estadísticas — comparación de los `plan_hash_value` para las queries monitorizadas.
3. **Procedimiento de carga de baseline pre-upgrade** — antes de cualquier upgrade o parche de Oracle, se identifican las queries críticas y sus planes actuales se cargan en la baseline como plan de fallback.

SPM no elimina el trabajo de tuning. Elimina la sorpresa: esa mañana en que llegas a la oficina y descubres que una query crítica ha dejado de funcionar como ayer, sin que nadie haya tocado nada.

## Fuentes oficiales

1. Oracle Database SQL Tuning Guide 19c — [Managing SQL Plan Baselines](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlad/managing-sql-plan-baselines.html)
2. Oracle Database PL/SQL Packages and Types Reference 19c — [DBMS_SPM](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPM.html)
3. Oracle Database Reference 19c — [OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES.html)
4. Oracle-Base (Tim Hall) — [SQL Plan Management (SPM) in Oracle Database](https://oracle-base.com/articles/11g/sql-plan-management-11gr1)

## Glosario
- **[SQL Plan Management (SPM)](/es/glossary/sql-plan-management/)** — Funcionalidad de Oracle Database que permite controlar y estabilizar los planes de ejecución de las queries mediante un repositorio de planes aprobados (baseline), previniendo regresiones de rendimiento debidas a variaciones del optimizer.

- **[SQL Plan Baseline](/es/glossary/awr/)** — Conjunto de uno o más planes de ejecución aceptados para un SQL statement específico, almacenado en el repositorio SPM. El optimizer utiliza únicamente los planes presentes en la baseline, ignorando planes alternativos aún no verificados.

- **[Plan fixed](/es/glossary/hash-join/)** (SPM) — Plan de ejecución marcado con el atributo `FIXED = YES` en la SQL Plan Baseline. Tiene precedencia absoluta sobre todos los demás planes de la baseline: el optimizer lo selecciona siempre, independientemente de eventuales planes alternativos encontrados.

- **[AWR](/es/glossary/sql-plan-management/)** (Oracle) — Automatic Workload Repository: snapshots periódicos de métricas de workload, base de los AWR reports y de ADDM. Conserva el historial de planes de ejecución a través de `DBA_HIST_SQLSTAT`, útil para identificar variaciones de plan a lo largo del tiempo.

- **[Hash Join](/es/glossary/sql-plan-baseline/)** — Algoritmo de join utilizado por el optimizer de Oracle para unir dos tablas construyendo una hash table en memoria sobre la tabla menor y escaneando la tabla mayor. Eficiente para grandes datasets sin índices selectivos; costoso cuando se aplica antes de los filtros selectivos.
