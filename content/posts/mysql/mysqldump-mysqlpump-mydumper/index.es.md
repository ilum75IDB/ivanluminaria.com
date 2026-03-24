---
title: "mysqldump vs mysqlpump vs mydumper: el backup que no te deja dormir"
description: "Una base de datos de 60 GB, un mysqldump que tardaba tres horas y bloqueaba las escrituras. Probé mysqlpump y mydumper en el mismo entorno, con tiempos reales de dump y restore. Esto es lo que encontré — y por qué elegir la herramienta de backup es una decisión arquitectónica, no operativa."
date: "2026-04-14T08:03:00+01:00"
draft: false
translationKey: "mysqldump_mysqlpump_mydumper"
tags: ["backup", "mysqldump", "mydumper", "restore", "mariadb"]
categories: ["mysql"]
image: "mysqldump-mysqlpump-mydumper.cover.jpg"
---

La llamada llegó un viernes por la tarde — porque estas cosas siempre pasan en viernes. El DBA de un cliente del sector logístico me escribe por Teams: "El backup de anoche tardó tres horas y media. Esta mañana los usuarios encontraron la aplicación lenta a las 8. ¿Podemos hablarlo?"

Podíamos hablarlo, sí. De hecho, deberíamos haberlo hablado hace tiempo.

El setup era un clásico: MySQL 8.0 sobre Rocky Linux, base de datos de unos 60 GB, un gestional con unas treinta tablas InnoDB de las cuales cuatro o cinco eran realmente grandes — la tabla de pedidos, la de movimientos de almacén, la historización de tracking. El backup se hacía cada noche con un mysqldump lanzado por cron a las 2:00. Había funcionado durante años. El problema es que la base de datos mientras tanto había crecido.

Tres horas de mysqldump significan tres horas de `--lock-all-tables` — o en el mejor caso tres horas de transacción consistente con `--single-transaction` que de todas formas mantiene un snapshot de InnoDB abierto todo el tiempo. Y cuando el dump termina a las 5:00 y el restore de prueba (que nadie hacía) habría requerido otras cuatro horas, la ventana de backup simplemente ya no existe.

---

## El problema real: mysqldump es single-threaded

Lo primero que hay que entender sobre {{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}} es que hace una sola cosa a la vez. Una tabla tras otra, una fila tras otra, un archivo SQL de salida. Punto.

No hay paralelismo. No hay compresión nativa. No hay forma de decir "usa 4 threads y termina antes". Es un programa nacido en el año 2000 — literalmente — y su diseño refleja una época en la que 60 GB eran una cantidad impensable para una base de datos MySQL.

El dump del cliente producía un archivo SQL de 45 GB. Un único archivo monolítico que contenía todas las tablas, todos los stored procedures, todos los triggers. Para hacer un restore bastaba con alimentar ese archivo a `mysql` — pero tardaba cuatro horas, porque el restore también es secuencial.

```bash
# El backup clásico — funciona, pero escala fatal
mysqldump --single-transaction --routines --triggers --events \
  --all-databases > /backup/full_backup.sql
```

Lo paradójico es que mysqldump tiene una ventaja enorme: está en todas partes. Viene incluido en cada instalación de MySQL, no requiere nada adicional, produce SQL legible. Si necesitas mover una tablita de 500 filas entre dos entornos, es perfecto. Si necesitas hacer backup de una base de datos de 60 GB en producción — no.

Le expliqué al cliente que teníamos dos alternativas: mysqlpump y mydumper. Dos herramientas con filosofías diferentes, limitaciones diferentes, y rendimiento que sobre el papel promete mucho pero que en la realidad hay que probar.

---

## mysqlpump: la promesa incumplida de Oracle

{{< glossary term="mysqlpump" >}}mysqlpump{{< /glossary >}} llegó con MySQL 5.7 como la evolución oficial de mysqldump. La promesa era clara: paralelismo en el dump, compresión nativa, gestión de usuarios. Sobre el papel, todo lo que le faltaba a mysqldump.

Lo configuré — en realidad ya estaba allí porque viene incluido en la distribución de MySQL — y lancé una primera prueba sobre la base de datos del cliente:

```bash
mysqlpump --single-transaction --default-parallelism=4 \
  --compress-output=zlib --all-databases > /backup/full_backup.sql.zlib
```

¿El resultado? 48 minutos para el dump, contra las tres horas y media de mysqldump. Una mejora importante. Pero luego miré con más detalle.

El paralelismo de mysqlpump funciona a nivel de tabla: si tienes 4 threads, hace dump de 4 tablas simultáneamente. El problema es que cuando tienes una tabla de 30 GB y tres tablas de 50 MB, tres threads terminan en treinta segundos y luego un solo thread se arrastra durante cuarenta minutos con la tabla grande. El paralelismo es tan efectivo como equilibrada sea tu base de datos — y las bases de datos de producción nunca están equilibradas.

