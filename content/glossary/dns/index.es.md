---
title: "DNS"
description: "DNS (Domain Name System) traduce nombres de host legibles en direcciones IP, habilitando la conectividad de red para bases de datos, listeners Oracle y servicios OCI."
translationKey: "glossary_dns"
aka: "Domain Name System"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

El DNS (Domain Name System) es el sistema distribuido que resuelve nombres de host simbólicos en direcciones IP. En entornos de bases de datos e infraestructura cloud, es el mecanismo subyacente que permite a clientes, aplicaciones y herramientas de administración alcanzar instancias Oracle, endpoints de OCI y servicios de red sin necesidad de codificar direcciones IP estáticas en las cadenas de conexión.

## Cómo funciona

Cuando un cliente Oracle intenta conectarse a un host mediante `tnsnames.ora` o Easy Connect, el sistema operativo consulta el resolver DNS configurado. El resolver recorre la jerarquía DNS (raíz → TLD → servidor autoritativo) y devuelve la dirección IP correspondiente al nombre de host.

```bash
# Verificar resolución DNS de un listener Oracle en OCI
nslookup db-prod.subnet.vcn.oraclevcn.com
dig +short db-prod.subnet.vcn.oraclevcn.com A
```

En OCI, cada VCN dispone de un resolver DNS interno que gestiona automáticamente los registros de los recursos del tenant (DB Systems, Autonomous Database, Load Balancers).

## Contexto operativo

Durante una actualización de Oracle 11g R2 → 19c en OCI, el DNS resulta crítico en al menos tres momentos:

- **Aprovisionamiento del nuevo DB System**: el nombre de host del sistema 19c destino debe ser resolvible por todos los clientes y los jobs de migración antes de iniciar la transferencia de datos.
- **Cutover y ROLLBACK**: si el plan utiliza un CNAME o un alias DNS como punto de acceso de la aplicación, el cambio del registro (con un TTL bajo preconfigurado) es el mecanismo de conmutación más rápido y reversible.
- **Conexiones entre subredes**: en arquitecturas multi-tier, las reglas de firewall y las security lists de OCI deben permitir el tráfico UDP/TCP en el puerto 53 hacia el resolver de la VCN.

Un TTL elevado en los registros DNS puede ralentizar el ROLLBACK: reducirlo a 60-300 segundos en las horas previas al cutover es una práctica estándar en los planes de migración de bajo riesgo.
