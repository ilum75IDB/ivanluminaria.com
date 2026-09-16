# PROMPT — Technical Leader come identità principale del sito

> **AGGIORNAMENTO 2026-09-16**: il titolo del ruolo è stato aggiornato da «Technical Leader per database mission-critical» a **«Technical Leader per database e Data Warehouse mission-critical»** (in tutte e 4 le lingue) per rendere esplicito che il perimetro include sia OLTP sia DWH. Le occorrenze nel corpo di questo prompt storico **non sono state modificate** — riflettono lo stato al momento del bootstrap del posizionamento (2026-09-14). Per il testo del ruolo attualmente live sul sito, riferirsi ai file `content/`, `config/`, `i18n/` e `data/`.

> **Per Claude Code.** Questo documento è un prompt autosufficiente: contiene decisioni, testi in 4 lingue, codice e verifiche. Applicalo dall'inizio alla fine, nell'ordine dei passi, **senza rimettere in discussione le decisioni già prese** (sezione 2). Fermati solo sui **punti aperti** della sezione 3.

- **Creato**: 2026-09-14, in una sessione del progetto `personal-branding-idb`
- **Repository**: `ivanluminaria.com` · **branch di lavoro**: `work-in-progress`
- **Fonti strategiche** (repo `~/Development/APPLICAZIONI/personal-branding-idb`):
  - `01-strategia/07-cv-technical-leader.md` — CV Technical Leader (IT, versione per SILICONDEV: **non** usare intestazione e contatti SILICONDEV)
  - `03-linkedin/01-headline.md` — frase d'effetto approvata
  - `06-consegne/06-tone-of-voice.md` — tone of voice approvato (serio 75 · informale 60 · rispettoso 80 · pragmatico 80 · istituzionale 65)
  - `01-strategia/04-avatar-cliente.md` — lettore di riferimento: Marco Ferrari, CIO di banca mid-tier
- **Regole di scrittura del repo**: `docs/WRITER_BRIEFING.md` e `docs/STILE_LINGUISTICO.md` (in particolare il tema *Credibilità*: niente «posso essere sincero?», «sinceramente», «a dire il vero»)

---

## 1. Obiettivo

Far emergere **«Technical Leader per database mission-critical»** come identità principale del sito, con i 4 profili storici (DWH Architect, Oracle DBA, Oracle PL/SQL, Project Manager) presentati come **pilastri** di quel ruolo.

| # | Modifica | File principali |
|---|---|---|
| A | Ruolo e frase d'effetto sotto il nome nella brand-bar | `layouts/partials/header/hybrid.html`, `i18n/*.yaml`, `assets/css/custom.css` |
| B | Pagina «Know-How e Impatto»: Technical Leader in evidenza, gli altri 4 come pilastri | `content/resumes/_index.*.md`, `layouts/shortcodes/kh-role.html`, `layouts/resumes/list.html`, `i18n/*.yaml`, `assets/css/custom.css` |
| C | Nuova pagina profilo `resumes/technical-leader/` in 4 lingue | `content/resumes/technical-leader/index.*.md` |
| D | CV Technical Leader **in inglese, 2 pagine**, sorgente md + PDF | `docs/CV_Technical_Leader_Ivan_Luminaria_202609_EN.md`, `docs/cv-print/cv-print.css`, `static/downloads/CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf` |
| E | Sezione `project-management` rinominata «Leadership tecnica e progetti» (slug invariato) | `content/posts/project-management/_index.*.md` |
| F | CTA di fine articolo: la sezione rimanda al profilo Technical Leader | `layouts/_partials/article-cta.html`, `data/cta_copy.yaml` |
| G | Description del sito e headline autore allineate | `config/_default/languages.*.toml`, `config/_default/params.toml` |

---

## 2. Decisioni già prese (non ridiscuterle)

1. **Nessuna nuova categoria «Technical Leader»**. Le sezioni del blog sono argomenti; Technical Leader è un ruolo. Si rinomina solo il **titolo** della sezione `project-management`, lasciando lo **slug invariato** (nessun URL cambia, nessun layout con le slice di sezioni va toccato).
2. **Know-How**: Technical Leader è la prima scheda, più grande; le 4 schede esistenti restano **identiche nel testo** e scendono sotto un titolo «I quattro pilastri».
3. **Brand-bar**: sotto «IVAN LUMINARIA» compaiono il ruolo e la frase d'effetto approvata. Su mobile la frase si nasconde.
4. **CV PDF**: inglese, **esattamente 2 pagine**, ottimizzato per il ruolo, con i contatti personali (non SILICONDEV). Nome file: `CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf`.
5. **Aree di intervento** nel CV e nella pagina: descritte in modo neutro, **senza marchio commerciale e senza prezzi**.
6. **CTA**: solo la sezione `project-management` passa al profilo `technical-leader`. Oracle, PostgreSQL, MySQL e Data Warehouse restano come sono.
7. **Branch**: si lavora solo su `work-in-progress`. **Mai push su `main`**: il merge lo decide Ivan (vedi passo 9).

---

## 3. Punti aperti — da chiedere a Ivan PRIMA di iniziare

Fai **una sola domanda** con i tre punti (usa `AskUserQuestion`), proponendo il default indicato.

| # | Domanda | Default proposto |
|---|---|---|
| Q1 | **Cronologia**: i CV sul sito (marzo 2026) mettono POSTE ITALIANE sotto IDEA DB CONSULTING «2021 – Present»; i CV di settembre 2026 mettono **SILICONDEV S.p.A. lug 2025 – oggi** e IDEA DB «2021 – giu 2025». Quale va nel profilo e nel PDF Technical Leader? | **Settembre 2026** (SILICONDEV da lug 2025). Gli altri 4 CV verranno allineati in un secondo momento, fuori da questo prompt |
| Q2 | **URL LinkedIn**: il sito usa `https://www.linkedin.com/in/ivanluminaria`, i CV `https://www.linkedin.com/in/ivan-luminaria`. Quale è quello giusto? (LinkedIn blocca le verifiche automatiche) | Quello già usato sul sito: `ivanluminaria` |
| Q3 | **Atradius**: nel CV di settembre compare «2022 – 2026» dentro un'esperienza IDEA DB chiusa a giugno 2025. Quali date? | **2022 – giu 2025** |

Sostituisci ovunque nei testi qui sotto i segnaposto `{{LINKEDIN_URL}}` e `{{ATRADIUS_DATE}}` con le risposte. I testi sono scritti con la cronologia di default (Q1): se Ivan sceglie diversamente, adatta solo la sezione esperienze.

---

## 4. Passo 0 — Allineamento del branch

```bash
cd ~/Development/APPLICAZIONI/My-Web-Site/ivanluminaria.com
git fetch origin
git checkout work-in-progress
git pull --ff-only origin work-in-progress
git merge --ff-only origin/main        # al 2026-09-14 main era avanti di 1 commit
git status -sb                         # deve essere pulito
hugo version                           # atteso v0.163+ extended
```

Se il merge fast-forward fallisce, **fermati** e chiedi a Ivan.

---

## 5. Passo A — Brand-bar: ruolo e frase d'effetto

### A.1 Contesto verificato

