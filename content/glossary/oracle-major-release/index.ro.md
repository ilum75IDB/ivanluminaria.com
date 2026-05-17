---
title: "Major release Oracle"
description: "Versiune principală a Oracle Database server cu schimbări semnificative de feature și ciclu de suport Premier dedicat. Numerotare: 19c, 21c, 23ai, 26ai."
translationKey: "glossary_oracle_major_release"
aka: "Oracle Database release model"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

O **major release** Oracle Database este o versiune principală a produsului cu schimbări semnificative de feature, ciclu de suport Premier dedicat și numerotare proprie. La fiecare major release Oracle introduce **noi sintaxe SQL, noi tipuri de date, noi modalități operaționale ale motorului**, și — periodic — ridică limita inferioară a versiunilor de compatibility suportate.

## Cum funcționează ciclul

Oracle alternează două tipuri de major release:

- **Long-Term Release (LTS)** — suport Premier extins (tipic 5 ani + 3 de extended). Este versiunea de referință pentru sistemele enterprise critice, unde upgrade-urile sunt planificate cu ani de avans. **19c** (LTS, lansată 2019) și **23ai** (LTS, lansată 2024) sunt LTS-urile recente.
- **Innovation Release** — suport scurt (tipic 2 ani de Premier, fără extended). Gândită pentru cei care vor să experimenteze noile feature devreme și apoi să consolideze pe LTS-ul următor. **21c** a fost Innovation Release-ul dintre 19c și 23ai.

## La ce servește să știi versiunea

Determină **ce poți scrie** în SQL-ul tău: `JSON Relational Duality`, `SQL Domain` și `Vector Search` există de la 23ai înainte; `ASSERTION` vor sosi cu 26ai. Determină și ce **nu mai poți scrie**: feature deprecate în versiuni precedente sunt eliminate la intervale regulate în major-urile ulterioare. Pe traseul de upgrade de la 19c la 23ai, diferențele impactează tipic DDL, view-uri de dicționar, și un mănunchi de pachete PL/SQL de sistem.

## Cele patru release-uri care contează pentru o schemă modernă

| Release | Tip | An | Ce aduce pe tema constrângerilor și domeniilor |
|---------|------|----|--------------------------------------|
| **19c** | LTS | 2019 | Punct de plecare: `CHECK` + lookup table |
| **21c** | Innovation | 2021 | Nimic substanțial pentru domeniile de valori |
| **23ai** | LTS | 2024 | `SQL Domain`, `ALTER DOMAIN`, `Annotations` |
| **26ai** | LTS | 2026 (anunțată) | `ASSERTION` cross-tabel |
