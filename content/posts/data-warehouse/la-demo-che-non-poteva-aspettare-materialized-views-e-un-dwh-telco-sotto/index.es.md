---
categories:
- data-warehouse
date: '2026-12-09'
description: Cómo las Materialized Views transformaron un prototipo DWH lento en un
  sistema de reportes creíble para un gran operador telco. Criterios de elección,
  estrategias de refresh y resultados medibles.
draft: false
image: la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto.cover.jpg
seoTitle: 'Materialized Views en DWH: rendimiento analítico en entorno Telco'
tags:
- materialized-views
- data-warehouse
- performance-tuning
- oracle
- postgresql
title: 'La demo que no podía esperar: Materialized Views en un DWH Telco'
translationKey: la_demo_che_non_poteva_aspettare_materialized_views_e_un_dwh_telco_sotto
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La demo que no podía esperar

Era un proyecto que no deberíamos haber hecho. No en el sentido de que fuera un error hacerlo — era exactamente el tipo de trabajo que nos gustaba — sino en el sentido de que nadie nos lo había encargado. El equipo de consultoría había decidido construir un prototipo de Data Warehouse para un gran operador telco móvil con el que llevábamos meses trabajando, convencidos de que la reportística detallada sobre clientes y tráfico telefónico podría abrir conversaciones comerciales nuevas. Una apuesta interna, financiada con horas no facturadas y bastante entusiasmo.

La idea era sencilla: llevar al equipo de marketing del cliente un dashboard que mostrara patrones de tráfico, distribución geográfica de las llamadas, segmentación por tipo de contrato. Datos que ellos ya tenían, pero que no conseguían leer de forma agregada. Nosotros teníamos acceso a los sistemas fuente, teníamos la experiencia, teníamos ganas de demostrar algo.

Lo que no habíamos calculado bien era la escala.

Los registros de detalle de llamadas — los CDR, *Call Detail Records* — se acumulaban a un ritmo de unos 500 GB al mes. Años de datos históricos, decenas de millones de filas por cada período mensual. Cuando empezamos a construir los reportes sobre estas tablas, la realidad se hizo sentir de forma bastante directa: los compañeros que probaban las consultas volvían con caras largas y números poco alentadores. Una hora y cuarenta y cinco minutos para una agregación mensual. Tres minutos para cargar el dashboard principal. El PM, que había creído en el proyecto desde el principio, había dejado de hacer preguntas entusiastas y había empezado a hacer preguntas preocupadas.

La demo estaba fijada. No se podía mover.

## Cuando el motor se atasca con los volúmenes

El problema no era un bug. Era estructural, y vale la pena entender por qué, porque es el mismo problema que se encuentra en cualquier entorno analítico que crece sin una estrategia de pre-agregación.

Las consultas de reportística sobre un DWH tienen una característica precisa: agregan grandes volúmenes de datos históricos para producir resultados sintéticos. Una consulta que calcula el tráfico mensual por cliente, por ejemplo, tiene que leer potencialmente millones de filas, aplicar funciones de agregación, hacer joins con la tabla maestra de clientes. El motor de base de datos ejecuta ese trabajo cada vez que alguien abre el reporte.

Una consulta típica sobre nuestro esquema tenía esta forma:

```sql
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    SUM(cdr.CALL_DURATION_SEC) / 60.0  AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                  AS TOTAL_CALLS,
    AVG(cdr.COST)                      AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
WHERE
    cdr.CALL_DATE >= TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
    AND cdr.CALL_DATE <  TRUNC(SYSDATE, 'MM')
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME
ORDER BY
    cm.REGION,
    TOTAL_DURATION_MIN DESC;
```

El plan de ejecución mostraba lo que esperábamos: un full scan sobre `call_detail_records` para el mes seleccionado, un hash join con `customer_master`, y luego la agregación. Con 500 GB mensuales de CDR e índices que ayudaban poco en consultas de rango temporal tan amplias, el tiempo de respuesta era el que era.

