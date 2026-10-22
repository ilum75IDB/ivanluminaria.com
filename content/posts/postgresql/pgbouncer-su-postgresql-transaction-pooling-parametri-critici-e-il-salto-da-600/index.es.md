---
categories:
- postgresql
date: '2026-11-17'
description: 12 microservicios, 600 conexiones simultáneas, PostgreSQL al límite.
  Cómo PgBouncer redujo las conexiones reales a 80 mejorando throughput y estabilidad.
  Transaction pooling, prepared statements, parámetros críticos.
draft: false
image: pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600.cover.jpg
seoTitle: 'PgBouncer: de 600 a 80 conexiones PostgreSQL sin perder throughput'
tags:
- pgbouncer
- connection-pooling
- postgresql
- performance
- scalability
title: 'PgBouncer: de 600 a 80 conexiones PostgreSQL sin perder throughput'
translationKey: pgbouncer_su_postgresql_transaction_pooling_parametri_critici_e_il_salto_da_600
webo_generated_at: 2026-10-22
webo_status: scheduled
---

## Seiscientas conexiones y un lunes por la mañana

El monitor del sistema mostraba números que no cuadraban. Una aplicación distribuida en doce microservicios, cada uno configurado con su propio pool interno de cincuenta conexiones hacia PostgreSQL. Sobre el papel: cincuenta por doce son seiscientas, pero en producción las instancias escalaban horizontalmente y los picos llevaban el total aún más arriba.

PostgreSQL no aguantaba. Las queries que normalmente completaban en pocos milisegundos esperaban slots libres durante decenas de segundos. El load average del servidor estaba constantemente por encima de diez. La memoria estaba casi agotada — no por los datos, sino por los propios procesos backend de PostgreSQL.

El equipo ya había intentado reducir los pools en el lado de la aplicación, pero cada microservicio lo desarrollaba un equipo distinto, con sus propias dependencias y restricciones. Coordinar una reducción uniforme habría llevado semanas. Hacía falta una solución a nivel de infraestructura.

Esa solución era PgBouncer.

## Por qué PostgreSQL sufre con cientos de conexiones

Antes de entender por qué PgBouncer ayuda, vale la pena entender por qué PostgreSQL sufre con muchas conexiones simultáneas — no es un defecto de configuración, es arquitectura.

PostgreSQL usa un modelo **process-per-connection**: cada conexión de cliente es atendida por un proceso OS separado, con su propio stack, su propia memoria privada y su propio overhead de context switch. En Linux, cada backend de PostgreSQL ocupa típicamente entre 5 y 10 MB de memoria privada (más la shared memory compartida). Con seiscientas conexiones activas, estamos hablando de 3-6 GB de RAM dedicados solo a los procesos backend — antes siquiera de ejecutar una query.

El problema se agrava con el **context switching**. El scheduler del kernel tiene que gestionar cientos de procesos que compiten por los cores de CPU. Cuando la mayoría de estos procesos está esperando I/O o locks, el kernel dedica tiempo a hacer scheduling en lugar de ejecutar trabajo útil. El resultado es visible en el load average: un servidor con ocho cores que muestra un load average de doce o quince no está haciendo doce veces el trabajo — está desperdiciando ciclos de CPU en overhead de scheduling.

También está el problema de los **locks y las estadísticas**. Cada conexión, incluso cuando está idle, mantiene estructuras de datos en memoria compartida. Con seiscientas conexiones, operaciones como `VACUUM`, `ANALYZE` y la gestión de locks se vuelven más costosas porque tienen que recorrer estructuras más grandes.

El parámetro `max_connections` de PostgreSQL existe precisamente por esto: no es un límite arbitrario, es una protección contra el colapso del sistema [1].

## Qué hace PgBouncer y cómo se posiciona en la arquitectura

PgBouncer es un connection pooler ligero que se sitúa entre los clientes (los microservicios) y PostgreSQL. Los clientes se conectan a PgBouncer como si fuera PostgreSQL — mismo puerto, mismo protocolo. PgBouncer mantiene un pool reducido de conexiones reales hacia la base de datos y las reutiliza entre los clientes.

