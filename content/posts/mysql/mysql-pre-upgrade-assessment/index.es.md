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
