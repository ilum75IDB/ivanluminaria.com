#!/usr/bin/env python3
"""
v2: Apply SEO-optimized descriptions to non-article pages (issue #89).
Replaces the existing descriptions with specifically-crafted ones,
adds home page description in language TOML files, and updates the
glossary index seoTitle to remove the obsolete "150+" hardcoded number.

Covers: section index (5x4=20), about (4), resumes (5x4=20),
glossary index (4 with both desc + seoTitle update), home (4 TOML).
Total: 52 frontmatter files + 4 TOML files.
"""
import re
from pathlib import Path
import sys

# Pages: {path: (seoTitle_override or None, description)}
# seoTitle: if None, keep what's already there.
PAGES = {
    # ===== SECTION INDEX (5 sezioni × 4 lingue) =====
    "content/posts/_index.it.md": (
        None,
        "Database Strategy: blog tecnico su Oracle, PostgreSQL, MySQL, DWH e project management. Articoli pratici da 30 anni di consulenza IT.",
    ),
    "content/posts/_index.en.md": (
        None,
        "Database Strategy: technical blog on Oracle, PostgreSQL, MySQL, data warehouse and project management. Hands-on articles from 30 years of IT consulting.",
    ),
    "content/posts/_index.es.md": (
        None,
        "Database Strategy: blog técnico sobre Oracle, PostgreSQL, MySQL, data warehouse y project management. Artículos prácticos de 30 años de consultoría IT.",
    ),
    "content/posts/_index.ro.md": (
        None,
        "Database Strategy: blog tehnic despre Oracle, PostgreSQL, MySQL, data warehouse și project management. Articole practice din 30 ani de consultanță IT.",
    ),
    "content/posts/oracle/_index.it.md": (
        None,
        "Articoli Oracle 19c+: amministrazione DBA, performance tuning, Data Guard, partitioning, AWR/ASH, sicurezza e migrazione su Oracle Cloud (OCI).",
    ),
    "content/posts/oracle/_index.en.md": (
        None,
        "Oracle 19c+ articles: DBA administration, performance tuning, Data Guard, partitioning, AWR/ASH, security and migration to Oracle Cloud (OCI).",
    ),
    "content/posts/oracle/_index.es.md": (
        None,
        "Artículos Oracle 19c+: administración DBA, performance tuning, Data Guard, partitioning, AWR/ASH, seguridad y migración a Oracle Cloud (OCI).",
    ),
    "content/posts/oracle/_index.ro.md": (
        None,
        "Articole Oracle 19c+: administrare DBA, performance tuning, Data Guard, partitioning, AWR/ASH, securitate și migrare la Oracle Cloud (OCI).",
    ),
    "content/posts/postgresql/_index.it.md": (
        None,
        "Articoli PostgreSQL: EXPLAIN ANALYZE, ottimizzazione query, pg_stat_statements, indici GIN/B-tree, VACUUM, autovacuum, ROLE, GRANT e best practice.",
    ),
    "content/posts/postgresql/_index.en.md": (
        None,
        "PostgreSQL articles: EXPLAIN ANALYZE, query optimization, pg_stat_statements, GIN/B-tree indexes, VACUUM, autovacuum, ROLE, GRANT and best practices.",
    ),
    "content/posts/postgresql/_index.es.md": (
        None,
        "Artículos PostgreSQL: EXPLAIN ANALYZE, optimización de queries, pg_stat_statements, índices GIN/B-tree, VACUUM, autovacuum, ROLE, GRANT y best practices.",
    ),
    "content/posts/postgresql/_index.ro.md": (
        None,
        "Articole PostgreSQL: EXPLAIN ANALYZE, optimizare query-uri, pg_stat_statements, indecși GIN/B-tree, VACUUM, autovacuum, ROLE, GRANT și best practices.",
    ),
    "content/posts/mysql/_index.it.md": (
        None,
        "Articoli MySQL e MariaDB: binary log, Galera Cluster, Group Replication, backup con mysqldump/mydumper, autenticazione, GRANT e pre-upgrade assessment.",
    ),
    "content/posts/mysql/_index.en.md": (
        None,
        "MySQL and MariaDB articles: binary log, Galera Cluster, Group Replication, backup with mysqldump/mydumper, authentication, GRANT and pre-upgrade assessment.",
    ),
    "content/posts/mysql/_index.es.md": (
        None,
        "Artículos MySQL y MariaDB: binary log, Galera Cluster, Group Replication, backup con mysqldump/mydumper, autenticación, GRANT y pre-upgrade assessment.",
    ),
    "content/posts/mysql/_index.ro.md": (
        None,
        "Articole MySQL și MariaDB: binary log, Galera Cluster, Group Replication, backup cu mysqldump/mydumper, autentificare, GRANT și pre-upgrade assessment.",
    ),
    "content/posts/data-warehouse/_index.it.md": (
        None,
        "Articoli Data Warehouse: modellazione dimensionale Kimball, SCD Tipo 2, fact table grain, bus matrix, range partitioning, ragged hierarchy ed ETL pratici.",
    ),
    "content/posts/data-warehouse/_index.en.md": (
        None,
        "Data Warehouse articles: Kimball dimensional modeling, SCD Type 2, fact table grain, bus matrix, range partitioning, ragged hierarchy and practical ETL.",
    ),
    "content/posts/data-warehouse/_index.es.md": (
        None,
        "Artículos Data Warehouse: modelado dimensional Kimball, SCD Tipo 2, fact table grain, bus matrix, range partitioning, ragged hierarchy y ETL prácticos.",
    ),
    "content/posts/data-warehouse/_index.ro.md": (
        None,
        "Articole Data Warehouse: modelare dimensională Kimball, SCD Tip 2, fact table grain, bus matrix, range partitioning, ragged hierarchy și ETL practici.",
    ),
    "content/posts/project-management/_index.it.md": (
        None,
        "Articoli Project Management IT: Scrum, standup meeting, smart working, AI Manager, gestione team, freelance e consulenza IT. Casi reali da 30 anni.",
    ),
    "content/posts/project-management/_index.en.md": (
        None,
        "IT Project Management articles: Scrum, standup meetings, smart working, AI Manager, team management, freelance and IT consulting. Real cases from 30 years.",
    ),
    "content/posts/project-management/_index.es.md": (
        None,
        "Artículos Project Management IT: Scrum, standup meetings, smart working, AI Manager, gestión de equipos, freelance y consultoría IT. Casos reales de 30 años.",
    ),
    "content/posts/project-management/_index.ro.md": (
        None,
        "Articole Project Management IT: Scrum, standup meetings, smart working, AI Manager, management echipe, freelance și consultanță IT. Cazuri reale din 30 ani.",
    ),
    # ===== ABOUT (4 lingue) =====
    "content/about.it.md": (
        None,
        "Ivan Luminaria: 30 anni di esperienza come DBA Oracle, PostgreSQL e DWH Architect. Specialista in performance tuning, alta disponibilità e sicurezza database.",
    ),
    "content/about.en.md": (
        None,
        "Ivan Luminaria: 30 years of experience as Oracle/PostgreSQL DBA and DWH Architect. Specialist in performance tuning, high availability and database security.",
    ),
    "content/about.es.md": (
        None,
        "Ivan Luminaria: 30 años de experiencia como DBA Oracle, PostgreSQL y DWH Architect. Especialista en performance tuning, alta disponibilidad y seguridad DB.",
    ),
    "content/about.ro.md": (
        None,
        "Ivan Luminaria: 30 ani de experiență ca DBA Oracle, PostgreSQL și DWH Architect. Specialist în performance tuning, înaltă disponibilitate și securitate DB.",
    ),
    # ===== RESUMES INDEX (4 lingue) =====
    "content/resumes/_index.it.md": (
        None,
        "Know-How e Impatto di Ivan Luminaria: i 4 profili professionali — DWH Architect, Oracle DBA, Oracle PL/SQL Developer, Project Manager Scrum/Agile.",
    ),
    "content/resumes/_index.en.md": (
        None,
        "Ivan Luminaria's Know-How and Impact: the 4 professional profiles — DWH Architect, Oracle DBA, Oracle PL/SQL Developer, Scrum/Agile Project Manager.",
    ),
    "content/resumes/_index.es.md": (
        None,
        "Know-How e Impacto de Ivan Luminaria: los 4 perfiles profesionales — DWH Architect, Oracle DBA, Oracle PL/SQL Developer, Project Manager Scrum/Agile.",
    ),
    "content/resumes/_index.ro.md": (
        None,
        "Know-How și Impact Ivan Luminaria: cele 4 profiluri profesionale — DWH Architect, Oracle DBA, Oracle PL/SQL Developer, Project Manager Scrum/Agile.",
    ),
    # ===== RESUMES SUBPAGES (4 ruoli × 4 lingue) =====
    "content/resumes/dwh-architect/index.it.md": (
        None,
        "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 anni di progettazione DWH, modellazione dimensionale Kimball, ETL e architetture analitiche.",
    ),
    "content/resumes/dwh-architect/index.en.md": (
        None,
        "Ivan Luminaria, Oracle/PostgreSQL Data Warehouse Architect: 30 years of DWH design, Kimball dimensional modeling, ETL and analytical architecture.",
    ),
    "content/resumes/dwh-architect/index.es.md": (
        None,
        "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 años de diseño DWH, modelado dimensional Kimball, ETL y arquitectura analítica.",
    ),
    "content/resumes/dwh-architect/index.ro.md": (
        None,
        "Ivan Luminaria, Data Warehouse Architect Oracle/PostgreSQL: 30 ani de proiectare DWH, modelare dimensională Kimball, ETL și arhitectură analitică.",
    ),
    "content/resumes/oracle-dba/index.it.md": (
        None,
        "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 anni in amministrazione database mission-critical, RAC, Data Guard, AWR/ASH e cloud migration.",
    ),
    "content/resumes/oracle-dba/index.en.md": (
        None,
        "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 years administering mission-critical databases, RAC, Data Guard, AWR/ASH and cloud migration.",
    ),
    "content/resumes/oracle-dba/index.es.md": (
        None,
        "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 años administrando bases de datos mission-critical, RAC, Data Guard, AWR/ASH y cloud migration.",
    ),
    "content/resumes/oracle-dba/index.ro.md": (
        None,
        "Ivan Luminaria, Oracle DBA & Performance Tuning Expert: 30 ani administrând baze de date mission-critical, RAC, Data Guard, AWR/ASH și cloud migration.",
    ),
    "content/resumes/oracle-plsql/index.it.md": (
        None,
        "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning: 30 anni in sviluppo, refactoring e ottimizzazione PL/SQL per applicazioni data-intensive enterprise.",
    ),
    "content/resumes/oracle-plsql/index.en.md": (
        None,
        "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning: 30 years developing, refactoring and optimizing PL/SQL code for enterprise data-intensive apps.",
    ),
    "content/resumes/oracle-plsql/index.es.md": (
        None,
        "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning: 30 años desarrollando y optimizando código PL/SQL para apps data-intensive enterprise.",
    ),
    "content/resumes/oracle-plsql/index.ro.md": (
        None,
        "Ivan Luminaria, Oracle PL/SQL Developer & SQL Tuning: 30 ani dezvoltând și optimizând cod PL/SQL pentru aplicații enterprise data-intensive.",
    ),
    "content/resumes/project-manager/index.it.md": (
        None,
        "Ivan Luminaria, Project Manager Scrum/Agile IT: 30 anni di gestione progetti software con solido background tecnico Oracle e Data Warehouse. Casi reali.",
    ),
    "content/resumes/project-manager/index.en.md": (
        None,
        "Ivan Luminaria, Scrum/Agile IT Project Manager: 30 years managing software projects with solid Oracle and Data Warehouse technical background. Real cases.",
    ),
    "content/resumes/project-manager/index.es.md": (
        None,
        "Ivan Luminaria, Project Manager Scrum/Agile IT: 30 años gestionando proyectos software con sólido background técnico Oracle y Data Warehouse. Casos reales.",
    ),
    "content/resumes/project-manager/index.ro.md": (
        None,
        "Ivan Luminaria, Project Manager Scrum/Agile IT: 30 ani gestionând proiecte software cu fundament tehnic solid Oracle și Data Warehouse. Cazuri reale.",
    ),
    # ===== GLOSSARY INDEX (4 lingue) - seoTitle + desc updated -=====
    "content/glossary/_index.it.md": (
        "Glossario Database e Project Management: termini tecnici",
        "Glossario Database Strategy: centinaia di termini su Oracle, PostgreSQL, MySQL, data warehouse e project management con definizioni e articoli correlati.",
    ),
    "content/glossary/_index.en.md": (
        "Database and Project Management Glossary: tech terms",
        "Database Strategy glossary: hundreds of terms on Oracle, PostgreSQL, MySQL, data warehouse and project management with definitions and related articles.",
    ),
    "content/glossary/_index.es.md": (
        "Glosario Database y Project Management: términos técnicos",
        "Glosario Database Strategy: cientos de términos sobre Oracle, PostgreSQL, MySQL, data warehouse y project management con definiciones y artículos relacionados.",
    ),
    "content/glossary/_index.ro.md": (
        "Glosar Database și Project Management: termeni tehnici",
        "Glosar Database Strategy: sute de termeni despre Oracle, PostgreSQL, MySQL, data warehouse și management de proiect cu definiții și articole relevante.",
    ),
}