El punto clave es que PgBouncer está escrito en C, es single-threaded con I/O asíncrono (basado en `libevent`), y gestiona miles de conexiones de cliente con un overhead mínimo. Una sola instancia de PgBouncer puede manejar tranquilamente mil conexiones de cliente usando unas pocas decenas de MB de RAM.

La arquitectura resultante es esta:

```text
[Microservicio A] ──┐
[Microservicio B] ──┤                    ┌──────────────────┐
[Microservicio C] ──┼──► [PgBouncer] ───►│  PostgreSQL      │
[Microservicio D] ──┤    (puerto 5432)   │  (80 conexiones) │
[Microservicio E] ──┘                    └──────────────────┘
  (600 conexiones cliente)
```

PgBouncer recibe las seiscientas conexiones de cliente, pero hacia PostgreSQL mantiene solo ochenta conexiones reales. Cuando un cliente envía una query, PgBouncer asigna una conexión backend disponible, ejecuta la query y — dependiendo del modo de pooling — libera esa conexión para otros clientes.

## Transaction pooling vs session pooling: la elección que lo cambia todo

PgBouncer soporta tres modos de pooling. Los dos relevantes en producción son **session pooling** y **transaction pooling**.

**Session pooling**: una conexión backend se asigna a un cliente durante toda la duración de su sesión. El backend se libera solo cuando el cliente se desconecta. Es el modo más compatible — funciona con todo — pero ofrece el menor ahorro: si un cliente mantiene la sesión abierta sin hacer queries, el backend sigue ocupado.

**Transaction pooling**: una conexión backend se asigna al cliente solo durante la duración de una transacción. En cuanto la transacción termina (COMMIT o ROLLBACK), el backend vuelve al pool y puede asignarse a otro cliente. Este es el modo que permite atender a seiscientos clientes con ochenta backends reales, porque en la práctica la mayoría de los clientes está idle entre una transacción y otra.

La elección entre los dos no es trivial. El transaction pooling tiene restricciones importantes:

- Las **variables de sesión** (`SET search_path`, `SET timezone`, etc.) no persisten entre transacciones distintas
- Los **prepared statements** con nombre no funcionan de forma transparente (lo vemos en la sección dedicada)
- Los **advisory locks** a nivel de sesión no funcionan
- `LISTEN/NOTIFY` no está soportado en transaction pooling

El session pooling es más seguro, pero requiere que los clientes se desconecten cuando no los necesitan — algo que los connection pools de aplicación ya hacen. En ese caso, el ahorro es real pero menos drástico.

En nuestro caso, los microservicios usaban un ORM estándar sin prepared statements con nombre, sin advisory locks, sin `LISTEN/NOTIFY`. El transaction pooling era la elección correcta.

## Instalación y configuración básica

En una distribución Debian/Ubuntu reciente, la instalación es directa [2]:

```bash
apt install pgbouncer
```

La configuración vive en dos archivos: `pgbouncer.ini` y `userlist.txt`.

### `pgbouncer.ini`

```ini
[databases]
; "appdb" es el nombre de la base de datos virtual expuesta por PgBouncer
; los clientes se conectan a este nombre
appdb = host=127.0.0.1 port=5432 dbname=appdb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; modo de pooling
pool_mode = transaction

; conexiones reales hacia PostgreSQL por pool
default_pool_size = 80

; máximo de conexiones cliente aceptadas por PgBouncer
max_client_conn = 1000

; pool de reserva para picos
reserve_pool_size = 10
reserve_pool_timeout = 5

; timeout de conexiones idle en el lado servidor
server_idle_timeout = 600

; log
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

; estadísticas
stats_period = 60
```

### `userlist.txt`

El archivo contiene las credenciales en el formato `"username" "password_hash"`. PgBouncer soporta hashes MD5 en el formato PostgreSQL (`md5` + md5(password + username)):

