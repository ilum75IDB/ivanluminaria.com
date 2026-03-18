---
title: "OLAP"
description: "Online Analytical Processing — procesare orientată spre analiza multidimensională a datelor, tipică pentru data warehouse-uri."
translationKey: "glossary_olap"
aka: "Online Analytical Processing"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**OLAP** (Online Analytical Processing) indică o abordare a procesării datelor orientată spre analiza multidimensională: agregări, drill-down, comparații temporale, slice-and-dice pe volume mari de date istorice.

## OLAP vs OLTP

| Caracteristică | OLAP | OLTP |
|----------------|------|------|
| Scop | Analiză și raportare | Tranzacții operative |
| Model de date | Star schema, denormalizat | 3NF, normalizat |
| Interogare tipică | Agregări pe milioane de linii | Citire/scriere a câtorva linii |
| Utilizatori | Analiști, management | Aplicații, operatori |
| Actualizare | Batch (ETL periodic) | Timp real |

## Operațiuni OLAP

Operațiunile fundamentale ale analizei OLAP sunt:

- **Drill-down**: de la nivelul agregat la detaliu
- **Drill-up** (roll-up): de la detaliu la nivelul agregat
- **Slice**: selectarea unei "felii" de date fixând o dimensiune (ex. doar anul 2025)
- **Dice**: selectarea unui sub-cub specificând mai multe dimensiuni
- **Pivot**: rotirea dimensiunilor de analiză (linii ↔ coloane)

## Implementări

- **ROLAP** (Relational OLAP): datele rămân în tabele relaționale, agregările sunt calculate cu interogări SQL. Este abordarea folosită în data warehouse-uri cu star schema
- **MOLAP** (Multidimensional OLAP): datele sunt pre-agregate în structuri multidimensionale (cuburi). Mai rapid pentru interogări dar necesită mai mult spațiu și timp de construire
- **HOLAP** (Hybrid): combinație a ambelor abordări
