---
title: "Oracle 19c, 21c, 23ai, 26ai: la reescritura silenciosa de los dominios de valores"
seoTitle: "Oracle 19c → 26ai: SQL Domains y Assertions en 7 años"
description: "Siete años de Oracle vistos a través de las enumeraciones: del CHECK del 19c a los SQL Domains del 23ai, hasta las Assertions del 26ai. Migración aseguradora."
date: "2026-06-23T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_19c_26ai_domini"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-19c-26ai-domini.cover.jpg"
---

En los últimos siete años Oracle ha reescrito en silencio cómo se modelan los **dominios de valores** en un esquema. Sin anuncios resonantes, sin la fanfarria que PostgreSQL y MySQL han sabido construir alrededor de sus `ENUM`. Cuatro major release — 19c, 21c, 23ai, 26ai — y una trayectoria que, vista desde arriba, cuenta una historia precisa: Oracle llegó el último, y llegó con una solución diferente.

Si buscas el cuadro horizontal (Oracle vs MySQL vs PostgreSQL, los tres caminos comparados lado a lado), está en [este artículo de la miniserie](/es/posts/oracle/enum-oracle-workaround-fino-a-23ai/). Aquí tomamos en cambio la lente vertical: una sola plataforma, siete años, cuatro releases. Qué tenías a disposición en cada período, qué cambia en lo que viene después.

---

## 19c (2019): el punto de partida

Oracle Database 19c, lanzada en 2019, es todavía hoy la **long-term release de referencia** para muchísimos sistemas enterprise — banking, asegurador, administración pública italiana, donde los upgrades tienen un ciclo largo y prudente. Cuando esta historia comienza, las herramientas a disposición para modelar una enumeración eran dos, y ninguna de las dos era "elegante":

```sql
-- Opción 1: CHECK inline (Oracle 19c)
CREATE TABLE polizas (
  id          NUMBER PRIMARY KEY,
  numero      VARCHAR2(20) NOT NULL,
  estado      VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_estado_poliza CHECK (estado IN
    ('EMITIDA','VIGENTE','SUSPENDIDA','VENCIDA','ANULADA','REVERSADA'))
);

-- Opción 2: lookup table con FK (Oracle 19c)
CREATE TABLE estados_poliza (
  codigo    VARCHAR2(20) PRIMARY KEY,
  etiqueta  VARCHAR2(100) NOT NULL,
  orden     NUMBER,
  activo    CHAR(1) DEFAULT 'Y' CHECK (activo IN ('Y','N'))
);

CREATE TABLE polizas (
  id             NUMBER PRIMARY KEY,
  numero         VARCHAR2(20) NOT NULL,
  estado_codigo  VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_estado FOREIGN KEY (estado_codigo)
    REFERENCES estados_poliza(codigo)
);
```

El `CHECK` es ligero, aplicado por el motor en runtime y usado incluso por el optimizador para **podar condiciones imposibles** [1] — pero es local a la columna, y replicar el mismo vínculo en veinte tablas que comparten el mismo dominio es un ejercicio de paciencia (y de disciplina en los code review). La lookup table es la vía del database puro, dominante en los proyectos enterprise: un JOIN más, pero también una enumeración que se vuelve un **objeto del database con vida propia** — etiquetas localizadas, orden de display, flag activo/inactivo, audit trail.

En 19c **esto era todo**. Ningún `CREATE TYPE ENUM` como PostgreSQL, ningún `ENUM` de columna como MySQL. Para quien venía de esos dos mundos, la sensación era: *"¿entonces no hay nada nativo?"*. Respuesta: no. Había el `CHECK`, había la lookup, y había veinte años de oficio acumulado sobre cómo hacerlos funcionar juntos.

---

## 21c (2021): una innovation release que se salta los dominios de valores

Oracle Database 21c — la "innovation release", llegada a Cloud en 2020 y on-premises en 2021 — trae cosas grandes: el **tipo JSON nativo** [2], las **blockchain table** y las **immutable table** para audit no manipulable, los **SQL Macros** para reusar fragmentos de SQL, la integración AutoML in-DB. Es una release llena de ideas nuevas.

