---
title: "Tres data marts, tres verdades sobre las ventas: el bus matrix como terreno común"
description: "Un grupo asegurador multi-país con tres departamentos, tres data marts crecidos en autonomía y tres números diferentes para las pólizas emitidas en febrero. El bus matrix no lo resolvió en una tarde — pero dio un terreno compartido sobre el que empezar a hablar."
date: "2026-05-12T08:03:00+01:00"
draft: false
translationKey: "bus_matrix_terreno_comune"
tags: ["data-warehouse", "bus-matrix", "conformed-dimensions", "kimball", "dimensional-modeling", "data-mart"]
categories: ["Data Warehouse"]
image: "bus-matrix-terreno-comune.cover.jpg"
---

La primera reunión fue extraña. En la sala había tres personas — el responsable comercial, la marketing manager de la red de agencias, el controller de administración — y cada uno tenía delante un Excel con las nuevas pólizas emitidas en febrero en un gran grupo asegurador italiano que opera en varios países europeos. Los totales no cuadraban. Diferencias del 9%, del 12%, del 16% según con qué dos compararas. Ninguno de los tres parecía especialmente sorprendido.

*"Siempre lo hacemos así,"* dijo el controller. *"Cada uno tiene el suyo. Luego, cuando el board pide la recaudación de primas, pasamos el mío porque es el que cuadra con el cierre contable."*

Ese fue el punto de partida del proyecto. No un desastre que descubrí yo, no un sistema que hubiera que salvar. Una situación que los tres conocían perfectamente y que se había vuelto inmanejable cuando el nuevo CFO, llegado hacía pocas semanas, empezó a hacer preguntas incómodas. Cosas como: *¿por qué la recaudación de primas por ramo es distinta entre comercial y finance?* O: *¿cuántos asegurados activos tenemos en realidad en Italia, 420 mil o 510 mil?*

No teníamos una respuesta. Teníamos tres.

## 🧩 Tres data marts crecidos por su cuenta

Cada departamento, con los años, se había construido su propio {{< glossary term="data-mart" >}}data mart{{< /glossary >}}. No por mala fe, no por elección estratégica: por necesidad. La IT central era lenta, los proyectos duraban meses, los departamentos necesitaban números ya. Así cada uno se hizo el suyo — a veces con herramientas BI distintas, a veces apoyándose en la misma base de datos pero en esquemas separados.

El resultado, años después, era este:

| Data mart   | Grain principal                      | Dimensiones                                | Sistema fuente                       |
|-------------|--------------------------------------|--------------------------------------------|--------------------------------------|
| Comercial   | Póliza × movimiento × día            | Asegurado, Producto, Agencia, Fecha        | Policy Management (mainframe)        |
| Marketing   | Cliente × campaña × mes              | Cliente, Campaña, Canal, Mes               | CRM + plataforma campaign management |
| Finance     | Movimiento contable × partida × mes  | Cuenta, Centro de coste, Ramo, Mes         | ERP contabilidad + reaseguro         |

Tres {{< glossary term="star-schema" >}}star schemas{{< /glossary >}}, tres definiciones de "cliente" (el asegurado privado, la empresa contratante, el contratante con titularidad conjunta), tres calendarios distintos (marketing en mes solar, finance en mes contable con cierre a día 25, comercial con la fecha de efecto de la póliza, que puede ir meses por detrás de la fecha de emisión). Y sobre todo, tres conceptos de "producto": el policy management identificaba la póliza con el código de tarifa interno, el CRM con el macroproducto comercial (Auto, Hogar, Vida, Salud), finance la agrupaba por ramo a efectos IVASS.

Cada uno de los tres números era *correcto* en su contexto. El problema era que no se hablaban entre sí.

## 🔍 El CFO había visto el problema antes que nosotros

Lo honesto que hay que decir es que el problema lo puso en agenda el CFO, no el equipo IT y no yo. Él no quería un data warehouse nuevo. Quería algo más prosaico: una sola línea de números que fuera la misma en todos los cuadros de mando. *"No me importa quién de vosotros tiene razón. Me importa que la recaudación de febrero sea un único número."*