# Home (TOML config): {toml_path: new_description}
HOME_DESCRIPTIONS = {
    "config/_default/languages.it.toml":
        "Ivan Luminaria, DBA Oracle/PostgreSQL, DWH Architect e PM. Blog tecnico Database Strategy con articoli pratici da 30 anni di consulenza IT.",
    "config/_default/languages.en.toml":
        "Ivan Luminaria, Oracle/PostgreSQL DBA, DWH Architect and PM. Database Strategy blog with hands-on articles from 30 years of IT consulting.",
    "config/_default/languages.es.toml":
        "Ivan Luminaria, DBA Oracle/PostgreSQL, DWH Architect y PM. Blog técnico Database Strategy con artículos prácticos de 30 años de consultoría IT.",
    "config/_default/languages.ro.toml":
        "Ivan Luminaria, DBA Oracle/PostgreSQL, DWH Architect și PM. Blog tehnic Database Strategy cu articole practice din 30 ani de consultanță IT.",
}


def escape_yaml_str(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def escape_toml_str(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def process_md(path_str: str, seo_title, description: str) -> tuple[bool, str]:
    path = Path(path_str)
    if not path.exists():
        return False, f"FILE NOT FOUND: {path}"

    text = path.read_text(encoding="utf-8")
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    # Replace description
    desc_pattern = re.compile(r'^description:\s*"[^"]*"\s*$', re.MULTILINE)
    new_desc_line = f'description: "{escape_yaml_str(description)}"'
    new_text, n_desc = desc_pattern.subn(new_desc_line, text, count=1)
    if n_desc != 1:
        return False, f"description not matched in {path}"
    text = new_text

    # Optionally replace seoTitle
    if seo_title is not None:
        if re.search(r'^seoTitle:', text, re.MULTILINE):
            seo_pattern = re.compile(r'^seoTitle:\s*"[^"]*"\s*$', re.MULTILINE)
            new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
            new_text, n_seo = seo_pattern.subn(new_seo_line, text, count=1)
            if n_seo != 1:
                return False, f"seoTitle existed but not matched in {path}"
            text = new_text
        else:
            title_pattern = re.compile(r'(^title:\s*"[^"]*"\s*$)', re.MULTILINE)
            new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
            new_text, n_title = title_pattern.subn(
                r"\1\n" + new_seo_line, text, count=1
            )
            if n_title != 1:
                return False, f"title not found in {path}"
            text = new_text

    path.write_text(text, encoding="utf-8")
    return True, f"OK: {path}"


def process_toml(path_str: str, description: str) -> tuple[bool, str]:
    """Add or update params.description in a language TOML file."""
    path = Path(path_str)
    if not path.exists():
        return False, f"FILE NOT FOUND: {path}"

    text = path.read_text(encoding="utf-8")
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    # Look for existing 'description = "..."' in [params] block
    # Strategy: find the [params] section header, then look for 'description = "..."' within it
    new_desc_line = f'  description = "{escape_toml_str(description)}"'

    # If there's already a 'description = "..."' line (anywhere in the file, simple match)
    pattern = re.compile(r'^\s*description\s*=\s*"[^"]*"\s*$', re.MULTILINE)
    if pattern.search(text):
        new_text = pattern.sub(new_desc_line, text, count=1)
    else:
        # Insert after [params] header (with 2 spaces indent matching surrounding)
        params_pattern = re.compile(r'(^\[params\]\s*$)', re.MULTILINE)
        m = params_pattern.search(text)
        if not m:
            return False, f"[params] section not found in {path}"
        # Insert right after [params] line
        new_text = params_pattern.sub(r"\1\n" + new_desc_line, text, count=1)

    path.write_text(new_text, encoding="utf-8")
    return True, f"OK: {path}"


def main():
    ok = 0
    fail = 0

    # Markdown pages
    for path_str, (seo_title, description) in PAGES.items():
        success, msg = process_md(path_str, seo_title, description)
        if success:
            ok += 1
            print(f"  ✓ {msg}")
        else:
            fail += 1
            print(f"  ✗ {msg}", file=sys.stderr)

    # TOML home configs
    for path_str, description in HOME_DESCRIPTIONS.items():
        success, msg = process_toml(path_str, description)
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
