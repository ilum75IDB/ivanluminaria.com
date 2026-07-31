---
categories:
- oracle
date: 2099-12-31
description: Oracle 26ai implementa CREATE ASSERTION, la restricción cross-tabla que
  SQL-92 prometía desde hace décadas. Sintaxis, comparación con triggers y casos reales
  en seguros.
draft: true
image: articolo-oracle-assertions-in-oracle-26ai.cover.jpg
seoTitle: 'CREATE ASSERTION en Oracle 26ai: restricciones cross-tabla declarativas'
tags:
- oracle-26ai
- integrity-constraints
- assertions
- sql-standard
- oracle-23ai
title: 'Tres triggers, un job nocturno y 1.247 pólizas huérfanas: ASSERTION en Oracle
  26ai'
translationKey: articolo_oracle_assertions_in_oracle_26ai
webo_generated_at: 2026-07-31
webo_status: da_tradurre
---

## Tres triggers, un job nocturno y 1.247 pólizas huérfanas

Era una migración batch de rutina — o al menos eso parecía. Un gran grupo asegurador italiano estaba consolidando datos históricos desde un sistema legacy: varios millones de filas en `polizze` y `beneficiari`, ventana de mantenimiento el sábado por la noche, script probado en staging. Para acelerar la carga, el equipo había deshabilitado temporalmente los triggers en las dos tablas. Procedimiento estándar, documentado en el runbook.

El problema apareció el domingo por la mañana, cuando el job nocturno de reconciliación terminó su ejecución de 45 minutos sobre 2,1 millones de pólizas y produjo un informe con 1.247 filas anómalas: pólizas en estado `ATTIVA` sin ningún beneficiario asociado. Violación directa de una regla de negocio crítica — "toda póliza activa debe tener al menos un beneficiario con cuota total igual al 100%" — que el sistema debía garantizar en todo momento.

La regla estaba implementada con tres triggers coordinados: uno `AFTER INSERT OR UPDATE` sobre `polizze` que verificaba la presencia de beneficiarios cuando el estado pasaba a `ATTIVA`, uno `AFTER DELETE` sobre `beneficiari` que comprobaba que la póliza vinculada no quedara huérfana, y un tercero `AFTER UPDATE` sobre `beneficiari` que recalculaba las cuotas. Más el job nocturno como red de seguridad para los casos que se escapaban — y algo siempre se escapaba, especialmente durante operaciones batch con triggers deshabilitados.

Tiempo de detección: unas 18 horas. Tiempo de corrección manual: media jornada de trabajo. Coste real: bajo, por suerte. Pero la pregunta que quedó sobre la mesa tras el incidente era la correcta: ¿existe alguna forma de expresar esta regla a nivel de esquema, de modo que no pueda ser eludida por ninguna operación DML, batch o no?

Con Oracle 26ai, la respuesta es sí.

## SQL-92 tenía razón, pero nadie le había hecho caso

El estándar SQL define `CREATE ASSERTION` desde 1992. La idea es sencilla: una restricción de integridad no debe limitarse a una sola fila o a una sola tabla — debe poder expresar predicados sobre el estado completo de la base de datos. La sintaxis original del estándar es:

```sql
CREATE ASSERTION nombre_restriccion CHECK (condicion_booleana)
```

donde `condicion_booleana` puede involucrar subqueries, agregaciones, joins entre tablas distintas. Semánticamente, la restricción se cumple cuando la condición es `TRUE` o `UNKNOWN`; se viola cuando es `FALSE`.

El problema es que ningún RDBMS mainstream había implementado nunca esta funcionalidad de forma completa. PostgreSQL no la tiene. MySQL no la tiene. SQL Server no la tiene. Los motivos son conocidos: evaluar un predicado que atraviesa varias tablas tiene un coste potencialmente elevado, y el momento correcto para hacerlo — ¿tras cada instrucción DML individual, o al final de la transacción? — abre cuestiones de implementación nada triviales. Resultado: durante treinta años, la funcionalidad permaneció en el documento del estándar sin llegar a los productos.

Oracle 23ai (renombrado posteriormente 26ai en la versión siguiente) es el primer RDBMS enterprise mainstream en llevarla a producción [1]. Es una decisión con un peso conceptual preciso: señala que Oracle se está tomando en serio la conformidad con el estándar SQL en funcionalidades que otros vendors han ignorado, y que el modelo relacional — con sus restricciones declarativas — sigue siendo la dirección de desarrollo, no una herencia que gestionar.

