---
title: "gcache"
description: "Buffer circolare su disco usato da Galera Cluster per conservare i writeset recenti e favorire IST rispetto a SST nei riavvii brevi."
translationKey: "glossary_gcache"
aka: "Galera Cache"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

Il gcache è un buffer circolare su disco che ogni nodo di un Galera Cluster mantiene localmente. Contiene i writeset replicati di recente e rappresenta la memoria operativa del processo di sincronizzazione incrementale tra nodi.

## Come funziona

Quando un nodo rientra nel cluster dopo un'assenza breve, Galera verifica se i writeset mancanti sono ancora presenti nel gcache del nodo donatore. Se lo sono, viene eseguita una **Incremental State Transfer (IST)**: il donatore invia solo i writeset mancanti, senza copiare l'intero dataset. Se invece il gcache non copre il gap, si ricade in una **State Snapshot Transfer (SST)**, operazione molto più costosa che trasferisce una snapshot completa del database.

Il parametro chiave è `gcache.size`, configurabile in `wsrep_provider_options`:

```ini
wsrep_provider_options = "gcache.size=2G"
```

Il valore predefinito è 128 MB, spesso insufficiente in ambienti con alto volume di scritture.

## Contesto operativo

Dimensionare correttamente il gcache è la principale leva per evitare SST indesiderate. La regola pratica è stimare il volume di writeset prodotto nel periodo di downtime atteso (manutenzione, riavvio, rete instabile) e impostare `gcache.size` a un valore superiore. Un gcache troppo piccolo forza SST anche per assenze di pochi minuti; uno troppo grande occupa spazio su disco senza benefici proporzionali.

Il file fisico del gcache si trova di default in `<datadir>/galera.cache` e la sua dimensione su disco corrisponde esattamente al valore configurato, allocato in anticipo.
