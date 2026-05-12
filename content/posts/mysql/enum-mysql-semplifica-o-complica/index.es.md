---
title: "ENUM en MySQL: cuando te simplifica la vida y cuando te complica los días"
description: "Las tres vías para modelar una enumeración en MySQL — ENUM nativo, CHECK constraint, tabla de lookup. Contadas en pareja: dónde ENUM es la elección correcta, dónde se convierte en una losa. Con la historia de un sistema de seguimiento de envíos que atravesó ambas fases."
date: "2026-06-02T08:03:00+01:00"
draft: false
translationKey: "enum_mysql_semplifica_o_complica"
tags: ["enum", "data-modeling", "schema-design", "alter-table", "check-constraint"]
categories: ["mysql"]
image: "enum-mysql-semplifica-o-complica.cover.jpg"
---

Hay una escena que se repite en cada proyecto, antes o después. Estás diseñando una tabla nueva, tienes que modelar una columna `status` o `type` o `category`, y la pregunta llega siempre igual: "¿ENUM nativo, CHECK constraint o tabla de lookup?". Tres vías, tres filosofías, y tres resultados muy diferentes según cómo evolucione el sistema.

ENUM es una de esas features que caracterizan a MySQL. Pocos otros DBMS mainstream tienen un tipo enumerado nativo — PostgreSQL lo tiene, y Oracle llegó a algo similar solo con los SQL Domains de la 23ai. Durante años, en MySQL, la elección de usar ENUM ha sido prácticamente automática: pocas líneas de DDL, legible, rápido, sin JOIN. Funciona. Hasta que te giras seis años después y aquel `status` de la tabla se ha convertido en un campo minado.

---

## Las tres vías, en dos líneas cada una

Antes de entrar en materia, las tres opciones esquematizadas. Usaremos el ejemplo de una tabla `pedidos` con un estado que toma un conjunto cerrado de valores.

**ENUM nativo**:

```sql
CREATE TABLE pedidos (
  id     INT PRIMARY KEY,
  status ENUM('NUEVO','EN_PROCESO','ENVIADO','ENTREGADO') NOT NULL
);
```

El tipo `ENUM` es una cadena con restricción: admite solo los valores declarados. Internamente MySQL almacena un entero (1 o 2 bytes, según cuántos valores) que actúa como índice en la lista. Resultado: almacenamiento compacto, lectura legible.

**CHECK constraint**:

```sql
CREATE TABLE pedidos (
  id     INT PRIMARY KEY,
  status VARCHAR(20) NOT NULL,
  CONSTRAINT chk_status CHECK (status IN ('NUEVO','EN_PROCESO','ENVIADO','ENTREGADO'))
);
```

Enfoque SQL estándar. Más verboso pero más flexible (las condiciones de CHECK pueden ser arbitrariamente complejas). Ojo: antes de MySQL 8.0.16 los CHECK se parseaban y se ignoraban silenciosamente. Solo desde la 8.0.16 se aplican de verdad.

**Tabla de lookup con FK**:

```sql
CREATE TABLE estados_pedido (
  codigo      VARCHAR(20) PRIMARY KEY,
  etiqueta    VARCHAR(100) NOT NULL,
  activo      BOOLEAN DEFAULT TRUE
);

CREATE TABLE pedidos (
  id             INT PRIMARY KEY,
  status_codigo  VARCHAR(20) NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_codigo) REFERENCES estados_pedido(codigo)
);
```

La vía "puramente base de datos". Más tablas, más JOIN, pero también más flexibilidad: puedes añadir atributos (etiquetas localizadas, orden de visualización, flags activo/inactivo), modificar los valores sin tocar el schema de las tablas hijas, y gestionar todo en runtime.

---

## Cuándo ENUM es la elección correcta

ENUM brilla en un contexto específico: **conjunto de valores estable, semántica controlada por schema**. Cuando los dos ingredientes están, ENUM es la opción más limpia.

Casos típicos donde la estabilidad existe de verdad:

