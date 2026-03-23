---
title: "ZDM"
description: "Zero Downtime Migration — herramienta Oracle para automatizar migraciones a OCI combinando Data Guard y Data Pump bajo una capa de orquestacion."
translationKey: "glossary_zdm"
aka: "Zero Downtime Migration"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**ZDM** (Zero Downtime Migration) es la herramienta que Oracle proporciona para automatizar las migraciones de bases de datos Oracle hacia OCI (Oracle Cloud Infrastructure) o hacia bases de datos on-premises de version superior. El nombre es algo optimista — el downtime no es cero, pero se reduce al minimo.

## Como funciona

ZDM es esencialmente un orquestador que combina tecnologias Oracle existentes bajo un unico flujo automatizado. Soporta dos modalidades:

- **Migracion fisica** (basada en Data Guard): crea un standby de la base de datos origen en el destino, lo sincroniza mediante redo transport, y luego ejecuta un switchover. Downtime del orden de minutos.
- **Migracion logica** (basada en Data Pump): ejecuta export e import logico con sincronizacion incremental mediante GoldenGate o Data Pump. Mas flexible pero mas lenta.

## Cuando usarlo

ZDM esta indicado para migraciones estandar donde la infraestructura origen y destino estan configuradas de forma convencional. La ventaja es la automatizacion: reduce la posibilidad de error humano en los pasos repetitivos.

## Cuando no usarlo

Para configuraciones complejas — RAC con DB links cross-engine, dependencias externas no estandar, procedimientos PL/SQL con llamadas HTTP — la capa de automatizacion de ZDM puede convertirse en un obstaculo. En estos casos, configurar Data Guard manualmente da mas control sobre los detalles y la secuencia de operaciones.

## Requisitos

ZDM requiere un host dedicado (el "ZDM service host") con acceso SSH tanto a la base de datos origen como al destino. El origen debe ser Oracle 11.2.0.4 o superior, el destino puede estar en OCI o on-premises.
