---
title: "ALTER TYPE ADD VALUE"
description: "Comando PostgreSQL che aggiunge un valore a un ENUM esistente. Operazione di metadata, transazionale, senza rebuild della tabella che usa il tipo."
translationKey: "glossary_postgresql_alter_type_add_value"
aka: "Estensione di ENUM PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`ALTER TYPE ... ADD VALUE` è il comando PostgreSQL che aggiunge un nuovo valore a un tipo enumerativo già esistente. È una delle modifiche DDL più frequenti su un ENUM, ed è una **delle differenze principali** rispetto a MySQL: in PostgreSQL non richiede un rebuild della tabella che usa il tipo.

## Come funziona

Sintassi: `ALTER TYPE nome_tipo ADD VALUE 'nuovo_valore' [BEFORE|AFTER 'altro_valore']`. Senza la clausola posizionale, il nuovo valore va in coda alla lista. Con `BEFORE` o `AFTER`, viene inserito nella posizione specificata, influenzando l'ordinamento usato da `ORDER BY` su quella colonna. È disponibile da PostgreSQL 9.1; il posizionamento `BEFORE`/`AFTER` è arrivato con la 9.6.

## A cosa serve

A estendere il vocabolario di un ENUM senza dover ricreare il tipo. È un'operazione di **solo metadata**: PostgreSQL aggiorna il catalogo `pg_enum` senza toccare le tabelle che usano il tipo, anche se contengono miliardi di righe. Si esegue in millisecondi, dentro una transazione, con la possibilità di rollback se qualcosa va storto nel deploy.

## Quando si usa

È la modifica naturale al ciclo di vita di un ENUM PostgreSQL: nuovo prodotto, nuovo canale, nuova policy di business → un nuovo valore da aggiungere al set. Diversamente da `ADD VALUE`, in PostgreSQL **non esiste un `DROP VALUE` nativo**: rimuovere un valore richiede di ricreare il tipo da zero e migrare le colonne che lo usano. Questa asimmetria è il principale limite operativo del tipo ENUM in PostgreSQL.
