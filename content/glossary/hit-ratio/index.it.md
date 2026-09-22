---
title: "Hit ratio"
description: "Percentuale di letture InnoDB servite dal Buffer Pool rispetto al totale. Valori sotto 990/1000 segnalano pressione sul disco."
translationKey: "glossary_hit_ratio"
aka: "Buffer Pool hit ratio"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

L'hit ratio misura quante letture di pagine InnoDB vengono soddisfatte direttamente dal Buffer Pool, senza accedere al disco. È l'indicatore primario dell'efficacia della memoria allocata a InnoDB: un valore alto significa che la working set dei dati caldi sta in RAM; un valore basso significa I/O fisico frequente e latenze più alte.

## Come si legge

MySQL esprime l'hit ratio nell'output di `SHOW ENGINE INNODB STATUS` nella sezione `BUFFER POOL AND MEMORY`, con la formula:

```
Buffer pool hit rate X / 1000
```

Un valore di `997 / 1000` significa che 997 letture su 1000 sono state servite dalla memoria. La soglia operativa comunemente accettata è **990/1000**: scendere sotto indica che il Buffer Pool è sottodimensionato rispetto al working set attivo.

## Contesto operativo

L'hit ratio è particolarmente instabile dopo un restart di MySQL: il Buffer Pool è freddo e le prime query generano page fault a cascata, abbassando il valore anche sotto 900/1000. InnoDB supporta il dump e il reload automatico del Buffer Pool (`innodb_buffer_pool_dump_at_shutdown` / `innodb_buffer_pool_load_at_startup`) proprio per accelerare il warm-up.

Un hit ratio cronicamente basso non si risolve solo aumentando `innodb_buffer_pool_size`: occorre anche verificare se query inefficienti eseguono full scan su tabelle grandi, evitando così di inquinare il Buffer Pool con pagine usate una volta sola.
