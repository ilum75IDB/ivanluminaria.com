---
categories:
- data-warehouse
date: '2026-07-07'
draft: false
image: data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati.cover.jpg
tags: []
title: 'La pausa del almuerzo que retrasó el go-live: Data Governance en el DWH'
translationKey: data_governance_nel_data_warehouse_dal_controllo_qualita_alla_conformita_normati
webo_generated_at: 2026-06-14
webo_status: scheduled
---

```
---
title: "La mesa fuera de la oficina: data governance antes del go-live de un DWH"
seoTitle: "Data governance en DWH: calidad, TDE y roles antes del go-live"
description: "Qué falta cuando un DWH está 'técnicamente listo': data ownership, calidad continua, TDE en Oracle 19c y Data Catalog. Caso real en sector asegurador."
tags: ["data-governance", "data-quality", "oracle-19c", "data-warehouse", "gdpr"]
---
```

## La mesa fuera de la oficina

Era uno de esos días de finales de primavera en que por fin se puede comer fuera. Carlo — senior data analyst de un gran grupo asegurador italiano con el que colaboro desde hace un par de años — estaba visiblemente satisfecho. El DWH estaba técnicamente listo: los datos cargados, el modelo dimensional aguantaba, las primeras queries de los informes funcionaban. Ya estaba pensando en cómo presentar el éxito a los managers la semana siguiente.

«Diría que estamos listos para el go-live», me dijo mientras cortaba la pizza.

Esperé un segundo antes de responder. No para enfriar el entusiasmo — el trabajo hecho era sólido — sino porque esa frase, "estamos listos", escondía una serie de preguntas que nadie había planteado en voz alta todavía. Y los gaps de governance que emergen después del go-live casi siempre los interpretan los managers como descuido, no como complejidad intrínseca del proyecto.

«Técnicamente sí», respondí. «Pero ¿ya tienes respuesta para: quién es el data owner de `policy_holder_data`? ¿Qué pasa si un informe muestra una prima anómala — quién la corrige y en cuánto tiempo? ¿Y el GDPR, cómo lo gestionamos a nivel de almacenamiento?»

Carlo dejó el tenedor.

Esa conversación duró hasta el café, y luego continuó delante del PC por la tarde. Este artículo es el intento de poner por escrito lo que nos dijimos.

---

## Lo que un DWH "listo" no incluye por defecto

Un Data Warehouse técnicamente funcional — ETL que corre, dimensiones pobladas, hechos agregados correctamente — es condición necesaria pero no suficiente para salir a producción en un contexto enterprise. Especialmente en sectores regulados como el asegurador, donde los datos incluyen datos de clientes, histórico de pólizas, pagos y — en algunos productos — datos sanitarios.

Las expectativas implícitas que managers y usuarios de negocio traen a la sala de reuniones el día del go-live afectan al menos cuatro áreas que raramente aparecen en los requisitos funcionales iniciales.

### Calidad de datos: no es un control, es un proceso

La calidad de los datos no es una casilla que marcar antes de la puesta en producción. Es un proceso continuo. En el DWH asegurador que estábamos discutiendo, las tablas `claims_history` y `premium_payments` llegaban de sistemas fuente con calidad heterogénea: algunas compañías del grupo tenían codificaciones distintas para el mismo tipo de siniestro, campos de fecha con formatos inconsistentes, valores nulos en columnas que deberían haber sido obligatorias.

Durante la carga ya habíamos implementado algunas reglas de validación en el ETL. Pero "validar en entrada" y "garantizar calidad en el tiempo" son dos cosas distintas. Hacen falta:

- **Umbrales de alerta**: si el número de registros rechazados en una carga supera el 2%, alguien tiene que saberlo antes de que se distribuyan los informes
- **Procesos de remediation**: ¿quién corrige los datos anómalos? ¿Con qué prioridad? ¿Con qué trazabilidad de auditoría?
- **Monitorización longitudinal**: un dato que era correcto hace seis meses puede no serlo si las reglas de negocio cambian

Carlo había gestionado la validación en entrada. La monitorización continua y los procesos de remediation estaban aún por definir.

