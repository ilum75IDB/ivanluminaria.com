---
title: "Major release Oracle"
description: "Versión principal del Database server Oracle con cambios significativos de feature y ciclo de soporte Premier dedicado. Numeración: 19c, 21c, 23ai, 26ai."
translationKey: "glossary_oracle_major_release"
aka: "Oracle Database release model"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

Una **major release** de Oracle Database es una versión principal del producto con cambios significativos de feature, ciclo de soporte Premier dedicado y numeración propia. En cada major release Oracle introduce **nuevas sintaxis SQL, nuevos tipos de datos, nuevas modalidades operativas del motor**, y — periódicamente — eleva el lower-bound de las versiones de compatibility soportadas.

## Cómo funciona el ciclo

Oracle alterna dos tipos de major release:

- **Long-Term Release (LTS)** — soporte Premier extendido (típicamente 5 años + 3 de extended). Es la versión de referencia para los sistemas enterprise críticos, donde los upgrades se planifican con años de anticipación. **19c** (LTS, lanzada 2019) y **23ai** (LTS, lanzada 2024) son las LTS recientes.
- **Innovation Release** — soporte breve (típicamente 2 años de Premier, sin extended). Pensada para quien quiere experimentar las nuevas feature pronto y después consolidar sobre la LTS sucesiva. **21c** fue la Innovation Release entre 19c y 23ai.

## Para qué sirve saber la versión

Determina **qué puedes escribir** en tu SQL: `JSON Relational Duality`, `SQL Domain` y `Vector Search` existen desde 23ai en adelante; las `ASSERTION` llegarán con la 26ai. Determina también qué **ya no puedes escribir**: feature deprecadas en versiones precedentes son removidas a intervalos regulares en las majors sucesivas. Sobre el upgrade path de 19c a 23ai, típicamente las diferencias impactan DDL, vistas del diccionario, y un puñado de package PL/SQL system.

## Las cuatro releases que cuentan para un esquema moderno

| Release | Tipo | Año | Qué aporta sobre vínculos y dominios |
|---------|------|------|--------------------------------------|
| **19c** | LTS | 2019 | Punto de partida: `CHECK` + lookup table |
| **21c** | Innovation | 2021 | Nada sustancial para los dominios de valores |
| **23ai** | LTS | 2024 | `SQL Domain`, `ALTER DOMAIN`, `Annotations` |
| **26ai** | LTS | 2026 (anunciada) | `ASSERTION` cross-tabla |
