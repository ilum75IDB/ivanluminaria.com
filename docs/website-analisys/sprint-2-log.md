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
| 2 | oracle-cloud-migration | 5 | da fare | — |
| 3 | oracle-data-guard | 3 | da fare | — |
| 4 | oracle-linux-kernel | 3 | da fare | — |
| 5 | oracle-partitioning | 6 | da fare | — |
| 6 | oracle-roles-privileges | 4 | da fare | — |

### MySQL (6 articoli, 38 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 7 | binary-log-mysql | 7 | da fare | — |
| 8 | galera-cluster-3-nodi | 6 | da fare | — |
| 9 | mysql-group-replication-binlog-migration | 7 | da fare | — |
| 10 | mysql-multi-istanza-secure-file-priv | 7 | da fare | — |
| 11 | mysql-users-and-hosts | 2 | da fare | — |
| 12 | mysqldump-mysqlpump-mydumper | 9 | da fare | — |

### PostgreSQL (4 articoli, 16 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 13 | explain-analyze-postgresql | 5 | da fare | — |
| 14 | pg-stat-statements | 6 (+1 mitig.assolutismo) | da fare | — |
| 15 | postgresql_roles_and_users | 0 (già pulito) | skip | — |
| 16 | vacuum-autovacuum-postgresql | 5 | da fare | — |

### Data Warehouse (5 articoli, 29 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 17 | bus-matrix-terreno-comune | 7 | da fare | — |
| 18 | fatto-grana-sbagliata | 6 | da fare | — |
| 19 | partitioning-dwh | 3 | da fare | — |
| 20 | ragged-hierarchies | 10 | da fare | — |
| 21 | scd-tipo-2 | 3 | da fare | — |

### Project Management (8 articoli, 16-17 modifiche annotate)

| # | Articolo | Mod IT | Stato | Commit |
|---|----------|-------:|-------|--------|
| 22 | 4-milioni-nessun-software | 1 | da fare | — |
| 23 | ai-github-project-management | 4 | da fare | — |
| 24 | ai-manager-project-management | 1 | da fare | — |
| 25 | bici-vs-auto-roma | 4 | da fare | — |
| 26 | pagamenti-60-90-120-giorni | 0 (già pulito) | skip | — |
| 27 | smartworking-consulenza-it | 3 | da fare | — |
| 28 | standup-meeting-15-minuti | 2 | da fare | — |
| 29 | tecnica-si-e-yes-and | 1 | da fare | — |

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
