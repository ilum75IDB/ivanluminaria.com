#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to Data Warehouse section articles (issue #89).
Modifies frontmatter of 5 articles × 4 languages = 20 files.
Creates .bak backup of each file before writing.
"""
import re
from pathlib import Path
import sys

UPDATES = {
    # ----- 1. bus-matrix-terreno-comune -----
    ("bus-matrix-terreno-comune", "it"): (
        "Bus matrix Kimball: data mart e conformed dimensions",
        "Bus matrix di Kimball per allineare data mart isolati: dimensioni conformi, processi di business e vendite confrontabili. Caso reale gruppo assicurativo.",
    ),
    ("bus-matrix-terreno-comune", "en"): (
        "Kimball bus matrix: data marts and conformed dimensions",
        "Kimball bus matrix to align isolated data marts: conformed dimensions, business processes and comparable sales. Real insurance group case.",
    ),
    ("bus-matrix-terreno-comune", "es"): (
        "Bus matrix Kimball: data marts y conformed dimensions",
        "Bus matrix de Kimball para alinear data marts aislados: conformed dimensions, procesos de negocio y ventas comparables. Caso real grupo asegurador.",
    ),
    ("bus-matrix-terreno-comune", "ro"): (
        "Bus matrix Kimball: data marts și conformed dimensions",
        "Bus matrix Kimball pentru alinierea data marts izolate: conformed dimensions, procese de business și vânzări comparabile. Caz real grup asigurări.",
    ),
    # ----- 2. fatto-grana-sbagliata -----
    ("fatto-grana-sbagliata", "it"): (
        "Data warehouse: la grana della fact table",
        "Data warehouse: la grana della fact table determina quali domande puoi rispondere. Errori frequenti nella granularità e impatto sul modello dimensionale.",
    ),
    ("fatto-grana-sbagliata", "en"): (
        "Data warehouse: fact table grain explained",
        "Data warehouse: fact table grain determines which questions you can answer. Common mistakes in granularity and their impact on the dimensional model.",
    ),
    ("fatto-grana-sbagliata", "es"): (
        "Data warehouse: la granularidad de la fact table",
        "Data warehouse: la granularidad de la fact table determina qué preguntas puedes responder. Errores frecuentes y su impacto en el modelo dimensional.",
    ),
    ("fatto-grana-sbagliata", "ro"): (
        "Data warehouse: granularitatea fact table",
        "Data warehouse: granularitatea fact table determină ce întrebări poți răspunde. Greșeli frecvente în granularitate și impactul pe modelul dimensional.",
    ),
    # ----- 3. partitioning-dwh -----
    ("partitioning-dwh", "it"): (
        "DWH partitioning: range partitioning su fact table",
        "Range partitioning su fact table da 800 milioni di righe: da query trimestrali di 12 minuti a 40 secondi. Implementazione mensile, exchange e indici locali.",
    ),
    ("partitioning-dwh", "en"): (
        "DWH partitioning: range partitioning on fact tables",
        "Range partitioning on an 800-million-row fact table: from 12-minute quarterly queries to 40 seconds. Monthly implementation, exchange and local indexes.",
    ),
    ("partitioning-dwh", "es"): (
        "Partitioning DWH: range partitioning en fact table",
        "Range partitioning en fact table de 800M filas: de queries trimestrales de 12 minutos a 40 segundos. Implementación mensual, exchange e índices locales.",
    ),
    ("partitioning-dwh", "ro"): (
        "DWH partitioning: range partitioning pe fact table",
        "Range partitioning pe fact table de 800 milioane rânduri: de la query-uri trimestriale de 12 minute la 40 de secunde. Implementare lunară, exchange.",
    ),
    # ----- 4. ragged-hierarchies -----
    ("ragged-hierarchies", "it"): (
        "Ragged hierarchy: gerarchie sbilanciate con self-parenting",
        "Ragged hierarchy nel data warehouse: bilanciamento di gerarchie sbilanciate con la tecnica del self-parenting. Drill-down corretto su clienti e gruppi.",
    ),
    ("ragged-hierarchies", "en"): (
        "Ragged hierarchy: unbalanced trees with self-parenting",
        "Ragged hierarchy in the data warehouse: balancing unbalanced trees with the self-parenting technique. Correct drill-down on customers and groups.",
    ),
    ("ragged-hierarchies", "es"): (
        "Ragged hierarchy: jerarquías desbalanceadas y self-parenting",
        "Ragged hierarchy en data warehouse: balanceo de jerarquías desbalanceadas con la técnica de self-parenting. Drill-down correcto en clientes y grupos.",
    ),
    ("ragged-hierarchies", "ro"): (
        "Ragged hierarchy: ierarhii dezechilibrate cu self-parenting",
        "Ragged hierarchy în data warehouse: echilibrarea ierarhiilor dezechilibrate cu tehnica self-parenting. Drill-down corect pe clienți și grupuri.",
    ),
    # ----- 5. scd-tipo-2 -----
    ("scd-tipo-2", "it"): (
        "SCD Tipo 2: Slowly Changing Dimensions con chiavi surrogate",
        "SCD Tipo 2 nel data warehouse: storicizzare dimensioni con chiavi surrogate e date di validità. Caso reale: dimensione clienti che evolve nel tempo.",
    ),
    ("scd-tipo-2", "en"): (
        "SCD Type 2: Slowly Changing Dimensions with surrogate keys",
        "SCD Type 2 in the data warehouse: historicising dimensions with surrogate keys and validity dates. Real case: a customer dimension that evolves over time.",
    ),
    ("scd-tipo-2", "es"): (
        "SCD Tipo 2: Slowly Changing Dimensions con claves subrogadas",
        "SCD Tipo 2 en data warehouse: historizar dimensiones con claves subrogadas y fechas de validez. Caso real: dimensión clientes que evoluciona en el tiempo.",
    ),
    ("scd-tipo-2", "ro"): (
        "SCD Tip 2: Slowly Changing Dimensions cu chei surogat",
        "SCD Tip 2 în data warehouse: istorizare dimensiuni cu chei surogat și date de valabilitate. Caz real: dimensiune clienți care evoluează în timp.",
    ),
}

BASE = Path("content/posts/data-warehouse")


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
