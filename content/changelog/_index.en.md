---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Release history for ivanluminaria.com — editorial milestones and structural changes marked with a CalVer scheme."
draft: false
layout: "simple"
---

This site follows a **CalVer** versioning scheme (`v<YYYY>.<MM>.<micro>`) to mark editorial milestones. We don't tag every single article published — only structural changes to profiles, workflow, or the site itself.

---

## v2026.09.001 — 20 September 2026

**Five pillar CVs with a strong narrative voice + CalVer versioning adopted**

Stabilisation release for the role profiles. The five profiles — [Technical Leader](/en/resumes/technical-leader/), [Project Manager](/en/resumes/project-manager/), [DWH Architect](/en/resumes/dwh-architect/), [Oracle DBA](/en/resumes/oracle-dba/), [Oracle PL/SQL](/en/resumes/oracle-plsql/) — now carry a timeless Professional Profile with a strong narrative voice differentiated by archetype. Each one addresses specific reader beliefs and closes on concrete operational value rather than generic formulas.

Main changes:

- Restoration of the strong narrative voice in each CV, replacing neutral "job description" paragraphs with positionings calibrated on the dominant archetype
- Specific references removed from the Profile — they remain in the Experience section where they can be cited with proper temporal context
- New Technical Leader page as master of the four specialist pillars
- Adopted CalVer versioning to mark the site's editorial milestones

Under the hood: updated source CV Markdowns in `docs/` from which the PDFs are generated; PDF pipeline using `pandoc` + `WeasyPrint` to regenerate the English CVs from the Markdown sources.

---

## v2026.08.001 — 31 August 2026

**Massive AI regeneration of cover images**

Graphic realignment coherent to the editorial brand: about thirty historical blog articles received AI-regenerated cover images. No substantive changes to contents — just more coherent covers as a visual palette.

---

## v2026.07.001 — 31 July 2026

**Editorial cadence continued + shell sync cross-Mac**

Continued weekly Tuesday publication cadence with new technical contents on the blog. Under the hood: re-sync of `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 June 2026

**Full refactor of the 4 specialist CVs + Bonjour LAN + PDF v2026-06**

Full refactor of the four specialist CVs (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 languages) with structural rewriting of the historical experience sections. Four v2026-06 PDFs published in `static/downloads/` in both standard and Randstad variants.

New LAN access via Bonjour: the site becomes reachable from phone, iPad, and other home-network devices via `ivanluminaria.local` and `ilum.local` — useful for real-time mobile preview.

An editorial rule was also added: original-language quotations + parallel translation for historical technical texts.

---

## v2026.05.001 — 31 May 2026

**Buffer MCP integration + RCCS2025 shell + article CTAs**

On the automation side: integrated the Buffer MCP server for automatic scheduling of LinkedIn posts directly from the shell — the weekly editorial workflow is now leaner. Refactor of the shell environment to the RCCS2025 standard (`wwwhelp`/`wwwgo` parametric).

End-of-article CTAs differentiated for the four profiles × four languages. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` on thin tag pages.

Continued weekly Tuesday publication cadence with new technical contents.

---

## v2026.04.001 — 30 April 2026

**Editorial cadence consolidated + /tags/ redesign + CI cron safety net**

Consolidation of the weekly Tuesday editorial cadence: added a third GitHub Actions cron as a final safety net, to protect publication from occasional infrastructure delays.

Redesign of the `/tags/` page with multi-section classification. Mobile search: bottom sheet implemented.

---

## v2026.03.001 — 31 March 2026

**Site bootstrap + editorial workflow setup**

First release reconstructed retroactively. Bootstrap of the Hugo site with automatic deploy to GitHub Pages. First technical contents of the Database Strategy blog published in four languages.

Editorial workflow setup: 3-title proposal for each article, ideas table with status, 5-term glossary, multilingual `hreflang`, `JSON-LD` breadcrumbs, OpenGraph tags. About Me page with LinkedIn/Email labels in four languages.