Pero para quien miraba al problema específico de la modelización de los dominios de valores, **21c no aporta nada**. Ningún `CREATE DOMAIN`, ninguna revisión del `CHECK`, ninguna meta-taxonomía integrada en el diccionario de datos. La elección del DBA que migra de 19c a 21c, sobre el tema enumeraciones, no cambia: `CHECK` o lookup.

Aún así vale la pena nombrarla, porque marca un pasaje: Oracle en esos dos años estaba trabajando en otra cosa, y quien esperaba una respuesta sobre el frente schema-domain debía esperar. **La espera duró dos años más de lo que se pensaba**, y terminó con el salto numérico hacia la 23ai — la primera señal, no solo nominal, de que Oracle estaba por cambiar de paso.

---

## 23ai (2024): SQL Domains, por fin

Abril de 2024, Oracle Database 23ai lanzada sobre engineered system (Exadata Cloud@Customer primero, luego disponibilidad más amplia). Entre las decenas de novedades — y hay muchas, desde la `JSON Relational Duality` hasta los `AI Vector Search` — el constructo que importa para nuestra historia es uno solo: el **SQL Domain** [3].

```sql
-- Oracle 23ai
CREATE DOMAIN estado_poliza AS VARCHAR2(20)
  CONSTRAINT chk_estado_poliza CHECK (VALUE IN
    ('EMITIDA','VIGENTE','SUSPENDIDA','VENCIDA','ANULADA','REVERSADA'))
  DEFAULT 'EMITIDA'
  ANNOTATIONS (
    display 'Estado Póliza',
    description 'Ciclo de vida de una póliza de seguros',
    ordering 'EMITIDA<VIGENTE<SUSPENDIDA<VENCIDA<ANULADA<REVERSADA'
  );

CREATE TABLE polizas (
  id      NUMBER PRIMARY KEY,
  numero  VARCHAR2(20) NOT NULL,
  estado  estado_poliza NOT NULL
);

CREATE TABLE historico_polizas (
  id_poliza    NUMBER,
  fecha_evento DATE,
  estado       estado_poliza NOT NULL,
  CONSTRAINT fk_pol FOREIGN KEY (id_poliza) REFERENCES polizas(id)
);
```

Tres cosas vale la pena leer con calma en este bloque.

**Primero**: el `DOMAIN` es un **objeto del diccionario de datos**. Se encuentra en `DBA_DOMAINS`, `USER_DOMAINS`, `ALL_DOMAINS`, con columnas que describen el tipo base, el vínculo, el default. Por primera vez, en Oracle, la **enumeración existe como entidad en el catálogo de esquema** sin requerir una segunda tabla de lookup. El design review que preguntaba "¿dónde está documentado que `estado` puede tomar solo estos seis valores?" encuentra ahora una respuesta directa.

**Segundo**: las `ANNOTATIONS`. Son pares clave/valor de metadatos que las herramientas BI, los procedimientos de UI generation y los frameworks de reporting pueden leer vía `USER_ANNOTATIONS_USAGE` para derivar automáticamente etiquetas de display, descripciones de campo, ordering de representación. En PostgreSQL el `DOMAIN` tiene solo tipo + vínculo; Oracle aquí dio un paso más, y es un paso que se nota cuando un report Power BI o Tableau se apoya directamente sobre el diccionario para construir sus mapas semánticos.

**Tercero**: una sola columna `estado` de tipo `estado_poliza` puede ser usada en **decenas de tablas**, y en todas se aplica el mismo vínculo, el mismo default, las mismas annotations. Lo que con el `CHECK` requería veinte `ALTER TABLE` para ser modificado, con el `DOMAIN` requiere un único `ALTER DOMAIN` [4].

---

## Una migración 19c → 23ai concreta

El esquema de una compañía aseguradora — multi-país, sector Surety — en Oracle 19c, alrededor de 1.800 tablas en el esquema aplicativo, y una taxonomía de estados de póliza replicada en **22 tablas** del módulo de gestión contratos. Cada vez que compliance pedía añadir un nuevo estado (última vez: `'EN_VERIFICACION_ANTILAVADO'` por una nueva policy normativa) eran 22 `ALTER TABLE` por planificar, testear, deployar en ventana nocturna.

