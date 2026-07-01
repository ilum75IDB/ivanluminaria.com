---
title: "join_buffer_size"
description: "Buffer MySQL allocato per thread per ogni join senza indice. Moltiplicato per le connessioni attive, può saturare la RAM del server."
translationKey: "glossary_join_buffer_size"
aka: "Join Buffer (MySQL)"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

`join_buffer_size` è un parametro di sessione MySQL che controlla la dimensione del buffer usato per eseguire join tra tabelle quando non è disponibile un indice adeguato. A differenza del `innodb_buffer_pool_size`, che è una risorsa condivisa, questo buffer viene allocato **per ogni thread attivo** che esegue un join di quel tipo.

## Come funziona

Quando MySQL non può sfruttare un indice per collegare due tabelle, ricorre a un **Block Nested-Loop Join** (o, nelle versioni più recenti, a un Hash Join). In entrambi i casi, i record della tabella "esterna" vengono caricati nel `join_buffer` per essere confrontati con la tabella "interna".

```sql
-- Verifica il valore corrente a livello di sessione
SHOW VARIABLES LIKE 'join_buffer_size';

-- Modifica per la sessione corrente
SET SESSION join_buffer_size = 4 * 1024 * 1024; -- 4 MB
```

Se il buffer non è sufficiente a contenere tutti i record, MySQL esegue più passaggi sulla tabella interna, aumentando l'I/O.

## Contesto operativo

Il rischio principale non è il valore assoluto del parametro, ma il suo **effetto moltiplicativo**: con 500 connessioni concorrenti e un `join_buffer_size` di 8 MB, il consumo potenziale supera i 4 GB di RAM, indipendentemente dal carico effettivo dei join.

Linee guida pratiche:

- Mantenere il valore globale basso (256 KB – 1 MB) e aumentarlo a livello di sessione solo per query specifiche che ne beneficiano.
- Prima di aumentare il buffer, verificare se l'assenza di indice è intenzionale o un'omissione: un indice appropriato elimina il problema alla radice.
- Monitorare `Select_full_join` e `Select_range_check` in `SHOW GLOBAL STATUS` per quantificare la frequenza dei join senza indice.
