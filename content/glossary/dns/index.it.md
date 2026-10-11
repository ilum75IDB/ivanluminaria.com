---
title: "DNS"
description: "DNS (Domain Name System) traduce nomi host leggibili in indirizzi IP, abilitando la connettività di rete per database, listener Oracle e servizi cloud OCI."
translationKey: "glossary_dns"
aka: "Domain Name System"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

Il DNS (Domain Name System) è il sistema distribuito che risolve nomi host simbolici in indirizzi IP. In ambito database e infrastruttura cloud, è il meccanismo sottostante che permette a client, applicazioni e strumenti di amministrazione di raggiungere istanze Oracle, endpoint OCI e servizi di rete senza dover codificare indirizzi IP statici nelle stringhe di connessione.

## Come funziona

Quando un client Oracle tenta di connettersi a un host tramite `tnsnames.ora` o Easy Connect, il sistema operativo interroga il resolver DNS configurato. Il resolver percorre la gerarchia DNS (root → TLD → authoritative server) e restituisce l'indirizzo IP corrispondente al nome host.

```bash
# Verifica risoluzione DNS di un listener Oracle su OCI
nslookup db-prod.subnet.vcn.oraclevcn.com
dig +short db-prod.subnet.vcn.oraclevcn.com A
```

In OCI, ogni VCN dispone di un resolver DNS interno che gestisce automaticamente i record per le risorse del tenant (DB System, Autonomous Database, Load Balancer).

## Contesto operativo

Durante un upgrade Oracle 11g R2 → 19c su OCI, il DNS diventa critico in almeno tre momenti:

- **Provisioning del nuovo DB System**: il nome host del target 19c deve essere risolvibile da tutti i client e dai job di migrazione dati prima di avviare il trasferimento.
- **Cutover e rollback**: se il piano prevede un CNAME o un alias DNS per il punto di accesso applicativo, il cambio del record (con TTL basso preimpostato) è il meccanismo di switch più rapido e reversibile.
- **Connessioni cross-subnet**: in architetture multi-tier, firewall e security list OCI devono permettere il traffico UDP/TCP sulla porta 53 verso il resolver VCN.

Un TTL elevato sui record DNS può rendere il rollback lento: abbassarlo a 60-300 secondi nelle ore precedenti il cutover è una pratica standard nei piani di migrazione a basso rischio.