```text
"app_user" "md5a1b2c3d4e5f6..."
"pgbouncer_admin" "md5..."
```

Para generar el hash correcto:

```bash
echo -n "passwordusername" | md5sum
# anteponer "md5" al resultado
```

Tras la configuración, arrancar PgBouncer y verificar que se conecta correctamente:

```bash
systemctl start pgbouncer
systemctl enable pgbouncer

# verificar conexión admin
psql -h 127.0.0.1 -p 5432 -U pgbouncer pgbouncer
```

## De seiscientas a ochenta: los números antes y después

Tras el deploy de PgBouncer en transaction pooling, los números cambiaron de forma sustancial. Algunas mediciones representativas, recogidas en las primeras semanas:

| Métrica | Antes | Después |
|---|---|---|
| Conexiones reales a PostgreSQL | 580-620 | 65-80 |
| RAM ocupada por los backends PG | ~4,2 GB | ~600 MB |
| Load average (8 cores) | 12-18 | 3-5 |
| Latencia media de query (p50) | 180 ms | 22 ms |
| Latencia p99 | 4,2 s | 310 ms |
| Timeouts de conexión | frecuentes | ausentes |

La reducción de latencia no se debe solo a menos contención en las conexiones. Con menos procesos backend activos, el kernel hace menos context switching, PostgreSQL gestiona estructuras de datos más pequeñas y `VACUUM` consigue completar sus ciclos sin ser interrumpido constantemente. Es un efecto en cascada.

El throughput global — queries por segundo — aumentó alrededor de un 40%, a pesar de que el número de conexiones reales se redujo casi un orden de magnitud. Este es el punto que suele sorprender: menos conexiones no significa menos trabajo hecho, significa menos overhead por unidad de trabajo.

## Prepared statements y transaction pooling: el nudo que hay que desatar

El problema más habitual al migrar a PgBouncer en transaction pooling tiene que ver con los **prepared statements**.

En PostgreSQL, los prepared statements con nombre (`PREPARE nombre AS ...`) están ligados a la sesión. En transaction pooling, cada transacción puede acabar en un backend distinto — por lo que un prepared statement creado en una transacción anterior no existe en el nuevo backend.

El resultado es un error del tipo:

```text
ERROR: prepared statement "s1" does not exist
```

Hay tres enfoques para gestionarlo:

**1. Usar prepared statements anónimos (a nivel de protocolo)**

Los drivers modernos como `libpq`, `asyncpg`, `psycopg3` y JDBC soportan los prepared statements a nivel de protocolo sin nombre explícito. PgBouncer los gestiona de forma transparente en transaction pooling. Si el framework usa este mecanismo (la mayoría de los ORM modernos lo hace), no hay problema.

**2. Deshabilitar los prepared statements en el lado de la aplicación**

Si el driver o el ORM usa prepared statements con nombre, la solución más sencilla es deshabilitarlos. En SQLAlchemy, por ejemplo:

```python
engine = create_engine(
    "postgresql+psycopg2://user:pass@pgbouncer-host/appdb",
    execution_options={"no_parameters": True},
    # o con psycopg2:
    connect_args={"options": "-c statement_timeout=30000"}
)
```

Con JDBC y el driver de PostgreSQL:

```text
jdbc:postgresql://pgbouncer-host/appdb?prepareThreshold=0
```

`prepareThreshold=0` le indica al driver que nunca use prepared statements del lado del servidor.

**3. Usar `DEALLOCATE ALL` entre transacciones**

Menos elegante, pero funciona: configurar PgBouncer con `server_reset_query = DEALLOCATE ALL` para limpiar los prepared statements cuando un backend vuelve al pool. Atención: esto añade latencia a cada liberación de conexión.

En nuestro caso, los microservicios usaban SQLAlchemy con psycopg2 y prepared statements con nombre. La solución fue añadir el equivalente de `prepareThreshold=0` en la configuración del driver — un cambio de dos líneas por servicio, desplegado en una tarde.

