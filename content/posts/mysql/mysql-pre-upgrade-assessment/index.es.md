---
title: "Antes de actualizar MySQL: las cifras que el cliente te pide y cómo encontrarlas de verdad"
description: "Cuatro servidores MySQL 8.0 en producción, un responsable de infraestructura que planifica la ventana de mantenimiento y cuatro preguntas directas: cuánto pesan, cuánto crecen, cuánto dura el backup, cuánto dura el restore. Cómo responder con números medidos en lugar de estimaciones a ojo."
date: "2026-05-05T08:03:00+01:00"
draft: false
translationKey: "mysql_pre_upgrade_assessment"
tags: ["mysql", "upgrade", "backup", "restore", "assessment", "information-schema", "mysqldump", "mydumper", "xtrabackup"]
categories: ["MySQL"]
image: "mysql-pre-upgrade-assessment.cover.jpg"
---

El correo del responsable de infraestructura llegó un lunes por la mañana, tres líneas secas. *"Hola, para el viernes necesito cuatro números para planificar la ventana de mantenimiento en los MySQL: cuánto pesan hoy, cuánto crecen al mes, cuánto tarda un backup completo, cuánto tardamos en reconstruirlos desde cero si algo sale mal. Gracias."*

Escenario clásico en una dirección IT de una Administración Pública italiana. Cuatro servidores MySQL 8.0 que soportan aplicaciones internas y un portal de usuarios, con versiones ligeramente desalineadas (8.0.32, 8.0.33, 8.0.34) porque se han parcheado en momentos distintos. Actualización de infraestructura prevista: nuevos hosts, sistema operativo actualizado, misma versión major de MySQL, con ventana de mantenimiento nocturna de seis horas.

El PM no quería un assessment académico. Quería cuatro cifras reales para poner en el plan de rollback. Y la tentación, cuando hay prisa, es responder a ojo: *"Serán unos 300 GB, el backup dura un par de horas, el restore quizás tres."* Números plausibles, incluso correctos tal vez, pero no medidos — y si te equivocas en la estimación del restore por un factor dos, la ventana no basta y el cutover se cae.

Me tomé media jornada. Este es el método que usé.

## 📏 1. Cuánto pesan de verdad — `information_schema`

La primera cifra es la más fácil de encontrar y la más engañosa de interpretar. En MySQL 8.0 el {{< glossary term="information-schema" >}}`information_schema`{{< /glossary >}} expone todo lo necesario, pero hay que saber qué preguntar.

```sql
-- Tamaño total por esquema (datos + índices)
SELECT
    table_schema                            AS schema_name,
    ROUND(SUM(data_length)  / 1024 / 1024 / 1024, 2) AS data_gb,
    ROUND(SUM(index_length) / 1024 / 1024 / 1024, 2) AS index_gb,
    ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) AS total_gb,
    COUNT(*)                                AS num_tables
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema')
GROUP BY table_schema
ORDER BY total_gb DESC;
```

Resultado típico en uno de los cuatro servidores:

| schema_name           | data_gb | index_gb | total_gb | num_tables |
|-----------------------|--------:|---------:|---------:|-----------:|
| portal_usuarios       |   58,34 |    21,07 |    79,41 |        142 |
| gestion_expedientes   |   31,12 |    14,88 |    46,00 |         97 |
| audit_log             |   28,45 |     9,20 |    37,65 |         12 |
| maestro_compartido    |    4,18 |     1,32 |     5,50 |         24 |
| *(otros esquemas)*    |    2,70 |     0,90 |     3,60 |         38 |
| **Total servidor**    |**124,79**|**47,37**|**172,16**|       313 |

Parece un dato cerrado, pero no lo es. Dos cosas importantes:

- **`data_length` e `index_length` son estimaciones** que InnoDB actualiza periódicamente y que dependen del último `ANALYZE TABLE`. En tablas muy volátiles pueden subestimar un 10-15%. Para datos críticos conviene contrastar con el tamaño físico de los ficheros `.ibd` en el datadir (`du -sh /var/lib/mysql/portal_usuarios/*.ibd`).
- **El total del servidor no es el tamaño del backup.** El fichero de dump (lógico) es más compacto porque no replica la fragmentación de InnoDB, pero contiene `INSERT`s textuales que pesan más que los datos binarios. En la práctica, el dump sin comprimir pesa el 70-90% de `data_length + index_length`. Con `gzip` estándar se baja al 15-25%, con `zstd -3` alrededor del 18-28% pero mucho más rápido.

Repitiendo la consulta en los cuatro servidores, el sizing total que llevé al PM fue:

| Servidor  | MySQL  | Esquemas | Total data + index | Ficheros .ibd en disco |
|-----------|:------:|---------:|-------------------:|-----------------------:|
| mysql-01  | 8.0.34 |        7 |           172,2 GB |                181 GB  |
| mysql-02  | 8.0.33 |        5 |            94,7 GB |                 98 GB  |
| mysql-03  | 8.0.32 |        9 |           218,5 GB |                229 GB  |
| mysql-04  | 8.0.34 |        4 |            46,1 GB |                 49 GB  |
| **Total** |        |       25 |         **531,5 GB** |           **557 GB** |

El gap entre "data + index" y "ficheros físicos" es el coste de la fragmentación y del tablespace `ibtmp1`. Merece la pena señalárselo al PM porque en el nuevo entorno se puede planificar un `OPTIMIZE TABLE` post-migración que recupera ese 5-6% de espacio.

## 📈 2. Cuánto crecen — snapshots periódicos y lectura del binary log

La cifra del crecimiento es más delicada. El PM pregunta "cuánto al mes", pero la respuesta útil es: *cuánto prevees que crezca en los próximos tres a seis meses, es decir, hasta el próximo assessment?* Hay dos enfoques, ambos válidos, que yo uso juntos.

**Enfoque 1 — snapshots periódicos.** Si dispones del histórico del monitoreo (Prometheus + `mysqld_exporter`, Zabbix, o incluso solo la carpeta de los backups historizados), puedes reconstruir la curva de tamaños. Si no tienes nada, empieza ya: un cron semanal que ejecuta la consulta anterior y escribe el resultado en una tabla `ops.sizing_history` — después de 6-8 semanas tienes un dato sólido.

```sql
-- Tabla de historización (ejecutar una sola vez)
CREATE TABLE ops.sizing_history (
    captured_at   TIMESTAMP NOT NULL,
    server_name   VARCHAR(50) NOT NULL,
    schema_name   VARCHAR(64) NOT NULL,
    data_bytes    BIGINT,
    index_bytes   BIGINT,
    num_tables    INT,
    PRIMARY KEY (captured_at, server_name, schema_name)
);

-- Snapshot semanal vía cron
INSERT INTO ops.sizing_history (captured_at, server_name, schema_name, data_bytes, index_bytes, num_tables)
SELECT
    NOW(),
    @@hostname,
    table_schema,
    SUM(data_length),
    SUM(index_length),
    COUNT(*)
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema', 'ops')
GROUP BY table_schema;
```

**Enfoque 2 — estimación a partir del {{< glossary term="binary-log" >}}binary log{{< /glossary >}}.** Este es el truco que mucha gente no usa. El binlog registra cada escritura, y su tamaño diario es un proxy excelente de la tasa de crecimiento de los datos (netos de updates y deletes, que generan tráfico pero no crecimiento neto). Con `expire_logs_days=7` tienes una semana de histórico lista para leer.

```bash
# Volumen diario del binlog (últimos 7 días)
ls -la /var/lib/mysql/binlog.* | awk '{print substr($6" "$7,1,6), $5}' | \
    sort | awk '{a[$1]+=$2} END {for (k in a) printf "%s  %.2f GB\n", k, a[k]/1024/1024/1024}'
```

