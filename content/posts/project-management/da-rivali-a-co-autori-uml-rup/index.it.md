---
title: "Da rivali a co-autori: come Booch, Rumbaugh e Jacobson hanno inventato UML (e quello che ne resta oggi)"
seoTitle: "Three Amigos, UML e RUP: la storia e cosa resta oggi"
description: "La storia dei Three Amigos di UML e RUP: come Booch, Rumbaugh e Jacobson, da rivali, hanno unificato l'object-oriented modeling. E cosa ne resta oggi."
date: "2026-06-30T08:03:00+01:00"
draft: false
translationKey: "da_rivali_a_co_autori_uml_rup"
tags: ["methodology"]
categories: ["project-management"]
image: "da-rivali-a-co-autori-uml-rup.cover.jpg"
---

L'altro giorno, in un'aula di formazione interna di un cliente del settore assicurativo, ho aperto un documento di progetto del 2003 per mostrare un esempio di architettura applicativa. Diagrammi UML, fasi RUP con i loro pallini colorati, use case schematici, sequenze di interazione tra attori e sistemi. Una collega più giovane di qualche anno si è avvicinata alla lavagna e mi ha chiesto, senza giri: *"Cosa sono queste sigle? Le ho viste in qualche corso ma non le ho mai capite davvero."*

La domanda mi ha fatto sorridere — non perché fosse strana, ma perché era la stessa che avrei fatto io vent'anni fa se qualcuno mi avesse messo davanti a quel poster. **UML e RUP sono due sigle che hanno fatto epoca**, e che oggi vivono una doppia vita: marginali nella conversazione corrente sul project management, ma ancora vive in nicchie precise dove il rigore documentale è obbligatorio. E dietro a quelle sigle c'è una delle storie più curiose dell'ingegneria del software degli ultimi trent'anni — la storia di **tre rivali che hanno scelto di stare nella stessa stanza**.

Vale la pena raccontarla.

---

## Gli anni '90: tre tribù, tre vocabolari

Per capire UML serve fare un passo indietro alla fine degli anni '80, quando l'object-oriented stava diventando il paradigma dominante di programmazione. Ma c'era un problema: ogni gruppo di ricerca e ogni azienda di tooling aveva inventato **un suo modo di rappresentare visivamente le classi, le relazioni, gli oggetti**. E i tre approcci principali, ciascuno con il suo profeta, si guardavano in cagnesco.

**Grady Booch**, americano, lavorava da metà anni '80 in **Rational Software** (la stessa azienda fondata da Mike Devlin e Paul Levy nel 1981). Aveva pubblicato il *Booch Method* nei primi anni '90: una notazione molto ricca di simboli — nuvolette, frecce, etichette — che diventava difficile da disegnare a mano ma straordinariamente espressiva quando supportata da uno strumento grafico. Era pensata per developer.

**James Rumbaugh**, americano anche lui, lavorava nei laboratori di ricerca di **General Electric**. Nel 1991 pubblicò *Object Modeling Technique* (OMT), un approccio più asciutto e più orientato al modeling dei dati che alla rappresentazione del comportamento. Funzionava bene in contesti dove il database era il centro del sistema. Era pensato per architetti.

**Ivar Jacobson**, svedese, aveva lavorato in **Ericsson** prima di fondare la propria società, *Objectory AB*. Il suo contributo originale era il concetto di **use case**: descrivere il sistema dal punto di vista dell'attore che lo usa, non dell'oggetto che lo compone. Era pensato per chi parlava con il business.

Tre tribù, tre vocabolari, **tre simbologie diverse per disegnare la stessa classe**. Conferenze separate, libri concorrenti, customer che dovevano scegliere quale tribù seguire. La competizione, nelle parole di chi ha vissuto quel periodo, era a tratti feroce — c'erano rapporti tecnici di un campo che criticavano apertamente le scelte degli altri due. Niente di personale, ma tre community che si guardavano dall'altra parte del fiume.

