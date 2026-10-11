---
title: "preupgrd.sql"
description: "Script Oracle di pre-upgrade da eseguire sull'istanza sorgente: analizza oggetti non validi, parametri deprecati e incompatibilità prima del cutover."
translationKey: "glossary_preupgrd_sql"
aka: "Oracle Pre-Upgrade Information Tool"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`preupgrd.sql` è lo script di pre-upgrade distribuito con Oracle 19c (e versioni precedenti con nomi analoghi). Va eseguito sull'istanza **sorgente**, prima di avviare qualsiasi procedura di migrazione, e produce un report testuale che fotografa lo stato del database rispetto ai requisiti della versione di destinazione.

## Cosa fa

Lo script interroga dizionario dati e viste interne per rilevare:

- oggetti non validi (`INVALID`) che potrebbero bloccare la fase di recompilazione post-upgrade
- parametri di inizializzazione deprecati o rimossi nella versione target
- feature obsolete ancora attive (es. `COMPATIBLE`, `DB_BLOCK_SIZE` fuori range)
- problemi di timezone, character set e componenti opzionali non migrabili automaticamente

L'output viene scritto in `$ORACLE_BASE/cfgtoollogs/db_unique_name/preupgrade/` come file di testo e, nelle versioni recenti, come script SQL correttivi già pronti.

```bash
sqlplus / as sysdba @$ORACLE_HOME/rdbms/admin/preupgrd.sql
```

## Quando si usa

`preupgrd.sql` si esegue **settimane prima** del cutover, non la notte stessa. Il report va analizzato dal DBA per pianificare le remediation: invalidare e ricompilare oggetti, rimuovere parametri obsoleti, aggiornare i componenti opzionali. In ambienti di produzione critici — come database finanziari da 8 TB — il report diventa input diretto per il piano di rollback e per la stima della finestra di manutenzione.

## Note operative

Oracle distribuisce versioni aggiornate dello script con ogni PSU/RU. Prima di eseguirlo, verificare di usare la copia presente nell'`ORACLE_HOME` **della versione di destinazione**, non di quella sorgente: è lì che risiede la logica di controllo aggiornata.
