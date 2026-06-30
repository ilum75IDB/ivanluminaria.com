# WRITER_BRIEFING — stile per la stesura degli articoli del blog

> **Single source of truth** per chi (umano o agent AI) scrive un nuovo articolo per il blog tecnico di Ivan Luminaria. Consolida le regole stilistiche, di tono e di struttura sparse in `CLAUDE.md`, `AI_CONTENT_GUIDELINES.md` e `DESCRIZIONE_PROGETTO_DATABASE_STRATEGY_BLOG.md`. Per il vocabolario di **frasi da evitare** vedi il file dedicato `STILE_LINGUISTICO.md`.

---

## 1. Identità del blog

Questo blog è un progetto tecnico e di portfolio professionale dedicato a **database engineering**, **data architecture** e **strategie di performance**. Tre obiettivi:

1. Condividere conoscenza pratica sui database (Oracle, PostgreSQL, MySQL) e sui sistemi Data Warehouse: funzionamento interno, performance tuning, decisioni architetturali.
2. Dimostrare competenza professionale costruita su 30 anni di progetti reali.
3. Diventare nel tempo una **risorsa di riferimento** sulla strategia dei database e sulle pratiche di engineering, non un blog di tutorial introduttivi.

Il principio guida:

> I database non sono semplici componenti software. Sono infrastrutture strategiche che determinano prestazioni, affidabilità e scalabilità dei sistemi digitali.

Gli articoli sono **saggi tecnici** o **case study ingegneristici**, non contenuti marketing né tutorial superficiali.

---

## 2. Pubblico di riferimento

Si scrive **per pari**:

- Database engineer e DBA in produzione
- Backend engineer che lavorano con dati su scala
- Data architect e CTO
- Technical decision maker

Si assume che il lettore:

- conosca SQL e i concetti base di RDBMS
- lavori con sistemi in produzione (non con corsi tutorial)
- conosca cosa sono indici, query plan, vincoli, transazioni
- sia interessato a performance, affidabilità, manutenibilità

Il blog **non è per principianti assoluti**: evitare spiegazioni base tipo "che cos'è una primary key" a meno che non siano centrali al punto dell'articolo. Quando un concetto base serve come ancora narrativa, citarlo brevemente assumendo che il lettore lo sappia già.

---

## 3. Voce e tono

Tono **tecnico, analitico, pragmatico, basato sull'esperienza**. Lo stile è quello di un ingegnere senior che racconta cosa è successo davvero in un progetto e cosa ha imparato.

**Evita** (anti-pattern di tono):

- Linguaggio marketing ("scopri il segreto di...", "rivoluziona il tuo workflow")
- Tono entusiastico-promozionale ("è incredibile come PostgreSQL...")
- Affermazioni assolute ("il modo migliore", "la verità è che")
- Generalizzazioni vuote ("i database sono importanti")
- Spiegazioni superficiali da SEO

**Preferisci**:

- Ragionamento di causa-effetto ("la query era lenta **perché** l'optimizer scegliesse hash join con statistiche stale")
- Implicazioni di performance e architettura ("la conseguenza in produzione è stata...")
- Scenari reali concreti con numeri ("4 ore di caricamento, 25 minuti dopo il fix, +400% parse")
- Trade-off espliciti ("dipende dal contesto: se hai X usa Y, se hai Z usa W")

---

## 4. Anti-pattern espliciti (no AI tells, no clickbait, no eroe-salvatore)

### 4.1 No AI tells

Mai usare formule tipiche da output LLM:

- "In conclusion..." / "In conclusione..."
- "It's worth noting that..." / "Va notato che..."
- "Let's dive in..." / "Immergiamoci..."
- "In today's fast-paced world..."
- Liste puntate compulsive dove un paragrafo basterebbe
- Frasi troppo perfettamente bilanciate (3 pro + 3 contro, 5 step rigidi)

Varia la lunghezza delle frasi. Usa giri colloquiali. Lascia trasparire opinioni. Scrivi come un umano stanco al lunedì mattina, non come un'API in cerca di approvazione.

