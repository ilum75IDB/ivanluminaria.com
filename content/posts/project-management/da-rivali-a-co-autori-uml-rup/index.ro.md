---
title: "De la rivali la co-autori: cum Booch, Rumbaugh și Jacobson au inventat UML (și ce a rămas astăzi)"
seoTitle: "Three Amigos, UML și RUP: istoria și ce a rămas astăzi"
description: "Povestea Three Amigos de la UML și RUP: cum Booch, Rumbaugh și Jacobson, din rivali, au unificat object-oriented modeling. Și ce a rămas astăzi."
date: "2026-06-30T08:03:00+01:00"
draft: false
translationKey: "da_rivali_a_co_autori_uml_rup"
tags: ["methodology"]
categories: ["project-management"]
image: "da-rivali-a-co-autori-uml-rup.cover.jpg"
---

Zilele trecute, într-o sală de formare internă a unui client din sectorul asigurărilor, am deschis un document de proiect din 2003 pentru a arăta un exemplu de arhitectură aplicativă. Diagrame UML, faze RUP cu punctele lor colorate, use case-uri schematice, secvențe de interacțiune între actori și sisteme. O colegă mai tânără cu câțiva ani s-a apropiat de tablă și m-a întrebat, fără ocolișuri: *"Ce înseamnă aceste acronime? Le-am văzut în niște cursuri dar nu le-am înțeles cu adevărat niciodată."*

Întrebarea m-a făcut să zâmbesc — nu pentru că ar fi fost ciudată, ci pentru că era exact aceeași pe care aș fi pus-o eu cu douăzeci de ani în urmă dacă cineva mi-ar fi pus în față acel poster. **UML și RUP sunt două acronime care au făcut epocă**, și care astăzi trăiesc o dublă viață: marginale în conversația curentă despre project management, dar încă vii în nișe precise unde rigoarea documentară este obligatorie. Iar în spatele acelor acronime se ascunde una dintre cele mai curioase povești din ingineria software-ului din ultimii treizeci de ani — povestea a **trei rivali care au ales să stea în aceeași cameră**.

Merită spusă.

---

## Anii '90: trei triburi, trei vocabulare

Pentru a înțelege UML trebuie să facem un pas înapoi până la sfârșitul anilor '80, când object-oriented devenea paradigma dominantă a programării. Dar exista o problemă: fiecare grup de cercetare și fiecare companie de tooling își inventase **propriul mod de a reprezenta vizual clasele, relațiile, obiectele**. Iar cele trei abordări principale, fiecare cu profetul său, se priveau cu suspiciune.

**Grady Booch**, american, lucra încă de la mijlocul anilor '80 la **Rational Software** (aceeași companie fondată de Mike Devlin și Paul Levy în 1981). Publicase *Booch Method* la începutul anilor '90: o notație foarte bogată în simboluri — norișori, săgeți, etichete — care devenea greu de desenat cu mâna dar extraordinar de expresivă atunci când era susținută de un instrument grafic. Era gândită pentru developeri.

**James Rumbaugh**, american și el, lucra în laboratoarele de cercetare ale **General Electric**. În 1991 a publicat *Object Modeling Technique* (OMT), o abordare mai sobră și mai orientată spre data modeling decât spre reprezentarea comportamentului. Funcționa bine în contexte unde baza de date era centrul sistemului. Era gândită pentru arhitecți.

**Ivar Jacobson**, suedez, lucrase la **Ericsson** înainte de a-și fonda propria companie, *Objectory AB*. Contribuția sa originală era conceptul de **use case**: descrierea sistemului din punctul de vedere al actorului care îl folosește, nu al obiectului care îl compune. Era gândită pentru cine vorbea cu business-ul.

Trei triburi, trei vocabulare, **trei simbologii diferite pentru a desena aceeași clasă**. Conferințe separate, cărți concurente, customers care trebuiau să aleagă ce trib să urmeze. Competiția, în cuvintele celor care au trăit acea perioadă, era uneori feroce — existau rapoarte tehnice dintr-un câmp care criticau deschis alegerile celorlalte două. Nimic personal, dar trei community care se priveau de pe celălalt mal al râului.