Resultado típico en uno de los servidores:

```
Abr 14   3,87 GB
Abr 15   4,12 GB
Abr 16   3,95 GB
Abr 17   4,44 GB
Abr 18   2,18 GB   # sábado
Abr 19   1,02 GB   # domingo
Abr 20   3,78 GB
```

Media entre semana ~4 GB/día de tráfico de escritura. La tasa de crecimiento neto del tablespace es típicamente entre el 20% y el 40% del volumen del binlog, según el mix de insert/update/delete. En nuestro caso, cruzando con los pocos snapshots disponibles, llegamos a una estimación de **+8-12 GB al mes por servidor**, con picos en `mysql-03` (el del portal de usuarios, más dinámico).

## 💾 3. Cuánto dura el backup — `mysqldump`, `mydumper`, `xtrabackup`

Aquí el PM espera un único número. La respuesta honesta es: depende de qué herramienta uses, y los tiempos pueden diferir en un orden de magnitud.

En el mismo servidor (`mysql-03`, 218 GB de data + índices, tablas InnoDB con algún MyISAM residual que nadie ha tocado desde 2014), medí empíricamente cuatro estrategias.

**`{{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}}` (lógico, single-threaded):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob \
    --all-databases > /backup/mysql-03-full.sql
```

Resultado: 2 horas 47 minutos. Fichero SQL sin comprimir: 189 GB. Con pipe en tiempo real a `gzip` (`| gzip -3 > ...gz`): 3 horas 22 minutos, fichero comprimido 38 GB.

**`mysqldump` + `zstd` (mi favorito para servidores PA donde el tiempo de CPU importa menos que la ventana):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob --all-databases | \
    zstd -3 -T4 > /backup/mysql-03-full.sql.zst
```

Resultado: 2 horas 58 minutos, fichero comprimido 42 GB. Ligeramente mayor que gzip pero **aproximadamente el doble de rápido** en descompresión al restore — que es el momento en que la velocidad realmente importa.

**`{{< glossary term="mydumper" >}}mydumper{{< /glossary >}}` (lógico, paralelo):**

```bash
time mydumper --host=localhost --user=backup --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --compress --rows=500000 \
    --outputdir=/backup/mysql-03-mydumper \
    --logfile=/backup/mysql-03-mydumper.log
```

Resultado: 47 minutos. Output: directorio con 312 ficheros comprimidos, total 41 GB. Casi 4x más rápido que `mysqldump` gracias al paralelismo a nivel de chunk de tabla.

**`xtrabackup` (físico, hot backup):**

```bash
time xtrabackup --backup --target-dir=/backup/mysql-03-xtra \
    --user=backup --password=*** --parallel=4 --compress --compress-threads=4
```

Resultado: 22 minutos. Output: 179 GB sin comprimir / 48 GB comprimidos. Es el más rápido porque copia los ficheros InnoDB a nivel físico en lugar de regenerar los `INSERT`, pero tiene una restricción importante: **las tablas MyISAM residuales se bloquean** durante su copia. Por suerte en `mysql-03` eran residuales y solo leídas por un batch nocturno, así que no impacta.

Resumen que presenté al PM:

| Herramienta             | Tiempo backup | Tamaño output | Notas                                             |
|-------------------------|--------------:|--------------:|---------------------------------------------------|
| `mysqldump` + gzip      | 3h 22m        | 38 GB         | baseline, single-thread, disponible en todos lados |
| `mysqldump` + zstd      | 2h 58m        | 42 GB         | más rápido en restore                              |
| `mydumper` + compress   | 47m           | 41 GB         | paralelo, excelente compromiso tiempo/espacio      |
| `xtrabackup` + compress | 22m           | 48 GB         | físico, el más rápido, restricciones en MyISAM    |