### 4.2 No clickbait e no auto-affermazioni di onestà

Mai usare:

- "Quello che nessuno ti dice..." / "Che nessuno sa..."
- "Il segreto che..."
- "Diciamoci la verità" / "Ad essere sinceri" / "Senza giri di parole" / "Raccontati onestamente" / "Senza pietà"

Il valore dell'articolo emerge **dai dettagli concreti**, non da promesse. Se il racconto è onesto, lo si vede dai numeri e dalle confessioni nei passaggi tecnici — non serve dichiararlo come tic da blogger.

Preferisci titoli di sezione descrittivi come "I limiti, racconti dall'esperienza", "Il caso concreto", "Cosa è andato storto" — non "La verità su Oracle".

### 4.3 No tono "eroe-salvatore"

Evitare di costruire ogni racconto come la storia in cui l'autore, da solo, salva il progetto/cliente/azienda da un disastro epocale. Smussa il protagonismo:

- Riconosci il **contributo del team**, del DBA del cliente, di un collega che ha avuto l'intuizione, del vendor, di un blog post letto al momento giusto, di una vecchia nota di Tom Kyte
- Preferisci forme collettive: "abbiamo capito che…", "il team ha proposto…", "ci siamo accorti che…"
- Evita le forme egocentriche: "ho risolto da solo…", "nessuno aveva visto che…", "sono stato l'unico a capire…"
- Anche i risultati vanno raccontati con misura: invece di "ho salvato un sistema critico", scrivi "il caricamento è passato da 4 ore a 25 minuti — non magia, una settimana di profiling e una conversazione fortunata col DBA del cliente"

Vale anche per i **titoli**: niente "come ho salvato…", "il segreto che ho scoperto…", "quello che nessuno ha capito tranne me…".

Il valore tecnico deve emergere **dall'analisi e dal dettaglio**, non dall'enfasi sul protagonismo dell'autore.

### 4.4 Riferimenti temporali vicini

Evitare riferimenti troppo indietro nel tempo (es. "due anni fa", "tre mesi fa") a meno che il contesto narrativo non lo richieda. Preferire:

- "l'altro giorno"
- "qualche giorno fa"
- "ieri" / "la settimana scorsa" / "la scorsa settimana"
- "questa mattina"

Se l'articolo richiede un arco temporale più lungo (es. "il mese precedente", "un paio di mesi fa"), **giustificarlo nel testo** con frasi tipo: "È un po' che volevo scrivere su questo argomento e non ho trovato il tempo… finalmente eccomi" o simili.

### 4.5 No vocabolario tossico

Vedi `STILE_LINGUISTICO.md` per la tabella alfabetica completa (88 voci) di parole/frasi da evitare con relative sostituzioni e tema linguistico. Esempi: `forse` → `probabilmente`, `magari` → `definiamo`, `però` → `e al tempo stesso`, `problema` → `situazione`, `bisogna` → `scegliamo di`.

In articolo tecnico le voci negative descrittive (es. "non si possono rimuovere valori in modo nativo") sono **constatazioni di fatto** e possono restare. Il filtro si applica ai passaggi narrativi e personali, non alle constatazioni tecniche.

---

## 5. Settori clienti reali (rotation tra articoli)

Nei racconti e negli aneddoti, **alternare i settori dei clienti** per cui Ivan ha lavorato davvero. **Non inventare settori in cui non ha mai lavorato** (es. retail di articoli sportivi, e-commerce moda, gaming, food delivery, foodtech, fintech consumer, cripto). Inventare settori falsi rende i racconti smentibili.

### Settori reali — lista di consultazione rapida

