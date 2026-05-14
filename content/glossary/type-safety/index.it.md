---
title: "Type safety"
description: "Proprietà di un sistema di tipi che impedisce, a parse-time, l'uso di valori incompatibili con il tipo dichiarato di colonna, parametro o variabile."
translationKey: "glossary_type_safety"
aka: "Sicurezza dei tipi, type checking"
articles:
  - "/posts/postgresql/enum-postgresql-paga-o-pesa"
---

La **type safety** è la proprietà di un sistema di tipi che impedisce, a parse-time o compile-time, l'uso di valori non compatibili con il tipo dichiarato. In ambito database significa che il motore rifiuta operazioni che violano i vincoli di tipo, prima ancora di eseguire la query.

## Come funziona

Quando una colonna, un parametro di funzione o una variabile sono dichiarati con un tipo specifico (es. `INTEGER`, un domain custom, un ENUM), il motore verifica al momento del parse che ogni valore assegnato o confrontato sia compatibile. Operazioni che mescolano tipi incompatibili senza un cast esplicito generano un errore prima dell'esecuzione, evitando bug che si manifesterebbero solo a runtime.

## A cosa serve

A spostare la rilevazione degli errori dal runtime al parse-time, riducendo il rischio di dati corrotti o inconsistenti in produzione. In PostgreSQL, ad esempio, un ENUM è un tipo a sé stante: una funzione che accetta un `stato_abbonamento` non potrà mai essere chiamata con una stringa libera. In MySQL, dove l'ENUM è una decorazione di una colonna `VARCHAR`, questa garanzia non esiste — il vincolo c'è solo sulla colonna, non sul tipo.

## Quando si usa

È utile in tutti i sistemi dove l'integrità semantica dei dati conta più della comodità di scrittura: billing, finanza, anagrafiche, qualunque dominio in cui un valore "fuori dominio" rappresenta un errore di business e non una variante accettabile. La type safety end-to-end è uno dei tratti distintivi di PostgreSQL e uno dei motivi per cui viene scelto in contesti enterprise.
