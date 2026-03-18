---
title: "RMAN"
description: "Recovery Manager — strumento Oracle per backup, restore e recovery del database, inclusa la creazione di database standby per Data Guard."
translationKey: "glossary_rman"
aka: "Recovery Manager"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RMAN** (Recovery Manager) è lo strumento nativo di Oracle per il backup, il restore e il recovery del database. È un'utility a riga di comando che gestisce tutte le operazioni di protezione dei dati in modo integrato con il database.

## Cosa fa

- **Backup**: completi, incrementali, dei soli archived log
- **Restore**: ripristino di datafile, tablespace o dell'intero database
- **Recovery**: applicazione dei redo log per portare il database a un punto nel tempo specifico
- **Duplicate**: creazione di copie del database, inclusi database standby per Data Guard

## RMAN e Data Guard

Per la creazione di un database standby, RMAN permette il `DUPLICATE ... FOR STANDBY FROM ACTIVE DATABASE` — una copia diretta via rete dal primario allo standby, senza bisogno di backup intermedi su nastro o disco. Il comando trasferisce tutti i datafile, i controlfile e li configura automaticamente per la replica.

## Perché RMAN e non copie manuali

RMAN conosce la struttura interna del database Oracle: sa quali blocchi sono cambiati (per gli incrementali), quali file servono, come applicare i redo. Una copia manuale dei file (con `cp` o `rsync`) non garantisce la consistenza e richiede che il database sia chiuso. RMAN può lavorare a database aperto, con impatto minimo sulle performance.
