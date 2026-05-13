---
title: "ENUM en PostgreSQL: cuando la elección compensa, y cuando se vuelve en tu contra"
seoTitle: "PostgreSQL ENUM vs CHECK vs lookup: la elección correcta"
description: "PostgreSQL ENUM vs CHECK vs tabla lookup: ALTER TYPE ADD VALUE no cuesta nada, eliminar un valor cuesta una migración. Tres caminos, un caso telco real."
date: "2026-06-09T08:03:00+01:00"
draft: false
translationKey: "enum_postgresql_paga_o_pesa"
tags: ["enum", "data-modeling", "schema-design", "alter-type", "check-constraint"]
categories: ["postgresql"]
image: "enum-postgresql-paga-o-pesa.cover.jpg"
---

La pregunta es la misma que nos hicimos [para MySQL](/es/posts/mysql/enum-mysql-semplifica-o-complica/): una columna `status` o `type` con un conjunto cerrado de valores, y tres caminos por delante — tipo enumerativo nativo, CHECK constraint, tabla de lookup. Cambia la base de datos, cambia la filosofía, y cambia también dónde cae el precio.

PostgreSQL tiene su propio ENUM, declarado como tipo independiente con `CREATE TYPE ... AS ENUM`. Está pensado de forma distinta al de MySQL: type-safe como un domain, transaccional como todo el resto del DDL, y con un detalle que hace tropezar a casi todos al primer paso — es **case-sensitive**. Para quien viene de MySQL es incómodo; para quien siempre ha trabajado con PostgreSQL es natural.

Vale la pena entrar en detalle, porque PostgreSQL ENUM no es "MySQL ENUM con otra sintaxis". Es otra cosa. Hay que entenderla por lo que es.

---

## Los tres caminos, en dos líneas cada uno

Usaremos el ejemplo de una tabla `suscripciones` con un estado que toma un conjunto cerrado de valores.

**ENUM nativo**:

```sql
CREATE TYPE estado_suscripcion AS ENUM (
  'ACTIVA','SUSPENDIDA','TERMINADA','VENCIDA'
);

CREATE TABLE suscripciones (
  id      BIGINT PRIMARY KEY,
  estado  estado_suscripcion NOT NULL
);
```

En PostgreSQL el tipo es un **objeto de primera clase**: lo creas una vez, lo reutilizas en muchas columnas, lo modificas con `ALTER TYPE`. Internamente la columna ocupa 4 bytes (un `OID` interno), el valor es validado por el motor, y la lectura devuelve la cadena original (case-sensitive).

**CHECK constraint**:

```sql
CREATE TABLE suscripciones (
  id      BIGINT PRIMARY KEY,
  estado  VARCHAR(20) NOT NULL,
  CONSTRAINT chk_estado 
    CHECK (estado IN ('ACTIVA','SUSPENDIDA','TERMINADA','VENCIDA'))
);
```

Enfoque SQL estándar. Más verboso pero más flexible (las condiciones de `CHECK` pueden ser arbitrariamente complejas). En PostgreSQL los `CHECK` constraint están plenamente aplicados desde siempre — nada de "silenciosamente ignorados" como pasaba en MySQL antes de la 8.0.16.

**Tabla de lookup con FK**:

```sql
CREATE TABLE estados_suscripcion (
  codigo      VARCHAR(20) PRIMARY KEY,
  etiqueta    VARCHAR(100) NOT NULL,
  activo      BOOLEAN DEFAULT TRUE
);

CREATE TABLE suscripciones (
  id            BIGINT PRIMARY KEY,
  estado_codigo VARCHAR(20) NOT NULL,
  CONSTRAINT fk_estado 
    FOREIGN KEY (estado_codigo) REFERENCES estados_suscripcion(codigo)
);
```

La vía "base-de-datos-pura". Más tablas, más JOIN, pero también más flexibilidad: atributos adicionales, etiquetas localizadas, orden de visualización, activación/desactivación en tiempo de ejecución.

---

## Qué cambia respecto a MySQL: tres cosas, antes de empezar

Si vienes de MySQL, hay tres detalles que conviene tener en el bolsillo antes de escribir el primer `CREATE TYPE`.

