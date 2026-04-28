---
title: "Cuando un índice hace más mal que bien: limpiar PostgreSQL del despilfarro"
description: "La base de datos central de un Ministerio, una tabla con 15 índices de los cuales 8 nunca usados, un junior que quería entenderlo todo. La limpieza que volvió a poner las consultas en su sitio, contada como si fuera ayer."
date: "2026-05-26T08:03:00+01:00"
draft: false
translationKey: "postgresql_indici_quando_fanno_male"
tags: ["indexes", "b-tree", "gin", "gist", "performance", "tuning", "query-tuning"]
categories: ["postgresql"]
image: "postgresql-indici-quando-fanno-male.cover.jpg"
---

El otro día un compañero me escribió: "Tengo una tabla con doce índices, va lentísima. No lo entiendo." Le contesté con dos líneas, pero mientras releía me vino a la cabeza Marco. Hace ya unos años, trabajaba en la base de datos central de un Ministerio — no importa cuál, el patrón se ve en todas partes. Y Marco era el junior que me habían asignado.

Tenía dos años y medio de PostgreSQL a sus espaldas, sabía escribir consultas decentes, conocía `EXPLAIN`. Pero sobre todo tenía esa cualidad que en este oficio te lleva lejos: preguntaba. No por pereza — por querer saber. Reformulaba los conceptos en voz alta para fijarlos, tomaba apuntes, anticipaba la siguiente pregunta con cosas como "espera, entonces si hago X debería esperarme Y, ¿no?". El junior que cualquier senior querría tener al lado cuando se abre una tabla que da miedo.

Aquel día abrimos una.

## La tabla que daba miedo

Se llamaba `cittadini_servizi` (`ciudadanos_servicios`). No es el nombre real — pero el patrón sí lo es.

Ochenta millones de filas. Una columna `cittadino_id`, una columna `servizi_attivi` que era un array de códigos (un ciudadano podía tener varios servicios activos: registro civil, tributario, sanitario, escolar, cada uno con su código numérico), una geometría con la residencia, un booleano `attivo`, un par de fechas, algo de metadatos. Nada exótico.

Encima había **quince índices**.

Marco los contó despacio, recorriendo `\d cittadini_servizi`. "Quince. Un poco demasiados, ¿no?"

"Depende. ¿Se usan?"

"¿Cómo se sabe?"

Y ahí empezó.

## El diagnóstico en cinco minutos

PostgreSQL lleva la cuenta de cuántas veces se ha usado cada índice. La vista se llama `pg_stat_user_indexes`. Marco no la había abierto nunca.

```sql
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'cittadini_servizi'
ORDER BY idx_scan ASC;
```

La salida fue brutal. Ocho índices con `idx_scan = 0`. Nunca — usados — ni — una — vez.

Marco miró la pantalla. "¿Nunca? ¿Ni de casualidad?"

"Nunca. `idx_scan` arranca a cero cuando arranca el motor y crece cada vez que el planner elige ese índice. Si después de semanas en producción sigue a cero, es que el planner nunca lo ha considerado útil."

"Pues los quitamos y listo."

"Para. Antes hay que entender por qué están."

Esa frase de ahí — no borres nada antes de haber entendido por qué existe — es la regla de oro cuando aterrizas en un sistema que no construiste tú. Esos `CREATE INDEX` los escribió alguien. Quizá tenía un motivo. Quizá creía tenerlo. Quizá no lo tenía en absoluto. Vete tú a saber.

Marco asintió y abrió el git log del repo de los DDL.

## "Pero si ya hay 15 índices, ¿por qué va lenta?"

Pregunta correcta. Premisa equivocada.

Porque parte de la suposición de que "más índices = más rápido", que es uno de los mitos más persistentes de los primeros años de PostgreSQL. La realidad es que un índice solo sirve si el planner lo elige, y el planner solo elige los índices que son del **tipo correcto** para la consulta que está evaluando.

Abrí una de las consultas críticas, una de las que el monitoring marcaba como lentas:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT cittadino_id
FROM cittadini_servizi
WHERE servizi_attivi && ARRAY[42, 71]
  AND attivo = true;