- Il layout di testata attivo è `hybrid` (`config/_default/params.toml` → `[header] layout = "hybrid"`), con override in `layouts/partials/header/hybrid.html`.
- Il nome è renderizzato da `{{ partial "logo.html" . }}` come `<a>` **figlio diretto** di `<div class="z-40 flex flex-row items-center">`. Il CSS esistente usa `nav .z-40 > a` (desktop, righe ~40-51) e regole mobile (righe ~1317-1356) che correggono un overflow del burger: **non romperle**.
- Soluzione: aggiungere ruolo e frase come **fratelli** del link, dentro lo stesso `div.z-40`, trasformato in colonna.

### A.2 `layouts/partials/header/hybrid.html`

Sostituisci:

```html
    <div class="z-40 flex flex-row items-center">
      {{ partial "logo.html" . }}
    </div>
```

con:

```html
    <div class="z-40 flex flex-col items-start brand-wrap">
      {{ partial "logo.html" . }}
      <span class="brand-role">{{ i18n "brand.role" }}</span>
      <span class="brand-tagline">{{ i18n "brand.tagline" }}</span>
    </div>
```

Verifica con `grep -rn "logo.html" layouts` che `layouts/partials/header/basic.html` non sia usato (è un override inattivo: non modificarlo).

### A.3 `i18n/*.yaml` — nuovo blocco `brand` (in fondo al file)

`i18n/it.yaml`
```yaml
brand:
  role: "Technical Leader per database mission-critical"
  tagline: "Aiuto CIO e CTO ad avere i dati pronti a rispondere al business, quando nascono le domande"
```

`i18n/en.yaml`
```yaml
brand:
  role: "Technical Leader for mission-critical databases"
  tagline: "Helping CIOs & CTOs have data ready the moment the business asks"
```

`i18n/es.yaml`
```yaml
brand:
  role: "Technical Leader para bases de datos de misión crítica"
  tagline: "Ayudo a CIOs y CTOs a tener los datos listos para responder al negocio, cuando surgen las preguntas"
```

`i18n/ro.yaml`
```yaml
brand:
  role: "Technical Leader pentru baze de date critice"
  tagline: "Ajut CIO și CTO să aibă datele pregătite pentru business, în momentul în care apar întrebările"
```

### A.4 `assets/css/custom.css`

Aggiungi **subito dopo** la regola `nav .z-40 > a:hover { … }` (sezione «HEADER / NAV BRAND»):

```css
/* 1b. BRAND BLOCK: nome + ruolo + frase d'effetto (Technical Leader, 2026-09) */
nav .z-40.brand-wrap {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.1rem;
}
.brand-role {
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  line-height: 1.2;
  color: var(--ivan-red);
}
.brand-tagline {
  font-size: 0.75rem;
  font-weight: 500;
  line-height: 1.35;
  color: var(--ivan-gray-obj);
  max-width: 32rem;
}
.dark .brand-role { color: #ff5c5c; }
.dark .brand-tagline { color: rgb(163, 163, 163); }
```

Aggiungi **in fondo** alla media query mobile che contiene `nav .z-40 { align-items: center !important; }` (righe ~1333-1356), prima della sua `}` di chiusura:

```css
  /* Brand block su mobile: ruolo su una riga con ellissi, frase nascosta */
  nav .z-40.brand-wrap {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
  .brand-tagline {
    display: none !important;
  }
  .brand-role {
    font-size: 0.7rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
```

Tra 768px e 1190px (hamburger attivo, spazio medio) la frase può andare a capo: controllalo a vista nel passo 8 e, se spinge il burger fuori dal viewport, nascondi `.brand-tagline` anche sotto 1190px.

**Commit**: `feat(brand): ruolo Technical Leader e frase d'effetto nella brand-bar (IT/EN/ES/RO)`

---

## 6. Passo B — Pagina «Know-How e Impatto»

### B.1 Shortcode `layouts/shortcodes/kh-role.html`

1. Nel commento dei parametri aggiungi:
   ```
       featured — "true" per la scheda principale (Technical Leader): stile in evidenza + etichetta
   ```
2. Dopo `{{- $sectors := .Get "sectors" -}}` aggiungi:
   ```go-html-template
   {{- $featured := eq (.Get "featured") "true" -}}
   ```
3. Sostituisci l'apertura della card e l'header:
   ```html
   <div class="kh-role-card" data-role="{{ $role }}">
     <div class="kh-role-main">
       <div class="kh-role-header">
         <h3 class="kh-role-title">{{ $title }}</h3>
       </div>
   ```
   con:
   ```html
   <div class="kh-role-card{{ if $featured }} kh-role-card--featured{{ end }}" data-role="{{ $role }}">
     <div class="kh-role-main">
       <div class="kh-role-header">
         {{ if $featured }}<div class="kh-role-eyebrow">{{ i18n "knowhow.featured_label" }}</div>{{ end }}
         <h3 class="kh-role-title">{{ $title }}</h3>
       </div>
   ```

### B.2 Contatore in `layouts/resumes/list.html`

Sostituisci:

```html
        {{ if gt $rolesCount 0 }}
          <div class="kh-header-count">
            <strong>{{ $rolesCount }}</strong>&nbsp;{{ i18n "knowhow.count_text" }}
          </div>
        {{ end }}
```

con (il ruolo principale non si conta tra i pilastri):

```html
        {{ if gt $rolesCount 1 }}
          <div class="kh-header-count">
            <strong>1</strong>&nbsp;{{ i18n "knowhow.role_word" }} · <strong>{{ sub $rolesCount 1 }}</strong>&nbsp;{{ i18n "knowhow.pillars_word" }}
          </div>
        {{ end }}
```

### B.3 `i18n/*.yaml` — chiavi nuove nel blocco `knowhow` (lascia le esistenti)

| Chiave | it | en | es | ro |
|---|---|---|---|---|
| `featured_label` | `"Il mio ruolo oggi"` | `"My role today"` | `"Mi rol hoy"` | `"Rolul meu astăzi"` |
| `role_word` | `"ruolo"` | `"role"` | `"rol"` | `"rol"` |
| `pillars_word` | `"pilastri"` | `"pillars"` | `"pilares"` | `"piloni"` |

`count_text` resta nel file (non più usato dal layout, innocuo).

### B.4 CSS — in `assets/css/custom.css`, dopo il blocco `.dark .kh-role-card { … }`

```css
/* Scheda principale Technical Leader */
.kh-role-card--featured {
  border: 2px solid var(--ivan-red);
  box-shadow: 0 10px 28px rgba(248, 0, 0, 0.08);
  margin-bottom: 3rem;
}
.kh-role-card--featured .kh-role-main {
  padding: 2.5rem 2.75rem;
  background: linear-gradient(135deg, #ffffff 0%, #fdf5f5 100%);
}
.dark .kh-role-card--featured .kh-role-main {
  background: linear-gradient(135deg, rgb(38, 38, 38) 0%, rgb(52, 36, 36) 100%);
}
.kh-role-card--featured .kh-role-title {
  font-size: 1.85rem !important;
}
.kh-role-card--featured .kh-role-body {
  font-size: 1.02rem;
}
.kh-role-eyebrow {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ivan-red);
  margin-bottom: 0.35rem;
}

/* Titolo di raccordo «I quattro pilastri» */
.kh-pillars {
  margin: 0 0 1.5rem;
  padding-top: 0.5rem;
}
.kh-pillars h2 {
  font-size: 1.5rem !important;
  font-weight: 800 !important;
  margin: 0 0 0.35rem !important;
}
.kh-pillars p {
  margin: 0;
  color: var(--ivan-gray-obj);
}
.dark .kh-pillars p {
  color: rgb(163, 163, 163);
}
```

