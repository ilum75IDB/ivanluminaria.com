---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Istoricul release-urilor pentru ivanluminaria.com — repere editoriale și schimbări structurale marcate cu schemă CalVer."
draft: false
layout: "simple"
---

Acest site urmează o schemă de versionare **CalVer** (`v<YYYY>.<MM>.<micro>`) pentru a marca reperele editoriale. Nu etichetăm fiecare articol publicat — doar schimbările structurale ale poziționării, ale rolurilor sau ale site-ului însuși.

---

## v2026.09.001 — 20 septembrie 2026

**Cinci CV-uri piloni cu voce narativă puternică + poziționare IDEA DB stabilizată**

Release de stabilizare. Cele cinci profiluri de rol — [Technical Leader](/ro/resumes/technical-leader/), [Project Manager](/ro/resumes/project-manager/), [DWH Architect](/ro/resumes/dwh-architect/), [Oracle DBA](/ro/resumes/oracle-dba/), [Oracle PL/SQL](/ro/resumes/oracle-plsql/) — au acum un Professional Profile atemporal cu voce narativă puternică diferențiată pe arhetip. Fiecare abordează credințe specifice ale buyer-ului și se închide cu o valoare operativă concretă în loc de formule generice.

Schimbări principale:

- Recuperarea vocii narative puternice în fiecare CV, înlocuind paragrafele neutre "de job description" cu poziționări calibrate pe arhetipul dominant
- Eliminarea mențiunilor specifice de clienți din Profile — numele companiilor rămân în secțiunea Experience unde este potrivit să fie citate cu context temporal
- Nouă pagină Technical Leader ca master al celor patru piloni specializați
- Adoptată versionarea CalVer pentru a marca reperele editoriale ale site-ului

Sub capotă: actualizate CV-urile Markdown sursă în `docs/` din care sunt generate PDF-urile; pipeline PDF cu `pandoc` + `WeasyPrint` pentru a regenera CV-urile în engleză din Markdown.

---

## v2026.08.001 — 31 august 2026

**Regenerare masivă a cover images cu AI**

Realiniere grafică coerentă cu brand-ul editorial: regenerate cu AI cover images pentru circa treizeci de articole istorice ale blogului (Data Warehouse, Oracle DBA, PostgreSQL, MySQL, Project Management, DWH Architect, AI Manager). Nicio modificare substanțială asupra conținutului articolelor — doar coperți mai coerente ca paletă vizuală.

---

## v2026.07.001 — 31 iulie 2026

**Articole Data Governance + Swap InnoDB Cluster + Assertions Oracle 26ai**

Trei articole noi publicate pe blog:

- Data Governance: pauza de prânz care a amânat go-live-ul (21 iulie)
- Swap la 100% pe InnoDB Cluster: când `join_buffer_size` multiplică (28 iulie)
- Assertions în Oracle 26ai: în sfârșit o restricție care traversează (4 august)

Sub capotă: resync `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 iunie 2026

**Refactor complet al celor 4 CV la pattern-ul Borzacchiello + Bonjour LAN + PDF v2026-06**

Refactor complet al celor patru CV specialiste (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 limbi) la pattern-ul Borzacchiello. Rescrise experiențele istorice (S.EL.DAT., Oracle Italia, Auselda AED Group, Libero Professionista) și publicate patru PDF v2026-06 în `static/downloads/` atât în versiune standard cât și în versiune Randstad.

Acces nou LAN via Bonjour: site-ul devine accesibil de pe telefon, iPad și alte device-uri ale rețelei domestice via `ivanluminaria.local` și `ilum.local` — util pentru previzualizarea mobilă în timp real.

Adăugată și o regulă editorială: manifestul Agile cu citație originală în engleză + traducere alăturată.

---

## v2026.05.001 — 31 mai 2026

**Articole UML/RUP + enum Oracle + Buffer MCP + shell RCCS2025**

Două articole noi publicate pe blog: *de la rivali la co-autori* (cum au unificat Booch, Rumbaugh și Jacobson UML/RUP) și *enum Oracle 19c-26ai + domenii* în patru limbi.

Pe frontul automatizării: integrat serverul MCP Buffer pentru scheduling automat al post-urilor LinkedIn direct din shell — flow-ul editorial săptămânal este acum mai fluid. Refactor al shell environment-ului la standardul RCCS2025 (`wwwhelp`/`wwwgo` parametrice).

CTA de sfârșit de articol diferențiate pentru cele patru profiluri × patru limbi. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` pe thin tag pages.

---

## v2026.04.001 — 30 aprilie 2026

**Cadență editorială consolidată + redesign /tags/ + CI cron safety net**

Articol *PostgreSQL indici când dor* în patru limbi. Consolidarea cadenței editoriale săptămânale de marți: adăugat un al treilea cron GitHub Actions ca safety net final, pentru a proteja publicarea de întârzierile ocazionale ale infrastructurii.

Redesign al paginii `/tags/` cu clasificare multi-secțiune (fix #84). Mobile search: bottom sheet implementat.

---

## v2026.03.001 — 31 martie 2026

**Bootstrap-ul site-ului + primele articole + setup-ul workflow-ului editorial**

Primul release reconstruit retroactiv. Bootstrap al site-ului Hugo cu deploy automat pe GitHub Pages. Primul articol Database Strategy publicat (art. #69: MySQL Group Replication binlog migration) în patru limbi.

Setup al workflow-ului editorial: propunere de 3 titluri per articol, tabel idei cu status, glosar de 5 termeni, `hreflang` multilingv, breadcrumbs `JSON-LD`, OpenGraph tags. Pagină Despre cu etichete LinkedIn/Email în patru limbi.