```

El operador `&&` significa "intersección de arrays": dame los ciudadanos que tengan al menos uno de los servicios 42 o 71 activo. Una consulta que el negocio pedía a menudo, para campañas dirigidas.

Tiempo: **8.4 segundos**. Plan: `Seq Scan on cittadini_servizi`. Filter: los 80 millones de filas enteritos.

"¡Pero si había un índice sobre `servizi_attivi`!"

"¡Lo hay! Es un B-tree. Y el B-tree no sabe qué hacer con `&&`."

## Cuándo basta el B-tree — y cuándo no

El **B-tree** es el índice que el 90% de los desarrolladores conoce y usa. Es un árbol equilibrado que ordena los valores. Funciona estupendamente para igualdad (`WHERE col = 'x'`), para rangos (`WHERE col BETWEEN ... AND ...`), para ordenación (`ORDER BY col`), para `LIKE` con prefijo (`WHERE col LIKE 'ABC%'`).

No funciona en cambio sobre:
- Operadores de array (`&&`, `<@`, `@>`)
- Búsquedas de subcadena (`LIKE '%x%'`)
- Containment de JSONB (`@>`)
- Rangos geométricos (`&&` sobre geometrías, distancias, bounding box)

Para eso hacen falta otros tipos.

"Y nosotros tenemos el array de servicios bajo un B-tree."

"Exacto. Es como tener un archivo en papel ordenado por NIF y pedirle al archivero que te encuentre todos los expedientes que contengan una determinada palabra clave dentro. El orden no ayuda."

"Entonces hace falta otro tipo de índice."

"Hace falta GIN."

## GIN: el inverso del B-tree

GIN viene de *Generalized Inverted Index*. Inverso, porque en lugar de indexar las filas por el valor de la columna, indexa cada elemento dentro de la columna y mantiene una lista de filas que lo contienen.

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi);
```

`USING GIN` es la clave. PostgreSQL construye un mapping: para cada código de servicio, una lista de filas que lo tienen en el array. Cuando llega la consulta con `&&`, el índice cruza las listas de los dos valores buscados y devuelve la unión. Sin seq scan.

Misma consulta, después:

```
Bitmap Index Scan on idx_cittadini_servizi_attivi_gin
  ...
Execution Time: 240 ms
```

De 8400 a 240 milisegundos. Un factor 35.

Marco celebró por lo bajini. Luego: "Si es tan potente, ¿por qué no usarlo siempre?"

"Porque en escritura te sale caro. Cada `INSERT` o `UPDATE` sobre esa columna tiene que actualizar todos los postings donde aparece ese valor. Es el precio de encontrar las cosas rápido — y las tablas con mucho churn lo pagan caro."

"Entonces GIN sí, pero solo si la tabla es predominantemente de lectura."

"Exacto. Nuestra `cittadini_servizi` recibía cargas nocturnas y luego durante todo el día solo lecturas. Caso ideal."

## GiST: para cuando los datos tienen forma

La otra consulta crítica era sobre las geometrías. El Ministerio hacía análisis territoriales: "encuéntrame todos los ciudadanos con residencia a 5 km del punto X, en la provincia de Y, activos". Una consulta así, con un B-tree espacial falso (porque alguien había puesto uno, pero sobre esa columna no se podía usar), iba en nested loop y tardaba medio minuto.

GiST — *Generalized Search Tree* — es la familia de índices que gestiona datos con geometría, rangos, similitud. No ordena los valores de forma lineal, porque hay datos que no son ordenables linealmente (un punto en el plano no está "antes" o "después" de otro). En su lugar, indexa por *bounding boxes* jerárquicos.

"Pero, ¿por qué no un B-tree compuesto sobre `(latitud, longitud)`?"

Buena pregunta. Marco había dado en el punto correcto.

"Porque el B-tree compuesto ordena primero por latitud y luego por longitud. Si necesitas encontrar puntos dentro de un rectángulo `(lat1, lon1, lat2, lon2)`, el índice consigue usar la restricción de latitud — pero después, en cada fila que pasa el filtro lat, tiene que verificar también lon. Sobre 80 millones de filas se convierte en media exploración."

"¿Y GiST?"

"GiST organiza los puntos por regiones geográficas. Cuando buscas un rectángulo, descarta regiones enteras con una comparación de bounding box. Está hecho para ese tipo de consulta."

```sql
CREATE INDEX idx_cittadini_residenza_gist
ON cittadini_servizi USING GIST (residenza);
```

Misma consulta "encuentra todos a 5 km de X", de 28 segundos a 380 ms.

