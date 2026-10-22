---
title: "DNS"
description: "DNS (Domain Name System) traduce nume de host în adrese IP, asigurând conectivitatea de rețea pentru baze de date, listener-e Oracle și servicii cloud OCI."
translationKey: "glossary_dns"
aka: "Domain Name System"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

DNS (Domain Name System) este sistemul distribuit care rezolvă nume de host simbolice în adrese IP. În contextul bazelor de date și al infrastructurii cloud, reprezintă mecanismul de bază care permite clienților, aplicațiilor și instrumentelor de administrare să ajungă la instanțe Oracle, endpoint-uri OCI și servicii de rețea fără a codifica adrese IP statice în șirurile de conexiune.

## Cum funcționează

Când un client Oracle încearcă să se conecteze la un host prin `tnsnames.ora` sau Easy Connect, sistemul de operare interoghează resolver-ul DNS configurat. Resolver-ul parcurge ierarhia DNS (rădăcină → TLD → server autoritativ) și returnează adresa IP corespunzătoare numelui de host.

```bash
# Verificarea rezoluției DNS pentru un listener Oracle pe OCI
nslookup db-prod.subnet.vcn.oraclevcn.com
dig +short db-prod.subnet.vcn.oraclevcn.com A
```

În OCI, fiecare VCN dispune de un resolver DNS intern care gestionează automat înregistrările pentru resursele tenant-ului (DB Systems, Autonomous Database, Load Balancers).

## Context operațional

În cadrul unui upgrade Oracle 11g R2 → 19c pe OCI, DNS devine critic în cel puțin trei momente:

- **Provizionarea noului DB System**: numele de host al sistemului țintă 19c trebuie să fie rezolvabil de toți clienții și job-urile de migrare înainte de a începe transferul de date.
- **Cutover și ROLLBACK**: dacă planul utilizează un CNAME sau un alias DNS ca punct de acces al aplicației, modificarea înregistrării (cu un TTL scăzut presetat) este mecanismul de comutare cel mai rapid și mai reversibil.
- **Conexiuni între subrețele**: în arhitecturi multi-tier, regulile de firewall și security list-urile OCI trebuie să permită traficul UDP/TCP pe portul 53 către resolver-ul VCN.

Un TTL ridicat pe înregistrările DNS poate încetini ROLLBACK-ul: reducerea acestuia la 60-300 de secunde în orele premergătoare cutover-ului este o practică standard în planurile de migrare cu risc redus.
