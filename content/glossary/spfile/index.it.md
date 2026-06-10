---
title: "SPFILE"
description: "SPFILE (Server Parameter File) è il file binario di Oracle che contiene i parametri di configurazione dell'istanza, modificabile a caldo senza riavvio."
translationKey: "glossary_spfile"
aka: "Server Parameter File"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

L'SPFILE è il file binario che Oracle legge all'avvio per inizializzare i parametri dell'istanza: `db_name`, `control_files`, `memory_target`, `sga_target` e decine di altri. A differenza del suo predecessore testuale PFILE (`init.ora`), l'SPFILE non si modifica manualmente con un editor di testo, ma tramite comandi SQL.

## Come funziona

All'avvio, Oracle cerca l'SPFILE in una posizione predefinita (`$ORACLE_HOME/dbs/spfile<SID>.ora` su Linux). Se non lo trova, ricade sul PFILE. Le modifiche ai parametri avvengono con `ALTER SYSTEM SET`, che scrive direttamente nel file binario:

```sql
-- Modifica persistente (sopravvive al riavvio)
ALTER SYSTEM SET memory_target = 2G SCOPE = SPFILE;

-- Modifica solo in memoria (persa al riavvio)
ALTER SYSTEM SET memory_target = 2G SCOPE = MEMORY;

-- Modifica sia in memoria sia nel file
ALTER SYSTEM SET memory_target = 2G SCOPE = BOTH;
```

Il parametro `SCOPE` controlla dove la modifica viene applicata: `SPFILE`, `MEMORY` o `BOTH`.

## Contesto operativo

L'SPFILE è il punto di riferimento per la configurazione persistente dell'istanza. Va incluso nei backup RMAN, che lo gestisce nativamente. In ambienti RAC (Real Application Clusters), un singolo SPFILE condiviso su ASM governa tutti i nodi, con la possibilità di impostare valori per-istanza tramite il prefisso `SID.*`.

Un errore comune è modificare manualmente il file binario: l'istanza non si avvierà più. Se l'SPFILE è corrotto, si ripristina dal backup RMAN o si ricrea da un PFILE con `CREATE SPFILE FROM PFILE`.