Nella media query `@media (max-width: 900px)` del blocco Know-How aggiungi:

```css
  .kh-role-card--featured .kh-role-main {
    padding: 1.75rem 1.5rem;
  }
  .kh-role-card--featured .kh-role-title {
    font-size: 1.45rem !important;
  }
```

### B.5 `content/resumes/_index.*.md` — frontmatter, intro, scheda principale, raccordo

In ciascuna lingua:

1. **Frontmatter**: sostituisci `seoTitle`, `description` e aggiorna `lastmod` alla data di applicazione. `title`, `hero_title`, `date`, `draft`, `image` restano invariati.
2. **Intro** `<div class="kh-intro">`: aggiungi **una riga finale** prima di `</div>` (testo sotto).
3. **Subito dopo** `</div>` dell'intro: inserisci la scheda Technical Leader e il blocco `kh-pillars`.
4. Le 4 schede esistenti (`dwh`, `pm`, `oracle`, `plsql`) restano **identiche**, nello stesso ordine, dopo il blocco `kh-pillars`.

Verifica le lunghezze con lo script del passo 8 (`seoTitle` ≤ 65, `description` ≤ 160): se una supera il limite, accorciala senza cambiarne il senso.

#### IT — `content/resumes/_index.it.md`

```yaml
seoTitle: "Ivan Luminaria, Technical Leader per database mission-critical"
description: "Technical Leader per database mission-critical: 30 anni tra banche, assicurazioni, telco e PA. Quattro pilastri: DWH, Oracle DBA, PL/SQL e project management."
```

Riga finale dell'intro:

```markdown
Oggi quelle profondità lavorano insieme, in un unico ruolo.
```

Scheda e raccordo:

```markdown
{{< kh-role role="tl" featured="true" title="Technical Leader per database mission-critical" roadmap="technical-leader" pdf="CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" sectors="Banking,Assicurazioni,Telco,Pubblica Amministrazione,Mobilità e pagamenti" >}}

Oggi il mio lavoro è affiancare CIO, CTO e IT Director quando un sistema dati mission-critical rallenta, si ferma o deve prendere una direzione nuova.

Quando la causa attraversa più livelli — applicazione, SQL, database, sistema operativo, storage, rete — serve chi li legga insieme.  
E chi sappia spiegare ogni passaggio a chi deve decidere.

Porto trent'anni di sistemi reali in banche, assicurazioni, telco e Pubblica Amministrazione.  
E un metodo che resta al team quando l'intervento finisce.

Sistemi più stabili.  
Decisioni difendibili.  
Persone più autonome.

{{< /kh-role >}}

<div class="kh-pillars">

## I quattro pilastri

Le competenze su cui si regge il ruolo di Technical Leader. Ognuna ha la sua roadmap e il suo CV.

</div>
```

#### EN — `content/resumes/_index.en.md`

```yaml
seoTitle: "Ivan Luminaria, Technical Leader for mission-critical databases"
description: "Technical Leader for mission-critical databases: 30 years across banking, insurance, telco and public sector. Four pillars: DWH, Oracle DBA, PL/SQL and PM."
```

Riga finale dell'intro:

```markdown
Today those depths work together, in a single role.
```

Scheda e raccordo:

```markdown
{{< kh-role role="tl" featured="true" title="Technical Leader for mission-critical databases" roadmap="technical-leader" pdf="CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" sectors="Banking,Insurance,Telco,Public sector,Mobility & payments" >}}

Today my work is to stand alongside CIOs, CTOs and IT Directors when a mission-critical data system slows down, stops, or needs to take a new direction.

When the cause runs across several layers — application, SQL, database, operating system, storage, network — you need someone who reads them together.  
And who can explain every step to the people who decide.

I bring thirty years of real systems in banking, insurance, telco and the public sector.  
And a method that stays with the team when the engagement ends.

More stable systems.  
Defensible decisions.  
More autonomous people.

{{< /kh-role >}}

<div class="kh-pillars">

## The four pillars

The expertise the Technical Leader role stands on. Each one has its own roadmap and CV.

</div>
```

#### ES — `content/resumes/_index.es.md`

```yaml
seoTitle: "Ivan Luminaria, Technical Leader de bases de datos críticas"
description: "Technical Leader de bases de datos de misión crítica: 30 años en banca, seguros, telco y sector público. Cuatro pilares: DWH, Oracle DBA, PL/SQL y PM."
```

Riga finale dell'intro:

```markdown
Hoy esas profundidades trabajan juntas, en un único rol.
```

Scheda e raccordo:

```markdown
{{< kh-role role="tl" featured="true" title="Technical Leader para bases de datos de misión crítica" roadmap="technical-leader" pdf="CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" sectors="Banca,Seguros,Telco,Sector público,Movilidad y pagos" >}}

Hoy mi trabajo es acompañar a CIOs, CTOs e IT Directors cuando un sistema de datos de misión crítica se ralentiza, se detiene o debe tomar una nueva dirección.

Cuando la causa atraviesa varios niveles — aplicación, SQL, base de datos, sistema operativo, almacenamiento, red — hace falta alguien que los lea juntos.  
Y que sepa explicar cada paso a quien debe decidir.

Aporto treinta años de sistemas reales en banca, seguros, telco y sector público.  
Y un método que se queda con el equipo cuando termina la intervención.

Sistemas más estables.  
Decisiones defendibles.  
Personas más autónomas.

{{< /kh-role >}}

<div class="kh-pillars">

## Los cuatro pilares

Las competencias sobre las que se apoya el rol de Technical Leader. Cada una tiene su roadmap y su CV.

</div>
```

#### RO — `content/resumes/_index.ro.md`

```yaml
seoTitle: "Ivan Luminaria, Technical Leader pentru baze de date critice"
description: "Technical Leader pentru baze de date critice: 30 de ani în banking, asigurări, telco și sectorul public. Patru piloni: DWH, Oracle DBA, PL/SQL și PM."
```

Riga finale dell'intro:

```markdown
Astăzi aceste profunzimi lucrează împreună, într-un singur rol.
```

Scheda e raccordo:

```markdown
{{< kh-role role="tl" featured="true" title="Technical Leader pentru baze de date critice" roadmap="technical-leader" pdf="CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" sectors="Banking,Asigurări,Telco,Sector public,Mobilitate și plăți" >}}

Astăzi munca mea este să fiu alături de CIO, CTO și IT Directori atunci când un sistem de date critic încetinește, se oprește sau trebuie să ia o direcție nouă.

Când cauza traversează mai multe niveluri — aplicație, SQL, bază de date, sistem de operare, stocare, rețea — e nevoie de cineva care să le citească împreună.  
Și care să știe să explice fiecare pas celor care decid.

Aduc treizeci de ani de sisteme reale în banking, asigurări, telco și sectorul public.  
Și o metodă care rămâne echipei după încheierea intervenției.

Sisteme mai stabile.  
Decizii care pot fi susținute.  
Oameni mai autonomi.

{{< /kh-role >}}

<div class="kh-pillars">

## Cei patru piloni

Competențele pe care se sprijină rolul de Technical Leader. Fiecare are propriul roadmap și propriul CV.

</div>
```

