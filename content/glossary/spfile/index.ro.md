---
title: "SPFILE"
description: "SPFILE (Server Parameter File) este fișierul binar Oracle citit la pornire, care conține parametrii de configurare ai instanței, modificabil fără repornirea bazei de date."
translationKey: "glossary_spfile"
aka: "Server Parameter File"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

SPFILE este fișierul binar pe care Oracle îl citește la pornire pentru a inițializa parametrii instanței: `db_name`, `control_files`, `memory_target`, `sga_target` și mulți alții. Spre deosebire de predecesorul său în format text PFILE (`init.ora`), SPFILE nu se editează manual cu un editor de text — modificările se fac prin comenzi SQL.

## Cum funcționează

La pornire, Oracle caută SPFILE într-o locație implicită (`$ORACLE_HOME/dbs/spfile<SID>.ora` pe Linux). Dacă nu îl găsește, recurge la PFILE. Modificările parametrilor se realizează cu `ALTER SYSTEM SET`, care scrie direct în fișierul binar:

```sql
-- Modificare persistentă (supraviețuiește repornirii)
ALTER SYSTEM SET memory_target = 2G SCOPE = SPFILE;

-- Doar în memorie (se pierde la repornire)
ALTER SYSTEM SET memory_target = 2G SCOPE = MEMORY;

-- Atât în memorie, cât și în fișier
ALTER SYSTEM SET memory_target = 2G SCOPE = BOTH;
```

Parametrul `SCOPE` controlează unde se aplică modificarea: `SPFILE`, `MEMORY` sau `BOTH`.

## Context operațional

SPFILE este sursa de referință pentru configurația persistentă a instanței. Trebuie inclus în backup-urile RMAN, care îl gestionează nativ. În medii RAC (Real Application Clusters), un singur SPFILE partajat pe ASM guvernează toți nodurile, cu posibilitatea de a seta valori per instanță prin prefixul `SID.*`.

O greșeală frecventă este editarea manuală a fișierului binar: instanța nu va mai porni. Dacă SPFILE este corupt, se restaurează dintr-un backup RMAN sau se recreează dintr-un PFILE cu `CREATE SPFILE FROM PFILE`.