### Ownership: la pregunta incómoda

«¿Quién es el data owner de `policy_holder_data`?», había preguntado en el almuerzo.

Carlo respondió: «Pues, IT».

Esa respuesta casi siempre es incorrecta — o al menos incompleta. IT gestiona la infraestructura y los procesos técnicos, pero el dato pertenece al negocio. En un contexto asegurador, el data owner de una tabla con datos personales y contractuales de clientes debería ser una función de negocio (por ejemplo, la dirección comercial o compliance), no el equipo técnico.

La distinción entre **Data Owner** (responsabilidad de negocio sobre el dato), **Data Steward** (gestión operativa de la calidad y las reglas) y **Data Custodian** (gestión técnica de la infraestructura) no es burocracia. Es la respuesta práctica a la pregunta "¿a quién llamo cuando este dato está mal?". Sin ese mapa, cada anomalía se convierte en una reunión de tres horas para decidir de quién es la situación.

### Glosario de datos: cuando "prima" no significa lo mismo para todos

En el grupo asegurador, el término "prima" tenía al menos tres definiciones operativas distintas según la unidad de negocio. El DWH las había consolidado en una única columna `premium_amount` en la tabla `premium_payments`, pero sin documentar qué definición se había adoptado ni por qué.

Un glosario de datos compartido — incluso en su forma más simple, un documento versionado con las definiciones acordadas entre negocio e IT — es la diferencia entre un informe que genera confianza y uno que genera discusiones. No hace falta una herramienta enterprise de cientos de miles de euros: hace falta una definición escrita, acordada y accesible.

### Data Lineage: la trazabilidad que salva las auditorías

«Si un analista de risk management pregunta de dónde viene este número», le dije a Carlo abriendo el PC, «¿puedes responderle en menos de una hora?»

Silencio.

El data lineage — la capacidad de trazar el recorrido de un dato desde la fuente hasta el informe final, a través de todas las transformaciones — es esencial en dos escenarios: el troubleshooting cotidiano ("¿por qué este valor ha cambiado respecto al mes pasado?") y las auditorías regulatorias ("demuéstrame que este agregado se calcula correctamente según las reglas X"). En un sector como el asegurador, el segundo escenario no es hipotético.

---

## GDPR: de restricción legal a decisión arquitectónica

Hasta este punto de la conversación, Carlo asentía con el aire de quien reconoce los gaps pero los ve como "cosas que añadir después". El punto de inflexión llegó con el GDPR.

«El GDPR lo gestionamos con la política de privacidad y el consentimiento», dijo Carlo. «El cumplimiento ya está cubierto legalmente.»

«El cumplimiento documental, sí», respondí. «Pero el GDPR en su artículo 32 habla explícitamente de medidas técnicas apropiadas, incluido el cifrado. Si alguien accede físicamente a los ficheros de la base de datos — un backup robado, un disco mal descomisionado, un acceso no autorizado al almacenamiento — ¿los datos de `policy_holder_data` son legibles en claro?»

Esa es la diferencia entre cumplimiento formal e implementación arquitectónica. El primero protege legalmente a la organización mientras no pasa nada. El segundo reduce la probabilidad de que pase algo, y reduce el impacto si ocurre.

### Transparent Data Encryption en Oracle 19c

Oracle Database 19c incluye Transparent Data Encryption (TDE) [1], una funcionalidad que cifra los datos en reposo — los ficheros de datos, los ficheros de redo log, los backups — sin requerir modificaciones en las aplicaciones. Para el DWH asegurador, esto significa que aunque alguien obtenga acceso físico a los ficheros en `oracle-dwh-prod-eu-01`, los datos permanecen ilegibles sin la clave de cifrado gestionada por el wallet de Oracle.

Habilitar TDE a nivel de tablespace es relativamente sencillo:

```sql
-- Creación del wallet y configuración de la master key (ejecutar como SYSDBA)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/wallet' IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "wallet_password" WITH BACKUP;

-- Cifrado del tablespace que contiene los datos sensibles
ALTER TABLESPACE policy_data ENCRYPTION ONLINE USING 'AES256' ENCRYPT;
```