Dicho así parece obvio. En la práctica, cuando le pides a tres departamentos que alineen sus definiciones, descubres que cada uno lleva años razonando sobre su propio mapa del territorio y no tiene ninguna gana de redibujarlo. Comercial cuenta primas brutas a fecha de emisión, finance las cuenta netas de comisiones a fecha de devengo. Marketing considera "cliente activo" a cualquiera con al menos una póliza en vigor en los últimos 12 meses, finance a cualquiera con una posición de primas abierta en el ejercicio. Nadie se equivoca. Simplemente responden a preguntas distintas.

Lo primero útil que hicimos, antes de tocar una línea de código, fue una serie de talleres de dos horas — uno por cada dimensión candidata — en los que cada departamento explicaba qué entendía. Con acta. El {{< glossary term="bus-matrix" >}}bus matrix{{< /glossary >}} que dibujamos después no nació de una genialidad arquitectónica: nació de la transcripción de esos talleres.

## 🚌 El bus matrix, sin mitología

Ralph {{< glossary term="kimball" >}}Kimball{{< /glossary >}} describe el bus matrix como una matriz bidimensional: en las filas los **procesos de negocio** (en nuestro caso emisión de pólizas, renovaciones, siniestros, recaudación de primas, campañas de marketing, suscripciones online…), en las columnas las **dimensiones conformadas** (cliente, póliza, intermediario, fecha, campaña, canal…). En las celdas, una X si ese proceso de negocio usa esa dimensión.

La matriz por sí sola no hace nada. No genera código, no crea tablas, no resuelve conflictos. Sirve para una cosa: forzar a todos a mirar la misma hoja.

Lo que terminamos dibujando, tras los talleres, era algo así (simplificado):

| Proceso de negocio              | Cliente | Póliza | Intermediario | Fecha | Campaña | Canal | Cuenta |
|---------------------------------|:-------:|:------:|:-------------:|:-----:|:-------:|:-----:|:------:|
| Emisión de pólizas              |    X    |   X    |      X        |   X   |    X    |   X   |        |
| Renovaciones                    |    X    |   X    |      X        |   X   |         |   X   |        |
| Siniestros abiertos             |    X    |   X    |               |   X   |         |       |        |
| Campañas a intermediarios       |         |        |      X        |   X   |    X    |   X   |        |
| Cobro de primas                 |    X    |   X    |      X        |   X   |         |       |   X    |
| Suscripciones online            |    X    |   X    |               |   X   |    X    |   X   |        |

Seis filas, siete columnas. Leído así, la hoja dice algo simple e incómodo a la vez: **la dimensión Cliente aparece en cinco procesos de seis, Póliza en cinco, Fecha en todos e Intermediario en cuatro**. Si la definición de Cliente es distinta entre comercial y marketing, cinco procesos de seis devolverán números incoherentes. No es un problema de BI, es un problema de maestro de datos.

## 🔗 Qué es una dimensión conformada

Una {{< glossary term="conformed-dimension" >}}dimensión conformada{{< /glossary >}} es una dimensión con la misma estructura, la misma semántica y la misma clave a través de varios data marts. No quiere decir "una única tabla física compartida" — puede estar replicada, puede vivir en esquemas distintos — pero sí quiere decir que si el cliente `IT_C00217654` aparece en el data mart comercial y en el de marketing, **es el mismo cliente, con los mismos atributos de clasificación, y los números relativos a él se pueden sumar sin reservas**.

Conformar una dimensión significa acordar tres cosas:

1. **La clave natural**: ¿cuál es el identificador único del cliente? ¿El código fiscal? ¿El NIF? ¿El código de contratante del sistema de pólizas? En los tres sistemas era distinto — el policy management usaba el código de contratante del mainframe (con lógica de deduplicación heredada de los noventa), el CRM usaba email + código fiscal, finance usaba el código de cliente del ERP con su propia numeración. Sin un mapeo explícito, tres "contratantes" distintos podían ser la misma persona — y peor todavía, en países distintos cambiaba la clave natural: codice fiscale en Italia, NIF en España, SIREN o número fiscal individual en Francia.

