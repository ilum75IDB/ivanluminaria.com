---
categories:
- oracle
date: '2026-10-27'
description: 'Cómo planificar el upgrade de Oracle 11g R2 a 19c en OCI para una base
  de datos financiera de 8 TB: estrategia XTTS, cutover en 4 horas y rollback demostrable.'
draft: false
image: oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback.cover.jpg
seoTitle: 'Upgrade Oracle 11g a 19c en OCI: 8 TB con XTTS y rollback'
tags:
- oracle
- database-migration
- upgrade
- oci
- disaster-recovery
- financial-systems
title: 'Oracle 11g R2 → 19c en OCI: 8 TB en finanzas, un plan de upgrade con fases
  y rollback'
translationKey: oracle_11g_r2_19c_su_oci_8_tb_in_finanza_un_piano_di_upgrade_con_fasi_e_rollback
webo_generated_at: 2026-10-10
webo_status: scheduled
---

*Cómo desbloquear la parálisis decisional sobre una instancia Oracle 11g EOL todavía en producción, elegir la estrategia de upgrade correcta para 8 TB cloud-to-cloud y llevar el cutover a cuatro horas con rollback listo en cada paso.*

---

## Una instancia que nadie quería tocar

Hay un patrón que quien lleva años trabajando con sistemas financieros conoce bien. Una instancia Oracle 11g Release 2 — en este caso concreto la **11.2.0.4**, última minor de toda la familia 11g, publicada en 2013 — sigue encendida en producción en 2026. Encima corre un sistema de middle-office para el control de límites de exposición intraday, construido en los años diez sobre PL/SQL complejo, con 420+ packages y procedimientos, 1.400 objetos aplicativos, y una lógica de posting contable que se ha ido estratificando a lo largo de varias releases de negocio. La base de datos pesa **8 TB** y crece algunos cientos de GB al año. Corre sobre una instancia OCI VM.Standard dedicada, migrada a la nube cuatro años antes con un lift-and-shift limpio.

Oracle declaró el Premier Support para 11g **concluido en enero de 2015**, el Extended Support **concluido en diciembre de 2020**. Desde hace casi seis años la instancia no recibe parches de seguridad, ningún fix de bug mayor, ninguna CPU trimestral. En las auditorías internas de los últimos tres años la instancia está sistemáticamente clasificada como «riesgo alto», pero nunca ha ocurrido un incidente lo suficientemente grave como para forzar la decisión. Mientras tanto el marco de compliance ha cambiado: DORA ha entrado en vigor, Banca d'Italia ha afinado sus expectativas sobre la soportabilidad de infraestructuras críticas, y los revisores externos han empezado a pedir planes de remediation con fechas.

**¿Por qué la instancia seguía en 11g?** No por falta de competencia técnica — el equipo interno sabía cómo hacer un upgrade. Estaba parada por **parálisis decisional**. La aplicación era crítica (detenerla significaba que los traders no veían sus límites de exposición en tiempo real), la ventana de downtime defendible ante el negocio era de cuatro horas como máximo una noche de sábado, ninguno de los vendors aplicativos involucrados estaba ya disponible para soporte, y nadie en el equipo interno quería **poner su firma** bajo un procedimiento de upgrade que tocaba el núcleo del posting contable. Era un caso clásico de *«mientras funciona, no se toca»* — comprensible, legítimo, insostenible.

## Cuando la decisión ya no se puede aplazar

En un momento dado la balanza de riesgos se invirtió. El riesgo de una vulnerabilidad sin parchear se volvió mayor que el riesgo del cutover. El risk committee pidió un plan con **fechas concretas** y **rollback demostrable**. El plan se propuso en seis semanas de estudio, se discutió en dos reuniones con el negocio, y se aprobó con el compromiso formal de **dejar la instancia antigua en solo lectura durante dos semanas tras el cutover**, por si fuera necesario volver atrás.

El target se eligió **19c (19.24)** — no 21c, no 23ai. Dos razones. La primera: 19c es la **Terminal Release** del branch 12.2, lo que en jerga Oracle significa que es la release destinada a Long-Term Support (Premier Support hasta 2027, Market-Driven Support hasta 2032). Es la versión más estable y mejor documentada del momento, con un ecosistema de patch set maduro. La segunda: 19c es el **mínimo target compatible** para un upgrade directo desde 11.2.0.4 (el direct upgrade está soportado: no se necesita ningún salto intermedio vía 12c). Saltar directamente a 21c o 23ai habría requerido un hop multi-release más largo y un riesgo de estabilidad post-migración mayor, con poco beneficio funcional para una aplicación legacy.

## Las opciones técnicas sobre la mesa