---

## Punctul de cotitură: octombrie 1994

La mijlocul lui 1994, Rational Software face mișcarea care schimbă totul. Mike Devlin, CEO-ul, a înțeles că fragmentarea devine o frână pentru adopția enterprise a object-oriented — și că niciunul dintre cele trei metode nu va câștiga niciodată singur. Decide atunci să **îi pună pe protagoniști împreună**.

În octombrie 1994, **James Rumbaugh părăsește General Electric și se mută la Rational**. Vestea face zgomot: doi dintre cei trei profeți ai object-oriented modeling lucrează acum în aceeași companie. Booch și Rumbaugh, care până în ziua anterioară semnau articole care își răspundeau reciproc pe revistele de specialitate, au acum birourile pe același coridor.

Un an mai târziu, în 1995, Rational achiziționează **Objectory AB**, iar **Ivar Jacobson** se alătură grupului. Gata: cei trei oameni care dominaseră dezbaterea despre object-oriented timp de cinci ani sunt în aceeași companie. Presa de specialitate, cu un amestec de curiozitate și ironie, îi botează **Three Amigos** — nu fără o doză de scepticism: chiar vor reuși trei persoane atât de diferite să lucreze împreună?

Cei trei, intervievați ani mai târziu, au povestit începuturile fără emfază. *"În primele luni fiecare își apăra propria notație. Apoi, treptat, am înțeles că niciuna dintre cele trei abordări, singură, nu era suficientă. Și era evident că piața nu va tolera pentru totdeauna trei standarde concurente."*

---

## UML, noiembrie 1997

Între 1995 și 1997, Three Amigos lucrează la fuziunea celor trei metode. Booch aduce bogăția simbolică pentru modeling-ul structural, Rumbaugh aduce disciplina modeling-ului datelor și stărilor, Jacobson aduce use case-urile ca punte spre business. Astfel se naște **UML — Unified Modeling Language**.

Traseul de standardizare trece prin **OMG (Object Management Group)** [1], consorțiul non-profit care administra deja alte standarde ale lumii object-oriented (cum ar fi CORBA). UML 1.0 este supus OMG în ianuarie 1997; **UML 1.1 este adoptat ca standard formal OMG în noiembrie 1997**.

În acea primă versiune UML oferea **nouă tipuri de diagrame** organizate în două familii: **structurale** (class diagram, object diagram, component diagram, deployment diagram) pentru a descrie structura statică, și **comportamentale** (use case, sequence, collaboration, statechart, activity) pentru a descrie comportamentul dinamic. De atunci specificația a crescut — UML 2.5 (cea actuală) are treisprezece tipuri de diagrame — dar nucleul a rămas.

Un standard se măsoară nu după cine îl creează, ci după cine îl folosește. Iar **UML a fost adoptat rapid** — în cei trei ani care au urmat a devenit limbajul de documentare arhitecturală dominant în banking, telco, administrația publică și asigurări, unde caietele de sarcini enterprise îl cereau explicit în specificații.

---

## RUP, 1998: procesul enterprise

UML era **limbajul**, dar era nevoie de un **proces** care să spună cum să-l folosești. Rational Software răspunde în 1998 cu **RUP — Rational Unified Process** [2]. O metodă de dezvoltare software iterativă, bazată pe contribuțiile precedente ale lui Booch și Jacobson, organizată în **patru faze secvențiale cu iterații interne** în fiecare fază:

- **Inception** — viziune, business case, scope
- **Elaboration** — arhitectură, cerințe detaliate, mitigarea riscurilor
- **Construction** — implementare iterativă
- **Transition** — deploy, beta, rollout

Spre deosebire de *waterfall*-ul clasic, RUP era **iterativ**: nu se termina o fază înainte de a o începe pe următoarea, ci se revenea înapoi de mai multe ori. Spre deosebire de metodele *lightweight* care aveau să sosească peste câțiva ani, totuși, era **heavyweight** — un proiect RUP enterprise tipic prevedea șase luni de Elaboration înainte de a scrie o linie de cod de producție. Documente formale, artefacte trasate, milestone documentate, audituri posibile.