Pero el problema más serio es otro. mysqlpump con `--single-transaction` no garantiza un backup consistente entre tablas diferentes. Lo dice la propia documentación, en una nota que la mayoría de la gente no lee:

> *mysqlpump does not guarantee consistency of the dumped data across tables when using parallelism. Tables dumped in different threads may be at different points in time.*

Relean esa frase. Si usas el paralelismo — que es la única razón para usar mysqlpump — pierdes la garantía de consistencia entre tablas. En una base de datos relacional. Donde las tablas tienen foreign keys entre sí.

Para un entorno de desarrollo o test, puede servir. ¿Para un backup de producción del que podrías tener que hacer restore en caso de desastre? No. Absolutamente no.

Otra nota: Oracle declaró mysqlpump **deprecado en MySQL 8.0.34** y lo eliminó en MySQL 8.4. Eso dice mucho sobre la confianza que Oracle misma tenía en esta herramienta.

---

## mydumper: la herramienta que cumple lo que promete

{{< glossary term="mydumper" >}}mydumper{{< /glossary >}} es un proyecto open source nacido en 2009 de la comunidad MySQL — en particular del trabajo de Domas Mituzas, Andrew Hutchings y luego mantenido por Max Bubenick. No es una herramienta de Oracle. No viene incluido en la distribución de MySQL. Hay que instalarlo por separado. Pero hace algo que ni mysqldump ni mysqlpump hacen: paralelismo real, a nivel de chunk dentro de la misma tabla.

```bash
# Instalación en Rocky Linux / CentOS
yum install https://github.com/mydumper/mydumper/releases/download/v0.16.9-1/mydumper-0.16.9-1.el8.x86_64.rpm
```

mydumper toma una tabla grande, la divide en chunks (por defecto basándose en la primary key) y asigna cada chunk a un thread diferente. Así que esa tabla de 30 GB no la exporta un solo thread — se rompe en pedazos y se descarga en paralelo.

El dump que lancé sobre la base de datos del cliente:

```bash
mydumper --threads 8 --compress --trx-consistency-only \
  --outputdir /backup/mydumper_full/ \
  --logfile /var/log/mydumper.log
```

22 minutos. Contra las tres horas y media de mysqldump y los 48 minutos de mysqlpump.

Pero la verdadera ventaja de mydumper no es solo la velocidad del dump — es la velocidad del restore. mydumper produce un archivo por cada tabla (o por cada chunk), y su compañero `myloader` los carga en paralelo:

```bash
myloader --threads 8 --directory /backup/mydumper_full/ \
  --overwrite-tables --compress-protocol
```

El restore que con mysqldump habría requerido cuatro horas, con myloader requirió una hora y veinte minutos. En una base de datos de 60 GB. Con ocho threads.

---

## Los números: pruebas en entorno real

Hice las pruebas en el mismo servidor del cliente — no en un entorno de laboratorio con discos NVMe y RAM infinita. Servidor real, carga real, discos SATA en RAID 10.

| Operación | mysqldump | mysqlpump (4 threads) | mydumper (8 threads) |
|-----------|-----------|----------------------|---------------------|
| **Dump** | 3h 25min | 48 min | 22 min |
| **Tamaño output** | 45 GB (SQL) | 12 GB (comprimido) | 9.8 GB (comprimido) |
| **Restore** | ~4h (estimado) | ~3h (estimado) | 1h 20min |
| **Consistencia entre tablas** | Sí | No (con paralelismo) | Sí |
| **Bloqueo escrituras** | No* | No* | No* |

*Con `--single-transaction` sobre InnoDB.

Algunas notas sobre los números:
- El restore de mysqldump y mysqlpump está estimado porque no hice la prueba completa en producción — demasiado arriesgado. Los tiempos se calcularon a partir de pruebas parciales sobre un subconjunto de tablas
- La compresión de mydumper (`--compress`) usa zstd por defecto, que comprime mejor y más rápido que zlib
- El restore con myloader desactiva los checks de foreign keys y reconstruye los índices al final, lo que acelera enormemente la carga

---

## Las opciones críticas que no debes olvidar

Sea cual sea la herramienta que elijas, hay opciones que debes incluir siempre. Las he visto olvidadas demasiadas veces, con consecuencias que van de la molestia al desastre.

### --single-transaction

Obligatorio en InnoDB. Sin esta opción, el dump adquiere locks que bloquean las escrituras. Con `--single-transaction`, el dump usa una transacción con isolation level REPEATABLE READ para obtener un snapshot consistente sin bloquear a nadie.

Atención: solo funciona en tablas InnoDB. Si tienes tablas MyISAM (y sí, en 2026 todavía las encuentro), esas se bloquearán de todos modos.