La distinción fundamental respecto a un `CHECK` constraint ordinario es esta: un `CHECK` evalúa un predicado sobre las columnas de la fila actual, en el momento de la inserción o la actualización. Una `ASSERTION` evalúa un predicado sobre el contenido completo de las tablas involucradas, tras cada operación DML que pudiera hacerlo falso. Son herramientas distintas para problemas distintos.

## `CREATE ASSERTION` en Oracle 26ai: la sintaxis

Retomando el esquema del proyecto asegurador, las dos tablas de referencia son:

```sql
-- Schema ins_core en oracle-node-01
CREATE TABLE polizze (
    id            NUMBER PRIMARY KEY,
    numero        VARCHAR2(20) NOT NULL,
    stato         VARCHAR2(10) CHECK (stato IN ('BOZZA','ATTIVA','SCADUTA','ANNULLATA')),
    data_inizio   DATE NOT NULL,
    data_fine     DATE
);

CREATE TABLE beneficiari (
    id            NUMBER PRIMARY KEY,
    id_polizza    NUMBER NOT NULL REFERENCES polizze(id),
    nome          VARCHAR2(100) NOT NULL,
    quota_pct     NUMBER(5,2) NOT NULL CHECK (quota_pct > 0 AND quota_pct <= 100)
);
```

La restricción que los tres triggers intentaban garantizar se expresa así:

```sql
-- Toda póliza ATTIVA debe tener al menos un beneficiario
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

Este es el patrón existencial clásico: "no existe ninguna póliza activa para la que no exista ningún beneficiario". La doble negación es la forma estándar de expresar "para todo X debe existir al menos un Y" en SQL, y las Assertions lo hacen por fin declarable a nivel de esquema [2].

La segunda restricción — las cuotas deben sumar 100 — usa un patrón con agregación:

```sql
-- Las cuotas de los beneficiarios de cada póliza ATTIVA deben sumar 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

Este segundo patrón es el que con los `CHECK` constraints tradicionales es sencillamente imposible de expresar: la condición involucra una agregación sobre filas distintas de la misma tabla, filtrada por join con otra tabla.

Para eliminar una Assertion:

```sql
DROP ASSERTION ins_core.polizza_ha_beneficiario;
```

La documentación de Oracle 26ai contempla también la posibilidad de deshabilitar temporalmente una Assertion con `DISABLE` y rehabilitarla con `ENABLE`, de forma análoga a los constraints tradicionales [1]. Este punto es relevante para las operaciones de mantenimiento — pero, como veremos, es también exactamente el punto crítico que hay que gestionar con cuidado.

## Por qué las alternativas pre-26ai no eran equivalentes

Vale la pena ser precisos en esto, porque la tentación de decir "también se puede hacer con triggers" es real — y técnicamente cierta, pero oculta diferencias importantes.

| Mecanismo | Declarativo | Resiste bulk load | Legible desde esquema | Coste de evaluación |
|---|---|---|---|---|
| `CHECK` constraint | ✅ | ✅ | ✅ | Bajo (fila única) |
| Trigger `AFTER` | ❌ | ❌ (deshabilitables) | ❌ | Medio (por fila) |
| `DEFERRABLE` constraint | ✅ | Parcial | ✅ | Bajo-medio |
| Materialised view + `WITH CHECK OPTION` | Parcial | ❌ | Parcial | Alto (refresh) |
| **ASSERTION** | ✅ | ✅ (si no se deshabilita) | ✅ | Medio-alto (cross-table) |

El `CHECK` constraint es declarativo y legible, pero no puede contener subqueries que referencien otras tablas — limitación conocida y documentada [3]. Oracle la aplica de forma explícita: un `CHECK` que intenta hacer `SELECT` sobre otra tabla genera un error en el momento de la creación.

Los triggers `AFTER INSERT/UPDATE/DELETE` funcionan, pero son procedurales. No aparecen en la definición del esquema de forma legible; se deshabilitan con `ALTER TABLE DISABLE ALL TRIGGERS` o con `ALTER TABLE ... DISABLE TRIGGER nombre`; en DML complejos con órdenes de disparo no triviales pueden producir resultados inesperados. El incidente de las 1.247 pólizas huérfanas es exactamente la consecuencia de esta fragilidad.

Los `DEFERRABLE` constraints gestionan la temporalidad — permiten posponer la verificación al final de la transacción en lugar de hacerla tras cada instrucción individual — pero no expresan predicados cross-tabla. Son útiles para DML multi-paso (inserta la fila padre, luego las hijas, verifica la foreign key solo al commit), no para restricciones que atraviesan tablas distintas [3].

