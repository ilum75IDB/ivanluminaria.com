---
title: "SQL*Net roundtrips to/from client"
description: "Estadística de sesión Oracle que cuenta los intercambios de red entre cliente y base de datos. Valores altos indican una aplicación chatty penalizada por latencia WAN."
translationKey: "glossary_sql_net_roundtrips_to_from_client"
aka: "SQL*Net message roundtrips"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

`SQL*Net roundtrips to/from client` es una estadística de sesión Oracle que cuenta cuántas veces el cliente y la base de datos intercambian un mensaje de red completo durante una sesión. No mide bytes transferidos, sino el número de ciclos petición/respuesta sobre el canal SQL*Net. Cada FETCH, cada llamada a procedimiento remoto y cada respuesta del servidor incrementa el contador.

## Cómo funciona

Oracle expone el valor a través de `V$SESSTAT` (o `V$MYSTAT` para la sesión actual), unida a `V$STATNAME`:

```sql
SELECT s.value AS roundtrips
FROM   v$mystat s
JOIN   v$statname n ON n.statistic# = s.statistic#
WHERE  n.name = 'SQL*Net roundtrips to/from client';
```

Cada ciclo petición/respuesta entre la capa de aplicación y el listener Oracle cuenta como un roundtrip. Con un `arraysize` bajo o recuperación fila a fila, los roundtrips crecen linealmente con el número de filas devueltas. Aumentar `arraysize` — o usar `BULK COLLECT` en el lado PL/SQL — reduce los roundtrips al empaquetar más filas en cada mensaje.

## Contexto operativo

La estadística se vuelve crítica cuando la base de datos se alcanza a través de una WAN o VPN cloud, donde cada roundtrip añade decenas de milisegundos. Una aplicación que realiza 10 000 roundtrips sobre una LAN de 0,1 ms acumula aproximadamente 1 segundo de latencia; sobre una WAN de 30 ms, la misma carga de trabajo acumula cerca de 5 minutos. Este es el perfil típico de un lift-and-shift no optimizado: las consultas son idénticas, pero el tiempo de respuesta percibido se desploma.

La relación entre `SQL*Net roundtrips` y el número de filas procesadas (u operaciones COMMIT) es el indicador clave. Una aplicación bien diseñada mantiene este ratio bajo mediante fetch en lote, connection pooling y eliminación de llamadas remotas innecesarias.