En el assessment propuse estandarizar en **`mydumper` para el backup periódico** (diario, poco espacio en disco, restore flexible por esquema) y **`xtrabackup` para el snapshot pre-upgrade** (muy rápido, ideal para la ventana de mantenimiento estrecha).

## ⏱️ 4. Cuánto dura el restore — la cifra que el PM se olvida de preguntar

El restore es donde fracasan los assessments mal hechos. Un backup puede tardar 47 minutos, pero reconstruir el mismo dataset puede tardar horas — y en la ventana de mantenimiento, eso es lo que cuenta.

De nuevo en `mysql-03`, medición empírica de cuánto tarda en reconstruir la base de datos desde cero usando los backups anteriores, en un host gemelo (misma CPU, mismo almacenamiento NVMe):

**Desde `mysqldump.sql.gz`:**

```bash
time gunzip -c /backup/mysql-03-full.sql.gz | \
    mysql --default-character-set=utf8mb4
```

Resultado: **5 horas 12 minutos**. Lento porque el restore lógico regenera cada fila con `INSERT`s individuales, actualiza los índices de forma transaccional y no puede paralelizar sobre una única tabla.

**Desde `mysqldump.sql.zst`:**

```bash
time zstd -dc /backup/mysql-03-full.sql.zst | \
    mysql --default-character-set=utf8mb4
```

Resultado: **4 horas 38 minutos**. Aquí se ve la ventaja de la descompresión zstd (aproximadamente 2x más rápida que gzip), que es el único elemento que difiere del test anterior.

**Desde `mydumper` con `myloader`:**

```bash
time myloader --host=localhost --user=root --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --directory=/backup/mysql-03-mydumper \
    --disable-redo-log --overwrite-tables
```

Resultado: **1 hora 52 minutos**. El flag `--disable-redo-log` (MySQL 8.0.21+) es el verdadero game-changer: salta la generación del {{< glossary term="redo-log-mysql" >}}redo log{{< /glossary >}} durante la carga inicial, reduciendo el overhead de I/O. Usar SOLO en una instancia vacía durante el import, nunca en producción.

**Desde `xtrabackup`:**

```bash
time xtrabackup --decompress --target-dir=/backup/mysql-03-xtra --parallel=4
time xtrabackup --prepare --target-dir=/backup/mysql-03-xtra
# luego rsync de los ficheros al nuevo datadir + arranque mysqld
```

Resultado: **34 minutos** (decompress) + **12 minutos** (prepare) + **6 minutos** (copia + restart) = **52 minutos totales**. Restore físico: copia binaria + crash recovery, sin SQL regenerado. Es la única opción que se acerca al tiempo del backup mismo.

Resumen de restore:

| Estrategia             | Tiempo restore | Notas                                                   |
|------------------------|---------------:|---------------------------------------------------------|
| `mysqldump` + gzip     | 5h 12m         | evitar para datasets > 50 GB                            |
| `mysqldump` + zstd     | 4h 38m         | solo si no hay alternativas                             |
| `mydumper` + myloader  | 1h 52m         | con `--disable-redo-log`, restore lógico rápido         |
| `xtrabackup`           | 52m            | físico, única opción compatible con ventanas estrechas  |

## 📋 5. La plantilla de respuesta al PM

Tras las mediciones en los cuatro servidores, consolidé todo en una única tabla, porque lo que el PM necesita es una página para adjuntar al plan de cutover, no treinta diapositivas.

| Servidor  | Tamaño actual | Crecimiento estimado | Backup (`xtrabackup`) | Restore (`xtrabackup`) | Restore peor caso (`mysqldump+gz`) |
|-----------|--------------:|---------------------:|----------------------:|-----------------------:|-----------------------------------:|
| mysql-01  |      172 GB   | +8 GB/mes            |               18 min  |                45 min  |                         4h 10m     |
| mysql-02  |       95 GB   | +3 GB/mes            |               11 min  |                28 min  |                         2h 25m     |
| mysql-03  |      219 GB   | +12 GB/mes           |               22 min  |                52 min  |                         5h 12m     |
| mysql-04  |       46 GB   | +2 GB/mes            |                6 min  |                15 min  |                         1h 20m     |
| **Total** |  **532 GB**   | **+25 GB/mes**       |          **57 min**   |         **2h 20m**     |                   **13h 07m**      |

