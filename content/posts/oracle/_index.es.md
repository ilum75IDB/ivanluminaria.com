---
title: "Oracle"
layout: "list"
date: "2026-03-10T08:03:00+01:00"
description: "Oracle Database: seguridad, rendimiento y arquitectura en la base de datos empresarial más longeva y compleja del mercado."
image: "oracle.cover.jpg"
---

He visto a un DBA apagar una producción con un `DROP TABLESPACE` lanzado en la ventana equivocada. He visto consultas de cuatro segundos convertirse en cuatro horas tras un upgrade, porque alguien había tocado `optimizer_features_enable` "si total era igual". He visto backups que no se restauraban, auditorías desactivadas "temporalmente" desde hace cinco años, e índices creados en producción a mano un viernes por la tarde.

Y he visto exactamente lo contrario: instancias Oracle que llevan veinte años funcionando sin un minuto de downtime no planificado, aguantando cargas enormes y sobreviviendo a tres upgrades mayores sin despeinarse.

La diferencia nunca ha sido la versión. Siempre ha sido **quién la gestionaba**.

------------------------------------------------------------------------

Trabajo con Oracle desde 1996. En casi treinta años he visto pasar Oracle 7, 8i, 9i, 10g, 11g, 12c, 19c, 21c, 23ai — y paradigmas, modas, consultores que vendían la feature del momento como la respuesta a cualquier problema.

El corazón del motor, sin embargo, ha seguido siendo el mismo: **sólido, complejo, despiadado con quien no lo conoce a fondo.**

Oracle no se aprende con tutoriales. Se aprende:

- con los **incidentes de producción** a las tres de la madrugada, cuando el manual sirve de poco y vale más un colega que ya ha visto ese comportamiento
- con las **migraciones** en las que el plan de ejecución cambia el día después del go-live y nadie entiende por qué
- con los **planes de ejecución** que se vuelven patológicos tras un `DBMS_STATS.GATHER_SCHEMA_STATS` lanzado con parámetros por defecto
- con las **`v$`** que dicen la verdad incluso cuando la aplicación miente
- con los **tuning packs** que sirven de verdad, y con los que pagaste y nunca vas a encender

------------------------------------------------------------------------

## 🔧 Qué miro cuando llego a una instancia nueva

Cuando un cliente me llama porque "la base de datos va lenta" o "algo no va bien", hay cinco cosas que miro antes de tocar cualquier parámetro. No es una checklist de curso de certificación — es lo que he aprendido a mirar después de perder demasiado tiempo en los sitios equivocados.

| Qué | Dónde lo miro | Por qué |
|---|---|---|
| **La carga real** | AWR, ASH, `v$active_session_history` | Entender quién consume de verdad CPU, I/O y `db time` — a menudo no es lo que sospecha el cliente |
| **Lo que ha tocado quien ha pasado antes** | `v$parameter` con `ismodified`, `dba_hist_parameter` | Los parámetros "no estándar" son la primera pista de debug pasado sin documentar |
| **Quién hace qué** | `dba_audit_trail`, `unified_audit_trail`, jobs programados | Encontrar los jobs nocturnos, las conexiones aplicativas reales, los accesos DBA sin trazar |
| **Estado de Data Guard** | `v$dataguard_stats`, `v$archive_dest_status` | Si hay standby, verificar que esté realmente alineado — no fiarse de los dashboards |
| **Espacio y crecimiento** | `dba_tablespaces`, `dba_hist_tbspc_space_usage` | Entender dónde se va a estrellar antes de que suceda, no después |

Una vez leídas estas cinco cosas, tengo el 70% del cuadro. Las otras preguntas vienen después — y vienen enfocadas.

------------------------------------------------------------------------

## 📚 De qué hablo aquí

Historias reales, números concretos y lecciones aprendidas sobre Oracle en producción. Arquitectura, rendimiento, seguridad, migraciones, tuning SQL, PL/SQL, gestión del almacenamiento y decisiones de diseño que separan una instalación que funciona de una que sobrevive.

Nada de teoría de folleto. Solo lo que he visto funcionar — y lo que he visto fracasar — en entornos reales: seguros, telco, administración pública, banca, farmacéutico.

------------------------------------------------------------------------

Con Oracle no basta conocer la sintaxis.

Hay que entender cómo razona el motor — y tener la humildad de admitir que, a veces, tiene razón él.
