---
title: "Ragged hierarchy"
description: "Ierarhie în care nu toate ramurile ating aceeași adâncime: unele niveluri intermediare lipsesc."
translationKey: "glossary_ragged_hierarchy"
aka: "Ierarhie dezechilibrată, Unbalanced hierarchy"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

O **ragged hierarchy** (ierarhie dezechilibrată) este o structură ierarhică în care nu toate ramurile ating aceeași adâncime. Unele niveluri intermediare lipsesc pentru anumite entități.

## Exemplu concret

Într-o ierarhie cu trei niveluri Top Group → Group → Client:

- Unii clienți au toate cele trei niveluri (ierarhie completă)
- Unii clienți au un Group dar niciun Top Group
- Unii clienți nu au nici Group nici Top Group (clienți direcți)

Rezultatul este o structură cu "goluri" care cauzează probleme în rapoartele de agregare: linii cu NULL, totaluri împărțite, drill-down-uri incomplete.

## De ce este o problemă în DWH

Instrumentele de BI și interogările SQL se așteaptă la ierarhii complete pentru a funcționa corect. Un GROUP BY pe o coloană cu NULL-uri produce rezultate neașteptate: liniile cu NULL sunt grupate separat, totalurile nu se potrivesc, iar același grup poate apărea pe mai multe linii.

## Cum se rezolvă

Tehnica standard este **self-parenting-ul**: o entitate fără părinte devine propriul părinte. Aceasta echilibrează ierarhia în amonte, în ETL, eliminând NULL-urile din tabela dimensională. Flag-uri suplimentare (`is_direct_client`, `is_standalone_group`) permit distingerea entităților echilibrate artificial de cele cu ierarhie naturală.