Añadir índices habría ayudado marginalmente. Particionar por fecha habría reducido el volumen escaneado, pero no teníamos tiempo de rediseñar el esquema antes de la demo. Hacía falta algo que desplazara el trabajo fuera de la consulta en sí.

## La experiencia que encuentra su momento

No fue una intuición repentina. Propuse las Materialized Views porque ya las había usado en otros contextos — en Oracle, en entornos de reportística financiera — y sabía que el patrón encajaba bien con lo que estábamos intentando hacer.

Una Materialized View es, en esencia, una consulta cuyos resultados se calculan una vez y se almacenan físicamente en disco como si fueran una tabla. Cuando una aplicación consulta la MV, no recalcula nada: lee datos ya agregados. La diferencia con una view estándar es exactamente esa: la view normal es una definición de consulta que se ejecuta cada vez, la MV es un resultado pre-calculado que se actualiza periódicamente.

Oracle soporta las Materialized Views desde hace mucho tiempo, con opciones sofisticadas de refresh y query rewriting automático [1][2]. PostgreSQL las introdujo en la versión 9.3 con una sintaxis más escueta pero igualmente eficaz [3]. En ambos casos, el principio es el mismo: desplaza el coste computacional del momento de la lectura al momento del refresh.

En nuestro contexto, ese era exactamente el trade-off adecuado. Los datos históricos no cambiaban. Los reportes del mes anterior eran estáticos. Podíamos pre-calcular todo una sola vez, o como mucho una vez al día, y servir los resultados en milisegundos.

## Candidatos ideales y escenarios donde no tiene sentido

No todas las consultas son buenas candidatas para una Materialized View. Antes de implementar, hicimos un mapeo rápido de los patrones de acceso.

Los candidatos ideales comparten algunas características:

**Agregaciones frecuentes sobre datos históricos estables.** Si la misma agregación se ejecuta decenas de veces al día sobre datos que cambian poco o nada, el coste del refresh periódico queda ampliamente justificado por el ahorro en lecturas. Los reportes mensuales sobre CDR eran el caso perfecto: los datos del mes anterior nunca cambian, los del mes en curso solo cambian con los nuevos registros que llegan.

**Joins complejos entre tablas grandes.** El join entre `call_detail_records` y `customer_master` era costoso porque implicaba millones de filas. Pre-calcularlo en la MV significaba que el dashboard nunca tenía que ejecutar ese join.

**Reportes con latencia tolerable en los datos.** Si marketing acepta reportes actualizados cada hora, o incluso cada noche, una MV con refresh programado es la solución natural. Si en cambio se necesita consistencia en tiempo real — un saldo bancario, una disponibilidad de almacén en vivo — las MV introducen complejidad sin resolver el problema.

Los casos en que **no** tiene sentido:

- Datos que cambian continuamente y requieren consistencia inmediata
- Consultas que se ejecutan raramente (el coste del refresh supera el beneficio)
- Tablas fuente pequeñas donde la consulta original ya es rápida
- Escenarios OLTP donde la latencia de escritura del refresh es inaceptable

En nuestro DWH, la distinción era clara: los datos históricos eran perfectos para las MV, los datos del día en curso podían seguir con consultas directas.

## Refresh, coherencia y el coste oculto

La parte que requiere más atención no es la creación de la MV, sino la gestión del refresh. Aquí es donde se toman las decisiones arquitectónicas que importan.

Oracle ofrece dos modalidades principales [2]:

- **`REFRESH COMPLETE`**: recalcula la MV entera desde cero. Simple, fiable, costoso en grandes volúmenes. Adecuado cuando los datos fuente cambian de forma no rastreable.
- **`REFRESH FAST`**: actualización incremental basada en los *materialized view logs*, estructuras que rastrean los cambios en las tablas fuente. Mucho más eficiente, pero requiere que las tablas base tengan los logs habilitados y que la consulta de la MV respete ciertos requisitos.

PostgreSQL [3] soporta únicamente el refresh completo (`REFRESH MATERIALIZED VIEW`), con la opción `CONCURRENTLY` que permite actualizar la MV sin bloquear las lecturas — siempre que exista un índice único sobre la propia MV.

