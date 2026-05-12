#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to Project Management section articles (issue #89).
Modifies frontmatter of 9 articles × 4 languages = 36 files.
Creates .bak backup of each file before writing.
"""
import re
from pathlib import Path
import sys

UPDATES = {
    # ----- 1. 4-milioni-nessun-software -----
    ("4-milioni-nessun-software", "it"): (
        "Fallimento progetto IT: 4 milioni e zero software",
        "Project management caso reale: cliente assicurativo spende 4 milioni in consulenza IT e ottiene zero software funzionante. Lezioni di vendor lock-in.",
    ),
    ("4-milioni-nessun-software", "en"): (
        "IT project failure: 4 million euros and zero software",
        "Real project management case: insurance client spends 4 million euros on IT consulting and gets zero working software. Vendor lock-in lessons.",
    ),
    ("4-milioni-nessun-software", "es"): (
        "Fracaso proyecto IT: 4 millones y cero software",
        "Caso real de gestión de proyectos: cliente asegurador gasta 4 millones en consultoría IT y obtiene cero software funcionando. Lecciones vendor lock-in.",
    ),
    ("4-milioni-nessun-software", "ro"): (
        "Eșec proiect IT: 4 milioane de euro și zero software",
        "Caz real management proiect: client asigurări cheltuie 4 milioane în consultanță IT și obține zero software funcțional. Lecții vendor lock-in.",
    ),
    # ----- 2. ai-github-project-management -----
    ("ai-github-project-management", "it"): (
        "Project management con AI e GitHub: workflow ordinato",
        "Project management con AI e GitHub: trasformare un progetto caotico in workflow misurabile con issue tracking, code review e intelligenza artificiale.",
    ),
    ("ai-github-project-management", "en"): (
        "Project management with AI and GitHub: ordered workflow",
        "Project management with AI and GitHub: turning a chaotic project into a measurable workflow with issue tracking, code review and artificial intelligence.",
    ),
    ("ai-github-project-management", "es"): (
        "Gestión proyectos con AI y GitHub: workflow ordenado",
        "Gestión de proyectos con AI y GitHub: transformar un proyecto caótico en workflow medible con issue tracking, code review e inteligencia artificial.",
    ),
    ("ai-github-project-management", "ro"): (
        "Management proiect cu AI și GitHub: workflow ordonat",
        "Management proiect cu AI și GitHub: transformarea unui proiect haotic în workflow măsurabil cu issue tracking, code review și inteligență artificială.",
    ),
    # ----- 3. ai-manager-project-management -----
    ("ai-manager-project-management", "it"): (
        "AI Manager: il ruolo che governa l'AI nei progetti",
        "AI Manager: il ruolo che governa l'impatto dell'intelligenza artificiale su architetture, processi e persone. Riflessioni da 30 anni di IT.",
    ),
    ("ai-manager-project-management", "en"): (
        "AI Manager: the role that governs AI in projects",
        "AI Manager: the professional role that governs the impact of artificial intelligence on architectures, processes and people. Reflections from 30 years in IT.",
    ),
    ("ai-manager-project-management", "es"): (
        "AI Manager: el rol que gobierna la IA en los proyectos",
        "AI Manager: el rol que gobierna el impacto de la inteligencia artificial sobre arquitecturas, procesos y personas. Reflexiones desde 30 años en IT.",
    ),
    ("ai-manager-project-management", "ro"): (
        "AI Manager: rolul care guvernează AI în proiecte",
        "AI Manager: rolul care guvernează impactul inteligenței artificiale asupra arhitecturilor, proceselor și oamenilor. Reflecții din 30 ani de IT.",
    ),
    # ----- 4. bici-vs-auto-roma -----
    ("bici-vs-auto-roma", "it"): (
        "Bici elettrica vs auto a Roma: pendolarismo a confronto",
        "Pendolarismo Roma: bici elettrica Brompton vs auto. 18 minuti vs 50, 35€ di parcheggio risparmiati. La scelta di mobilità sostenibile, dati reali.",
    ),
    ("bici-vs-auto-roma", "en"): (
        "E-bike vs car in Rome: real commuting comparison",
        "Commuting in Rome: electric Brompton vs car. 18 minutes vs 50, €35 of parking saved per day. The sustainable mobility choice from a practical view.",
    ),
    ("bici-vs-auto-roma", "es"): (
        "Bici eléctrica vs coche en Roma: pendolarismo",
        "Pendolarismo en Roma: Brompton eléctrica vs coche. 18 minutos vs 50, 35€ de aparcamiento ahorrados. La elección de movilidad sostenible, datos reales.",
    ),
    ("bici-vs-auto-roma", "ro"): (
        "Bicicletă electrică vs mașină la Roma: pendulare",
        "Pendulare în Roma: Brompton electrică vs mașină. 18 minute vs 50, 35€ de parcare economisiți. Alegerea mobilității sustenabile, date reale.",
    ),
    # ----- 5. pagamenti-60-90-120-giorni -----
    ("pagamenti-60-90-120-giorni", "it"): (
        "Pagamenti 60-90-120 giorni: Italia vs Europa",
        "Pagamenti a 60-90-120 giorni nella consulenza IT italiana: confronto con le regole europee. DSO, direttiva 2011/7/UE e strategie per freelance.",
    ),
    ("pagamenti-60-90-120-giorni", "en"): (
        "Payment terms 60-90-120 days: Italy vs Europe",
        "60-90-120 day payment terms in Italian IT consulting: comparison with European rules. DSO, EU directive 2011/7 and strategies for IT freelancers.",
    ),
    ("pagamenti-60-90-120-giorni", "es"): (
        "Pagos 60-90-120 días: Italia vs Europa",
        "Pagos a 60-90-120 días en consultoría IT italiana: comparación con las reglas europeas. DSO, directiva 2011/7/UE y estrategias para freelancers IT.",
    ),
    ("pagamenti-60-90-120-giorni", "ro"): (
        "Plăți 60-90-120 zile: Italia vs Europa",
        "Plăți la 60-90-120 zile în consultanța IT italiană: comparație cu regulile europene. DSO, directiva 2011/7/UE și strategii pentru freelanceri IT.",
    ),
    # ----- 6. smartworking-consulenza-it -----
    ("smartworking-consulenza-it", "it"): (
        "Smart working consulenza IT: i numeri reali",
        "Smart working nella consulenza IT: analisi economica e strategica del lavoro da remoto. Numeri reali, KPI, presenteismo e produttività vs ufficio.",
    ),
    ("smartworking-consulenza-it", "en"): (
        "Smart working in IT consulting: the real numbers",
        "Smart working in IT consulting: economic and strategic analysis of remote work. Real numbers, KPIs, presenteeism and productivity compared to in-office.",
    ),
    ("smartworking-consulenza-it", "es"): (
        "Smart working en consultoría IT: números reales",
        "Smart working en consultoría IT: análisis económico y estratégico del trabajo remoto. Números reales, KPIs, presenteísmo y productividad vs oficina.",
    ),
    ("smartworking-consulenza-it", "ro"): (
        "Smart working în consultanța IT: cifrele reale",
        "Smart working în consultanța IT: analiză economică și strategică a muncii la distanță. Cifre reale, KPI, prezenteism și productivitate vs birou.",
    ),
    # ----- 7. standup-meeting-15-minuti -----
    ("standup-meeting-15-minuti", "it"): (
        "Standup meeting Scrum: i 15 minuti che li fanno funzionare",
        "Standup meeting Scrum: perché solo i 15 minuti li fanno funzionare. Timeboxing, parking lot, regole pratiche del daily meeting che reggono nel tempo.",
    ),
    ("standup-meeting-15-minuti", "en"): (
        "Scrum standup meetings: 15 minutes that make them work",
        "Scrum standup meetings: why only the 15-minute constraint makes them work. Timeboxing, parking lot and daily meeting rules that hold up over time.",
    ),
    ("standup-meeting-15-minuti", "es"): (
        "Standup meeting Scrum: los 15 minutos que funcionan",
        "Standup meeting Scrum: por qué solo los 15 minutos los hacen funcionar. Timeboxing, parking lot y reglas prácticas del daily meeting que aguantan.",
    ),
    ("standup-meeting-15-minuti", "ro"): (
        "Standup meeting Scrum: 15 minute care funcționează",
        "Standup meeting Scrum: de ce doar 15 minute le fac să funcționeze. Timeboxing, parking lot și reguli practice ale daily meeting care rezistă în timp.",
    ),
    # ----- 8. team-di-progetto-che-reggono -----
    ("team-di-progetto-che-reggono", "it"): (
        "Project management: 5 regole per team che reggono",
        "Project management: 5 regole osservate nei team che reggono sotto pressione. Psychological safety, bus factor, outcome vs output, knowledge transfer.",
    ),
    ("team-di-progetto-che-reggono", "en"): (
        "Project management: 5 rules for teams that hold",
        "Project management: 5 rules observed in teams that hold under pressure. Psychological safety, bus factor, outcome vs output, knowledge transfer.",
    ),
    ("team-di-progetto-che-reggono", "es"): (
        "Gestión proyectos: 5 reglas para equipos que aguantan",
        "Gestión de proyectos: 5 reglas observadas en equipos que aguantan bajo presión. Psychological safety, bus factor, outcome vs output, knowledge transfer.",
    ),
    ("team-di-progetto-che-reggono", "ro"): (
        "Management proiect: 5 reguli pentru echipe care rezistă",
        "Management proiect: 5 reguli observate în echipele care rezistă sub presiune. Psychological safety, bus factor, outcome vs output, knowledge transfer.",
    ),
    # ----- 9. tecnica-si-e-yes-and -----
    ("tecnica-si-e-yes-and", "it"): (
        "Tecnica Yes-And: gestione conflitti nei team IT",
        "La tecnica Yes-And dal teatro di improvvisazione applicata alla gestione dei conflitti nei team IT. Caso reale di riunione che stava degenerando.",
    ),
    ("tecnica-si-e-yes-and", "en"): (
        "Yes-And technique: conflict management in IT teams",
        "The Yes-And technique from improvisational theatre applied to conflict management in IT teams. Real case of a meeting that was about to blow up.",
    ),
    ("tecnica-si-e-yes-and", "es"): (
        "Técnica Yes-And: gestión de conflictos en equipos IT",
        "La técnica Yes-And del teatro de improvisación aplicada a la gestión de conflictos en equipos IT. Caso real de una reunión que iba a estallar.",
    ),
    ("tecnica-si-e-yes-and", "ro"): (
        "Tehnica Yes-And: gestionare conflicte în echipe IT",
        "Tehnica Yes-And din teatrul de improvizație aplicată la gestionarea conflictelor în echipe IT. Caz real al unei ședințe ce era pe punctul de a exploda.",
    ),
}

BASE = Path("content/posts/project-management")


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