El upgrade a 23ai no se hizo **por** este problema — se hizo por otras razones (consolidación infraestructural, fin del soporte Premier en 19c). Pero una vez en 23ai, el equipo arquitectural puso en plan un pequeño refactor: convertir la taxonomía de estados póliza en un SQL Domain único.

Los pasos, en síntesis, fueron estos:

```sql
-- 1) Creación del domain con los valores históricos ya presentes en producción
CREATE DOMAIN estado_poliza AS VARCHAR2(20)
  CONSTRAINT chk_estado_poliza CHECK (VALUE IN
    ('EMITIDA','VIGENTE','SUSPENDIDA','VENCIDA','ANULADA','REVERSADA',
     'EN_VERIFICACION_ANTILAVADO'))
  DEFAULT 'EMITIDA';

-- 2) Sobre la tabla principal, declaración del domain en la columna existente
ALTER TABLE polizas MODIFY (estado estado_poliza);

-- 3) Lo mismo para cada una de las 21 tablas dependientes
ALTER TABLE historico_polizas MODIFY (estado estado_poliza);
ALTER TABLE polizas_primas    MODIFY (estado estado_poliza);
-- ... etc.

-- 4) Drop de los viejos CHECK inline redundantes (ahora el domain los sustituye)
ALTER TABLE polizas           DROP CONSTRAINT chk_estado_poliza;
ALTER TABLE historico_polizas DROP CONSTRAINT chk_estado_hist;
-- ... etc.
```

Las 22 tablas fueron migradas en una ventana de mantenimiento de poco más de una hora — casi todo el tiempo fue consumido por la **validación de las filas existentes** (`VALIDATE`, default en Oracle), que leyó cada tabla para confirmar que ningún valor histórico violara el vínculo del domain. Para las tablas más grandes (histórico pólizas, ~340 millones de filas) se eligió `NOVALIDATE` con un cleanup posterior vía batch: en producción la integridad hacia adelante estaba garantizada por el domain, y los datos históricos ya habían sido controlados con un script de pre-flight.

El resultado final, tras el refactor: una sola línea de DDL para modificar la taxonomía. La próxima petición de compliance — habrá una, siempre — costará un `ALTER DOMAIN`, no una semana de planificación.

No es una historia de heroísmo. Es la historia de un equipo que reconoció una oportunidad en el momento correcto y la tomó — Oracle finalmente había dado la herramienta, solo quedaba tomarla en la mano.

---

## 26ai (2026): ASSERTION y lo que se ve en el horizonte

Oracle 26ai (anunciada como próxima major release) trae sobre la mesa, entre otras cosas, las **`ASSERTION`**: un constructo SQL estándar sobre el papel desde hace décadas, nunca verdaderamente implementado por ningún DBMS mainstream, que permite expresar vínculos **cross-tabla** validados a nivel transaccional por el motor del database.

Para nuestra historia, las `ASSERTION` son la pieza que cierra un círculo. Con el SQL Domain del 23ai resolvimos el problema "mismo vínculo sobre muchas columnas". Con las `ASSERTION` del 26ai se abre otra posibilidad: vínculos que involucran **múltiples tablas juntas**, garantizados por el database sin que tenga que intervenir un trigger o un check aplicativo.

```sql
-- Ejemplo (sintaxis indicativa basada en el estándar SQL):
CREATE ASSERTION al_menos_un_estado_activo CHECK (
  (SELECT COUNT(*) FROM estados_poliza WHERE activo = 'Y') >= 1
);

CREATE ASSERTION historico_coherente CHECK (
  NOT EXISTS (
    SELECT 1 FROM polizas p
    LEFT JOIN historico_polizas h ON h.id_poliza = p.id
    WHERE p.estado = 'REVERSADA' AND h.estado IS NULL
  )
);
```

Vínculos así hoy se escriben como trigger — con todos los problemas del caso: triggers que se olvidan en deploys sucesivos, transacciones que bypassan el check por el isolation level, race condition difíciles de diagnosticar. Las `ASSERTION` desplazarían la responsabilidad al motor. Cuando 26ai esté disponible en test y sobre workloads reales, será materia para profundizar — pero el diseño de una taxonomía hoy ya puede tener en cuenta dónde los vínculos cross-tabla vivirán mejor mañana.

---

## Lo que Oracle sigue sin tener

