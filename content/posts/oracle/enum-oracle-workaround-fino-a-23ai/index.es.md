---
title: "Enumeraciones en Oracle: veinte años de workaround, y el camino que se abrió con la 23ai"
seoTitle: "Oracle SQL Domains 23ai: enum, CHECK y lookup tables"
description: "Oracle nunca tuvo ENUM nativo. CHECK constraints, lookup tables y SQL Domains 23ai: tres caminos, un caso real banking, y qué llegará con la 26ai."
date: "2026-06-16T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_workaround_fino_a_23ai"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-workaround-fino-a-23ai.cover.jpg"
---

La pregunta es la misma que nos hicimos [para MySQL](/es/posts/mysql/enum-mysql-semplifica-o-complica/) y luego [para PostgreSQL](/es/posts/postgresql/enum-postgresql-paga-o-pesa/): una columna `status` o `type` con un conjunto cerrado de valores, y tres caminos por delante. Cambia el database, cambia la filosofía, y cambia también **lo que el database pone a disposición**. En Oracle, hasta hace poco, faltaba justamente la primera opción de las otras dos partes — el tipo ENUM nativo. Durante veinte años, modelar una enumeración en Oracle ha sido un ejercicio de workaround: dos caminos practicables y un tercero que nunca fue realmente una enumeración.

Con la 23ai llegó una respuesta estructural: los **SQL Domains** [1]. Vale la pena entrar en el detalle, porque Oracle llegó el último pero llegó bien — y mientras tanto la cultura "lookup table" que se formó en el campo no pierde su lugar.

---

## Los tres caminos, en dos líneas cada uno

Usaremos el ejemplo de una tabla `transacciones` con un estado que toma un conjunto cerrado de valores. Sector banking — el terreno clásico de Oracle en Italia, donde un plan de cuentas y una taxonomía de estados está regulada, auditada, raramente improvisada.

**CHECK constraint**:

```sql
CREATE TABLE transacciones (
  id       NUMBER PRIMARY KEY,
  importe  NUMBER(15,2) NOT NULL,
  estado   VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_estado CHECK (estado IN
    ('EN_ESPERA','AUTORIZADA','COMPLETADA','REVERTIDA','RECHAZADA'))
);
```

Enfoque SQL estándar. Oracle aplica los `CHECK` constraint desde hace décadas — ninguna sorpresa sobre la validez del vínculo como ocurría en MySQL antes de la 8.0.16. Simple, legible, y para proyectos pequeños lo resuelve enseguida. El precio, en un sistema real, se descubre después: la misma lista de valores se replica en cada tabla que tiene la misma columna `estado`, y cada modificación se convierte en un `ALTER TABLE` por cada tabla. Veremos por qué importa.

**Tabla de lookup con foreign key**:

```sql
CREATE TABLE estados_transaccion (
  codigo     VARCHAR2(20) PRIMARY KEY,
  etiqueta   VARCHAR2(100) NOT NULL,
  orden      NUMBER,
  activo     CHAR(1) DEFAULT 'Y' CHECK (activo IN ('Y','N'))
);

CREATE TABLE transacciones (
  id             NUMBER PRIMARY KEY,
  importe        NUMBER(15,2) NOT NULL,
  estado_codigo  VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_estado
    FOREIGN KEY (estado_codigo) REFERENCES estados_transaccion(codigo)
);
```

El camino "database puro" y — no es casualidad — la elección cultural dominante en los proyectos Oracle enterprise. Una tabla más, un JOIN más, y a cambio una enumeración que es **un objeto del database con vida propia**: le puedes adjuntar etiquetas localizadas, orden de display, flag activo/inactivo, audit trail sobre `MODIFY` de la taxonomía, y reglas de negocio más ricas que un simple "admitido/no admitido". En los sistemas que he visto en banking, telco y administración pública italiana en los últimos veinte años, **ocho veces de cada diez la elección fue esta** — y con buena razón.

**Pseudo-pattern (SUBTYPE, COLLECTION, type-object)**:

```sql
-- Desaconsejado como "enumeración" para una columna persistente:
CREATE OR REPLACE TYPE estado_transaccion_t AS OBJECT (
  codigo VARCHAR2(20)
);
/
```