Marco tomaba apuntes rápidos. "Entonces: B-tree para ordenación e igualdad, GIN para containment de array y JSONB, GiST para geometría y rangos. ¿Algo más?"

"De momento basta. Existen BRIN, SP-GiST, hash, pero son casos más nicho. Cuando los necesites, te acordarás."

## Bonus: los índices parciales

Quedaba una última cosa antes de volver a la pregunta inicial (qué índices tirar). Los ciudadanos "activos" eran alrededor del 35% del total. Todo lo demás era histórico, expedientes cerrados, archivados. Las consultas operativas filtraban siempre por `attivo = true`.

"Entonces cada índice contiene un 65% de filas que no se buscan nunca."

"Exacto. Espacio desperdiciado y trabajo de VACUUM también. Solución: índice parcial."

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi)
WHERE attivo = true;
```

Ese `WHERE` lo cambia todo. El índice solo contiene las filas activas. Sobre los datos reales, el espacio ocupado se redujo a la mitad y la velocidad mejoró otro 15-20% porque el índice era más pequeño de recorrer.

"¿Y las consultas con `attivo = false`?"

"Van en seq scan, pero pasa una vez por semana para los informes del archivo. Allí el seq scan va perfectamente bien."

## La limpieza

A estas alturas teníamos:

- Entendido por qué 8 índices no se usaban (eran duplicados de otros, o B-trees sobre columnas donde el planner prefería un seq scan, o restos de consultas que ya no existían)
- Sustituido 2 B-trees inadecuados por un GIN y un GiST
- Convertido 2 índices "completos" en índices parciales

Resultado neto:

| Concepto | Antes | Después |
|----------|------:|--------:|
| Índices totales | 15 | 7 |
| Espacio índices | 42 GB | 18 GB |
| Tiempo medio consultas operativas | 4.1 s | 0.4 s |
| Tiempo INSERT batch nocturno | 38 min | 22 min |

Marco miró la tabla, después a mí. "O sea, hemos mejorado tanto la lectura como la escritura, simplemente quitando cosas."

"Y poniendo las tres correctas en el sitio correcto. Pero sí, sobre todo quitando. Cada índice es un coste. En cada DML. Para siempre."

## La frase que le repetí tres veces

Aquel día le dije lo mismo de tres formas distintas, porque quería que se la llevara con él:

> Cuando piensas en un índice que crear sobre una tabla, no pienses "uno más, total no hace daño". Un índice es un coste permanente sobre cada `INSERT`, `UPDATE`, `DELETE` — más disco, más WAL, más VACUUM, más contención. Lo creas solo si hace falta de verdad. Y si está y no hace falta, fuera.

Marco lo escribió en su cuaderno. Años después se convirtió en el senior de otro proyecto. Me llegó un mensaje un día: *"Me ha tocado una tabla con veintidós índices. Ocho a cero. Hice la limpieza. Pensé en ti."*

Esa es la mejor cosa que un junior te puede decir.

------------------------------------------------------------------------

## Glosario

**[B-tree](/es/glossary/b-tree/)** — La estructura de árbol equilibrado usada para la mayoría de los índices. Funciona estupendamente para igualdad, rangos y ordenación. No sabe gestionar arrays, subcadenas internas, geometrías.

**[GIN Index](/es/glossary/gin-index/)** — *Generalized Inverted Index*. Indexa elementos individuales dentro de valores compuestos (arrays, JSONB, full-text). Rápido en lectura para consultas de containment, lento en escritura sobre tablas con mucho churn.

**[GiST Index](/es/glossary/gist-index/)** — *Generalized Search Tree*. Indexa datos con estructura geométrica o de rangos usando bounding boxes jerárquicos. Imprescindible para geometrías, rangos temporales, similitud.

**[pg_stat_user_indexes](/es/glossary/pg-stat-user-indexes/)** — Vista de sistema PostgreSQL que registra cuántas veces se ha usado cada índice (`idx_scan`). La herramienta principal para identificar índices inútiles en producción.

**[Índice Parcial](/es/glossary/indice-parziale/)** — Índice que cubre solo un subconjunto de las filas de la tabla, definido con `WHERE` en el `CREATE INDEX`. Reduce espacio y tiempo de mantenimiento cuando las consultas filtran sistemáticamente sobre una condición.
