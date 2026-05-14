# Sprint 2-bis — Log di lavoro: estensione "Fonti ufficiali" agli articoli tecnici

**Data inizio**: 2026-05-14
**Obiettivo**: aggiungere sezione `## Fonti ufficiali` + note `[n]` agli articoli tecnici che riportano comandi/sintassi/parametri/flag
**Branch**: `claude/plan-may-articles-YrcWA`
**Riferimento**: CLAUDE.md punto 11 (Fonti ufficiali per comandi tecnici)

## Pre-requisito: audit Sprint 1 — ✅ COMPLETATO (commit 538a088)

Verifica HTTP status su tutti i 20 URL nelle 5 sezioni "Fonti ufficiali" già esistenti (Sprint 1):
- ✅ 15 link 200 OK (Oracle 19c, PostgreSQL, Python, RFC4180)
- ⚠️ 3 link MySQL 403 da curl (anti-bot lato server, validi da browser — verificati con WebFetch)
- ❌ 2 link MariaDB 404 (path `/docs/server/architecture/` ormai inesistente) → fixati a `mariadb.com/kb/en/...`

**Risultato finale**: 20/20 URL OK.

## Pattern di lavoro per ciascun articolo

1. Leggere l'articolo IT, identificare 3-6 comandi/sintassi/parametri/flag candidati nota
2. Cercare la documentazione ufficiale di ciascuno (cliccare sul vendor giusto: Oracle 19c, PostgreSQL current, MySQL 8.0, MariaDB kb, ecc.)
3. **Verificare HTTP status di ogni URL prima di inserirlo** (curl + WebFetch per dev.mysql.com)
4. Inserire note `[n]` nel testo IT
5. Aggiungere sezione `## Fonti ufficiali` prima del Glossario (numerata 1..N)
6. Replicare in EN/ES/RO (link identici, note nel testo tradotte coerentemente)
7. Commit per articolo: `Sprint 2-bis: <slug> — aggiunta Fonti ufficiali (N note x 4 lingue)`
8. Aggiornare questo log

**Regola critica**: ZERO link 404 in produzione. Se un link non è verificabile, scartare o sostituire.

## Articoli candidati (20 totali)

### Oracle (3 articoli)

| # | Articolo | Stato | Commit |
|---|----------|-------|--------|
| 1 | oracle-awr-ash | ✅ done (5 note) | bb410f0 |
| 2 | oracle-data-guard | ✅ done (5 note) | 5d722eb |
| 3 | oracle-linux-kernel | ✅ done (5 note) | 318f98a |

### MySQL (6 articoli)

| # | Articolo | Stato | Commit |
|---|----------|-------|--------|
| 4 | binary-log-mysql | da fare | — |
| 5 | enum-mysql-semplifica-o-complica | da fare | — |
| 6 | mysql-group-replication-binlog-migration | da fare | — |
| 7 | mysql-pre-upgrade-assessment | da fare | — |
| 8 | mysql-users-and-hosts | da fare | — |
| 9 | mysqldump-mysqlpump-mydumper | da fare | — |

### PostgreSQL (6 articoli)

| # | Articolo | Stato | Commit |
|---|----------|-------|--------|
| 10 | enum-postgresql-paga-o-pesa | da fare | — |
| 11 | like-optimization-postgresql | ✅ done (3 note) | bbe7808 |
| 12 | pg-stat-statements | ✅ done (4 note) | 84bce01 |
| 13 | postgresql-indici-quando-fanno-male | da fare | — |
| 14 | postgresql_roles_and_users | da fare | — |
| 15 | vacuum-autovacuum-postgresql | ✅ done (6 note) | 5b8fb68 |

### Data Warehouse (5 articoli)

| # | Articolo | Stato | Commit |
|---|----------|-------|--------|
| 16 | bus-matrix-terreno-comune | da fare | — |
| 17 | fatto-grana-sbagliata | da fare | — |
| 18 | partitioning-dwh | da fare | — |
| 19 | ragged-hierarchies | da fare | — |
| 20 | scd-tipo-2 | da fare | — |

## Articoli ESCLUSI (10 — niente comandi tecnici, no Fonti ufficiali)

- oracle/oracle-cloud-migration (narrazione, no SQL)
- project-management/4-milioni-nessun-software
- project-management/ai-github-project-management
- project-management/ai-manager-project-management
- project-management/bici-vs-auto-roma
- project-management/pagamenti-60-90-120-giorni
- project-management/smartworking-consulenza-it
- project-management/standup-meeting-15-minuti
- project-management/team-di-progetto-che-reggono
- project-management/tecnica-si-e-yes-and

## Note per ripresa post-timeout

Se sessione ripresa:
1. Leggere lo stato di ogni articolo
2. Articoli con `✅ done` → completati
3. Articoli con `da fare` → da iniziare
4. Verificare ultimo commit `Sprint 2-bis: <slug>` per capire dove riprendere
