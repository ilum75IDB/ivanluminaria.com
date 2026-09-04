---
title: "gcache"
description: "Buffer circular pe disc menținut de fiecare nod Galera Cluster pentru a stoca writeset-urile recente și a favoriza IST față de SST la reporniri scurte."
translationKey: "glossary_gcache"
aka: "Galera Cache"
articles:
  - "/posts/mysql/galera-cluster-quorum-split-brain-e-bootstrap-di-emergenza-con-due-nodi-giu"
---

gcache-ul este un buffer circular pe disc pe care fiecare nod dintr-un Galera Cluster îl menține local. Conține writeset-urile replicate recent și reprezintă memoria operațională a procesului de sincronizare incrementală între noduri.

## Cum funcționează

Când un nod revine în cluster după o absență scurtă, Galera verifică dacă writeset-urile lipsă se află încă în gcache-ul nodului donator. Dacă da, se execută o **Incremental State Transfer (IST)**: donatorul trimite doar writeset-urile lipsă, fără a copia întregul dataset. Dacă gcache-ul nu acoperă intervalul lipsă, clusterul recurge la o **State Snapshot Transfer (SST)**, operațiune mult mai costisitoare care transferă un snapshot complet al bazei de date.

Parametrul cheie este `gcache.size`, configurabil în `wsrep_provider_options`:

```ini
wsrep_provider_options = "gcache.size=2G"
```

Valoarea implicită este 128 MB, adesea insuficientă în medii cu volum ridicat de scrieri.

## Context operațional

Dimensionarea corectă a gcache-ului este principala pârghie pentru a evita operațiunile SST nedorite. Regula practică este să se estimeze volumul de writeset-uri produs în fereastra de inactivitate așteptată (mentenanță, repornire, instabilitate de rețea) și să se seteze `gcache.size` peste acel prag. Un gcache prea mic forțează SST chiar și după absențe de câteva minute; unul prea mare ocupă spațiu pe disc fără beneficiu proporțional.

Fișierul fizic al gcache-ului se află implicit la `<datadir>/galera.cache`, iar dimensiunea sa pe disc corespunde exact valorii configurate, pre-alocată la pornire.
