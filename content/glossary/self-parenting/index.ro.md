---
title: "Self-parenting"
description: "Tehnică de echilibrare a ierarhiilor dezechilibrate: cine nu are un părinte devine propriul părinte."
translationKey: "glossary_self_parenting"
aka: "Auto-referință ierarhică"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

**Self-parenting-ul** este o tehnică de dimensional modeling folosită pentru a echilibra ierarhiile dezechilibrate (ragged hierarchies). Principiul este simplu: o entitate care nu are un nivel ierarhic superior devine propriul părinte la acel nivel.

## Cum funcționează

Într-o ierarhie cu trei niveluri Top Group → Group → Client:

- Un Client fără Group folosește propriul nume/ID ca Group
- Un Group fără Top Group folosește propriul nume/ID ca Top Group

Rezultatul este o tabelă dimensională fără NULL-uri în coloanele ierarhice, cu toate nivelurile întotdeauna populate.

## Flag-urile de distincție

Pentru a nu pierde informația despre care entități au fost echilibrate artificial, se adaugă flag-uri dimensiunii:

- `is_direct_client = 'Y'`: clientul nu avea un Group în sursă
- `is_standalone_group = 'Y'`: Group-ul nu avea un Top Group în sursă

Aceste flag-uri permit business-ului să filtreze "adevăratele" top group-uri de clienții promovați.

## De ce în ETL, nu în raport

Self-parenting-ul se aplică o dată în ETL, nu în fiecare raport individual. Un raport ar trebui să facă GROUP BY și JOIN, nu să decidă cum să gestioneze nivelurile lipsă. Dacă logica de echilibrare este în model, toate rapoartele beneficiază automat.