Para una base de datos Oracle de 8 TB que actúa como almacenamiento de un aplicativo mission-critical con una ventana de cutover de cuatro horas, las estrategias realistas son cinco. Vale la pena articularlas juntas, porque la elección es un trade-off entre tiempo de preparación, downtime efectivo, complejidad del rollback y coste de licenciamiento de las herramientas auxiliares.

| Estrategia | Downtime | Prep | Rollback | Notas |
|---|---|---|---|---|
| **DBUA in-place** (direct 11.2.0.4 → 19c) | 6-12 horas en 8 TB | Días | Difícil (restore backup) | Soportado pero demasiado downtime para este caso |
| **Data Pump expdp/impdp** full | 10-20 horas en 8 TB | Días | Fácil (instancia antigua intacta) | Lento pero limpio. Demasiado downtime |
| **Transportable Tablespaces (TTS) + Data Pump metadata** | 4-6 horas en 8 TB | 1 semana | Fácil | Copia inicial larga, cutover aceptable |
| **Cross-Platform Transportable Tablespaces con Incremental Backups (XTTS)** | **2-4 horas en 8 TB** | **2 semanas en paralelo** | **Fácil (RO en la fuente)** | **Elegido** — minimiza el cutover a costa de una prep larga |
| **Oracle Zero Downtime Migration (ZDM)** | 10-30 minutos | 3-4 semanas + licensing | Automatizado | Opción premium, descartada por coste del tool + complejidad de setup |

La elección recayó en **XTTS con incremental backups**. Permite dividir el upgrade en dos fases distintas: una **larga pero invisible para el negocio** (prep de dos semanas de copia y sincronización) y una **corta y visible** (cutover de cuatro horas en la noche del sábado). El método está documentado por Oracle en MOS Note 2471245.1 y es el más utilizado en producción para bases de datos de gran tamaño cross-version y cross-platform. El rollback sigue siendo sencillo porque la fuente no se toca — permanece en producción hasta el momento del cutover, y puede reactivarse en treinta minutos incluso después.

## El plan, en seis fases

### Fase 0 — Assessment (2 semanas antes del cutover)

Ejecución de **`preupgrd.sql`** (la herramienta de pre-upgrade distribuida con 19c, que hay que ejecutar en la fuente 11.2.0.4 después de copiarla desde la descarga de 19c) + **`autoupgrade.jar`** en modo analyze. El output es un informe que enumera:

- Objetos inválidos a remediar antes del upgrade
- Parámetros `init.ora` deprecados (clásicos en 11g: `background_dump_dest`, `user_dump_dest`, `plsql_v2_compatibility`)
- Features deprecadas usadas por el aplicativo (la más común: tipos `LONG` y `RAW`, hay que verificar si la app tiene dependencias)
- Estadísticas obsoletas en tablas grandes
- Contraseñas con hashing débil (11g aceptaba `DES` por defecto, 19c requiere `SHA-2`)

En este caso el informe señaló 23 objetos inválidos (casi todos procedurales, resolubles con una recompilación), 7 parámetros deprecados en el `spfile`, y **ningún uso de LONG/RAW** en el código aplicativo (verificado vía `dba_tab_columns`). Dos semanas fueron suficientes para arreglarlo todo sin prisas.

### Fase 1 — Construcción del entorno 19c target en OCI

En paralelo a la Fase 0, aprovisionamiento de una **nueva instancia OCI** con 19c (19.24 RU trimestral actual), misma shape que la fuente pero con **almacenamiento NVMe local** para rendimiento de import, no network block volume. Instalación limpia, configuración de red, listener y service name idénticos a la fuente (para minimizar el cambio aplicativo en el cutover). Los **tablespaces USER se crean vacíos** con la misma topología que la fuente — mismos nombres, mismos tamaños iniciales, misma extensión. Los tablespaces de sistema (`SYSTEM`, `SYSAUX`, `UNDO`, `TEMP`) son los nativos de 19c, no los transportados.

### Fase 2 — Initial RMAN backup level 0 + rollforward inicial (días 1-7 de prep)

Backup incremental **level 0** de todos los tablespaces USER de la fuente, en formato *backupset*, mediante RMAN con paralelismo alto (`CONFIGURE DEVICE TYPE DISK PARALLELISM 8`). Transferencia al target vía **Object Storage OCI** (bucket compartido entre las dos instancias — latencia baja, sin salto a internet). Rollforward inicial en el target 19c mediante **convert** cross-version (`RMAN> CONVERT DATAFILE ... TO PLATFORM 'Linux x86 64-bit'` si es cross-platform, o simple restore si es la misma plataforma).

Duración: ~5-6 días para 8 TB con esa shape de almacenamiento. La operación es completamente **en background**, sin impacto sobre la fuente productiva.

### Fase 3 — Incremental backup level 1 cíclicos (días 7-14 de prep)

