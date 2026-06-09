---
title: "WAL"
description: "Write-Ahead Log — registru secvențial al tuturor modificărilor unei baze de date PostgreSQL, scris înaintea fișierelor de date. Baza durability-ului, crash recovery-ului, replicării fizice și logice."
translationKey: "glossary_wal"
aka: "Write-Ahead Log"
articles:
  - "/posts/postgresql/replica-logica-in-postgresql-scenari-d-uso-configurazione-e-monitoraggio"
---

**WAL** (Write-Ahead Log) este registrul secvențial al tuturor modificărilor aduse bazei de date PostgreSQL: fiecare INSERT, UPDATE, DELETE, DDL este scris aici **înainte** ca modificările să fie aplicate pe fișierele de date propriu-zise. Este fundamentul durability-ului, crash recovery-ului, replicării fizice și replicării logice.

## De ce "Write-Ahead"

Regula este: o tranzacție este considerată committed doar atunci când înregistrarea WAL corespunzătoare a fost `fsync`-ată pe disc. Chiar dacă serverul crash-uiește imediat după, fișierul de date poate fi reconstruit replicând înregistrările WAL din ultimul checkpoint. Această garanție îi permite lui PostgreSQL să tolereze crash-uri bruște fără corupere a bazei de date.

## Structură pe disc

Înregistrările WAL sunt grupate în **segmente** de 16 MB implicit (configurabil prin `wal_segment_size`) în directorul `pg_wal/`. Fiecare segment are un nume hexazecimal de 24 de caractere (de exemplu `000000010000000000000042`) care codifică timeline + offset LSN — **Log Sequence Number**-ul, identificatorul monoton de poziție în WAL.

## Replicare logică și WAL

Replicarea logică PostgreSQL **decodifică** înregistrările WAL (inițial în format fizic) în modificări logice rând cu rând (INSERT/UPDATE/DELETE cu valorile coloanelor) prin plugin-ul `pgoutput`. Acest pas de "logical decoding" este cel care le permite subscriber-ilor să aplice modificările pe tabele chiar cu layout fizic diferit (de exemplu PostgreSQL 13 → 15 cu tablespace schimbat). Fără WAL nu există replicare.
