---
title: "Data Catalog"
description: "Inventar centralizat al activelor de date cu metadate, lineage și căutare integrată: face guvernanța accesibilă fără intervenție tehnică."
translationKey: "glossary_data_catalog"
aka: "Catalog de Date Enterprise"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Un Data Catalog este inventarul organizat al tuturor activelor de date disponibile într-o organizație: tabele, view-uri, dataset-uri, rapoarte, API-uri, fișiere. Fiecare activ este însoțit de metadate tehnice și de business, lineage, clasificări de calitate și un glosar comun. Scopul este ca datele să poată fi găsite și înțelese fără a deschide un ticket către echipa tehnică pentru fiecare întrebare.

## Cum funcționează

Catalog-ul colectează metadate din surse eterogene prin conectori (baze de date relaționale, data lake-uri, instrumente BI, pipeline-uri ETL). Pentru fiecare activ expune:

- **metadate tehnice**: schemă, tip de date, cardinalitate, frecvență de actualizare
- **metadate de business**: proprietar, descriere în limbaj natural, etichete de domeniu
- **lineage**: graf care arată de unde provine un dat și unde este consumat
- **data quality score**: metrici agregate calculate de procesele de validare upstream

Utilizatorii caută active prin full-text search sau navigare pe domeniu și etichete. Data steward-ii îmbogățesc intrările cu adnotări și aprobări.

## Când se folosește

Data Catalog devine necesar când numărul surselor depășește capacitatea de documentare manuală — de regulă peste 20-30 dataset-uri active — sau când conformitatea reglementară impune trasabilitate end-to-end (GDPR, HIPAA, SOX). Este și punctul natural de intrare pentru data contract-uri: catalog-ul expune specificațiile unui dataset, iar contractul formalizează garanțiile de calitate și SLA-urile.

Fără catalog, guvernanța rămâne un document Word actualizat rar; cu el, devine un sistem viu interogabil de oricine are acces.
