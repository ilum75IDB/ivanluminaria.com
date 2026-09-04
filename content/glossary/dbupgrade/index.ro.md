---
title: "dbupgrade"
description: "Utilitar Oracle care actualizează dicționarul de date al sistemului în timpul unui upgrade de versiune, înlocuind vechiul catupgrd.sql începând cu versiunea 12c."
translationKey: "glossary_dbupgrade"
aka: "dbupgrade (succesor al catupgrd.sql)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

`dbupgrade` este scriptul shell introdus de Oracle începând cu versiunea 12c pentru a înlocui `catupgrd.sql`. Rolul său este de a aduce dicționarul de date al sistemului la nivelul noii versiuni Oracle instalate, recompilând componentele interne și actualizând view-urile, pachetele și metadatele de sistem.

## Cum funcționează

`dbupgrade` este rulat de DBA după pornirea bazei de date în modul upgrade (`STARTUP UPGRADE`). Intern, orchestrează aceeași secvență de scripturi SQL pe care `catupgrd.sql` o executa manual, dar cu gestionare integrată a erorilor, paralelism configurabil și loguri structurate pentru fiecare componentă.

```bash
# Pornirea bazei de date în modul upgrade
sqlplus / as sysdba <<EOF
STARTUP UPGRADE;
EXIT;
EOF

# Rularea upgrade-ului dicționarului de date
cd $ORACLE_HOME/bin
./dbupgrade -n 4 -l /u01/upgrade_logs
```

Parametrul `-n` controlează numărul de procese paralele; `-l` specifică directorul de loguri. La finalizare, baza de date este repornită în modul normal și se execută `utlrp.sql` pentru recompilarea obiectelor invalide.

## Când se folosește

`dbupgrade` este obligatoriu în orice upgrade Oracle in-place sau după restaurarea bazei de date pe un `ORACLE_HOME` de versiune superioară. Face parte din fluxul DBUA (Database Upgrade Assistant) și poate fi invocat manual pentru upgrade-uri neinteractive sau automatizate prin scripturi. În scenarii cu baze de date de dimensiuni mari — precum un upgrade de la 12c la 21c pe tablespace-uri de 12 TB — gradul de paralelism ales influențează direct durata totală a procesului.
