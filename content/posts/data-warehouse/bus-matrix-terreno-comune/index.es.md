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
