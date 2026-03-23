---
title: "Cutover"
description: "Momento critico de una migracion en el que el sistema de produccion se traslada definitivamente de la vieja a la nueva infraestructura."
translationKey: "glossary_cutover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

El **cutover** es el momento en que un sistema de produccion se traslada de la vieja infraestructura a la nueva. Es la fase mas visible de una migracion — la que todos recuerdan, para bien o para mal.

## Anatomia de un cutover

Un cutover bien planificado sigue un runbook detallado con pasos numerados, tiempos estimados, criterios de exito y procedimientos de rollback para cada paso. Los componentes tipicos:

1. **Stop aplicativo** — cierre de conexiones y verificacion de que ninguna sesion esta activa
2. **Sincronizacion final** — en una migracion Data Guard, verificacion de que transport lag y apply lag estan a cero
3. **Switchover/migracion** — la operacion tecnica que transfiere el servicio
4. **Validacion** — pruebas de conectividad, consultas de verificacion, pruebas funcionales
5. **Apertura gradual** — readmision progresiva de los usuarios

## Downtime y ventanas

El downtime de un cutover es el tiempo entre la desconexion del ultimo usuario y la reconexion del primero. Con Data Guard switchover, el downtime puede ser del orden de minutos. Con Data Pump, puede ser de horas o dias.

La ventana de cutover se planifica en los momentos de menor utilizacion: noches, fines de semana, festivos. Pero "menor utilizacion" no significa "cero utilizacion" — en empresas manufactureras con turnos 24/7, no existe un momento en que la base de datos no la necesite nadie.

## Rollback

Todo cutover debe tener un plan de rollback. Con Data Guard, el rollback es un segundo switchover — relativamente sencillo. Con Data Pump, el rollback significa reiniciar la base de datos original y aceptar la perdida de las transacciones ocurridas despues del inicio de la migracion. La calidad del plan de rollback es inversamente proporcional a la probabilidad de necesitarlo — pero cuidado con no tenerlo.
