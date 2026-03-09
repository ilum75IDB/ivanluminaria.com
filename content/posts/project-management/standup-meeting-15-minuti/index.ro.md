---
title: "Standup meeting: de ce funcționează doar dacă durează 15 minute"
description: "Un standup care începe bine și în trei săptămâni devine o ședință de 45 de minute. Cum să impui constrângerea de 15 minute și de ce este singurul lucru care face ca daily meeting-ul să funcționeze cu adevărat."
date: "2026-01-27T10:00:00+01:00"
draft: false
translationKey: "standup_meeting_15_minuti"
tags: ["standup", "agile", "meeting", "team-management", "scrum"]
categories: ["Project Management"]
image: "standup-meeting.cover.jpg"
---

Prima zi de luni a proiectului. Echipă nouă, metodologie nouă, speranțe noi. PM-ul propune standup-ul zilnic. Toți dau din cap. "Cincisprezece minute, în picioare, trei întrebări. Simplu."

Prima săptămână funcționează. La 9:15 începe, la 9:28 ești deja la birou. Fiecare spune ce are de spus în două minute, se semnalează blocajele, se salută. Eficiență pură.

A doua săptămână cineva ridică mâna în mijlocul rundei: "Pot să explic un moment problema pe care o am cu integrarea?" Cinci minute de discuție tehnică între două persoane. Ceilalți șase stau și ascultă ceva ce nu-i privește.

A treia săptămână standup-ul durează treizeci și cinci de minute. Cineva aduce laptopul. Altcineva se așază. Runda celor trei întrebări a devenit o ședință de status cu discuții libere, demo-uri improvizate și dezbateri arhitecturale.

În a patra săptămână echipa începe să sară peste standup. "Oricum durează jumătate de oră, n-am timp."

Am văzut această secvență de cel puțin zece ori în cariera mea. Nu e ghinion. E un pattern.

------------------------------------------------------------------------

## ⏱️ De ce constrângerea de 15 minute nu e negociabilă

Standup-ul are un singur scop: **să sincronizeze echipa**. Nu e o ședință de analiză. Nu e un moment de rezolvare de probleme. Nu e o sesiune de design. E un punct rapid de aliniere.

Iar constrângerea de timp este ceea ce îl face să fie așa.

Când standup-ul durează 15 minute, se întâmplă lucruri specifice:

- Oamenii se pregătesc **înainte** de ședință, pentru că știu că au două minute
- Problemele sunt **semnalate**, nu rezolvate. Rezolvarea are loc după, între persoanele implicate
- Echipa menține percepția că standup-ul este **util și respectuos cu timpul lor**
- Nimeni nu vine gândindu-se "iată, încă o jumătate de oră pierdută"

Când standup-ul depășește 20 de minute, mecanismul se strică:

| Durată | Efect asupra echipei |
|---|---|
| 10-15 min | Focus ridicat, participare activă, percepție pozitivă |
| 15-20 min | Acceptabil, dar unii încep să se distragă |
| 20-30 min | Persoanele neinvolucrate în thread-urile lungi se deconectează mental |
| 30-45 min | Echipa percepe standup-ul ca pierdere de timp. Încep absențele |
| 45+ min | Standup-ul e mort. A devenit o ședință de status deghizată în practică agilă |

Cel mai periculos lucru nu este depășirea în sine. E că se întâmplă gradual. Trei minute în plus azi, cinci mâine. Nimeni nu observă până nu e prea târziu.

------------------------------------------------------------------------

## ❓ Cele trei întrebări — și nimic altceva

Standup-ul clasic se bazează pe trei întrebări:

1. **Ce am făcut ieri?**
2. **Ce voi face azi?**
3. **Mă blochează ceva?**

Simplu. Dar simplitatea e trădătoare, pentru că tentația de a extinde e constantă.

"Ce am făcut ieri" nu înseamnă să-ți povestești ziua. Înseamnă să spui: "Am terminat migrarea tabelelor lookup" sau "Am lucrat la bug-ul #247, nu l-am rezolvat încă." Zece secunde, nu trei minute.

