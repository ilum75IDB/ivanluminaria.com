---
title: "RMAN Incremental Backup"
description: "Backup Oracle RMAN che registra solo i blocchi modificati dall'ultimo backup di livello uguale o superiore. Level 0 è la base, level 1 è il delta."
translationKey: "glossary_rman_incremental_backup"
aka: "RMAN Incremental Backup (Oracle Recovery Manager)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

L'RMAN Incremental Backup è una strategia di backup Oracle che non copia l'intero datafile ma solo i blocchi dati modificati rispetto all'ultimo backup di livello uguale o superiore. Questo riduce drasticamente la finestra di backup e il volume trasferito, rendendolo lo strumento di riferimento per sincronizzare database di grandi dimensioni durante le migrazioni.

## Come funziona

Il meccanismo si basa su due livelli:

- **Level 0**: equivale a un backup completo, ma è la base della catena incrementale. Tutti i blocchi vengono copiati.
- **Level 1**: copia solo i blocchi modificati dopo l'ultimo backup level 0 o level 1.

RMAN traccia i blocchi modificati tramite il **Change Tracking File** (se abilitato), evitando la scansione completa dei datafile.

```bash
# Backup incrementale level 0 (base)
rman target /
BACKUP INCREMENTAL LEVEL 0 DATABASE;

# Backup incrementale level 1 (delta)
BACKUP INCREMENTAL LEVEL 1 DATABASE;

# Applicazione del delta a una copia immagine
RECOVER COPY OF DATABASE WITH TAG 'incr_merge';
```

## Quando si usa

In contesti di migrazione — come il passaggio da Oracle 12c a 21c su database da 12 TB — l'approccio tipico è:

1. Eseguire un backup level 0 (o una copia fisica iniziale) sul sistema sorgente.
2. Applicare backup level 1 successivi per ridurre il gap di dati durante la finestra di cutover.
3. Al momento del downtime, applicare l'ultimo incrementale e aprire il database di destinazione.

Questo schema minimizza il downtime finale a pochi minuti, indipendentemente dalla dimensione del database. Il limite principale è la dipendenza dalla catena: un backup level 1 senza un level 0 valido non è applicabile.
