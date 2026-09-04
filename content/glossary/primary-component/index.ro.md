---
title: "Primary Component (PC)"
description: "Primary Component este subsetul de noduri Galera care deține quorumul și poate accepta scrieri, prevenind scenariile de split-brain."
translationKey: "glossary_primary_component"
aka: "PC, partiție de quorum"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

Într-un cluster Galera, nu toate nodurile sunt echivalente în orice moment: doar cele care formează **Primary Component** au dreptul de a procesa scrieri. PC-ul este subsetul de noduri care a atins quorumul — adică majoritatea voturilor totale ale clusterului — și care poate astfel să opereze în siguranță. Nodurile excluse din PC intră în starea `non-Primary` și nu mai acceptă instrucțiuni DML.

## Cum funcționează

Galera folosește un protocol de membership bazat pe **wsrep** (Write-Set Replication). Fiecare nod schimbă heartbeat-uri și voturi cu celelalte. Când o partiție de rețea sau o cădere izolează un grup de noduri, fiecare grup calculează independent dacă deține mai mult de jumătate din voturile totale ale clusterului.

- Grupul cu **mai mult de jumătate din voturi** devine (sau rămâne) Primary Component.
- Grupul minoritar trece în starea `non-Primary`: conexiunile clienților primesc o eroare și nicio scriere nu este acceptată.

Acest mecanism este principala protecție împotriva **split-brain**: două partiții nu pot crede simultan că sunt PC-ul și să divergă în tăcere.

## Context operațional

Cazul critic este clusterul cu **două noduri**: dacă un nod cade, supraviețuitorul deține exact 50% din voturi și nu poate atinge quorumul. Intră în starea `non-Primary` chiar dacă funcționează perfect. Soluția standard este adăugarea unui al treilea nod sau a unui arbitru ușor (`garbd`) pentru a garanta că o parte poate depăși întotdeauna 50%.

În scenarii de mentenanță sau bootstrap de urgență, este posibil să se forțeze manual formarea PC-ului:

```sql
SET GLOBAL wsrep_provider_options='pc.bootstrap=YES';
```

Această operațiune trebuie executată cu atenție: dacă există o altă partiție activă cu date mai recente, promovarea nodului greșit poate duce la pierderea tranzacțiilor deja confirmate.