2. **Los atributos compartidos**: ¿qué columnas pertenecen a la dimensión conformada? País, región, provincia, tipo de contratante (persona física / jurídica), franja de edad, segmento de riesgo, fecha del primer contrato, canal de adquisición. Todo lo demás se queda en tablas dimensionales *locales* a cada data mart, sin interferir con el análisis cross-departamento.

3. **La grain**: la dimensión conformada tiene una fila por contratante individual, no una fila por "segmento de clientes". Si marketing quiere razonar por segmento, añade un atributo `segmento_marketing` a la dimensión conformada y lo rellena con su propia lógica.

En estas tres cosas trabajamos seis semanas. No fue divertido. Marketing temía perder su modelo de segmentación por comportamiento, comercial no quería que el maestro de contratantes pasara "bajo control de finance", y finance pretendía que la clave natural fuera la suya porque "es la que se usa para facturar y para IVASS". El compromiso fue: dimensión conformada gestionada por un nuevo equipo central de datos, con representantes de los tres departamentos en el comité de gobierno y una clave subrogada interna que actúa de pivote entre las tres claves naturales distintas.

## 🛠️ Cómo integramos sin reescribir todo

Aquí está la parte técnica que normalmente queda en segundo plano frente a la narrativa del "proyecto salvado". La verdad es que no reescribimos los tres data marts. Hubiera sido un proyecto de dos años y nadie lo habría financiado.

La estrategia fue por capas.

**Capa 1 — Dimensiones conformadas centralizadas.** Creamos un esquema `dim_conformed` con las dimensiones compartidas (`dim_customer`, `dim_policy`, `dim_intermediary`, `dim_date`, `dim_campaign`, `dim_channel`). `dim_customer` es la más compleja: poblada por un proceso de record matching entre policy management, CRM y ERP, con reglas explícitas para las colisiones (mismo código fiscal, nacionalidades distintas → merge si mismo país de residencia; mismo email, códigos fiscales distintos → flag manual).

```sql
CREATE TABLE dim_conformed.dim_customer (
    sk_customer         BIGINT PRIMARY KEY,      -- clave subrogada central
    customer_code       VARCHAR(20) NOT NULL,    -- clave natural acordada
    country_code        CHAR(2)  NOT NULL,       -- IT, ES, FR, DE, ...
    tax_id              VARCHAR(20),             -- CF / NIF / SIREN / Steuer-ID
    email_primary       VARCHAR(120),
    party_type          VARCHAR(10),             -- person, company
    first_name          VARCHAR(80),
    last_name           VARCHAR(80),
    legal_name          VARCHAR(120),            -- para personas jurídicas
    birth_year          INT,                     -- NULL para empresas
    gender              CHAR(1),                 -- NULL para empresas
    region              VARCHAR(40),
    province            VARCHAR(40),
    risk_segment        VARCHAR(20),             -- low, medium, high
    acquisition_channel VARCHAR(30),             -- agency, broker, direct, online
    first_policy_date   DATE,                    -- fecha del primer contrato en el grupo
    status              VARCHAR(10),             -- active, dormant, churned
    valid_from          DATE NOT NULL,
    valid_to            DATE,                    -- SCD Tipo 2 sobre region, risk_segment, status
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    record_source       VARCHAR(20),             -- PMS, CRM, ERP, MERGE
    last_update_ts      TIMESTAMP NOT NULL
);

CREATE INDEX ix_dim_customer_natural ON dim_conformed.dim_customer(customer_code, is_current);
CREATE INDEX ix_dim_customer_tax_id  ON dim_conformed.dim_customer(country_code, tax_id) WHERE tax_id IS NOT NULL;
```

Unas 3,1 millones de filas para 1,8 millones de contratantes distintos en los cuatro países principales (la diferencia es el histórico de versiones en {{< glossary term="scd" >}}SCD Tipo 2{{< /glossary >}}).

**Capa 2 — Bridge entre claves antiguas y claves nuevas.** Los tres data marts existentes seguían funcionando con sus claves locales. Creamos una tabla de mapeo para cada uno:

