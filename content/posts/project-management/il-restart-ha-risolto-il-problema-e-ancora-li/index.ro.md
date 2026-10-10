---
categories:
- project-management
date: '2026-10-13'
description: Un incident care se închide fără cauză reconstituită nu e un episod izolat.
  Cum citești AWR, ASH și change log la rece înainte să apară al doilea defect.
draft: false
image: il-restart-ha-risolto-il-problema-e-ancora-li.cover.jpg
seoTitle: 'Incident rezolvat singur: problema rămâne în sistem'
tags:
- incident-management
- post-mortem
- database
- observability
- reliability
title: Repornirea a rezolvat. Problema e încă acolo.
translationKey: il_restart_ha_risolto_il_problema_e_ancora_li
webo_generated_at: 2026-10-10
webo_status: scheduled
---

# Repornirea a rezolvat. Problema e încă acolo.

*De ce un incident care se închide fără un lanț cauzal reconstituit nu este un episod izolat — și ce rămâne cu adevărat în sistem pentru a privi la rece.*

---
## Vineri, 19:40

Există un moment pe care un CIO îl cunoaște bine și care nu apare în rapoarte. Incidentul a început joi noaptea la 02:17 — o încetinire pe un serviciu critic, latențe peste prag, câteva sesiuni în timeout, puțini clienți afectați. Echipa de gardă s-a conectat, a observat patruzeci de minute, a luat câteva urme, nu a înțeles. La 03:11 curba a revenit. De la sine. Echipa a mai așteptat treizeci de minute pentru siguranță, a văzut sistemul stabilizându-se, a închis puntea. Dimineața, daily stand-up-ul a vorbit despre asta trei minute: *«a revenit, să-l ținem sub observație»*. În după-amiaza de vineri, cu trei ședințe de business în agendă, nimeni nu a mai vorbit despre asta.

La 19:40 CIO-ul iese din birou. Sistemul ține. Weekendul începe. Incidentul intră, fără ca nimeni să fi decis să-l pună acolo, în categoria mentală **«episod ocazional»**. Nu e o decizie formală — e o decizie prin omisiune: nimeni nu scrie, nimeni nu întreabă, thread-ul Slack dedicat încetează să se populeze, post-mortem-ul nu este convocat. Luni dimineața sistemul ține încă. Marți la fel. La sfârșitul săptămânii următoare, în debrieful operațional, subiectul nu mai apare nici măcar ca rând.

Momentul în care se pierde fereastra de reconstrucție nu este momentul incidentului. **Este vineri seara.** Nu când s-a stricat, ci când s-a încetat să se mai privească.

## Ce mai are sistemul, chiar dacă nimeni nu s-a dus să vadă

Există o convingere răspândită, aproape o evidență a meseriei, care spune: *«după ce incidentul a revenit, fără log-urile din acel moment, cauza nu mai poate fi reconstituită»*. Este adevărată într-un singur caz — când *nicio* urmă nu a fost păstrată. În aproape toate celelalte cazuri, sistemul are mai multă memorie decât cred cei care îl operează, iar fereastra de investigare este mult mai lungă decât sugerează dinamica urgenței.

Pe un database Oracle, **AWR** (Automatic Workload Repository) păstrează snapshot-uri la fiecare oră, cu o retenție implicită de opt zile și configurabilă până la cinci săptămâni. În fiecare snapshot se găsesc wait event-urile dominante, planurile de execuție ale query-urilor de top, statisticile de I/O, sesiunile active, segmentele cele mai contestate. **ASH** (Active Session History) păstrează un eșantion al sesiunilor active pe secundă, în formă circulară, utilizabil ulterior pentru a reconstitui *ce făcea exact* fiecare sesiune în minutul incidentului. **Alert log**-ul înregistrează erori, lock-uri, schimbări de stare. Sistemul de operare păstrează metrici de CPU, memorie, I/O. Storage-ul păstrează pattern-uri de latență și queue depth. **Repository-ul de change** — dacă există, și ar trebui să existe întotdeauna — înregistrează fiecare modificare de configurație, fiecare release aplicativ, fiecare patch de infrastructură. Observabilitatea modernă, discutată într-un alt articol din această serie, păstrează serii temporale de săptămâni sau luni.

