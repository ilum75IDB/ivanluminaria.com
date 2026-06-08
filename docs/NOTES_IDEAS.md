# Note e Idee per futuri articoli

## Issue create

### Oracle Text: indicizzare e ricercare testo in modo efficiente — Issue #101
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/101
- **Concept**: L'articolo esplorerà le capacità di full-text search di Oracle Text, una componente integrata di Oracle Database. Verranno presentati i concetti di base degli indici CONTEXT, CATSEARCH e CTXXPATH, spiegando come configurarli, ottimizzarli per diverse tipologie di dati testuali (documenti, email, XML) e utilizzarli nelle query. L'obiettivo è fornire una guida pratica per implementare ricerche testuali avanzate e performanti.
- **Sezione**: Oracle
- **Slot proposto**: (da definire)
- **Data nota**: 2026-06-08
- **Data issue**: 2026-06-08


### Mini-serie cross-DB sulle enumerazioni (4 articoli, giugno 2026)

Quattro articoli in quattro settimane consecutive, stesso tono didattico (linee guida applicate come commento alle 4 issue):

1. **MySQL #86** — le tre strade in MySQL (ENUM nativo, CHECK, lookup). Slot **2026-06-02**
2. **PostgreSQL #87** — le tre strade in PostgreSQL (CREATE TYPE ENUM, CHECK, lookup). Slot **2026-06-09**
3. **Oracle #70** — le tre strade in Oracle + chiusura confronto cross-DB. Slot **2026-06-16**
4. **Oracle #88** — deep-dive verticale: evoluzione delle feature 19c → 21c → 23ai → 26ai. Slot **2026-06-23**

I quattro articoli si linkeranno reciprocamente nella sezione "Aggancio cross-DB".

### Articolo MySQL: Enumerazioni con ENUM nativo, CHECK e tabelle lookup — Issue #86
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/86
- **Concept**: Le tre strade per modellare enumerazioni in MySQL (ENUM nativo, CHECK constraint da 8.0.16+, tabelle di lookup con FK). Tono didattico con caso reale. Valorizzazione di ENUM nativo come feature distintiva di MySQL, ma onestà sui limiti (case-insensitive, ALTER TABLE per modifiche, ordinamento posizionale). Primo pezzo della mini-serie cross-DB.
- **Sezione**: MySQL
- **Slot proposto**: 2026-06-02
- **Data nota**: 2026-03-31
- **Data issue**: 2026-05-11

### Articolo PostgreSQL: Enumerazioni con CREATE TYPE ENUM, CHECK e tabelle lookup — Issue #87
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/87
- **Concept**: Le tre strade per modellare enumerazioni in PostgreSQL (CREATE TYPE ... AS ENUM, CHECK constraint, tabelle di lookup con FK). Valorizzazione del tipo ENUM PostgreSQL (case-sensitive, ordinabile, transaction-safe) e della feature chiave ALTER TYPE ADD VALUE. Secondo pezzo della mini-serie cross-DB.
- **Sezione**: PostgreSQL
- **Slot proposto**: 2026-06-09
- **Data nota**: 2026-03-31
- **Data issue**: 2026-05-11

### Articolo Oracle: Enumerazioni - evoluzione delle feature da 19c a 26ai — Issue #88
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/88
- **Concept**: Deep-dive verticale Oracle che chiude la mini-serie. Come si modellavano le enumerazioni in 19c (solo CHECK e lookup), cosa cambia in 21c, l'arrivo di SQL Domains in 23ai, le Assertions in 26ai. Tabella riepilogativa CHECK / Lookup / Domain / Assertion x 19c / 21c / 23ai / 26ai.
- **Sezione**: Oracle
- **Slot proposto**: 2026-06-23
- **Data nota**: 2026-05-11
- **Data issue**: 2026-05-11

### Articolo PM: UML e RUP - storia dei Three Amigos — Issue #85
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/85
- **Concept**: Spiegazione a un collega su cosa siano UML/RUP diventata storia: i "Three Amigos" (Booch, Rumbaugh, Jacobson) da rivali a co-autori dentro Rational Software, fusione delle tre metodologie object-oriented, standardizzazione OMG, arrivo di Agile/Scrum, nicchia di sopravvivenza di RUP in contesti regolamentati (brevetti, medicale, aviazione). Angolo "storia umana di collaborazione" + filo del presente con Agile.
- **Sezione**: Project Management
- **Data nota**: 2026-05-11
- **Data issue**: 2026-05-11

### Articolo PM: L'importanza della documentazione progettuale — Issue #66
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/66
- **Data nota**: 2026-03-29
- **Data issue**: 2026-03-30

## Da approfondire

