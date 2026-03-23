---
title: "BYOL"
description: "Bring Your Own License — programa Oracle que permite reutilizar las licencias on-premises en el cloud OCI sin costes adicionales de licensing."
translationKey: "glossary_byol"
aka: "Bring Your Own License"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**BYOL** (Bring Your Own License) es un programa de Oracle que permite a las empresas transferir las licencias de software adquiridas para la infraestructura on-premises a Oracle Cloud Infrastructure (OCI), sin necesidad de comprar nuevas licencias cloud.

## Como funciona

Cuando una empresa ya tiene licencias Oracle — tipicamente Enterprise Edition con opciones como RAC, Data Guard o Partitioning — puede "llevarlas consigo" en la migracion a OCI. El contrato de soporte (Software Update License & Support) se mantiene, y las licencias se asocian a los recursos cloud en lugar de a los servidores fisicos.

En OCI, cada OCPU corresponde a una processor license, con una relacion 1:1 transparente. Esto hace que el calculo sea predecible y conforme a las politicas de licensing de Oracle.

## Por que es importante en las migraciones

El BYOL es a menudo el factor decisivo en la eleccion de OCI frente a otros proveedores cloud. En AWS o Azure, Oracle aplica reglas de licensing diferentes: cada vCPU cuenta como medio procesador, y opciones como RAC no estan soportadas o requieren licencias adicionales. Una auditoria Oracle en un cloud que no sea OCI puede convertir un ahorro aparente en un coste imprevisto muy significativo.

## Que cubre

- Oracle Database (todas las ediciones)
- Opciones del database (RAC, Data Guard, Partitioning, Advanced Compression, etc.)
- Oracle Middleware y otros productos Oracle con licencias elegibles

El BYOL no es automatico: debe solicitarse y configurarse en el momento del provisioning de los recursos OCI, especificando las licencias existentes en el contrato.
