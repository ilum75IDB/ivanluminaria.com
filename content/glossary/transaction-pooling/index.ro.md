---
title: "Transaction Pooling"
description: "Mod de pooling în care backend-ul este alocat clientului doar pe durata unei tranzacții, maximizând reutilizarea conexiunilor reale la baza de date."
translationKey: "glossary_transaction_pooling"
aka: "Transaction-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

Transaction Pooling este modul de pooling cel mai agresiv disponibil în instrumente precum PgBouncer: o conexiune fizică la backend-ul PostgreSQL este alocată unui client doar pentru intervalul necesar finalizării unei singure tranzacții. Imediat ce apare COMMIT sau ROLLBACK, backend-ul revine în pool și devine disponibil pentru orice alt client care așteaptă.

## Cum funcționează

Din perspectiva clientului, conexiunea pare persistentă. Intern, pooler-ul urmărește limitele tranzacțiilor și reasignează backend-ul fizic la fiecare ciclu. Cu 1000 de clienți conectați și tranzacții de scurtă durată, pot fi suficiente 20–50 de conexiuni reale către PostgreSQL.

Parametrul esențial în PgBouncer este `pool_mode = transaction`, configurabil global sau per bază de date:

```ini
[databases]
mydb = host=127.0.0.1 port=5432 pool_mode=transaction
```

## Când se folosește și limitările sale

Este alegerea standard pentru aplicațiile web cu concurență ridicată — de obicei un backend cu propriul pool de conexiuni, plasat în spatele PgBouncer, care la rândul său se conectează la PostgreSQL. Reduce drastic numărul de procese backend active, scăzând consumul de memorie și overhead-ul de context switching.

Limitările sunt concrete: orice funcționalitate care depinde de starea sesiunii pe server — prepared statements de pe server, variabile de sesiune setate cu `SET`, advisory locks, cursori `WITH HOLD` — nu funcționează corect în Transaction Pooling, deoarece sesiunea backend se schimbă între tranzacții. Soluția este fie utilizarea Session Pooling pentru acele workload-uri, fie dezactivarea funcționalităților incompatibile la nivelul aplicației.
