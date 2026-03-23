---
title: "SCAN Listener"
description: "Single Client Access Name — componente de Oracle RAC que proporciona un unico punto de acceso al cluster, distribuyendo las conexiones entre los nodos disponibles."
translationKey: "glossary_scan_listener"
aka: "Single Client Access Name"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

El **SCAN Listener** (Single Client Access Name) es el componente de Oracle RAC que proporciona un unico nombre DNS para acceder al cluster. Las aplicaciones se conectan al SCAN name sin necesidad de conocer los nodos individuales: el listener distribuye automaticamente las conexiones entre los nodos activos.

## Como funciona

SCAN es un nombre DNS que resuelve a tres direcciones IP virtuales (VIP), distribuidas entre los nodos del cluster. Cuando un cliente se conecta al SCAN name, el DNS devuelve una de las tres IPs, y el listener en esa IP redirige la conexion al nodo mas apropiado segun el servicio solicitado y la carga.

La ventaja es que los connection strings de la aplicacion nunca cambian: si un nodo se anade o elimina del cluster, SCAN gestiona todo de forma transparente.

## Configuracion tipica

Un connection string que usa SCAN:

    jdbc:oracle:thin:@//scan-name.example.com:1521/service_name

Las tres SCAN VIP se ejecutan en cualquier nodo del cluster. En un cluster de dos nodos, un nodo aloja dos VIPs y el otro uno (o viceversa).

## En las migraciones

En las migraciones a OCI, el SCAN listener se reconfigura con el DNS de la nueva infraestructura. Es uno de los pasos del cutover: actualizar los connection strings para apuntar al nuevo SCAN name en OCI. Si el naming esta bien gestionado, es un cambio en un solo punto (el connection pool de la aplicacion), no en decenas de archivos de configuracion dispersos.
