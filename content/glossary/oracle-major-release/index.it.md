---
title: "Major release Oracle"
description: "Versione principale del Database server Oracle con cambiamenti significativi di feature e ciclo di supporto Premier dedicato. Numerazione: 19c, 21c, 23ai, 26ai."
translationKey: "glossary_oracle_major_release"
aka: "Oracle Database release model"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

Una **major release** di Oracle Database è una versione principale del prodotto con cambiamenti significativi di feature, ciclo di supporto Premier dedicato e numerazione propria. Ad ogni major release Oracle introduce **nuove sintassi SQL, nuovi tipi di dato, nuove modalità operative del motore**, e — periodicamente — alza la lower-bound delle versioni di compatibility supportate.

## Come funziona il ciclo

Oracle alterna due tipi di major release:

- **Long-Term Release (LTS)** — supporto Premier esteso (tipicamente 5 anni + 3 di extended). È la versione di riferimento per i sistemi enterprise critici, dove gli upgrade sono pianificati con anni di anticipo. **19c** (LTS, rilasciata 2019) e **23ai** (LTS, rilasciata 2024) sono le LTS recenti.
- **Innovation Release** — supporto breve (tipicamente 2 anni di Premier, no extended). Pensata per chi vuole sperimentare le nuove feature presto e poi consolidare sulla LTS successiva. **21c** è stata l'Innovation Release tra 19c e 23ai.

## A cosa serve sapere la versione

Determina **cosa puoi scrivere** nel tuo SQL: `JSON Relational Duality`, `SQL Domain` e `Vector Search` esistono dalla 23ai, le `ASSERTION` arriveranno con la 26ai. Determina anche cosa **non puoi più scrivere**: feature deprecate in versioni precedenti vengono rimosse a intervalli regolari nelle major successive. Sull'upgrade path da 19c a 23ai, tipicamente le differenze impattano DDL, viste del dizionario, e una manciata di package PL/SQL system.

## Le quattro release che contano per uno schema moderno

| Release | Tipo | Anno | Cosa porta sul tema vincoli e domini |
|---------|------|------|--------------------------------------|
| **19c** | LTS | 2019 | Punto di partenza: `CHECK` + lookup table |
| **21c** | Innovation | 2021 | Nulla di sostanziale per i domini di valori |
| **23ai** | LTS | 2024 | `SQL Domain`, `ALTER DOMAIN`, `Annotations` |
| **26ai** | LTS | 2026 (annunciata) | `ASSERTION` cross-tabella |
