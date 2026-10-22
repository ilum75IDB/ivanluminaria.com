---
title: "XTTS (Cross-Platform Transportable Tablespaces)"
description: "Metodo Oracle per migrare database multi-terabyte tra versioni diverse minimizzando il downtime tramite backup RMAN incrementali ciclici."
translationKey: "glossary_xtts"
aka: "Cross-Platform Transportable Tablespaces"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

XTTS (Cross-Platform Transportable Tablespaces) è la tecnica Oracle che consente di spostare tablespace tra piattaforme e versioni di database differenti — ad esempio da Oracle 11gR2 su Linux x86 a Oracle 19c su OCI — trasportando i datafile direttamente anziché eseguire un export/import logico. Per database nell'ordine dei terabyte, questo approccio riduce il downtime del cutover finale da giorni a poche ore.

## Come funziona

Il processo si articola in tre fasi distinte:

1. **Backup RMAN level 0** — copia completa dei datafile dei tablespace sorgente, trasferita sulla destinazione e ripristinata.
2. **Incrementali ciclici (level 1)** — eseguiti più volte nelle settimane precedenti il cutover, riducono progressivamente il delta tra sorgente e destinazione.
3. **Cutover finale** — l'ultimo incrementale viene applicato con il tablespace sorgente in read-only, il plug-in sulla destinazione completa la migrazione.

```bash
# Esempio: generazione script RMAN per backup level 0
$ORACLE_HOME/perl/bin/perl xttdriver.pl --backup_to_dest \
  --tablespaces USERS,FINANCE \
  --level 0
```

Lo script `xttdriver.pl` (incluso in Oracle MOS) orchestra backup, conversione endian e trasferimento dei file.

## Quando si usa

XTTS è la scelta corretta quando:

- Il database supera qualche centinaio di GB e un export Data Pump richiederebbe finestre di manutenzione inaccettabili.
- La migrazione attraversa versioni maggiori (es. 11g → 19c) o piattaforme con endianness diversa.
- Il SLA impone un downtime massimo misurabile in ore, non in giorni.

Il limite principale è la complessità operativa: richiede coordinamento preciso tra DBA sorgente e destinazione, verifica della compatibilità del character set e gestione degli oggetti non trasportabili (sequenze, sinonimi, grant) che vanno migrati separatamente con Data Pump.
