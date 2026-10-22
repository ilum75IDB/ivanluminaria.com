---
title: "default_pool_size"
description: "Parametro di PgBouncer che definisce il numero di connessioni reali a PostgreSQL per ogni coppia database/utente, cruciale per dimensionare il pool."
translationKey: "glossary_default_pool_size"
aka: null
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

`default_pool_size` è un parametro fondamentale di PgBouncer, un connection pooler leggero e performante per PostgreSQL. Questo parametro determina il numero massimo di connessioni *reali* che PgBouncer mantiene aperte verso il server PostgreSQL per ogni combinazione univoca di database e utente. È il fulcro per dimensionare correttamente il pool di connessioni e garantire un'efficiente gestione delle risorse.

## Cosa fa e come funziona

PgBouncer agisce da intermediario tra le applicazioni client e il server PostgreSQL. Invece di far aprire una nuova connessione a PostgreSQL per ogni richiesta client, PgBouncer mantiene un pool di connessioni pre-esistenti e le riutilizza. Il parametro `default_pool_size` controlla la dimensione di questo pool per ogni specifica coppia (database, utente).

Ad esempio, se `default_pool_size` è impostato a `20` e PgBouncer gestisce connessioni per `db1` con `user_a` e `db2` con `user_b`, manterrà fino a 20 connessioni per `(db1, user_a)` e altre 20 per `(db2, user_b)`. Questo meccanismo riduce l'overhead di creazione e chiusura delle connessioni, migliorando le performance e la scalabilità. Il parametro si applica indipendentemente dalla `pool_mode` (Session, Transaction, Statement).

Ecco un esempio di configurazione in `pgbouncer.ini`:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb
anotherdb = host=127.0.0.1 port=5432 dbname=anotherdb

[pgbouncer]
default_pool_size = 20
pool_mode = transaction
```

## Impatto e dimensionamento

Il corretto dimensionamento di `default_pool_size` è cruciale per le prestazioni complessive del sistema:

*   **Valore troppo basso**: Se il numero di connessioni disponibili nel pool è insufficiente rispetto alle richieste concorrenti, i client dovranno attendere che una connessione si liberi. Questo introduce latenza, riduce il throughput e può causare colli di bottiglia.
*   **Valore troppo alto**: Un `default_pool_size` eccessivo porta PgBouncer ad aprire troppe connessioni verso PostgreSQL. Ciò può sovraccaricare il server di database, consumando memoria e CPU per la gestione delle connessioni, e potenzialmente annullando i benefici del pooling.

Il dimensionamento ottimale dipende da vari fattori: il carico di lavoro (numero di query per secondo, durata delle transazioni), il numero di client concorrenti, la `pool_mode` utilizzata (Transaction pooling consente generalmente pool più piccoli ed efficienti) e le risorse hardware del server PostgreSQL. È consigliabile monitorare le statistiche di PgBouncer (es. `SHOW STATS`, `SHOW POOLS`) per osservare `waiting_clients` e l'utilizzo del pool, e aggiustare il valore in base alle esigenze reali.