### --routines --triggers --events

Los stored procedures, triggers y scheduled events no se incluyen en el dump por defecto. Tienes que pedirlos explícitamente. He visto restores que "funcionaban perfectamente" — excepto que faltaban todos los triggers de auditoría y la aplicación escribía datos sin trazabilidad.

### --set-gtid-purged (MySQL) o --gtid (mydumper)

Si usas replicación basada en GTID — y deberías — el dump tiene que gestionar los GTID correctamente. Si no lo hace, el restore en una réplica genera conflictos de replicación que te volverán loco.

### Verificación del restore

Esto no es una opción — es una práctica. El backup que no verificas es el backup que no tienes. Tengo un cliente que hacía backups cada noche durante tres años. El día que tuvo que hacer un restore, descubrió que el archivo estaba corrupto desde la semana anterior. Tres años de backups, cero pruebas de restore.

```bash
# Verificación mínima con mydumper: restore en instancia de test
myloader --threads 4 --directory /backup/mydumper_full/ \
  --host test-mysql-server --overwrite-tables

# Contar filas de las tablas principales
mysql -h test-mysql-server -e "
  SELECT table_name, table_rows
  FROM information_schema.tables
  WHERE table_schema = 'production_db'
  ORDER BY table_rows DESC LIMIT 10;"
```

---

## Cuándo usar qué

Después de treinta años de bases de datos, mi regla es simple:

**mysqldump** — para bases de datos de menos de 5 GB, migraciones puntuales, dumps de tablas individuales, entornos de desarrollo donde la velocidad no es crítica. Es la navaja suiza: hace todo, lentamente, pero lo hace.

**mysqlpump** — ya no lo recomiendo. Deprecado por Oracle, consistencia no garantizada con el paralelismo, y mydumper hace todo lo que mysqlpump prometía pero mejor. Si lo estás usando, planifica la migración a mydumper.

**mydumper/myloader** — para cualquier base de datos de producción de más de 10 GB. Paralelismo real, consistencia garantizada, restores rápidos. Requiere una instalación separada, pero el tiempo que ahorras en el primer backup lo compensa con creces.

---

## La estrategia completa: no solo logical backup

Algo que siempre digo a los clientes: el backup lógico (mysqldump, mydumper) es **un** componente de la estrategia, no la estrategia entera.

Para el cliente de logística montamos este esquema:

1. **mydumper cada noche** — backup lógico completo, 8 threads, compresión zstd, retención 7 días
2. **Binary log continuo** — con `binlog_expire_logs_seconds` a 7 días, para el {{< glossary term="pitr" >}}point-in-time recovery{{< /glossary >}}
3. **Percona XtraBackup semanal** — backup físico en caliente, para el restore más rápido posible en caso de desastre total
4. **Test de restore automático** — un script que cada domingo hace el restore del backup de mydumper en una instancia de prueba y verifica el conteo de filas

El backup lógico es cómodo porque es portable — puedes hacer restore en cualquier versión de MySQL, en cualquier arquitectura. Pero para una base de datos de 60 GB, un backup físico con XtraBackup te permite un restore en 15-20 minutos en lugar de una hora y media. Cuando la base de datos de producción está caída y el teléfono suena, esa hora de diferencia importa.

El viernes siguiente, el DBA del cliente me escribió otra vez por Teams. Pero esta vez el mensaje era diferente: "Backup terminado en 23 minutos. Sin impacto en los usuarios. Gracias."

De nada. Pero la próxima vez, no esperes a que el backup tarde tres horas para pedirme ayuda.

------------------------------------------------------------------------

## Glosario

**[mysqldump](/es/glossary/mysqldump/)** — Utilidad de backup lógico incluida en cada instalación de MySQL. Produce un archivo SQL secuencial con todas las instrucciones para recrear esquema y datos. Single-threaded, fiable pero lenta en bases de datos grandes.

**[mysqlpump](/es/glossary/mysqlpump/)** — Evolución de mysqldump introducida en MySQL 5.7, con soporte para paralelismo a nivel de tabla y compresión nativa. Deprecado por Oracle en MySQL 8.0.34 por problemas de consistencia.

**[mydumper](/es/glossary/mydumper/)** — Herramienta open source de backup lógico para MySQL/MariaDB con paralelismo real a nivel de chunk. Divide las tablas grandes en pedazos y los exporta con threads múltiples, con restore paralelo mediante myloader.

**[PITR](/es/glossary/pitr/)** — Point-in-Time Recovery: técnica que combina un backup completo con los binary logs para llevar la base de datos a cualquier momento en el tiempo, no solo a la hora del backup.

**[GTID](/es/glossary/gtid/)** — Global Transaction Identifier: identificador único asignado a cada transacción en MySQL, que simplifica la gestión de la replicación y el seguimiento de transacciones entre master y réplica.