A pune laolaltă aceste surse după șaptezeci și două de ore necesită metodă — dar este o reconstrucție *mai precisă*, nu mai puțin precisă, decât cea făcută la cald în plin incident. **La cald se caută pentru a opri simptomul. La rece se citește pentru a înțelege lanțul.** Sunt două acte diferite, cu scopuri diferite; al doilea este îngreunat de presiunea primului, nu de trecerea timpului.

## Un caz, și ce s-a întâmplat trei săptămâni mai târziu

Un context bancar, serviciu de autorizare plăți pe Oracle în înaltă disponibilitate, sarcină de vârf în jur de 1.400 de tranzacții pe secundă în intervalele comerciale. Într-o sâmbătă după-amiază, timp de patruzeci și două de minute, latența medie a serviciului a crescut de la 180 ms la peste 2 secunde, cu o fracțiune de tranzacții în timeout. Monitoringul a alertat, echipa de gardă s-a conectat, a văzut un *enqueue wait* dominant pe un tabel de sesiune utilizator. Înainte să se decidă o contramăsură, curba a revenit. În patruzeci și două de minute sistemul era din nou în prag.

Post-mortem-ul a fost scurt. Ipoteza de lucru, formulată fără dovezi solide, a fost *«un pattern de sarcină anormal al sâmbetei după-amiaza, poate legat de o campanie comercială»*. Echipa a închis ticket-ul, weekendul a reînceput, luni sistemul ținea. (Numerele — sarcină, latențe, timpi — sunt reprezentative pentru contexte similare; detaliile cazului specific sunt anonimizate din motive de confidențialitate contractuală.)

Trei săptămâni mai târziu, aceeași combinație de evenimente s-a repetat — de data aceasta într-o joi seara, în plină fereastră operațională, cu un volum de tranzacții dublu față de sâmbăta precedentă. Sistemul nu a mai revenit de la sine. Downtime-ul a durat două ore și zece minute. Board-ul a cerut o reconstrucție.

La acel moment, cu urgența celui de-al doilea incident, s-a făcut analiza care nu fusese făcută la rece cu trei săptămâni înainte. AWR-ul de sâmbătă avea, în două snapshot-uri consecutive, o schimbare netă în planul de execuție al unui query critic — efect al unui recalcul de statistici automat activat când tabelul depășise un anumit prag de creștere. ASH-ul arăta secvența de sesiuni care intraseră în așteptare pe acel query, cu contorul de waiteri care crescuse progresiv până la punctul de a declanșa escaladarea pe resursa internă a bazei de date. Registrul de change arăta că un nou release aplicativ, cu patru zile înainte de incidentul de sâmbătă, introdusese un apel suplimentar la acel query de fiecare dată când un utilizator deschidea o sesiune — apel care devenea critic doar când volumul de deschidere a sesiunilor depășea o anumită concurență.

Toate acestea erau deja în sistem sâmbătă după-amiaza. Firul dintre creșterea tabelului, recalculul statisticilor, schimbarea planului, noul release, creșterea concurenței nu era *inferabil din simptomele înregistrate*. Era *lizibil* de către cineva care ar fi pus laolaltă sursele cu un model cauzal în minte — chiar și două săptămâni mai târziu. Diferența nu a fost de date disponibile. **A fost de decizie de a privi.**

## TIA-ul este un predictor, nu un episod

