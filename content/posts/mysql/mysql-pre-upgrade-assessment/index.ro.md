---
title: "Înainte de a face upgrade la MySQL: cifrele pe care clientul ți le cere și cum să le găsești cu adevărat"
description: "Patru servere MySQL 8.0 în producție, un responsabil de infrastructură care planifică fereastra de mentenanță și patru întrebări directe: cât de mari sunt, cât de repede cresc, cât durează un backup complet, cât durează un restore complet. Cum să răspunzi cu cifre măsurate în loc de estimări aproximative."
date: "2026-05-05T08:03:00+01:00"
draft: false
translationKey: "mysql_pre_upgrade_assessment"
tags: ["mysql", "upgrade", "backup", "restore", "assessment", "information-schema", "mysqldump", "mydumper", "xtrabackup"]
categories: ["MySQL"]
image: "mysql-pre-upgrade-assessment.cover.jpg"
---

Mail-ul de la responsabilul de infrastructură a sosit într-o luni dimineață, trei rânduri seci. *"Salut, până vineri am nevoie de patru cifre pentru a planifica fereastra de mentenanță pe MySQL-uri: cât de mari sunt astăzi, cât de mult cresc pe lună, cât durează un backup complet, cât ne ia să le reconstruim de la zero dacă ceva merge prost. Mulțumesc."*

Scenariu clasic într-o direcție IT a unei Administrații Publice italiene. Patru servere MySQL 8.0 care susțin aplicații interne și un portal pentru utilizatori, cu versiuni ușor diferite (8.0.32, 8.0.33, 8.0.34) pentru că au fost patch-uite în momente diferite. Upgrade de infrastructură planificat: noi host-uri, sistem de operare actualizat, aceeași versiune major de MySQL, cu fereastră de mentenanță nocturnă de șase ore.

PM-ul nu voia un assessment academic. Voia patru cifre reale de pus în planul de rollback. Iar tentația, când ai grabă, este să răspunzi după ureche: *"Or fi vreo 300 GB, backup-ul durează vreo două ore, restore-ul poate trei."* Cifre plauzibile, poate chiar corecte, dar nemăsurate — iar dacă greșești estimarea restore-ului cu un factor de doi, fereastra nu mai este suficientă și cutover-ul pică.

Mi-am luat o jumătate de zi. Iată metoda pe care am folosit-o.

## 📏 1. Cât cântăresc cu adevărat — `information_schema`

Prima cifră este cea mai simplă de găsit și cea mai înșelătoare de interpretat. În MySQL 8.0 {{< glossary term="information-schema" >}}`information_schema`{{< /glossary >}} expune tot ce este necesar, dar trebuie să știi ce să ceri.

```sql
-- Dimensiuni totale pe schemă (date + indecși)
SELECT
    table_schema                            AS schema_name,
    ROUND(SUM(data_length)  / 1024 / 1024 / 1024, 2) AS data_gb,
    ROUND(SUM(index_length) / 1024 / 1024 / 1024, 2) AS index_gb,
    ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) AS total_gb,
    COUNT(*)                                AS num_tables
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema')
GROUP BY table_schema
ORDER BY total_gb DESC;
```

Rezultat tipic pe unul dintre cele patru servere:

| schema_name            | data_gb | index_gb | total_gb | num_tables |
|------------------------|--------:|---------:|---------:|-----------:|
| portal_utilizatori     |   58,34 |    21,07 |    79,41 |        142 |
| gestiune_dosare        |   31,12 |    14,88 |    46,00 |         97 |
| audit_log              |   28,45 |     9,20 |    37,65 |         12 |
| master_partajat        |    4,18 |     1,32 |     5,50 |         24 |
| *(alte scheme)*        |    2,70 |     0,90 |     3,60 |         38 |
| **Total server**       |**124,79**|**47,37**|**172,16**|       313 |

Pare un rezultat închis, dar nu este. Două lucruri importante:

- **`data_length` și `index_length` sunt estimări** pe care InnoDB le actualizează periodic și care depind de ultimul `ANALYZE TABLE`. Pe tabele foarte volatile pot subestima cu 10-15%. Pentru date critice merită să verificăm cu dimensiunea fizică a fișierelor `.ibd` din datadir (`du -sh /var/lib/mysql/portal_utilizatori/*.ibd`).
- **Totalul serverului nu este dimensiunea backup-ului.** Fișierul de dump (logic) este mai compact pentru că nu replică fragmentarea InnoDB, dar conține `INSERT`-uri textuale care cântăresc mai mult decât datele binare. În practică, dump-ul necomprimat cântărește 70-90% din `data_length + index_length`. Cu `gzip` standard se coboară la 15-25%, cu `zstd -3` în jur de 18-28% dar mult mai rapid.

Rulând interogarea pe cele patru servere, sizing-ul total pe care l-am prezentat PM-ului a fost:

| Server    | MySQL  | Scheme | Total data + index | Fișiere .ibd pe disc |
|-----------|:------:|-------:|-------------------:|---------------------:|
| mysql-01  | 8.0.34 |      7 |           172,2 GB |              181 GB  |
| mysql-02  | 8.0.33 |      5 |            94,7 GB |               98 GB  |
| mysql-03  | 8.0.32 |      9 |           218,5 GB |              229 GB  |
| mysql-04  | 8.0.34 |      4 |            46,1 GB |               49 GB  |
| **Total** |        |     25 |         **531,5 GB** |         **557 GB** |

Diferența dintre "data + index" și "fișiere fizice" este costul fragmentării și al tablespace-ului `ibtmp1`. Merită evidențiat pentru PM pentru că pe noul mediu se poate planifica un `OPTIMIZE TABLE` post-migrare care recuperează acel 5-6% de spațiu.