**Commit**: `feat(resumes): Technical Leader come profilo principale nella pagina Know-How (IT/EN/ES/RO)`

---

## 7. Passo C — Pagina profilo `content/resumes/technical-leader/`

Crea `index.it.md`, `index.en.md`, `index.es.md`, `index.ro.md` con **la stessa struttura** delle pagine esistenti (modello: `content/resumes/oracle-dba/index.*.md`, `layout: "simple"`).

- **IT**: usa il testo completo qui sotto.
- **EN**: traduzione fedele dell'IT (non il CV di 2 pagine, che è una sintesi).
- **ES** e **RO**: traduzione fedele dell'IT. Per i titoli di sezione e le formule fisse («Scarica PDF», «Profilo LinkedIn», «Torna alla pagina precedente», riga GDPR, luogo e data) **copia esattamente** le formulazioni già usate in `content/resumes/oracle-dba/index.es.md` e `index.ro.md`.
- In tutte le lingue: «Technical Leader» resta in inglese; nomi di prodotto, aziende e acronimi restano invariati; numeri identici.
- Frontmatter per lingua:

| Lingua | `title` | `seoTitle` (≤65) | `description` (≤160) |
|---|---|---|---|
| it | `Technical Leader per database mission-critical` | `Ivan Luminaria \| Technical Leader per database mission-critical` | `Ivan Luminaria, Technical Leader per database mission-critical: 30 anni tra Oracle, PostgreSQL, MySQL e DWH al fianco di CIO e CTO in banche, telco e PA.` |
| en | `Technical Leader for Mission-Critical Databases` | `Ivan Luminaria \| Technical Leader, Mission-Critical Databases` | `Ivan Luminaria, Technical Leader for mission-critical databases: 30 years of Oracle, PostgreSQL, MySQL and DWH alongside CIOs and CTOs in banking and telco.` |
| es | `Technical Leader para bases de datos de misión crítica` | `Ivan Luminaria \| Technical Leader, bases de datos críticas` | `Ivan Luminaria, Technical Leader de bases de datos críticas: 30 años de Oracle, PostgreSQL, MySQL y DWH junto a CIOs y CTOs en banca, telco y sector público.` |
| ro | `Technical Leader pentru baze de date critice` | `Ivan Luminaria \| Technical Leader, baze de date critice` | `Ivan Luminaria, Technical Leader pentru baze de date critice: 30 de ani de Oracle, PostgreSQL, MySQL și DWH alături de CIO și CTO în banking, telco și PA.` |

(Il carattere `\|` nella tabella è solo escape Markdown: nel frontmatter scrivi `|`.)

### Testo IT completo — `content/resumes/technical-leader/index.it.md`