"Ce voi face azi" nu e un plan detaliat. E o declarație de intenție: "Azi termin bug-ul #247 și încep testele de integrare."

"Mă blochează ceva?" e întrebarea cea mai importantă. Pentru că aici apar dependențele, bottleneck-urile, problemele pe care cineva singur nu le poate rezolva. Dar — și asta e fundamental — **blocajul se semnalează, nu se rezolvă în direct**.

Când cineva spune "Sunt blocat pentru că nu am acces la mediul de staging", răspunsul corect nu e o discuție de cincisprezece minute despre cine trebuie să dea accesul, cum se configurează și de ce nu funcționa ieri. Răspunsul corect e: "Ok, vorbim după standup, eu și tu."

Această disciplină este ceea ce menține standup-ul sub 15 minute. Fără ea, fiecare blocaj devine o ședință în interiorul ședinței.

------------------------------------------------------------------------

## 💀 Când standup-ul moare

Am identificat o listă destul de precisă a modurilor în care un standup poate muri. Le enumăr nu din pesimism, ci pentru că recunoașterea lor e singura cale de prevenire.

### Thread killer-ul

O persoană descrie o problemă tehnică complexă. Altă persoană răspunde. Pornește un dialog între doi, în timp ce șase persoane stau. Facilitatorul nu intervine pentru că "e un subiect important". Cincisprezece minute pierdute.

### Demo-ul improvizat

"Stați, vă arăt ce am făcut." Screen share, navigare în aplicație, explicarea detaliilor de UI. Interesant? Poate. Relevant pentru standup? Nu.

### Managerul care pune întrebări

PM-ul sau team lead-ul începe să aprofundeze: "Feature-ul ăla e la 60% sau 70%? Când prevezi să termini? Ai vorbit cu clientul?" Standup-ul se transformă într-un raport individual.

### Absența facilitatorului

Fără cineva care să țină ritmul, standup-ul devine o conversație liberă. Conversația liberă e minunată la cafenea, nu la 9:15 dimineața când opt persoane au de lucru.

### Laptopul deschis

Când oamenii aduc laptopul la standup, mesajul implicit e: "Această ședință nu merită atenția mea completă." Și au dreptate — dacă standup-ul durează 40 de minute, chiar nu o merită.

------------------------------------------------------------------------

## 🛠️ Cum faci un standup să funcționeze — cu adevărat

După douăzeci de ani de proiecte, rețeta mea e aceasta. Nu e elegantă, nu e din manual, dar funcționează.

### 1. Timer vizibil

Un cronometru pe ecranul partajat (sau un telefon pe masă) care pornește când începe standup-ul. Toți îl văd. Când arată 15 minute, standup-ul se termină. Punct.

Nu e autoritar. E un acord de echipă. Timer-ul nu e inamicul — e gardianul timpului tuturor.

### 2. Facilitator cu mandatul de a tăia

Ai nevoie de o persoană — prin rotație sau fixă — al cărei singur rol e să spună: "Ok, asta o aprofundăm după. Următorul." Nu e lipsă de respect. E respect pentru cele șase persoane care așteaptă.

Cel mai bun facilitator o face natural: "Interesant, discutăm imediat după. Marco, e rândul tău."

### 3. În picioare, cu adevărat

Nu e folclor. A sta în picioare are un efect psihologic concret: oamenii vor să termine repede. Când te așezi, te relaxezi. Când stai în picioare, tinzi spre sinteză.

Dacă echipa e la distanță, principiul se traduce în: camere pornite, fără multitasking. Semnalul trebuie să fie: "Aceste 15 minute au atenția mea completă."

### 4. Fără laptopuri, fără screen sharing

Standup-ul e verbal. Dacă ceva necesită un demo, o diagramă, o explicație vizuală — nu e material de standup. E material pentru o ședință separată, cu persoanele potrivite.

### 5. Parking lot