- **Días de la semana** (`'LUN','MAR','MIE','JUE','VIE','SAB','DOM'`) — no han cambiado nunca y no van a cambiar
- **Estados binarios o ternarios fijos** (`'ACTIVO','INACTIVO'` o `'PUBLICO','PRIVADO','BORRADOR'`)
- **Tipologías de transacción contable** donde el plan de cuentas está regulado por ley
- **Polaridad o signo** en medidas técnicas

En todos estos casos ENUM te da tres ventajas concretas:

1. **Almacenamiento compacto**: 1-2 bytes por fila contra los 4 de un INT que hace de FK. En una tabla con 200 millones de filas son 400-600 MB ahorrados. No es la razón principal para elegir ENUM, pero es un bonus
2. **Legibilidad en las queries**: `WHERE status = 'ENVIADO'` sin JOIN, sin alias de tablas adicionales. Cuando tienes que debuggear a las tres de la mañana, cuenta
3. **Sin migración extra**: la "tabla de lookup" ya es el propio schema. Sin seed de datos, sin sincronización, sin FK que gestionar en el deploy

En un sistema donde el dominio es realmente cerrado, ENUM quita complejidad. Una columna, una restricción declarada en el CREATE TABLE, fin.

---

## El caso concreto: un sistema de seguimiento de envíos

Hace un tiempo estaba trabajando con el equipo de IT de un gran operador postal italiano. Se trataba de diseñar el modelo de datos para un sistema de seguimiento de envíos: paquetes que entran en almacén, que se reciben, se clasifican, se entregan. El `status` era una columna central, presente en prácticamente cada query.

En la primera versión del sistema, los estados eran cinco, bien definidos por el negocio: `RECIBIDO`, `EN_ALMACEN`, `EN_ENTREGA`, `ENTREGADO`, `RECHAZADO`. ENUM, sin lugar a dudas, era la elección correcta:

```sql
ALTER TABLE envios
  ADD COLUMN status ENUM('RECIBIDO','EN_ALMACEN','EN_ENTREGA','ENTREGADO','RECHAZADO') 
  NOT NULL DEFAULT 'RECIBIDO';
```

Durante dos años en producción funcionó en silencio. Sin JOIN en los listados de entrega, sin tablas de estados que mantener, cada query con `WHERE status = '...'` se leía como una frase en prosa. El DBA dormía tranquilo.

Después empezaron los problemas.

---

## Los límites, contados con honestidad

La primera señal llegó como un email del product manager: hay que añadir un estado `RESERVADO`, para gestionar los envíos que el cliente ha anunciado pero aún no ha entregado al almacén. Operación aparentemente banal. Operación que requiere esto:

```sql
ALTER TABLE envios
  MODIFY COLUMN status 
  ENUM('RESERVADO','RECIBIDO','EN_ALMACEN','EN_ENTREGA','ENTREGADO','RECHAZADO') 
  NOT NULL DEFAULT 'RECIBIDO';
```

Parece una sola línea. Pero si quieres añadir `RESERVADO` **antes** de `RECIBIDO` (por coherencia semántica en la secuencia), MySQL tiene que reescribir la tabla. Toda ella. Sobre `envios` con ciento cincuenta millones de filas, en producción, incluso con `Online DDL` bien configurado, son bastantes horas de carga extra sobre el storage y sobre el replication lag. Añadirlo simplemente al final con `MODIFY COLUMN status ENUM(...,'RESERVADO')` habría sido más ligero — pero habría creado un conjunto de valores con un ordenamiento posicional absurdo: ¿`ENTREGADO` viene "antes" que `RESERVADO` en el sort? Técnicamente sí.

Aquí están, los límites de ENUM, contados sin compasión:

**Case-insensitive**. `'ACTIVO'` y `'activo'` son el mismo valor. Para quien viene de PostgreSQL puede ser una sorpresa amarga. En MySQL es un design choice explícito, pero conviene saberlo de antemano.