A partir de ese momento, RMAN **incremental level 1 cada 4 horas** en la fuente (`BACKUP INCREMENTAL LEVEL 1 FOR RECOVER OF COPY WITH TAG 'xtts_incr' ...`). Transferencia continua al target, rollforward aplicado en el target. El **lag** entre fuente y target se mantiene por debajo de las 6 horas durante toda la semana anterior al cutover. Monitorización con scripts dedicados que rastrean el SCN de ambas instancias.

### Fase 4 — Pre-cutover testing (fin de semana anterior al go-live)

En un entorno de staging — copia completa de la aplicación y la base de datos — simulación completa del procedimiento de cutover. Validación del aplicativo con el endpoint 19c, smoke test de todos los procesos batch nocturnos, prueba de todos los servicios online que llaman a stored procedures complejas. Corrección de cuatro diferencias de comportamiento detectadas (ninguna grave: una `ORA-29913` en una external table con un path absoluto hardcodeado, dos queries con hints deprecados, un job de `DBMS_SCHEDULER` con un parámetro que había cambiado de formato).

### Fase 5 — Cutover nocturno (noche del sábado, 4 horas)

| Hora | Acción |
|---|---|
| **T−00:30** | Comunicación al equipo de negocio: freeze inminente |
| **T+00:00** | `SHUTDOWN IMMEDIATE` del aplicativo (stop de escrituras en la fuente) |
| **T+00:10** | Último RMAN incremental level 1 en la fuente |
| **T+00:40** | Apply del último incremental en el target 19c |
| **T+01:00** | Fuente 11g puesta en `READ ONLY` en todos los tablespaces USER |
| **T+01:10** | Export de metadata vía **Data Pump** (`expdp TRANSPORT_TABLESPACES=...`) — todos los tablespaces USER + users + grants + public synonyms + sequences + views + packages + triggers + jobs |
| **T+01:40** | Transporte físico de los datafiles USER de la fuente al target (metadata ya aplicada) + import de metadata en 19c (`impdp TRANSPORT_DATAFILES=... TRANSPORT_TABLESPACES=... REMAP_SCHEMA=...` si es necesario) |
| **T+02:30** | `ALTER TABLESPACE ... READ WRITE` en el target + `UTL_RECOMP.RECOMP_PARALLEL` para recompilar objetos inválidos |
| **T+03:00** | Smoke test de todos los servicios aplicativos contra el nuevo endpoint 19c |
| **T+03:30** | Switch del service name DNS aplicativo (TTL reducido preventivamente a 60 segundos) al nuevo endpoint |
| **T+04:00** | **GO-LIVE** |

### Fase 6 — El plan de rollback (las dos semanas tras el go-live)

Dos redes de seguridad, en orden de invasividad creciente:

**Red 1 — Switch DNS hacia atrás**: la antigua 11g permanece encendida en solo lectura durante 14 días. En caso de problemas graves irresolubles en las primeras horas, basta con **volver a poner `READ WRITE` en los tablespaces de la fuente** (operación de pocos segundos) y **revertir el service name DNS**. El aplicativo vuelve a hablar con la 11g en menos de 30 minutos, perdiendo como máximo los datos escritos en el 19c tras el cutover (cuantificables y recuperables vía Data Pump desde el 19c a la 11g, si fuera necesario). Coste de esta red: mantener la instancia 11g encendida dos semanas más.

**Red 2 — Snapshot OCI**: snapshot a bloques de la instancia 19c antes del cutover + snapshot de la 11g con el último estado RW. En caso de catástrofe durante el propio cutover (p. ej., corrupción del metadata durante el import), restore de los snapshots en 1-2 horas. Red de seguridad raramente necesaria, pero da tranquilidad al risk committee cuando se aprueba el plan.

## Los primeros días tras el go-live

El primer lunes por la mañana es el momento crítico. La apertura del mercado trae la primera oleada de carga real sobre una instancia 19c que hasta ese momento solo había visto el test del sábado por la noche. La monitorización atenta de las primeras 48 horas se centra en tres aspectos:

- **Planes de ejecución cambiados**: 19c introduce un cost-based optimizer significativamente diferente al de 11g — Automatic SQL Plan Management, Statistics Advisor más agresivo, nuevos algoritmos de join. En este caso, de los 420+ packages aplicativos, 11 queries críticas cambiaron de plan con regresión de rendimiento. Resueltas en 48 horas con hints específicos (`USE_NL`, `INDEX`) o baselines de `SPM` capturadas del plan anterior ejecutado en staging.
- **Estadísticas**: recolección completa post-upgrade con el **nuevo optimizer de 19c**, sin reutilizar los valores de 11g, que estarían obsoletos sobre estructuras de memoria diferentes. Operación pesada (horas) pero necesaria.
- **AWR comparison**: snapshots AWR durante 48 horas pre-cutover en la 11g y 48 horas post-cutover en la 19c, comparación con `DBMS_WORKLOAD_REPOSITORY.AWR_DIFF_REPORT_HTML`. Sin degradación sistémica, mejora neta en algunas queries batch (el 19c tiene un adaptive join que el 11g no tenía).