Era răspunsul potrivit pentru contextul în care se născuse. În anii 1998-2005, RUP a fost adoptat masiv în banking-ul european, în administrația publică, în sistemele de telecomunicații. **IBM achiziționează Rational în 2003** pentru 2,1 miliarde de dolari — o operație care evalua, de fapt, RUP ca asset strategic la fel ca UML.

---

## Februarie 2001: Manifestul Agile schimbă vântul

În timp ce RUP își atingea apogeul de adopție, **de cealaltă parte a râului** se năștea ceva complet diferit. Între 11 și 13 februarie 2001, **șaptesprezece dezvoltatori se întâlnesc într-o stațiune de ski din Utah** — Snowbird — și semnează un poster de câteva rânduri care avea să devină **Manifestul Agile** [3].

Patru perechi de valori, fiecare cu forma "X peste Y":

- *Indivizi și interacțiuni peste procese și instrumente*
- *Software funcțional peste documentație cuprinzătoare*
- *Colaborare cu clientul peste negociere contractuală*
- *Răspuns la schimbare peste urmărirea unui plan*

Era exact opusul RUP-ului. Acolo unde RUP punea procesele în centru, Agile punea oamenii. Acolo unde RUP cerea șase luni de documente înainte de cod, Agile cerea software funcțional la fiecare două săptămâni. Acolo unde RUP formaliza contractele, Agile cerea conversații continue cu clientul.

Niciunul dintre cei șaptesprezece semnatari, merită spus, nu ataca RUP în mod explicit. Manifestul nu numește niciun metod concurent. Dar mesajul era clar, iar în următorii zece ani vântul s-a schimbat. **Scrum**, **XP** (Extreme Programming), **Kanban** au devenit vocabularul standard al echipei de dezvoltare. RUP, în multe contexte, a încetat să fie propus în noile proiecte.

Merită menționat că multe idei ale Agile **nu s-au născut din nimic**. **User story** sunt use case despuiate de formalismul lui Jacobson, **sprint**-urile scurte sunt Elaboration-urile RUP scurtate, iar chiar ceremonia BDD numită *"Three Amigos meeting"* — developer, tester și business analyst care discută împreună o user story înainte de a o începe — este un omagiu explicit grupului Booch, Rumbaugh și Jacobson. Agile nu atât a contrazis UML, **mai mult i-a eliberat ideile de greutatea procesului**. Este material care merită un articol aparte, în viitor.

Nu este mort. Dar vântul s-a schimbat.

---

## Ce a rămas astăzi, douăzeci de ani mai târziu

La douăzeci de ani de la Manifestul Agile, unde ne aflăm?

**UML este încă viu**, dar într-un mod diferit față de cum credeau Three Amigos. Nu mai este limbajul universal pentru a descrie arhitectura unui sistem — acel rol a fost adesea preluat de diagrame mai libere, de architecture decision records (ADR) în markdown, de desene în Mermaid sau draw.io care nu respectă sintaxa UML formală dar îi poartă spiritul. **UML ca notație formală supraviețuiește** în caietele de sarcini ale administrației publice, în proiectele de certificare ISO, și în contexte academice unde predarea object-oriented modeling face încă parte din curriculum.

**RUP, în schimb, și-a găsit nișa** — și este o nișă departe de a fi marginală. Supraviețuiește viu și bine în sectoarele unde **rigoarea documentară este obligatorie prin lege sau prin audit**:

- **Aviație și aerospațial** — sisteme avionice certificate DO-178C, unde fiecare cerință trebuie urmărită de la colectare până la test
- **Medical** — dispozitive sub IEC 62304, unde procesul de dezvoltare software este certificat împreună cu produsul
- **Patente și R&D farmaceutic** — unde trasabilitatea procesului de inovație are valoare legală
- **Banking critic** — sisteme core de plată unde documentația formală face parte din contractul reglementar

În aceste contexte, **un metod agile pur nu trece auditul**. E nevoie să poți demonstra unui auditor extern, ani după release, de ce s-a făcut o anumită alegere arhitecturală și ce alternative fuseseră luate în considerare. RUP — sau un descendent direct al său — este încă modul standard de a face asta.

