---
title: "RMAN"
description: "Recovery Manager — herramienta Oracle para backup, restore y recovery de la base de datos, incluyendo la creacion de bases de datos standby para Data Guard."
translationKey: "glossary_rman"
aka: "Recovery Manager"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RMAN** (Recovery Manager) es la herramienta nativa de Oracle para el backup, restore y recovery de la base de datos. Es una utilidad de linea de comandos que gestiona todas las operaciones de proteccion de datos de forma integrada con la base de datos.

## Que hace

- **Backup**: completos, incrementales, solo de archived logs
- **Restore**: recuperacion de datafiles, tablespaces o de toda la base de datos
- **Recovery**: aplicacion de redo logs para llevar la base de datos a un punto en el tiempo especifico
- **Duplicate**: creacion de copias de la base de datos, incluyendo bases de datos standby para Data Guard

## RMAN y Data Guard

Para la creacion de una base de datos standby, RMAN permite el `DUPLICATE ... FOR STANDBY FROM ACTIVE DATABASE` — una copia directa por red del primario al standby, sin necesidad de backups intermedios en cinta o disco. El comando transfiere todos los datafiles y controlfiles y los configura automaticamente para la replica.

## Por que RMAN y no copias manuales

RMAN conoce la estructura interna de la base de datos Oracle: sabe que bloques han cambiado (para los incrementales), que archivos se necesitan, como aplicar los redo. Una copia manual de archivos (con `cp` o `rsync`) no garantiza la consistencia y requiere que la base de datos este cerrada. RMAN puede trabajar con la base de datos abierta, con impacto minimo en el rendimiento.
