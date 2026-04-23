---
title: "MySQL"
layout: "list"
description: "MySQL y MariaDB: seguridad, rendimiento y arquitectura en una de las bases de datos más utilizadas del mundo."
image: "mysql.cover.jpg"
---

He visto servidores MySQL con 64GB de RAM e `innodb_buffer_pool_size` dejado a 128MB — "porque es el default y no tocamos nada". He visto tablas MyISAM aún en producción en 2026 porque "no tenemos tiempo de convertirlas", con locks a nivel de tabla que bloqueaban aplicaciones enteras durante los backups. He visto réplicas master-slave con 47.000 segundos de retraso y nadie que se daba cuenta, porque nadie miraba `Seconds_Behind_Master`.

Y he visto exactamente lo contrario: parques MySQL con cientos de instancias gestionadas con disciplina, donde cada decisión — storage engine, charset, binlog format, topología — se toma con consciencia y no por inercia.

La diferencia nunca ha sido el motor. Siempre ha sido **la seriedad con la que alguien eligió las opciones**.

------------------------------------------------------------------------

MySQL es la base de datos que no necesita presentación. Es el motor que impulsó el crecimiento de la web durante más de veinte años.

Nacida en 1995 en Suecia, en 2008 fue adquirida por Sun Microsystems — y cuando Oracle completó la adquisición de Sun en 2010, MySQL acabó en el portafolio del mayor proveedor de bases de datos comerciales del mundo. **Yo era empleado de Oracle en ese momento**, y recuerdo bien el clima: por un lado la curiosidad de ver cómo Oracle gestionaría un producto open source tan popular, por otro el temor de que MySQL fuera marginado a favor de la base de datos propietaria.

Ese temor llevó a Michael "Monty" Widenius — el creador original de MySQL — a hacer el fork en 2009, dando vida a **MariaDB**. Un proyecto que comparte sus raíces con MySQL pero ha tomado caminos propios en motores de almacenamiento, optimizador y funcionalidades avanzadas.

La historia ha demostrado que ambos proyectos sobrevivieron y evolucionaron. Pero en el día a día de quien gestiona producciones reales, MySQL sigue siendo el que *parece* sencillo y en cambio esconde decisiones críticas:

- **storage engines mezclados** por vieja costumbre — MyISAM, InnoDB y a veces Archive conviven sin motivo
- **charset equivocado** (latin1 en vez de utf8mb4) que corrompe en silencio los datos multilingües
- **binlog en formato STATEMENT** que causa inconsistencias en replicación con consultas no deterministas
- **`sql_mode`** permisivo por "retrocompatibilidad" — consultas que devuelven resultados distintos en cada ejecución
- **replicación sin monitoring activo** — y cuando el master se cae, el slave lleva tres días de retraso

------------------------------------------------------------------------

## 🔧 Las elecciones que marcan la diferencia en producción

Hay cinco decisiones que — bien tomadas — hacen funcionar MySQL durante diez años, y — mal tomadas — te obligan a reescribir medio aplicativo. Son decisiones triviales de enumerar, incomodísimas de cambiar después.

| Elección | Qué decide | Cómo la configuro |
|---|---|---|
| **Storage engine** | Granularidad de lock, transaccionalidad, crash recovery | InnoDB siempre, salvo casos marginales y motivados — MyISAM es un vestigio, no una elección |
| **`innodb_buffer_pool_size`** | Memoria para caché de datos e índices InnoDB | 70-80% de la RAM en servidor dedicado, el resto es desperdicio para el motor |
| **Charset y collation** | Codificación de caracteres y ordenamiento | `utf8mb4` + `utf8mb4_0900_ai_ci` — nada de `utf8` (que en MySQL es incompleto) |
| **`binlog_format`** | Formato de los logs binarios para replicación y PITR | `ROW` casi siempre — `STATEMENT` causa problemas en replicación con consultas no deterministas |
| **`sql_mode`** | Qué errores tolera MySQL y cuáles no | Strict mode activo, `ONLY_FULL_GROUP_BY` incluido — un MySQL permisivo es un MySQL que te miente |

Cinco elecciones. Treinta minutos de discusión. Años de operatividad sin incidentes serios.

------------------------------------------------------------------------

## 📚 De qué hablo aquí

Historias reales y decisiones operativas sobre MySQL y MariaDB en producción. Seguridad, gestión de usuarios y privilegios, tuning de InnoDB, replicación master-slave e InnoDB Cluster, estrategias de upgrade y migración, backups consistentes con `mysqldump` y herramientas físicas, diferencias reales entre MySQL y MariaDB que emergen solo bajo carga.

Nada de recetas genéricas. Solo lo que he visto funcionar en entornos reales — postal, telco, finance, administración pública — donde MySQL aguanta parques de instancias en paralelo y no puede permitirse decisiones tomadas "por inercia".

------------------------------------------------------------------------

Usar MySQL no es solo ejecutar consultas.

Es entender cómo el motor gestiona conexiones, privilegios y recursos bajo carga real — y reconocer que la simplicidad aparente es, a menudo, la trampa más cara.