| Settore                                | Clienti reali (riferimenti per autenticità interna) |
|----------------------------------------|-------------------------------------------------------|
| Assicurazioni & crediti commerciali    | ATRADIUS (Surety, multi-paese EU), Generali, RAS     |
| Telecomunicazioni (Telco)              | TIM (anche via HUAWEI), Vodafone IT/ES, TRE, Telecom |
| Banking & Finance                      | Banca d'Italia, FINWAVE                              |
| Pubblica Amministrazione               | Vari enti PA (via AUSELDA AED GROUP)                 |
| Postale & logistica                    | Poste Italiane (~1500 istanze MySQL/PostgreSQL)      |
| Trasporti & mobilità                   | FAI Service (cooperativa autotrasporti), Telepass    |
| Farmaceutico                           | Menarini (via Oracle Italia)                         |
| Automotive (storico, anni '90)         | Rover Italia (via S.EL.DAT.)                         |

### Convenzione di anonimizzazione

Quando il racconto richiede un settore generico, scegli uno tra quelli sopra **senza nominare il cliente specifico**:

- "un grande gruppo assicurativo italiano"
- "un operatore telco mobile"
- "una banca commerciale"
- "un'azienda della Pubblica Amministrazione"
- "un operatore postale e logistico nazionale"
- "una cooperativa di autotrasporti"
- "un grande gruppo farmaceutico italiano"
- "un costruttore automotive europeo (storico anni '90)"

### Regola di rotation

**Alternare i settori tra articoli successivi**. Mostra esplicitamente la rotation quando rilevante: "ultimi 3 articoli: Telco / Banking / Postale → questo articolo usa Assicurazioni".

---

## 6. Struttura tipica dell'articolo

Pattern editoriale ricorrente (può variare ma è la base):

1. **Aggancio reale** — apertura con un aneddoto, caso vissuto, ticket arrivato, dato sorprendente. **Mai** aprire con "I database sono importanti perché...".
2. **Problema/Situazione** — cosa stava succedendo, con dettagli concreti (numeri, schema fittizio ma realistico, comportamento osservato)
3. **Spiegazione tecnica** — perché succede così; come funziona davvero il pezzo del sistema in questione; cosa fa l'optimizer/il lock manager/il planner sotto il cofano
4. **Strategia di soluzione o trade-off** — cosa si è scelto e perché; alternative considerate e scartate; cosa cambia in produzione
5. **Implicazioni di performance/architettura** — ricadute sul sistema più ampio, sulla manutenibilità, sui costi
6. **Chiusura no-eroe** — takeaway che valorizza team/esperienza/processo, non eroismo individuale. Varianti accettate: "Confronto cross-DB", "Conclusioni e best practice", "Chiusura della serie".

L'articolo deve trasmettere **knowledge transfer da un ingegnere esperto** a pari, non lezioni da maestro a allievi.

---

## 7. Convenzioni Markdown (output)

L'output del writer è il **body Markdown puro** dell'articolo. Il frontmatter Hugo viene aggiunto/aggiornato fuori dal writer (da web-orchestrator o manualmente).

### Heading

- **`##`** per sezioni principali, **`###`** per sotto-sezioni
- **MAI `#` (h1)** — Hugo lo aggiunge dal frontmatter `title`

#### Stile dei titoli di sezione (REGOLA TASSATIVA)

I titoli `##` devono essere **specifici al contenuto della sezione**, possibilmente **narrativi/evocativi**, mai etichette generiche da "scaletta di un compito di scuola".

**Vietati** (titoli pigri, da rigettare sempre, anche se la sezione fa effettivamente quel mestiere):

- ❌ `## Chiusura`
- ❌ `## Conclusione` / `## Conclusioni`
- ❌ `## Riflessioni` / `## Riflessione finale`
- ❌ `## Considerazioni finali`
- ❌ `## Note finali` / `## Note`
- ❌ `## Sommario` / `## Sintesi`
- ❌ `## Pensieri`
- ❌ `## Conclusioni e takeaway`
- ❌ `## Introduzione` (l'articolo inizia, non ha bisogno di annunciarlo)
- ❌ `## Premessa`

**Preferiti** (titoli che richiamano un personaggio, un dettaglio, un'immagine specifica della sezione):

- ✅ `## Le domande di Claudio` (per una sezione dove le domande del junior consolidano le scelte)
- ✅ `## Il giorno dopo, in silenzio` (per una sezione che racconta il successo silenzioso del lavoro fatto)
- ✅ `## Quello che resta sul quaderno` (per una sezione che condensa il know-how trasferito)
- ✅ `## La telefonata delle 3` (per una sezione che apre con l'episodio chiave)
- ✅ `## Quando il backup ha salvato sette anni di dati` (per una sezione tecnica con ancora narrativa concreta)
- ✅ `## ORA-00205 e la lezione che non è quella ovvia` (titolo che usa il codice errore come ancora + suggerisce la sorpresa)

Regola pratica: prima di scrivere un titolo, chiediti **"un lettore esperto, leggendo solo questo titolo, capisce di cosa parla questa sezione specificamente in questo articolo, oppure potrebbe stare in qualsiasi articolo del blog?"**. Se sta in qualsiasi articolo, non è un buon titolo.

Vale anche per la sezione **finale** dell'articolo: il titolo della chiusura deve essere narrativo/specifico (es. "Le domande di Claudio", "Il giorno dopo", "Quello che resta del runbook"), MAI "Chiusura" o "Conclusioni". Le sezioni `## Fonti ufficiali` e `## Glossario candidato` sono **eccezione**: hanno nome fisso convenzionale.

**Per le traduzioni** (EN/ES/RO): il traduttore deve **mantenere il carattere narrativo/specifico del titolo IT**. Se l'IT dice `## Le domande di Claudio`, EN dice `## Claudio's questions` — non `## Closing` né `## Conclusion`. Non normalizzare mai un titolo narrativo a un'etichetta generica in traduzione.

### Code blocks

Sempre con linguaggio dichiarato:

- ` ```sql ` per query SQL
- ` ```bash ` per comandi shell
- ` ```python ` per codice Python
- ` ```yaml ` per config
- ` ```text ` per output stdout o file di log

I commenti dentro i code block possono essere in italiano (es. `-- aggiunto per perf`).

### Citazioni e documenti in lingua originale

Quando citi un **documento storico, un manifesto, uno slogan o una frase celebre** nella sua lingua originale (es. le quattro coppie di valori dell'Agile Manifesto in inglese, un motto, una definizione canonica), riporta **sempre l'originale seguito dalla traduzione affiancata** nella lingua del file, sulla stessa riga, nel formato:

```
*testo nella lingua originale* — traduzione nella lingua del file
```

Esempio (file italiano):

- *Working software over comprehensive documentation* — Il software funzionante più che la documentazione esaustiva

**Mai** lasciare un blocco o un elenco in lingua straniera senza traduzione: il lettore deve capirlo senza cercare altrove. La regola vale in tutte le lingue del sito (IT/EN/ES/RO): l'originale resta invariato, cambia solo la lingua della parte tradotta. Nel file EN, se l'originale è già inglese, non serve il doppione.

### Dati e scenari (anonimizzati)

Quando l'articolo cita comandi/sintassi/parametri/feature tecnici, includi una sezione opzionale con:

- Hostname mascherati: `mysql-node-01`, `oracle-prod-eu-03`, senza dominio
- Schema fittizi ma realistici: `customer`, `order_log`, `payment_audit`
- Numeri concreti (righe, GB, ms, versioni)
- Metriche before/after quando rilevanti

**Mai citare clienti reali** — vedi §5 per le formule generiche.

Se l'articolo è puramente narrativo (PM, opinion, racconto senza comandi citabili), **ometti** questa sezione: non lasciare placeholder vuoti.

### Sezione `## Fonti ufficiali` (prima del Glossario)

**Obbligatoria** se l'articolo cita comandi/sintassi/parametri/flag che il lettore potrebbe copiare in produzione.

Notazione:

- Nel corpo: nota numerica `[1]` `[2]` dopo l'affermazione tecnica
- A fine articolo (prima del Glossario):

```markdown
## Fonti ufficiali

1. Oracle Database SQL Language Reference 19c — [AUDIT (Unified Auditing)](https://docs.oracle.com/...)
2. PostgreSQL Documentation — [pg_stat_statements](https://www.postgresql.org/...)
```

**REGOLE**:

- **MAI inventare URL**. Se non hai un URL verificato, scrivi `<TODO: scout fonte ufficiale per "<termine>">` come placeholder visibile
- Domini autorevoli ammessi: `docs.oracle.com`, `www.postgresql.org/docs/`, `dev.mysql.com/doc/`, `mariadb.com/kb/`, `docs.percona.com`, `oracle-base.com` (Tim Hall), `docs.github.com`
- Target: 3-6 note per articolo tecnico, non 50. Devono pesare
- Per articoli narrativi puri (PM/opinion) scrivi: _"Articolo narrativo: sezione Fonti ufficiali non obbligatoria (nessun comando/sintassi/parametro citato)."_

### Sezione `## Glossario candidato` (ultima sezione)

**Sempre** presente come ultima sezione dell'articolo. Formato 5 voci brevi (30-50 parole ciascuna):

```markdown
## Glossario candidato

- **TERMINE** (contesto se rilevante) — definizione breve, 15-40 parole.
- **AWR** (Oracle) — Automatic Workload Repository: snapshot periodici di metriche di workload, base degli AWR report e di ADDM.
- ...
```

Selezione criteri (in ordine di priorità):

- **Acronimi** (es. AWR, SCD, ETL, MVCC)
- **Concetti tecnici specifici** (es. buffer pool, execution plan, hash join)
- **Tool o tecnologie** menzionate nell'articolo

**Riuso di termini esistenti**: ammesso al massimo 2 per articolo. Gli altri 3 devono essere nuovi, in modo che ogni articolo porti valore aggiunto al glossario complessivo.

> _Nota_: la conversione delle voci di glossario in mini-pagine `/glossary/<slug>/` (4 lingue ciascuna) è uno **step separato** del workflow editoriale, non scope del writer.

---

## 8. Lunghezza target

**1500-2500 parole** indicative. Lascia che sia la chiarezza a guidare, non il count rigido:

- < 800 parole = red flag "articolo troppo magro per essere utile"
- 800-1500 = corto ma accettabile per topic mirato (es. anti-pattern singolo, glossario espanso)
- 1500-2500 = sweet spot per saggio tecnico tipico
- 2500-3500 = articolo lungo, ammesso se la complessità lo richiede (es. comparazione cross-DB, migration story)
- \> 3500 = red flag "spezza in 2 articoli o taglia"

---

## 9. Output del writer — 3 titoli candidati in cima

L'output del writer (la bozza Markdown italiana finale) deve **iniziare** con un commento HTML che propone **3 alternative del titolo** per la review umana. Esempio:

```markdown
<!-- TITOLI CANDIDATI (review umana sceglie il preferito)
1. ENUM in PostgreSQL: 4 strategie a confronto
2. Modellare valori chiusi in PostgreSQL: ENUM, lookup table, CHECK, dominio
3. Quando NON usare un ENUM su PostgreSQL: storia di una migrazione complessa
-->

## Aggancio reale

[apertura dell'articolo, primo paragrafo del body...]
```

**Convenzioni**:

- Esattamente **3 titoli**, numerati `1.` `2.` `3.`
- Variare gli angoli: 1 narrativo/empatico, 1 più tecnico-keyword, 1 più storia/case study
- I 3 titoli non vengono renderizzati da Hugo (sono dentro un commento HTML) — servono solo all'editor umano in fase di approvazione bozza
- Il titolo definitivo viene scelto in fase di **approvazione bozza** (Step 4 del workflow editoriale webo) e applicato al frontmatter Hugo `title`

**Anti-pattern per i titoli**:

- ❌ "Come ho salvato un cluster MySQL da un disastro"
- ❌ "Il segreto di Oracle 19c che nessuno conosce"
- ❌ "Quello che PostgreSQL non vuole farti sapere"
- ✅ "Cluster MySQL ridondante: lessons learned dopo 18 mesi in produzione"
- ✅ "Statistiche stale in Oracle 19c: diagnostica e fix"
- ✅ "PostgreSQL VACUUM in pratica: cosa succede sotto il cofano"

---

## 10. Cosa NON è scope del writer

Per chiarezza, il writer (umano o LLM agent) produce **solo il body Markdown italiano + i 3 titoli candidati nel commento iniziale**. Tutto il resto è gestito separatamente:

| Aspetto | Quando viene fatto | Chi |
|---|---|---|
| Frontmatter Hugo (`title`, `date`, `draft`, `webo_status`) | Step 3 webo (`build_frontmatter` aggiunto post-stesura) | web-orchestrator |
| Traduzioni EN / ES / RO | Step 5 webo (cascade Sonnet→Gemini) | LLM separati |
| Generazione cover image | Step 6 webo (scope futuro #20, oggi solo prompt MD) | manuale + AI futura |
| Mini-pagine glossario `/glossary/<slug>/` | Step separato post-pubblicazione | manuale |
| Aggiornamento `HUGO_PUBLICATIONS_TABLE.md` e `GLOSSARIO_TERMINI.md` | Step 7 webo (Assegna data) | web-orchestrator |
| Pubblicazione (commit su `main` + GitHub Actions deploy) | Step 7 webo (cherry-pick atomico) | web-orchestrator |
| Post LinkedIn / Buffer schedule | Fase 3 futura | web-orchestrator |
| **SEO frontmatter** (`seoTitle` ≤65, `description` ≤160) in 4 lingue | Step di approvazione/traduzione | umano o LLM separato |

Il writer **si concentra sulla qualità del contenuto** in italiano; tutta la pipeline tecnica + multilingua + asset visivi + scheduling è gestita altrove.

---

## 11. Riferimenti rapidi (cross-link)

- **Vocabolario di parole/frasi da evitare** → `STILE_LINGUISTICO.md` (88 voci alfabetiche + 51 temi linguistici)
- **Workflow editoriale completo** (dall'idea alla pubblicazione, 9 step) → web-orchestrator `docs/workflow/publishing/WORKFLOW_DA_IDEA_A_PUBBLICAZIONE.md`
- **Step 3 dettagliato** (writer Sonnet, branch `publication-workflow`, frontmatter) → web-orchestrator `docs/workflow/publishing/STEP_03_BOZZA_IT.md`
- **Calendario festività** (slot scheduling) → `docs/HOLIDAYS_CALENDAR.md`
- **Tabella pubblicazioni** → `docs/HUGO_PUBLICATIONS_TABLE.md`

---

## Note di manutenzione

Questo file consolida e **sostituisce** le sezioni "writing articles" sparse in:

- `CLAUDE.md` punti 2-7, 10-11 (sezione `## Content Guidelines > Writing articles`)
- `AI_CONTENT_GUIDELINES.md` paragrafi 1, 2, 3, 4, 5, 7, 10 (in inglese)
- `DESCRIZIONE_PROGETTO_DATABASE_STRATEGY_BLOG.md` paragrafi 1, 6, 7, 9

Cosa **resta** nei file originali (non duplicato qui):

- `STILE_LINGUISTICO.md` — tabella vocabolario (consultata separatamente, è una reference tabular)
- `AI_CONTENT_GUIDELINES.md` § 6 (Image Generation Rules) e § 9 (Glossary Term Pages) — gestione cover image + mini-pagine glossario, scope di altri step
- `DESCRIZIONE_PROGETTO_DATABASE_STRATEGY_BLOG.md` §§ 2-5, 8, 10 — context architetturale Hugo + multilingua + filosofia + illustrazioni AI, irrilevante per il writer

Quando aggiorni le regole di stile, modifica **questo file** + sincronizza eventualmente `CLAUDE.md` con un link breve ("vedi `WRITER_BRIEFING.md`").

---

**Ultimo aggiornamento**: 2026-06-07 (creazione iniziale, draft consolidato).
