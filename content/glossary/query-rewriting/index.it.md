---
title: "Query Rewriting"
description: "Funzionalità Oracle che redirige automaticamente una query sulle tabelle base verso una Materialized View equivalente, senza toccare il codice applicativo."
translationKey: "glossary_query_rewriting"
aka: "Automatic Query Rewriting"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

Il Query Rewriting è una funzionalità del query optimizer di Oracle che intercetta una query SQL diretta alle tabelle base e la redirige in modo trasparente verso una Materialized View (MV) che contiene già il risultato pre-calcolato. L'applicazione non sa nulla di questa sostituzione: invia la stessa query di sempre, riceve i dati più velocemente.

## Come funziona

Quando si crea o altera una MV con `ENABLE QUERY REWRITE`, si autorizza l'optimizer a usarla come fonte alternativa. Oracle verifica che la MV sia semanticamente equivalente alla query in arrivo — stesse aggregazioni, stesse colonne, stessa logica di filtro — e, se la corrispondenza regge, sostituisce il piano di esecuzione.

```sql
CREATE MATERIALIZED VIEW mv_traffico_giornaliero
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT data_chiamata, id_cella, SUM(durata_sec) AS totale_durata
FROM fatto_chiamate
GROUP BY data_chiamata, id_cella;
```

Dopo questa definizione, una query `SELECT data_chiamata, SUM(durata_sec) FROM fatto_chiamate GROUP BY data_chiamata` può essere risolta leggendo la MV invece della tabella base, se l'optimizer ritiene conveniente farlo.

## Quando si usa

Il Query Rewriting è utile nei Data Warehouse con query analitiche pesanti e frequenti sulle stesse aggregazioni. Il prerequisito fondamentale è che la MV sia **fresca**: se i dati sono obsoleti rispetto alla tabella base, Oracle può scegliere di non usarla (comportamento controllabile tramite il parametro `QUERY_REWRITE_INTEGRITY`). Va abilitato anche il parametro di sessione/sistema `QUERY_REWRITE_ENABLED`. In ambienti con refresh frequenti o near-real-time, il beneficio si riduce e occorre bilanciare il costo del refresh con il guadagno in lettura.
