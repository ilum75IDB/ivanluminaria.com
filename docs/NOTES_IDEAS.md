# Note e Idee per futuri articoli

## Issue create

### Articolo PM: L'importanza della documentazione progettuale — Issue #66
- **Issue**: https://github.com/ilum75IDB/ivanluminaria.com/issues/66
- **Data nota**: 2026-03-29
- **Data issue**: 2026-03-30

## Da approfondire

### Articolo Oracle: Assertions in Oracle 26ai
- **Sezione**: Oracle
- **Concept**: Le Assertions sono vincoli di integrita cross-tabella introdotti in Oracle 26ai. Sintassi SQL standard (CREATE ASSERTION ... CHECK), espressioni existential e universal. Feature nuova che pochi conoscono — potenziale articolo forte.
- **Fonte**: https://oracle-base.com/articles/26/assertions-26
- **Data nota**: 2026-03-31

### Articolo MySQL: Enumerazioni in MySQL con caso reale
- **Sezione**: MySQL
- **Concept**: Come gestire le enumerazioni in MySQL (ENUM nativo, CHECK constraint, tabelle di lookup). Caso reale concreto. Da scrivere prima dell'articolo Oracle #70 per poterlo linkare come confronto cross-database.
- **Collegamento**: si linka dall'articolo #70 (enumerazioni Oracle) e viceversa
- **Data nota**: 2026-03-31

### Articolo PostgreSQL: Enumerazioni in PostgreSQL con caso reale
- **Sezione**: PostgreSQL
- **Concept**: Come gestire le enumerazioni in PostgreSQL (CREATE TYPE ... AS ENUM, ALTER TYPE ADD VALUE, pro e contro). Caso reale concreto. Da scrivere prima dell'articolo Oracle #70 per poterlo linkare come confronto cross-database.
- **Collegamento**: si linka dall'articolo #70 (enumerazioni Oracle) e viceversa
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