---

## La svolta: ottobre 1994

A metà del 1994, Rational Software fa la mossa che cambia tutto. Mike Devlin, il CEO, ha capito che la frammentazione sta diventando un freno per l'adozione enterprise dell'object-oriented — e che nessuno dei tre metodi vincerà mai da solo. Decide allora di **mettere insieme i protagonisti**.

A ottobre 1994, **James Rumbaugh lascia General Electric e si trasferisce in Rational**. La notizia fa rumore: due dei tre profeti dell'object-oriented modeling adesso lavorano nella stessa azienda. Booch e Rumbaugh, che fino al giorno prima firmavano articoli che si rispondevano a vicenda sui giornali specializzati, ora hanno gli uffici sullo stesso corridoio.

Un anno dopo, nel 1995, Rational acquisisce **Objectory AB**, e **Ivar Jacobson** si unisce al gruppo. È fatta: i tre uomini che avevano dominato il dibattito sull'object-oriented per cinque anni sono nella stessa azienda. La stampa specializzata, con un misto di curiosità e ironia, li battezza **i Three Amigos** — non senza una punta di scetticismo: davvero tre persone così diverse riusciranno a lavorare insieme?

I tre, intervistati anni dopo, hanno raccontato gli inizi senza enfasi. *"Per i primi mesi ognuno difendeva la propria notazione. Poi, gradualmente, abbiamo capito che nessuno dei tre approcci, da solo, era sufficiente. Ed era ovvio che il mercato non avrebbe sopportato per sempre tre standard concorrenti."*

---

## UML, novembre 1997

Tra il 1995 e il 1997 i Three Amigos lavorano alla fusione dei tre metodi. Booch porta la ricchezza simbolica per il modeling strutturale, Rumbaugh porta la disciplina del modeling dei dati e degli stati, Jacobson porta gli use case come ponte verso il business. Nasce così **UML — Unified Modeling Language**.

Il percorso di standardizzazione passa attraverso **OMG (Object Management Group)** [1], il consorzio non-profit che amministrava già altri standard del mondo object-oriented (come CORBA). UML 1.0 viene sottomesso all'OMG a gennaio 1997; **UML 1.1 viene adottato come standard formale OMG a novembre 1997**.

