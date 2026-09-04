---
title: "dbupgrade"
description: "Utility Oracle che aggiorna il dizionario dati durante un upgrade di versione, sostituendo il vecchio catupgrd.sql dalla 12c in poi."
translationKey: "glossary_dbupgrade"
aka: "dbupgrade (successore di catupgrd.sql)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

`dbupgrade` è lo script shell introdotto da Oracle a partire dalla versione 12c per sostituire `catupgrd.sql`. Si occupa di portare il dizionario dati di sistema al livello della nuova versione Oracle installata, ricompilando i componenti interni e aggiornando le viste, i package e i metadati di sistema.

## Come funziona

`dbupgrade` viene eseguito dal DBA dopo aver avviato il database in modalità upgrade (`STARTUP UPGRADE`). Internamente orchestra una sequenza di script SQL equivalente a quella che `catupgrd.sql` eseguiva manualmente, ma con gestione degli errori, parallelismo configurabile e log strutturati per ogni componente.

```bash
# Avvio del database in modalità upgrade
sqlplus / as sysdba <<EOF
STARTUP UPGRADE;
EXIT;
EOF

# Esecuzione dell'upgrade del dizionario dati
cd $ORACLE_HOME/bin
./dbupgrade -n 4 -l /u01/upgrade_logs
```

Il parametro `-n` controlla il numero di processi paralleli; `-l` specifica la directory dei log. Al termine, il database viene riavviato in modalità normale e si esegue `utlrp.sql` per ricompilare gli oggetti invalidi.

## Quando si usa

`dbupgrade` è obbligatorio in qualsiasi percorso di upgrade Oracle in-place o dopo un restore del database su un nuovo `ORACLE_HOME` di versione superiore. È parte integrante del flusso DBUA (Database Upgrade Assistant) e può essere invocato anche manualmente per upgrade non interattivi o automatizzati via script. Nei contesti con database di grandi dimensioni — come upgrade da 12c a 21c su tablespace da 12 TB — la scelta del grado di parallelismo incide sensibilmente sui tempi complessivi.
