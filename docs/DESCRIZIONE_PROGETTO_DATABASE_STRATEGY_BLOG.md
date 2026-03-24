# Ivan Luminaria -- Database Strategy Blog

## Descrizione del Progetto per Collaborazione con AI

## 1. Scopo del Progetto

Questo progetto è un **blog tecnico e portfolio professionale** dedicato
a database engineering, data architecture e strategie di performance.

Il sito ha tre obiettivi principali:

1.  Condividere conoscenza pratica sui database: funzionamento interno,
    performance tuning e architettura.
2.  Dimostrare competenza professionale su PostgreSQL, Oracle, MySQL e
    sistemi Data Warehouse.
3.  Pubblicare contenuti tecnici di alto valore per ingegneri,
    architetti e decisori tecnici.

Il blog è scritto con un **tono analitico, tecnico e orientato al
metodo**, evitando linguaggio marketing o spiegazioni superficiali.

Il principio guida del progetto è:

> I database non sono semplici componenti software.\
> Sono infrastrutture strategiche che determinano prestazioni,
> affidabilità e scalabilità dei sistemi digitali.

------------------------------------------------------------------------

# 2. Architettura Tecnica

Il sito è costruito usando un'**architettura completamente statica**,
progettata per semplicità, affidabilità e performance.

## Stack Tecnologico

-   **Hugo** -- Static Site Generator
-   **GitHub** -- Versionamento del codice
-   **GitHub Pages** -- Hosting del sito
-   **GitHub Actions** -- Pipeline automatica di build e deploy

Questa architettura garantisce:

-   nessun backend runtime
-   superficie di attacco minima
-   caricamento delle pagine estremamente veloce
-   build completamente deterministiche

## Struttura del Repository (semplificata)

    project-root
    │
    ├── archetypes/
    ├── assets/
    │   └── css/
    │       └── custom.css
    │
    ├── content/
    │   ├── about.*.md
    │   ├── posts/
    │   │   ├── postgresql/
    │   │   ├── mysql/
    │   │   └── query-tuning/
    │   │
    │   └── resumes/
    │
    ├── layouts/
    │   ├── partials/
    │   ├── shortcodes/
    │   └── templates base
    │
    ├── static/
    │   ├── img/
    │   └── downloads/
    │
    ├── config/
    │   └── _default/
    │
    └── .github/workflows/

## Flusso di Deploy

1.  Lo sviluppatore effettua un push sul repository GitHub.
2.  GitHub Actions avvia il workflow di build.
3.  Hugo genera il sito statico nella cartella `/public`.
4.  Il sito viene automaticamente pubblicato su GitHub Pages.

Questo garantisce **CI/CD completamente automatizzato** per il blog.

------------------------------------------------------------------------

# 3. Struttura dei Contenuti

Il blog è organizzato in **sezioni tematiche** dedicate a problemi reali
di database engineering.

## Sezioni principali

### Database Strategy

Riflessioni architetturali di alto livello sui sistemi dati.

Argomenti:

-   decisioni architetturali sui database
-   compromessi tra performance e scalabilità
-   strategie di modellazione dati
-   affidabilità dei sistemi

### Query Tuning

Analisi approfondite sulle performance delle query.

Esempi:

-   ottimizzazione delle ricerche LIKE
-   analisi degli execution plan
-   strategie di indexing
-   comportamento dell'optimizer

### Security & Access Control

Temi legati alla sicurezza dei database:

-   ruoli e privilegi
-   gestione degli accessi
-   sicurezza in ambienti di produzione

### Professional Roadmap

La sezione **Resumes** presenta roadmap strutturate delle competenze
professionali:

-   capacità tecniche
-   competenze architetturali
-   ruoli professionali

Questa sezione rappresenta **una mappa delle competenze**, non
semplicemente un curriculum.

------------------------------------------------------------------------

# 4. Strategia Multilingua

Il sito è progettato per essere **multilingua**.

Lingue supportate:

-   Italiano
-   Inglese
-   Spagnolo
-   Rumeno

Hugo gestisce automaticamente le lingue tramite sottodirectory:

    /it/
    /en/
    /es/
    /ro/