În cardiologie și neurologie preventivă există un concept care merită ținut în minte când te gândești la incidentele care revin de la sine. Se numește **TIA — Atac Ischemic Tranzitoriu**. Este un eveniment neurologic care se manifestă ca un AVC — tulburări de vorbire, slăbiciune a unui membru, vedere încețoșată — și **revine spontan în câteva minute sau ore**, fără sechele permanente. Pacientul la urgențe, dacă ajunge, este externat cu analize în normă și recomandarea de a controla tensiunea.

Cine cunoaște cifrele știe că un TIA este unul dintre **cei mai puternici predictori de AVC major în cele nouăzeci de zile următoare**. Literatura de specialitate indică că aproximativ un pacient din zece va avea un AVC clinic în cele trei luni următoare TIA-ului, iar jumătate dintre aceștia în patruzeci și opt de ore — dacă nu se face reconstrucția mecanismului și nu se instituie prevenția. TIA-ul nu este un episod izolat: este sistemul care a arătat o dată, în formă reversibilă, cum va eșua în formă ireversibilă dacă nimeni nu intervine asupra cauzei. (Cifre epidemiologice de referință — *DE VERIFICAT* cu ghidurile ESO/AHA actualizate pentru citarea publică.)

Un incident care revine de la sine are aceeași natură. Sistemul a arătat, în formă reversibilă, un mecanism care — cu cauza neînlăturată — se va manifesta din nou. Nu neapărat în același punct, nu neapărat cu aceeași sarcină, nu neapărat în sâmbăta după-amiaza de presiune comercială scăzută. **Al doilea incident alege cel mai prost moment cu precizie statistică**: pentru că acea cauză neînlăturată continuă să lucreze, și pentru că sarcina operațională crește până găsește fereastra potrivită.

TIA-ul și incidentul revenit împart și o a doua caracteristică, mai incomodă. Ambele **induc ușurare**. Pacientul externat de la urgențe cu analize în normă crede că a scăpat-o, nu că a fost avertizat. Echipa care vede curba revenind crede că sistemul a ținut, nu că sistemul a vorbit. Ușurarea nu este o reacție greșită — este umană, legitimă, necesară după orele de tensiune. **Momentul în care ușurarea devine un risc este cel în care închide fereastra de investigare înainte ca investigarea să fi fost măcar deschisă.**

## Întrebările care preced închiderea ticket-ului

Niciuna dintre aceste întrebări nu vrea să convingă pe cineva să transforme fiecare incident într-un proiect de șase săptămâni. Toate servesc la a decide **dacă o revenire spontană închide cazul sau îl deschide**, înainte ca acesta să fie închis prin omisiune.

**1. Cauza care ar explica atât începutul cât și revenirea spontană a fost articulată, sau explicăm doar simptomul?**
Un incident care începe pentru că «a existat un pattern de sarcină anormal» nu explică revenirea: sarcina anormală nu s-a stins de la sine în exact patruzeci și două de minute. Dacă nu există un model cauzal care să dea seama *de ambele extreme* ale intervalului, investigarea nu s-a închis — a încetat doar să pună întrebări.

**2. Ce sursă mai păstrează încă urme ale incidentului, și pentru cât timp?**
AWR, ASH, alert log, log OS, metrici de storage, change log, telemetrie aplicativă. Fiecare are o retenție diferită. Cartografierea ferestrei reziduale de investigare înainte de a decide dacă se investighează costă treizeci de minute și mută decizia din planul emoțional (*«acum suntem obosiți»*) în planul operațional (*«avem treisprezece zile»*).

**3. Dacă același mecanism s-ar repeta cu dublul sarcinii, sistemul ar mai ține?**
Este întrebarea pe care un cardiolog experimentat o pune după un TIA. Sistemul a ținut o dată în condiții favorabile — presiune comercială scăzută, fereastră de descărcare, concurență limitată. Întrebarea nu este *«va reveni?»*. Este *«când va reveni, va reveni în condiții pe care sistemul le mai poate absorbi?»*. Dacă răspunsul este *«nu știm»*, episodul nu este ocazional: este un semnal încă necitit.