**Ordenamiento por posición de declaración**, no alfabético. Si la query hace `ORDER BY status`, el orden es el de cómo declaraste los valores en el `CREATE TABLE`. Bug sutil: añades `'RESERVADO'` al final para no rehacer la tabla, y de repente tu reporte ordenado por estado muestra `'RESERVADO'` después de `'RECHAZADO'`. Nadie se queja hasta que alguien se da cuenta.

**Modificaciones pesadas en tablas grandes**. Añadir un valor al final es ligero. Cambiar la posición, renombrar un valor, eliminar un valor — todo requiere un rebuild. Con Online DDL en MySQL 8 es menos doloroso que antes, pero no es gratis.

**Lock de tabla en algunos escenarios**. Las combinaciones de operaciones que requieren `ALGORITHM=COPY` siguen existiendo, y en tablas críticas hay que evaluarlas con cuidado.

En el sistema de seguimiento, seis años después, se habían añadido doce estados. Cada nuevo estado — porque un nuevo courier, porque un nuevo canal, porque una nueva política de devolución — era un ALTER nocturno con el DBA de pie frente al monitor. ENUM había pasado de simplificar la vida a complicarla.

---

## Cuándo pasar a CHECK o a lookup

La pregunta se convierte en: ¿a partir de qué punto conviene dejar ENUM y tomar otra vía?

Las banderas rojas son tres:

1. **Los valores cambian a menudo**: si cada trimestre el negocio pide añadir, renombrar o desactivar un valor, el schema no debería ser la "tabla" de las enumeraciones. Una verdadera tabla de lookup gestionada desde un panel de admin es la vía
2. **Hacen falta atributos adicionales**: descripción localizada en 4 idiomas, etiqueta corta vs extendida, orden de visualización, flag activo/inactivo. Todo esto en ENUM no lo metes. Con lookup table, cada valor es una fila que puede tener cuantas columnas quieras
3. **Decenas de valores en crecimiento**: pasados los 20-30 valores, ENUM se vuelve difícil de leer y mantener en el `CREATE TABLE`. El `DDL` se convierte en una lista interminable

En estos casos `CHECK` constraint es un compromiso intermedio: más flexible que ENUM (renombrar un valor es solo un `ALTER CONSTRAINT`), menos estructurado que una verdadera lookup table. Va bien para conjuntos de 5-15 valores que se tocan de vez en cuando, pero sin necesidad de atributos.

En el caso del seguimiento de envíos, al final la reescritura fue hacia lookup table. Vale la pena decirlo: no porque ENUM fuera "equivocado" en la versión 1. Era correcto, seis años antes, para un dominio que era realmente pequeño y estable. Se volvió equivocado cuando el dominio cambió, y nadie lo había previsto. Que es exactamente lo que pasa en muchos proyectos reales.

---

## Lookup table bien hecha

Si decides ir por la vía lookup, vale la pena diseñarla de modo que te permita crecer en el tiempo. El patrón natural — el que vemos en sistemas maduros — separa dos roles que ENUM tenía mezclados: el **identificador** del valor y la **descripción** del valor.

```sql
CREATE TABLE estados_envio (
  id            SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  codigo        ENUM('RECIBIDO','EN_ALMACEN','EN_ENTREGA','ENTREGADO','RECHAZADO') NOT NULL UNIQUE,
  descripcion   VARCHAR(200) NOT NULL,
  orden         SMALLINT NOT NULL DEFAULT 0,
  activo        BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO estados_envio (codigo, descripcion, orden) VALUES
  ('RECIBIDO',    'Envío recibido en almacén',         10),
  ('EN_ALMACEN',  'A la espera de clasificación',      20),
  ('EN_ENTREGA',  'Asignado al courier',               30),
  ('ENTREGADO',   'Entregado al destinatario',         40),
  ('RECHAZADO',   'Rechazado por el destinatario',     50);

CREATE TABLE envios (
  id         INT PRIMARY KEY,
  estado_id  SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_estado FOREIGN KEY (estado_id) REFERENCES estados_envio(id)
);
```

