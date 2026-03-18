---
title: "Redo Log"
description: "Archivos de log donde Oracle registra cada modificacion de datos antes de escribirla en los datafiles, garantizando la recuperacion en caso de fallo."
translationKey: "glossary_redo_log"
aka: "Online Redo Log, Archived Redo Log"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**Redo Log** es el mecanismo con el que Oracle registra cada modificacion de datos (INSERT, UPDATE, DELETE, DDL) antes de que se escriba definitivamente en los datafiles. Es la garantia fundamental de durabilidad de las transacciones.

## Como funciona

Oracle escribe las modificaciones en los redo log online de forma secuencial y continua. Los redo log estan organizados en grupos circulares: cuando un grupo se llena, Oracle pasa al siguiente. Cuando todos los grupos han sido utilizados, Oracle vuelve al primero (log switch).

## Online vs Archived

- **Online redo log**: los archivos activos donde Oracle escribe en tiempo real. Son circulares y se sobreescriben
- **Archived redo log**: copias de los redo log online guardadas antes de la sobreescritura. Necesarios para la recuperacion point-in-time y para Data Guard

El modo `ARCHIVELOG` de la base de datos activa la creacion automatica de los archived log. Sin el, los redo se sobreescriben y la recuperacion se limita al ultimo backup completo.

## Por que son importantes

Los redo log son el corazon de la recuperacion y la replica en Oracle. Sin redo:

- No es posible la recuperacion tras un crash (instance recovery)
- No es posible la recuperacion point-in-time (media recovery)
- Data Guard no puede funcionar (la replica se basa enteramente en los redo)
- No es posible el flashback database