En nuestro caso optamos por un enfoque pragmático: refresh completo nocturno para las MV sobre datos históricos, ejecutado mediante un scheduler interno en las horas de baja actividad. La carga sobre el sistema fuente durante el refresh quedaba concentrada en una ventana temporal aceptable, y los reportes de la mañana encontraban los datos ya listos.

La configuración Oracle para el refresh automático tenía esta estructura:

```sql
-- Creación del job de refresh (Oracle DBMS_SCHEDULER)
BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'REFRESH_MV_MONTHLY_TRAFFIC',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN DBMS_MVIEW.REFRESH(''MV_MONTHLY_TRAFFIC_SUMMARY'', ''C''); END;',
        start_date      => TRUNC(SYSDATE + 1) + INTERVAL '2' HOUR,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Refresh nocturno MV tráfico mensual para reportística de marketing'
    );
END;
/
```

Un detalle que vale la pena subrayar: el refresh completo sobre una MV grande bloquea temporalmente las consultas sobre esa MV (en Oracle, salvo que se use `ATOMIC_REFRESH => FALSE`). Planificar el refresh en las horas adecuadas no es un detalle operativo secundario — es parte del diseño.

## Los reportes vuelven a la vida

La MV que resolvió el problema principal agregaba el tráfico mensual por cliente y región:

```sql
CREATE MATERIALIZED VIEW mv_monthly_traffic_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM')          AS CALL_MONTH,
    SUM(cdr.CALL_DURATION_SEC) / 60.0   AS TOTAL_DURATION_MIN,
    COUNT(cdr.ID_CDR)                   AS TOTAL_CALLS,
    AVG(cdr.COST)                       AS AVG_COST_PER_CALL
FROM
    call_detail_records cdr
    JOIN customer_master cm ON cdr.ID_CUSTOMER = cm.ID_CUSTOMER
GROUP BY
    cm.REGION,
    cm.ID_CUSTOMER,
    cm.NAME,
    cm.SURNAME,
    TRUNC(cdr.CALL_DATE, 'MM');

-- Índice para las consultas más frecuentes del dashboard
CREATE INDEX idx_mv_monthly_region_month
    ON mv_monthly_traffic_summary (REGION, CALL_MONTH);
```

Los números tras el primer refresh eran los que esperábamos. La consulta de agregación mensual que tardaba 45 segundos bajó a 2 segundos — y esos 2 segundos eran casi en su totalidad latencia de red y renderizado de la aplicación, no procesamiento de la base de datos. La carga del dashboard de marketing pasó de 3 minutos a unos 10 segundos.

El PM vio los resultados en una pantalla de prueba la tarde anterior a la demo. No dijo mucho. Asintió, preguntó si estábamos seguros de que los datos eran correctos, y cuando le confirmamos que sí, eran los mismos datos de antes solo pre-agregados, dijo "bien" y cerró el portátil.

Era el tipo de aprobación silenciosa que vale más que cualquier cumplido.

## Más allá de la demo: el valor que permanece

La demo salió bien. El equipo de marketing del cliente interactuó con los reportes, hizo preguntas sobre los datos, preguntó si era posible añadir filtros por tipo de contrato y por área geográfica. Nadie comentó la velocidad — y ese era exactamente el resultado correcto. Cuando un sistema funciona como debe, los usuarios no piensan en la infraestructura. Piensan en los datos.

La objeción implícita que sobrevolaba el proyecto — "ya tenemos los datos, ¿por qué deberíamos invertir en un DWH separado?" — se disolvió en el momento en que el equipo de marketing vio patrones que antes no podía ver. No porque los datos fueran nuevos, sino porque eran accesibles de una forma diferente. La reportística agregada y navegable cambia el tipo de preguntas que se pueden hacer.

