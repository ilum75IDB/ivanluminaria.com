---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Storico delle release del sito ivanluminaria.com — milestone editoriali e cambiamenti strutturali marcati con schema CalVer."
draft: false
layout: "simple"
---

Questo sito segue uno schema di versionamento **CalVer** (`v<YYYY>.<MM>.<micro>`) per marcare le milestone editoriali. Non tagghiamo ogni singolo articolo pubblicato — solo i cambiamenti strutturali del posizionamento, dei ruoli o del sito stesso.

---

## v2026.09.001 — 20 settembre 2026

**5 CV pilastri con voci forti + posizionamento IDEA DB stabilizzato**

Rilascio di stabilizzazione. I cinque profili di ruolo — [Technical Leader](/it/resumes/technical-leader/), [Project Manager](/it/resumes/project-manager/), [DWH Architect](/it/resumes/dwh-architect/), [Oracle DBA](/it/resumes/oracle-dba/), [Oracle PL/SQL](/it/resumes/oracle-plsql/) — hanno ora un Professional Profile atemporale con voce forte differenziata per archetipo. Ognuno smonta credenze specifiche del buyer avatar e chiude su un valore operativo concreto, non su formule generiche.

Cambiamenti principali:

- Recupero della voce forte narrativa in ogni CV, sostituendo i paragrafi neutri "da job description" con posizionamenti calibrati sull'archetipo dominante
- Rimozione dei clienti-flag specifici dal Profile — i nomi delle aziende restano nella sezione Experience dove è appropriato citarli con contesto temporale
- Nuova pagina Technical Leader come master dei quattro pilastri specialistici
- Adottato versionamento CalVer per marcare le milestone editoriali del sito

Sotto il cofano: aggiornati i CV Markdown sorgente in `docs/` da cui vengono generati i PDF; pipeline PDF con `pandoc` + `WeasyPrint` per rigenerare i CV in inglese a partire dai Markdown.

---

## v2026.08.001 — 31 agosto 2026

**Rigenerazione massiva delle cover images con AI**

Riallineamento grafico coerente al brand editoriale: rigenerate con AI le cover images di circa trenta articoli storici del blog (Data Warehouse, Oracle DBA, PostgreSQL, MySQL, Project Management, DWH Architect, AI Manager). Nessuna modifica sostanziale ai contenuti degli articoli — solo copertine più coese come palette visiva.

---

## v2026.07.001 — 31 luglio 2026

**Articoli Data Governance + Swap InnoDB Cluster + Assertions Oracle 26ai**

Tre nuovi articoli pubblicati sul blog:

- Data Governance: la pausa pranzo che ha rimandato il go-live (21 luglio)
- Swap al 100% su InnoDB Cluster: quando `join_buffer_size` moltiplica (28 luglio)
- Assertions in Oracle 26ai: finalmente un vincolo che attraversa (4 agosto)

Sotto il cofano: risync di `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 giugno 2026

**Refactor completo dei 4 CV al pattern Borzacchiello + Bonjour LAN + PDF v2026-06**

Refactor completo dei quattro CV specialistici (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 lingue) al pattern Borzacchiello. Riscritte le esperienze storiche (S.EL.DAT., Oracle Italia, Auselda AED Group, Libero Professionista) e pubblicati quattro PDF v2026-06 in `static/downloads/` sia in versione standard sia in versione Randstad.

Nuovo accesso LAN via Bonjour: il sito diventa raggiungibile da telefono, iPad e altri device della rete domestica via `ivanluminaria.local` e `ilum.local` — utile per l'anteprima mobile in tempo reale.

Aggiunta anche una regola editoriale: manifesto Agile con citazione originale in inglese + traduzione affiancata.

---

## v2026.05.001 — 31 maggio 2026

**Articoli UML/RUP + enum Oracle + Buffer MCP + shell RCCS2025**

Due nuovi articoli pubblicati sul blog: *da rivali a co-autori* (come Booch, Rumbaugh e Jacobson hanno unificato UML/RUP) e *enum Oracle 19c-26ai + domini* in quattro lingue.

Sul fronte automazione: integrato il server MCP Buffer per lo scheduling automatico dei post LinkedIn direttamente dalla shell — il flusso editoriale settimanale ora è più snello. Refactor dello shell environment allo standard RCCS2025 (`wwwhelp`/`wwwgo` parametrici).

CTA di fine articolo differenziate per i quattro profili × quattro lingue. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` sulle thin tag pages.

---

## v2026.04.001 — 30 aprile 2026

**Cadenza editoriale consolidata + redesign /tags/ + CI cron paracadute**

Articolo *PostgreSQL indici quando fanno male* in quattro lingue. Consolidamento della cadenza editoriale settimanale del martedì: aggiunto un terzo cron GitHub Actions come paracadute finale, per proteggere la pubblicazione dai ritardi occasionali dell'infrastruttura.

Redesign della pagina `/tags/` con classificazione multi-sezione (fix #84). Mobile search: implementato bottom sheet.

---

## v2026.03.001 — 31 marzo 2026

**Bootstrap del sito + primi articoli + setup workflow editoriale**

Prima release ricostruita retroattivamente. Bootstrap del sito Hugo con deploy automatico su GitHub Pages. Primo articolo Database Strategy pubblicato (art. #69: MySQL Group Replication binlog migration) in quattro lingue.

Setup del workflow editoriale: proposta di 3 titoli per ogni articolo, tabella idee con status, glossario a 5 termini, `hreflang` multilingua, breadcrumbs `JSON-LD`, OpenGraph tags. Pagina Chi Sono con etichette LinkedIn/Email in quattro lingue.
