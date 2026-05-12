#!/usr/bin/env python3
"""
Apply SEO seoTitle + description to MySQL section articles (issue #89).
Modifies frontmatter of 8 articles × 4 languages = 32 files.
Creates .bak backup of each file before writing.
"""
import re
from pathlib import Path
import sys

UPDATES = {
    # ----- 1. binary-log-mysql -----
    ("binary-log-mysql", "it"): (
        "MySQL binary log: gestione, retention e PITR",
        "MySQL binary log: gestione, retention e point-in-time recovery. Caso reale di server con disco al 95% e 180 GB di binlog in sei mesi.",
    ),
    ("binary-log-mysql", "en"): (
        "MySQL binary log: management, retention and PITR",
        "MySQL binary log: management, retention and point-in-time recovery. Real case of a server with disk at 95% and 180 GB of binlogs in six months.",
    ),
    ("binary-log-mysql", "es"): (
        "MySQL binary log: gestión, retención y PITR",
        "MySQL binary log: gestión, retención y point-in-time recovery. Caso real de servidor con disco al 95% y 180 GB de binlog en seis meses.",
    ),
    ("binary-log-mysql", "ro"): (
        "MySQL binary log: gestionare, retenție și PITR",
        "MySQL binary log: gestionare, retenție și point-in-time recovery. Caz real de server cu discul la 95% și 180 GB de binlog în șase luni.",
    ),
    # ----- 2. galera-cluster-3-nodi -----
    ("galera-cluster-3-nodi", "it"): (
        "MySQL Galera Cluster 3 nodi: replica sincrona e quorum",
        "MySQL Galera Cluster a 3 nodi per l'alta disponibilità: replica sincrona, quorum, SST/IST. Configurazione completa contro il single point of failure.",
    ),
    ("galera-cluster-3-nodi", "en"): (
        "MySQL Galera Cluster 3-node: sync replication and quorum",
        "3-node MySQL Galera Cluster for high availability: synchronous replication, quorum, SST/IST. Full configuration against single point of failure.",
    ),
    ("galera-cluster-3-nodi", "es"): (
        "MySQL Galera Cluster 3 nodos: replicación síncrona y quórum",
        "MySQL Galera Cluster de 3 nodos para alta disponibilidad: replicación síncrona, quórum, SST/IST. Configuración contra el single point of failure.",
    ),
    ("galera-cluster-3-nodi", "ro"): (
        "MySQL Galera Cluster 3 noduri: replicare sincronă și quorum",
        "MySQL Galera Cluster cu 3 noduri pentru high availability: replicare sincronă, quorum, SST/IST. Configurare împotriva single point of failure.",
    ),
    # ----- 3. mysql-group-replication-binlog-migration -----
    ("mysql-group-replication-binlog-migration", "it"): (
        "MySQL Group Replication: binary log su volume dedicato",
        "MySQL Group Replication a 3 nodi: migrazione dei binary log su volume dedicato senza perdere il quorum. Caso reale con filesystem al 92%.",
    ),
    ("mysql-group-replication-binlog-migration", "en"): (
        "MySQL Group Replication: binary logs on dedicated volume",
        "3-node MySQL Group Replication: migrating binary logs to a dedicated volume without losing quorum. Real case with filesystem at 92%.",
    ),
    ("mysql-group-replication-binlog-migration", "es"): (
        "MySQL Group Replication: binary logs en volumen dedicado",
        "MySQL Group Replication de 3 nodos: migración de binary logs a un volumen dedicado sin perder el quórum. Caso real con filesystem al 92%.",
    ),
    ("mysql-group-replication-binlog-migration", "ro"): (
        "MySQL Group Replication: binary logs pe volum dedicat",
        "MySQL Group Replication cu 3 noduri: migrare binary logs pe un volum dedicat fără pierderea quorum-ului. Caz real cu filesystem la 92%.",
    ),
    # ----- 4. mysql-multi-istanza-secure-file-priv -----
    ("mysql-multi-istanza-secure-file-priv", "it"): (
        "MySQL multi-istanza: secure-file-priv e CSV export",
        "MySQL multi-istanza su Linux: esportare un CSV con INTO OUTFILE bloccato da secure-file-priv. Connessione via socket Unix e workaround dalla shell.",
    ),
    ("mysql-multi-istanza-secure-file-priv", "en"): (
        "MySQL multi-instance: secure-file-priv and CSV export",
        "MySQL multi-instance on Linux: exporting a CSV with INTO OUTFILE blocked by secure-file-priv. Unix socket connection and shell workaround real case.",
    ),
    ("mysql-multi-istanza-secure-file-priv", "es"): (
        "MySQL multi-instancia: secure-file-priv y export CSV",
        "MySQL multi-instancia en Linux: exportar un CSV con INTO OUTFILE bloqueado por secure-file-priv. Conexión por socket Unix y workaround desde shell.",
    ),
    ("mysql-multi-istanza-secure-file-priv", "ro"): (
        "MySQL multi-instanță: secure-file-priv și export CSV",
        "MySQL multi-instanță pe Linux: export CSV cu INTO OUTFILE blocat de secure-file-priv. Conectare prin socket Unix și workaround din shell.",
    ),
    # ----- 5. mysql-pre-upgrade-assessment -----
    ("mysql-pre-upgrade-assessment", "it"): (
        "MySQL 8.0 pre-upgrade assessment: dimensioni e tempi",
        "MySQL 8.0 pre-upgrade assessment: misurare dimensioni, crescita, tempi di backup e restore con information_schema. Cifre vere per pianificare.",
    ),
    ("mysql-pre-upgrade-assessment", "en"): (
        "MySQL 8.0 pre-upgrade assessment: sizing and timing",
        "MySQL 8.0 pre-upgrade assessment: measuring sizes, growth, backup and restore times with information_schema. Real numbers to plan maintenance window.",
    ),
    ("mysql-pre-upgrade-assessment", "es"): (
        "MySQL 8.0 pre-upgrade assessment: tamaños y tiempos",
        "MySQL 8.0 pre-upgrade assessment: medir tamaños, crecimiento, tiempos de backup y restore con information_schema. Cifras reales para planificar.",
    ),
    ("mysql-pre-upgrade-assessment", "ro"): (
        "MySQL 8.0 pre-upgrade assessment: dimensiuni și timpi",
        "MySQL 8.0 pre-upgrade assessment: dimensiuni, creștere, timpi de backup și restore cu information_schema. Cifre reale pentru planificare.",
    ),
    # ----- 6. mysql-users-and-hosts -----
    ("mysql-users-and-hosts", "it"): (
        "MySQL utenti e host: autenticazione e GRANT spiegati",
        "MySQL utenti e host: 'mario' e 'mario'@'localhost' sono entità diverse. Modello di autenticazione MySQL/MariaDB, errori frequenti e GRANT corretti.",
    ),
    ("mysql-users-and-hosts", "en"): (
        "MySQL users and hosts: authentication and GRANT explained",
        "MySQL users and hosts: 'mario' and 'mario'@'localhost' are different entities. MySQL/MariaDB authentication model, common mistakes and correct GRANTs.",
    ),
    ("mysql-users-and-hosts", "es"): (
        "MySQL usuarios y hosts: autenticación y GRANT explicados",
        "MySQL usuarios y hosts: 'mario' y 'mario'@'localhost' son entidades distintas. Modelo de autenticación MySQL/MariaDB, errores comunes y GRANTs.",
    ),
    ("mysql-users-and-hosts", "ro"): (
        "MySQL utilizatori și host: autentificare și GRANT",
        "MySQL utilizatori și host: 'mario' și 'mario'@'localhost' sunt entități diferite. Model autentificare MySQL/MariaDB, greșeli comune și GRANT.",
    ),
    # ----- 7. mysqldump-mysqlpump-mydumper -----
    ("mysqldump-mysqlpump-mydumper", "it"): (
        "MySQL backup: mysqldump vs mydumper vs mysqlpump",
        "Backup MySQL a confronto: mysqldump vs mydumper vs mysqlpump su database da 60 GB. Tempi reali di dump e restore, parallelismo e scelta architetturale.",
    ),
    ("mysqldump-mysqlpump-mydumper", "en"): (
        "MySQL backup: mysqldump vs mydumper vs mysqlpump",
        "MySQL backup tools compared: mysqldump vs mydumper vs mysqlpump on a 60 GB database. Real dump and restore times, parallelism and architectural choice.",
    ),
    ("mysqldump-mysqlpump-mydumper", "es"): (
        "MySQL backup: mysqldump vs mydumper vs mysqlpump",
        "Backup MySQL: mysqldump vs mydumper vs mysqlpump en base de datos de 60 GB. Tiempos reales de dump y restore, paralelismo y decisión arquitectónica.",
    ),
    ("mysqldump-mysqlpump-mydumper", "ro"): (
        "MySQL backup: mysqldump vs mydumper vs mysqlpump",
        "Backup MySQL: mysqldump vs mydumper vs mysqlpump pe bază de date de 60 GB. Timpi reali dump și restore, paralelism și decizie arhitecturală.",
    ),
    # ----- 8. enum-mysql-semplifica-o-complica -----
    ("enum-mysql-semplifica-o-complica", "it"): (
        "MySQL ENUM vs CHECK vs lookup: le tre strade",
        "MySQL ENUM vs CHECK constraint vs tabella di lookup: tre strade per modellare un'enumerazione. Vantaggi, limiti e caso reale di tracking spedizioni.",
    ),
    ("enum-mysql-semplifica-o-complica", "en"): (
        "MySQL ENUM vs CHECK vs lookup: the three roads",
        "MySQL ENUM vs CHECK constraint vs lookup table: three ways to model an enumeration. Pros, cons and real case of a shipment tracking system.",
    ),
    ("enum-mysql-semplifica-o-complica", "es"): (
        "MySQL ENUM vs CHECK vs lookup: las tres vías",
        "MySQL ENUM vs CHECK constraint vs tabla de lookup: tres vías para modelar una enumeración. Ventajas, límites y caso real de seguimiento de envíos.",
    ),
    ("enum-mysql-semplifica-o-complica", "ro"): (
        "MySQL ENUM vs CHECK vs lookup: cele trei căi",
        "MySQL ENUM vs CHECK constraint vs tabelă lookup: trei căi pentru modelarea unei enumerări. Avantaje, limite și caz real de tracking expedieri.",
    ),
}

BASE = Path("content/posts/mysql")


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
