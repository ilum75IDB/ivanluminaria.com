---
title: "Bus Factor"
description: "Numărul de persoane din echipă care, dacă ar lipsi simultan, ar bloca proiectul. Măsoară concentrarea cunoașterii critice în puține capete."
translationKey: "glossary_bus_factor"
aka: "Truck Factor, Lottery Factor"
articles:
  - "/posts/project-management/team-di-progetto-che-reggono"
---

**Bus Factor** (cunoscut și ca Truck Factor sau Lottery Factor) este o metrică empirică ce răspunde la întrebarea: *"Câte persoane din echipă trebuie să lipsească simultan ca proiectul să se oprească?"*. Numele, puțin macabru, vine de la scenariul ipotetic al colegului lovit de un autobuz — dar se aplică la fel de bine la concedii prelungite, îmbolnăviri, demisii, transferuri.

## Cum se calculează

Nu există o formulă matematică exactă, ci o estimare rațională care pleacă de la câteva întrebări:

- Cine este singura persoană care știe să configureze cluster-ul de producție?
- Cine este singura persoană care cunoaște domeniul funcțional al unei anumite zone?
- Cine a scris bucata de cod cea mai critică fără să o documenteze?
- Cine ține relația cu un stakeholder cheie de la client?

Dacă răspunsul la fiecare întrebare este "o singură persoană", bus factor-ul este 1 pe acea competență. Bus factor-ul echipei este minimul dintre toate bus factor-urile competențelor critice individuale.

## Valori tipice

- **Bus factor = 1**: risc critic. O singură persoană deține cunoaștere ce ar bloca proiectul. Frecvent în echipe mici sau în activități "de guru".
- **Bus factor = 2**: fragil. Acoperit dacă o persoană lipsește, dar dacă lipsesc amândouă proiectul se oprește.
- **Bus factor ≥ 3**: rezilient. Cunoașterea este distribuită suficient pentru a absorbi absențe multiple.

Ținta pragmatică în proiectele reale este menținerea bus factor-ului ≥ 3 pe competențele cu adevărat critice, acceptând valori mai mici pe zone mai periferice.

## Cum se ridică bus factor-ul

Patru instrumente, toate cu cost mic dar care cer timp de calendar:

- **Documentație minimă**: nu enciclopedii, ci runbook-uri operaționale de 2-5 pagini pe procedurile critice
- **Pair working**: două persoane pe aceeași activitate, alternând între "mâinile pe tastatură" și "observă și întreabă"
- **Rotație**: cine a făcut mereu X trece luna asta la Y, și invers. Chiar și doar pentru o săptămână
- **Knowledge transfer recurent**: 30 de minute în agendă în fiecare săptămână pe o temă specifică, înregistrate

## Semnale că bus factor-ul este scăzut

- Când o persoană pleacă în concediu, echipa încetinește vizibil
- Unele activități sunt asignate sistematic aceleiași persoane
- O procedură critică nu a fost niciodată documentată
- Lead-ul este singurul care știe "de ce"-ul anumitor alegeri arhitecturale
