---
title: "ASSERTION"
description: "Vincolo di integrità dichiarativo SQL che valida un predicato sull'intero stato del database, anche su più tabelle simultaneamente."
translationKey: "glossary_assertion"
aka: "Constraint dichiarativo multi-tabella"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un ASSERTION è un vincolo di integrità dichiarativo introdotto da SQL-92 che esprime un predicato booleano sull'intero stato del database. A differenza di `CHECK` — limitato alla singola riga o al massimo alla singola tabella — un ASSERTION può coinvolgere più tabelle e aggregazioni, ed è violato se il predicato risulta `FALSE` dopo qualsiasi operazione DML o DDL.

## Come funziona

L'ASSERTION viene definito con `CREATE ASSERTION` e associato a uno schema. Il motore lo valuta al termine di ogni transazione (o, in alcune implementazioni, dopo ogni statement): se il predicato ritorna `FALSE`, la transazione viene respinta con ROLLBACK automatico.

```sql
CREATE ASSERTION max_ordini_per_cliente
CHECK (
  NOT EXISTS (
    SELECT cliente_id
    FROM ordini
    GROUP BY cliente_id
    HAVING COUNT(*) > 1000
  )
);
```

Il predicato può referenziare qualsiasi tabella visibile nello schema, usare subquery, aggregazioni e join. L'enforcement è a carico del motore, non dell'applicazione.

## Quando si usa

Gli ASSERTION coprono regole di business che non si possono esprimere con `CHECK` o `FOREIGN KEY`: limiti aggregati, invarianti cross-tabella, vincoli temporali su dati distribuiti su più entità. Il costo è reale: ogni transazione che tocca le tabelle referenziate può innescare la rivalutazione del predicato, con impatto sulle performance in scenari ad alto volume di scrittura.

SQL-92 li ha standardizzati, ma per decenni nessun RDBMS enterprise mainstream li ha implementati nativamente. Oracle 23ai/26ai rappresenta il primo caso di adozione in un motore di produzione di larga scala.