**Case-sensitive**. `'ACTIVA'` y `'activa'` son dos valores distintos. En MySQL eran el mismo valor — una decisión de diseño que a algunos parecía "cómoda" y a otros "resbaladiza". PostgreSQL toma el camino opuesto: si declaraste `'ACTIVA'`, siempre tendrás que escribir `'ACTIVA'`. Las consultas no normalizadas fallarán con *invalid input value*. Es rigor, y una vez que te acostumbras se aprecia, pero el primer día es una sorpresa que cuesta algunos minutos.

**Type safety real, no simulada**. ENUM es un tipo, no una restricción sobre `VARCHAR`. Puedes crear una función que acepte `estado_suscripcion` como parámetro, y el motor rechazará en parse-time cualquier llamada con una cadena libre. Lo mismo vale para procedimientos, vistas, índices parciales. En MySQL esta seguridad no existe — `ENUM` es una columna `VARCHAR` decorada.

**ALTER TYPE es casi gratis (y transaccional)**. Añadir un valor al final de un ENUM PostgreSQL es una operación de metadata. Ni rebuild de la tabla, ni bloqueo de escritura prolongado. Y como todo el DDL de PostgreSQL, está dentro de la transacción: si el commit falla, el ENUM queda como estaba. Esta es la diferencia más tangible respecto a MySQL, donde `MODIFY COLUMN ENUM(...)` sobre una tabla grande puede tenerte despierto una noche entera.

---

## Cuándo ENUM es la elección correcta en PostgreSQL

El mismo principio de MySQL, aplicado al contexto PostgreSQL: **conjunto de valores estable, semántica controlada por el esquema**. Cuando estos dos ingredientes están presentes, ENUM en PostgreSQL tiene incluso alguna ventaja extra respecto al primo MySQL:

1. **Type safety end-to-end**: ENUM es un tipo que atraviesa funciones, procedimientos, foreign data wrappers. No es solo una restricción sobre una columna, es una garantía de coherencia que PostgreSQL aplica a todo el stack de código SQL
2. **Almacenamiento compacto**: 4 bytes por fila (como un `INT` que actúa de FK), comparable a MySQL. En tablas de cientos de millones de filas no es el driver principal, pero es coherente
3. **ALTER TYPE ADD VALUE económico**: la modificación más frecuente — añadir un nuevo valor — cuesta prácticamente cero
4. **DDL transaccional**: añadir un valor dentro de una transacción que incluye también el deploy del código aplicativo es una garantía de atomicidad que pocos otros DBMS te regalan

En un sistema donde el dominio está realmente cerrado y bien definido, ENUM en PostgreSQL quita complejidad y añade seguridad. Una `CREATE TYPE`, una columna, fin.

---

## El caso concreto: estados de suscripción en un operador móvil

Nos tocó, hace unos proyectos, diseñar el modelo de datos para la gestión de las suscripciones de un operador móvil europeo. Stack PostgreSQL, millones de SIM activas, una tabla `suscripciones` con un `estado` leído por prácticamente todas las consultas del billing.

En la primera versión los estados eran cuatro, bien definidos por el negocio: `ACTIVA`, `SUSPENDIDA`, `TERMINADA`, `VENCIDA`. ENUM era la elección natural:

```sql
CREATE TYPE estado_suscripcion AS ENUM (
  'ACTIVA','SUSPENDIDA','TERMINADA','VENCIDA'
);

ALTER TABLE suscripciones
  ADD COLUMN estado estado_suscripcion NOT NULL DEFAULT 'ACTIVA';
```

Durante un año y medio funcionó en silencio. Type-safe, legible, performante. Ninguna tabla de lookup que seedear, ninguna FK que mantener en el deploy. Nadie se acordaba ya de ella — y ese es el mejor cumplido que se le puede hacer a un esquema.

Luego, como es normal, el producto creció.

La primera llamada llegó del equipo antifraude: hacía falta distinguir entre `SUSPENDIDA_POR_MOROSIDAD` y `SUSPENDIDA_VOLUNTARIA`. Operación fácil en PostgreSQL — aquí es donde la diferencia con MySQL se ve:

```sql
ALTER TYPE estado_suscripcion ADD VALUE 'SUSPENDIDA_POR_MOROSIDAD' AFTER 'SUSPENDIDA';
ALTER TYPE estado_suscripcion ADD VALUE 'SUSPENDIDA_VOLUNTARIA'    AFTER 'SUSPENDIDA_POR_MOROSIDAD';
```

