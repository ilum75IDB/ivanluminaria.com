---
aka: State Snapshot Transfer
articles:
- /posts/mysql/galera-cluster-3-nodi
- /posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu
description: State Snapshot Transfer — meccanismo di Galera Cluster per trasferire
  una copia completa dei dati a un nodo che si unisce al cluster.
title: SST
translationKey: glossary_sst
---

**SST** (State Snapshot Transfer) è il meccanismo con cui un nodo Galera che si unisce al cluster (o che è rimasto offline troppo a lungo) riceve una copia completa dell'intero dataset da un nodo donatore.

## Come funziona

Quando un nodo si unisce al cluster e il gap di transazioni mancanti supera la dimensione del gcache, il cluster avvia un SST. Il nodo donatore crea un'istantanea completa del database e la trasferisce al nodo ricevente. I metodi disponibili sono: `mariabackup` (non blocca il donatore), `rsync` (veloce ma blocca il donatore in lettura), e `mysqldump` (lento e bloccante).

## A cosa serve

SST è essenziale per due scenari: l'aggiunta di un nuovo nodo al cluster (primo join) e il recupero di un nodo che è rimasto offline così a lungo che le transazioni mancanti non sono più disponibili nel gcache del donatore.

## Quando si usa

SST viene attivato automaticamente da Galera quando necessario. La scelta del metodo SST (`wsrep_sst_method`) va fatta in fase di configurazione. In produzione, `mariabackup` è la scelta raccomandata perché non blocca il nodo donatore, evitando di degradare il cluster durante il trasferimento.
