---
title: "ENUM (MySQL)"
description: "Tipo di dato MySQL che ammette un set predefinito di valori stringa, memorizzato internamente come indice numerico di 1-2 byte."
translationKey: "glossary_mysql_enum"
aka: "MySQL ENUM type"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

L'**ENUM (MySQL)** è un tipo di dato che ammette solo un insieme predefinito di valori stringa, dichiarato al momento della creazione della colonna. È una delle feature caratteristiche di MySQL — pochi altri DBMS mainstream hanno un tipo enumerato nativo.

## Come funziona

Quando dichiari `status ENUM('NEW','ACTIVE','CLOSED')`, MySQL assegna a ciascun valore un indice numerico: 'NEW'=1, 'ACTIVE'=2, 'CLOSED'=3. Sul disco viene memorizzato l'indice intero, non la stringa. La conversione avviene in lettura. Sotto i 256 valori dichiarati ENUM occupa 1 byte per riga; tra 256 e 65535, occupa 2 byte.

## A cosa serve

ENUM offre tre vantaggi concreti: storage compatto (1-2 byte invece di N caratteri di un VARCHAR), vincolo "ammette solo questi valori" dichiarato a livello di schema senza bisogno di CHECK separato, lettura leggibile nelle query (`WHERE status = 'ACTIVE'`) senza JOIN su tabelle di lookup.

## Quando usarlo

È la scelta giusta quando il dominio dei valori è davvero chiuso e stabile nel tempo: giorni della settimana, stati binari o ternari fissi, polarità, tipologie regolamentate da legge. È perfetto anche dentro una lookup table piccola (5-50 righe), dove i suoi limiti diventano irrilevanti.

## Limiti da conoscere

- **Case-insensitive**: `'ACTIVE'` e `'active'` sono lo stesso valore (diverso comportamento rispetto a PostgreSQL)
- **Ordinamento per posizione di dichiarazione**, non alfabetico — un `ORDER BY` può produrre risultati sorprendenti
- **Modificare l'ENUM** (aggiungere un valore in mezzo, rinominare, riordinare) richiede un rebuild della tabella, costoso su tabelle grandi