In quella prima versione UML offriva **nove tipi di diagrammi** organizzati in due famiglie: **strutturali** (class diagram, object diagram, component diagram, deployment diagram) per descrivere la struttura statica, e **comportamentali** (use case, sequence, collaboration, statechart, activity) per descrivere il comportamento dinamico. Da allora la specifica è cresciuta — UML 2.5 (l'attuale) ha tredici tipi di diagrammi — ma il nucleo è rimasto quello.

Uno standard si misura non da chi lo crea, ma da chi lo usa. E **UML è stato adottato rapidamente** — nei tre anni successivi è diventato il linguaggio di documentazione architetturale dominante in banking, telco, PA e assicurativo, dove gli appalti enterprise lo richiedevano esplicitamente nei capitolati.

---

## RUP, 1998: il processo enterprise

UML era il **linguaggio**, ma serviva un **processo** che dicesse come usarlo. Rational Software risponde nel 1998 con **RUP — Rational Unified Process** [2]. Un metodo di sviluppo software iterativo, basato sui contributi precedenti di Booch e Jacobson, organizzato in **quattro fasi sequenziali con iterazioni interne** a ciascuna fase:

- **Inception** — visione, business case, scope
- **Elaboration** — architettura, requisiti dettagliati, mitigazione dei rischi
- **Construction** — implementazione iterativa
- **Transition** — deploy, beta, rollout

A differenza del *waterfall* classico, RUP era **iterativo**: non si finiva una fase prima di iniziare la successiva, ma si tornava indietro più volte. A differenza dei metodi *lightweight* che sarebbero arrivati pochi anni dopo, però, era **heavyweight** — un progetto RUP enterprise tipico prevedeva sei mesi di Elaboration prima di scrivere una riga di codice di produzione. Documenti formali, artefatti tracciati, milestone documentate, audit possibili.

Era la risposta giusta per il contesto in cui era nato. Negli anni 1998-2005, RUP è stato adottato massivamente in banking europeo, in pubblica amministrazione, nei sistemi di telecomunicazioni. **IBM acquisisce Rational nel 2003** per 2,1 miliardi di dollari — un'operazione che valeva, di fatto, RUP come asset strategico tanto quanto UML.

---

## Febbraio 2001: l'Agile Manifesto cambia il vento

Mentre RUP raggiungeva il suo apice di adozione, **dall'altra parte del fiume** stava nascendo qualcosa di completamente diverso. Tra l'11 e il 13 febbraio 2001, **diciassette sviluppatori si incontrano in una stazione sciistica dello Utah** — Snowbird — e firmano un poster di poche righe che sarebbe diventato l'**Agile Manifesto** [3].

Quattro coppie di valori, ciascuna con la forma "X over Y":

- *Individuals and interactions over processes and tools*
- *Working software over comprehensive documentation*
- *Customer collaboration over contract negotiation*
- *Responding to change over following a plan*

Era esattamente il rovescio di RUP. Dove RUP metteva i processi al centro, Agile metteva le persone. Dove RUP chiedeva sei mesi di documenti prima del codice, Agile chiedeva codice funzionante ogni due settimane. Dove RUP formalizzava i contratti, Agile chiedeva conversazioni continue con il committente.

Nessuno dei diciassette firmatari, vale la pena dirlo, attaccava esplicitamente RUP. Il Manifesto non nomina nessun metodo concorrente. Ma il messaggio era chiaro, e nei dieci anni successivi il vento è cambiato. **Scrum**, **XP** (Extreme Programming), **Kanban** sono diventati il vocabolario standard del team di sviluppo. RUP, in molti contesti, ha smesso di essere proposto nei nuovi progetti.

Non è morto. Ma il vento è cambiato.

---

## Cosa resta oggi, vent'anni dopo

Vent'anni dopo l'Agile Manifesto, dove ci troviamo?

**UML è ancora vivo**, ma in modo diverso da come pensavano i Three Amigos. Non è più il linguaggio universale per descrivere l'architettura di un sistema — quel ruolo è stato spesso preso da diagrammi più liberi, da architecture decision records (ADR) in markdown, da disegni in Mermaid o draw.io che non rispettano la sintassi UML formale ma ne portano lo spirito. **UML come notazione formale sopravvive** nei capitolati della pubblica amministrazione, nei progetti di certificazione ISO, e nei contesti accademici dove insegnare l'object-oriented modeling è ancora parte del curriculum.

**RUP, invece, ha trovato la sua nicchia** — ed è una nicchia tutt'altro che marginale. Sopravvive vivo e vegeto nei settori dove il **rigore documentale è obbligatorio per legge o per audit**:

- **Aviazione e aerospace** — sistemi avionici certificati DO-178C, dove ogni requisito deve essere tracciato dalla raccolta al test
- **Medicale** — dispositivi sotto IEC 62304, dove il processo di sviluppo software è certificato insieme al prodotto
- **Brevetti e R&D farmaceutico** — dove la tracciabilità del processo di innovazione ha valore legale
- **Banking critico** — sistemi core di pagamento dove la documentazione formale è parte del contratto regolatorio

In questi contesti, **un metodo agile pura non passa l'audit**. Serve poter dimostrare a un revisore esterno, anni dopo il rilascio, perché una certa scelta architetturale è stata fatta e quali alternative erano state considerate. RUP — o un suo discendente diretto — è ancora il modo standard di farlo.

Per il resto, **Scrum e Kanban dominano**. Le [stand-up giornaliere di 15 minuti](/it/posts/project-management/standup-meeting-15-minuti/) che ho raccontato in un altro articolo sono il rituale Agile per eccellenza, e non sarebbero esistite se nel 2001 quei diciassette in Utah non avessero firmato quel poster.

---

## La lezione che porto via dai Three Amigos

La lezione che mi resta da questa storia — quella che ho provato a spiegare alla collega davanti alla lavagna, quel giorno — non è UML, e non è RUP.

È che **tre persone che facevano la stessa cosa in modo competitivo hanno deciso, a un certo punto, di stare nella stessa stanza**. Hanno smesso di pubblicare articoli che si rispondevano a vicenda, hanno smesso di difendere ogni dettaglio della propria notazione, e hanno cercato il pezzo di valore comune. Non è stato indolore — ci sono voluti due anni di confronti dentro Rational prima che UML 1.0 fosse pronto. Ma è successo.

Ed è una lezione che vale, nel project management di oggi, molto più di qualsiasi dettaglio sintattico di UML. Quando un team di sviluppo si divide tra fazioni che difendono ciascuna il proprio framework preferito — Scrum vs Kanban, microservizi vs monolite, REST vs GraphQL — la lezione dei Three Amigos è che il valore di un metodo non si misura nella sua superiorità teorica, ma nella sua **capacità di stare nella stessa stanza con altri metodi diversi** e produrre qualcosa di nuovo.

Non c'è un metodo superiore. Ci sono contesti diversi, e metodi adatti a contesti diversi. UML e RUP sono adatti dove il rigore documentale è obbligatorio. Scrum e Kanban sono adatti dove la velocità di iterazione è obbligatoria. Entrambi sopravvivono, accanto, perché entrambi servono.

E le storie come quella dei Three Amigos servono a ricordarcelo, ogni tanto.

---

## Fonti ufficiali

1. Object Management Group — [Unified Modeling Language (UML) specification](https://www.omg.org/spec/UML/)
2. Rational Unified Process — [overview e fasi (IBM/Rational documentation archive)](https://www.ibm.com/docs/en/rational-soft-arch/9.7.0?topic=overview-rational-unified-process)
3. Beck, Beedle, van Bennekum et al. — [Manifesto for Agile Software Development (febbraio 2001)](https://agilemanifesto.org/)

---

## Glossario

- **[Three Amigos](/it/glossary/three-amigos/)** — Soprannome dato dalla stampa specializzata a Grady Booch, James Rumbaugh e Ivar Jacobson, i tre creatori di UML che lavoravano in Rational Software tra il 1994 e il 1998. Da rivali divennero co-autori di uno standard unificato.
- **[UML](/it/glossary/uml/)** — Unified Modeling Language. Linguaggio standard di modellazione object-oriented, adottato da OMG nel novembre 1997 a partire dalla fusione di tre metodi precedenti (Booch Method, OMT, Objectory). Include diagrammi strutturali e comportamentali.
- **[RUP](/it/glossary/rup/)** — Rational Unified Process. Metodo di sviluppo software iterativo rilasciato da Rational nel 1998, organizzato in quattro fasi (Inception, Elaboration, Construction, Transition). Heavyweight e document-intensive, oggi vive in nicchie regolamentate (aviazione, medicale, banking critico).
- **[Use Case](/it/glossary/use-case/)** — Tecnica di analisi dei requisiti introdotta da Ivar Jacobson che descrive il sistema dal punto di vista dell'attore che lo usa, non degli oggetti che lo compongono. Uno dei tre pilastri che hanno alimentato UML.
- **[Agile Manifesto](/it/glossary/agile-manifesto/)** — Documento di poche righe firmato a Snowbird, Utah, l'11-13 febbraio 2001 da diciassette sviluppatori. Quattro coppie di valori che spostavano il focus dello sviluppo software dalle pratiche heavyweight (RUP-like) alle pratiche lightweight (Scrum, XP, Kanban).