Los `TYPE` de Oracle (SUBTYPE PL/SQL, COLLECTION SQL, type-object) son potentes, pero **no son ENUMs**. No dan validación nativa sobre los valores persistidos, no tienen un mecanismo de lookup legible vía SQL puro, y el diccionario de datos no los ve como "taxonomía". Son una herramienta de abstracción aplicativa, no un mecanismo de vínculo. Quien los ha usado para simular ENUMs generalmente se ha arrepentido cuando el primer report de negocio pidió saber "cuántos estados activos hay" — y de la tabla no se podían extraer sin una consulta PL/SQL.

---

## Qué cambia respecto a MySQL y PostgreSQL

Si llegas desde las dos partes anteriores de la miniserie, tres cosas hay que tener en cuenta antes de escribir el primer `CREATE TABLE` en Oracle.

**Ningún tipo ENUM nativo**. En MySQL tienes `ENUM('A','B','C')` como tipo de columna; en PostgreSQL tienes `CREATE TYPE ... AS ENUM` como objeto autónomo. En Oracle, hasta la 23ai, estas dos opciones simplemente no existían. Quedaban `CHECK` y lookup tables.

**`CHECK` se aplica plenamente desde siempre**. A diferencia de MySQL pre-8.0.16 (donde los `CHECK` se parseaban y silenciosamente se ignoraban [2]), Oracle valida los vínculos `CHECK` desde antes del milenio. Un detalle histórico pero relevante: si vienes de MySQL, aquí no hay duda sobre su eficacia.

**Cultura de la lookup table arraigada**. La comunidad Oracle, por el tipo de clientes que la usan (banking, asegurador, administración pública, telco), siempre ha preferido la lookup table al `CHECK`. No por dogma, sino porque en esos contextos la evolución del conjunto de valores es frecuente, el audit es obligatorio, la localización de las etiquetas es un estándar. La lookup table es un gimnasio de flexibilidad — el `CHECK` es una promesa de rigidez.

---

## Cuándo basta el `CHECK`

Quedándonos dentro del patrón de las otras dos partes, los casos en que `CHECK` en Oracle es realmente la elección correcta son pocos y precisos:

- **Conjuntos de valores que nunca cambiarán**. Polaridad de una medida (`'POS','NEG','ZERO'`), días de la semana, meses del año, polaridad contable (`'DEBE','HABER'`)
- **Tablas con una sola referencia al conjunto**. Si la columna existe en **una sola** tabla, el precio del `ALTER TABLE` para añadir un valor es marginal
- **Proyectos pequeños o monolíticos**, donde el dominio del valor está claro en el código y no necesita exponerse como "configuración" a las interfaces de usuario

Fuera de estos tres escenarios, según mi experiencia, el `CHECK` envejece mal. Veo emerger el mismo patrón en fase de evolución: el negocio pide añadir un nuevo valor — digamos `'AUTORIZACION_MANUAL'` para las transacciones que requieren intervención manual — y te das cuenta de que la cadena está replicada en 14 tablas. Catorce `ALTER TABLE`, catorce tests de regresión, catorce release notes. La lookup table habría requerido un `INSERT`.

---

## La cultura de la lookup table en Oracle (y por qué hay un motivo)

En un proyecto banking de hace algún tiempo — una plataforma de pagos, Oracle 19c, alrededor de 1.200 tablas en el esquema aplicativo, equipo distribuido Italia/Rumania — la taxonomía de los estados de transacción se había modelado con dos tablas:

- `estados_transaccion` (codigo, etiqueta_it, etiqueta_en, orden, activo, grupo)
- `estados_transaccion_audit` (trigger de MODIFY que mantenía la historia de quién había cambiado qué)

Sin `CHECK`. Una sola FK a `estados_transaccion.codigo` en cada columna de estado — `transacciones.estado_codigo`, `transacciones_historico.estado_codigo`, `movimientos.estado_codigo`, y una docena de otras tablas del módulo de reconciliación.