```sql
-- Verificación del estado de cifrado de los tablespaces
SELECT tablespace_name, encrypted
FROM dba_tablespaces
WHERE encrypted = 'YES';
```

Lo que TDE no hace: no protege frente a un usuario con acceso SQL legítimo a la base de datos. No es un sustituto de la gestión de accesos y privilegios. Es una capa de protección específica para el dato en reposo — exactamente lo que el GDPR considera una "medida técnica apropiada" en el contexto de la protección contra accesos físicos no autorizados o pérdida de soportes [2].

La conversación con Carlo derivó hacia un punto práctico: implementar TDE antes del go-live es una operación planificable con downtime controlado. Implementarla después, sobre un sistema en producción con terabytes de datos históricos ya cargados, es una operación más compleja y arriesgada. La ventana de oportunidad era esa.

---

## Un framework de calidad que aguanta en el tiempo

Volviendo a la calidad de los datos: lo que teníamos en marcha era una serie de controles en el ETL. Lo que hacía falta era un framework.

La diferencia es sustancial. Los controles en el ETL bloquean o señalan los registros no conformes en el momento de la carga. Un framework de calidad añade:

**Monitorización proactiva**: jobs programados que verifican periódicamente las condiciones de calidad sobre las tablas ya cargadas. Por ejemplo, una query que comprueba cada mañana si existen registros en `policy_holder_data` con `fiscal_code` nulo o con formato no válido — datos que podrían haber entrado por rutas de carga no estándar.

```sql
-- Ejemplo de control de calidad programado sobre policy_holder_data
SELECT
    COUNT(*) AS anomalias_codigo_fiscal,
    SYSDATE AS fecha_control
FROM policy_holder_data
WHERE fiscal_code IS NULL
   OR NOT REGEXP_LIKE(fiscal_code, '^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$');
```

**Umbrales y notificaciones**: si el recuento de anomalías supera un umbral definido (por ejemplo, más de 50 registros con código fiscal no válido en un día), el sistema notifica al Data Steward responsable antes de que se distribuyan los informes.

**Trazabilidad de remediation**: cada corrección manual sobre los datos debe quedar documentada — quién corrigió, cuándo, por qué, cuál era el valor original. En un contexto asegurador, esa trazabilidad es relevante tanto para las auditorías internas como para eventuales verificaciones regulatorias.

---

## El Data Catalog: donde la governance se vuelve navegable

Un Data Catalog [3] es la infraestructura que hace navegable todo lo que hemos discutido hasta aquí. No es una herramienta opcional para equipos grandes: es la diferencia entre una governance que existe solo en documentos y una governance que los usuarios de negocio pueden usar de verdad.

En el contexto del DWH asegurador, un Data Catalog mínimo debería responder a estas preguntas sin necesidad de llamar al equipo técnico:

- ¿Qué contiene la tabla `claims_history`? ¿Qué columnas? ¿Con qué reglas de negocio?
- ¿De dónde vienen los datos de `premium_payments`? ¿A través de qué transformaciones?
- ¿Quién es el data owner de `policy_holder_data`? ¿A quién contacto si encuentro una anomalía?
- ¿Qué tablas contienen datos personales sujetos al GDPR?

Herramientas enterprise como Apache Atlas, Collibra o Alation gestionan esto de forma estructurada. Para un primer go-live, incluso una solución más ligera — una wiki estructurada, una hoja compartida con las definiciones acordadas — es infinitamente mejor que nada. Lo importante es que exista, que se mantenga actualizada y que los usuarios sepan dónde encontrarla.

La integración con el glosario de datos es natural: las definiciones acordadas (por ejemplo, la definición de "prima" adoptada en el DWH) viven en el catalog y se referencian desde la documentación de las columnas. El lineage, idealmente, es visualizable desde la misma herramienta.

---

## Quién hace qué: los tres roles que no se pueden ignorar

Antes de cerrar la conversación con Carlo, pusimos por escrito un mapa de roles. No como ejercicio formal, sino como respuesta práctica a la pregunta: cuando algo sale mal, ¿a quién llamo?