Dos `ALTER TYPE` de metadata. Milisegundos. Ni rebuild, ni bloqueos significativos sobre una tabla `suscripciones` con decenas de millones de filas. La misma operación en MySQL, recuerdo, habría requerido un `MODIFY COLUMN ENUM(...)` con toda la tabla reescrita en Online DDL, y un DBA en pie delante del monitor.

Un punto a favor de PostgreSQL. De verdad.

Luego, unos trimestres más tarde, llegaron los problemas.

---

## Los límites, contados desde la experiencia

Los límites de PostgreSQL ENUM existen. No son peores que los de MySQL — son **diferentes**, y aparecen en puntos distintos del ciclo de vida.

**No se elimina un valor de forma nativa**. Parece un detalle, pero es el límite más grande. Si el negocio decide "retirar" el estado `VENCIDA` (porque tal vez en el nuevo modelo comercial es absorbido por `TERMINADA`), en PostgreSQL no tienes un `ALTER TYPE DROP VALUE`. Debes:

1. Crear un nuevo tipo con los valores reducidos
2. Actualizar todas las filas de la tabla para migrarlas al nuevo conjunto
3. Cambiar el tipo de la columna (`ALTER COLUMN ... TYPE`)
4. Dropear el tipo viejo

Todo esto, en una tabla grande, es exactamente la migración pesada que en MySQL habrías pagado para **añadir** un valor — aquí la pagas para **quitar** uno. La simetría es graciosa solo sobre el papel: en producción, sigue siendo mucha carga.

**Renombrar un valor es fácil, pero transaccional**. `ALTER TYPE ... RENAME VALUE 'X' TO 'Y'` existe desde PostgreSQL 10. Operación rápida y limpia. Pero — hay una sutileza — el ALTER TYPE está dentro de la transacción, sí, pero si el rename ocurre en una transacción que otras sesiones tienen abiertas sobre ese tipo, podrías encontrarte con locks. En sistemas con alta concurrencia no es tan trivial como parece.

**Ordenación por posición**. Como en MySQL, el orden en que has declarado los valores cuenta para `ORDER BY`. Si añadiste `SUSPENDIDA_POR_MOROSIDAD` `AFTER 'SUSPENDIDA'`, el orden es coherente. Pero si se te olvida y haces `ALTER TYPE ... ADD VALUE 'NUEVO'` sin especificar la posición, el valor va al final. El sort de los dashboards puede sorprenderte.

**Los índices GIN/GiST no lo tratan como cadena**. Ventaja o desventaja según el caso de uso, pero si pensabas hacer encima una full text search, recuerda que ENUM no es `text`. Hay que castearlo, y el cast a veces impide el uso del índice.

En el sistema de las suscripciones, después de dos años los estados habían pasado a once, y una solicitud de "limpieza" del dominio (eliminar tres, renombrar dos) transformó una aparente "modificación trivial" en una migración de un fin de semana, con dump-restore parcial de algunas tablas satélite que usaban el tipo. El precio había llegado — solo en un punto distinto del ciclo de vida respecto a MySQL.

---

## Cuándo pasar a CHECK o a lookup

Las banderas rojas son las mismas que en MySQL — la base de datos cambia, la lógica del proyecto no:

1. **Los valores cambian con frecuencia** — no solo se añaden, también se renombran o retiran. Si el vocabulario está en evolución activa, el esquema no es el lugar adecuado para alojarlo
2. **Hacen falta atributos adicionales** — descripciones multilingües, etiqueta breve/extensa, orden de visualización, flag activo. ENUM no los aloja
3. **Decenas de valores en crecimiento** — más allá de 20-30, el `CREATE TYPE` se vuelve una lista kilométrica difícil de leer

`CHECK` constraint en PostgreSQL es un compromiso intermedio limpio: más fácil de modificar que un ENUM (basta un `ALTER TABLE ... DROP CONSTRAINT ... ADD CONSTRAINT ...`), menos estructurado que una lookup real. Va bien para conjuntos de 5-15 valores que se tocan de vez en cuando.

En el caso de las suscripciones, la primera oleada de evolución (4 → 11 estados) la digerimos con `ALTER TYPE ADD VALUE`. La segunda oleada — la que pedía eliminaciones y renombrados múltiples — fue la ocasión para reescribir hacia una lookup table. No porque ENUM hubiera sido "incorrecto" desde el principio. Era correcto para un dominio pequeño y estable, y se volvió incómodo cuando el dominio dejó de ser estable.