Hay una cosa que, todavía hoy, Oracle no ofrece: un **tipo enumerativo nativo** como los de PostgreSQL (`CREATE TYPE ... AS ENUM`) o MySQL (`ENUM(...)`). Vale la pena decirlo abiertamente, porque alguien podría preguntárselo.

El SQL Domain es **conceptualmente más potente** que un ENUM tradicional (es un vínculo reutilizable, no un tipo "cerrado"), pero también es **más verboso** de declarar y tiene un overhead de indirección en el diccionario de datos. Para el caso de uso más simple — una columna en una sola tabla, conjunto de valores muy pequeño, ningún metadato — el `CHECK` inline sigue siendo más conciso. Oracle 23ai, en otras palabras, no sustituyó el `CHECK`: le añadió una herramienta para cuando el `CHECK` ya no bastaba.

Es coherente con la filosofía Oracle: dar herramientas potentes y generales, dejando al diseñador la responsabilidad de elegir el nivel correcto de abstracción. PostgreSQL y MySQL hicieron la elección opuesta — dar un tipo listo y específico — y para muchos casos esa elección es más inmediata. Son dos culturas diferentes, ambas legítimas.

---

## La trayectoria, vista desde finales de 2026

Siete años, cuatro releases, y una línea que desde fuera parece continua pero vista desde dentro está hecha de pausas y de saltos. La 19c era el punto de partida: dos caminos conocidos y ningún tercero. La 21c trajo otras cosas, quedándose quieta sobre este terreno. La 23ai abrió el **camino estructural** que faltaba desde hacía décadas. La 26ai cierra el círculo sobre los vínculos que superan la tabla individual.

No es una historia heroica. Oracle llegó después de PostgreSQL (que tiene los `DOMAIN` desde finales de los años '90) y después de MySQL (que tiene los `ENUM` desde siempre). Pero cuando llegó, llegó con una idea diferente — más general, más integrada en el diccionario, más extensible vía annotations — y esa idea se está convirtiendo en el modo estándar de modelar dominios de valores en los nuevos esquemas Oracle que veo nacer en producción hoy.

La pregunta que llevarse a casa, para quien modela esquemas enterprise en Oracle: **ya no "qué camino tomo", sino "cuándo el `CHECK` inline me basta, y cuándo vale la pena declarar un `DOMAIN`"**. Las dos opciones conviven, y saber cuándo pasar de una a la otra es hoy el verdadero discrimen.

---

## Fuentes oficiales

1. Oracle Database 19c SQL Language Reference — [constraint_clause (CHECK y otros vínculos)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html)
2. Oracle Database 21c Database New Features Guide — [Innovation Release overview](https://docs.oracle.com/en/database/oracle/oracle-database/21/nfcoa/index.html)
3. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
4. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glosario

- **[SQL Domain](/es/glossary/oracle-sql-domain/)** — Constructo introducido en Oracle 23ai que permite definir un dominio reutilizable (tipo base + CHECK + DEFAULT + annotations) como objeto del diccionario de datos. Por primera vez en Oracle, una enumeración existe en el catálogo de esquema sin requerir una tabla de lookup.
- **[Annotations (Oracle 23ai)](/es/glossary/oracle-annotations/)** — Pares clave/valor de metadatos asociables a objetos del esquema (columnas, domain, tablas), legibles vía `USER_ANNOTATIONS_USAGE`. Usadas por herramientas BI y UI generation para derivar automáticamente etiquetas de display, descripciones, ordering.
- **[VALIDATE / NOVALIDATE](/es/glossary/oracle-validate-novalidate/)** — Modos de aplicación de un vínculo Oracle en el momento de la creación o modificación: `VALIDATE` lee todas las filas existentes para verificar conformidad (default), `NOVALIDATE` salta el control para no bloquear tablas grandes en ventana de mantenimiento.
- **[Major release Oracle](/es/glossary/oracle-major-release/)** — Versión principal del Database server con cambios significativos de feature, ciclo de soporte Premier dedicado y numeración propia (19c, 21c, 23ai, 26ai). Diferentes de los patch set y las release update intermedias.
- **[ASSERTION](/es/glossary/sql-assertion/)** — Constructo SQL estándar para expresar vínculos cross-tabla validados a nivel transaccional por el motor del database. Anunciado en Oracle 26ai.
