# Skill: blog-idea-to-issue

Quando invocata, **trasforma un'idea di articolo** (in chat o referenziata in `docs/NOTES_IDEAS.md`) **in una issue GitHub strutturata "rich"** pronta per essere creata su `ilum75IDB/ivanluminaria.com`, e gestisce il post-creazione aggiornando i file di tracciamento.

Skill **project-local** in `.claude/skills/blog-idea-to-issue/` → disponibile solo in questo progetto. Specificità del template editoriale e dei file di tracking giustificano lo scope locale.

L'obiettivo è abilitare un **agent automatico futuro** che, dato un input idea, produca una issue completa e standardizzata (kick-off doc per la stesura), riducendo il lavoro manuale di Ivan a una sola approvazione + esecuzione del comando `gh issue create`.

---

## Scope

**Solo `blog-article`** — la skill non gestisce issue di tipo `bug`, `enhancement` o feature del sito (per quelle si usa la skill globale `github-crea-issue` o si scrive il comando a mano). Label sempre applicate:

- `blog-article` (sempre)
- `<sezione>` (esattamente una tra: `oracle`, `postgresql`, `mysql`, `data-warehouse`, `project-management`, `ai-manager`)

---

## Quando attivarsi

Trigger validi (l'utente intende esplicitamente convertire una idea in issue):

- `/blog-idea-to-issue <descrizione idea>`
- `/blog-idea-to-issue --from-notes <riferimento idea da NOTES_IDEAS.md>`
- "trasforma questa idea in issue: …"
- "crea una issue per un articolo su X"
- "promuovi a issue l'idea Y" / "promuovi l'idea su Y a issue"
- "scrivimi la issue per l'articolo su X"

**NON attivarsi** per richieste generiche tipo "fammi vedere le idee" (→ Ideas dashboard rule del CLAUDE.md), "creiamo una issue per quel bug" (→ skill `github-crea-issue` o comando a mano).

---

## Argomenti

| Forma | Comportamento |
|---|---|
| `/blog-idea-to-issue <testo libero>` | Auto-detect: tratta il testo come idea libera. Genera il body rich a partire dal testo. |
| `/blog-idea-to-issue --from-notes <riferimento>` | Forza lookup in `docs/NOTES_IDEAS.md`. Il `<riferimento>` può essere: (a) titolo o frammento del titolo di una idea sotto `## Da approfondire`, (b) parte del **Concept** se distintiva. La skill fa match case-insensitive e mostra all'utente l'idea trovata per conferma. |
| `/blog-idea-to-issue --level=minimal` | Genera body in versione minimal (solo Concept, Struttura proposta 3-5 punti, Sezione, Settore business, "Fonti ufficiali da scoutare" obbligatoria). Default: `rich`. |
| `/blog-idea-to-issue --dry-run` | Genera tutto e mostra all'utente, ma **NON** produce il comando `gh issue create` finale. Utile per ispezionare il body senza intenzione di pushare. |
| `/blog-idea-to-issue --usage` | Stampa istruzioni + esempi e termina. |

Default level: **rich**. Argomenti combinabili (`--from-notes 'enumerazioni Oracle' --level=minimal`).

---

## Auto-detect input (default)

Se l'utente non passa `--from-notes` esplicito, la skill prova entrambe le strade in ordine:

1. **Match testuale su `docs/NOTES_IDEAS.md`**: cerca se il testo dell'utente corrisponde (anche parzialmente, ≥60% sovrapposizione di parole-chiave significative) al titolo o al **Concept** di una idea sotto `## Da approfondire`. Se trova **un solo match con confidenza alta**, procede come `--from-notes`. Se trova **più match**, chiede all'utente quale usare via `AskUserQuestion`.
2. **Fallback a testo libero**: se nessun match plausibile, tratta il testo come idea libera.

Mostra sempre all'utente, all'inizio della procedura, qual è il branch scelto e perché — l'utente può correggere prima che la skill prosegua.

---

## Procedura operativa

### Passo 0 — Pre-flight check

1. **CWD = root di `ivanluminaria.com`**: verifica con `git rev-parse --show-toplevel`. Se non lo è (es. siamo in un'altra cartella, o repo diverso), errore chiaro + suggerimento `cd <path>` + termina.
2. **`gh` CLI disponibile**: `which gh` + `gh auth status`. Se `gh` manca o non autenticato, errore + suggerisci `gh auth login` + termina. (Nota: storicamente la CLAUDE.md del progetto diceva "gh non disponibile" → quella sezione è obsoleta; oggi `gh` è installato).
3. **File di tracking presenti**: `docs/NOTES_IDEAS.md`, `docs/GITHUB_ISSUES.md`, `docs/HUGO_PUBLICATIONS_TABLE.md`. Se mancano, segnala ma procedi (alcuni passi del post-creazione verranno saltati).
4. **`docs/HOLIDAYS_CALENDAR.md`**: leggi all'occorrenza per gestire shift festività (vedi Passo 4).

### Passo 1 — Risolvi l'input

1. Auto-detect (vedi sezione "Auto-detect input"): determina se l'input è un riferimento a `NOTES_IDEAS.md` o un testo libero.
2. **Se da `NOTES_IDEAS.md`**: estrai dalla nota il titolo, il Concept, la Sezione (se presente), la Fonte (se presente), la Data nota. Mostra all'utente l'idea trovata e chiedi conferma.
3. **Se testo libero**: estrai dal testo gli elementi che riesci a inferire (sezione tecnologica, tema, eventuali numeri/scenari menzionati).
4. **Se la sezione non è inferibile**: chiedi all'utente via `AskUserQuestion` quale sezione del blog (`oracle` / `postgresql` / `mysql` / `data-warehouse` / `project-management` / `ai-manager`).

### Passo 2 — Calcola il numero della prossima issue (best-effort)

```bash
gh issue list --repo ilum75IDB/ivanluminaria.com --state all --limit 1 --json number
```

Il prossimo numero **probabile** è `<ultimo>+1`. **Non garantito** (qualcuno può aprire una issue tra l'esecuzione del comando e il momento in cui la skill lo prepara): la skill usa il numero per **anticipare** il prossimo (es. nella sezione "Glossario candidato" quando riferisce ad articolo correlato), ma il numero reale lo conosciamo solo **dopo** l'esecuzione di `gh issue create`. Mai usare il numero anticipato in modo load-bearing.

### Passo 3 — Scout delle fonti ufficiali (WebSearch)

**Questa è la sezione più importante della skill** — l'utente l'ha chiesta esplicitamente: la issue deve **sempre includere l'istruzione di creare la sezione "Fonti ufficiali"** nell'articolo, e idealmente proporre già 3-6 candidati pre-scoutati.

1. Identifica nel concept i **comandi, parametri, sintassi, feature di prodotto** che plausibilmente andranno citati nell'articolo (es. `pg_stat_statements`, `binlog_expire_logs_seconds`, `CREATE DOMAIN`, `wsrep_cluster_size`, `AUDIT POLICY`).
2. Per ciascuno, usa **`WebSearch`** per cercare la doc ufficiale del vendor. **Allowlist domini** ufficiali considerati validi:
   - `docs.oracle.com` (Oracle Database)
   - `www.postgresql.org/docs/` (PostgreSQL)
   - `dev.mysql.com/doc/` (MySQL)
   - `dev.mysql.com/blog-archive/` (MySQL engineering blog)
   - `mariadb.com/kb/` (MariaDB)
   - `galeracluster.com/library/documentation/` (Galera)
   - `docs.percona.com` (Percona)
   - `oracle-base.com` (Tim Hall — semi-ufficiale, ampiamente accettato per Oracle)
   - `docs.kernel.org` (Linux kernel)
   - `redhat.com/.../documentation` (RHEL)
   - `docs.github.com` (GitHub Actions/CI)
3. **Mai inventare URL** (regola globale Ivan/Claude). Se WebSearch non trova un risultato accettabile, scrivi `<TODO: scout fonte ufficiale per "<termine>">` come placeholder.
4. **Target**: 3-6 fonti per articolo tecnico. Per articoli puramente narrativi (es. PM su standup, Smart Working, racconti), la sezione può essere meno densa o assente — in tal caso scrivi "Articolo narrativo: sezione 'Fonti ufficiali' non obbligatoria (nessun comando/sintassi/parametro citato)" e procedi.
5. **Output di questo passo** = una lista di candidati pronti da inserire nella sezione `## Fonti ufficiali da scoutare` del body issue.

### Passo 4 — Calcola lo slot di pubblicazione candidato

1. Leggi `docs/HUGO_PUBLICATIONS_TABLE.md` per ricavare il **Next available slot** (martedì successivo al più recente articolo programmato).
2. Leggi `docs/HOLIDAYS_CALENDAR.md` per verificare festività italiane: se lo slot martedì è festivo, **shift a mercoledì** stessa settimana (vedi regola 11 del CLAUDE.md).
3. Lo slot è una **proposta**, non un commitment — l'utente potrà cambiarlo dopo la creazione.

### Passo 5 — Costruisci il body issue (template rich)

Salva il body in `/tmp/issue-body.md` (file temporaneo che verrà letto da `--body-file`). Struttura completa, con sezioni omettibili **solo** se genuinamente non applicabili al tema:

```markdown
## Concept

<2-4 paragrafi: cosa racconta l'articolo, perché è interessante, l'angolo distintivo.
Se da NOTES_IDEAS.md: riprendi il Concept della nota e arricchiscilo.
Se testo libero: genera il Concept dal testo dell'utente.>

## Tono e angolo editoriale

- **Taglio**: <didattico / racconto / tecnico-pratico / storia umana>
- **Prospettiva**: prima persona, racconto del campo (esperienza diretta)
- **Caso reale come ancora** (se applicabile): <breve descrizione situazione/cliente/scenario>
- **Tono no-eroe**: <es. "il fix è stato diagnosi corretta + valori ragionevoli, non salvataggio epico">
- **Niente clickbait**: niente "quello che nessuno ti dice", "il segreto…", auto-affermazioni di onestà
- **Settore business** (rotation dai settori reali da CV): <vedi sezione sotto>

## Settore business (dal CV)

<scegli UNO settore reale dalla tabella sotto, alternando rispetto agli articoli recenti
per evitare di concentrarsi su uno solo. Mostra la rotation: "ultimi 3 articoli hanno usato
Telco / Banking / Postale → questo articolo usa Assicurazioni">

**Tabella settori reali** (da CV in `content/resumes/`):
- Assicurazioni & crediti commerciali (ATRADIUS, Generali, RAS)
- Telecomunicazioni — Telco (TIM, Vodafone IT/ES, TRE, Telecom)
- Banking & Finance (Banca d'Italia, FINWAVE)
- Pubblica Amministrazione (vari enti via AUSELDA AED GROUP)
- Postale & logistica (Poste Italiane)
- Trasporti & mobilità (FAI Service, Telepass)
- Farmaceutico (Menarini via Oracle Italia)
- Automotive storico anni '90 (Rover Italia via S.EL.DAT.)

**Anonimizzazione consigliata**: "un grande gruppo assicurativo italiano", "un operatore telco mobile",
"una banca commerciale", "un'azienda della Pubblica Amministrazione", "un operatore postale e logistico
nazionale", "una cooperativa di autotrasporti".

## Struttura proposta

1. **Apertura** — <hook narrativo concreto: situazione di partenza, ticket arrivato, dato sorprendente, aneddoto vissuto>
2. **<sezione 2>** — <dettaglio>
3. **<sezione 3>** — <dettaglio>
4. **<sezione 4>** — <dettaglio>
5. **<sezione 5>** — <dettaglio>
6. **<…fino a 8-10 sezioni se serve>**
N. **Chiusura no-eroe** — <takeaway che valorizza il team, l'esperienza, non l'eroismo individuale>

## Titoli candidati (3 ipotesi)

1. **<titolo principale proposto, narrativo/empatico, per il campo `title` del frontmatter>**
2. <alternativa A — variante più tecnica>
3. <alternativa B — variante più narrativa>

**Nota SEO**: il `title` (uno dei 3 sopra) va nel frontmatter dell'articolo per H1.
Il `seoTitle` (≤65 char, keyword-driven) va compilato in fase di stesura, **non** nella issue.

## Dati / scenario reali (anonimizzati)

<inserisci qui numeri, versioni, comandi, hostname mascherati, RAM, query, dimensioni tabelle,
metriche before/after. Per articoli narrativi puri: ometti questa sezione.>

Hostname suggeriti: `<tech>-node-01`, `<tech>-node-02`, ecc. (senza dominio).
Tabelle e schema: nomi fittizi ma realistici (es. `customer`, `order_log`, `payment_audit`).

## Fonti ufficiali da scoutare

> ⚠️ **OBBLIGATORIA** se l'articolo cita comandi/sintassi/parametri/flag che il lettore può copiare
> in produzione (regola 11 del CLAUDE.md). Pre-scoutate qui sotto le candidate; in fase di stesura
> verranno verificate, integrate e inserite come sezione `## Fonti ufficiali` numerata prima del Glossario,
> con note `[n]` nel corpo dell'articolo.

<Lista di 3-6 fonti scoutate via WebSearch, formato:>

1. **<Vendor>** — [<Titolo doc>](<URL ufficiale>) — copre: `<comando/feature>`
2. **<Vendor>** — [<Titolo doc>](<URL ufficiale>) — copre: `<comando/feature>`
3. <TODO: scout fonte ufficiale per "<termine non trovato>"> *(placeholder per stesura)*

## Glossario candidato (5 termini, almeno 3 nuovi)

> Da inserire come sezione `## Glossario` a fine articolo (regola 10 del CLAUDE.md).
> Verificare in `docs/GLOSSARIO_TERMINI.md` quali esistono già (max 2 riusati).

- **<Termine 1>** (nuovo) — <descrizione breve 1-2 frasi>
- **<Termine 2>** (nuovo) — <descrizione breve>
- **<Termine 3>** (nuovo) — <descrizione breve>
- **<Termine 4>** (riuso da articolo #<nn>) — <descrizione breve>
- **<Termine 5>** (nuovo) — <descrizione breve>

## Scena cover image (descrizione per prompt)

<5-10 righe: scena visiva concreta, metafora visiva che lega al tema, coerente con tono no-eroe
(se il tema è "no-eroe", la scena non mette il personaggio principale al centro). Da archiviare
poi in `docs/cover-image-prompts/<slug>.cover.md` allo step 7 del workflow di scrittura.>

## Sezione

<oracle | postgresql | mysql | data-warehouse | project-management | ai-manager>

## Slot proposto

<YYYY-MM-DD (giorno-settimana) — dal calendario editoriale, con eventuale shift festività>

Motivazione slot: <"next available slot dopo l'ultimo programmato" / "shift mercoledì per festività X">

## Collegamenti

<se applicabile:>

- Articolo correlato: #<nn> "<titolo>"
- Mini-serie: <descrizione posizione nella serie>
- Follow-up di: #<nn>

## Note

- **4 lingue**: IT (master), EN, ES, RO — tutte e 4 le versioni con stesso `date` di pubblicazione
- **SEO frontmatter**: `seoTitle` ≤65 char (keyword-driven) + `description` ≤160 char in tutte le 4 lingue
- **Sezione "Fonti ufficiali"** obbligatoria prima del Glossario se l'articolo cita comandi (regola 11)
- **Sezione "Glossario"** obbligatoria a fine articolo (regola 10), 5 termini, mini-pagine in `content/glossary/<slug>/`
- **Cover image**: solo prompt + filename (no placeholder), salvato in `docs/cover-image-prompts/<slug>.cover.md` (step 7)
- **Settori clienti**: variare tra articoli (regola 7), usare solo settori reali da CV
- **Anonimizzazione**: hostname, schema, cliente — sempre anonimizzati
```

### Passo 6 — Genera comando `gh issue create` finale

**Formato copia-incolla unico** (blocco singolo), seguendo le regole del CLAUDE.md (sezione "GitHub Issues > Regole di formattazione"):

```bash
cat > /tmp/issue-body.md << 'ISSUE_EOF'
<body completo del Passo 5>
ISSUE_EOF
gh issue create \
  --repo ilum75IDB/ivanluminaria.com \
  --title "Articolo <Sezione>: <titolo principale ASCII-safe>" \
  --label "<sezione>,blog-article" \
  --body-file /tmp/issue-body.md
```

**Regole hard sul titolo**:

- **Prefisso obbligatorio**: `"Articolo <Sezione>: "` dove `<Sezione>` è `Oracle` / `PostgreSQL` / `MySQL` / `DWH` / `PM` / `AI Manager` (formato leggibile, non lo slug della label).
- **Nessun carattere accentato**: à→a, è→e, é→e, ù→u, ò→o, ì→i. **Hard requirement** della shell zsh (regola 5 CLAUDE.md).
- **Nessun apice singolo non escapato**, nessun backtick, nessun `$()`. Il body usa `<<'ISSUE_EOF'` (quoted heredoc) → al suo interno **i backtick e i `$` sono safe**.
- **Lunghezza titolo**: max ~100 char (≤80 raccomandato). Il `seoTitle` ≤65 char è una cosa diversa e va nel frontmatter, non nel titolo issue.

### Passo 7 — Approvazione esplicita dell'utente

**Mai eseguire `gh issue create` automaticamente.** La skill mostra:

1. Il **body completo** della issue (output del Passo 5)
2. Il **comando finale** (output del Passo 6) come blocco di codice copia-incollabile
3. Una richiesta di approvazione via `AskUserQuestion`:
   - Opzione A: "Sì, eseguo io il comando dal mio terminale e ti dò il link"
   - Opzione B: "Modifica X prima" (l'utente può richiedere modifiche al body — il passo 5 si rifà)
   - Opzione C: "Annulla, non creiamo la issue"

Se Sì → vai al Passo 8. Se Modifica → torna al Passo 5 con il feedback. Se Annulla → segnala e termina.

### Passo 8 — Post-creazione: aggiornamento file di tracking

**L'utente esegue il comando** dal suo terminale e fornisce alla skill **il link della issue creata** (es. `https://github.com/ilum75IDB/ivanluminaria.com/issues/95`). Senza link, la skill non può procedere — chiedilo esplicitamente (regola CLAUDE.md: "chiedere sempre il link della issue appena creata").

Una volta ricevuto il link:

1. **Estrai il numero issue** dal link (regex `/issues/(\d+)`).
2. **Aggiorna `docs/GITHUB_ISSUES.md`**: aggiungi una nuova riga nella **sezione corrispondente** (`## Issue Aperte — Sezione <Sezione>`) con:
   ```
   | <nn> | <URL completo> | <titolo issue ASCII-safe> | aperta |
   ```
   Se la sezione della tabella non esiste ancora per quella sezione del blog, creala.
3. **Aggiorna `docs/NOTES_IDEAS.md`** (solo se l'idea veniva da lì):
   - **Sposta la nota** dalla sezione `## Da approfondire` alla sezione `## Issue create`
   - Riformatta nel pattern delle voci esistenti in `## Issue create`:
     ```
     ### <Titolo nota originale> — Issue #<nn>
     - **Issue**: <URL completo>
     - **Concept**: <riprendi dalla nota originale>
     - **Sezione**: <Sezione>
     - **Slot proposto**: <data dal Passo 4>
     - **Data nota**: <data nota originale>
     - **Data issue**: <data odierna YYYY-MM-DD>
     ```
4. **Commit + push** sul branch operativa corrente (mai diretto su `main` — regola globale). Format Conventional Commits italiano:
   ```
   docs(blog): tracciamento issue #<nn> <titolo sintetico>

   - GITHUB_ISSUES.md: aggiunta riga nella sezione <Sezione>
   - NOTES_IDEAS.md: nota promossa da "Da approfondire" a "Issue create"   <-- solo se applicabile
   ```
   Mai `--no-verify`, mai `--amend`, mai `Co-Authored-By: Claude`.

### Passo 9 — Riepilogo finale

Mostra all'utente:

- ✅ Issue `#<nn>` creata: `<URL>`
- ✅ `GITHUB_ISSUES.md` aggiornato (sezione `<Sezione>`)
- ✅ `NOTES_IDEAS.md` aggiornato (se applicabile)
- ✅ Commit `<hash>` pushato su `<branch>`
- 📅 Slot pubblicazione proposto: `<YYYY-MM-DD>`
- 📝 Prossimo passo suggerito: "quando sei pronto a scrivere l'articolo, segui la procedura a step 0→7 del CLAUDE.md (sezione 'Procedura a step con commit intermedi')"

---

## Casi limite

- **Idea da NOTES_IDEAS.md non trovata**: nessun match con confidenza ≥60%. Mostra all'utente le top-3 voci più simili e chiedi se intendeva una di quelle, o se vuole procedere con testo libero usando l'input originale.

- **Sezione non inferibile dall'input**: l'idea non menziona esplicitamente Oracle/Postgres/MySQL/DWH/PM/AI Manager. Chiedi via `AskUserQuestion`.

- **Slot del calendario non leggibile** (`docs/HUGO_PUBLICATIONS_TABLE.md` malformato): segnala e proponi slot generico `<TBD>` nel body. L'utente lo correggerà manualmente.

- **WebSearch fallisce o non disponibile**: la sezione `## Fonti ufficiali da scoutare` conterrà solo placeholder `<TODO: scout fonte ufficiale per "<termine>">`. Segnala chiaramente all'utente che lo scout è da rifare a mano (o in una sessione successiva).

- **`gh` non disponibile o non autenticato**: errore al Passo 0 + suggerisci `gh auth login`. **Non** generare un workaround con `curl` o API proxy.

- **Titolo con caratteri accentati**: rilevali nel Passo 6 e sostituiscili automaticamente (à→a, è→e, é→e, ù→u, ò→o, ì→i). Mostra all'utente la sostituzione fatta.

- **Issue duplicata**: prima di proporre il comando finale (Passo 6), fai un controllo veloce:
  ```bash
  gh issue list --repo ilum75IDB/ivanluminaria.com --label blog-article --state all \
    --search "<keyword distintive del titolo>"
  ```
  Se trovi titoli molto simili (≥70% match), avvisa l'utente: "potenziale duplicato della issue #<nn> '<titolo>' — vuoi procedere comunque?"

- **Branch corrente = `main`**: regola safety globale → push diretto su main vietato. Segnala e suggerisci di creare/spostarsi su un branch operativa (es. `claude/blog-issue-<slug>-<short-id>`). Non procedere col commit del Passo 8 finché siamo su `main`.

- **Working tree sporco con modifiche non correlate**: prima del commit del Passo 8, mostra `git status --porcelain` e chiedi conferma (rischio di includere file non voluti). Default: chiedi conferma con `AskUserQuestion`.

- **Articolo puramente narrativo** (PM, smart working, racconti, opinion): la sezione "Fonti ufficiali da scoutare" può essere vuota o ridotta. Sostituire con: "Articolo narrativo: sezione 'Fonti ufficiali' non obbligatoria (nessun comando/sintassi/parametro citato). Aggiungere in stesura solo se emergono riferimenti a metodologie/spec ufficiali (es. PMBOK, ITIL, ISO)."

- **L'utente vuole una mini-serie cross-DB** (3-4 articoli collegati): la skill gestisce **una issue per volta**. Per la coerenza della serie, il body deve includere la sezione "Mini-serie" che esplicita posizione nella serie + link ai pezzi compagni (anche se non ancora creati). L'utente lancia la skill N volte, una per ogni pezzo.

---

## Note di design

- **Perché project-local e non globale**: la skill referenzia file di tracking specifici (`docs/NOTES_IDEAS.md`, `docs/GITHUB_ISSUES.md`, `docs/HUGO_PUBLICATIONS_TABLE.md`, `docs/HOLIDAYS_CALENDAR.md`, `docs/GLOSSARIO_TERMINI.md`), sezioni del blog hardcoded, settori CV specifici. Una versione "globale" richiederebbe parametrizzazione massiccia che diluirebbe la skill. Se altri progetti Ivan adottano un workflow editoriale simile (es. un secondo sito Hugo), si potrà fare `/skill-copy` adattando i path.

- **Perché level=rich di default**: l'obiettivo dichiarato dall'utente è abilitare un **agent automatico** futuro che generi issue end-to-end. Più info nella issue → meno improvvisazione in stesura → meno errori di tono/struttura. Il livello `minimal` resta come escape valve per casi semplici.

- **Perché auto-detect + flag esplicito coesistono**: l'auto-detect è il flusso "agentico" ideale (l'utente parla naturalmente, la skill capisce); il flag `--from-notes` è il flusso "esplicito" per quando l'auto-detect sbaglia o per workflow automatici che vogliono determinismo (es. cron job che processa idee a batch).

- **Perché WebSearch attivo di default per le fonti**: l'utente ha esplicitamente chiesto "ricordati di inserire nella issue anche di creare la sezione delle fonti autorevoli". La sola istruzione testuale ("scouta le fonti in fase di stesura") rischia di essere disattesa. Pre-scoutando già in fase di issue, la sezione "Fonti ufficiali" dell'articolo parte già con 3-6 link verificati. Se WebSearch non trova fonti, mette `<TODO>` esplicito che obbliga l'autore a chiuderlo prima di pubblicare.

- **Perché approvazione esplicita obbligatoria (mai auto-execute)**: principio globale "agent propone, utente approva, l'agent esegue solo ciò che è approvato". Inoltre `gh issue create` ha effetti visibili (la issue è pubblica sul repo) — è un "azione visibile a terzi" che richiede conferma (regola globale "executing actions with care"). Anche con agent automatico futuro, l'approvazione resta — semmai cambia chi la dà (es. via webhook approval invece che chat).

- **Perché commit + push automatico del tracking**: `GITHUB_ISSUES.md` e `NOTES_IDEAS.md` sono **file di repo**, non file utente esterni. Devono essere committati per non andare persi. La granularità è un commit per issue creata (atomicità leggibile in git log). Push su branch operativa, mai su main (regola safety).

- **Perché la skill anticipa il numero della prossima issue senza usarlo load-bearing**: il numero permette di anticipare riferimenti incrociati (es. "Mini-serie: questo è il #87, gemello di #86 già creata"), ma `gh issue list` non è atomico con `gh issue create` → un altro evento può intercalarsi. Quindi la skill usa il numero solo per text **non-critico** (suggerimenti, link suggeriti). Il numero reale entra nei file di tracking solo dopo che l'utente lo conferma fornendo il link al Passo 8.

- **Perché niente `Co-Authored-By: Claude` nel commit**: regola globale (memoria `~/.claude/memory-global/feedback_no_claude_coauthor.md`). Mai aggiungere quel trailer in nessun commit di nessuna skill.

- **Differenza rispetto alla skill globale `github-crea-issue`**: quella skill è generica (bug, enhancement, articolo, qualsiasi) e si attiva dal racconto naturale di un problema/feature ("ho trovato un bug…", "vorrei aggiungere…"). Questa skill è specializzata su `blog-article` e produce un body **molto più ricco** (settore, hook, fonti scoutate, glossario, cover scene). Sono complementari: se Ivan dice "mi è venuta un'idea per un articolo su X", entrambe potrebbero attivarsi — `blog-idea-to-issue` ha precedenza per `blog-article`.

---

## Esempi di output

### Esempio 1 — Idea da NOTES_IDEAS.md (riferimento esplicito)

**Utente:** `/blog-idea-to-issue --from-notes "Assertions in Oracle 26ai"`

**Skill:**

```
🔍 Trovata 1 idea in docs/NOTES_IDEAS.md (sezione "Da approfondire"):

   ### Articolo Oracle: Assertions in Oracle 26ai
   - Concept: Le Assertions sono vincoli di integrita cross-tabella introdotti in Oracle 26ai...
   - Sezione: Oracle
   - Fonte: https://oracle-base.com/articles/26/assertions-26
   - Data nota: 2026-03-31

✅ Procedo con questa idea.

🔢 Prossimo numero issue: ~#96 (anticipato, non load-bearing)

🌐 Scouting fonti ufficiali (WebSearch)...
   ✅ Oracle Database SQL Language Reference 26ai — CREATE ASSERTION
   ✅ Oracle Base — Assertions in 26ai (Tim Hall)
   ✅ Oracle SQL Domains 23ai (per confronto)
   ⚠️ <TODO: scout fonte ufficiale per "esistenza universal/existential">

📅 Slot proposto: 2026-06-30 (martedì) — next available dopo #88 del 2026-06-23

📝 Body issue generato (formato rich):
   [mostra body completo qui ~80 righe]

🚀 Comando finale pronto per copia-incolla:

   [blocco bash con cat + gh issue create]

❓ Approvi? (Sì / Modifica X / Annulla)
```

**Utente:** "Sì"

**Skill:** *(attende esecuzione e link)*

```
✋ Esegui il comando sopra dal tuo terminale, poi incollami il link
   della issue appena creata.
```

**Utente:** `https://github.com/ilum75IDB/ivanluminaria.com/issues/96`

**Skill:**

```
✅ Issue #96 registrata.

📝 Aggiornamenti file di tracking:
   - docs/GITHUB_ISSUES.md: aggiunta riga nella sezione "Issue Aperte — Sezione Oracle"
   - docs/NOTES_IDEAS.md: nota promossa da "Da approfondire" a "Issue create"

💾 Commit a1b2c3d pushato su claude/plan-may-articles-YrcWA:
   docs(blog): tracciamento issue #96 Articolo Oracle Assertions in 26ai

🎯 Quando vuoi scriverla, segui la procedura step 0→7 del CLAUDE.md.
```

### Esempio 2 — Idea da testo libero

**Utente:** "trasforma questa in issue: ho visto un caso interessante con un cliente del settore farmaceutico dove avevamo PostgreSQL 14 con autovacuum disabilitato per 6 mesi su una tabella da 200M righe. Ho rifatto VACUUM FULL in 4 ore di downtime, recuperando 180GB. Voglio raccontare diagnosi, scelte e perche autovacuum off era un errore."

**Skill:** *(auto-detect: nessun match in NOTES_IDEAS.md ≥60%, procede come testo libero)*

```
ℹ️ Auto-detect: nessun match in docs/NOTES_IDEAS.md.
   Procedo come testo libero.

📋 Inferito dal testo:
   - Sezione: postgresql (riferimento esplicito a "PostgreSQL 14")
   - Settore: farmaceutico → suggerito "Menarini-style" anonimizzato come "un grande gruppo farmaceutico italiano"
   - Tema centrale: autovacuum disabilitato, VACUUM FULL emergency, bloat recovery

🌐 Scouting fonti ufficiali...
   ✅ PostgreSQL 14 — VACUUM
   ✅ PostgreSQL 14 — Routine Vacuuming
   ✅ PostgreSQL 14 — pg_stat_all_tables (n_dead_tup)

📅 Slot proposto: 2026-07-07 (martedì)

📝 Body issue generato (rich):

   ## Concept
   Caso reale di intervento su PostgreSQL 14 in un grande gruppo farmaceutico italiano:
   tabella da 200M righe, autovacuum disabilitato per 6 mesi per "evitare impatto sulle
   performance applicative". Quando il bloat ha rallentato le query critiche, il fix
   è stato un VACUUM FULL da 4 ore in finestra di manutenzione, con recupero di 180GB
   di spazio fisico. L'articolo racconta la diagnosi (n_dead_tup, pg_bloat_check),
   la scelta tra VACUUM FULL / pg_repack / dump+restore, e perché disabilitare
   autovacuum era un errore di valutazione iniziale.

   ## Tono e angolo editoriale
   - Taglio tecnico-pratico, prima persona
   - Caso reale come ancora: il bloat che ha bloccato le query batch notturne
   - Tono no-eroe: il VACUUM FULL non è eroismo, è cleanup di una scelta
     architetturale sbagliata fatta a monte
   - Settore: Farmaceutico (rotation: ultimi 3 articoli sono stati MySQL Postale,
     PostgreSQL Banking, Oracle Telco → questo articolo varia su Farmaceutico)

   [... resto del body ~100 righe]

❓ Approvi? (Sì / Modifica / Annulla)
```

### Esempio 3 — `--dry-run` (senza creare nulla)

**Utente:** `/blog-idea-to-issue --dry-run --from-notes "mailing list newsletter"`

**Skill:**

```
🔍 Match trovato: "Mailing list per notifica nuovi articoli" (sezione: Idee feature sito / marketing).

⚠️ ATTENZIONE: questa nota è in "## Idee feature sito / marketing", non in "## Da approfondire".
   La skill blog-idea-to-issue gestisce solo blog-article. Per feature/marketing del sito
   serve la skill globale `github-crea-issue`.

   Vuoi che convertia comunque il concept in articolo (es. "Come ho scelto di NON fare la
   newsletter al lancio del blog")? Oppure indirizziamo a `github-crea-issue`?
```

### Esempio 4 — Articolo narrativo puro (PM)

**Utente:** "scrivi una issue per un articolo PM sul perché le retrospective che durano più di 60 minuti perdono valore"

**Skill:**

```
📋 Inferito:
   - Sezione: project-management
   - Tipo: articolo narrativo (PM, no comandi/sintassi)
   - Settore: variabile (PM è cross-settore)

🌐 Sezione "Fonti ufficiali" → NON obbligatoria (articolo narrativo).
   Aggiungerò nel body: "Aggiungere solo se emergono riferimenti a metodologie/spec
   ufficiali (es. PMBOK, ITIL, ISO 21500)".

📅 Slot proposto: 2026-07-14 (martedì)

📝 Body issue (rich, sezione fonti compressa):
   [...]
```

---

## Esempi di invocazione

| Comando / frase | Comportamento |
|---|---|
| `/blog-idea-to-issue --from-notes "Assertions Oracle"` | Lookup in NOTES_IDEAS.md, match esplicito |
| `/blog-idea-to-issue ho un caso PostgreSQL pgvector + RAG da raccontare` | Auto-detect → testo libero |
| `/blog-idea-to-issue --level=minimal MySQL EXPLAIN cost-based` | Auto-detect testo libero, body minimal |
| `/blog-idea-to-issue --dry-run --from-notes "newsletter"` | Mostra preview senza generare il comando finale |
| "trasforma in issue l'idea della newsletter mailing list" | Trigger naturale → auto-detect match NOTES_IDEAS.md |
| "scrivimi la issue per un articolo Oracle sull'auto-indexing in 21c" | Trigger naturale → testo libero, sezione=oracle |
| "promuovi a issue 'documentazione progettuale'" | Trigger naturale → lookup NOTES_IDEAS.md |

**NON attivare:**

| Comando / frase | Motivo |
|---|---|
| "fammi vedere le idee" | → Ideas dashboard rule (lettura tabella, non promozione) |
| "creiamo una issue per il bug del footer" | → skill `github-crea-issue` (label `bug`, non `blog-article`) |
| "qual è il prossimo articolo in calendario?" | → Lettura di `HUGO_PUBLICATIONS_TABLE.md`, non promozione idea |
| "scrivimi l'articolo su X" | → Procedura step 0→7 del CLAUDE.md (stesura), non creazione issue |

---

## Riferimenti

- **CLAUDE.md di progetto** (`./CLAUDE.md`):
  - Sezione "Writing articles" (regole 1-11) — fonte autorevole per tono, struttura, vincoli editoriali
  - Sezione "Procedura a step con commit intermedi" — workflow di stesura post-issue
  - Sezione "GitHub Issues > Regole di formattazione" — vincoli su `gh issue create` (titoli ASCII-safe, body-file, no backtick in body inline)
  - Sezione "Publication Schedule" — calendario editoriale, slot, shift festività
  - Tabella settori reali da CV — per rotation settore business

- **File di tracking** (letti/scritti dalla skill):
  - `docs/NOTES_IDEAS.md` (input + sposta nota a "Issue create" al Passo 8)
  - `docs/GITHUB_ISSUES.md` (aggiunge riga nella sezione corretta al Passo 8)
  - `docs/HUGO_PUBLICATIONS_TABLE.md` (legge per slot proposto)
  - `docs/HOLIDAYS_CALENDAR.md` (legge per shift festività)
  - `docs/GLOSSARIO_TERMINI.md` (consulta per "riuso vs nuovo" nel glossario candidato)
  - `content/resumes/` (settori reali da CV — già sintetizzati nella tabella CLAUDE.md)

- **Skill complementari**:
  - `~/.claude/skills/github-crea-issue/` (globale) — per issue di tipo bug/enhancement, non blog-article
  - `~/.claude/skills/handoff/` (globale) — per recap di sessione, non di articoli
  - Procedura "step 0→7 scrittura articolo" nel CLAUDE.md di progetto — workflow naturale **successivo** alla creazione della issue prodotta da questa skill

- **Memorie globali rilevanti**:
  - `~/.claude/memory-global/feedback_no_claude_coauthor.md` — mai `Co-Authored-By: Claude` nei commit
  - Regola safety globale "mai push diretto su main" — il commit del Passo 8 va sul branch operativa

- **Repo GitHub**: <https://github.com/ilum75IDB/ivanluminaria.com>
  - Label disponibili (già create): `oracle`, `postgresql`, `mysql`, `data-warehouse`, `project-management`, `ai-manager`, `blog-article` — vedi tabella nel CLAUDE.md