¿Has notado la sorpresa? En la lookup, el campo `codigo` sigue siendo un **`ENUM`**. No un `VARCHAR(20)`, no una cadena libre. ENUM, el mismo que acabamos de criticar. Y es exactamente la elección correcta: todos los contras que vimos antes — el rebuild en modificación, el ordenamiento posicional, el efecto en tablas grandes — aquí simplemente *no duelen*. La lookup tiene 5, 20, como máximo 50 filas. Un rebuild sobre 50 filas es un parpadeo. La restricción "admite solo estos valores" la pagamos a coste cero, sin escribir un `CHECK` explícito.

Tres cosas interesantes emergen de este schema.

**La master lleva solo el id**, no el código. Dos bytes por fila (`SMALLINT`) en lugar de los 20+ de un `VARCHAR(20)`. En una tabla con 150 millones de filas son 2-3 GB de diferencia entre datos e índices, además de JOIN más rápidos gracias a la comparación entre enteros.

**El código y la descripción son atributos de la lookup, no clave**. Renombrar un estado — pasar de "Entregado" a "Entregado al destinatario" — es un `UPDATE` sobre una sola fila de la lookup. Sin migración, sin rebuild, sin `ALTER` sobre la master. El schema de las tablas hijas no se toca. Tener el `codigo` como clave natural parecía elegante hace cuatro años, pero la primera vez que el negocio pide cambiar el texto de una etiqueta entiendes por qué existía el id sustituto.

**Los atributos extra cuestan nada de añadir**: una columna `descripcion_corta` para los tracciados SMS, una columna `orden` para el sort visual en dashboards, una tabla relacionada para las traducciones multilingües. Todo esto era imposible con ENUM "puro", y es normal con una lookup table bien diseñada.

El precio a pagar es que las queries ad-hoc requieren un JOIN para leer el nombre del estado en claro:

```sql
SELECT e.id, ee.codigo
FROM envios e
JOIN estados_envio ee ON ee.id = e.estado_id
WHERE ee.codigo = 'EN_ENTREGA';
```

Más verboso que un `WHERE status = 'EN_ENTREGA'` sobre ENUM, pero es el precio de la flexibilidad. Y sobre los reportes más frecuentes el JOIN se optimiza con un índice compuesto y una `view` que encapsula la complejidad, dejando las queries aplicativas legibles.

### Añadir un valor y reordenar el ENUM

Veamos cómo se hacen las dos operaciones "delicadas" sobre este patrón. El negocio pide añadir el estado `RESERVADO`, para los envíos anunciados pero aún no recibidos.

**Caso 1 — añadir al final del ENUM, con `orden` lógico controlado por la columna**:

```sql
-- Extiende el ENUM añadiendo el valor al final (operación rápida)
ALTER TABLE estados_envio
  MODIFY COLUMN codigo 
    ENUM('RECIBIDO','EN_ALMACEN','EN_ENTREGA','ENTREGADO','RECHAZADO','RESERVADO') NOT NULL;

-- Inserta la nueva fila; el orden lógico es 5 (antes de RECIBIDO=10)
INSERT INTO estados_envio (codigo, descripcion, orden, activo) VALUES
  ('RESERVADO', 'Envío anunciado, aún no recibido', 5, TRUE);
```

Fíjate en la separación de responsabilidades: el **orden de declaración del ENUM** no corresponde necesariamente al **orden lógico** del estado en el workflow. Este último lo gestiona la columna `orden`, que es explícita y ordenable como queramos. El valor numérico interno del ENUM es un detalle de implementación que ignoramos.

**Caso 2 — reordenar realmente el ENUM** (si de verdad queremos que `RESERVADO` esté en primera posición también internamente):

```sql
ALTER TABLE estados_envio
  MODIFY COLUMN codigo 
    ENUM('RESERVADO','RECIBIDO','EN_ALMACEN','EN_ENTREGA','ENTREGADO','RECHAZADO') NOT NULL;
```