```markdown
---
title: "Technical Leader per database mission-critical"
seoTitle: "Ivan Luminaria | Technical Leader per database mission-critical"
description: "Ivan Luminaria, Technical Leader per database mission-critical: 30 anni tra Oracle, PostgreSQL, MySQL e DWH al fianco di CIO e CTO in banche, telco e PA."
date: "AAAA-MM-GG"
lastmod: "AAAA-MM-GG"
draft: false
layout: "simple"
---

**[Scarica PDF]({{% staticurl "downloads/CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn]({{LINKEDIN_URL}})**

---

## Profilo Professionale

Technical Leader con quasi 30 anni di esperienza su database mission-critical Oracle, PostgreSQL e MySQL e su Data Warehouse enterprise.

Affianco CIO, CTO e IT Director quando un sistema dati rallenta, si ferma o deve cambiare direzione. Quando la causa attraversa più livelli — applicazione, SQL, database, sistema operativo, storage, rete, architettura dei dati — leggo la catena per intero e spiego ogni passaggio a chi deve decidere.

Tre pilastri tecnici: **database administration**, **performance e troubleshooting**, **Data Warehouse e data architecture**. Due capacità che li tengono insieme: **coordinamento tecnico dei team** e **trasferimento di competenze**, perché ogni intervento lasci sistemi più stabili e persone più autonome.

---

## Aree di intervento

- **Health Check dei database** — valutazione strutturata di performance, affidabilità, capacità e rischi latenti su Oracle, PostgreSQL e MySQL, con un report di evidenze e una roadmap di priorità.
- **Post-Incident Root Cause Analysis** — ricostruzione dell'incidente sui dati reali (AWR, ADDM, ASH, wait event, log applicativi e infrastrutturali), separando cause, conseguenze e semplici correlazioni, con un piano di remediation verificabile.
- **Technical leadership continuativa** — valutazioni tecniche indipendenti, coordinamento tra sviluppo, DBA e infrastruttura, governance delle decisioni architetturali.
- **Data Warehouse design** — progettazione end-to-end di DWH e pipeline ETL/ELT su Oracle e PostgreSQL, con attenzione a modellazione, tempi di caricamento e sostenibilità nel tempo.

---

## Risultati in evidenza

- Circa **1.500 istanze** MySQL e PostgreSQL amministrate per un operatore postale e logistico nazionale.
- **Oltre 30 database Oracle critici (70+ istanze)** su Exadata per un operatore telco con **oltre 20 milioni di utenti** prepagati; fino a **800 milioni di record di traffico al giorno**; query critiche sotto i **500 ms**.
- Batch analitici critici ridotti **da 4 ore a meno di 30 minuti** su Oracle in OCI e Autonomous Database.
- Data Warehouse multi-paese su **4 Paesi europei**: **oltre 60.000 righe di PL/SQL** e caricamento giornaliero completo in **meno di 2 ore**.
- Pipeline ETL/ELT che integrano **oltre 15 sorgenti eterogenee** su dataset superiori ai **2 miliardi di righe**.

---

## Competenze Chiave

### Database mission-critical

- Oracle Database 8i → 21c, Oracle Exadata, Oracle RAC, Oracle Data Guard, Oracle Autonomous Database
- PostgreSQL 14+ (query optimization, partitioning, `pg_stat_statements`, PgBouncer, replica logica, tuning di autovacuum)
- MySQL enterprise (amministrazione, replica, ottimizzazione InnoDB)
- Alta disponibilità e disaster recovery (Data Guard, RMAN, Flashback, procedure di switchover/failover)
- Sicurezza (Oracle TDE, gestione privilegi, auditing), Storage Management (ASM, tablespace)
- Installazione, patching (PSU/CPU/RU), upgrade, migrazioni cross-platform

### Performance tuning cross-layer

- Analisi e diagnostica: AWR, ADDM, ASH, Statspack, SQL Trace, TKPROF, Explain Plan
- SQL tuning: query complesse, hints, SQL Profiles, SQL Plan Management
- Instance tuning: memoria (SGA/PGA), parametri di inizializzazione, analisi dei wait event
- Design per la performance: indicizzazione (B-tree, Bitmap, Function-based), partitioning (Range, List, Hash, Composite), compression
- Lettura a livelli: applicazione → SQL → database → sistema operativo → storage → rete → architettura dati

### Data Warehouse e Data Architecture

- Metodologie Kimball e Inmon: Star Schema, Snowflake, Slowly Changing Dimensions, Bus Matrix
- ETL/ELT con PL/SQL e Unix Shell scripting, Oracle Data Integrator, Oracle Warehouse Builder (progetti legacy)
- Business Intelligence: Oracle Analytics Cloud (Semantic Model Designer, dashboard, report)
- Integrazione di sorgenti eterogenee (Oracle, SQL Server, file, sistemi enterprise)

### Cloud

- Oracle Cloud Infrastructure (Compute, Storage, Networking, Database Services, Autonomous Database)
- AWS Aurora PostgreSQL, ambienti Microsoft Azure Database

### Leadership tecnica e coordinamento

- Coordinamento di team distribuiti da 3 a 7 persone, in contesti multiculturali e full remote
- Agile e Scrum (sprint planning, daily stand-up, retrospective, backlog refinement), con formazione certificata
- Circa 10 progetti gestiti con budget tra €100K e €500K, con un solido track record di consegna nei tempi
- Strumenti: Jira, Microsoft Project, Git/GitHub

### Formazione e mentoring

- Trainer in Oracle Italia (2000-2001): SQL, Advanced SQL, PL/SQL, Oracle DBA, Performance & Tuning, Discoverer, Forms, Reports
- Onboarding e mentoring di sviluppatori junior e consulenti

---

## Esperienza Professionale

### SILICONDEV S.p.A. — Roma, Italia (Full Remote)
**Senior Database Consultant — MySQL & PostgreSQL DBA** (per POSTE ITALIANE) | Lug 2025 – Presente

- Amministrazione di circa 1.500 istanze MySQL e PostgreSQL tra produzione, certificazione e sviluppo.
- Monitoraggio delle performance, query tuning, gestione della replica e capacity planning su scala enterprise.
- Supporto ai team di sviluppo e infrastruttura in un contesto database eterogeneo con requisiti di continuità operativa.

---

### IDEA DB CONSULTING S.R.L. — Roma, Italia (Full Remote Europa)
**Amministratore Unico · Technical Leader database & DWH** | 2021 – Giu 2025

- **Oracle DBA, Performance Tuning & PM DWH Lead** (per GENERALI Assicurazioni) | Feb 2024 – Mag 2025:
  - Amministrazione e tuning avanzato di database Oracle da 500 GB a 8 TB per applicazioni del settore assicurativo.
  - Analisi AWR/ADDM, ottimizzazione SQL, risoluzione proattiva dei colli di bottiglia; interfaccia diretta con il cliente su requisiti e scope.
- **DWH Architect & PM Lead** (per ATRADIUS, divisione Surety) | {{ATRADIUS_DATE}}:
  - Data Warehouse Oracle unificato per consolidare i dati di 4 Paesi europei da sorgenti eterogenee (Oracle, SQL Server, file esterni).
  - Intero data model e livello ETL, oltre 60.000 righe di PL/SQL, con framework di caricamento, checkpoint e logging in tempo reale; caricamento giornaliero completo in meno di 2 ore.
- **DWH Architect & Oracle DBA** (per FAI SERVICE) | 2021 – 2023:
  - Modello dati Snowflake su Oracle Analytics Cloud, ETL su Oracle 19c in OCI, dashboard per fatturazione, segmentazione e portafoglio.
- **PL/SQL Expert & Oracle DBA** (per FINWAVE S.p.A.) | 2020 – 2022:
  - Sviluppo PL/SQL avanzato e ottimizzazione di query per applicazioni finanziarie con milioni di transazioni giornaliere.
- **Clienti Banking, Telepass e altri**:
  - Batch analitici critici ridotti da 4 ore a meno di 30 minuti su Oracle in OCI e Autonomous Database.
  - ETL/ELT da oltre 15 sorgenti eterogenee su dataset superiori ai 2 miliardi di righe; DWH su PostgreSQL come alternativa sostenibile a Oracle.

---

### NIMIS CONSULTING S.R.L. — Roma, Italia (Full Remote)
**Senior Oracle DBA & Performance Tuning Expert** (per TIM / HUAWEI) | 2020 – 2022

- Oltre 30 database Oracle critici (70+ istanze) su cluster Exadata a 3 e 5 nodi.
- Reperibilità 24/7 per sistemi al servizio di oltre 20 milioni di utenti prepagati mobile; fact table fino a 800 milioni di record di traffico al giorno.
- Performance tuning proattivo (AWR/ADDM) per SLA sotto i 500 ms; ASM e Oracle TDE.

---

### LIBERO PROFESSIONISTA / CONSULENTE INDIPENDENTE — Roma, Italia (Full Remote Europa)
**Project Manager & Senior DWH Consultant · Oracle DBA · Performance Tuning** | 2013 – 2020

- Circa 10 progetti gestiti per clienti Banking, Telco e servizi, con budget tra €100K e €500K.
- Team da 3 a 7 persone in contesti multiculturali distribuiti, con approccio Agile.
- Data Warehouse per Banking, Insurance e Telco con pipeline da 500 milioni di righe per ciclo di caricamento.
- Configurazioni Oracle Data Guard per alta disponibilità e disaster recovery.

---

### AUSELDA AED GROUP S.P.A. — Roma, Italia
**Data Warehouse Architect · Oracle Project DBA** (per la Pubblica Amministrazione) | 2009 – 2013

- Progettazione Kimball/Inmon di DWH per enti della Pubblica Amministrazione, sviluppo ETL/ELT, product specialist Oracle Warehouse Builder.

---

### ORACLE ITALIA S.R.L. — Varie sedi, Italia & Madrid, Spagna
**Data Warehouse Architect · Oracle DBA · SQL & PL/SQL Developer · Training Specialist** | 1999 – 2009

- Data Warehouse per clienti Telco (TIM, Vodafone, TRE), Finance (Banca d'Italia, Generali, RAS) e Farmaceutico (Menarini); ingaggio internazionale su Vodafone Spagna.
- Training Specialist (2000-2001) su SQL, PL/SQL, Oracle DBA e Performance & Tuning.

---

### ETNOTEAM S.P.A. · 1999 — S.EL.DAT. S.P.A. · 1997 – 1999
**Web e Software Developer · Junior Oracle DBA** (per Telecom, Rover Italia)

---

## Formazione

- **Facoltà di Ingegneria Informatica (Ingegneria del Software)** | Università degli Studi Roma Tre, Roma | 1994 – 2000
- **Diploma di Maturità Scientifica** | Liceo Scientifico Isacco Newton / Manieri Copernico, Roma | 1988 – 1993
- **Inglese Avanzato (C1/C2)** | The British Council, Roma | 2003 – 2004
- Formazione continua: Scrum Agile e Project Management (Randstad / Forma.temp, 2024) · Data Wrangling with SQL (Coursera, UC Davis, 2021) · Advanced SQL for Query Tuning e Oracle 12c (LinkedIn Learning, 2020)

---

## Lingue

- **Italiano**: Madrelingua
- **Inglese**: C1/C2 (Fluente, professionale)
- **Spagnolo**: C1 (Fluente)
- **Rumeno**: C1 (Fluente)
- **Francese**: A1/A2 (Base)

---

## Competenze Trasversali

- Lettura trasversale delle situazioni complesse, fino alla causa reale
- Traduzione tra livello tecnico e livello business, per team e management
- Coordinamento di team distribuiti, in presenza e full remote
- Mentoring e trasferimento di competenze
- Gestione delle priorità sotto pressione operativa
- Comunicazione tecnica chiara, basata sulle evidenze

---

*Autorizzo il trattamento dei miei dati personali ai sensi dell'Art. 13 del Regolamento UE 2016/679 (GDPR).*

Roma, Settembre 2026

---

**[Scarica PDF]({{% staticurl "downloads/CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf" %}})** | **[Profilo LinkedIn]({{LINKEDIN_URL}})** | **[Torna alla pagina precedente](/it/resumes/)**
```