```sql
CREATE TABLE dim_conformed.xref_customer (
    source_system   VARCHAR(10) NOT NULL,   -- PMS | CRM | ERP
    country_code    CHAR(2)     NOT NULL,   -- para distinguir homonimias entre países
    source_key      VARCHAR(50) NOT NULL,   -- clave local en el sistema de origen
    sk_customer     BIGINT      NOT NULL,   -- puntero a la dim_customer conformada
    mapping_quality VARCHAR(20),            -- exact_match, fuzzy_match, manual
    mapping_ts      TIMESTAMP   NOT NULL,
    PRIMARY KEY (source_system, country_code, source_key)
);
```

La xref se rellena con un job nocturno que lee los maestros origen, contrasta con la dimensión conformada, aplica las reglas de matching y registra los casos ambiguos en una tabla de anomalías gestionada manualmente por el equipo de datos. En los cuatro países, la cola de casos ambiguos rondaba el 1,5% — un volumen manejable por dos personas en dos horas al día.

**Capa 3 — Vistas de integración.** Sobre las tres {{< glossary term="fact-table" >}}fact tables{{< /glossary >}} originales creamos vistas que sustituyen la clave local por la clave subrogada conformada:

```sql
CREATE OR REPLACE VIEW vw_fact_new_business_conformed AS
SELECT
    f.policy_id,
    xc.sk_customer,           -- clave conformada, no la del PMS local
    xp.sk_policy,
    xi.sk_intermediary,
    xd.sk_date,
    f.gross_premium,
    f.net_premium,
    f.commission_amount,
    f.policy_duration_months
FROM pms_dm.fact_new_business f
LEFT JOIN dim_conformed.xref_customer      xc
       ON xc.source_system = 'PMS'
      AND xc.country_code  = f.country_code
      AND xc.source_key    = f.pms_customer_code
LEFT JOIN dim_conformed.xref_policy        xp
       ON xp.source_system = 'PMS'
      AND xp.source_key    = f.pms_tariff_code
LEFT JOIN dim_conformed.xref_intermediary  xi
       ON xi.source_system = 'PMS'
      AND xi.country_code  = f.country_code
      AND xi.source_key    = f.pms_agent_code
JOIN dim_conformed.dim_date xd
       ON xd.calendar_date = f.effective_date;
```

Ningún departamento tuvo que dejar de usar su data mart. Quien quería análisis mono-departamento, los seguía haciendo en el suyo. Quien necesitaba cross-departamento, usaba las vistas conformadas.

## 📊 La pregunta que antes era imposible

La primera consulta realmente cross-mart que lanzamos — la que antes del trabajo sobre las dimensiones conformadas habría salido con tres respuestas distintas — parecía trivial:

```sql
-- Intermediarios alcanzados por una campaña y nuevas pólizas emitidas en los 60 días siguientes
SELECT
    dc.country_code,
    dc.risk_segment,
    COUNT(DISTINCT cm.sk_intermediary)   AS targeted_intermediaries,
    COUNT(DISTINCT nb.sk_customer)       AS converted_customers,
    SUM(nb.gross_premium)                AS new_business_premium,
    ROUND(100.0 * COUNT(DISTINCT nb.sk_customer)
          / NULLIF(COUNT(DISTINCT cm.sk_intermediary), 0), 1) AS conversion_ratio_pct
FROM vw_fact_campaign_conformed cm
JOIN dim_conformed.dim_intermediary di
     ON di.sk_intermediary = cm.sk_intermediary AND di.is_current
LEFT JOIN vw_fact_new_business_conformed nb
     ON nb.sk_intermediary = cm.sk_intermediary
    AND nb.sk_date BETWEEN cm.sk_date AND cm.sk_date + 60
LEFT JOIN dim_conformed.dim_customer dc
     ON dc.sk_customer = nb.sk_customer AND dc.is_current
WHERE cm.campaign_code = 'Q1_2026_AUTO_BROKER_PUSH'
GROUP BY dc.country_code, dc.risk_segment
ORDER BY new_business_premium DESC NULLS LAST;
```

Antes, esta consulta se hacía exportando dos CSV, cargándolos en Excel y haciendo BUSCARV sobre el código de agente/contratante — que en los dos sistemas estaba escrito de forma distinta (el CRM usaba el código broker interno, el PMS el código RUI). Los errores de matching estaban en torno al 20-30% y nadie los medía. La gestión por país añadía complicaciones: un broker que operaba a la vez en Italia y España aparecía dos veces.