**4. Cine ar avea autoritatea să convoace o reconstrucție la rece, și cu ce fereastră temporală?**
Adesea investigarea post-revenire nu este deschisă nu printr-o decizie, ci prin absența unui proprietar. Echipa operațională a trecut la următorul ticket, arhitectul nu are mandat explicit, managementul a văzut sistemul stabil. **Nominalizarea proprietarului reconstrucției la rece înainte de următorul incident** este intervenția organizațională cea mai subestimată — și cea mai ieftină — din întreaga guvernanță a rezilienței.

## Valoarea de a privi când urgența a trecut

Există un paradox care merită explicitat, pentru că răstoarnă o intuiție comună. **Reconstrucția la rece este mai precisă, nu mai puțin, decât cea la cald** — când sursele sunt păstrate. La cald se caută cu anxietatea de a opri simptomul, cu board-ul care cere actualizări la fiecare zece minute, cu ipotezele care se suprapun. La rece se citește cu timp pentru a compara surse diferite, a verifica corelații, a elimina piste care la cald păreau relevante și care la rece se dovedesc coincidențe.

Cine a făcut multe reconstrucții *post-revenire* știe și un al doilea lucru: **lanțul cauzal care emerge nu este aproape niciodată cel bănuit în după-amiaza incidentului**. Ipoteza *«pattern de sarcină anormal»* este plauzibilă la cald, unde tot ce s-a văzut este o curbă anormală. Devine evident parțială la rece, când intră în joc change log-ul săptămânii precedente, creșterea tabelului, recalculul statisticilor, noul release aplicativ.

Costul organizațional al unei reconstrucții la rece — trei sau cinci zile de timp al unor persoane experte, cu sistemul deja stabil și nicio urgență pe cap — este o fracțiune din costul celui de-al doilea incident, în zile de downtime, ședințe de board, conversații cu clienții, renegocieri de SLA. Comparația, pentru un CFO, se face în douăzeci de secunde. Rezistența, când există, rareori este de buget: este de **atenție**. Organizația care tocmai a expirat respirația de ușurare este fiziologic puțin dispusă să transforme acea respirație într-un nou ciclu de analiză. Tocmai acesta este motivul pentru care, în multe contexte, este util ca reconstrucția să fie convocată de **o figură externă operativității** — care nu a trăit cele patruzeci și două de ore de tensiune și care poate propune, cu calm, să se privească atunci când a privi costă mai puțin.

## O întrebare de dus cu tine

Nu există o regulă universală pentru incidentele care revin de la sine. Există, pentru fiecare organizație care gestionează incidente critice, o întrebare care merită pusă data viitoare când curba revine fără intervenție:

*«Mecanismul care explică cum a început explică și cum s-a terminat — sau explicăm doar faptul că s-a terminat?»*

Dacă răspunsul are vreo ezitare, episodul nu este încă ocazional. Este un sistem care a vorbit o dată. A doua oară va alege momentul în care a vorbi costă mai mult.

## Glosar
**[AWR](/ro/glossary/awr/)** — Automatic Workload Repository — instrument de diagnostic integrat in Oracle Database pentru colectarea si analiza statisticilor de performanta.

**[ASH](/ro/glossary/ash/)** — Active Session History — componenta Oracle care inregistreaza starea fiecarei sesiuni active o data pe secunda...

**[wait event](/ro/glossary/wait-event/)** — Eveniment de asteptare inregistrat de Oracle de fiecare data cand o sesiune nu poate continua si trebuie sa astepte o resursa — I/O, lock, retea sau CPU.

**[piano di esecuzione](/ro/glossary/piano-di-esecuzione/)** — Secvența de operații aleasă de optimizatorul SQL pentru a executa o interogare: scanări, join-uri, sortări. Statisticile învechite îl degradează fără semnal vizibil.

**[TIA](/ro/glossary/tia/)**