Las materialised views con `WITH CHECK OPTION` son una aproximación creativa: se crea una vista que expone las violaciones, se añade una restricción sobre la vista. No es una restricción en sentido estricto, tiene costes de refresh, y el comportamiento en escenarios de concurrencia es menos predecible.

## Cuándo tiene sentido usarlas, y cuándo no

Las Assertions no son gratuitas. El coste de evaluación es real: cada operación DML sobre una tabla involucrada en una Assertion puede requerir la ejecución de la subquery de verificación. En tablas con DML de alta frecuencia — millones de inserts por segundo, sistemas OLTP con latencia crítica — este overhead hay que medirlo antes de adoptar la funcionalidad en producción.

Los casos en que las Assertions tienen sentido:

- **Reglas de integridad estables en el tiempo**: si el predicado cambia raramente, el coste de `DROP/CREATE` es asumible. Si la regla cambia cada sprint, los triggers son más flexibles.
- **Frecuencia DML moderada**: sistemas transaccionales normales, no pipelines de ingesta de alto throughput.
- **Predicados que involucran agregaciones o existencia cross-tabla**: exactamente los casos que los `CHECK` constraints no cubren.
- **Entornos donde la legibilidad del esquema es crítica**: auditoría, compliance, incorporación de nuevos DBAs — tener la restricción declarada en el esquema es una ventaja documental concreta.

Los casos que hay que evitar o evaluar con cuidado:

- **Bulk load con direct-path insert**: el `INSERT /*+ APPEND */` en Oracle bypasea el buffer cache y escribe directamente en los datafiles. El comportamiento de las Assertions en este escenario — si se evalúan, cuándo, con qué granularidad — hay que verificarlo en el entorno específico [4]. No dar por sentado que el comportamiento sea idéntico al conventional insert.
- **Tablas con DML de altísima frecuencia**: el coste de evaluación se multiplica por cada operación. Medir primero.
- **Funcionalidad en fase de maduración**: Oracle 26ai es una versión reciente. Las Assertions son una funcionalidad nueva, y el comportamiento en edge cases — concurrencia elevada, rollbacks parciales, operaciones DDL concurrentes — hay que probarlo en el entorno de destino antes de adoptar en producción [4].

Un punto que vale la pena subrayar: también una Assertion se puede deshabilitar, con `DISABLE`. Esto significa que el problema de las operaciones de mantenimiento no desaparece — se desplaza. La diferencia respecto a los triggers es que deshabilitar una Assertion es una operación DDL explícita, visible en el catálogo del sistema, más difícil de hacer "por error" en un script de migración. No es una protección absoluta, pero es un mecanismo de seguridad más robusto.

## Patrones recurrentes: el recetario

Tres patrones cubren la mayor parte de las restricciones cross-tabla que se encuentran en la práctica.

**Patrón "al menos uno"** — cada fila de la tabla A debe tener al menos una fila correspondiente en B:

```sql
-- Toda póliza ATTIVA debe tener al menos un beneficiario
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

**Patrón "suma restringida"** — una agregación sobre filas de B, agrupadas por clave de A, debe respetar una condición:

```sql
-- Las cuotas de los beneficiarios de cada póliza ATTIVA deben sumar 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

**Patrón "todos deben"** — cada fila de A debe satisfacer una condición que involucra B (variante con condición negada):

```sql
-- Todo siniestro abierto debe referirse a una póliza en estado ATTIVA
-- (ejemplo con tabla sinistri adicional)
CREATE ASSERTION ins_core.sinistro_su_polizza_attiva CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.sinistri s
        JOIN   ins_core.polizze p ON p.id = s.id_polizza
        WHERE  s.stato = 'APERTO'
        AND    p.stato <> 'ATTIVA'
    )
);
```

Estos tres patrones, combinados, cubren la gran mayoría de las restricciones de integridad cross-tabla que en los sistemas pre-26ai acababan en triggers. La sintaxis es más verbosa que un `CHECK` constraint simple, pero es declarativa, legible, y vive en el esquema.

## La conexión con el artículo #88 y la dirección de Oracle

Quien haya leído el artículo sobre la evolución de Oracle de 19c a 26ai recordará que las Assertions aparecían en la última sección, como una de las funcionalidades más significativas de la nueva versión — pero sin mayor profundización. Este artículo es esa profundización.