**Data Owner**: es una figura de negocio, no técnica. Decide las reglas de uso del dato, aprueba los cambios en las definiciones, es responsable de la calidad desde el punto de vista del negocio. Para `policy_holder_data`, el Data Owner natural era la dirección de compliance del grupo.

**Data Steward**: es el puente entre negocio e IT. Gestiona operativamente las reglas de calidad, monitoriza las anomalías, coordina la remediation. Puede ser una figura técnica con fuerte sensibilidad de negocio, o viceversa. En nuestro caso, Carlo era el candidato natural para este rol en algunas de las tablas clave.

**Data Custodian**: es el equipo técnico. Gestiona la infraestructura, implementa las reglas técnicas definidas por el Data Owner y el Data Steward, garantiza disponibilidad y seguridad. La responsabilidad de TDE, los backups, los accesos a la base de datos — todo eso es scope del Data Custodian.

La distinción no es burocracia. Es la respuesta operativa a la pregunta "quién es responsable de qué". Sin ese mapa, cada situación se convierte en una discusión sobre quién debería resolverla, en lugar de una discusión sobre cómo resolverla.

---

## «Ahora sé qué falta»

Hacia las cinco de la tarde, Carlo se levantó de la silla y dijo algo que me quedó grabado: «Bien. Ahora sé qué falta. Y sé cómo presentarlo a los managers sin que parezca que hemos hecho un trabajo a medias.»

Esa es la diferencia entre llegar a una reunión de go-live con los gaps ocultos y llegar con los gaps mapeados y un plan para cerrarlos. Los managers no esperan perfección — esperan que el equipo sepa dónde está y hacia dónde va.

Retrasamos el go-live tres semanas. En ese tiempo: definimos los Data Owners para las tablas principales, implementamos TDE en el tablespace que contenía los datos personales, escribimos un glosario de datos mínimo para los términos críticos, configuramos los primeros controles de calidad programados y esbozamos la estructura del Data Catalog.

No era todo. Pero era suficiente para llegar a la reunión con los managers con las respuestas correctas a las preguntas correctas. El mérito no fue de una intuición puntual — fue de una conversación franca entre dos personas con perspectivas distintas que trabajaban hacia el mismo objetivo.

---

## Fuentes oficiales

1. Oracle Database Security Guide 19c — [Configuring Transparent Data Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-transparent-data-encryption.html)
2. Reglamento (UE) 2016/679 — [Artículo 32: Seguridad del tratamiento](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679)
3. DAMA International — [DAMA-DMBOK2: Data Management Body of Knowledge](https://www.dama.org/dama-dm-bok-2) — cubre Data Governance, Data Quality, Data Lineage, Data Catalog, Data Stewardship

---

## Glosario candidato

- **Data Governance** — El conjunto de procesos, políticas, estándares y métricas que aseguran el uso eficaz de la información, garantizando su calidad, integridad, seguridad y conformidad normativa. No es un proyecto con fecha de fin: es un framework operativo continuo.

- **Data Lineage** — La capacidad de trazar el recorrido de un dato desde la fuente a través de todos los sistemas y transformaciones, hasta el destino final. Esencial para troubleshooting, auditorías regulatorias y verificación de la corrección de los cálculos.

- **Transparent Data Encryption (TDE)** (Oracle) — Funcionalidad de Oracle Database que cifra los datos en reposo — ficheros de datos, redo log, backups — sin modificaciones en las aplicaciones. Protege frente a accesos físicos no autorizados a los soportes de almacenamiento.

- **Data Quality** — La medida en que los datos son precisos, completos, coherentes, válidos y oportunos. No es un control puntual sino un proceso continuo de monitorización, alertas y remediation que garantiza la fiabilidad de los análisis en el tiempo.

- **Data Catalog** — Inventario organizado de todos los datos disponibles en una organización, con metadatos, glosario, lineage y herramientas de búsqueda. Hace la governance navegable para los usuarios de negocio sin requerir intervención técnica para cada pregunta sobre los datos.