Parecía sobreingeniería, hasta el día en que compliance pidió poder "**congelar**" temporalmente un estado (por ejemplo `'REVERTIDA'`) durante una auditoría, sin eliminarlo del esquema — nada de nuevas filas con ese valor, pero las filas históricas debían permanecer legibles y consultables. Con la lookup table fue un `UPDATE estados_transaccion SET activo = 'N' WHERE codigo = 'REVERTIDA'` más algún check aplicativo. **Tres líneas de código**. Si hubiéramos tenido `CHECK` con la lista de cadenas inlined en 18 tablas, habría sido una semana de trabajo entre DDL, regression test y ventana de deploy.

No es la historia de un héroe — es la historia de una elección arquitectónica hecha cinco años antes por el equipo de diseño, y de un compliance que encontró el esquema listo para la pregunta que planteó. La cultura lookup table en Oracle creció a partir de cientos de episodios así.

---

## La llegada de los SQL Domains en 23ai

Con Oracle Database 23ai (lanzada en engineered system en abril de 2024 y luego en disponibilidad más amplia) llega un constructo que faltaba: el **SQL Domain** [1]. Es la primera vez que Oracle da una respuesta estructural al problema "centralizar el dominio de una columna como objeto del database".

```sql
CREATE DOMAIN estado_transaccion AS VARCHAR2(20)
  CONSTRAINT chk_estado_transaccion CHECK (VALUE IN
    ('EN_ESPERA','AUTORIZADA','COMPLETADA','REVERTIDA','RECHAZADA'))
  DEFAULT 'EN_ESPERA'
  ANNOTATIONS (display 'Estado Transacción',
               description 'Estado del ciclo de vida de una transacción');

CREATE TABLE transacciones (
  id       NUMBER PRIMARY KEY,
  importe  NUMBER(15,2) NOT NULL,
  estado   estado_transaccion NOT NULL
);
```

El `DOMAIN` es un objeto del diccionario de datos (visible en `DBA_DOMAINS`), reutilizable en cualquier columna, y trae consigo todo el paquete: el tipo base, el vínculo `CHECK`, un `DEFAULT`, y — característica original Oracle, no presente en el `DOMAIN` de PostgreSQL — un sistema de **annotations** que pueden ser leídas por las herramientas BI, de reporting y de UI generation para derivar etiquetas de display, descripciones, ordering, etc.

El punto fuerte no es la sintaxis — es el **ALTER DOMAIN**.

---

## `ALTER DOMAIN`: el superpoder que faltaba

```sql
ALTER DOMAIN estado_transaccion
  CONSTRAINT chk_estado_transaccion CHECK (VALUE IN
    ('EN_ESPERA','AUTORIZADA','COMPLETADA','REVERTIDA','RECHAZADA',
     'AUTORIZACION_MANUAL'));
```

Ese único statement actualiza el vínculo **para todas las columnas que usan `estado_transaccion`** — en 18 tablas, en 50, no importa. Oracle se hace cargo de propagar el check, y de validar las filas existentes (con `VALIDATE` o `NOVALIDATE`, según como prefieras gestionar la transición).

Es lo que la lookup table ya daba a nivel lógico (un único lugar donde cambiar los valores admitidos), ahora llevado a nivel del **catálogo schema**, sin requerir un JOIN, sin requerir una tabla en más, y sin los 4 bytes de OID de una FK numérica.

Para quien ha trabajado veinte años con Oracle, es una de esas features que hacen decir: "**por fin**". No porque la lookup table haya perdido su lugar — el domain no sustituye la lookup cuando se necesitan etiquetas localizadas, ordering de display dinámico o audit trail. La sustituye cuando se necesitaban **solamente** validación y default centralizados. Y esos casos son muchos.

---

## Cuándo elegir qué, hoy

Una guía operativa, sintética:

| Caso | Camino recomendado |
|------|--------------------|
| Conjunto fijo, 1 tabla, dominio del valor conocido e inmutable | `CHECK` constraint inline |
| Conjunto fijo, **múltiples** tablas, en Oracle pre-23ai | Lookup table con FK |
| Conjunto fijo, múltiples tablas, **en Oracle 23ai+** | `SQL DOMAIN` |
| Conjunto evolutivo + etiquetas localizadas + ordering dinámico + audit | Lookup table con FK (también en 23ai+) |
| Validación cross-tabla (ej. suma de estados = N) | Trigger hoy, `ASSERTION` (26ai, próximamente) mañana |

