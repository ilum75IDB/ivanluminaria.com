---
title: "Lookup table"
description: "Tabelă de referință conectată prin foreign key care stochează valorile valide ale unei enumerări, împreună cu eventuale atribute descriptive."
translationKey: "glossary_lookup_table"
aka: "Tabelă de referință"
articles:
  - "/posts/mysql/enum-mysql-semplifica-o-complica"
---

**Lookup table** este o tabelă de referință care stochează valorile valide ale unui domeniu enumerat, conectată la tabelele care o folosesc prin foreign key. Este calea "pur bază de date" pentru a modela o enumerare, alternativă la tipurile native ca ENUM sau la CHECK constraint.

## Cum este făcută

Schema canonică include cel puțin trei coloane: un `id` surogat (de obicei `SMALLINT` sau `TINYINT`) ca primary key, un `cod` textual (cheia naturală, de obicei unică), și o `descriere` extinsă. Adesea se adaugă atribute ca `ordine` pentru sortarea vizuală, `activ` pentru soft-delete, și timestamp-uri de audit.

## La ce servește

Avantajul principal față de ENUM este flexibilitatea: redenumirea unei descrieri este un `UPDATE` pe un rând, fără migrare sau rebuild al tabelei care o referențiază. Se pot adăuga atribute (etichete localizate, ordine, flag-uri) fără a atinge schema tabelelor copii. Este potrivită când valorile se schimbă în timp sau când sunt necesare metadate asociate.

## Când se folosește

Este alegerea potrivită atunci când:
- Valorile sunt modificate cu o anumită frecvență (adăugare, redenumire, dezactivare)
- Sunt necesare atribute suplimentare (traduceri, ordine, flag-uri)
- Se doresc gestionate valorile la runtime fără DDL (panouri admin)
- Numărul de valori crește în timp, peste 20-30

Prețul de plătit este JOIN-ul necesar în query-uri, care însă se optimizează ușor cu indexuri compuse și view-uri dedicate.
