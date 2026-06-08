---
title: "WAL (Write-Ahead Log)"
draft: false
type: glossary
section_hint: postgresql
---

registro sequenziale di tutte le modifiche apportate al database PostgreSQL, scritto prima che le modifiche vengano applicate ai file di dati. È la sorgente da cui la replica logica estrae le operazioni da trasmettere ai subscriber tramite il processo di decodifica logica.
