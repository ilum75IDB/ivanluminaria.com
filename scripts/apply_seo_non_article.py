#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to non-article pages (issue #89).
Covers: section index (5x4=20), about (4), resumes (5x4=20), glossary index (4).
Total: 48 files.
"""
import re
from pathlib import Path
import sys

# (path, lang): (seoTitle, description_override_or_None)
# If description is None, the existing one is kept (only seoTitle is added).
UPDATES = {
    # ===== SECTION INDEX =====
    # /posts/ (Database Strategy main section)
    ("content/posts/_index.it.md", "it"): (
        "Database Strategy: blog Ivan Luminaria su DB e architettura",
        None,
    ),
    ("content/posts/_index.en.md", "en"): (
        "Database Strategy: Ivan Luminaria's blog on DB and architecture",
        None,
    ),
    ("content/posts/_index.es.md", "es"): (
        "Database Strategy: blog de Ivan Luminaria sobre DB y arquitectura",
        None,
    ),
    ("content/posts/_index.ro.md", "ro"): (
        "Database Strategy: blogul Ivan Luminaria pe DB și arhitectură",
        None,
    ),
    # /posts/oracle/
    ("content/posts/oracle/_index.it.md", "it"): (
        "Oracle Database: articoli su DBA, performance, tuning",
        None,
    ),
    ("content/posts/oracle/_index.en.md", "en"): (
        "Oracle Database: DBA, performance and tuning articles",
        None,
    ),
    ("content/posts/oracle/_index.es.md", "es"): (
        "Oracle Database: artículos sobre DBA, rendimiento, tuning",
        None,
    ),
    ("content/posts/oracle/_index.ro.md", "ro"): (
        "Oracle Database: articole DBA, performanță, tuning",
        None,
    ),
    # /posts/postgresql/
    ("content/posts/postgresql/_index.it.md", "it"): (
        "PostgreSQL: architettura, performance e tuning",
        None,
    ),
    ("content/posts/postgresql/_index.en.md", "en"): (
        "PostgreSQL: architecture, performance and tuning articles",
        None,
    ),
    ("content/posts/postgresql/_index.es.md", "es"): (
        "PostgreSQL: arquitectura, rendimiento y tuning",
        None,
    ),
    ("content/posts/postgresql/_index.ro.md", "ro"): (
        "PostgreSQL: arhitectură, performanță și tuning",
        None,
    ),
    # /posts/mysql/
    ("content/posts/mysql/_index.it.md", "it"): (
        "MySQL e MariaDB: articoli su performance e sicurezza",
        None,
    ),
    ("content/posts/mysql/_index.en.md", "en"): (
        "MySQL and MariaDB: performance and security articles",
        None,
    ),
    ("content/posts/mysql/_index.es.md", "es"): (
        "MySQL y MariaDB: artículos de rendimiento y seguridad",
        None,
    ),
    ("content/posts/mysql/_index.ro.md", "ro"): (
        "MySQL și MariaDB: articole performanță și securitate",
        None,
    ),
    # /posts/data-warehouse/
    ("content/posts/data-warehouse/_index.it.md", "it"): (
        "Data Warehouse: architettura, modellazione, ETL",
        # desc was 172ch, shorten to be safe under 160
        "Architettura Data Warehouse nella pratica: modellazione dimensionale, gerarchie, ETL e strategie di caricamento. Dai dati al supporto decisionale.",
    ),
    ("content/posts/data-warehouse/_index.en.md", "en"): (
        "Data Warehouse: architecture, modeling, ETL",
        # desc was 164ch
        "Data Warehouse architecture in practice: dimensional modeling, hierarchies, ETL and loading strategies. When data drives decisions, not just operations.",
    ),
    ("content/posts/data-warehouse/_index.es.md", "es"): (
        "Data Warehouse: arquitectura, modelado, ETL",
        # desc was 175ch
        "Arquitectura Data Warehouse en la práctica: modelado dimensional, jerarquías, ETL y estrategias de carga. De los datos al soporte de decisiones.",
    ),
    ("content/posts/data-warehouse/_index.ro.md", "ro"): (
        "Data Warehouse: arhitectură, modelare, ETL",
        # desc was 182ch
        "Arhitectură Data Warehouse în practică: modelare dimensională, ierarhii, ETL și strategii de încărcare. De la date la suport decizional.",
    ),
    # /posts/project-management/
    ("content/posts/project-management/_index.it.md", "it"): (
        "Project Management IT: Scrum, AI, consulenza",
        None,
    ),
    ("content/posts/project-management/_index.en.md", "en"): (
        "IT Project Management: Scrum, AI, consulting",
        None,
    ),
    ("content/posts/project-management/_index.es.md", "es"): (
        "Project Management IT: Scrum, AI, consultoría",
        None,
    ),
    ("content/posts/project-management/_index.ro.md", "ro"): (
        "Project Management IT: Scrum, AI, consultanță",
        None,
    ),
    # ===== ABOUT =====
    ("content/about.it.md", "it"): (
        "Ivan Luminaria: DBA Oracle, PostgreSQL e DWH Architect",
        None,
    ),
    ("content/about.en.md", "en"): (
        "Ivan Luminaria: Oracle/PostgreSQL DBA and DWH Architect",
        None,
    ),
    ("content/about.es.md", "es"): (
        "Ivan Luminaria: DBA Oracle, PostgreSQL y DWH Architect",
        None,
    ),
    ("content/about.ro.md", "ro"): (
        "Ivan Luminaria: DBA Oracle, PostgreSQL și DWH Architect",
        None,
    ),
    # ===== RESUMES INDEX =====
    ("content/resumes/_index.it.md", "it"): (
        "Know-How e Impatto: 30 anni di DBA, DWH e team IT",
        None,
    ),
    ("content/resumes/_index.en.md", "en"): (
        "Know-How and Impact: 30 years of DBA, DWH and IT teams",
        None,
    ),
    ("content/resumes/_index.es.md", "es"): (
        "Know-How e Impacto: 30 años de DBA, DWH y equipos IT",
        # desc was 160ch (borderline) — shorten slightly
        "Treinta años de trabajo en sistemas que no pueden detenerse — bases de datos, data warehouse, equipos. Profundidad técnica e impacto en el negocio.",
    ),
    ("content/resumes/_index.ro.md", "ro"): (
        "Know-How și Impact: 30 ani de DBA, DWH și echipe IT",
        # desc was 159ch (borderline) — shorten slightly
        "Treizeci de ani de muncă pe sisteme care nu se pot opri — baze de date, data warehouse, echipe. Profunzime tehnică și impact pe business.",
    ),
    # ===== RESUMES SUBPAGES =====
    # dwh-architect
    ("content/resumes/dwh-architect/index.it.md", "it"): (
        "Ivan Luminaria | Data Warehouse Architect Oracle/PostgreSQL",
        "Data Warehouse Architect Oracle/PostgreSQL — quasi 30 anni di esperienza nella progettazione e gestione di soluzioni DWH complesse ad alte prestazioni.",
    ),
    ("content/resumes/dwh-architect/index.en.md", "en"): (
        "Ivan Luminaria | Data Warehouse Architect Oracle/PostgreSQL",
        None,
    ),
    ("content/resumes/dwh-architect/index.es.md", "es"): (
        "Ivan Luminaria | Data Warehouse Architect Oracle/PostgreSQL",
        None,
    ),
    ("content/resumes/dwh-architect/index.ro.md", "ro"): (
        "Ivan Luminaria | Data Warehouse Architect Oracle/PostgreSQL",
        "Data Warehouse Architect Oracle/PostgreSQL — aproape 30 de ani de experiență în proiectarea soluțiilor DWH complexe și de înaltă performanță.",
    ),
    # oracle-dba
    ("content/resumes/oracle-dba/index.it.md", "it"): (
        "Ivan Luminaria | Oracle DBA & Performance Tuning Expert",
        "Oracle DBA & Performance Tuning Expert — quasi 30 anni di esperienza in amministrazione, ottimizzazione e gestione di database Oracle mission-critical.",
    ),
    ("content/resumes/oracle-dba/index.en.md", "en"): (
        "Ivan Luminaria | Oracle DBA & Performance Tuning Expert",
        "Oracle DBA & Performance Tuning Expert — nearly 30 years of experience in administration, optimization and management of mission-critical Oracle databases.",
    ),
    ("content/resumes/oracle-dba/index.es.md", "es"): (
        "Ivan Luminaria | Oracle DBA & Performance Tuning Expert",
        "Oracle DBA & Performance Tuning Expert — casi 30 años de experiencia en administración, optimización y gestión de bases de datos Oracle mission-critical.",
    ),
    ("content/resumes/oracle-dba/index.ro.md", "ro"): (
        "Ivan Luminaria | Oracle DBA & Performance Tuning Expert",
        "Oracle DBA & Performance Tuning Expert — aproape 30 de ani de experiență în administrarea și optimizarea bazelor de date Oracle mission-critical.",
    ),
    # oracle-plsql
    ("content/resumes/oracle-plsql/index.it.md", "it"): (
        "Ivan Luminaria | Oracle PL/SQL Developer & SQL Tuning",
        "Oracle PL/SQL Developer & SQL Performance Tuning Expert — quasi 30 anni di esperienza in sviluppo e ottimizzazione di codice PL/SQL data-intensive.",
    ),
    ("content/resumes/oracle-plsql/index.en.md", "en"): (
        "Ivan Luminaria | Oracle PL/SQL Developer & SQL Tuning",
        "Oracle PL/SQL Developer & SQL Performance Tuning Expert — nearly 30 years designing, developing and optimizing robust PL/SQL code for data-intensive apps.",
    ),
    ("content/resumes/oracle-plsql/index.es.md", "es"): (
        "Ivan Luminaria | Oracle PL/SQL Developer & SQL Tuning",
        "Oracle PL/SQL Developer & SQL Performance Tuning Expert — casi 30 años de experiencia en desarrollo y optimización de código PL/SQL data-intensive.",
    ),
    ("content/resumes/oracle-plsql/index.ro.md", "ro"): (
        "Ivan Luminaria | Oracle PL/SQL Developer & SQL Tuning",
        "Oracle PL/SQL Developer & SQL Performance Tuning Expert — aproape 30 de ani de experiență în dezvoltarea și optimizarea codului PL/SQL data-intensive.",
    ),
    # project-manager
    ("content/resumes/project-manager/index.it.md", "it"): (
        "Ivan Luminaria | Project Manager Scrum/Agile in IT",
        None,
    ),
    ("content/resumes/project-manager/index.en.md", "en"): (
        "Ivan Luminaria | Project Manager Scrum/Agile in IT",
        None,
    ),
    ("content/resumes/project-manager/index.es.md", "es"): (
        "Ivan Luminaria | Project Manager Scrum/Agile en IT",
        None,
    ),
    ("content/resumes/project-manager/index.ro.md", "ro"): (
        "Ivan Luminaria | Project Manager Scrum/Agile în IT",
        None,
    ),
    # ===== GLOSSARY INDEX =====
    ("content/glossary/_index.it.md", "it"): (
        "Glossario Database e Project Management: 150+ termini tecnici",
        "Glossario di termini tecnici e acronimi su database, data warehouse e project management. Ogni voce include definizione e link agli articoli correlati.",
    ),
    ("content/glossary/_index.en.md", "en"): (
        "Database and Project Management Glossary: 150+ tech terms",
        "Glossary of technical terms and acronyms on databases, data warehousing and project management. Each entry includes a clear definition and related articles.",
    ),
    ("content/glossary/_index.es.md", "es"): (
        "Glosario Database y Project Management: 150+ términos técnicos",
        "Glosario de términos técnicos y acrónimos de bases de datos, data warehouse y gestión de proyectos. Cada entrada incluye definición y artículos relacionados.",
    ),
    ("content/glossary/_index.ro.md", "ro"): (
        "Glosar Database și Project Management: 150+ termeni tehnici",
        "Glosar de termeni tehnici și acronime din baze de date, data warehouse și management de proiect. Fiecare intrare include definiție și articole relevante.",
    ),
}


def escape_yaml_str(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def process_file(path_str: str, seo_title: str, description) -> tuple[bool, str]:
    path = Path(path_str)
    if not path.exists():
        return False, f"FILE NOT FOUND: {path}"

    text = path.read_text(encoding="utf-8")
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    # 1) Optionally replace description
    if description is not None:
        desc_pattern = re.compile(r'^description:\s*"[^"]*"\s*$', re.MULTILINE)
        new_desc_line = f'description: "{escape_yaml_str(description)}"'
        new_text, n_desc = desc_pattern.subn(new_desc_line, text, count=1)
        if n_desc != 1:
            return False, f"description line not matched: {path}"
        text = new_text

    # 2) Insert/replace seoTitle
    if re.search(r'^seoTitle:', text, re.MULTILINE):
        seo_pattern = re.compile(r'^seoTitle:\s*"[^"]*"\s*$', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_seo = seo_pattern.subn(new_seo_line, text, count=1)
        if n_seo != 1:
            return False, f"seoTitle existed but not matched: {path}"
        text = new_text
    else:
        title_pattern = re.compile(r'(^title:\s*"[^"]*"\s*$)', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_title = title_pattern.subn(
            r"\1\n" + new_seo_line, text, count=1
        )
        if n_title != 1:
            return False, f"title line not found: {path}"
        text = new_text

    path.write_text(text, encoding="utf-8")
    return True, f"OK: {path}"


def main():
    ok = 0
    fail = 0
    for (path_str, lang), (seo_title, description) in UPDATES.items():
        success, msg = process_file(path_str, seo_title, description)
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
