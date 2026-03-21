---
title: "Sequential Scan"
description: "Operazione di lettura in cui PostgreSQL legge tutti i blocchi di una tabella senza utilizzare indici, efficiente su tabelle piccole ma problematica su tabelle grandi."
translationKey: "glossary_sequential-scan"
aka: "Seq Scan / Full Table Scan"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

Il **Sequential Scan** (Seq Scan) è l'operazione con cui PostgreSQL legge una tabella dall'inizio alla fine, blocco per blocco, senza utilizzare alcun indice. È l'equivalente PostgreSQL del Full Table Scan di Oracle.

## Quando è normale

Su tabelle piccole (poche migliaia di righe), il sequential scan è spesso la scelta più efficiente. Leggere una tabella intera in sequenza è più veloce che fare lookup su un indice quando la tabella sta in poche pagine. L'optimizer sceglie il sequential scan quando stima che sia più economico di un index scan.

## Quando è un problema

Su tabelle grandi (milioni di righe), un sequential scan per restituire poche righe è un segnale d'allarme. Significa che manca un indice appropriato o che le statistiche della tabella sono obsolete e l'optimizer fa stime sbagliate. pg_stat_statements aiuta a identificare queste situazioni mostrando le query con il peggior rapporto blocchi letti / righe restituite.

## Come diagnosticarlo

EXPLAIN mostra "Seq Scan on tabella" nel piano di esecuzione. Se il filtro successivo scarta la maggior parte delle righe (rows removed by filter >> rows), quasi certamente serve un indice sulla colonna del filtro.
