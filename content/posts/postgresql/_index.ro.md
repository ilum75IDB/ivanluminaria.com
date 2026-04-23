---
description: "PostgreSQL: arhitectură, performanță și proiectare într-unul dintre cele mai avansate și longevive sisteme open source de baze de date."
layout: "list"
title: "PostgreSQL"
image: "postgresql.cover.jpg"
---

Am văzut PostgreSQL în producție cu `shared_buffers` la 128MB pe mașini cu 256GB de RAM — "pentru că am urmat default-ul". Am văzut `autovacuum` dezactivat pentru că "încetinea sistemul", iar trei luni mai târziu o tabelă de 500 de milioane de rânduri cu 80% bloat și interogări care nu se mai terminau. Am văzut replici streaming rupte în tăcere de săptămâni, și ne-am dat seama doar când master-ul a căzut și failover-ul nu a pornit.

Și am văzut exact opusul: clustere Postgres care susțin mii de conexiuni concurente, gestionează terabytes de date și supraviețuiesc la upgrade-uri majore fără un minut de downtime perceput.

Diferența nu este în cod. Este în **cine a avut curajul să atingă default-urile în loc să le îndure**.

------------------------------------------------------------------------

PostgreSQL nu este doar o bază de date open source. Este rezultatul a aproape patru decenii de evoluție academică și industrială.

Născut în 1986 la Universitatea Berkeley ca evoluție a Ingres, proiectul POSTGRES a introdus concepte care pe atunci erau avangardiste: **extensibilitate, tipuri de date personalizate, reguli și un model relațional avansat**. În 1996 a apărut suportul SQL iar numele a devenit PostgreSQL. Lumea, însă, a continuat să îi spună simplu "Postgres". Și e perfect în regulă așa.

După douăzeci de ani de lucru cu el, un lucru am învățat: PostgreSQL **îl răsplătește pe cel care îl studiază și îl pedepsește pe cel care îl lasă pe default-uri**. Este un motor conceput să fie tunat, nu instalat și uitat. Presupunerile din dezvoltare sunt demontate de realitatea producției:

- **VACUUM și autovacuum** nu sunt opționale — sunt ca spălatul pe dinți
- **`shared_buffers`** la default-ul de 128MB este rezonabil doar pe un laptop
- **`work_mem`** setat greșit înmulțit cu conexiunile active îți provoacă un OOM în cel mai prost moment
- **Replicile** au nevoie de monitoring activ — streaming-ul se rupe în tăcere
- **Extensiile** pot schimba comportamentul catalogului și bloca upgrade-urile

------------------------------------------------------------------------

## 🔧 Parametrii pe care nu îi las niciodată pe default

Când pun în producție un cluster Postgres, sunt cinci parametri pe care nu îi las niciodată la valoarea de fabrică. Nu pentru că default-ul ar fi greșit în mod absolut, ci pentru că e gândit să ruleze oriunde — și "oriunde" nu este niciodată mașina ta de producție.

| Parametru | Ce reglează | Cum îl setez |
|---|---|---|
| **`shared_buffers`** | Cache-ul partajat al Postgres | De obicei 25% din RAM — nu mai mult, cache-ul filesystem-ului face restul |
| **`effective_cache_size`** | Ce crede planner-ul că este în cache | 50-75% din RAM — nu alocă nimic, influențează alegerile optimizatorului |
| **`work_mem`** | Memorie pentru sort și hash pe operație | Mic (4-16MB) dacă sunt multe conexiuni, mare doar pentru încărcări analitice dedicate |
| **`autovacuum_*`** | Curățarea automată a dead tuples | Niciodată dezactivat. Eventual tunat (`naptime`, `cost_limit`) pentru a fi mai agresiv pe tabele calde |
| **`wal_level` + `max_wal_senders`** | Detaliul WAL, slot-uri pentru replici | `replica` sau `logical` după caz, senders dimensionați pe replicile reale plus marjă |

Cinci parametri. Douăzeci de minute de analiză. Luni de probleme de performanță evitate.

------------------------------------------------------------------------

## 📚 Despre ce vorbesc aici

Povești reale și alegeri tehnice pe PostgreSQL în producție. Arhitectură, VACUUM și bloat, tuning de parametri, replicare streaming și logică, strategii de upgrade, backup-uri cu pg_basebackup și WAL archiving, extensii care chiar ajută (și cele care se puteau evita).

Fără rețete preambalate. Doar ce am văzut funcționând pe medii reale — postal, bănci, administrație publică, telco — unde Postgres susține mii de instanțe în paralel și nu își poate permite aproximări.

------------------------------------------------------------------------

A alege PostgreSQL nu înseamnă doar a alege o bază de date open source.

Înseamnă a alege un motor conceput pentru a fi extins, analizat și înțeles — și a accepta că fără puțin studiu default-urile nu te vor duce departe.
