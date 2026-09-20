---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Istoricul release-urilor pentru ivanluminaria.com — repere editoriale și schimbări structurale marcate cu schemă CalVer."
draft: false
layout: "simple"
---

Acest site urmează o schemă de versionare **CalVer** (`v<YYYY>.<MM>.<micro>`) pentru a marca reperele editoriale. Nu etichetăm fiecare articol publicat — doar schimbările structurale ale profilurilor, ale workflow-ului sau ale site-ului însuși.

---

## v2026.09.001 — 20 septembrie 2026

**Cinci CV-uri piloni cu voce narativă puternică + versionare CalVer adoptată**

Release de stabilizare a profilurilor de rol. Cele cinci profiluri — [Technical Leader](/ro/resumes/technical-leader/), [Project Manager](/ro/resumes/project-manager/), [DWH Architect](/ro/resumes/dwh-architect/), [Oracle DBA](/ro/resumes/oracle-dba/), [Oracle PL/SQL](/ro/resumes/oracle-plsql/) — au acum un Professional Profile atemporal cu voce narativă puternică diferențiată pe arhetip. Fiecare abordează credințe specifice ale cititorului și se închide cu o valoare operativă concretă în loc de formule generice.

Schimbări principale:

- Recuperarea vocii narative puternice în fiecare CV, înlocuind paragrafele neutre "de job description" cu poziționări calibrate pe arhetipul dominant
- Eliminate referințele specifice din Profile — rămân în secțiunea Experience unde este potrivit să fie citate cu context temporal
- Nouă pagină Technical Leader ca master al celor patru piloni specializați
- Adoptată versionarea CalVer pentru a marca reperele editoriale ale site-ului

Sub capotă: actualizate CV-urile Markdown sursă în `docs/` din care sunt generate PDF-urile; pipeline PDF cu `pandoc` + `WeasyPrint` pentru a regenera CV-urile în engleză din Markdown.

---

## v2026.08.001 — 31 august 2026

**Regenerare masivă a cover images cu AI**

Realiniere grafică coerentă cu brand-ul editorial: circa treizeci de articole istorice ale blogului au primit cover images regenerate cu AI. Nicio modificare substanțială asupra conținutului — doar coperți mai coerente ca paletă vizuală.

---

## v2026.07.001 — 31 iulie 2026

**Cadență editorială continuată + sync shell cross-Mac**

Continuarea publicării săptămânale de marți cu conținut tehnic nou pe blog. Sub capotă: resync `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 iunie 2026

**Refactor complet al celor 4 CV specialiste + Bonjour LAN + PDF v2026-06**

Refactor complet al celor patru CV specialiste (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 limbi) cu rescriere structurală a secțiunilor de experiență istorică. Publicate patru PDF v2026-06 în `static/downloads/` atât în versiune standard cât și în versiune Randstad.

Acces nou LAN via Bonjour: site-ul devine accesibil de pe telefon, iPad și alte device-uri ale rețelei domestice via `ivanluminaria.local` și `ilum.local` — util pentru previzualizarea mobilă în timp real.

Adăugată și o regulă editorială: citate în limba originală + traducere alăturată pentru textele tehnice istorice.

---

## v2026.05.001 — 31 mai 2026

**Integrare MCP Buffer + shell RCCS2025 + CTA articole**

Pe frontul automatizării: integrat serverul MCP Buffer pentru scheduling automat al post-urilor LinkedIn direct din shell — flow-ul editorial săptămânal este acum mai fluid. Refactor al shell environment-ului la standardul RCCS2025 (`wwwhelp`/`wwwgo` parametrice).

CTA de sfârșit de articol diferențiate pentru cele patru profiluri × patru limbi. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` pe thin tag pages.

Continuarea publicării săptămânale de marți cu conținut tehnic nou.

---

## v2026.04.001 — 30 aprilie 2026

**Cadență editorială consolidată + redesign /tags/ + CI cron safety net**

Consolidarea cadenței editoriale săptămânale de marți: adăugat un al treilea cron GitHub Actions ca safety net final, pentru a proteja publicarea de întârzierile ocazionale ale infrastructurii.

Redesign al paginii `/tags/` cu clasificare multi-secțiune. Mobile search: bottom sheet implementat.

---

## v2026.03.001 — 31 martie 2026

**Bootstrap-ul site-ului + setup-ul workflow-ului editorial**

Primul release reconstruit retroactiv. Bootstrap al site-ului Hugo cu deploy automat pe GitHub Pages. Publicate primele conținuturi tehnice ale blogului Database Strategy în patru limbi.

Setup al workflow-ului editorial: propunere de 3 titluri per articol, tabel idei cu status, glosar de 5 termeni, `hreflang` multilingv, breadcrumbs `JSON-LD`, OpenGraph tags. Pagină Despre cu etichete LinkedIn/Email în patru limbi.