---

## Lookup table bien hecha, con un ENUM dentro

También aquí el patrón es análogo al que vimos en MySQL, y — sorpresa hasta cierto punto — un ENUM dentro de la lookup table tiene sentido también en PostgreSQL.

```sql
CREATE TYPE codigo_estado_suscripcion AS ENUM (
  'ACTIVA','SUSPENDIDA','TERMINADA','VENCIDA'
);

CREATE TABLE estados_suscripcion (
  id          SMALLSERIAL PRIMARY KEY,
  codigo      codigo_estado_suscripcion NOT NULL UNIQUE,
  descripcion TEXT NOT NULL,
  orden       SMALLINT NOT NULL DEFAULT 0,
  activo      BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO estados_suscripcion (codigo, descripcion, orden) VALUES
  ('ACTIVA',     'Suscripción activa y operativa',         10),
  ('SUSPENDIDA', 'Suspendida, puede reactivarse',          20),
  ('TERMINADA',  'Cancelada por el cliente',               30),
  ('VENCIDA',    'Caducidad natural del contrato',         40);

CREATE TABLE suscripciones (
  id        BIGINT PRIMARY KEY,
  estado_id SMALLINT NOT NULL,
  CONSTRAINT fk_estado 
    FOREIGN KEY (estado_id) REFERENCES estados_suscripcion(id)
);
```

Las tres ventajas son las mismas que vimos en MySQL:

**La master lleva solo el id**, no el codigo. Dos bytes (`SMALLINT`) en lugar de los 4 del OID del ENUM directo — en tablas de cientos de millones de filas son GB ahorrados.

**Código y descripción son atributos de la lookup, no clave**. Renombrar la descripción de un estado — pasar de "Suspendida, puede reactivarse" a "Suspensión temporal, puede reactivarse" — es un `UPDATE` sobre una sola fila. Ni ALTER TYPE, ni migración sobre la master.

**Los atributos extra no cuestan nada**: un campo para la descripción breve, una tabla vinculada para las traducciones, un flag `valido_desde/valido_hasta` para gestionar estados válidos solo en ciertos periodos. Todo esto, con ENUM "puro" sobre la master, era inaccesible.

Y sobre el ENUM interno a la lookup, **todos los límites que enumeramos antes se vuelven irrelevantes**: la tabla `estados_suscripcion` tiene 11 filas, un rebuild sobre 11 filas es invisible, una migración es trivial. La restricción "solo admite estos valores" la pagamos a coste cero, sin escribir un `CHECK` separado.

### Añadir y retirar valores en el patrón lookup

En el patrón lookup, las dos operaciones "delicadas" se vuelven ligeras.

**Añadir un estado** (`RESERVADA`, porque ahora las suscripciones pueden "reservarse" antes de la activación):

```sql
-- Extiende el ENUM en la lookup (operación de metadata, milisegundos)
ALTER TYPE codigo_estado_suscripcion ADD VALUE 'RESERVADA' BEFORE 'ACTIVA';

-- Inserta la nueva fila
INSERT INTO estados_suscripcion (codigo, descripcion, orden, activo) VALUES
  ('RESERVADA', 'Suscripción reservada, aún no activa', 5, TRUE);
```

**Retirar un estado** (`VENCIDA` absorbida por `TERMINADA`): aquí en PostgreSQL no hay `DROP VALUE`. Pero en una lookup de pocas filas, recrear el tipo es cuestión de pocos segundos incluso en producción:

```sql
-- 1. Migra las filas de la lookup que usan el valor "viejo"
UPDATE estados_suscripcion SET codigo = 'TERMINADA' WHERE codigo = 'VENCIDA';
-- (Una sola fila; bajo la FK la master sigue apuntando al mismo id)

-- 2. Crea el nuevo tipo con el vocabulario actualizado
CREATE TYPE codigo_estado_suscripcion_v2 AS ENUM (
  'RESERVADA','ACTIVA','SUSPENDIDA','TERMINADA'
);

-- 3. Cambia el tipo de la columna en la lookup
ALTER TABLE estados_suscripcion 
  ALTER COLUMN codigo TYPE codigo_estado_suscripcion_v2 
  USING codigo::text::codigo_estado_suscripcion_v2;

-- 4. Dropea el tipo viejo
DROP TYPE codigo_estado_suscripcion;
ALTER TYPE codigo_estado_suscripcion_v2 RENAME TO codigo_estado_suscripcion;
```

