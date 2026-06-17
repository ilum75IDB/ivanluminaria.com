# CLAUDE.md — ivanluminaria.com

## Project Overview

Personal and professional website of **Ivan Luminaria** — Oracle DBA, DWH Architect & Project Manager with ~30 years of experience across Oracle, PostgreSQL and MySQL environments. The site is a multilingual Hugo static site deployed to GitHub Pages.

Live URL: `https://ivanluminaria.com/`

## Tech Stack

- **Static Site Generator**: [Hugo](https://gohugo.io/) (extended version, latest)
- **Theme**: [Congo](https://github.com/jpanther/congo) — installed as a Git submodule under `themes/congo/`
- **Deployment**: GitHub Actions → GitHub Pages (workflow at `.github/workflows/hugo.yml`)
- **CSS**: Custom overrides in `assets/css/custom.css` (Inter font, brand colors, fixed navbar, syntax highlighting)
- **Languages**: Hugo multilingual — Italian (default, weight 1), English (weight 2), Spanish (weight 3), Romanian (weight 4)

## Directory Structure

```
.
├── archetypes/          # Hugo archetypes (default.md)
├── assets/
│   ├── css/custom.css   # All custom CSS (brand colors, layout fixes)
│   └── img/             # Avatar image
├── config/
│   └── _default/
│       ├── languages.{it,en,es,ro}.toml   # Per-language config
│       ├── menus.{it,en,es,ro}.toml       # Navigation menus
│       ├── markup.toml                     # Goldmark / syntax highlighting
│       ├── module.toml                     # Hugo module config
│       └── params.toml                     # Theme parameters & author info
├── content/
│   ├── about.{it,en,es,ro}.md             # About page (all languages)
│   ├── posts/
│   │   ├── _index.{it,en,es,ro}.md        # Posts section landing
│   │   └── database-strategy.cover.jpg    # Section cover image
│   └── resumes/
│       ├── index.{it,en,es,ro}.md         # Resumes / CV page
│       └── resumes.cover.jpg              # Section cover image
├── data/
│   └── taxonomy_images.toml               # Taxonomy cover images mapping
├── layouts/
│   ├── baseof.html                        # Base template override
│   ├── simple.html                        # Simple layout (used by About)
│   ├── list.html                          # List layout override
│   ├── _default/
│   │   ├── single.html                    # Single article template
│   │   └── term.html                      # Taxonomy term template
│   ├── _partials/
│   │   ├── article-link.html
│   │   └── article-meta.html
│   ├── partials/
│   │   └── translations.html              # Language switcher dropdown
│   └── shortcodes/
│       └── staticurl.html                 # {{</* staticurl "path" */>}} shortcode
├── static/
│   ├── img/                               # Static images (avatar, flags)
│   └── downloads/                         # PDF resumes
├── themes/congo/                          # Congo theme (Git submodule)
├── hugo.toml                              # Main Hugo config
└── .github/workflows/hugo.yml             # CI/CD: build & deploy
```

## Build & Development

```bash
# Local development server (with drafts) — mostra ciò che sarà live su GitHub Pages
hugo server -D

# Local development server con anche i post programmati (date future) visibili — per revisione pre-pubblicazione
hugo server -D -F --navigateToChanged

# Production build
hugo --minify
```

Hugo **extended** version is required (for SCSS/PostCSS processing in the Congo theme).

**Alias zsh disponibili** (caricati automaticamente quando l'utente attiva l'ambiente con `workwww`):

- `hserve` → `hugo server -D --navigateToChanged` — simula esattamente cosa è online su GitHub Pages (draft visibili, post con data futura nascosti)
- `hservepreview` → `hugo server -D -F --navigateToChanged` — include anche i post `scheduled` (data futura), utile per la revisione pre-pubblicazione

Vedi la sezione **Shell environment (`scripts/shell/`)** sotto per la struttura completa dei file zsh.

## Shell environment (`scripts/shell/`)

L'ambiente shell del progetto segue lo **standard RCCS2025** (env separato + help/navigation parametrici). I file sono in `scripts/shell/` e vengono caricati dal `~/.zshrc` dell'utente quando si attiva l'ambiente con `workwww`.

```
scripts/shell/
├── www_env.zsh            # Variabili, alias Hugo/Git/Deploy, funzioni www_new_page/post, wrapper wwwgo/wwwhelp
├── www_help.zsh           # Sistema help parametrico (wwwhelp -U/-N/-C/-G/-L/-V/-H)
├── www_go_manager.zsh     # Go manager parametrico (wwwgo project|content|posts|... + help/list)
└── config/
    └── zshrc.txt          # Copia di riferimento del ~/.zshrc dell'utente (master globale gestione progetti)
```

**Comandi parametrici principali**:

- `wwwhelp` → menu sezioni (7 sezioni); `wwwhelp -U` Hugo, `-N` Navigazione, `-C` Contenuti, `-G` Git, `-L` Links, `-V` Variabili, `-H` Help & Setup
- `wwwgo` → lista 10 directory target; `wwwgo project|content|posts|resumes|config|docs|css|layouts|shell|scripts`; alias `root` (= `project`), `blog` (= `posts`)

**`scripts/shell/config/zshrc.txt`** è una **copia di riferimento** del `~/.zshrc` master di Ivan (vive in `~/`, fuori dal repo, gestisce il menu progetti: RCC/GDM/WWW/GMA/WEBO). Serve a:

1. **Documentare** la struttura del menu globale e come WWW si integra (case `3|www` carica `scripts/shell/www_env.zsh`)
2. **Recuperare** il file in caso di perdita dell'home dell'utente (es. cambio Mac, formattazione)
3. **Confrontare** modifiche al `~/.zshrc` master quando si lavora cross-progetto

⚠️ **Non è il file attivo**: modificarlo non ha effetti sulla shell. Per modifiche reali al menu progetti l'utente edita direttamente `~/.zshrc`, poi (se vuole tracciare il cambio) ricopia il file qui con: `cp ~/.zshrc scripts/shell/config/zshrc.txt`.

Per modifiche all'ambiente WWW invece (alias, funzioni, variabili, sezioni help, target navigazione) si editano i file `www_*.zsh` in `scripts/shell/`, che vengono ricaricati con `workwww` o `prjmenu`.

## Accesso LAN via Bonjour

Oltre al server puramente locale (`hserve` / `wwwserver dev`), il progetto
espone il sito anche sulla LAN domestica via mDNS, per anteprima da telefono /
iPad / altro computer:

```
http://ivanluminaria.local:1313/      # nome primario
http://ilum.local:1313/               # alias breve (3 char, come il prefisso shell `www`)
```

**Comandi rapidi** (env caricato con `workwww`):

| Comando | Effetto |
|---|---|
| `wwwserver start` | Hugo server LAN in background (`bind 0.0.0.0`, drafts + scheduled visibili) |
| `wwwserver status` / `stop` / `restart` | Stato / stop / restart del server background |
| `wwwserver dev` / `preview` | Foreground locale 127.0.0.1 (= `hserve` / `hservepreview`) |
| `wwwserver enable` / `disable` | LaunchAgent persistente (parte al login) |
| `wwwbonjour on` / `off` / `status` / `test` | Gestione annuncio mDNS dei due nomi |
| `wwwopenlan` / `wwwopenshort` | Browser su nome lungo / alias breve |
| `wwwhelp -S` / `wwwhelp -B` | Schede help dedicate |

**Caveat — leggere prima di esporre**:

- **Hugo NON ha auth**. `wwwserver start` (e `enable`) espone **tutto** il sito
  con `--buildDrafts --buildFuture`: chiunque sulla WiFi può vedere bozze e
  articoli scheduled. Accettabile per la WiFi domestica privata di Ivan; per
  scenari "ospiti in casa" usare `wwwserver dev` puro locale.
- I link interni sono riscritti automaticamente con `--baseURL
  http://ivanluminaria.local:1313/ --appendPort=false` per evitare il rimbalzo
  a `localhost` quando navighi dal cellulare. Cambiare bind manualmente senza
  passare dal manager rompe i link interni.
- L'IP del Mac viene ricavato a runtime da `ipconfig getifaddr`; se cambia
  (nuovo lease DHCP), `announce.sh` ri-annuncia entro 30s.

**File coinvolti** (copie di riferimento nel repo; le copie attive vivono fuori
in `~/Library/Application Support/bonjour-lan/` e `~/Library/LaunchAgents/`):

- `scripts/shell/www_server_manager.zsh` — sub-comandi `wwwserver`
- `scripts/shell/www_bonjour_manager.zsh` — sub-comandi `wwwbonjour`
- `deploy/launchd/announce.sh` — annuncio mDNS condiviso multi-progetto
- `deploy/launchd/com.ivanluminaria.bonjour.www.plist` — LaunchAgent Bonjour
- `deploy/launchd/com.ivanluminaria.www.plist` — LaunchAgent server Hugo

Doc completa: [`docs/BONJOUR_LAN_ACCESS.md`](docs/BONJOUR_LAN_ACCESS.md).

## Deployment

Pushing to the `main` branch triggers the GitHub Actions workflow (`.github/workflows/hugo.yml`) which:

1. Checks out the repo with submodules
2. Sets up Hugo (latest extended)
3. Runs `hugo --minify`
4. Uploads `public/` as a Pages artifact
5. Deploys to GitHub Pages

## Multilingual Architecture

- **Default language**: Italian (`it`), with `defaultContentLanguageInSubdir = true` (content lives under `/it/`)
- Content files use the suffix convention: `about.it.md`, `about.en.md`, etc.
- Section indexes use: `_index.it.md`, `_index.en.md`, etc.
- Bundle pages use: `index.it.md`, `index.en.md`, etc.
- Each language has its own menu config in `config/_default/menus.{lang}.toml`
- Language switcher is a custom partial at `layouts/partials/translations.html` using flag images from `static/img/flags/`

### Adding a New Language

1. Create `config/_default/languages.{code}.toml` with appropriate weight
2. Create `config/_default/menus.{code}.toml` with translated menu items
3. Add translated content files with the `.{code}.md` suffix
4. Add the flag image to `static/img/flags/{code}.png`

## Brand & Design System

Defined in `assets/css/custom.css`:

| Token               | Value       | Usage                            |
|----------------------|-------------|----------------------------------|
| `--ivan-blue`        | `#336791`   | Postgres blue — brand name, strong text, breadcrumbs |
| `--ivan-red`         | `#F80000`   | Oracle red — links, nav menu, blockquote borders     |
| `--ivan-red-dark`    | `#b30000`   | Hover states for links                               |
| `--ivan-gray-title`  | `#4a4a4a`   | Headings (h1–h4)                                     |
| `--ivan-gray-obj`    | `#6b7280`   | SQL identifiers in code blocks                       |
| `--ivan-sql-green`   | `#2e8b57`   | SQL keywords in code blocks                          |

Font: **Inter** (loaded from Google Fonts), base size 20px.

## Content Guidelines

- The site has a distinctive authorial voice — thoughtful, direct, professional but personal
- Content is written in Markdown with Hugo shortcodes
- Use `{{</* staticurl "path" */>}}` shortcode when referencing static assets (needed for correct GitHub Pages subpath resolution)
- Goldmark is configured with `unsafe = true` to allow raw HTML in Markdown
- Cover images for sections are placed alongside content files (e.g., `database-strategy.cover.jpg`)

### Writing articles

When writing a new blog article, **always** follow these steps:

1. **Read the content guidelines first** — before drafting any text, read the files in `docs/`, in particular:
   - `docs/AI_CONTENT_GUIDELINES.md` (English version)
   - `docs/AI_CONTENT_GUIDELINES_IT.md` (Italian version)
   - `docs/prompt-master.md` (master prompt with tone & style rules)
   - `docs/DESCRIZIONE_PROGETTO_DATABASE_STRATEGY_BLOG.md` and `docs/database_strategy_blog_project_description_FULL.md` (project context)
   - `docs/STILE_LINGUISTICO.md` (vocabolario di termini da evitare e relative sostituzioni — consultare in scrittura e in revisione)
2. **Write like a human** — the text **must not** sound AI-generated. Avoid generic filler, motivational closings, bullet-point-heavy structures, and overly polished phrasing. Use Ivan's voice: direct, experienced, occasionally ironic, grounded in real-world project stories. Vary sentence length, use colloquial turns where appropriate, and let opinions show.
3. **No AI tells** — never use patterns like "In conclusion…", "It's worth noting that…", "Let's dive in…", "In today's fast-paced world…", or similar clichés typical of LLM output.
4. **Riferimenti temporali vicini** — evitare riferimenti troppo indietro nel tempo (es. "due anni fa", "tre mesi fa") a meno che non sia richiesto esplicitamente dal contesto dell'articolo. Preferire sempre espressioni vicine: "l'altro giorno", "qualche giorno fa", "ieri", "la settimana scorsa", "la scorsa settimana". Se il racconto richiede un arco temporale più lungo (mese precedente, un paio di mesi fa), giustificarlo nel testo con frasi tipo: "È un po' che volevo scrivere su questo argomento e non ho trovato il tempo… finalmente eccomi" o simili.
5. **No generalizzazioni da clickbait** — evitare frasi come "quello che nessuno ti dice", "che nessuno sa", "che non tutti sanno", "il segreto che…". Queste generalizzazioni svalorizzano il lavoro e suonano come marketing. Il valore dell'articolo deve emergere dal contenuto, non da promesse sensazionalistiche nel titolo o nel testo.

   **Evitare anche le auto-affermazioni di onestà** — formule come "raccontati onestamente", "senza giri di parole", "senza pietà", "diciamoci la verità", "ad essere sinceri" implicano che altrove non si sia onesti, e suonano come un tic da blogger. Se il racconto è onesto, lo si vede dai dettagli concreti; non serve dichiararlo. Preferire titoli di sezione descrittivi come "I limiti, racconti dall'esperienza", "Il caso concreto", "Cosa è andato storto".
6. **Niente tono "eroe salvatore dell'universo"** — evitare di costruire ogni racconto come la storia in cui Ivan, da solo, salva il progetto/cliente/azienda da un disastro epocale. Smussare il protagonismo: riconoscere il contributo del team, del DBA del cliente, di un collega che ha avuto l'intuizione, del vendor, di una vecchia nota di Tom Kyte o di un blog post letto al momento giusto. Preferire forme collettive ("abbiamo capito che…", "il team ha proposto…", "ci siamo accorti che…") alle forme egocentriche ("ho risolto da solo…", "nessuno aveva visto che…", "sono stato l'unico a capire…"). Anche i risultati vanno raccontati con misura: invece di "ho salvato un sistema critico", "il caricamento è passato da 4 ore a 25 minuti — non magia, una settimana di profiling e una conversazione fortunata col DBA del cliente". Il valore tecnico dell'articolo deve emergere dall'analisi e dal dettaglio, non dall'enfasi sul protagonismo. Vale anche per i titoli: niente "come ho salvato…", "il segreto che ho scoperto…", "quello che nessuno ha capito tranne me…".
7. **Variare i settori di business dei clienti — usando solo settori reali** — nei racconti e negli aneddoti, alternare i mercati e i settori dei clienti per cui Ivan ha lavorato davvero (vedi i CV in `content/resumes/`). **Non inventare settori in cui non ha mai lavorato** (es. retail di articoli sportivi, e-commerce moda, gaming, food delivery, ecc.). Questo rende i racconti credibili e non smentibili. Lista di consultazione rapida dei settori reali:

   | Settore                                | Clienti reali (esempi)                                                  |
   |----------------------------------------|-------------------------------------------------------------------------|
   | Assicurazioni & crediti commerciali    | ATRADIUS (Surety, multi-paese EU), Generali Assicurazioni, RAS         |
   | Telecomunicazioni (Telco)              | TIM (anche via HUAWEI), Vodafone Italia/Spagna (Madrid), TRE, Telecom  |
   | Banking & Finance                      | Banca d'Italia, FINWAVE S.p.A. (applicazioni finanziarie)              |
   | Pubblica Amministrazione               | Vari enti PA (via AUSELDA AED GROUP)                                    |
   | Postale & logistica                    | Poste Italiane (~1500 istanze MySQL/PostgreSQL)                         |
   | Trasporti & mobilità                   | FAI Service (cooperativa autotrasporti), Telepass                       |
   | Farmaceutico                           | Menarini (via Oracle Italia)                                            |
   | Automotive (storico, anni '90)         | Rover Italia (via S.EL.DAT.)                                            |

   Quando il racconto richiede un settore generico, scegliere uno tra quelli sopra senza nominare il cliente specifico (es. "un grande gruppo assicurativo italiano", "un operatore telco mobile", "una banca commerciale", "un'azienda della Pubblica Amministrazione"). Alternare i settori tra articoli successivi per non concentrarsi su uno solo.
8. **SEO frontmatter: `seoTitle` + `description` ottimizzate fin dalla prima stesura** — ogni articolo, in **tutte e 4 le lingue**, deve avere nel frontmatter:

   - **`title`**: titolo narrativo/empatico per l'H1 e l'apertura dell'articolo (es. "Cuando un LIKE '%valor%' ralentiza todo: un caso real de optimización PostgreSQL"). Può essere lungo e d'impatto, **non deve essere keyword-driven**.
   - **`seoTitle`**: titolo keyword-driven per il `<title>` HTML e SERP Google. **Lunghezza target: 50–60 caratteri** (massimo 65). Deve contenere le keyword principali per cui vogliamo posizionarci (es. "PostgreSQL LIKE con %valor%: índice GIN y pg_trgm"). Si applica via override in `layouts/_partials/head.html`.
   - **`description`**: meta description per SERP e social preview. **Lunghezza target: 140–160 caratteri** (massimo 160). Deve riassumere il contenuto in modo informativo, contenendo 2–3 keyword secondarie. Niente clickbait, niente promesse vuote.

   **Regole di compilazione**:
   - Scrivere `seoTitle` e `description` **contestualmente** alla stesura dell'articolo (non come correzione retroattiva)
   - Tradurre/adattare entrambi i campi per ciascuna lingua (non lasciare seoTitle in italiano nelle versioni EN/ES/RO)
   - **Verifica della lunghezza prima di committare**: contare i caratteri di `seoTitle` (≤65) e `description` (≤160) per ogni lingua
   - Le keyword da inserire vanno scelte pensando a "cosa cercherebbe su Google chi ha questo problema" (es. nome tecnologia + funzione + sintomo: "PostgreSQL LIKE wildcard slow"), non a "come voglio che l'articolo si chiami"
   - Per gli **articoli già esistenti senza `seoTitle`**, Hugo fa fallback automatico su `.Title` (vedi `layouts/_partials/head.html`) — quindi non sono "rotti", ma vanno aggiornati progressivamente in audit SEO retroattivi

9. **Generare la descrizione della scena per l'immagine di copertina** — dopo aver completato la scrittura dell'articolo in tutte le lingue, fornire **solo la descrizione della scena** da rappresentare (non ripetere il prompt master — il prompt base è già in mano a chi genera le immagini). La scena va scritta in modo specifico e coerente con il tema dell'articolo, tramite una metafora visiva che rispecchi il tono dell'articolo (es. se l'articolo ha tono no-eroe, la scena non deve mettere il personaggio principale al centro). Fornire anche il **nome del file** che l'utente dovrà usare per salvare l'immagine, seguendo la convenzione `<slug>.cover.jpg` da posizionare nella cartella dell'articolo (`content/posts/<sezione>/<slug>/`). **Non creare file placeholder** per la cover image — sarà l'utente a generare l'immagine e inserirla.

   **Archiviare il prompt come file Markdown** in `docs/cover-image-prompts/<slug>.cover.md` (stesso nome dell'immagine ma estensione `.md`), con questa struttura: `# Cover image prompt — <filename>` / `## Articolo di riferimento` (slug, sezione, titolo IT) / `## Descrizione della scena` (5-10 righe, specifica e visiva) / `## Metafora visiva` (2-3 frasi che legano scena e tema) / `## File output` (nome file, path destinazione, formato). Questo permette in futuro di rigenerare un'immagine coerente o variarne lo stile mantenendo il concetto.
10. **Sezione Glossario a fine articolo** — ogni articolo deve terminare con una sezione `## Glossario` che elenca **5 termini tecnici o acronimi** tra i più importanti contenuti nell'articolo. Ogni voce del glossario deve avere il formato: **Termine** — descrizione breve e chiara (1-2 frasi). I termini vanno scelti privilegiando: acronimi (es. AWR, SCD, ETL), concetti tecnici specifici (es. buffer pool, execution plan), e tecnologie/strumenti menzionati nell'articolo. Evitare termini troppo generici (es. "database", "SQL") a meno che non siano centrali per l'articolo. **Riuso di termini esistenti**: è ammesso riprendere termini già presenti nel glossario, ma **al massimo 2 per articolo**. Gli altri 3 (almeno) devono essere nuovi, in modo che ogni articolo porti valore aggiunto al glossario complessivo del blog. Il glossario deve essere presente in **tutte e 4 le versioni linguistiche** dell'articolo, con le descrizioni tradotte. Dopo aver scritto il glossario, **aggiornare sempre** il file `docs/GLOSSARIO_TERMINI.md` aggiungendo i nuovi termini o aggiornando la colonna "Contenuto in" per i termini già presenti.

11. **Sezione `## Fonti ufficiali` prima del Glossario** — per ogni articolo che riporta **comandi, sintassi, parametri o flag** che il lettore potrebbe copiare in produzione, aggiungere una sezione `## Fonti ufficiali` (prima del Glossario, dopo l'ultima sezione di contenuto) con i link alla **documentazione ufficiale** del vendor/progetto.

   **Convenzione di notazione**:
   - Nel corpo dell'articolo, mettere una nota numerica `[1]`, `[2]`... dopo l'affermazione tecnica o il comando citato. Esempio: *"La sintassi corretta per abilitare una policy Unified Audit è `AUDIT POLICY nome_policy` [1]."*
   - In fondo all'articolo, sezione `## Fonti ufficiali` con elenco numerato:
     ```markdown
     ## Fonti ufficiali

     1. Oracle Database SQL Language Reference 19c — [AUDIT (Unified Auditing)](https://docs.oracle.com/...)
     2. PostgreSQL Documentation — [pg_stat_statements](https://www.postgresql.org/...)
     ```

   **Quando aggiungere una nota**:
   - ✅ **Comandi/sintassi/parametri/flag** che il lettore potrebbe copiare in produzione (es. `AUDIT POLICY`, `CREATE INDEX CONCURRENTLY`, `binlog_expire_logs_seconds`). **Anche se il termine è già linkato al glossario interno**: glossario e fonte ufficiale sono complementari, non alternativi (il glossario chiarisce *cosa significa*, la fonte conferma *come si scrive*)
   - ✅ Affermazioni tecniche controverse (licensing, comportamenti version-specific)
   - ✅ Parametri/comportamenti che cambiano tra versioni del prodotto
   - ❌ Costatazioni narrative o opinioni personali
   - ❌ Casi reali di consulenza Ivan
   - ❌ Termini concettuali del glossario senza comando associato (es. "buffer pool", "MVCC")

   **Target**: 3-6 note per articolo tecnico, non 50. Devono pesare. La sezione `## Fonti ufficiali` va presente in **tutte e 4 le versioni linguistiche** con gli stessi link (la documentazione ufficiale è in inglese in tutti i casi).

### Procedura a step con commit intermedi (anti-timeout)

La scrittura di un articolo in 4 lingue + glossario + aggiornamento docs è troppo pesante per una singola sessione. Per evitare timeout e perdita di lavoro, **ogni step deve concludersi con commit + push**. Se la sessione scade, la successiva riprende dallo step non completato.

| Step | Cosa fare | Commit message |
|------|-----------|----------------|
| **0** | Leggere issue, `docs/AI_CONTENT_GUIDELINES.md`, `docs/database_strategy_blog_project_description_FULL.md` | *(nessun commit, solo lettura)* |
| **0b** | Proporre **3 titoli** all'utente tra cui scegliere (l'utente può anche suggerirne uno proprio) | *(nessun commit, solo output testuale)* |
| **1** | Creare la directory dell'articolo e scrivere la versione **IT** (con `seoTitle` ≤65ch e `description` ≤160ch nel frontmatter, e se l'articolo riporta comandi/sintassi/parametri, includere note `[n]` nel testo e la sezione `## Fonti ufficiali` prima del Glossario — vedi punto 11) | `Articolo #XX: <slug> - versione italiana (IT)` |
| **2** | Scrivere la versione **EN** (con `seoTitle` e `description` tradotti/adattati) | `Articolo #XX: <slug> - traduzione inglese (EN)` |
| **3** | Scrivere la versione **ES** (con `seoTitle` e `description` tradotti/adattati) | `Articolo #XX: <slug> - traduzione spagnola (ES)` |
| **4** | Scrivere la versione **RO** (con `seoTitle` e `description` tradotti/adattati) | `Articolo #XX: <slug> - traduzione rumena (RO)` |
| **5** | Glossario: creare mini-pagine nuove (4 lingue ciascuna) + aggiungere sezione glossario alle 4 versioni dell'articolo | `Glossario: mini-pagine e sezione glossario per <slug>` |
| **6** | Aggiornare `docs/HUGO_PUBLICATIONS_TABLE.md`, `docs/GITHUB_ISSUES.md`, `docs/GLOSSARIO_TERMINI.md` | `Aggiornamento docs: pubblicazione e issue per <slug>` |
| **7** | Generare prompt cover image, **salvarlo come file Markdown in `docs/cover-image-prompts/<slug>.cover.md`** (convenzione: stesso nome dell'immagine ma estensione `.md`), e fornire comando `gh issue close` | `Cover prompt: <slug>` |

**Regole:**
- **Commit + push dopo ogni step** — non accumulare mai più di uno step senza committare
- **Se la sessione riparte**, leggere lo stato del repo (ultimo commit, file esistenti) per capire da quale step riprendere
- **Lo step 0 (lettura)** legge solo `docs/AI_CONTENT_GUIDELINES.md`, `docs/database_strategy_blog_project_description_FULL.md` e `docs/STILE_LINGUISTICO.md` (non leggere i duplicati in italiano né articoli esistenti)
- **Lo step 0b (proposta titoli)** è obbligatorio: proporre 3 titoli all'utente e permettergli di sceglierne uno o suggerirne un altro
- **Gli step 1-4 (scrittura lingue)** sono sequenziali: IT è il master, le altre sono traduzioni adattate (non letterali)
- **Lo step 5 (glossario)** può essere fatto tutto insieme perché le mini-pagine sono brevi

### Workflow: aggiunta glossario a un articolo esistente

Quando l'utente chiede di aggiungere la sezione Glossario a un articolo che ne è privo, seguire **sempre** questi passi nell'ordine indicato:

1. **Leggere l'articolo** in tutte e 4 le lingue per identificare i termini tecnici principali
2. **Leggere `docs/GLOSSARIO_TERMINI.md`** per sapere quali termini esistono già (con relative mini-pagine)
3. **Scegliere 5 termini** (o il numero richiesto dall'utente) privilegiando: acronimi, concetti tecnici specifici dell'articolo, tecnologie menzionate. Includere anche termini già esistenti nel glossario se sono rilevanti per l'articolo
4. **Creare le mini-pagine** per i termini nuovi:
   - Directory: `content/glossary/<slug>/`
   - File: `index.{it,en,es,ro}.md` (4 lingue)
   - Formato frontmatter: `title`, `description`, `translationKey: "glossary_<slug>"`, `aka` (se applicabile), `articles` (lista dei path degli articoli)
   - Contenuto: definizione, come funziona, a cosa serve, quando si usa
   - Copiare il formato esatto dalle mini-pagine esistenti (es. `content/glossary/awr/`)
5. **Aggiungere la sezione Glossario** all'articolo in tutte e 4 le lingue:
   - Posizione: alla fine dell'articolo, dopo l'ultima sezione, preceduta da un separatore `------------------------------------------------------------------------`
   - Titolo: `## Glossario` (IT), `## Glossary` (EN), `## Glosario` (ES), `## Glosar` (RO)
   - Formato voci con link alla mini-pagina: `**[Termine](/{lang}/glossary/{slug}/)** — descrizione breve (1-2 frasi)`
   - **IMPORTANTE**: ogni termine DEVE avere il link alla mini-pagina del glossario, usando il prefisso lingua corretto (`/it/`, `/en/`, `/es/`, `/ro/`). Esempio: `**[AWR](/it/glossary/awr/)** — Automatic Workload Repository...`
6. **Aggiornare `docs/GLOSSARIO_TERMINI.md`**:
   - Aggiungere i nuovi termini in ordine alfabetico
   - Per i termini già presenti, aggiungere il nuovo articolo nella colonna "Contenuto in"
   - Aggiornare il contatore "Totale termini" e "Totale articoli con glossario"
7. **Commit e push** con messaggio nel formato: `Glossario: aggiunta sezione glossario a <slug> (IT/EN/ES/RO)`
8. **Fornire il comando `gh issue comment`** per aggiornare la issue di tracciamento (es. #60) con il riepilogo del lavoro svolto: termini aggiunti, file creati/modificati, progresso complessivo. **Non dimenticare mai questo passo.**

## Homepage Layout

The homepage (`layouts/_partials/home/custom.html`) uses an editorial magazine-style layout. Sections are displayed in a **fixed order** defined by the `$sections` slice in the template.

### Section display rules

- **Latest** section: 1 hero (full-width image above title) + 5 grid articles (total 6, controlled by `homepage.recentLimit` param)
- **Each category section**: 1 hero (2-column: image left, text right) + up to 4 grid articles (total max 5)
- **All images** must use **3:2 aspect ratio** — never change this

### Image sizes (3:2 ratio)

| Element             | srcset                          | CSS class                        |
|---------------------|---------------------------------|----------------------------------|
| Latest hero         | `800x533` / `1200x800`         | `.editorial-hero-img`            |
| Latest grid         | `300x200` / `600x400`          | `.editorial-grid-img`            |
| Category hero       | `450x` / `900x`                | `.editorial-category-hero-img`   |
| Category grid       | `300x200` / `600x400`          | `.editorial-grid-img`            |

### Category hero layout

Each category section hero uses a **2-column layout** (CSS class `.editorial-category-hero`):
- **Left column**: cover image (3:2, linked to article)
- **Right column** (`.editorial-category-hero-text`): 3 rows — title, date + reading time, description
- Below 480px: collapses to single column (image on top)

### Section order

| #  | Section                  | Slug                 | Articles displayed       |
|----|--------------------------|----------------------|--------------------------|
| 1  | Ultimi articoli (Latest) | *(all sections)*     | 1 hero + 5 grid = 6     |
| 2  | Data Warehouse Architect | `data-warehouse`     | 1 hero + up to 4 grid   |
| 3  | Project Management       | `project-management` | 1 hero + up to 4 grid   |
| 4  | Oracle                   | `oracle`             | 1 hero + up to 4 grid   |
| 5  | PostgreSQL               | `postgresql`         | 1 hero + up to 4 grid   |
| 6  | MySQL                    | `mysql`              | 1 hero + up to 4 grid   |

**Important**: When adding new sections, update both this table and the `$sections` slice in `layouts/_partials/home/custom.html`. Never modify the image aspect ratios or the category hero 2-column structure.

## Custom Layouts & Overrides

- **`layouts/partials/translations.html`**: Custom language switcher with flag dropdown (replaces Congo default)
- **`layouts/shortcodes/staticurl.html`**: Resolves static asset URLs with correct base path
- **`layouts/_default/single.html`**: Article template with cover image support
- **`layouts/simple.html`**: Used by the About page for a clean profile layout
- **Navbar**: CSS-forced to `position: fixed` with `z-index: 9999` (see custom.css)

## Publication Schedule

Articles are published **one per week, every Tuesday at 08:03 CET**, starting from 16 December 2025. Three GitHub Actions cron run on Tuesday at 05:47 UTC, 06:47 UTC and 09:05 UTC (≈ 07:47 / 08:47 / 11:05 CEST in summer): the first publishes the article, the second is backup in case the first is delayed by GitHub Actions queue (common during peak hours like `:00`/`:05`), the third is a last-resort safety net (deploy after the LinkedIn post but ensures publication eventually). The article is online well before the LinkedIn post goes out (scheduled on Buffer at ~10:05–10:15 CET).

### Rules

1. **Cadence**: one article per Tuesday, no gaps
2. **Time**: always `T08:03:00+01:00`
3. **First article**: 2025-11-18 (Tuesday)
4. **New articles**: take the next available Tuesday slot after the last published article
5. **Backdated articles**: if the user asks to publish an article in the past, assign it to the **Previous available slot** date. Then update the Previous available slot to the Tuesday before the new oldest article
6. **All 4 language versions** of each article share the same date
7. **Schedule table format**: always show the columns below. When reorganising dates, fill the "New Date" column; use `—` if no change is needed
8. **Colonna "Scritto il"**: ogni articolo ha una colonna `Scritto il` che indica la **data effettiva in cui l'articolo è stato scritto e committato** (corrisponde alla data di chiusura della issue). Questa data è indipendente dalla data di pubblicazione — un articolo può essere scritto oggi ma avere una data di pubblicazione passata (backdating) o futura (scheduling). Quando si scrive un nuovo articolo, compilare sempre questa colonna con la data del giorno corrente. Quando l'utente chiede "l'ultimo articolo scritto", ordinare per `Scritto il` (non per `Date`).
9. **Article status values**:
   - **published**: article is live on the site (publication date is in the past)
   - **scheduled**: article is written in all 4 languages, committed to the repo, and has a future publication date. The corresponding GitHub issue should be closed
   - **planned**: only the GitHub issue exists (article not yet written). The corresponding issue is still open
10. **Slot markers** (at the bottom of `docs/HUGO_PUBLICATIONS_TABLE.md`):
   - **Previous available slot**: the first Tuesday before the oldest article's date. Used when inserting backdated articles
   - **Next available slot**: the first Tuesday after the most recent article's date. Used for new articles
   - Both must be updated after every schedule change
11. **Martedì festivo (festività italiane)**: se uno slot martedì coincide con una **festività italiana** (vedi `docs/HOLIDAYS_CALENDAR.md`), spostare la pubblicazione al **mercoledì successivo** alle 08:03 CET. Il post LinkedIn principale segue lo slot (anche al mercoledì). Per le festività degli altri paesi (UK/ES/RO) **non si fa alcuno shift** — l'articolo è online in tutte le lingue ma non c'è una "pubblicazione" locale. Casi noti 2026: martedì 06/01 (Epifania) → mercoledì 07/01; martedì 02/06 (Festa della Repubblica) → mercoledì 03/06; martedì 08/12 (Immacolata) → mercoledì 09/12.
12. **Calendario festività**: consultare `docs/HOLIDAYS_CALENDAR.md` per le festività ufficiali IT/UK/ES/RO. **Il 15 dicembre di ogni anno** preparare il calendario dell'anno successivo aggiungendo una nuova sezione al file.

### Current Schedule

The full publication table is maintained in **`docs/HUGO_PUBLICATIONS_TABLE.md`**. Always read and update that file when working with the schedule.

When adding a new article, update the table in `docs/HUGO_PUBLICATIONS_TABLE.md`, assign the next available Tuesday slot, and update both slot markers accordingly.

### Publication dashboard rule

When the user asks for the "tabella delle pubblicazioni" (publication table), **always show 3 tables**:

1. **Tabella pubblicazioni** — the Current Schedule table above (all published, scheduled and planned articles with dates), **inclusa la colonna "Scritto il"** che mostra quando l'articolo è stato effettivamente scritto. La tabella deve essere ordinata per data di pubblicazione (`Date`), ma la colonna `Scritto il` permette di identificare rapidamente l'ordine cronologico di scrittura
2. **Tabella issue aperte** — all open issues grouped by section (from `docs/GITHUB_ISSUES.md`)
3. **Riepilogo per sezione** — a summary table with columns: Sezione, Pubblicati, Programmati (scheduled), Pianificati (issue aperte), Totale

When the user asks for "l'ultimo articolo scritto" or similar, **always refer to the `Scritto il` column** (most recent date), not the publication date.

### Ideas dashboard rule

When the user asks for "tabella delle idee", "fammi vedere le idee", or "fammi vedere gli appunti per gli articoli da scrivere", **always read `docs/NOTES_IDEAS.md`** and show a table with columns: Sezione, Titolo/Concept, Collegamento, Data nota.

## Important Notes

- The Congo theme is a **Git submodule** — always clone/checkout with `--recurse-submodules` or run `git submodule update --init`
- The `baseURL` in `hugo.toml` is set for the custom domain (`https://ivanluminaria.com/`)
- PDF resumes are stored in `static/downloads/` and linked from the resumes content pages
- The `.gitignore` excludes `public/`, `resources/_gen/`, and `.hugo_build.lock`

## GitHub Issues

In questo ambiente **`gh` CLI è disponibile e autenticato** (verifica con `gh auth status`). Claude e le skill di progetto (es. `.claude/skills/blog-idea-to-issue/`) possono usarlo per **leggere** le issue del repository (es. `gh issue list --repo ilum75IDB/ivanluminaria.com --label blog-article --state all`, `gh issue view <n> --json number,title,body,labels`).

Per la **creazione, chiusura e modifica** delle issue (`gh issue create`, `gh issue close`, `gh issue edit`), invece, il principio resta: **Claude prepara il comando completo pronto per copia-incolla** e l'utente lo esegue dal proprio terminale. Questo per safety — la scrittura su issue è un'azione pubblicamente visibile sul repo, e segue la regola globale "agent propone, utente approva, l'agent esegue solo ciò che è approvato". Mai eseguire operazioni di scrittura `gh` autonomamente.

### Consultare le issue aperte

Due strade complementari:

1. **`gh issue list` / `gh issue view`** (preferito per query specifiche, filtri, lettura body completo): es. `gh issue list --repo ilum75IDB/ivanluminaria.com --label blog-article --state open --json number,title,body`.
2. **`docs/GITHUB_ISSUES.md`** (indice riepilogativo curato a mano): tracking file con i link delle issue raggruppate per sezione. Utile per overview rapide e per la "Dashboard delle pubblicazioni" (vedi sezione apposita). Resta autoritativo per la vista aggregata anche con `gh` disponibile.

Regole di mantenimento di `docs/GITHUB_ISSUES.md`:

1. Quando si crea una nuova issue, **aggiungere la riga** nella sezione corrispondente (es. "Issue Aperte — Sezione Oracle"). La skill `blog-idea-to-issue` lo fa automaticamente al Passo 8.
2. Quando una issue viene chiusa, **spostarla** dalla sezione aperte alla sezione "Issue Chiuse" con la data di chiusura.
3. Quando l'utente crea una issue manualmente dal proprio terminale, **chiedergli sempre il link** per poterlo inserire in `GITHUB_ISSUES.md`. Non procedere senza aver aggiornato il file.

### Chiusura issue di articoli pubblicati

Quando si chiude una issue relativa a un articolo pubblicato, il commento di chiusura deve contenere:

1. **Data di pubblicazione** — la data prevista dal calendario editoriale (es. 2025-11-11)
2. **URL dell'articolo** — link alla versione italiana sul sito live (es. `https://ivanluminaria.com/it/posts/data-warehouse/scd-tipo-2/`)
3. **Conferma tutte le lingue** — specificare che l'articolo è stato pubblicato in tutte e 4 le lingue (IT, EN, ES, RO)
4. **Breve riassunto** — 2-3 frasi che descrivono il contenuto dell'articolo

Formato del comando:

```
gh issue close <numero> --repo ilum75IDB/ivanluminaria.com --comment "Articolo pubblicato il <data>.

URL: https://ivanluminaria.com/it/posts/<sezione>/<slug>/

Pubblicato in tutte le lingue: IT, EN, ES, RO.

<breve riassunto del contenuto>"
```

Dopo la chiusura, **aggiornare `docs/GITHUB_ISSUES.md`**: spostare la issue dalla sezione aperte alla sezione chiuse con la data di chiusura.

### Regole di formattazione per i comandi gh issue create

**CRITICO — il comando deve funzionare con copia-incolla diretto nel terminale macOS (zsh):**

1. **NON usare backtick `` ` `` o triple backtick `` ``` `` nel body** — la shell li interpreta come command substitution e il comando fallisce. Per i blocchi di codice nel body, usare indentazione con 4 spazi oppure scrivere la parola `Codice:` seguita dal contenuto su righe successive.
2. **NON usare `$(cat <<'EOF' ... EOF)`** per il body — è fragile con contenuti complessi. Usare il flag `--body-file` con un file temporaneo.
3. **Approccio obbligatorio — blocco unico copia-incolla**: genera un **unico blocco di codice** che contiene sia il `cat` per creare il file temporaneo sia il comando `gh issue create`, separati da `&&`. In questo modo l'utente fa un solo copia-incolla e la issue viene creata immediatamente. Formato:
   ```
   cat > /tmp/issue-body.md << 'ISSUE_EOF'
   ... contenuto body ...
   ISSUE_EOF
   gh issue create --repo ilum75IDB/ivanluminaria.com --title "..." --label "..." --body-file /tmp/issue-body.md
   ```
4. Nel body della issue, i blocchi di codice vanno scritti con triple backtick normalmente — saranno interpretati correttamente da GitHub perché il file viene letto da `--body-file`, non parsato dalla shell.
5. **NON usare caratteri accentati nei titoli** del comando `gh issue create` (nei `--title`). Sostituire à→a, è→e, é→e, ù→u, ò→o, ì→i, ecc. I titoli delle issue devono essere ASCII-safe.
6. **Testare mentalmente**: prima di fornire il comando, verificare che non ci siano apici, virgolette o backtick che possano confondere la shell zsh.

### Label GitHub create

Le seguenti label sono già state create nel repository `ilum75IDB/ivanluminaria.com`:

| Label                | Colore    | Descrizione                          |
|----------------------|-----------|--------------------------------------|
| `oracle`             | `#F80000` | Articoli sezione Oracle              |
| `blog-article`       | `#336791` | Nuovo articolo del blog              |
| `postgresql`         | `#336791` | Articoli sezione PostgreSQL          |
| `mysql`              | `#00758F` | Articoli sezione MySQL               |
| `project-management` | `#4a4a4a` | Articoli sezione Project Management  |
| `data-warehouse`     | `#1E3A5F` | Articoli sezione Data Warehouse Architect |
| `ai-manager`         | `#8B5CF6` | Articoli sezione AI Manager          |

Quando si crea una nuova issue per un articolo, usare sempre la label `blog-article` insieme alla label della sezione corrispondente (es. `--label "oracle,blog-article"`).

## Sincronizzazione repo con l'utente

L'utente lavora in locale sul suo Mac, Claude lavora su una branch separata. Ogni volta che si fanno modifiche o si devono sincronizzare i repo, seguire queste regole.

### Dopo ogni commit/push di Claude

Dopo aver fatto commit e push sulla branch di sviluppo, fornire **sempre** all'utente i comandi per:

1. Posizionarsi sulla branch corretta (se non ci è già)
2. Aggiornare il repo locale con le modifiche

Formato:

```bash
git fetch origin <branch-name>
git checkout <branch-name>
git pull origin <branch-name>
```

### Quando l'utente dice di aver fatto modifiche in locale

Fornire i comandi per aggiornare il repo remoto in modo che Claude possa poi aggiornare il suo repo locale:

```bash
git add <files>
git commit -m "descrizione modifiche"
git push -u origin <branch-name>
```

Poi, dopo che l'utente conferma il push, Claude esegue `git pull origin <branch-name>` per allinearsi.

### Quando l'utente dice "ora possiamo portare tutto online"

Significa: merge nella branch main, push al remoto, e ritorno sulla branch di sviluppo. Fornire i comandi nell'ordine:

```bash
git checkout main
git pull origin main
git merge <branch-name> -m "Merge <branch-name>: <descrizione>"
git push -u origin main
git checkout <branch-name>
```

Dove `<branch-name>` è la branch di sviluppo corrente.

**Messaggio di merge obbligatorio**: il comando `git merge` deve **sempre** includere un messaggio esplicativo (flag `-m`) che riassuma cosa è stato fatto nella branch. Il messaggio deve:

1. Iniziare con `Merge <branch-name>:` seguito da una descrizione
2. Elencare in modo sintetico le modifiche principali (nuovi articoli, bug fix, modifiche CSS, ecc.)
3. Se ci sono issue chiuse, menzionarle (es. `Fix #57, #58`)

Esempio:
```
git merge claude/blog-fix-homepage-xyz -m "Merge claude/blog-fix-homepage-xyz: fix hero images e layout homepage

- Fix #57: sostituito .Fill con .Fit per hero images (no cropping)
- Fix #58: max-width 1600px per monitor grandi, navbar contenuta
- Ottimizzate dimensioni font e layout griglia per desktop e mobile
- Aggiunte descrizioni articoli nella griglia homepage"
```

## LinkedIn Post per promozione articoli

Quando l'utente chiede di creare un post LinkedIn per promuovere un nuovo articolo del blog (o dice "fammi il post LinkedIn", "prepara il post per LinkedIn", ecc.), **seguire automaticamente queste regole** senza bisogno che vengano ripetute ogni volta.

### Cadenza settimanale

Due post a settimana:

1. **Martedì** — post principale con link all'articolo appena pubblicato (l'articolo è online dalle 08:10 CET, il post va schedulato su Buffer per le ~10:05–10:15 CET)
2. **Venerdì ~15:00** — post teaser che anticipa l'articolo del martedì successivo, creando curiosità senza spoilerare il contenuto. **Se il venerdì cade su una festività italiana** (vedi `docs/HOLIDAYS_CALENDAR.md`), **anticipare il teaser al giovedì stesso orario** — l'engagement in giornata festiva è quasi zero e il post va sprecato

### Slot Buffer principali

Gli slot fissi configurati su Buffer per la pubblicazione automatica dei post LinkedIn sono:

| Slot                         | Quando si usa                                             | Orario CET |
|------------------------------|-----------------------------------------------------------|------------|
| **Martedì 10:15**            | Post principale (settimana standard)                      | 10:15      |
| **Mercoledì 16:20**          | Post principale (quando il martedì è festività italiana)  | 16:20      |
| **Giovedì 17:10**            | Teaser (quando il venerdì è festività italiana)           | 17:10      |
| **Venerdì 15:20**            | Teaser (settimana standard)                               | 15:20      |

**Importante — non confondere gli orari**:
- L'**articolo Hugo** va online sul sito alle **08:03 CET** (cron GitHub Actions). Questo orario riguarda solo il sito, non il post LinkedIn
- Il **post LinkedIn** segue invece gli slot Buffer sopra
- Nei testi dei post LinkedIn **non specificare orari** — usare solo il giorno della settimana (es. "Next Wednesday on the blog", "Mercoledì prossimo sul blog"). Questo evita disallineamenti tra orario articolo (08:03 CET) e orario post Buffer

Quando l'utente chiede "fammi i post della settimana" o simili, generare **entrambi** i post: quello del martedì per l'articolo in uscita e quello del venerdì per l'articolo della settimana successiva.

### Post teaser del venerdì — regole specifiche

- **NON includere il link all'articolo** — l'articolo non è ancora pubblicato. Usare solo il link alla homepage: `👉 https://ivanluminaria.com`
- **NON spoilerare** il contenuto — non dire esplicitamente di cosa parla l'articolo. Lanciare un indizio, un numero, una situazione misteriosa che crei curiosità
- **Chiudere con** "Martedì prossimo sul blog." / "Next Tuesday on the blog."
- **NON aggiungere** la riga sulle traduzioni disponibili (l'articolo non è ancora online)
- Stesse regole di tono, formato e hashtag del post principale

### Formato

- Due versioni: prima `🇬🇧 English version:` poi `🇮🇹 Versione italiana:` (ordine EN → IT per massimizzare l'anteprima su feed internazionali, dato che i primi ~150 caratteri sono quelli che compaiono nel preview LinkedIn)
- Post **BREVE**: massimo 8-10 righe per lingua (deve essere letto in 15 secondi da cellulare)
- La riga con il link all'articolo deve iniziare con 👉
- Dopo il link all'articolo, aggiungere **sempre** una riga che segnala le traduzioni disponibili: "Disponibile anche in 🇬🇧 English, 🇪🇸 Español e 🇷🇴 Română sul sito." (nella versione EN: "Also available in 🇮🇹 Italiano, 🇪🇸 Español and 🇷🇴 Română on the website.")
- Chiudere con un blocco unico di hashtag (10-15, mix italiano/inglese)

### Tono

- Prima persona singolare (è Ivan che parla)
- Leggermente ironico, come chi racconta un aneddoto a un collega al bar
- Aprire con un dato, un numero o una situazione concreta che agganci subito
- Niente frasi motivazionali, niente "in conclusione", niente "scopri come"
- Deve sembrare scritto da una persona vera, non da un'AI
- Frasi corte, ritmo veloce, qualche frase secca ad effetto

### Divieti

- Non usare "In un mondo dove...", "È fondamentale...", "Let's dive in...", "In today's fast-paced world..."
- Non usare assolutismi da clickbait: "quello che nessuno ti dice", "tutti sanno", "non tutti sanno", "il segreto che...", "cosa nessuno sa". Il valore deve emergere dal contenuto, non da promesse sensazionalistiche
- Non usare elenchi puntati
- Non fare il riassunto dell'articolo — creare curiosità
- Non essere didattico o professorale
- Non superare le 10 righe per versione

### Hashtag

- 10-15 hashtag in un blocco unico alla fine del post
- Mix italiano/inglese per massimizzare la reach
- Coprire: prodotto/tecnologia, tema dell'articolo, luogo se rilevante, angolo professionale

### Procedura

1. Leggere l'articolo (almeno la versione italiana) per capire il tema, l'angolo personale e i dati chiave
2. Identificare l'hook migliore: un numero, un paradosso, una situazione concreta vissuta in prima persona
3. Scrivere il post seguendo le regole sopra
4. Proporre il risultato completo (EN + IT + hashtag) pronto per il copia-incolla su LinkedIn

### Scheduling automatico via MCP Buffer ufficiale

Oltre al workflow copia-incolla manuale (sopra), il progetto integra il **server MCP ufficiale di Buffer** (`https://mcp.buffer.com/mcp`) per schedulare i post LinkedIn direttamente in coda Buffer, evitando il passaggio manuale via dashboard.

**Setup**:

- Server MCP configurato in `.mcp.json` (project scope, committato — contiene solo URL pubblico, nessun token)
- Auth: OAuth 2.1 al primo tool call → Claude apre browser, l'utente autorizza l'app Buffer, token salvato in `~/.claude/.credentials` (mai nel repo)
- Account Buffer: piano Free → 3 canali simultanei + **10 post in coda per canale** (sufficiente per cadenza 2 post/settimana × 5 settimane)
- File di tracking idempotenza: `docs/BUFFER_QUEUE.md` (committato), aggiornato dopo ogni scheduling riuscito

**Quando attivare il workflow MCP**:

- **Trigger esplicito**: l'utente dice "schedula i post Buffer per articolo X" / "schedula main e teaser per `<slug>`" / "metti in coda Buffer X"
- **Mai automatico** dopo step 4 (RO) o dopo il commit della versione finale — richiede sempre l'approvazione esplicita del testo prima del push verso Buffer
- **Mai sovrascrivere** uno slot Buffer già occupato senza istruzione esplicita: se la query `get_scheduled_posts` rileva conflitto, Claude segnala e si ferma

**Flusso operativo "schedula post Buffer per articolo X"**:

1. **Idempotency check**: leggere `docs/BUFFER_QUEUE.md` → se lo slug X compare già in "Coda corrente" o "Storico", fermarsi e segnalarlo all'utente (eventuale comando di re-schedule esplicito necessario)
2. **Calcolo slot**:
   - Leggere `docs/HUGO_PUBLICATIONS_TABLE.md` per ottenere la data di pubblicazione `D` dell'articolo X
   - Leggere `docs/HOLIDAYS_CALENDAR.md` per verificare festività italiane
   - **Main slot**: `D` alle 10:15 CET (shift mercoledì 16:20 se `D` è festività)
   - **Teaser slot**: venerdì precedente (`D − 4 giorni`) alle 15:20 CET (shift giovedì 17:10 se festività)
3. **Generazione testi**: scrivere main e teaser seguendo TUTTE le regole della macro-sezione "LinkedIn Post per promozione articoli" sopra (formato EN→IT, tono, divieti AI-tells, hashtag, lunghezza max 10 righe/lingua, teaser senza link articolo + chiusura "Martedì prossimo sul blog")
4. **Verifica slot Buffer**: chiamata MCP `get_scheduled_posts` sui due slot calcolati → se uno o entrambi sono già occupati da altri post, segnalare conflitto all'utente e fermarsi
5. **Approvazione esplicita dell'utente**: mostrare i 2 testi completi + le 2 datetime calcolate + lo stato slot Buffer → chiedere conferma `Sì/No` via `AskUserQuestion`. **Mai pushare senza esplicito Sì.**
6. **Scheduling via MCP**: su `Sì`, chiamata MCP `create_post` × 2 (uno per teaser, uno per main) sul canale LinkedIn collegato, con `scheduled_at` esatto e testo approvato
7. **Aggiornamento tracking**: aggiungere riga in "Coda corrente" di `docs/BUFFER_QUEUE.md` con `slug | data pubblicazione | teaser_post_id | teaser_scheduled_at | main_post_id | main_scheduled_at | timestamp scheduling`
8. **Commit + push**: messaggio convenzionale `chore(buffer): schedule post LinkedIn per <slug> (teaser <date> + main <date>)`

**Comandi correlati supportati**:

- *"fammi vedere la coda Buffer"* → MCP `get_scheduled_posts` + render tabella in chat
- *"aggiorna stato coda Buffer"* → query post `published` recenti → sposta entry da "Coda corrente" a "Storico" in `BUFFER_QUEUE.md`
- *"cancella post Buffer di articolo X"* → idempotency check + MCP `delete_post` × 2 (teaser + main) + rimozione riga `BUFFER_QUEUE.md` + commit
- *"riscrivi il testo del post Buffer di X"* → MCP `update_post` (NON delete+create — preserva il `post_id` e lo slot)

**Cosa il workflow MCP NON sostituisce**:

- La revisione manuale del testo prima del push (step 5 sopra è obbligatorio)
- Le regole di tono, formato, divieti AI-tells (valgono identiche)
- L'eventuale shift dello slot per festività italiane (Claude lo calcola, ma se la festività emerge a posteriori va corretto manualmente con `update_post` via MCP)
- La possibilità di pubblicare un post fuori coda Buffer (post manuale dal LinkedIn nativo) → in quel caso aggiornare comunque `BUFFER_QUEUE.md` per coerenza tracking
