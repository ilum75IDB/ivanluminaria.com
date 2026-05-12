---
title: "Online DDL"
description: "Meccanismo MySQL/InnoDB che permette di eseguire operazioni di ALTER TABLE senza bloccare le scritture concorrenti, con limiti precisi a seconda dell'operazione."
translationKey: "glossary_mysql_online_ddl"
aka: "MySQL Online DDL"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

L'**Online DDL** è il meccanismo di MySQL e dello storage engine InnoDB che permette di eseguire molte operazioni di `ALTER TABLE` senza bloccare le scritture concorrenti sulla tabella. È stato introdotto in MySQL 5.6 e ampliato progressivamente nelle versioni successive.

## Come funziona

MySQL valuta automaticamente l'operazione richiesta e sceglie tra tre algoritmi: `INSTANT` (modifica solo i metadati, frazione di secondo), `INPLACE` (modifica la tabella senza copiarla, supporta DML in parallelo), `COPY` (rebuild completo, blocca le scritture). L'algoritmo usato dipende dal tipo di ALTER e dalla versione di MySQL.

## A cosa serve

Ridurre drasticamente il downtime durante manutenzioni di schema su database in produzione. Operazioni come aggiungere una colonna in fondo, aggiungere un indice, modificare un default sono diventate praticamente istantanee. Operazioni più pesanti (cambio tipo colonna, ricostruzione di un indice primario) richiedono ancora rebuild, ma spesso con concorrenza preservata.

## Quando attenzione

Online DDL non è gratis: anche `INPLACE` genera carico significativo su I/O e replication lag. Su tabelle da centinaia di milioni di righe, anche operazioni "online" possono produrre ore di lag sui replica. Inoltre certe operazioni (es. modificare una colonna ENUM aggiungendo valori in mezzo) cadono ancora in `ALGORITHM=COPY` e bloccano le scritture. Vale sempre la pena specificare esplicitamente `ALGORITHM=INPLACE, LOCK=NONE` per essere sicuri del comportamento, e testare prima su una replica.