Sobre una tabla de 6 filas, MySQL rebuilda en milisegundos. Los `id` de las filas existentes se mantienen idénticos (la sequence de AUTO_INCREMENT no se toca con el rebuild), el valor ENUM se remapea internamente por el motor, y la integridad referencial desde la master `envios` queda intacta. La master no sabe nada de todo esto: sigue conteniendo `estado_id = 3` y a través de la FK resuelve siempre a la fila correcta de la lookup.

Este es el punto real: **los id estables de la lookup son el ancla de la integridad referencial**. Cualquier cosa que cambiemos en la lookup — reorden ENUM, renombre código, modificación descripción — la master sigue funcionando. Los 150 millones de filas no se tocan nunca.

ENUM, en este sitio, ha vuelto a ser la herramienta adecuada. La misma herramienta que era un problema en la master es una ventaja en la lookup. Cambia el contexto, cambia el juicio.

---

## La regla de oro

La síntesis que me llevo de esta historia, y que repito a los equipos cuando llega la pregunta "¿ENUM o lookup?", es simple:

> Si los valores no van a cambiar nunca, ENUM es la elección correcta. Si van a cambiar — aunque sea solo "de vez en cuando" — no ates el vocabulario al schema.

Eso es todo. Lo difícil no es escoger entre las tres vías. Lo difícil es entender con honestidad, al momento de la elección, en cuál de los dos mundos estás. Y eso, normalmente, lo entiendes mirando cómo ha cambiado el dominio en los últimos dos o tres años — no leyendo los requisitos del próximo sprint.

---

## La mini-serie cross-DB

Este es el primero de cuatro artículos sobre enumeraciones en los distintos DBMS. La pregunta "¿ENUM o lookup?" no es solo de MySQL — cada base de datos tiene su filosofía, y es interesante ver cómo la misma elección cambia de forma al pasar de un mundo a otro.

Próximas entregas:

- **PostgreSQL** — `CREATE TYPE ... AS ENUM`, `ALTER TYPE ADD VALUE`, y la sorpresa: en PostgreSQL ENUM es *case-sensitive*
- **Oracle** — `CHECK` constraint, los SQL Domains de la 23ai, y por qué Oracle llegó "tarde" a este tema
- **Oracle, deep-dive vertical** — cómo se modelaban las enumeraciones en 19c, qué cambia en 21c, 23ai y 26ai, hasta las nuevas Assertions

Misma pregunta, tres filosofías. Lo bueno está justamente en la comparación.

------------------------------------------------------------------------

## Glosario

**[ENUM (MySQL)](/es/glossary/mysql-enum/)** — Tipo de dato de MySQL que admite un conjunto predefinido de valores cadena, almacenado internamente como un índice numérico de 1-2 bytes. Una de las features características de MySQL.

**[CHECK constraint](/es/glossary/check-constraint/)** — Restricción SQL estándar que limita los valores admitidos en una columna mediante una expresión booleana. En MySQL se aplica realmente solo desde la versión 8.0.16.

**[Lookup table](/es/glossary/lookup-table/)** — Tabla de referencia conectada vía foreign key que almacena los valores válidos de una enumeración, con eventuales atributos descriptivos (etiqueta, orden, flag activo).

**[Online DDL](/es/glossary/mysql-online-ddl/)** — Mecanismo MySQL/InnoDB que permite ejecutar ALTER TABLE sin bloquear las escrituras concurrentes, con tres algoritmos (`INSTANT`, `INPLACE`, `COPY`) elegidos automáticamente según la operación.

**[Clave subrogada](/es/glossary/chiave-surrogata/)** — Identificador numérico generado por la base de datos (típicamente un `AUTO_INCREMENT`) distinto de la clave natural. En la lookup table es el ancla de la integridad referencial, porque se mantiene estable aunque cambien el código o la descripción.
