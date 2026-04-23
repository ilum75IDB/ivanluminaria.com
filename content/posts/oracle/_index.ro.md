---
title: "Oracle"
layout: "list"
date: "2026-03-10T08:03:00+01:00"
description: "Oracle Database: securitate, performanță și arhitectură pe cea mai longevivă și complexă bază de date enterprise de pe piață."
image: "oracle.cover.jpg"
---

Am văzut un DBA oprind o producție cu un `DROP TABLESPACE` lansat pe fereastra greșită. Am văzut interogări de patru secunde devenind de patru ore după un upgrade, pentru că cineva atinsese `optimizer_features_enable` "oricum era la fel". Am văzut backup-uri care nu se restaurau, audituri dezactivate "temporar" de cinci ani, și indecși creați în producție cu mâna liberă într-o vineri după-amiază.

Și am văzut exact opusul: instanțe Oracle care funcționează de douăzeci de ani fără un minut de downtime neplanificat, susțin încărcări uriașe și supraviețuiesc la trei upgrade-uri majore fără să clipească.

Diferența nu a fost niciodată versiunea. A fost întotdeauna **cine o gestiona**.

------------------------------------------------------------------------

Lucrez cu Oracle din 1996. În aproape treizeci de ani am văzut trecând Oracle 7, 8i, 9i, 10g, 11g, 12c, 19c, 21c, 23ai — și paradigme, tendințe, consultanți care vindeau funcționalitatea lunii ca răspuns la orice problemă.

Inima motorului, însă, a rămas aceeași: **solidă, complexă, neiertătoare cu cei care nu o cunosc în profunzime.**

Oracle nu se învață din tutoriale. Se învață:

- din **incidentele de producție** la trei dimineața, când manualul e de puțin folos și valorează mai mult un coleg care a mai văzut acel comportament
- din **migrări** în care planul de execuție se schimbă a doua zi după go-live și nimeni nu înțelege de ce
- din **planurile de execuție** care devin patologice după un `DBMS_STATS.GATHER_SCHEMA_STATS` lansat cu parametri impliciți
- din **`v$`** care spun adevărul chiar și când aplicația minte
- din **tuning pack-urile** care chiar ajută, și cele pe care le-ai plătit și nu le vei porni niciodată

------------------------------------------------------------------------

## 🔧 Ce mă uit când ajung pe o instanță nouă

Când un client mă sună pentru că "baza de date merge încet" sau "ceva nu e în regulă", sunt cinci lucruri la care mă uit înainte să ating vreun parametru. Nu e un checklist dintr-un curs de certificare — e ce am învățat să mă uit după ce am pierdut timp prea des în locurile greșite.

| Ce | Unde mă uit | De ce |
|---|---|---|
| **Încărcarea reală** | AWR, ASH, `v$active_session_history` | A înțelege cine consumă cu adevărat CPU, I/O și `db time` — adesea nu e ce suspectează clientul |
| **Ce a atins cine a venit înainte** | `v$parameter` cu `ismodified`, `dba_hist_parameter` | Parametrii "non-standard" sunt primul indiciu de debug trecut fără documentație |
| **Cine face ce** | `dba_audit_trail`, `unified_audit_trail`, job-uri programate | Găsirea job-urilor nocturne, a conexiunilor aplicative reale, a acceselor DBA netrasate |
| **Starea Data Guard** | `v$dataguard_stats`, `v$archive_dest_status` | Dacă există standby, verificat că e cu adevărat aliniat — fără încredere în dashboards |
| **Spațiul și creșterea** | `dba_tablespaces`, `dba_hist_tbspc_space_usage` | A înțelege unde te îndrepți spre impact înainte să se întâmple, nu după |

Odată citite aceste cinci lucruri, am 70% din tablou. Celelalte întrebări vin după — și vin țintite.

------------------------------------------------------------------------

## 📚 Despre ce vorbesc aici

Povești reale, numere concrete și lecții învățate pe Oracle în producție. Arhitectură, performanță, securitate, migrări, tuning SQL, PL/SQL, gestionarea stocării și decizii de proiectare care separă o instalare care funcționează de una care supraviețuiește.

Fără teorie de broșură. Doar ce am văzut funcționând — și ce am văzut eșuând — pe medii reale: asigurări, telco, administrație publică, bănci, farmaceutic.

------------------------------------------------------------------------

La Oracle nu este suficient să cunoști sintaxa.

Trebuie să înțelegi cum gândește motorul — și să ai umilința de a recunoaște că, uneori, are dreptate el.