Pentru restul, **Scrum și Kanban domină**. [Stand-up-urile zilnice de 15 minute](/ro/posts/project-management/standup-meeting-15-minuti/) pe care le-am descris într-un alt articol sunt ritualul Agile prin excelență, și nu ar exista dacă în 2001 acei șaptesprezece din Utah nu ar fi semnat acel poster.

---

## Lecția pe care o iau cu mine de la Three Amigos

Lecția care îmi rămâne din această poveste — cea pe care am încercat să o explic colegei din fața tablei, în acea zi — nu este UML, și nu este RUP.

Este că **trei persoane care făceau același lucru în mod competitiv au decis, la un moment dat, să stea în aceeași cameră**. Au încetat să publice articole care își răspundeau reciproc, au încetat să apere fiecare detaliu al propriei notații, și au căutat bucata de valoare comună. Nu a fost nedureros — au fost nevoie de doi ani de confruntări în interiorul Rational înainte ca UML 1.0 să fie gata. Dar s-a întâmplat.

Și este o lecție care valorează, în project management-ul de astăzi, mult mai mult decât orice detaliu sintactic al UML. Când o echipă de dezvoltare se împarte în facțiuni care apără fiecare framework-ul preferat — Scrum vs Kanban, microservicii vs monolit, REST vs GraphQL — lecția Three Amigos este că valoarea unui metod nu se măsoară în superioritatea sa teoretică, ci în **capacitatea sa de a sta în aceeași cameră cu alte metode diferite** și de a produce ceva nou.

Nu există un metod superior. Există contexte diferite, și metode potrivite pentru contexte diferite. UML și RUP sunt potrivite acolo unde rigoarea documentară este obligatorie. Scrum și Kanban sunt potrivite acolo unde viteza de iterație este obligatorie. Ambele supraviețuiesc, una lângă cealaltă, pentru că ambele servesc.

Iar poveștile precum cea a Three Amigos servesc să ne-o amintească, din când în când.

---

## Surse oficiale

1. Object Management Group — [Unified Modeling Language (UML) specification](https://www.omg.org/spec/UML/)
2. Rational Unified Process — [overview și faze (IBM/Rational documentation archive)](https://www.ibm.com/docs/en/rational-soft-arch/9.7.0?topic=overview-rational-unified-process)
3. Beck, Beedle, van Bennekum et al. — [Manifesto for Agile Software Development (februarie 2001)](https://agilemanifesto.org/)

---

## Glosar

- **[Three Amigos](/ro/glossary/three-amigos/)** — Poreclă dată de presa de specialitate lui Grady Booch, James Rumbaugh și Ivar Jacobson, cei trei creatori ai UML care lucrau la Rational Software între 1994 și 1998. Din rivali au devenit co-autori ai unui standard unificat.
- **[UML](/ro/glossary/uml/)** — Unified Modeling Language. Limbaj standard de modelare object-oriented, adoptat de OMG în noiembrie 1997 pornind de la fuziunea a trei metode precedente (Booch Method, OMT, Objectory). Include diagrame structurale și comportamentale.
- **[RUP](/ro/glossary/rup/)** — Rational Unified Process. Metodă de dezvoltare software iterativă lansată de Rational în 1998, organizată în patru faze (Inception, Elaboration, Construction, Transition). Heavyweight și document-intensiv, astăzi trăiește în nișe reglementate (aviație, medical, banking critic).
- **[Use Case](/ro/glossary/use-case/)** — Tehnică de analiză a cerințelor introdusă de Ivar Jacobson care descrie sistemul din punctul de vedere al actorului care îl folosește, nu al obiectelor care îl compun. Unul dintre cei trei piloni care au alimentat UML.
- **[Manifestul Agile](/ro/glossary/agile-manifesto/)** — Document de câteva rânduri semnat la Snowbird, Utah, pe 11-13 februarie 2001 de șaptesprezece dezvoltatori. Patru perechi de valori care au deplasat focusul dezvoltării software de la practicile heavyweight (RUP-like) la practicile lightweight (Scrum, XP, Kanban).
