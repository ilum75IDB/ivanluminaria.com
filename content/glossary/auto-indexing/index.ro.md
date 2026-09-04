---
title: "Auto-Indexing"
description: "Funcționalitate Oracle (din 19c) care analizează workload-ul SQL, creează indecși invizibili și îi promovează automat dacă îmbunătățesc performanța."
translationKey: "glossary_auto_indexing"
aka: "Automatic Indexing (Oracle)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Auto-Indexing este o funcționalitate introdusă în Oracle 19c care delegă motorului de baze de date gestionarea ciclului de viață al indecșilor: analiza workload-ului SQL, crearea experimentală, validarea și promovarea. În Oracle 21c comportamentul a devenit configurabil cu o granularitate mai mare.

## Cum funcționează

Procesul se desfășoară în trei faze automate:

1. **Analiză** — Oracle monitorizează workload-ul prin Automatic Workload Repository (AWR) și identifică interogările candidate să beneficieze de indecși noi.
2. **Creare invizibilă** — Indecșii candidați sunt creați ca `INVISIBLE`, deci optimizatorul îi ignoră în condiții normale.
3. **Validare și promovare** — Oracle rulează teste interne comparând planurile de execuție. Dacă indexul reduce costul, este promovat la `VISIBLE`; altfel rămâne invizibil sau este eliminat.

```sql
-- Verificarea configurației Auto-Indexing
SELECT * FROM DBA_AUTO_INDEX_CONFIG;

-- Activare / dezactivare explicită
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'IMPLEMENT');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'OFF');
```

## Context operațional

Auto-Indexing este conceput pentru medii OLTP cu workload variabil sau dificil de profilat manual. Pe baze de date de producție cu scheme stabile și indecși deja optimizați, riscul este crearea de indecși redundanți care cresc overhead-ul operațiunilor INSERT/UPDATE/DELETE și consumă spațiu în tablespace.

**Recomandare practică**: în medii de producție critice, rulați mai întâi în modul `REPORT ONLY` înainte de a activa `IMPLEMENT`. Dezactivați explicit cu `OFF` atunci când DBA-ul gestionează manual strategia de indexare.

```sql
-- Mod report: analizează dar nu creează indecși
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'REPORT ONLY');

-- Lista indecșilor gestionați automat
SELECT INDEX_NAME, STATUS, AUTO
FROM DBA_INDEXES
WHERE AUTO = 'YES';
```
