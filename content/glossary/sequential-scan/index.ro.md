---
title: "Sequential Scan"
description: "Operație de citire în care PostgreSQL citește toate blocurile unei tabele fără a folosi indexuri, eficientă pe tabele mici dar problematică pe tabele mari."
translationKey: "glossary_sequential-scan"
aka: "Seq Scan / Full Table Scan"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**Sequential Scan** (Seq Scan) este operația prin care PostgreSQL citește o tabelă de la început până la sfârșit, bloc cu bloc, fără a folosi vreun index. Este echivalentul PostgreSQL al Full Table Scan din Oracle.

## Când este normal

Pe tabele mici (câteva mii de rânduri), sequential scan-ul este adesea opțiunea cea mai eficientă. Citirea unei tabele întregi secvențial este mai rapidă decât lookup-urile pe un index când tabela încape în câteva pagini. Optimizer-ul alege sequential scan-ul când estimează că este mai ieftin decât un index scan.

## Când este o problemă

Pe tabele mari (milioane de rânduri), un sequential scan pentru a returna puține rânduri este un semnal de alarmă. Înseamnă că lipsește un index adecvat sau că statisticile tabelei sunt depășite și optimizer-ul face estimări greșite. pg_stat_statements ajută la identificarea acestor situații arătând query-urile cu cel mai prost raport blocuri citite / rânduri returnate.

## Cum se diagnostichează

EXPLAIN arată "Seq Scan on tabel" în planul de execuție. Dacă filtrul ulterior elimină majoritatea rândurilor (rows removed by filter >> rows), aproape sigur este nevoie de un index pe coloana filtrului.
