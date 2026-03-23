---
title: "BYOL"
description: "Bring Your Own License — programma Oracle che permette di riutilizzare le licenze on-premises nel cloud OCI senza costi aggiuntivi di licensing."
translationKey: "glossary_byol"
aka: "Bring Your Own License"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**BYOL** (Bring Your Own License) è un programma Oracle che consente alle aziende di trasferire le licenze software acquistate per l'infrastruttura on-premises verso Oracle Cloud Infrastructure (OCI), senza dover acquistare nuove licenze cloud.

## Come funziona

Quando un'azienda ha già licenze Oracle — tipicamente Enterprise Edition con opzioni come RAC, Data Guard o Partitioning — può "portarle con sé" nella migrazione a OCI. Il contratto di supporto (Software Update License & Support) viene mantenuto, e le licenze vengono associate alle risorse cloud invece che ai server fisici.

Su OCI, ogni OCPU corrisponde a un processor license, con un rapporto 1:1 trasparente. Questo rende il calcolo prevedibile e conforme alle policy di licensing Oracle.

## Perché è importante nelle migrazioni

Il BYOL è spesso il fattore decisivo nella scelta di OCI rispetto ad altri cloud provider. Su AWS o Azure, Oracle applica regole di licensing diverse: ogni vCPU conta come mezzo processore, e le opzioni come RAC non sono supportate o richiedono licenze aggiuntive. Un audit Oracle su un cloud non-OCI può trasformare un apparente risparmio in un costo imprevisto molto significativo.

## Cosa copre

- Oracle Database (tutte le edizioni)
- Opzioni del database (RAC, Data Guard, Partitioning, Advanced Compression, ecc.)
- Oracle Middleware e altri prodotti Oracle con licenze idonee

Il BYOL non è automatico: va richiesto e configurato al momento del provisioning delle risorse OCI, specificando le licenze esistenti nel contratto.
