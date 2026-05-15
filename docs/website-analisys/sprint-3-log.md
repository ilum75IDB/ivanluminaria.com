# Sprint 3 — Log di lavoro

**Data inizio**: 2026-05-15
**Branch**: `claude/plan-may-articles-YrcWA`
**Obiettivo**: chiudere i task P1 residui dell'audit (tag governance, JSON-LD fix, P1 mitigations)

## Task

| # | Task | Tipo | Effort | Stato | Commit |
|---|------|------|--------|-------|--------|
| 1 | Data Guard licensing box (P1-8, sezione 2.6 audit) | mitigation | S | da fare | — |
| 2 | MySQL anonymous user mitigation (P1-9, sezione 2.8 audit) | mitigation | S | da fare | — |
| 3 | JSON-LD double-quoting fix (P1-7, sezione 1.3 audit) | bug Hugo template | S | da fare | — |
| 4 | Tag governance: 126→~30 tag (P1-6, sezione 1.1 audit) | refactoring metadati | M | da fare | — |
| 5 | `expire_logs_days` → `binlog_expire_logs_seconds` in mysql-pre-upgrade-assessment (P1-10) | mitigation | XS | da fare | — |

**Nota**: il caveat su `pg_stat_statements` (sezione 3 audit — "Con qualche eccezione PgBouncer multi-tenant, replica logica downstream...") è **già stato applicato** durante Sprint 2 nella revisione stilistica (vedere il primo paragrafo dell'articolo IT/EN/ES/RO).

## Pattern di lavoro

Per ogni task: leggere → identificare modifica → applicare → verificare → commit per task + push.

## Sequenza

Si comincia dai task più semplici (mitigations testuali) per warm-up, poi JSON-LD fix (1 template), poi tag governance (sforzo maggiore).
