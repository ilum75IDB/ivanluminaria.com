#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to Oracle section articles (issue #89).
Modifies frontmatter of 6 articles × 4 languages = 24 files.
Creates .bak backup of each file before writing.
"""
import re
from pathlib import Path
import sys

# (slug, lang): (seoTitle, description)
UPDATES = {
    # ----- 1. oracle-data-guard -----
    ("oracle-data-guard", "it"): (
        "Oracle Data Guard 19c: caso reale DR e switchover automatico",
        "Oracle Data Guard 19c: migrazione da single instance dopo un crash di 6 ore. Architettura DR, primary/standby, switchover automatico.",
    ),
    ("oracle-data-guard", "en"): (
        "Oracle Data Guard 19c: real DR case with automatic switchover",
        "Oracle Data Guard 19c: migration from single instance after a 6-hour outage. DR architecture, primary/standby, automatic switchover.",
    ),
    ("oracle-data-guard", "es"): (
        "Oracle Data Guard 19c: caso real DR y switchover automático",
        "Oracle Data Guard 19c: migración desde single instance tras una caída de 6 horas. Arquitectura DR, primary/standby, switchover automático.",
    ),
    ("oracle-data-guard", "ro"): (
        "Oracle Data Guard 19c: caz real DR cu switchover automat",
        "Oracle Data Guard 19c: migrare de la single instance după 6 ore de downtime. Arhitectură DR, primary/standby, switchover automat real.",
    ),
    # ----- 2. oracle-partitioning -----
    ("oracle-partitioning", "it"): (
        "Oracle Partitioning: range, interval e partition pruning",
        "Oracle Partitioning su tabella da 2 miliardi di righe: range, interval, partition pruning, indici locali. Da ore a secondi sulle query.",
    ),
    ("oracle-partitioning", "en"): (
        "Oracle Partitioning: range, interval and partition pruning",
        "Oracle Partitioning on a 2-billion-row table: range, interval, partition pruning, local indexes. From hours to seconds on reporting queries.",
    ),
    ("oracle-partitioning", "es"): (
        "Oracle Partitioning: range, interval y partition pruning",
        "Oracle Partitioning en tabla de 2 mil millones de filas: range, interval, partition pruning, índices locales. De horas a segundos.",
    ),
    ("oracle-partitioning", "ro"): (
        "Oracle Partitioning: range, interval și partition pruning",
        "Oracle Partitioning pe tabelă de 2 miliarde de rânduri: range, interval, partition pruning, indecși locali. De la ore la secunde.",
    ),
    # ----- 3. oracle-roles-privileges -----
    ("oracle-roles-privileges", "it"): (
        "Oracle ruoli e privilegi: least privilege con SQL reale",
        "Sicurezza Oracle: ridisegno del modello GRANT con ruoli custom e Unified Audit, applicando il least privilege. Caso reale con SQL pronto.",
    ),
    ("oracle-roles-privileges", "en"): (
        "Oracle security: roles, privileges and least privilege",
        "Oracle security: redesigning the GRANT model with custom roles and Unified Audit, applying least privilege. Real case with copy-paste SQL.",
    ),
    ("oracle-roles-privileges", "es"): (
        "Seguridad Oracle: roles, privilegios y mínimo privilegio",
        "Seguridad Oracle: rediseño del modelo GRANT con roles personalizados y Unified Audit, aplicando el mínimo privilegio. Caso real con SQL listo.",
    ),
    ("oracle-roles-privileges", "ro"): (
        "Securitate Oracle: roluri, privilegii și least privilege",
        "Securitate Oracle: redesign al modelului GRANT cu roluri custom și Unified Audit, aplicând least privilege. Caz real cu SQL gata pentru copy-paste.",
    ),
    # ----- 4. oracle-awr-ash -----
    ("oracle-awr-ash", "it"): (
        "Oracle AWR e ASH: diagnosi performance in 10 minuti",
        "Oracle 19c performance tuning con AWR e ASH: trovare un full table scan in una stored procedure in 10 minuti, vigilia di go-live.",
    ),
    ("oracle-awr-ash", "en"): (
        "Oracle AWR and ASH: performance diagnosis in 10 minutes",
        "Oracle 19c performance tuning with AWR and ASH: finding a hidden full table scan in a stored procedure in 10 minutes, the eve of a go-live.",
    ),
    ("oracle-awr-ash", "es"): (
        "Oracle AWR y ASH: diagnóstico de rendimiento en 10 minutos",
        "Tuning Oracle 19c con AWR y ASH: encontrar un full table scan oculto en un procedimiento almacenado en 10 minutos, antes de un go-live.",
    ),
    ("oracle-awr-ash", "ro"): (
        "Oracle AWR și ASH: diagnostic performanță în 10 minute",
        "Tuning Oracle 19c cu AWR și ASH: găsirea unui full table scan ascuns într-o procedură stocată în 10 minute, în ajunul unui go-live.",
    ),
    # ----- 5. oracle-linux-kernel -----
    ("oracle-linux-kernel", "it"): (
        "Oracle su Linux: tuning kernel, Huge Pages e THP",
        "Oracle 19c su Linux: tuning del kernel per performance reali. Huge Pages, THP, swappiness, I/O scheduler, ulimit — numeri prima e dopo.",
    ),
    ("oracle-linux-kernel", "en"): (
        "Oracle on Linux: kernel tuning, Huge Pages and THP",
        "Oracle 19c on Linux: kernel tuning for real performance. Huge Pages, THP, swappiness, I/O scheduler, ulimit — before and after numbers.",
    ),
    ("oracle-linux-kernel", "es"): (
        "Oracle en Linux: tuning del kernel, Huge Pages y THP",
        "Oracle 19c en Linux: tuning del kernel para rendimiento real. Huge Pages, THP, swappiness, I/O scheduler, ulimit — números antes/después.",
    ),
    ("oracle-linux-kernel", "ro"): (
        "Oracle pe Linux: tuning kernel, Huge Pages și THP",
        "Oracle 19c pe Linux: tuning kernel pentru performanță reală. Huge Pages, THP, swappiness, I/O scheduler, ulimit — cifre înainte/după.",
    ),
    # ----- 6. oracle-cloud-migration -----
    ("oracle-cloud-migration", "it"): (
        "Oracle to OCI: migrazione cloud reale con BYOL e Data Guard",
        "Migrazione Oracle 19c on-premises a OCI: 2 TB con RAC e Data Guard. BYOL licensing, Data Pump, cutover notturno — cronaca reale.",
    ),
    ("oracle-cloud-migration", "en"): (
        "Oracle to OCI: real cloud migration with BYOL and Data Guard",
        "Oracle 19c on-premises to OCI migration: 2 TB with RAC and Data Guard. BYOL licensing, Data Pump, overnight cutover — real chronicle.",
    ),
    ("oracle-cloud-migration", "es"): (
        "Oracle a OCI: migración cloud real con BYOL y Data Guard",
        "Migración Oracle 19c on-premises a OCI: 2 TB con RAC y Data Guard. Licensing BYOL, Data Pump, cutover nocturno — crónica real.",
    ),
    ("oracle-cloud-migration", "ro"): (
        "Oracle la OCI: migrare cloud reală cu BYOL și Data Guard",
        "Migrare Oracle 19c on-premises la OCI: 2 TB cu RAC și Data Guard. Licensing BYOL, Data Pump, cutover peste noapte — cronică reală.",
    ),
}

BASE = Path("content/posts/oracle")


def escape_yaml_str(s: str) -> str:
    """Escape a string for inclusion inside YAML double-quotes."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def process_file(slug: str, lang: str, seo_title: str, description: str) -> tuple[bool, str]:
    path = BASE / slug / f"index.{lang}.md"
    if not path.exists():
        return False, f"FILE NOT FOUND: {path}"

    text = path.read_text(encoding="utf-8")

    # Backup before any modification
    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")

    # 1) Replace description line
    desc_pattern = re.compile(r'^description:\s*"[^"]*"\s*$', re.MULTILINE)
    new_desc_line = f'description: "{escape_yaml_str(description)}"'
    new_text, n_desc = desc_pattern.subn(new_desc_line, text, count=1)
    if n_desc != 1:
        return False, f"description line not matched (or matched multiple): {path}"

    # 2) Insert seoTitle right after title (if not already present)
    if re.search(r'^seoTitle:', new_text, re.MULTILINE):
        # Already present: replace
        seo_pattern = re.compile(r'^seoTitle:\s*"[^"]*"\s*$', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_seo = seo_pattern.subn(new_seo_line, new_text, count=1)
        if n_seo != 1:
            return False, f"seoTitle existed but not matched: {path}"
    else:
        # Add new: insert right after title line
        title_pattern = re.compile(r'(^title:\s*"[^"]*"\s*$)', re.MULTILINE)
        new_seo_line = f'seoTitle: "{escape_yaml_str(seo_title)}"'
        new_text, n_title = title_pattern.subn(
            r"\1\n" + new_seo_line, new_text, count=1
        )
        if n_title != 1:
            return False, f"title line not found, cannot insert seoTitle: {path}"

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
