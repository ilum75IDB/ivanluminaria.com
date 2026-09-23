---
title: "Changelog"
seoTitle: "Changelog · ivanluminaria.com"
description: "Histórico de releases de ivanluminaria.com — hitos editoriales y cambios estructurales marcados con esquema CalVer."
draft: false
layout: "simple"
---

Este sitio sigue un esquema de versionado **CalVer** (`v<YYYY>.<MM>.<micro>`) para marcar los hitos editoriales. No etiquetamos cada artículo publicado — solo los cambios estructurales a los perfiles, al workflow o al sitio en sí.

---

## v2026.09.001 — 20 de septiembre de 2026

**Cinco CV pilares con voz narrativa fuerte + versionado CalVer adoptado**

Release de estabilización de los perfiles de rol. Los cinco perfiles — [Technical Leader](/es/resumes/technical-leader/), [Project Manager](/es/resumes/project-manager/), [DWH Architect](/es/resumes/dwh-architect/), [Oracle DBA](/es/resumes/oracle-dba/), [Oracle PL/SQL](/es/resumes/oracle-plsql/) — cuentan ahora con un Professional Profile atemporal con voz narrativa fuerte diferenciada por arquetipo. Cada uno enfrenta creencias específicas del lector y cierra con un valor operativo concreto en lugar de fórmulas genéricas.

Cambios principales:

- Recuperación de la voz narrativa fuerte en cada CV, sustituyendo los párrafos neutros "de job description" con posicionamientos calibrados sobre el arquetipo dominante
- Eliminadas las referencias específicas del Profile — permanecen en la sección Experience, donde es apropiado citarlas con contexto temporal
- Nueva página Technical Leader como master de los cuatro pilares especialistas
- Adoptado versionado CalVer para marcar los hitos editoriales del sitio

Bajo el capó: actualizados los CV Markdown fuente en `docs/` desde los que se generan los PDF; pipeline PDF con `pandoc` + `WeasyPrint` para regenerar los CV en inglés desde los Markdown.

---

## v2026.08.001 — 31 de agosto de 2026

**Regeneración masiva de las cover images con AI**

Realineación gráfica coherente al brand editorial: unos treinta artículos históricos del blog recibieron cover images regeneradas con AI. Ninguna modificación sustancial a los contenidos — solo portadas más coherentes como paleta visual.

---

## v2026.07.001 — 31 de julio de 2026

**Cadencia editorial continuada + sync shell cross-Mac**

Continuación de la publicación semanal del martes con nuevos contenidos técnicos en el blog. Bajo el capó: resync de `scripts/shell/config/zshrc.txt` v7.1 cross-Mac.

---

## v2026.06.001 — 30 de junio de 2026

**Refactor completo de los 4 CV especialistas + Bonjour LAN + PDF v2026-06**

Refactor completo de los cuatro CV especialistas (Project Manager, DWH Architect, Oracle DBA, Oracle PL/SQL × 4 idiomas) con reescritura estructural de las secciones de experiencia histórica. Publicados cuatro PDF v2026-06 en `static/downloads/` en versión standard y Randstad.

Nuevo acceso LAN vía Bonjour: el sitio es accesible desde teléfono, iPad y otros dispositivos de la red doméstica vía `ivanluminaria.local` y `ilum.local` — útil para vista previa móvil en tiempo real.

Añadida también una regla editorial: citas en idioma original + traducción paralela para los textos técnicos históricos.

---

## v2026.05.001 — 31 de mayo de 2026

**Integración MCP Buffer + shell RCCS2025 + CTA de artículo**

En el frente de la automatización: integrado el servidor MCP Buffer para el scheduling automático de posts LinkedIn directamente desde la shell — el flujo editorial semanal ahora es más ágil. Refactor del shell environment al estándar RCCS2025 (`wwwhelp`/`wwwgo` paramétricos).

CTA de fin de artículo diferenciadas para los cuatro perfiles × cuatro idiomas. SEO cleanup: `robots.txt`, taxonomy categories, `noindex` en thin tag pages.

Continuación de la publicación semanal del martes con nuevos contenidos técnicos.

---

## v2026.04.001 — 30 de abril de 2026

**Cadencia editorial consolidada + redesign /tags/ + CI cron safety net**

Consolidación de la cadencia editorial semanal del martes: añadido un tercer cron GitHub Actions como safety net final, para proteger la publicación de los retrasos ocasionales de la infraestructura.

Redesign de la página `/tags/` con clasificación multi-sección. Mobile search: bottom sheet implementado.

---

## v2026.03.001 — 31 de marzo de 2026

**Bootstrap del sitio + setup del workflow editorial**

Primer release reconstruido retroactivamente. Bootstrap del sitio Hugo con deploy automático en GitHub Pages.

El material que alimenta el blog proviene de un archivo personal construido durante casi treinta años de trabajo en informática — apuntes técnicos, memorias de proyecto, notas tomadas proyecto tras proyecto, incident tras incident. La reelaboración de ese patrimonio ha producido los primeros artículos del blog Database Strategy, publicados en cuatro idiomas.

Setup del workflow editorial: propuesta de 3 títulos por artículo, tabla ideas con status, glosario a 5 términos, `hreflang` multilingüe, breadcrumbs `JSON-LD`, OpenGraph tags. Página Sobre Mí con etiquetas LinkedIn/Email en cuatro idiomas.
