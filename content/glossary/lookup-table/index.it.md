---
title: "Lookup table"
description: "Tabella di riferimento collegata via foreign key che memorizza i valori validi di un'enumerazione, insieme ad eventuali attributi descrittivi."
translationKey: "glossary_lookup_table"
aka: "Tabella di lookup, reference table"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

La **lookup table** è una tabella di riferimento che memorizza i valori validi di un dominio enumerato, collegata alle tabelle che la usano tramite una foreign key. È la via "database-puro" per modellare un'enumerazione, alternativa a tipi nativi come ENUM o a CHECK constraint.

## Come è fatta

Lo schema canonico include almeno tre colonne: un `id` surrogato (tipicamente `SMALLINT` o `TINYINT`) come primary key, un `codice` testuale (la chiave naturale, spesso univoca), e una `descrizione` estesa. Spesso si aggiungono attributi come `ordine` per il sort visuale, `attivo` per il soft-delete, e timestamp di audit.

## A cosa serve

Il vantaggio principale rispetto ad ENUM è la flessibilità: rinominare una descrizione è una `UPDATE` su una riga, niente migration né rebuild della tabella che la referenzia. Si possono aggiungere attributi (etichette localizzate, ordine, flag) senza toccare lo schema delle tabelle figlie. È adatta quando i valori cambiano nel tempo o quando servono metadati associati.

## Quando si usa

È la scelta giusta quando:
- I valori vengono modificati con una certa frequenza (aggiunta, rinomina, disattivazione)
- Servono attributi aggiuntivi (traduzioni, ordine, flag)
- Si vogliono gestire i valori a runtime senza DDL (pannelli admin)
- Il numero di valori cresce nel tempo, oltre i 20-30

Il prezzo da pagare è il JOIN necessario nelle query, che però si ottimizza facilmente con indici composti e view dedicate.
