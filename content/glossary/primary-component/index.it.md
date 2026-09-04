---
title: "Primary Component (PC)"
description: "Il Primary Component è il sottoinsieme di nodi Galera che detiene il quorum e può accettare scritture, prevenendo lo split-brain."
translationKey: "glossary_primary_component"
aka: "PC, quorum partition"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

In un cluster Galera, non tutti i nodi sono uguali in ogni momento: solo quelli che formano il **Primary Component** hanno il diritto di processare scritture. Il PC è il sottoinsieme di nodi che ha raggiunto il quorum — ovvero la maggioranza dei voti del cluster — e che quindi può continuare a operare in modo sicuro. I nodi esclusi dal PC entrano in stato `non-Primary` e smettono di accettare DML.

## Come funziona

Galera usa un protocollo di membership basato su **wsrep** (Write-Set Replication). Ogni nodo trasmette heartbeat e voti agli altri; quando una partizione di rete o un crash isola un gruppo di nodi, ciascun gruppo calcola se detiene la maggioranza dei voti totali del cluster.

- Il gruppo con **più della metà dei voti** diventa (o rimane) il Primary Component.
- Il gruppo minoritario passa in stato `non-Primary`: le connessioni client ricevono un errore e nessuna scrittura viene accettata.

Questo meccanismo è il presidio principale contro lo **split-brain**: due partizioni non possono entrambe credere di essere il PC e divergere silenziosamente.

## Contesto operativo

Il caso critico è il cluster a **due nodi**: se un nodo cade, il superstite ha esattamente il 50% dei voti e non raggiunge il quorum. Entra in stato `non-Primary` anche se è perfettamente funzionante. La soluzione tipica è aggiungere un terzo nodo (o un arbitro `garbd`) per garantire che un lato possa sempre superare il 50%.

In scenari di manutenzione o bootstrap di emergenza, è possibile forzare manualmente la formazione del PC con:

```sql
SET GLOBAL wsrep_provider_options='pc.bootstrap=YES';
```

Questa operazione va eseguita con cautela: se esiste un'altra partizione attiva con dati più recenti, si rischia di promuovere il nodo sbagliato e perdere transazioni.
