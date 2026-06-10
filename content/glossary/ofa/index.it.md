---
title: "OFA"
description: "OFA (Optimal Flexible Architecture) è la convenzione Oracle per organizzare path e file di un'istanza in modo prevedibile, portabile e manutenibile."
translationKey: "glossary_ofa"
aka: "Optimal Flexible Architecture"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

OFA (Optimal Flexible Architecture) è la convenzione di naming e layout dei path raccomandata da Oracle per organizzare i file di un'istanza: datafile, control file, redo log, archived log e backup. Seguirla non è obbligatorio, ma rende l'ambiente prevedibile per chiunque debba operarci, inclusi strumenti come DBCA e RMAN.

## Come funziona

OFA definisce una gerarchia di directory con radice in un mount point dedicato, tipicamente nella forma `/u01/app/oracle/oradata/<DB_NAME>/`. I file vengono poi distribuiti in sottodirectory per tipo:

```
/u01/app/oracle/                  # ORACLE_BASE
  product/19.0.0/dbhome_1/        # ORACLE_HOME
  oradata/ORCL/                   # datafile e control file
  fast_recovery_area/ORCL/        # FRA: archived log, backup, flashback log
  admin/ORCL/adump/               # audit trail
```

I datafile seguono il pattern `<tablespace_name>_<n>.dbf`, i redo log `redo<group>_<member>.log`. Il naming sistematico permette di identificare a colpo d'occhio il ruolo di ogni file.

## Quando si usa

OFA è rilevante in fase di installazione e provisioning: DBCA la applica di default, e RMAN la presuppone quando si configurano i path di backup. Ambienti che deviano da OFA tendono ad accumulare debito operativo: script di manutenzione scritti per un'istanza non funzionano su un'altra, e il troubleshooting notturno diventa più lento. In contesti multi-istanza o RAC, rispettare OFA è praticamente indispensabile per mantenere la sanità mentale del team.
