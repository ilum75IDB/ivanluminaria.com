---
title: "OID (Object Identifier)"
description: "Identificatore numerico interno usato da PostgreSQL per riferirsi a oggetti di sistema (tabelle, tipi, funzioni). Numero intero non firmato a 4 byte."
translationKey: "glossary_postgresql_oid"
aka: "PostgreSQL OID, Object Identifier"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

L'**OID** (Object Identifier) è un identificatore numerico interno che PostgreSQL usa per riferirsi a oggetti di sistema, come tabelle, tipi di dato, funzioni, schemi, ruoli. È un intero non firmato a 4 byte gestito da PostgreSQL stesso, distinto dalle chiavi primarie delle tabelle utente.

## Come funziona

Ogni oggetto del catalogo di sistema (es. `pg_class` per tabelle, `pg_type` per tipi, `pg_enum` per valori ENUM) ha una colonna `oid` che funge da identificatore univoco. Gli OID vengono assegnati automaticamente dal motore e usati come chiavi nei JOIN tra cataloghi di sistema. PostgreSQL espone diverse funzioni di conversione (`oid::regclass`, `oid::regtype`, ecc.) per ricavare il nome leggibile di un oggetto dal suo OID.

## A cosa serve

A identificare ogni singolo oggetto del database in modo univoco e stabile attraverso il dump-restore. Per i tipi ENUM, ogni valore dichiarato in `CREATE TYPE ... AS ENUM` riceve un OID, che viene salvato nelle righe della tabella che usa il tipo. Questo permette di memorizzare il valore in soli 4 byte mantenendo allo stesso tempo il legame con il nome leggibile e l'ordinamento posizionale.

## Quando si usa

Raramente in modo diretto nelle applicazioni — l'OID è un dettaglio implementativo che la maggior parte delle query non vede. Diventa rilevante quando si analizzano i cataloghi di sistema (`information_schema`, `pg_catalog`), quando si scrivono strumenti di introspection o monitoring, e quando si debugga il comportamento di tipi complessi come gli ENUM o i domini.