Sobre la base de esta tabla, la ventana de mantenimiento de seis horas es **compatible con un rollback basado en `xtrabackup`** (snapshot 57 min + restore 2h 20m = 3h 17m, con margen de 2h 43m para debug y verificaciones), pero **incompatible con un rollback basado en `mysqldump`** (más de 13 horas). Decisión operativa: `xtrabackup` como estrategia de rollback principal, `mydumper` como fallback para restores selectivos por esquema si surgen problemas puntuales durante el cutover.

El PM me pidió cuatro números. Le di veinticuatro. Pero son veinticuatro números medidos — no estimaciones a ojo — y la diferencia está toda ahí.

## Lo que aprendí

Un pre-upgrade assessment no es un documento técnico, es una herramienta de gobernanza del riesgo. El cliente que pregunta "cuánto dura el backup" en realidad está preguntando *"si todo sale mal en la ventana de mantenimiento, ¿llegamos a levantar los servicios antes de las 6 de la mañana?"*. Si tu respuesta es "unas tres horas, creo", esa pregunta sigue sin respuesta y el riesgo no se ha medido.

La parte técnica — las consultas, las herramientas, las mediciones — es la parte fácil. La parte difícil es hacer que las cifras medidas acaben en el plan de cutover, que el PM las lea, que el equipo ops las use para calibrar la ventana. En nuestro caso el PM quiso añadir una diapositiva más en la reunión con el vendor del nuevo storage: *"mirad, estas son las cifras de referencia; si vuestro array no aguanta estos throughputs de restore, el plan no funciona"*. Y eso es exactamente lo que debería hacer un buen PM.

Al final el upgrade pasó en cuatro horas, no seis. Sin rollback. El cliente nos dio las gracias no por la ventana corta, sino por el hecho de que habían **sabido siempre qué pasaría si algo salía mal**. Que es el verdadero objetivo de un pre-upgrade assessment bien hecho.

------------------------------------------------------------------------

## Glosario

**[information_schema](/es/glossary/information-schema/)** — Esquema de sistema de MySQL (solo lectura) que expone metadatos sobre bases de datos, tablas, índices, usuarios y estado del servidor. Punto de partida para cualquier assessment, sizing o análisis estructural.

**[xtrabackup](/es/glossary/xtrabackup/)** — Herramienta de backup físico en caliente para MySQL/MariaDB desarrollada por Percona. Copia directamente los ficheros InnoDB mientras la base de datos está en ejecución, gestionando las transacciones en curso mediante el redo log. Significativamente más rápida que los backups lógicos en datasets grandes.

**[Pre-upgrade assessment](/es/glossary/pre-upgrade-assessment/)** — Medición estructurada del tamaño, tasa de crecimiento, tiempos de backup y tiempos de restore de una base de datos antes de un upgrade. Sirve para dimensionar la ventana de mantenimiento y definir una estrategia de rollback realista.

**[mysqldump](/es/glossary/mysqldump/)** — Utilidad de backup lógico incluida en cada instalación de MySQL. Produce un fichero SQL secuencial con todas las instrucciones necesarias para recrear esquema y datos. Single-threaded, fiable pero lenta en bases de datos grandes.

**[mydumper](/es/glossary/mydumper/)** — Herramienta open source de backup lógico para MySQL/MariaDB con paralelismo real a nivel de chunk. Divide las tablas grandes en piezas y las exporta con múltiples threads, con restore paralelo mediante myloader.