La lookup table **no ha muerto** con los SQL Domains. Sigue siendo la elección correcta cuando la enumeración es una **entidad de negocio** — con sus atributos, su evolución, su gobernanza. El SQL Domain es el complemento ideal cuando la enumeración es un **vínculo de esquema** — un dominio puro, sin atributos, reutilizado en muchas columnas.

---

## Qué llega con la 26ai: las Assertions

Oracle 26ai (anunciada como próxima major release) trae — entre otras cosas — el soporte formal a las **`ASSERTION`** [3]: un constructo SQL estándar, presente sobre el papel desde hace décadas y nunca verdaderamente implementado por ningún DBMS mainstream, que permite expresar vínculos **cross-tabla**. Vínculos que hoy hay que codificar como trigger o como check aplicativo, con todos los riesgos del caso (trigger que se olvidan, transacciones que bypassan el vínculo, race condition con isolation level relajados).

Ejemplo posible:

```sql
CREATE ASSERTION al_menos_uno_activo CHECK (
  (SELECT COUNT(*) FROM estados_transaccion WHERE activo = 'Y') >= 1
);
```

La idea es que el motor del database garantice este vínculo **a nivel transaccional** — nada de trigger, nada de código aplicativo, validación centralizada. Para las enumeraciones gestionadas con lookup table, las `ASSERTION` abren un escenario nuevo: la integridad de toda la taxonomía (no solo de la columna individual) se vuelve expresable en DDL.

Es material que desarrollaremos cuando la 26ai esté disponible en test, en workloads reales. Por ahora, vale la pena saberla en camino y prepararse — el diseño de una taxonomía de estados hoy ya puede tener en cuenta dónde los vínculos cross-tabla vivirán mejor mañana.

---

## La pregunta que me llevo de la miniserie

Tres databases, tres filosofías, tres caminos — y una pregunta que sigue siendo válida en todas partes: **¿cuán estable es tu conjunto de valores?**

- Si es verdaderamente estable y local → `CHECK` (y en Oracle 23ai+ → `DOMAIN`).
- Si tiene atributos propios y una gobernanza → lookup table, en cualquier DB.
- Si es una evolución frecuente de valores "anagráficos" → lookup table, siempre.

El resto son detalles de sintaxis y de motor. Lo que cuenta — y lo que he aprendido en tres décadas de schema design, en clientes que iban de la compañía aseguradora multi-país al banco comercial italiano — es que **la rigidez de un esquema se paga en la evolución, y la flexibilidad se paga en la integridad**. La elección es siempre dónde quieres pagar el precio. Oracle 23ai, por fin, te da otro punto donde pagarlo — más conveniente, en muchos casos, que antes.

---

## Fuentes oficiales

1. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
2. MySQL 8.0 Reference Manual — [CHECK Constraints (8.0.16+)](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
3. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glosario

- **[SQL Domain](/es/glossary/oracle-sql-domain/)** — Constructo introducido en Oracle 23ai que permite definir un tipo base + vínculos + default + annotations como objeto del diccionario de datos, reutilizable en muchas columnas. Equivalente conceptual del `DOMAIN` de PostgreSQL, pero más rico en features de metadatos.
- **[CHECK constraint](/es/glossary/check-constraint/)** — Vínculo SQL que limita los valores admisibles en una columna o una fila mediante una condición booleana. Validado por el motor del database en el momento de INSERT o UPDATE.
- **[Lookup table](/es/glossary/lookup-table/)** — Tabla auxiliar que contiene el conjunto de valores admitidos para una columna de tipología, referenciada vía foreign key desde las tablas "principales". Permite evolución runtime del conjunto de valores sin modificaciones al esquema.
- **[ALTER DOMAIN](/es/glossary/oracle-alter-domain/)** — Comando Oracle 23ai+ que modifica el vínculo de un `SQL DOMAIN` propagando el cambio a todas las columnas que usan el dominio. Sustituye múltiples `ALTER TABLE` con una única operación.
- **[ASSERTION](/es/glossary/sql-assertion/)** — Constructo SQL estándar (todavía no implementado por casi ningún DBMS mainstream) para expresar vínculos cross-tabla validados a nivel transaccional. Anunciado en Oracle 26ai.