En el contexto más amplio del roadmap de Oracle, las Assertions se encuadran en una tendencia precisa: acercar el producto a la conformidad completa con el estándar SQL, en funcionalidades que habían permanecido teóricas durante décadas. JSON Relational Duality, True Cache y las Assertions comparten esta característica — son respuestas a necesidades reales que el modelo relacional ya había teorizado, pero que los productos nunca habían implementado completamente.

No es nostalgia por el purismo relacional. Es reconocer que algunas ideas del modelo relacional — las restricciones declarativas en primer lugar — tienen un valor práctico concreto que la industria ha subestimado durante años, delegando en triggers y lógica de aplicación lo que debería haber estado en el esquema.

## La restricción que no se rompe porque no hay código que romper

Tres triggers coordinados, un job nocturno de 45 minutos, y 1.247 pólizas huérfanas encontradas 18 horas después del incidente. No es un desastre — es una situación gestionada, corregida, documentada. Pero el coste de mantenimiento de esos tres triggers a lo largo del tiempo es real: cada modificación a la lógica de negocio requiere actualizar el código procedural, probarlo, coordinar los firing orders, acordarse de rehabilitarlos después de cada operación batch.

La Assertion no es una varita mágica. Tiene un coste de evaluación, tiene limitaciones en escenarios de bulk load, es una funcionalidad nueva en una versión de Oracle que todavía no está en producción en todas partes. Antes de adoptarla en un sistema crítico, conviene probar el comportamiento específico en el entorno de destino — en particular para los patrones de DML que se usan realmente, no solo para los casos estándar.

El punto conceptual, sin embargo, es sólido: el código que no se escribe no se rompe. Una restricción declarada en el esquema es visible, legible, difícil de eludir por error. Un trigger es código procedural que vive en un lugar separado, se deshabilita con una instrucción, y requiere que quien hace la migración batch sepa que existe y que importa.

Mover la regla de negocio al lugar correcto — el esquema — es una decisión de diseño, no solo una cuestión técnica. Las Assertions de Oracle 26ai hacen posible esta elección por primera vez de forma declarativa en un RDBMS enterprise mainstream. Vale la pena entenderlas, incluso para quien no vaya a migrar a 26ai la semana que viene.

## Fuentes oficiales

1. Oracle Database 23ai — `CREATE ASSERTION` syntax and semantics — `<TODO: scout fuente oficial para "CREATE ASSERTION Oracle 23ai/26ai documentation">`
2. Oracle Database 23ai New Features Guide — Integrity Constraints — `<TODO: scout fuente oficial para "Oracle 23ai New Features Guide — Integrity Constraints">`
3. Oracle Database SQL Language Reference — [Constraint Clauses](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/constraint.html) — cubre `CHECK`, `DEFERRABLE`, restricciones de integridad existentes (URL a verificar para versión 26ai)
4. Oracle Database 26ai Release Notes — estado GA vs preview de las Assertions, limitaciones conocidas — `<TODO: scout fuente oficial para "Oracle 26ai Release Notes">`
5. ISO/IEC 9075 SQL Standard, SQL-92 — definición original de `CREATE ASSERTION` — `<TODO: scout referencia pública accesible para SQL-92 CREATE ASSERTION>`

## Glosario
- **[ASSERTION](/es/glossary/predicato-existential/)** (Oracle 26ai / estándar SQL) — restricción de integridad declarativa que expresa un predicado sobre el estado completo de la base de datos, pudiendo involucrar varias tablas. Definida en SQL-92, implementada por primera vez en un RDBMS enterprise mainstream con Oracle 23ai/26ai.

- **Predicado existencial** (SQL) — expresión lógica que afirma la existencia de al menos una fila que satisface una condición. En SQL se expresa típicamente con `EXISTS` o `NOT EXISTS` en subquery correlacionada; es el patrón base para las Assertions de tipo "al menos uno".

- **Predicado universal** (SQL) — expresión lógica que afirma que una condición se cumple para todas las filas de un conjunto. En SQL se expresa indirectamente con `NOT EXISTS (... WHERE NOT condicion)`, porque SQL no tiene un cuantificador universal nativo.

- **DEFERRABLE constraint** (Oracle / estándar SQL) — restricción de integridad cuya verificación puede posponerse al final de la transacción en lugar de hacerse tras cada instrucción DML individual. Útil para DML multi-paso, pero no equivalente a una Assertion: no expresa predicados cross-tabla.

- **Direct-path insert** (Oracle) — modalidad de carga de datos que bypasea el buffer cache y escribe directamente en los datafiles, activable con el hint `/*+ APPEND */`. Interactúa con las restricciones de integridad de forma distinta al conventional insert; el comportamiento con las Assertions debe verificarse caso por caso.