### Articolo Oracle: Assertions in Oracle 26ai
- **Sezione**: Oracle
- **Concept**: Le Assertions sono vincoli di integrita cross-tabella introdotti in Oracle 26ai. Sintassi SQL standard (CREATE ASSERTION ... CHECK), espressioni existential e universal. Feature nuova che pochi conoscono — potenziale articolo forte. Parzialmente coperto dall'articolo #88 (Oracle evoluzione 19c→26ai) come sezione finale, ma resta materiale per un eventuale approfondimento dedicato.
- **Fonte**: https://oracle-base.com/articles/26/assertions-26
- **Data nota**: 2026-03-31

## Idee feature sito / marketing

### Mailing list per notifica nuovi articoli
- **Sezione**: Sito / Marketing
- **Concept**: Dare agli utenti la possibilità di iscriversi a una mailing list per essere avvisati dei nuovi articoli (e potenzialmente di contenuti esclusivi: approfondimenti, anticipazioni, note a margine non pubblicate nel blog). Target: DBA, architetti, CTO che preferiscono email a RSS o LinkedIn.
- **Valutazione attuale**: da rimandare. Il blog è troppo giovane (1 mese, 31 articoli), l'audience tecnica usa RSS (già generati da Hugo automaticamente) e LinkedIn per seguire. Ora una mailing list duplicherebbe questi canali senza valore aggiunto reale.
- **Quando rivalutare**: tra 3-6 mesi (luglio-ottobre 2026), quando:
  - I dati di Search Console e analytics mostrano un'audience consolidata
  - Si sarà capito chi legge e cosa cerca
  - Si avrà un'idea di quale contenuto "extra" offrire agli iscritti rispetto al blog pubblico
- **Scelte tecniche candidate** (da rivalutare al momento della decisione):
  - **Buttondown**: privacy-friendly, minimal, €9/mese dopo i primi 100 iscritti. Embed form leggero, markdown-native, GDPR-ready
  - **ConvertKit / Kit**: creator-focused, piano free fino a 1000 iscritti, automazioni più avanzate
  - **Substack**: gratuito ma "proprietario", rischia di spostare contenuto fuori dal blog
  - **ListMonk self-hosted**: zero costi ricorrenti, ma da gestire manualmente (setup SMTP, backup lista)
- **Requisiti obbligatori per GDPR**:
  - Form con checkbox di consenso esplicito
  - Double opt-in (conferma via email prima dell'iscrizione effettiva)
  - Link di disiscrizione in ogni email
  - Aggiornamento privacy policy con base giuridica del trattamento (consenso art. 6.1.a GDPR)
  - Retention policy chiara
- **Pre-requisito "soft"**: definire prima un tema editoriale della newsletter che NON sia solo "link al nuovo articolo" (per evitare di duplicare RSS/LinkedIn)
- **Data nota**: 2026-04-21

### Log delle azioni / engineering log del sito
- **Sezione**: Sito / Trasparenza
- **Concept**: Pagina pubblica `/log/` con elenco cronologico delle azioni fatte sul sito giorno per giorno: modifiche al layout, articoli pubblicati, fix tecnici, decisioni di design. Stile *engineering log*, non *diary personale*: bullet asciutti, niente celebrazioni di sé, solo fatti. Coerente col posizionamento Database Strategy: mostra che il sito è curato come un sistema vivo, applicando la stessa mentalità DBA al sito stesso (osservabilità, tracciabilità, post-mortem).
- **Target**: altri tecnici curiosi del processo, eventuali clienti che vogliono vedere un fornitore "vivo" e metodico, archivio personale per ricordare il "perché" di una decisione presa mesi prima.
- **Tre forme possibili**:
  - **Auto da git log**: pagina generata da Hugo a ogni build, derivata dai commit. Pro: zero manutenzione, sempre aggiornato. Contro: i messaggi commit sono tecnici e vanno filtrati/riscritti
  - **Manuale asciutto**: pagina aggiornata a mano, una riga al giorno max. Pro: tono curato e selezionato. Contro: alta probabilità di abbandono dopo 2-3 settimane se ci si dimentica
  - **Ibrido (consigliato)**: auto-generato dai commit + override manuale settimanale per "summary di alto livello". Bilanciamento sostenibile
- **Stile imprescindibile**: niente celebrazione ("oggi ho fatto tante cose"), niente narrativa personale, solo fatti tecnici. Es. "redesign /tags/ raggruppato per sezione" invece di "ho dedicato l'intera giornata al redesign della pagina tag e finalmente sono soddisfatto del risultato".
- **Domande aperte da chiarire prima di implementare**:
  - Granularità: quotidiana, settimanale, per release?
  - Visibilità: link nel footer, voce di menu, o solo accessibile via URL diretto?
  - Tutte le modifiche o solo quelle "rilevanti per il lettore"? (es. fix di un typo non serve)
  - Retention: tutto lo storico o ultimi 6-12 mesi?
- **Pattern di riferimento (da studiare)**: `/changelog` di Linear, `/now` di Derek Sivers, `build log` di @levelsio, GitHub releases.
- **Data nota**: 2026-04-28
