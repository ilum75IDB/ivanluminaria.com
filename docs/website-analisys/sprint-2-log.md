# Sprint 2 — Log di lavoro: revisione stilistica massiva

**Data inizio**: 2026-05-14
**Obiettivo**: applicare le ~125 modifiche stilistiche annotate sui 29 articoli IT (+ propagazione a EN, ES, RO)
**Branch**: `claude/plan-may-articles-YrcWA`
**Fonte annotazioni**: `docs/website-analisys/stylistic-annotations/*.md` (1 file per sezione)
**Regola**: vedere `docs/STILE_LINGUISTICO.md` per i criteri

## Pattern applicato

Per ciascuno dei 29 articoli:
1. Leggere le annotazioni nel file `stylistic-annotations/<sezione>.md`
2. Applicare modifiche IT con Edit
3. Propagare equivalenti su EN, ES, RO
4. Commit per articolo: `Sprint 2: <slug> — STILE_LINGUISTICO (N mod x 4 lingue)`
5. Aggiornare questo log con `✅ tutto done`

## Articoli — stato (29 totali)

### Oracle (6 articoli, 25 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 1 | oracle-awr-ash | 4 | ✅ tutto done | (questo commit) |
| 2 | oracle-cloud-migration | 5 | ✅ tutto done | cc28468 (batch Oracle) |
| 3 | oracle-data-guard | 3 | ✅ tutto done | cc28468 (batch Oracle) |
| 4 | oracle-linux-kernel | 3 | ✅ tutto done | cc28468 (batch Oracle) |
| 5 | oracle-partitioning | 6 | ✅ tutto done | cc28468 (batch Oracle) |
| 6 | oracle-roles-privileges | 4 | ✅ tutto done | cc28468 (batch Oracle) |

### MySQL (6 articoli, 38 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 7 | binary-log-mysql | 6 | ✅ tutto done | cf3f4b9 (batch MySQL) |
| 8 | galera-cluster-3-nodi | 6 | ✅ tutto done | cf3f4b9 (batch MySQL) |
| 9 | mysql-group-replication-binlog-migration | 7 IT / 6 EN-ES-RO | ✅ tutto done | cf3f4b9 (batch MySQL) |
| 10 | mysql-multi-istanza-secure-file-priv | 7 | ✅ tutto done | cf3f4b9 (batch MySQL) |
| 11 | mysql-users-and-hosts | 2 | ✅ tutto done | cf3f4b9 (batch MySQL) |
| 12 | mysqldump-mysqlpump-mydumper | 9 | ✅ tutto done | cf3f4b9 (batch MySQL) |

### PostgreSQL (4 articoli, 16 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 13 | explain-analyze-postgresql | 5 | ✅ tutto done | aee7c1b (batch PG via WIP-2) |
| 14 | pg-stat-statements | 6 (+1 mitig.assolutismo) | ✅ tutto done | aee7c1b (batch PG via WIP-2) |
| 15 | postgresql_roles_and_users | 0 (già pulito) | skip | — |
| 16 | vacuum-autovacuum-postgresql | 5 | ✅ tutto done | aee7c1b (batch PG via WIP-2) |

### Data Warehouse (5 articoli, 29 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 17 | bus-matrix-terreno-comune | 7 | ✅ tutto done | a01ee7d (batch DW) |
| 18 | fatto-grana-sbagliata | 7 | ✅ tutto done | a01ee7d (batch DW) |
| 19 | partitioning-dwh | 3 | ✅ tutto done | a01ee7d (batch DW) |
| 20 | ragged-hierarchies | 11 | ✅ tutto done | a01ee7d (batch DW) |
| 21 | scd-tipo-2 | 3 | ✅ tutto done | a01ee7d (batch DW) |

### Project Management (8 articoli, 16-17 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 22 | 4-milioni-nessun-software | 1 | ✅ tutto done | 196d1e8 (batch PM) |
| 23 | ai-github-project-management | 4 | ✅ tutto done | 196d1e8 (batch PM) |
| 24 | ai-manager-project-management | 1 | ✅ tutto done | 196d1e8 (batch PM) |
| 25 | bici-vs-auto-roma | 4 | ✅ tutto done | 196d1e8 (batch PM) |
| 26 | pagamenti-60-90-120-giorni | 0 (già pulito) | skip | — |
| 27 | smartworking-consulenza-it | 3 | ✅ tutto done | 196d1e8 (batch PM) |
| 28 | standup-meeting-15-minuti | 2 | ✅ tutto done | 196d1e8 (batch PM) |
| 29 | tecnica-si-e-yes-and | 1 | ✅ tutto done | 196d1e8 (batch PM) |

## Note per ripresa post-timeout

Se ripreso da nuova sessione:
1. Leggere lo Stato di ogni articolo
2. Articoli con `✅ tutto done` → completati
3. Articoli con `in-corso (IT done)`, `(EN done)`, ecc. → riprendere dalla lingua mancante
4. Articoli con `skip` → già puliti, niente da fare
5. Articoli con `da fare` → da iniziare

Convenzione commit: `Sprint 2: <slug> — STILE_LINGUISTICO (N mod x 4 lingue)`

## Totale stimato

- 27 articoli con modifiche (2 skip): pagamenti-60-90-120-giorni + postgresql_roles_and_users
- ~125 modifiche IT × 4 lingue = ~500 modifiche totali nei file
- Effort: 2-3 ore di applicazione meccanica

## ✅ Sprint 2 COMPLETATO — 2026-05-14

Tutte le 5 sezioni applicate con 5 batch commit principali (1 manuale + 4 da agenti paralleli):

| Sezione | Commit | Articoli | Mod IT |
|---------|--------|----------|--------|
| Oracle (parte) | 5271019 | 1 (oracle-awr-ash) | 4 |
| Oracle (resto) | cc28468 | 5 | 21 |
| MySQL | cf3f4b9 | 6 | 37 |
| PostgreSQL | aee7c1b (via WIP-2) | 3 | 16 |
| Data Warehouse | a01ee7d | 5 | 31 |
| Project Management | 196d1e8 | 7 | 16 |
| **Totale** | — | **27** | **125** |

Effort effettivo (sessione Claude):
- Articolo manuale (oracle-awr-ash): ~10 min
- 5 agenti paralleli + commit per sezione: ~25 min totali
- Totale parallelizzato: ~35 min (vs ~3h sequenziali)

Tutte le modifiche × 4 lingue = ~500 sostituzioni file applicate.