Nelle altre lingue il link finale punta a `/en/resumes/`, `/es/resumes/`, `/ro/resumes/`.

**Commit**: `feat(resumes): pagina profilo Technical Leader (IT/EN/ES/RO)`

---

## 8. Passo D — CV Technical Leader in inglese, 2 pagine

### D.1 Contesto verificato

- I 4 PDF esistenti in `static/downloads/` sono stati prodotti con Google Docs e sono di 4 pagine: **non** servono da modello tecnico.
- Sul Mac sono disponibili `pandoc` e Google Chrome; **non** sono installati typst, LaTeX, weasyprint, pdfinfo.
- Pipeline: Markdown → HTML standalone con CSS di stampa A4 (pandoc) → PDF (Chrome headless) → conteggio pagine (Python).

### D.2 `docs/cv-print/cv-print.css`

```css
@page { size: A4; margin: 13mm 15mm; }
html { font-size: 9.6pt; }
body {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #222;
  line-height: 1.32;
  margin: 0;
}
h1 {
  font-size: 20pt;
  margin: 0;
  color: #336791;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
p.role { margin: 1pt 0 0; font-size: 11.5pt; font-weight: 700; color: #F80000; }
p.contact { margin: 2pt 0 6pt; font-size: 8.8pt; color: #555; }
h2 {
  font-size: 10.2pt;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #336791;
  border-bottom: 1px solid #d6dde6;
  padding-bottom: 1.5pt;
  margin: 8pt 0 3.5pt;
}
h3 { font-size: 9.8pt; margin: 5pt 0 1.5pt; color: #111; }
p { margin: 0 0 3.5pt; }
ul { margin: 0 0 3.5pt; padding-left: 11pt; }
li { margin: 0 0 1.2pt; }
strong { color: #111; }
a { color: inherit; text-decoration: none; }
hr { display: none; }
h2, h3, li { break-inside: avoid; }
p.gdpr { margin-top: 6pt; font-size: 7.8pt; color: #666; }
```

### D.3 `docs/CV_Technical_Leader_Ivan_Luminaria_202609_EN.md`

Contatti: stessi dei CV EN esistenti (`docs/CV_Oracle_DBA_Ivan_Luminaria_202603_EN.md`), ma **solo la città** al posto dell'indirizzo completo.

```markdown
# Ivan Luminaria

<p class="role">Technical Leader for Mission-Critical Databases</p>
<p class="contact">Rome, Italy · (+39) 335 727 1217 · ivan.luminaria@gmail.com · {{LINKEDIN_URL}}</p>

## Profile

Technical Leader with nearly 30 years on mission-critical Oracle, PostgreSQL and MySQL databases and enterprise Data Warehouses. I work alongside CIOs, CTOs and IT Directors when a data system slows down, stops or needs a new direction: I read the whole chain — application, SQL, database, operating system, storage, network, data architecture — and explain every step to the people who decide. Three technical pillars (database administration, performance & troubleshooting, data warehouse & data architecture), held together by team coordination and knowledge transfer.

## Areas of engagement

- **Database Health Check** — structured assessment of performance, reliability, capacity and latent risks, with an evidence-based report and a prioritised roadmap.
- **Post-Incident Root Cause Analysis** — incident reconstruction on real data (AWR, ASH, wait events, application and infrastructure logs), separating causes, consequences and correlations.
- **Ongoing technical leadership** — independent technical assessments, coordination across development, DBA and infrastructure teams, governance of architectural decisions.
- **Data Warehouse design** — end-to-end DWH and ETL/ELT pipelines on Oracle and PostgreSQL.

## Key results

- About **1,500 MySQL and PostgreSQL instances** administered for a national postal and logistics operator.
- **30+ critical Oracle databases (70+ instances)** on Exadata for a telco with **20M+ prepaid mobile users**; up to **800M call records per day**; critical queries **under 500 ms**.
- Critical analytical batches cut **from 4 hours to under 30 minutes** (Oracle on OCI and Autonomous Database).
- Multi-country DWH across **4 European countries**: **60,000+ lines of PL/SQL**, full daily load **under 2 hours**.
- ETL/ELT pipelines integrating **15+ heterogeneous sources** on datasets above **2 billion rows**.

## Core expertise

- **Databases**: Oracle 8i–21c, Exadata, RAC, Data Guard, Autonomous Database · PostgreSQL 14+ · MySQL enterprise · HA/DR (RMAN, Flashback, switchover/failover) · security (TDE, privileges, auditing) · ASM · patching, upgrades, cross-platform migrations
- **Performance**: AWR, ADDM, ASH, SQL Trace/TKPROF, execution plans, SQL Profiles, SQL Plan Management, indexing, partitioning, compression, cross-layer diagnosis
- **Data Warehouse**: Kimball & Inmon, star and snowflake schemas, SCD, bus matrix, PL/SQL ETL/ELT, ODI, OWB, Oracle Analytics Cloud
- **Cloud**: Oracle Cloud Infrastructure, Autonomous Database, AWS Aurora PostgreSQL, Azure Database
- **Leadership**: distributed teams of 3–7 people, Agile/Scrum, ~10 projects (€100K–€500K), Jira, MS Project, Git/GitHub, mentoring and technical training

## Experience

### SILICONDEV S.p.A. — Senior Database Consultant, MySQL & PostgreSQL DBA · Jul 2025 – present
- For POSTE ITALIANE: ~1,500 MySQL and PostgreSQL instances across production, certification and development; performance monitoring, query tuning, replication, capacity planning.

### IDEA DB CONSULTING S.R.L. — Sole Director · Technical Leader, databases & DWH · 2021 – Jun 2025
- **Generali Assicurazioni** (Feb 2024 – May 2025): Oracle DBA, performance tuning and DWH project lead on 500 GB–8 TB databases; direct client interface on requirements and scope.
- **Atradius**, Surety division ({{ATRADIUS_DATE}}): DWH architect and PM lead; unified Oracle DWH for 4 European countries, 60,000+ lines of PL/SQL, daily load under 2 hours.
- **FAI Service** (2021 – 2023): snowflake data model on Oracle Analytics Cloud, ETL on Oracle 19c in OCI.
- **Finwave** (2020 – 2022): advanced PL/SQL and query optimisation for financial applications with millions of daily transactions.
- **Banking, Telepass and other clients**: batches from 4 h to under 30 min; ETL/ELT from 15+ sources on 2B+ rows; PostgreSQL DWH as a cost-effective alternative to Oracle.

### NIMIS CONSULTING S.R.L. — Senior Oracle DBA & Performance Tuning Expert · 2020 – 2022
- For TIM / Huawei: 30+ critical Oracle databases (70+ instances) on 3- and 5-node Exadata clusters; 24/7 on-call; SLAs under 500 ms; ASM and TDE.

### Freelance consultant — Project Manager & Senior DWH Consultant · 2013 – 2020
- ~10 projects (€100K–€500K) in banking, telco and services; teams of 3–7 in distributed, multicultural settings; DWH pipelines handling 500M rows per load; Oracle Data Guard HA/DR.

### Earlier career · 1997 – 2013
- **Auselda AED Group** (2009 – 2013): DWH architect and Oracle project DBA for the Italian public sector.
- **Oracle Italia** (1999 – 2009): DWH architect, DBA and PL/SQL developer for TIM, Vodafone (Italy and Spain), Bank of Italy, Generali; Oracle trainer 2000 – 2001.
- **Etnoteam** (1999) and **S.EL.DAT.** (1997 – 1999): software development and junior Oracle DBA.

## Education & languages

- Computer Engineering studies (Software Engineering), Roma Tre University, 1994 – 2000 · Scientific high school diploma, 1993
- Italian (native) · English C1/C2 · Spanish C1 · Romanian C1 · French A2

<p class="gdpr">I authorise the processing of my personal data pursuant to Art. 13 of EU Regulation 2016/679 (GDPR). Rome, September 2026.</p>
```