Después, la consulta corre en unos 5 segundos sobre Oracle Exadata con datos de un trimestre en los cuatro países y devuelve **un único número** por combinación país × segmento de riesgo. Marketing lo compara con finance, finance lo compara con comercial, y si hay discrepancia se mira el join: no el concepto de cliente.

| Métrica                              | Antes                      | Después                       |
|--------------------------------------|----------------------------|-------------------------------|
| Definiciones de "contratante"        | 3                          | 1 (con atributos por departamento) |
| Diferencias entre cuadros departamentales | 9-16% según el KPI    | < 0,5% (solo timing ETL)      |
| Tiempo para análisis cross-departamento | 1-2 días de Excel       | consulta directa sobre vistas |
| Coste del re-platforming completo    | estimado 18-24 meses       | 4 meses + gobierno continuo   |

El re-platforming completo nunca lo pagamos porque no fue necesario. El bus matrix y las dimensiones conformadas no sustituyen un refactor: te dan tiempo para hacerlo con calma cuando realmente toca, un proceso cada vez.

## 🧠 Por qué el bus matrix se hace antes de codificar

El motivo por el que esto se hace al principio — y no después de que tres data marts hayan crecido por su cuenta — es elemental: conformar después cuesta diez veces más que conformar antes.

Cuando partes de cero, la dimensión conformada es un documento de página y media escrito en una reunión de dos horas. Cuando partes de tres data marts en producción desde hace seis años, es un proyecto de seis meses con un comité de gobierno, un equipo central de datos, un proceso de matching que construir, tablas de mapeo que mantener y bloqueos organizativos que negociar.

Kimball escribió el bus matrix en los noventa con esta intención exacta: dar a los equipos un papel para colgar en la pared antes de abrir el editor SQL. Es un ejercicio de alineamiento, no de arquitectura. La arquitectura viene después, y sale mucho mejor si el papel se ha hecho.

## Lo que aprendí

El trabajo técnico — la `dim_customer`, las xref, las vistas — fue la parte fácil. La parte difícil fue llevar a tres departamentos a ponerse de acuerdo sobre qué significa "cliente". Y esa parte no la resolví yo: la resolvió el CFO con su peso político, el comité de gobierno con seis semanas de paciencia, y el DBA del cliente que tenía una memoria histórica impresionante de cada decisión tomada en años anteriores y por qué.

Cuando hoy veo un proyecto de DWH que arranca sin un bus matrix dibujado y compartido, levanto la mano antes de empezar. No por hacer el listo — para recordarme que esa fase, la de alinear las definiciones, no se puede saltar. Si la saltas, la pagas después con intereses. Si la haces, el resto del proyecto se vuelve casi aburrido. Y es exactamente como debería ser.

------------------------------------------------------------------------

## Glosario

**[Bus Matrix](/es/glossary/bus-matrix/)** — Matriz bidimensional de Kimball con los procesos de negocio en las filas y las dimensiones conformadas en las columnas. Sirve para alinear a los departamentos en las definiciones antes de empezar el diseño físico del data warehouse.

**[Conformed Dimension](/es/glossary/conformed-dimension/)** — Dimensión compartida con la misma estructura, semántica y clave entre varios data marts. Permite sumar medidas procedentes de procesos de negocio distintos sin ambigüedad.

**[Data Mart](/es/glossary/data-mart/)** — Subconjunto del data warehouse enfocado a un único proceso de negocio o área funcional (ventas, marketing, finance). Puede construirse de forma autónoma por un departamento, pero corre el riesgo de divergir de los demás si falta la conformidad de dimensiones.

**[Kimball](/es/glossary/kimball/)** — Ralph Kimball, metodología de diseño de data warehouse basada en modelado dimensional, star schema y bus matrix. Enfoque bottom-up que parte de los procesos de negocio y construye data marts integrados mediante dimensiones conformadas.

**[Star Schema](/es/glossary/star-schema/)** — Modelo de datos con una fact table central conectada a varias tablas dimensionales. Es el patrón base de cualquier data mart Kimball y el terreno natural sobre el que actúan las dimensiones conformadas.
