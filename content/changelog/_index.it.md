---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Storico delle release del sito ivanluminaria.com — milestone editoriali e cambiamenti strutturali marcati con schema CalVer."
draft: false
layout: "simple"
---

Questo sito segue uno schema di versionamento **CalVer** (`v<YYYY>.<MM>.<micro>`) per marcare le milestone editoriali. Non tagghiamo ogni singolo articolo pubblicato — solo i cambiamenti strutturali dei profili, del workflow o del sito stesso.

---

## v2026.09.001 — 20 settembre 2026

**5 CV pilastri con voci forti + versionamento CalVer adottato**

Rilascio di stabilizzazione dei profili di ruolo. I cinque profili — [Technical Leader](/it/resumes/technical-leader/), [Project Manager](/it/resumes/project-manager/), [DWH Architect](/it/resumes/dwh-architect/), [Oracle DBA](/it/resumes/oracle-dba/), [Oracle PL/SQL](/it/resumes/oracle-plsql/) — hanno ora un Professional Profile atemporale con voce forte differenziata per archetipo. Ognuno smonta credenze specifiche del lettore e chiude su un valore operativo concreto, non su formule generiche.

Cambiamenti principali:

- Recupero della voce forte narrativa in ogni CV, sostituendo i paragrafi neutri "da job description" con posizionamenti calibrati sull'archetipo dominante
- Rimossi i riferimenti puntuali dal Profile — restano nella sezione Experience dove è appropriato citarli con contesto temporale
- Nuova pagina Technical Leader come master dei quattro pilastri specialistici
- Adottato versionamento CalVer per marcare le milestone editoriali del sito

Sotto il cofano: aggiornati i CV Markdown sorgente in `docs/` da cui vengono generati i PDF; pipeline PDF con `pandoc` + `WeasyPrint` per rigenerare i CV in inglese a partire dai Markdown.

---

## v2026.08.001 — 31 agosto 2026

**Rigenerazione massiva delle cover images con AI**

Riallineamento grafico coerente al brand editoriale: rigenerate con AI le cover images di circa trenta articoli storici del blog. Nessuna modifica sostanziale ai contenuti — solo copertine più coese come palette visiva.

---

## v2026.07.001 — 31 luglio 2026

**Prosecuzione della cadenza editoriale + sync shell cross-Mac**

Prosecuzione della pubblicazione settimanale del martedì con nuovi contenuti tecnici pubblicati sul blog. Sotto il cofano: risync di `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 giugno 2026

**Refactor completo dei 4 CV specialistici + Bonjour LAN + PDF v2026-06**

Refactor completo dei quattro CV specialistici (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 lingue) con riscrittura strutturale delle sezioni di esperienza storica. Pubblicati quattro PDF v2026-06 in `static/downloads/` sia in versione standard sia in versione Randstad.

Nuovo accesso LAN via Bonjour: il sito diventa raggiungibile da telefono, iPad e altri device della rete domestica via `ivanluminaria.local` e `ilum.local` — utile per l'anteprima mobile in tempo reale.

Aggiunta anche una regola editoriale: citazioni in lingua originale + traduzione affiancata per i testi tecnici storici.

---

## v2026.05.001 — 31 maggio 2026

**Integrazione MCP Buffer + shell RCCS2025 + CTA articoli**

Sul fronte automazione: integrato il server MCP Buffer per lo scheduling automatico dei post LinkedIn direttamente dalla shell — il flusso editoriale settimanale ora è più snello. Refactor dello shell environment allo standard RCCS2025 (`wwwhelp`/`wwwgo` parametrici).

CTA di fine articolo differenziate per i quattro profili × quattro lingue. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` sulle thin tag pages.

Prosecuzione della pubblicazione settimanale del martedì con nuovi contenuti tecnici.

---

## v2026.04.001 — 30 aprile 2026

**Cadenza editoriale consolidata + redesign /tags/ + CI cron paracadute**

Consolidamento della cadenza editoriale settimanale del martedì: aggiunto un terzo cron GitHub Actions come paracadute finale, per proteggere la pubblicazione dai ritardi occasionali dell'infrastruttura.

Redesign della pagina `/tags/` con classificazione multi-sezione. Mobile search: implementato bottom sheet.

---

## v2026.03.001 — 31 marzo 2026

**Bootstrap del sito + setup workflow editoriale**

Prima release ricostruita retroattivamente. Bootstrap del sito Hugo con deploy automatico su GitHub Pages.

Il materiale che alimenta il blog viene da un archivio personale costruito in quasi trent'anni di lavoro nell'informatica — appunti tecnici, memorie di progetto, note prese progetto dopo progetto, incident dopo incident. La rielaborazione di quel patrimonio ha prodotto i primi articoli del blog Database Strategy, pubblicati in quattro lingue.

Setup del workflow editoriale: proposta di 3 titoli per ogni articolo, tabella idee con status, glossario a 5 termini, `hreflang` multilingua, breadcrumbs `JSON-LD`, OpenGraph tags. Pagina Chi Sono con etichette LinkedIn/Email in quattro lingue.