Cuatro pasos, todos sobre una tabla pequeña. La master `suscripciones` — la de cientos de millones de filas — nunca se toca. Sigue referenciando `estado_id`, y la FK resuelve siempre a la fila correcta de la lookup. **La integridad está anclada al id subrogado**, no al código ENUM, y esta es la clave del patrón.

---

## La regla de oro

El mensaje que me llevo del caso de las suscripciones — y que vale, idéntico, tanto en PostgreSQL como en MySQL — es:

> Si los valores del dominio no van a cambiar nunca, ENUM es la elección correcta. Si van a cambiar — aunque sea "de vez en cuando" — no ates el vocabulario al esquema.

La diferencia entre las dos bases de datos no está en esta regla. Está en **dónde cae el precio** cuando el dominio cambia:

- **En MySQL**, añadir un valor en posición específica cuesta un rebuild de la tabla. Añadirlo al final es económico, pero corrompe el ordenamiento.
- **En PostgreSQL**, añadir es siempre económico (incluso en posición específica). Eliminar o reorganizar es la migración pesada.

Entender tu caso de uso significa entender **qué tipo de evolución es probable que sufra el dominio**. ¿Solo añadidos? PostgreSQL ENUM es un aliado. ¿Añadidos y eliminaciones? Mejor una lookup table desde el principio.

---

## La miniserie cross-DB

Este es el segundo de una miniserie sobre las enumeraciones en los distintos DBMS. La pregunta "¿ENUM o lookup?" no tiene una respuesta universal — cambia de cara según la base de datos. El primer artículo, sobre MySQL, está disponible aquí:

- **[ENUM en MySQL: cuando te simplifica la vida y cuando te complica los días](/es/posts/mysql/enum-mysql-semplifica-o-complica/)** — la misma pregunta, una filosofía distinta, y el caso real de un sistema de tracking de envíos

Las próximas entregas:

- **Oracle** — `CHECK` constraint, los SQL Domains de 23ai, y por qué Oracle llegó "tarde" a este tema
- **Oracle, deep-dive vertical** — cómo se modelaban las enumeraciones en 19c, qué cambió en 21c, 23ai y 26ai, hasta llegar a las nuevas Assertions

> 📖 **Si has llegado aquí primero**: te recomiendo leer también [el primer artículo de la miniserie, el de MySQL](/es/posts/mysql/enum-mysql-semplifica-o-complica/). Muchos de los patrones que aparecen aquí — los tres caminos, la lookup table bien hecha, el ENUM dentro de la lookup — se introducen allí. La comparación lo hace todo más claro.

------------------------------------------------------------------------

## Glosario

**[CREATE TYPE AS ENUM](/es/glossary/postgresql-create-type-enum/)** — Statement DDL de PostgreSQL que crea un tipo enumerativo como objeto de primera clase. A diferencia de MySQL, el tipo existe independientemente de las columnas que lo usan y puede ser reutilizado.

**[ALTER TYPE ADD VALUE](/es/glossary/postgresql-alter-type-add-value/)** — Comando PostgreSQL que añade un valor a un ENUM existente. Operación de metadata, transaccional, sin rebuild de la tabla. Disponible desde PostgreSQL 9.1, con posicionamiento `BEFORE`/`AFTER` desde 9.6.

**[OID (Object Identifier)](/es/glossary/postgresql-oid/)** — Identificador numérico interno usado por PostgreSQL para referirse a objetos del sistema (tablas, tipos, funciones). Para los ENUM, el valor está almacenado como OID interno de 4 bytes.

**[Type safety](/es/glossary/type-safety/)** — Propiedad de un sistema de tipos que impide, en parse-time o compile-time, el uso de valores incompatibles. ENUM en PostgreSQL es un tipo independiente, no una restricción sobre `VARCHAR`, y esto habilita type safety end-to-end en funciones y procedimientos.

**[Lookup table](/es/glossary/lookup-table/)** — Tabla de referencia vinculada vía foreign key que almacena los valores válidos de una enumeración, con eventuales atributos descriptivos (etiqueta, orden, flag activo). Patrón preferido cuando el dominio evoluciona en el tiempo.