### D.4 Generazione e verifica delle 2 pagine

```bash
cd ~/Development/APPLICAZIONI/My-Web-Site/ivanluminaria.com
SRC=docs/CV_Technical_Leader_Ivan_Luminaria_202609_EN.md
OUT=static/downloads/CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf
HTML="$TMPDIR/cv-technical-leader.html"

# pandoc 3.x: --embed-resources; se la versione è 2.x usa --self-contained
pandoc "$SRC" -s --embed-resources --css docs/cv-print/cv-print.css \
  --metadata pagetitle="Ivan Luminaria — Technical Leader CV" -o "$HTML"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/$OUT" "file://$HTML"

python3 - "$OUT" <<'EOF'
import re, sys
b = open(sys.argv[1], 'rb').read()
print("pagine:", len(re.findall(rb'/Type\s*/Page(?!s)', b)))
EOF
```

**Criterio**: esattamente **2 pagine**, con la seconda piena almeno a metà.

- Più di 2 pagine: abbassa `html { font-size }` di 0,2pt alla volta fino a 9pt; se non basta, riduci «Earlier career» a una sola riga e accorcia «Core expertise». Mai togliere i numeri di «Key results».
- Meno di 2 pagine piene: alza `font-size` fino a 10pt e i margini di `h2`.
- Apri il PDF (`open "$OUT"`) e controlla a vista: niente titoli orfani in fondo alla pagina 1, nessun carattere mancante (€, –, ·).

**Commit**: `feat(resumes): CV Technical Leader EN in 2 pagine (sorgente md, CSS di stampa, PDF)`

---

## 9. Passo E — Sezione `project-management` → «Leadership tecnica e progetti»

Slug, cartella e URL **invariati**. In ciascun `content/posts/project-management/_index.*.md`:

1. Sostituisci `title`, `seoTitle`, `description`.
2. Inserisci **all'inizio del corpo** (subito dopo il frontmatter) il paragrafo nuovo seguito da una riga `------------------------------------------------------------------------`. Il resto del corpo resta invariato.

| Lingua | `title` | `seoTitle` | `description` |
|---|---|---|---|
| it | `Leadership tecnica e progetti` | `Leadership tecnica e project management IT: casi reali` | `Leadership tecnica e project management IT: decisioni, team, metodo e consulenza, con storie vere e numeri da 30 anni di progetti in banche, telco e PA.` |
| en | `Technical Leadership & Projects` | `Technical leadership and IT project management: real cases` | `Technical leadership and IT project management: decisions, teams, method and consulting, with true stories and numbers from 30 years of projects.` |
| es | `Liderazgo técnico y proyectos` | `Liderazgo técnico y project management IT: casos reales` | `Liderazgo técnico y project management IT: decisiones, equipos, método y consultoría, con historias reales y números de 30 años de proyectos.` |
| ro | `Leadership tehnic și proiecte` | `Leadership tehnic și project management IT: cazuri reale` | `Leadership tehnic și project management IT: decizii, echipe, metodă și consultanță, cu povești reale și cifre din 30 de ani de proiecte.` |

Paragrafi di apertura:

- **it**: `Questa sezione racconta la parte del mestiere che non sta nei piani di esecuzione: le decisioni, i team, il metodo. È lo spazio della **leadership tecnica**, dove persone, sistemi e scelte devono funzionare insieme.`
- **en**: `This section covers the part of the job that does not live in execution plans: decisions, teams, method. It is the space of **technical leadership**, where people, systems and choices have to work together.`
- **es**: `Esta sección cuenta la parte del oficio que no está en los planes de ejecución: las decisiones, los equipos, el método. Es el espacio del **liderazgo técnico**, donde personas, sistemas y decisiones deben funcionar juntos.`
- **ro**: `Această secțiune povestește partea meseriei care nu se află în planurile de execuție: deciziile, echipele, metoda. Este spațiul **leadership-ului tehnic**, unde oamenii, sistemele și alegerile trebuie să funcționeze împreună.`

Il titolo della sezione compare anche nella home (`layouts/_partials/home/custom.html` usa `$section.Title`): nessuna modifica ai layout. Verifica nel passo 11 che le sigle «PM» nelle pulsantiere di `layouts/_default/list.html` restino accettabili; **non** modificarle senza chiedere.

**Commit**: `feat(posts): sezione project-management rinominata «Leadership tecnica e progetti» (slug invariato)`

---

## 10. Passo F — CTA di fine articolo

### F.1 `layouts/_partials/article-cta.html`

Nel `dict` `$sectionToProfile` cambia **solo**:

```
      "project-management" "project-manager" -}}
```

in:

```
      "project-management" "technical-leader" -}}
```

### F.2 `data/cta_copy.yaml` — nuovo profilo in fondo al file

