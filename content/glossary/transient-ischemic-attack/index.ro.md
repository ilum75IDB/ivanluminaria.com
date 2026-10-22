---
title: "Transient Ischemic Attack"
description: "Un TIA (Transient Ischemic Attack) este o defecțiune scurtă și aparent auto-rezolvată care semnalează o problemă structurală nerezolvată în sistem."
translationKey: "glossary_transient_ischemic_attack"
aka: "TIA, mini-AVC (metaforă de sisteme)"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

În medicină, un Transient Ischemic Attack (TIA) este un episod neurologic tranzitoriu care se rezolvă spontan în mai puțin de 24 de ore, fără a lăsa leziuni permanente detectabile. În managementul proiectelor IT și operațiunile de sisteme, termenul este folosit ca metaforă pentru defecțiunile scurte și aparent auto-rezolvate care semnalează de fapt o problemă structurală nerezolvată.

## Mecanismul metaforei

Așa cum un TIA clinic precede adesea un accident vascular cerebral complet, un „TIA de sistem" — un crash rezolvat printr-un restart, un timeout dispărut de la sine, un vârf de latență care s-a calmat fără intervenție — este un semnal de avertizare, nu o rezolvare. Sistemul și-a revenit, dar cauza rădăcină este încă prezentă. A închide episodul pentru că „s-a rezolvat singur" este exact raționamentul care transformă un avertisment într-un incident major.

## Context operațional

În proiectele IT, TIA-urile apar ca:

- reporniri nocturne ale aplicațiilor care „rezolvă totul" fără ca nimeni să știe de ce
- interogări lente care revin la viteză normală după repornirea connection pool-ului
- erori intermitente în cozile de mesaje care dispar înainte ca cineva să deschidă un ticket

Răspunsul corect nu este să celebrezi recuperarea, ci să deschizi o analiză post-mortem chiar și atunci când sistemul a revenit la funcționare normală. Un TIA nediagnosticat este datorie tehnică cu dată de expirare necunoscută.

## Note

Termenul este deliberat provocator: folosirea lui într-o retrospectivă sau într-un raport de incident ajută echipa să mute focusul de la „e din nou sus" la „de ce a căzut".
