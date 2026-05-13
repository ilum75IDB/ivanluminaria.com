---
title: "CREATE TYPE AS ENUM"
description: "Statement DDL di PostgreSQL che crea un tipo enumerativo come oggetto di prima classe, riutilizzabile su più colonne e modificabile con ALTER TYPE."
translationKey: "glossary_postgresql_create_type_enum"
aka: "PostgreSQL ENUM type, tipo enumerativo PostgreSQL"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

`CREATE TYPE ... AS ENUM` è lo statement DDL di PostgreSQL che dichiara un tipo enumerativo, ovvero un dominio chiuso di valori testuali ammessi. A differenza di MySQL, in PostgreSQL l'ENUM è un **tipo di dato a sé stante**, non una decorazione di una colonna `VARCHAR`.

## Come è fatto

La sintassi base è `CREATE TYPE nome_tipo AS ENUM ('valore1','valore2',...)`. Una volta creato, il tipo può essere usato come tipo di una o più colonne (`stato stato_abbonamento`), come tipo di parametro di funzioni e procedure, e nelle dichiarazioni di indici parziali. Internamente PostgreSQL memorizza ciascun valore come un OID di 4 byte, mantenendo l'ordinamento posizionale dichiarato al `CREATE TYPE`.

## A cosa serve

A imporre, a livello di schema, l'appartenenza di un valore a un insieme chiuso. È più rigoroso di un `CHECK` constraint perché definisce un **tipo** — quindi il vincolo viaggia con la colonna anche attraverso funzioni, view, e parametri di procedura. Le query con `WHERE stato = 'ATTIVO'` sono leggibili e veloci, senza bisogno di JOIN con tabelle di lookup.

## Quando si usa

È la scelta giusta quando il set di valori è **stabile nel tempo** (giorni della settimana, stati binari, polarità tecniche) e la semantica deve essere controllata dallo schema. Sconsigliato quando il vocabolario evolve frequentemente o servono attributi extra (etichette localizzate, ordine di display, flag), perché PostgreSQL non offre `ALTER TYPE DROP VALUE` nativo: rimuovere un valore richiede ricreazione del tipo e migrazione delle colonne.
