---
title: "wsrep_cluster_size"
description: "Variabile di stato Galera che indica il numero di nodi attivi nel cluster. Scendere sotto il quorum blocca le scritture su tutti i nodi superstiti."
translationKey: "glossary_wsrep_cluster_size"
aka: "Galera cluster size status variable"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

`wsrep_cluster_size` è una variabile di stato esposta dal plugin wsrep (Galera) che riporta quanti nodi sono attualmente connessi e sincronizzati nel cluster. Non è un parametro di configurazione: il suo valore è dinamico e cambia in tempo reale al variare della topologia.

## Come funziona

Il valore si legge con una semplice query:

```sql
SHOW STATUS LIKE 'wsrep_cluster_size';
```

In un cluster a 3 nodi correttamente operativo il risultato atteso è `3`. Galera calcola il quorum con la formula `⌊N/2⌋ + 1`: su 3 nodi il quorum minimo è 2. Se `wsrep_cluster_size` scende a `1`, il nodo superstite non raggiunge il quorum, imposta `wsrep_cluster_status` a `non-Primary` e rifiuta le scritture per evitare split-brain.

## Contesto operativo

Monitorare `wsrep_cluster_size` è il primo controllo da eseguire quando un'applicazione segnala errori di scrittura su un cluster Galera. Un valore inferiore al totale dei nodi attesi non indica necessariamente un'interruzione critica: due nodi su tre mantengono il quorum e il cluster rimane in stato `Primary`. Il problema sorge quando si perde la maggioranza.

Nei cluster a 2 nodi (configurazione sconsigliata in produzione) qualsiasi perdita di un nodo porta `wsrep_cluster_size` a `1` e blocca immediatamente le scritture, rendendo necessario un bootstrap manuale o l'uso di un nodo arbitro (garbd).

## Note

`wsrep_cluster_size` descrive la dimensione della vista corrente del cluster (Primary Component), non il numero totale di nodi configurati. Un nodo in stato `Donor/Desynced` o `Joiner` può temporaneamente non comparire nel conteggio o abbassarlo durante un SST/IST.