## Los parámetros críticos que hay que entender antes de ir a producción

Tres parámetros de `pgbouncer.ini` merecen atención específica [3]:

**`default_pool_size`**: el número de conexiones reales hacia PostgreSQL por cada par (base de datos, usuario). Es el parámetro más importante. ¿Cómo elegirlo? Una regla empírica: `num_cores * 2` como punto de partida, luego medir. Con ocho cores, se empieza en dieciséis y se sube hasta encontrar el punto de saturación. En nuestro caso, ochenta conexiones en un servidor con dieciséis cores y SSD NVMe era el punto de equilibrio.

**`max_client_conn`**: el número máximo de conexiones de cliente que PgBouncer acepta en total. Debe ser mayor que el número de conexiones que los clientes pueden abrir. Si los seiscientos clientes abren una conexión cada uno, `max_client_conn` debe ser al menos seiscientos, mejor mil para tener margen. Cuando se supera este límite, PgBouncer rechaza nuevas conexiones — mejor un error explícito que un timeout silencioso.

**`reserve_pool_size`** y **`reserve_pool_timeout`**: el pool de reserva es un conjunto de conexiones adicionales que PgBouncer puede abrir cuando el pool principal está agotado. Si un cliente espera más de `reserve_pool_timeout` segundos por una conexión, PgBouncer recurre al reserve pool. Es una red de seguridad para los picos, no una solución estructural: si el reserve pool se agota con regularidad, hay que aumentar `default_pool_size`.

Un parámetro que suele pasarse por alto es **`server_idle_timeout`**: cuántos segundos de inactividad tienen que transcurrir antes de que PgBouncer cierre una conexión backend. El valor por defecto es seiscientos segundos (diez minutos). En entornos con tráfico muy variable — alto durante el día, casi nulo por la noche — bajarlo a ciento cincuenta o doscientos segundos reduce el número de conexiones idle que PostgreSQL mantiene abiertas en las horas de baja actividad.

## Leer los números: SHOW STATS y SHOW POOLS

PgBouncer expone una consola de administración accesible conectándose a la base de datos virtual `pgbouncer`:

```bash
psql -h 127.0.0.1 -p 5432 -U pgbouncer_admin pgbouncer
```

El comando más útil para el monitoreo diario es `SHOW STATS` [4]:

```sql
SHOW STATS;
```

```text
 database | total_xact_count | total_query_count | total_received | total_sent | total_xact_time | total_query_time | total_wait_time | avg_xact_count | avg_query_count | avg_recv | avg_sent | avg_xact_time | avg_query_time | avg_wait_time
----------+------------------+-------------------+----------------+------------+-----------------+------------------+-----------------+----------------+-----------------+----------+----------+---------------+----------------+---------------
 appdb    |        284721043 |         284721043 |   182043219872 | 9823041928 |    492831029183 |     492831029183 |      1823041928 |            312 |             312 |   199823 |    10782 |          1732 |           1732 |             6
```

Las columnas clave: `avg_wait_time` (tiempo medio de espera por una conexión backend — si supera unos pocos milisegundos, el pool es demasiado pequeño) y `avg_xact_time` (duración media de las transacciones).

`SHOW POOLS` muestra el estado en tiempo real de los pools:

```sql
SHOW POOLS;
```

```text
 database | user     | cl_active | cl_waiting | sv_active | sv_idle | sv_used | sv_tested | sv_login | maxwait | maxwait_us | pool_mode
----------+----------+-----------+------------+-----------+---------+---------+-----------+----------+---------+------------+-----------
 appdb    | app_user |       412 |          0 |        78 |       2 |       0 |         0 |        0 |       0 |          0 | transaction
```

- `cl_active`: clientes con una conexión backend asignada
- `cl_waiting`: clientes esperando una conexión backend — si este número es constantemente > 0, el pool está saturado
- `sv_active`: backends ocupados
- `sv_idle`: backends libres en el pool
- `maxwait`: tiempo máximo de espera de un cliente (en segundos) — el indicador de alarma principal

