---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Histórico de releases de ivanluminaria.com — hitos editoriales y cambios estructurales marcados con esquema CalVer."
draft: false
layout: "simple"
---

Este sitio sigue un esquema de versionado **CalVer** (`v<YYYY>.<MM>.<micro>`) para marcar los hitos editoriales. No etiquetamos cada artículo publicado — solo los cambios estructurales al posicionamiento, a los roles o al sitio en sí.

---

## v2026.09.001 — 20 de septiembre de 2026

**Cinco CV pilares con voz narrativa fuerte + posicionamiento IDEA DB estabilizado**

Release de estabilización. Los cinco perfiles de rol — [Technical Leader](/es/resumes/technical-leader/), [Project Manager](/es/resumes/project-manager/), [DWH Architect](/es/resumes/dwh-architect/), [Oracle DBA](/es/resumes/oracle-dba/), [Oracle PL/SQL](/es/resumes/oracle-plsql/) — cuentan ahora con un Professional Profile atemporal con voz narrativa fuerte diferenciada por arquetipo. Cada uno enfrenta creencias específicas del buyer y cierra con un valor operativo concreto en lugar de fórmulas genéricas.

Cambios principales:

- Recuperación de la voz narrativa fuerte en cada CV, sustituyendo los párrafos neutros "de job description" con posicionamientos calibrados sobre el arquetipo dominante
- Eliminación de las menciones específicas de clientes del Profile — los nombres de las empresas permanecen en la sección Experience, donde es apropiado citarlos con contexto temporal
- Nueva página Technical Leader como master de los cuatro pilares especialistas
- Adoptado versionado CalVer para marcar los hitos editoriales del sitio

Bajo el capó: actualizados los CV Markdown fuente en `docs/` desde los que se generan los PDF; pipeline PDF con `pandoc` + `WeasyPrint` para regenerar los CV en inglés desde los Markdown.

---

## v2026.08.001 — 31 de agosto de 2026

**Regeneración masiva de las cover images con AI**

Realineación gráfica coherente al brand editorial: regeneradas con AI las cover images de unos treinta artículos históricos del blog (Data Warehouse, Oracle DBA, PostgreSQL, MySQL, Project Management, DWH Architect, AI Manager). Ninguna modificación sustancial a los contenidos de los artículos — solo portadas más coherentes como paleta visual.

---

## v2026.07.001 — 31 de julio de 2026

**Artículos Data Governance + Swap InnoDB Cluster + Assertions Oracle 26ai**

Tres nuevos artículos publicados en el blog:

- Data Governance: el descanso para almorzar que retrasó el go-live (21 de julio)
- Swap al 100% en InnoDB Cluster: cuando `join_buffer_size` multiplica (28 de julio)
- Assertions en Oracle 26ai: finalmente una restricción que atraviesa (4 de agosto)

Bajo el capó: resync de `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 de junio de 2026

**Refactor completo de los 4 CV al pattern Borzacchiello + Bonjour LAN + PDF v2026-06**

Refactor completo de los cuatro CV especialistas (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 idiomas) al pattern Borzacchiello. Reescritas las experiencias históricas (S.EL.DAT., Oracle Italia, Auselda AED Group, Freelance) y publicados cuatro PDF v2026-06 en `static/downloads/` en versión standard y Randstad.

Nuevo acceso LAN vía Bonjour: el sitio es accesible desde teléfono, iPad y otros dispositivos de la red doméstica vía `ivanluminaria.local` y `ilum.local` — útil para vista previa móvil en tiempo real.

Añadida también una regla editorial: manifiesto Agile con cita original en inglés + traducción paralela.

---

## v2026.05.001 — 31 de mayo de 2026

**Artículos UML/RUP + enum Oracle + Buffer MCP + shell RCCS2025**

Dos nuevos artículos publicados en el blog: *de rivales a co-autores* (cómo Booch, Rumbaugh y Jacobson unificaron UML/RUP) y *enum Oracle 19c-26ai + domains* en cuatro idiomas.

En el frente de la automatización: integrado el servidor MCP Buffer para el scheduling automático de posts LinkedIn directamente desde la shell — el flujo editorial semanal ahora es más ágil. Refactor del shell environment al estándar RCCS2025 (`wwwhelp`/`wwwgo` paramétricos).

CTA de fin de artículo diferenciadas para los cuatro perfiles × cuatro idiomas. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` en thin tag pages.

---

## v2026.04.001 — 30 de abril de 2026

**Cadencia editorial consolidada + redesign /tags/ + CI cron safety net**

Artículo *PostgreSQL índices cuando duelen* en cuatro idiomas. Consolidación de la cadencia editorial semanal del martes: añadido un tercer cron GitHub Actions como safety net final, para proteger la publicación de los retrasos ocasionales de la infraestructura.

Redesign de la página `/tags/` con clasificación multi-sección (fix #84). Mobile search: bottom sheet implementado.

---

## v2026.03.001 — 31 de marzo de 2026

**Bootstrap del sitio + primeros artículos + setup del workflow editorial**

Primer release reconstruido retroactivamente. Bootstrap del sitio Hugo con deploy automático en GitHub Pages. Primer artículo Database Strategy publicado (art. #69: MySQL Group Replication binlog migration) en cuatro idiomas.

Setup del workflow editorial: propuesta de 3 títulos por artículo, tabla ideas con status, glosario a 5 términos, `hreflang` multilingüe, breadcrumbs `JSON-LD`, OpenGraph tags. Página Sobre Mí con etiquetas LinkedIn/Email en cuatro idiomas.
