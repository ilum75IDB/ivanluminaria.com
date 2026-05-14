# Sprint 1 — Log di lavoro

**Data inizio**: 2026-05-14
**Obiettivo**: 5 fix tecnici P0 + esordio sezione `## Fonti ufficiali` sugli articoli toccati
**Branch**: `claude/plan-may-articles-YrcWA`

## Pattern applicato

Per ciascuno dei 5 articoli:
1. Correggere l'errore tecnico segnalato dall'audit B (verifica empirica in `audit_verification.md` sezione 2)
2. Aggiungere note `[n]` nel testo dopo le affermazioni tecniche critiche
3. Aggiungere sezione `## Fonti ufficiali` prima del Glossario, con link alla doc ufficiale
4. Replicare in tutte e 4 le lingue (IT/EN/ES/RO)
5. Commit per articolo con messaggio `Sprint 1 P0-N: <slug> — fix tecnico + Fonti ufficiali (4 lingue)`

## Convenzione note

- `[1]`, `[2]`, ... dopo l'affermazione tecnica nel testo
- Sezione `## Fonti ufficiali` con elenco numerato
- Sezione posizionata **prima** del Glossario
- Stessa sezione in tutte e 4 le lingue (link in inglese)

## Articoli — stato

| # | Articolo | Sezione | Errore tecnico | Stato | Commit |
|---|----------|---------|----------------|-------|--------|
| 1 | oracle-roles-privileges | Oracle | Unified Audit: `AUDIT POLICY` non `ALTER AUDIT POLICY ENABLE` | ✅ tutto done (IT/EN/ES/RO) | (questo commit) |
| 2 | galera-cluster-3-nodi | MySQL | Durabilità con `flush_log_at_trx_commit=2`: riformulare come trade-off | ✅ tutto done (IT/EN/ES/RO) | (questo commit) |
| 3 | mysql-multi-istanza-secure-file-priv | MySQL | CSV con sed: aggiungere caveat + esempio Python | ✅ tutto done (IT/EN/ES/RO) | (questo commit) |
| 4 | oracle-partitioning | Oracle | CTAS + rename con DML concorrente: avvertenza | da fare | — |
| 5 | explain-analyze-postgresql | PostgreSQL | `default_statistics_target`: MCV/histogram, non "100 righe campione" | da fare | — |

## Note per ripresa post-timeout

Se ripreso da nuova sessione, leggere la colonna "Stato":
- `da fare` → non iniziato
- `in-corso` → iniziato (riprendere da qui)
- `✅ IT done`, `✅ EN done`, ecc. → parziale, riprendere dalla lingua mancante
- `✅ tutto done` → completato, ricontrollare commit

Convenzione commit message: `Sprint 1 P0-<N>: <slug> — fix tecnico + Fonti ufficiali (4 lingue)`
