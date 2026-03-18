# AI_CONTENT_GUIDELINES.md

## Linee guida per generazione contenuti e immagini

Questo documento definisce le regole che i sistemi AI devono seguire
quando generano contenuti per il **blog Ivan Luminaria -- Database
Strategy**.

L'obiettivo è mantenere coerenza in:

-   profondità tecnica
-   tono editoriale
-   stile visivo
-   chiarezza concettuale

------------------------------------------------------------------------

# 1. Tono Editoriale

I contenuti devono essere scritti con **tono tecnico, analitico e
professionale**.

Evitare:

-   linguaggio marketing
-   claim esagerati
-   stile motivazionale
-   tutorial superficiali

Preferire:

-   analisi tecnica
-   ragionamento ingegneristico
-   esempi reali
-   spiegazioni architetturali

Gli articoli devono sembrare **saggi tecnici di ingegneria**, non
contenuti marketing.

------------------------------------------------------------------------

# 2. Stile di Scrittura

Caratteristiche preferite:

-   spiegazioni tecniche chiare
-   ragionamento strutturato
-   paragrafi concisi
-   esempi pratici
-   comprensione profonda dei database

Gli articoli devono spiegare:

-   causa ed effetto
-   implicazioni sulle performance
-   comportamento dei sistemi

Evitare frasi generiche come:

"i database sono importanti"

Spiegare sempre **perché** e **come**.

------------------------------------------------------------------------

# 3. Struttura degli Articoli

Struttura consigliata:

1.  Introduzione del problema
2.  Spiegazione tecnica
3.  Esempio reale
4.  Strategia di implementazione
5.  Implicazioni su performance o architettura
6.  Conclusione pratica

L'articolo deve sembrare **condivisione di esperienza da parte di un
ingegnere esperto**.

------------------------------------------------------------------------

# 4. Pubblico Target

Il pubblico è composto da:

-   database engineer
-   backend engineer
-   system architect
-   CTO
-   decision maker tecnici

Si assume che il lettore:

-   conosca SQL
-   lavori con ambienti di produzione
-   sia interessato a affidabilità e performance

Spiegazioni troppo basilari devono essere evitate.

------------------------------------------------------------------------

# 5. Temi Preferiti

Argomenti adatti al blog:

-   query optimization
-   strategie di indexing
-   analisi execution plan
-   architettura database
-   modelli di access control
-   pratiche di sicurezza
-   performance tuning
-   affidabilità dei sistemi

Evitare articoli base come:

"cos'è un database".

Concentrarsi su **comportamento dei sistemi sotto carico reale**.

------------------------------------------------------------------------

# 6. Regole per le Immagini

Le immagini devono seguire lo stile retro illustrato del blog.

Prompt suggerito:

retro 1950s cartoon illustration, minimal vector art, mid-century
modern, ispirazione art deco, geometric shapes, elegant silhouettes,
limited color palette (black, red, beige, brown, white), textured paper
background, dim lighting, vintage editorial illustration style, 16:9
aspect ratio

Le immagini devono rappresentare **concetti tecnici attraverso metafore
visive**.

Esempi:

control room database\
ingegneri che monitorano sistemi dati\
guardie di sicurezza che proteggono un vault dati\
operatori che analizzano dashboard

Evitare:

-   immagini fotorealistiche
-   stock photos moderne
-   grafiche UI moderne

------------------------------------------------------------------------

# 7. Coerenza Concettuale

Ogni articolo deve mantenere coerenza concettuale tra:

-   titolo
-   spiegazione tecnica
-   illustrazione

Le immagini devono rafforzare l'idea centrale dell'articolo.

Esempio:

Articolo su access control → illustrazione con guardie o checkpoint di
sicurezza che controllano l'accesso a una struttura dati.

------------------------------------------------------------------------

# 8. Sezione Glossario

Ogni articolo deve terminare con una sezione `## Glossario` che elenca
**fino a 10 termini tecnici o acronimi chiave** utilizzati nell'articolo.

Formato per ogni voce:

**Termine** — Descrizione breve e chiara (1–2 frasi).

Criteri di selezione — privilegiare:

-   acronimi (es. AWR, SCD, ETL)
-   concetti tecnici specifici (es. buffer pool, execution plan)
-   strumenti o tecnologie menzionati nell'articolo

Evitare termini troppo generici (es. "database", "SQL") a meno che non
siano centrali per l'argomento dell'articolo.

Il glossario deve essere presente in **tutte e 4 le versioni
linguistiche** dell'articolo, con le descrizioni tradotte in ciascuna
lingua.

Dopo aver scritto il glossario, **aggiornare sempre** il file
`DOCS/GLOSSARIO_TERMINI.md` — aggiungendo i nuovi termini o aggiornando
la colonna "Contenuto in" per i termini già presenti.

------------------------------------------------------------------------

# 9. Obiettivo Finale

Il blog deve evolvere in **una base di conoscenza tecnica sulla
strategia dei database e sull'ingegneria dei sistemi dati**.

I contenuti devono privilegiare:

-   chiarezza
-   profondità
-   accuratezza
-   utilità pratica

L'obiettivo finale è costruire **una risorsa di riferimento per
ingegneri e architetti di sistemi dati**.