```yaml
technical-leader:
  profile_slug: "technical-leader"
  dossier_file: "CV_Technical_Leader_Ivan_Luminaria_202609_EN.pdf"
  it:
    title: "Un sistema dati che rallenta, un incidente da spiegare al board, una scelta tecnica da difendere: prima della prossima decisione ti farebbe comodo chi legge la catena per intero."
    text_intro: "Trent'anni al fianco di team e decisori su database mission-critical — banking, telco, assicurativo, PA italiana e altri mercati."
    bridge: "Per conoscermi meglio,"
    link_profile: "vai al mio profilo Technical Leader"
    or_word: "oppure"
    link_dossier: "scarica il mio dossier in PDF"
  en:
    title: "A data system slowing down, an incident to explain to the board, a technical choice to defend: before the next decision, someone who reads the whole chain would come in handy."
    text_intro: "Thirty years alongside teams and decision-makers on mission-critical databases — banking, telco, insurance, Italian public sector and other markets."
    bridge: "To get to know me better,"
    link_profile: "visit my Technical Leader profile"
    or_word: "or"
    link_dossier: "download my dossier in PDF"
  es:
    title: "Un sistema de datos que se ralentiza, un incidente que explicar al consejo, una decisión técnica que defender: antes de la próxima decisión te vendría bien alguien que lea la cadena completa."
    text_intro: "Treinta años junto a equipos y responsables de decisión en bases de datos de misión crítica — banca, telco, seguros, administración pública italiana y otros mercados."
    bridge: "Para conocerme mejor,"
    link_profile: "ve a mi perfil Technical Leader"
    or_word: "o"
    link_dossier: "descarga mi dosier en PDF"
  ro:
    title: "Un sistem de date care încetinește, un incident de explicat în consiliul de administrație, o alegere tehnică de susținut: înainte de următoarea decizie ți-ar prinde bine cineva care citește tot lanțul."
    text_intro: "Treizeci de ani alături de echipe și decidenți pe baze de date critice — banking, telco, asigurări, administrația publică italiană și alte piețe."
    bridge: "Pentru a mă cunoaște mai bine,"
    link_profile: "vezi profilul meu Technical Leader"
    or_word: "sau"
    link_dossier: "descarcă dosarul meu în PDF"
```

Aggiorna anche il commento in testa al file: «copy editoriale per i **5** profili professionali».

**Commit**: `feat(cta): la sezione Leadership tecnica e progetti rimanda al profilo Technical Leader`

---

## 11. Passo G — Description del sito e headline autore

### G.1 `config/_default/languages.*.toml` → `[params] description`

| Lingua | Nuova `description` (≤160) |
|---|---|
| it | `Ivan Luminaria, Technical Leader per database mission-critical Oracle, PostgreSQL e MySQL. Blog Database Strategy con casi reali da 30 anni di IT.` |
| en | `Ivan Luminaria, Technical Leader for mission-critical Oracle, PostgreSQL and MySQL databases. Database Strategy blog with real cases from 30 years of IT.` |
| es | `Ivan Luminaria, Technical Leader de bases de datos críticas Oracle, PostgreSQL y MySQL. Blog Database Strategy con casos reales de 30 años de IT.` |
| ro | `Ivan Luminaria, Technical Leader pentru baze de date critice Oracle, PostgreSQL și MySQL. Blog Database Strategy cu cazuri reale din 30 de ani de IT.` |

### G.2 `config/_default/params.toml` → `[author] headline`

Oggi: `headline = "Oracle DBA & DWH Architect"`. Prima di cambiarla, esegui `grep -rn "author.headline\|Author.headline\|\.headline" layouts themes/congo/layouts | head` per vedere dove compare.

- Se è visibile in pagina: `headline = "Technical Leader · Database mission-critical"`.
- Se viene usata anche in JSON-LD o meta: stessa stringa (è un campo non localizzato).

**Commit**: `chore(seo): description del sito e headline autore allineate al ruolo di Technical Leader`

---

## 12. Verifiche finali (prima del push)

### 12.1 Lunghezze SEO

```bash
python3 - <<'EOF'
import re, glob
files = (glob.glob("content/resumes/_index.*.md")
         + glob.glob("content/resumes/technical-leader/index.*.md")
         + glob.glob("content/posts/project-management/_index.*.md"))
for f in sorted(files):
    t = open(f, encoding="utf-8").read()
    for key, lim in (("seoTitle", 65), ("description", 160)):
        m = re.search(rf'^{key}:\s*"(.*)"\s*$', t, re.M)
        if m:
            n = len(m.group(1))
            print(("OK " if n <= lim else "KO ") + f"{f} {key}={n}/{lim}")
for f in sorted(glob.glob("config/_default/languages.*.toml")):
    m = re.search(r'description\s*=\s*"(.*)"', open(f, encoding="utf-8").read())
    n = len(m.group(1)); print(("OK " if n <= 160 else "KO ") + f"{f} description={n}/160")
EOF
```

Correggi ogni `KO` accorciando il testo, senza cambiarne il senso.

### 12.2 Lessico

```bash
grep -n -i -E "posso essere sincer|sinceramente|onestamente|francamente|a dire il vero|\bproblema\b|\bperò\b|\bmagari\b|\bforse\b" \
  content/resumes/_index.it.md content/resumes/technical-leader/index.it.md \
  content/posts/project-management/_index.it.md data/cta_copy.yaml i18n/it.yaml
```

Le occorrenze nei testi **preesistenti** non toccati da questo prompt restano: segnalale a Ivan senza correggerle.

### 12.3 Build e anteprima

```bash
hugo --gc --minify --printPathWarnings 2>&1 | tail -20      # nessun ERROR, nessun WARN nuovo
hserve                                                      # alias di anteprima (draft visibili)
```

Controlla nel browser, in **chiaro e scuro**, a **1440px, 1024px e 390px**:

- [ ] Brand-bar: nome, ruolo e frase allineati; a 390px il burger resta visibile e cliccabile, frase nascosta, ruolo con ellissi.
- [ ] `/it/resumes/`: scheda Technical Leader in evidenza con etichetta «Il mio ruolo oggi», contatore «1 ruolo · 4 pilastri», titolo «I quattro pilastri», 4 schede invariate.
- [ ] Pulsante «Leggi la roadmap» → `/it/resumes/technical-leader/`; «Scarica PDF» → il PDF di 2 pagine (HTTP 200).
- [ ] `/en/`, `/es/`, `/ro/` delle stesse pagine.
- [ ] Home: la sezione si chiama «Leadership tecnica e progetti» (e traduzioni); gli URL `/*/posts/project-management/` funzionano.
- [ ] Un articolo della sezione (es. `/it/posts/project-management/4-milioni-nessun-software/`): la CTA finale rimanda al profilo Technical Leader.
- [ ] Un articolo Oracle: la CTA rimanda ancora al profilo DBA.

---

## 13. Push e consegna a Ivan

```bash
git push origin work-in-progress
```

Poi fornisci a Ivan, secondo la sezione «Workflow git» del `CLAUDE.md` del repo:

1. l'elenco dei commit fatti e delle verifiche superate (con eventuali `KO` corretti);
2. i punti che richiedono il suo occhio (resa della brand-bar tra 768 e 1190px, headline autore);
3. **solo se Ivan lo chiede**, i comandi di merge su `main`:

```bash
git checkout main
git pull origin main
git merge work-in-progress -m "Merge work-in-progress: Technical Leader come identità principale (brand-bar, Know-How, profilo e CV EN, sezione Leadership tecnica e progetti, CTA)"
git push origin main
git checkout work-in-progress
```

Il push su `main` avvia il deploy su GitHub Pages: **non eseguirlo in autonomia**.

---

## 14. Fuori scope (non farlo in questa sessione)

- Riallineare i 4 CV esistenti (marzo 2026) alla cronologia di settembre 2026.
- Pubblicare l'articolo «Il dottore tutto pazzo» (storia in `personal-branding-idb/08-storie/01-dottore-tutto-pazzo_V3.md`): ha un suo workflow editoriale in 4 lingue.
- Rinominare slug o cartelle di sezione, creare nuove sezioni, modificare le slice di sezioni nei layout.
- Pagina servizi, prezzi, form di contatto.