Tras 14 días, con cero rollbacks necesarios y métricas estables, la antigua 11g fue **apagada y archivada** (snapshot preservado durante 90 días para auditoría, después retención normal). El risk committee cerró el punto en su agenda por primera vez en cinco años.

## Lo que conviene llevarse, si estás en la misma situación

Un upgrade de 11g a 19c no es una operación técnicamente complicada — es una operación **políticamente** complicada. La técnica es conocida, documentada, repetida en miles de implementaciones. Lo que realmente mantiene las instancias EOL en producción es la combinación de: aplicativo crítico sin vendor de soporte activo, ventana de downtime estrecha, ausencia de un procedimiento de rollback demostrable que permita a quien firma dormir la noche después del cutover.

Tres preguntas merecen plantearse si estás evaluando un upgrade similar:

**1. ¿Cuál es el máximo downtime aplicativo defendible ante el negocio, y qué estrategia técnica cabe en esa ventana?** Si la respuesta es *«cuatro horas como máximo en una noche de sábado»*, XTTS con incremental es casi obligatorio para bases de datos de más de 2-3 TB. Si la respuesta es *«diez minutos como máximo»*, ZDM es la única opción realista — y hay que presupuestar el tool.

**2. ¿Cuál es el plan de rollback, medido en minutos?** Un plan de rollback que requiere *«restore completo desde el backup»* no es un plan de rollback, es una esperanza. Un plan serio es *«switch del service name DNS hacia atrás en 30 minutos con la instancia antigua encendida en solo lectura»*. La diferencia, ante el risk committee, lo es todo.

**3. ¿Quién firma el procedimiento de cutover, y qué necesita esa persona para firmar?** En los casos reales que hemos visto, el bloqueo nunca es técnico — es la búsqueda de esa firma. Cuando el plan incluye rollback medible, snapshot pre-cutover, pre-test completo en staging, la firma llega. Sin esos elementos, el plan se queda en el cajón durante años.

Una instancia 11g en producción en 2026 no es un error — es un síntoma. El plan de upgrade no es solo técnica: es el momento en que se reactiva una decisión que llevaba años paralizada.

---

*Ivan Luminaria es Technical Leader para bases de datos mission-critical. Trabaja con CIO, CTO y IT Director de bancos mid-tier, aseguradoras, telcos, utilities y grandes administraciones públicas italianas con un método de lectura cross-layer construido en casi treinta años de sistemas reales.*

## Glosario
- **[XTTS](/es/glossary/xtts/)** (Oracle) — Cross-Platform Transportable Tablespaces with Incremental Backups: método de migración RMAN que combina un backup level 0 inicial con incrementales cíclicos para minimizar el downtime de cutover en bases de datos de gran tamaño.
- **[Terminal Release](/es/glossary/cutover/)** (Oracle) — Release designada para soporte a largo plazo dentro de un branch de versión. 19c es la Terminal Release del branch 12.2, con Premier Support hasta 2027 y Market-Driven Support hasta 2032.
- **[SPM baseline](/es/glossary/xtts/)** — SQL Plan Management baseline: mecanismo de Oracle para fijar un plan de ejecución específico para una query, evitando regresiones de rendimiento tras cambios en el optimizer o en las estadísticas.
- **[AWR](/es/glossary/preupgrd-sql/)** (Oracle) — Automatic Workload Repository: repositorio de snapshots periódicos de métricas de workload, base de los AWR reports y de ADDM. Permite comparar el comportamiento del sistema antes y después de un cambio mayor.
- **[cutover](/es/glossary/cutover/)** — En el contexto de una migración de base de datos, el momento de transición controlada en que el tráfico de producción se redirige de la instancia origen a la instancia destino. Su duración y reversibilidad son los parámetros clave del plan de upgrade.

## Fuentes oficiales

1. Oracle Database Upgrade Guide 19c — [Direct Upgrade Paths to Oracle Database 19c](https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/oracle-database-release-numbers.html)
2. Oracle MOS Note 2471245.1 — Cross Platform Transportable Tablespaces with Incremental Backups (referencia interna MOS, requiere cuenta My Oracle Support)
3. Oracle Database — [AutoUpgrade Tool Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/about-autoupgrade-tool.html)
4. Oracle Database — [DBMS_WORKLOAD_REPOSITORY Reference](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_WORKLOAD_REPOSITORY.html)