De fiecare dată când apare un subiect care merită aprofundare, facilitatorul îl notează pe o listă vizibilă — "parking lot". După standup, persoanele implicate rămân și discută. Ceilalți merg să lucreze.

Parking lot-ul e instrumentul cel mai subestimat în managementul standup-urilor. Permite să spui "discutăm după" fără ca subiectul să fie uitat.

------------------------------------------------------------------------

## 📊 Standup-ul în cifre

Să facem un calcul pe care nimeni nu-l face niciodată.

O echipă de 8 persoane. Standup zilnic. 220 de zile lucrătoare pe an.

| Scenariu | Durată | Ore/persoană/an | Ore totale echipă/an |
|---|---|---|---|
| Standup de 15 minute | 15 min | 55 ore | 440 ore |
| Standup de 30 minute | 30 min | 110 ore | 880 ore |
| Standup de 45 minute | 45 min | 165 ore | 1.320 ore |

Diferența dintre un standup bine gestionat și unul scăpat de sub control este de **880 de ore pe an**. Pentru o echipă de 8 persoane. Sunt 110 zile lucrătoare. Aproape cinci luni-om.

Și asta fără a număra efectul indirect: un standup de 45 de minute nu fură doar 45 de minute. Fură și cele 10-15 minute de concentrare necesare după pentru a reintra în fluxul de lucru.

------------------------------------------------------------------------

## 🔄 Standup remote vs în persoană

Din 2020 standup-urile sunt adesea remote. Se schimbă mijlocul, dar principiile rămân identice. Cu câteva precauții suplimentare.

### Remote e mai rău (dacă nu ești atent)

- Latența audio creează suprapuneri care alungesc timpii
- Multitasking-ul e invizibil (dar real)
- Lipsa limbajului corporal face mai dificil pentru facilitator să știe când să taie
- Screen sharing-ul e la un click distanță, iar tentația de a-l folosi e mare

### Cum gestionezi standup-ul remote

| Practică | Motiv |
|---|---|
| Ordine de vorbire predefinită | Evită "cine vorbește?" și tăcerile stânjenitoare |
| Camere pornite | Semnalează prezență și atenție |
| Chat pentru parking lot | Captează subiecte în timp real fără a întrerupe |
| Timer partajat pe ecran | Același principiu ca standup-ul în persoană |
| Toți pe mute cu excepția celui care vorbește | Elimină zgomotul de fond și tentația de a întrerupe |

Cel mai eficient truc pe care l-am găsit pentru standup-urile remote este **runda cu ștafetă**: fiecare persoană, după ce vorbește, o numește pe următoarea. "Am terminat. Sara, e rândul tău." Asta menține atenția activă și dă ritm ședinței.

------------------------------------------------------------------------

## 🎯 Standup-ul e un instrument, nu un ritual

Ce m-a frapat întotdeauna e ușurința cu care standup-ul devine un ritual gol. Îl faci pentru că "așa se face", pentru că "suntem agili", pentru că "framework-ul o cere". Dar nimeni nu se mai întreabă: funcționează?

Un standup funcționează când echipa îl percepe ca util. Când la 9:15 oamenii vin cu plăcere, spun ce au de spus în două minute, îi ascultă pe ceilalți, și la 9:30 sunt la birou știind exact ce se întâmplă în proiect.

Un standup nu funcționează când oamenii îl percep ca o obligație. Când oftează uitându-se la ceas. Când verifică telefonul. Când se gândesc "puteam folosi jumătatea asta de oră să lucrez."

Diferența dintre cele două scenarii e aproape întotdeauna aceeași: dacă constrângerea de 15 minute e respectată sau nu.

Nu ai nevoie de framework-uri sofisticate. Nu ai nevoie de certificări. Ai nevoie de un timer, un facilitator cu coloană vertebrală și conștiința că timpul oamenilor are valoare.

Cincisprezece minute. Trei întrebări. Parking lot pentru rest.

Tot restul e zgomot.
