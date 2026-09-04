---
title: "Primary Component (PC)"
description: "El Primary Component es el subconjunto de nodos Galera que posee el quórum y puede aceptar escrituras, evitando situaciones de split-brain."
translationKey: "glossary_primary_component"
aka: "PC, partición de quórum"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

En un clúster Galera, no todos los nodos son equivalentes en todo momento: solo los que forman el **Primary Component** tienen derecho a procesar escrituras. El PC es el subconjunto de nodos que ha alcanzado el quórum — es decir, la mayoría de los votos totales del clúster — y que por tanto puede operar de forma segura. Los nodos excluidos del PC pasan al estado `non-Primary` y dejan de aceptar sentencias DML.

## Cómo funciona

Galera utiliza un protocolo de membresía basado en **wsrep** (Write-Set Replication). Cada nodo intercambia heartbeats y votos con el resto. Cuando una partición de red o un fallo aísla a un grupo de nodos, cada grupo calcula de forma independiente si posee más de la mitad de los votos totales del clúster.

- El grupo con **más de la mitad de los votos** se convierte (o permanece) en el Primary Component.
- El grupo minoritario pasa al estado `non-Primary`: las conexiones de los clientes reciben un error y no se acepta ninguna escritura.

Este mecanismo es la principal protección contra el **split-brain**: dos particiones no pueden creer simultáneamente que son el PC y divergir de forma silenciosa.

## Contexto operativo

El caso más crítico es el clúster de **dos nodos**: si uno cae, el superviviente tiene exactamente el 50% de los votos y no alcanza el quórum. Entra en estado `non-Primary` aunque esté completamente operativo. La solución habitual es añadir un tercer nodo o un árbitro ligero (`garbd`) para garantizar que un lado siempre pueda superar el 50%.

En escenarios de mantenimiento o bootstrap de emergencia, es posible forzar manualmente la formación del PC:

```sql
SET GLOBAL wsrep_provider_options='pc.bootstrap=YES';
```

Esta operación debe ejecutarse con precaución: si existe otra partición activa con datos más recientes, promover el nodo equivocado puede provocar la pérdida de transacciones ya confirmadas.