Para el monitoreo automático, estos valores se extraen fácilmente con cualquier sistema de métricas. Prometheus tiene un exporter dedicado (`pgbouncer_exporter`) que expone todas las métricas de `SHOW STATS` y `SHOW POOLS` en formato scrape [5].

## Lo que queda después del deploy

PgBouncer no es una solución mágica y no elimina la necesidad de diseñar bien la capa de acceso a los datos. Si las queries son lentas, PgBouncer no las acelera. Si la base de datos tiene problemas de locks, PgBouncer no los resuelve. Lo que hace es eliminar un cuello de botella específico — el overhead de gestión de conexiones — que en arquitecturas de microservicios se convierte rápidamente en el problema dominante.

Lo que llama la atención, mirando los números a posteriori, es lo sencillo que era el diagnóstico: el servidor tenía memoria suficiente para los datos, CPU suficiente para las queries, I/O suficiente para las escrituras. Estaba sufriendo por el puro overhead de gestionar seiscientos procesos OS simultáneamente. PgBouncer desplazó ese problema fuera de PostgreSQL, donde puede gestionarse de forma mucho más eficiente.

Un punto que vale la pena tener en cuenta para arquitecturas futuras: en un sistema con muchos microservicios, el connection pooling no debería ser un añadido a posteriori. Debería ser parte del diseño inicial, al mismo nivel que el load balancer o el service mesh. El coste de añadirlo después — coordinar los equipos, gestionar la migración, probar la compatibilidad de los prepared statements — es real, aunque al final manejable.

El equipo añadió después PgBouncer como componente estándar en el template de deploy para todos los nuevos servicios. Ya no es una decisión que tomar caso por caso.

## Fuentes oficiales

1. PostgreSQL Documentation — [Connections and Authentication: max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html)
2. PgBouncer Documentation — [Installation](https://www.pgbouncer.org/install.html)
3. PgBouncer Documentation — [Configuration file pgbouncer.ini](https://www.pgbouncer.org/config.html)
4. PgBouncer Documentation — [Usage: SHOW commands](https://www.pgbouncer.org/usage.html)
5. prometheus-community — [pgbouncer_exporter](https://github.com/prometheus-community/pgbouncer_exporter)

## Glosario
- **[PgBouncer](/es/glossary/pgbouncer/)** — Connection pooler ligero para PostgreSQL, escrito en C con I/O asíncrono. Se sitúa entre los clientes y la base de datos, manteniendo un pool reducido de conexiones reales hacia PostgreSQL y reutilizándolas entre muchos clientes.

- **[Transaction pooling](/es/glossary/pgbouncer/)** — Modo de pooling en el que una conexión backend se asigna al cliente solo durante la duración de una transacción. En cuanto la transacción termina, el backend vuelve al pool disponible para otros clientes. Permite atender a muchos clientes con pocas conexiones reales.

- **[Session pooling](/es/glossary/transaction-pooling/)** — Modo de pooling en el que una conexión backend permanece asignada a un cliente durante toda la duración de su sesión. Más compatible que el transaction pooling, pero menos eficiente porque el backend está ocupado incluso cuando el cliente está idle.

- **[`max_connections`](/es/glossary/pgbouncer/)** (PostgreSQL) — Parámetro de configuración que limita el número máximo de conexiones simultáneas aceptadas por PostgreSQL. No es un límite arbitrario: refleja el coste real en memoria y overhead de scheduling de cada proceso backend.

- **[`default_pool_size`](/es/glossary/transaction-pooling/)** (PgBouncer) — Número de conexiones reales hacia PostgreSQL mantenidas por PgBouncer para cada par (base de datos, usuario). Es el parámetro principal para dimensionar el pool: demasiado bajo provoca esperas, demasiado alto devuelve el problema de las conexiones excesivas a PostgreSQL.
