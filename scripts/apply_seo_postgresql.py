#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to PostgreSQL section articles (issue #89).
Modifies frontmatter of 6 articles × 4 languages = 24 files.
Creates .bak backup of each file before writing.
"""
import re
from pathlib import Path
import sys

# (slug, lang): (seoTitle, description)
UPDATES = {
    # ----- 1. explain-analyze-postgresql -----
    ("explain-analyze-postgresql", "it"): (
        "EXPLAIN ANALYZE PostgreSQL: leggere il piano di esecuzione",
        "PostgreSQL EXPLAIN ANALYZE: leggere un execution plan, riconoscere nested loop costosi e ANALYZE su statistiche vecchie. Caso reale 2M righe.",
    ),
    ("explain-analyze-postgresql", "en"): (
        "EXPLAIN ANALYZE PostgreSQL: reading the execution plan",
        "PostgreSQL EXPLAIN ANALYZE: reading an execution plan, spotting costly nested loops and stale statistics. Real case on 2-million-row table.",
    ),
    ("explain-analyze-postgresql", "es"): (
        "EXPLAIN ANALYZE PostgreSQL: leer el plan de ejecución",
        "PostgreSQL EXPLAIN ANALYZE: leer un plan de ejecución, detectar nested loop costosos y ANALYZE sobre estadísticas viejas. Caso real con 2M filas.",
    ),
    ("explain-analyze-postgresql", "ro"): (
        "EXPLAIN ANALYZE PostgreSQL: citirea planului de execuție",
        "PostgreSQL EXPLAIN ANALYZE: citirea planului de execuție, nested loop costisitor și ANALYZE pe statistici vechi. Caz real cu 2M rânduri.",
    ),
    # ----- 2. like-optimization-postgresql -----
    ("like-optimization-postgresql", "it"): (
        "PostgreSQL LIKE con %valore%: GIN index e pg_trgm",
        "Ottimizzazione PostgreSQL: LIKE '%valore%' genera full scan. Uso di pg_trgm e indice GIN per trasformare un wildcard search in lookup veloce.",
    ),
    ("like-optimization-postgresql", "en"): (
        "PostgreSQL LIKE with %value%: GIN index and pg_trgm",
        "PostgreSQL optimization: LIKE '%value%' causes full scan. Using pg_trgm and GIN index to turn a wildcard search into a fast lookup. Real case.",
    ),
    ("like-optimization-postgresql", "es"): (
        "PostgreSQL LIKE con %valor%: índice GIN y pg_trgm",
        "Optimización PostgreSQL: LIKE '%valor%' genera full scan. Uso de pg_trgm e índice GIN para convertir una búsqueda wildcard en lookup rápido.",
    ),
    ("like-optimization-postgresql", "ro"): (
        "PostgreSQL LIKE cu %valoare%: index GIN și pg_trgm",
        "Optimizare PostgreSQL: LIKE '%valoare%' generează full scan. Folosirea pg_trgm și index GIN pentru a transforma căutarea wildcard în lookup rapid.",
    ),
    # ----- 3. pg-stat-statements -----
    ("pg-stat-statements", "it"): (
        "pg_stat_statements: diagnosi query PostgreSQL",
        "PostgreSQL pg_stat_statements: l'estensione di diagnosi query da installare per prima. Trovare le tre query che consumano l'80% delle risorse.",
    ),
    ("pg-stat-statements", "en"): (
        "pg_stat_statements: PostgreSQL query diagnostics",
        "PostgreSQL pg_stat_statements: the first query diagnostics extension to install. Find the three queries consuming 80% of database resources.",
    ),
    ("pg-stat-statements", "es"): (
        "pg_stat_statements: diagnóstico de queries PostgreSQL",
        "PostgreSQL pg_stat_statements: la extensión de diagnóstico de queries a instalar primero. Encontrar las tres queries que consumen el 80%.",
    ),
    ("pg-stat-statements", "ro"): (
        "pg_stat_statements: diagnosticare query PostgreSQL",
        "PostgreSQL pg_stat_statements: extensia de diagnosticare query de instalat prima. Găsește cele trei query-uri care consumă 80% din resurse.",
    ),
    # ----- 4. postgresql-indici-quando-fanno-male -----
    ("postgresql-indici-quando-fanno-male", "it"): (
        "PostgreSQL: indici inutilizzati e pg_stat_user_indexes",
        "PostgreSQL: trovare e rimuovere indici inutilizzati con pg_stat_user_indexes. Caso reale: tabella con 15 indici di cui 8 mai usati.",
    ),
    ("postgresql-indici-quando-fanno-male", "en"): (
        "PostgreSQL: unused indexes and pg_stat_user_indexes",
        "PostgreSQL: how to find and drop unused indexes with pg_stat_user_indexes. Real case: a table with 15 indexes, 8 of them never used.",
    ),
    ("postgresql-indici-quando-fanno-male", "es"): (
        "PostgreSQL: índices no usados y pg_stat_user_indexes",
        "PostgreSQL: encontrar y eliminar índices no usados con pg_stat_user_indexes. Caso real: una tabla con 15 índices, 8 nunca usados.",
    ),
    ("postgresql-indici-quando-fanno-male", "ro"): (
        "PostgreSQL: indecși nefolosiți și pg_stat_user_indexes",
        "PostgreSQL: cum găsești și elimini indecșii nefolosiți cu pg_stat_user_indexes. Caz real: tabel cu 15 indecși, 8 nefolosiți niciodată.",
    ),
    # ----- 5. postgresql_roles_and_users -----
    ("postgresql_roles_and_users", "it"): (
        "PostgreSQL ROLE: utenti, ruoli e GRANT con least privilege",
        "PostgreSQL ROLE: utenti e ruoli sono lo stesso oggetto. Modello mentale, GRANT, NOINHERIT e creazione di un account read-only manutenibile.",
    ),
    ("postgresql_roles_and_users", "en"): (
        "PostgreSQL ROLE: users, roles and GRANT with least privilege",
        "PostgreSQL ROLE: users and roles are the same object. Mental model, GRANT, NOINHERIT and how to build a truly maintainable read-only account.",
    ),
    ("postgresql_roles_and_users", "es"): (
        "PostgreSQL ROLE: usuarios, roles y GRANT con least privilege",
        "PostgreSQL ROLE: usuarios y roles son el mismo objeto. Modelo mental, GRANT, NOINHERIT y construir un usuario read-only realmente mantenible.",
    ),
    ("postgresql_roles_and_users", "ro"): (
        "PostgreSQL ROLE: utilizatori, roluri și GRANT least privilege",
        "PostgreSQL ROLE: utilizatorii și rolurile sunt același obiect. Model mental, GRANT, NOINHERIT și construirea unui utilizator read-only mentenabil.",
    ),
    # ----- 6. vacuum-autovacuum-postgresql -----
    ("vacuum-autovacuum-postgresql", "it"): (
        "PostgreSQL VACUUM e autovacuum: diagnosi e tuning del bloat",
        "PostgreSQL VACUUM e autovacuum: diagnosi del bloat su database da 200 GB, lettura di pg_stat_user_tables e tuning senza disabilitare nulla.",
    ),
    ("vacuum-autovacuum-postgresql", "en"): (
        "PostgreSQL VACUUM and autovacuum: bloat diagnosis and tuning",
        "PostgreSQL VACUUM and autovacuum: bloat diagnosis on a 200 GB database, reading pg_stat_user_tables and tuning without disabling anything.",
    ),
    ("vacuum-autovacuum-postgresql", "es"): (
        "PostgreSQL VACUUM y autovacuum: diagnóstico y tuning de bloat",
        "PostgreSQL VACUUM y autovacuum: diagnóstico de bloat en base de datos de 200 GB, lectura de pg_stat_user_tables y tuning sin desactivar nada.",
    ),
    ("vacuum-autovacuum-postgresql", "ro"): (
        "PostgreSQL VACUUM și autovacuum: diagnostic și tuning bloat",
        "PostgreSQL VACUUM și autovacuum: diagnostic bloat pe bază de date 200 GB, citirea pg_stat_user_tables și tuning fără a dezactiva nimic.",
    ),
}

BASE = Path("content/posts/postgresql")


def escape_yaml_str(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def process_file(slug: str, lang: str, seo_title: str, description: str) -> tuple[bool, str]:
    path = BASE / slug / f"index.{lang}.md"
    if not path.exists():
        return False, f"FILE NOT FOUND: {path}"

    text = path.read_text(encoding="utf-8")
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    desc_pattern = re.compile(r'^description:\s*"[^"]*"\s*$', re.MULTILINE)
    new_desc_line = f'description: "{escape_yaml_str(description)}"'
    new_text, n_desc = desc_pattern.subn(new_desc_line, text, count=1)
    if n_desc != 1:
        return False, f"description line not matched: {path}"

    if re.search(r'^seoTitle:', new_text, re.MULTILINE):
        seo_pattern = re.compile(r'^seoTitle:\s*"[^"]*"\s*$', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_seo = seo_pattern.subn(new_seo_line, new_text, count=1)
        if n_seo != 1:
            return False, f"seoTitle existed but not matched: {path}"
    else:
        title_pattern = re.compile(r'(^title:\s*"[^"]*"\s*$)', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_title = title_pattern.subn(
            r"\1\n" + new_seo_line, new_text, count=1
        )
        if n_title != 1:
            return False, f"title line not found: {path}"

    path.write_text(new_text, encoding="utf-8")
    return True, f"OK: {path}"


def main():
    ok = 0
    fail = 0
    for (slug, lang), (seo_title, description) in UPDATES.items():
        success, msg = process_file(slug, lang, seo_title, description)
        if success:
            ok += 1
            print(f"  ✓ {msg}")
        else:
            fail += 1
            print(f"  ✗ {msg}", file=sys.stderr)
    print(f"\nDone: {ok} updated, {fail} failed")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