Il selettore della lingua è implementato tramite un componente template
personalizzato.

------------------------------------------------------------------------

# 5. Stile Visivo del Sito

Il sito utilizza un'estetica tecnica pulita.

Principi di design:

-   tipografia leggibile
-   minimo rumore visivo
-   contrasto forte per leggibilità tecnica
-   gerarchia visiva chiara

Lo stile è definito principalmente nel file:

    assets/css/custom.css

La palette colori richiama ecosistemi database:

-   blu PostgreSQL
-   rosso Oracle

L'identità visiva comunica **ingegneria seria e profondità tecnica**.

------------------------------------------------------------------------

# 6. Tono e Stile di Scrittura

Il blog evita intenzionalmente:

-   linguaggio marketing
-   affermazioni sensazionalistiche
-   tutorial superficiali

Preferisce invece:

-   spiegazioni analitiche
-   scenari reali
-   ragionamento architetturale

Il tono è:

-   tecnico
-   preciso
-   pragmatico
-   basato sull'esperienza

Gli articoli sono scritti come **case study ingegneristici**, non come
contenuti SEO.

------------------------------------------------------------------------

# 7. Pubblico di Riferimento

I lettori principali sono:

-   database engineer
-   backend engineer
-   data architect
-   CTO e technical leader

Si assume che il lettore:

-   conosca SQL
-   lavori con sistemi in produzione
-   sia interessato a performance e affidabilità

Il blog **non è pensato per principianti**.

------------------------------------------------------------------------

# 8. Visione di Lungo Periodo

L'obiettivo a lungo termine è costruire una **risorsa di riferimento
sulla strategia dei database e sulle pratiche di engineering**.

Direzioni future:

-   saggi architetturali più profondi
-   casi reali di performance tuning
-   analisi di system design
-   confronti tra database diversi

Il blog vuole diventare **una base di conoscenza tecnica costruita
sull'esperienza reale**.

------------------------------------------------------------------------

# 9. Filosofia del Progetto

La filosofia del progetto può essere riassunta così:

> Un database che semplicemente funziona non è sufficiente.\
> Deve scalare, restare affidabile sotto carico e sostenere il business
> che dipende da esso.

Questo progetto nasce per esplorare **cosa serve davvero per ottenere
tutto questo**.

------------------------------------------------------------------------

# 10. Stile Visivo delle Illustrazioni Generate con AI

Le immagini del blog sono generate tramite modelli AI.

L'obiettivo non è il fotorealismo, ma **illustrazione concettuale** che
rappresenti idee tecniche.

Lo stile è ispirato alle **illustrazioni editoriali degli anni '50**.

## Direzione Artistica

Le immagini devono seguire questi principi:

-   stile cartone retro anni '50
-   arte vettoriale minimal
-   forme geometriche marcate
-   linee fluide
-   composizione mid-century modern
-   influenze Art Deco
-   silhouette eleganti

Devono ricordare le **illustrazioni tecniche delle riviste vintage**.

## Palette Colori

Colori consentiti:

-   nero
-   rosso
-   beige
-   marrone
-   bianco

Eventualmente grigi neutri.

Palette moderne e colori saturi devono essere evitati.

## Atmosfera

Le immagini devono evocare:

-   grafica editoriale vintage
-   atmosfera da jazz club
-   illuminazione soffusa
-   texture carta ruvida

Devono sembrare stampate in **una rivista tecnica degli anni '50**.

## Principi di Composizione

Le immagini rappresentano concetti tecnici tramite metafore visive.

Esempi:

control room → monitoraggio database\
operatori che analizzano schermi → analisi query\
ingegneri attorno a console → architettura dati\
guardie o porte blindate → sicurezza database

I personaggi possono essere leggermente stilizzati nello stile **UPA
animation**.

## Formato Immagini

-   rapporto 16:9
-   stile vettoriale minimal
-   pochi elementi visivi
-   silhouette chiare

## Scopo delle Immagini

Le immagini **non sono decorative**.

Servono a:

-   introdurre visivamente il tema dell'articolo
-   rafforzare la comprensione concettuale
-   creare identità editoriale riconoscibile
