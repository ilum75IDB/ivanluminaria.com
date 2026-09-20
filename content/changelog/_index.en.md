---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Release history for ivanluminaria.com — editorial milestones and structural changes marked with a CalVer scheme."
draft: false
layout: "simple"
---

This site follows a **CalVer** versioning scheme (`v<YYYY>.<MM>.<micro>`) to mark editorial milestones. We don't tag every single article published — only structural changes to positioning, roles, or the site itself.

---

## v2026.09.001 — 20 September 2026

**Five pillar CVs with a strong narrative voice + IDEA DB positioning stabilised**

Stabilisation release. The five role profiles — [Technical Leader](/en/resumes/technical-leader/), [Project Manager](/en/resumes/project-manager/), [DWH Architect](/en/resumes/dwh-architect/), [Oracle DBA](/en/resumes/oracle-dba/), [Oracle PL/SQL](/en/resumes/oracle-plsql/) — now carry a timeless Professional Profile with a strong narrative voice differentiated by archetype. Each one addresses specific buyer beliefs and closes on concrete operational value rather than generic formulas.

Main changes:

- Restoration of the strong narrative voice in each CV, replacing neutral "job description" paragraphs with positionings calibrated on the dominant archetype
- Removal of specific client mentions from the Profile — company names remain in the Experience section where they can be cited with proper temporal context
- New Technical Leader page as master of the four specialist pillars
- Adopted CalVer versioning to mark the site's editorial milestones

Under the hood: updated source CV Markdowns in `docs/` from which the PDFs are generated; PDF pipeline using `pandoc` + `WeasyPrint` to regenerate the English CVs from the Markdown sources.

---

## v2026.08.001 — 31 August 2026

**Massive AI regeneration of cover images**

Graphic realignment coherent to the editorial brand: about thirty historical blog articles (Data Warehouse, Oracle DBA, PostgreSQL, MySQL, Project Management, DWH Architect, AI Manager) received AI-regenerated cover images. No substantive changes to article contents — just more coherent covers as a visual palette.

---

## v2026.07.001 — 31 July 2026

**Articles: Data Governance + Swap on InnoDB Cluster + Assertions in Oracle 26ai**

Three new articles published on the blog:

- Data Governance: the lunch break that delayed the go-live (21 July)
- Swap at 100% on InnoDB Cluster: when `join_buffer_size` multiplies (28 July)
- Assertions in Oracle 26ai: finally a constraint that spans (4 August)

Under the hood: re-sync of `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 June 2026

**Full refactor of the 4 CVs to the Borzacchiello pattern + Bonjour LAN + PDF v2026-06**

Full refactor of the four specialist CVs (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 languages) to the Borzacchiello pattern. Historical experiences rewritten (S.EL.DAT., Oracle Italy, Auselda AED Group, Freelance Consultant) and four v2026-06 PDFs published in `static/downloads/` in both standard and Randstad variants.

New LAN access via Bonjour: the site becomes reachable from phone, iPad, and other home-network devices via `ivanluminaria.local` and `ilum.local` — useful for real-time mobile preview.

An editorial rule was also added: Agile manifesto quoted in the original English + parallel translation.

---

## v2026.05.001 — 31 May 2026

**Articles UML/RUP + Oracle enum + Buffer MCP + RCCS2025 shell**

Two new articles published on the blog: *from rivals to co-authors* (how Booch, Rumbaugh and Jacobson unified UML/RUP) and *Oracle enum 19c-26ai + domains* in four languages.

On the automation side: integrated the Buffer MCP server for automatic scheduling of LinkedIn posts directly from the shell — the weekly editorial workflow is now leaner. Refactor of the shell environment to the RCCS2025 standard (`wwwhelp`/`wwwgo` parametric).

End-of-article CTAs differentiated for the four profiles × four languages. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` on thin tag pages.

---

## v2026.04.001 — 30 April 2026

**Editorial cadence consolidated + /tags/ redesign + CI cron safety net**

Article *PostgreSQL indexes when they hurt* in four languages. Consolidation of the weekly Tuesday editorial cadence: added a third GitHub Actions cron as a final safety net, to protect publication from occasional infrastructure delays.

Redesign of the `/tags/` page with multi-section classification (fix #84). Mobile search: bottom sheet implemented.

---

## v2026.03.001 — 31 March 2026

**Site bootstrap + first articles + editorial workflow setup**

First release reconstructed retroactively. Bootstrap of the Hugo site with automatic deploy to GitHub Pages. First Database Strategy article published (art. #69: MySQL Group Replication binlog migration) in four languages.

Editorial workflow setup: 3-title proposal for each article, ideas table with status, 5-term glossary, multilingual `hreflang`, `JSON-LD` breadcrumbs, OpenGraph tags. About Me page with LinkedIn/Email labels in four languages.