Las Materialized Views no eran la respuesta a todo. El DWH todavía necesitaba trabajo: la gestión de las actualizaciones incrementales, la historización de los maestros, el tratamiento de las excepciones en los CDR. Pero habían resuelto el problema que bloqueaba el proyecto en ese momento concreto, y habían fijado un principio arquitectónico que usaríamos como base para el resto del desarrollo: pre-calcular lo que es estable, dejar dinámico solo lo que debe serlo.

El proyecto no se quedó en prototipo. En los meses siguientes se convirtió en un contrato.

## Lo que queda en el cuaderno

La lección más útil de esta historia no tiene que ver con las Materialized Views en sí. Tiene que ver con el momento en que una herramienta técnica se vuelve relevante.

Las MV no eran una novedad para ninguno de nosotros. Eran una herramienta que conocíamos, que habíamos usado en otros contextos, que sabíamos que funcionaba en determinados escenarios. El valor no estaba en la invención, sino en el reconocimiento: este problema, en este momento, con estas restricciones de tiempo, se resuelve así.

Hay situaciones en que la solución correcta es la que ya conoces, no la que estás intentando aprender. Saber cuándo aplicar lo que ya tienes en el cajón es una competencia que se construye con los años y con los proyectos, no con los tutoriales.

El PM dio confianza y espacio para implementar algo que no estaba en el plan original. El equipo colaboró para verificar la corrección de los datos tras el refresh. El DBA del cliente revisó el impacto sobre el sistema fuente durante la ventana de refresh nocturna y dio el visto bueno. Nadie salvó nada solo — salió bien porque las personas adecuadas hicieron las cosas adecuadas en el momento adecuado.

El cuaderno técnico se enriquece así: no con soluciones nuevas, sino con contextos en los que las soluciones antiguas siguen funcionando.

## Fuentes oficiales

1. Oracle Database SQL Language Reference 19c — [CREATE MATERIALIZED VIEW](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-MATERIALIZED-VIEW.html) — sintaxis completa, opciones `REFRESH FAST/COMPLETE`, `ON COMMIT`, `BUILD IMMEDIATE/DEFERRED`
2. Oracle Database Data Warehousing Guide 19c — [Basic Materialized Views](https://docs.oracle.com/en/database/oracle/oracle-database/19/dwhsg/basic-materialized-views.html) — conceptos, estrategias de uso en DWH, query rewriting
3. PostgreSQL Documentation — [Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html) — `CREATE MATERIALIZED VIEW`, `REFRESH MATERIALIZED VIEW`, opción `CONCURRENTLY`

## Glosario
- **[Materialized View (MV)](/es/glossary/materialized-view/)** — Vista pre-calculada y almacenada físicamente en disco. Contiene el resultado de una consulta ejecutada de antemano; las lecturas posteriores leen datos ya agregados sin recalcular. Compatible con Oracle, PostgreSQL, SQL Server y otros RDBMS.

- **[Refresh (MV)](/es/glossary/materialized-view/)** — Proceso de actualización de los datos de una Materialized View para reflejar los cambios en las tablas base. Puede ser completo (recálculo total) o incremental (solo las variaciones rastreadas en los MV log). La frecuencia y la modalidad son decisiones arquitectónicas con impacto directo en el rendimiento.

- **[Call Detail Record (CDR)](/es/glossary/refresh/)** — Registro que describe una única llamada telefónica: identificador de cliente, fecha, duración, tipo de llamada, coste. En los sistemas telco los CDR son el dato operativo primario y se acumulan en volúmenes muy elevados (cientos de GB mensuales para operadores de tamaño medio).

- **[Query Rewriting](/es/glossary/materialized-view/)** — Funcionalidad de Oracle que intercepta automáticamente una consulta sobre las tablas base y la redirige hacia una Materialized View equivalente, sin modificaciones en el código de la aplicación. Se activa con `ENABLE QUERY REWRITE` en la definición de la MV.

- **[Data Warehouse (DWH)](/es/glossary/refresh/)** — Sistema de base de datos optimizado para el análisis de datos históricos, que agrega información de distintas fuentes operativas. A diferencia de los sistemas OLTP, prioriza las lecturas masivas y las agregaciones frente a las escrituras frecuentes y puntuales.
