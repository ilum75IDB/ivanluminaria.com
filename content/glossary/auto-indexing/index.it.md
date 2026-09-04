---
title: "Auto-Indexing"
description: "Funzionalità Oracle (da 19c) che analizza il workload, crea indici invisibili e li promuove automaticamente se migliorano le performance."
translationKey: "glossary_auto_indexing"
aka: "Automatic Indexing (Oracle)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Auto-Indexing è una funzionalità introdotta in Oracle 19c che delega al database stesso la gestione del ciclo di vita degli indici: analisi del workload SQL, creazione sperimentale, validazione e promozione. In Oracle 21c il comportamento è diventato configurabile con maggiore granularità.

## Come funziona

Il processo si articola in tre fasi automatiche:

1. **Analisi** — Oracle monitora il workload tramite l'Automatic Workload Repository (AWR) e identifica le query candidate a beneficiare di nuovi indici.
2. **Creazione invisibile** — Gli indici candidati vengono creati come `INVISIBLE`, quindi non usati dall'ottimizzatore in condizioni normali.
3. **Validazione e promozione** — Oracle esegue test interni confrontando i piani di esecuzione. Se l'indice riduce il costo, viene promosso a `VISIBLE`; altrimenti rimane invisibile o viene eliminato.

```sql
-- Verifica lo stato dell'Auto-Indexing sul database
SELECT * FROM DBA_AUTO_INDEX_CONFIG;

-- Abilita / disabilita esplicitamente
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'IMPLEMENT');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'OFF');
```

## Contesto operativo

Auto-Indexing è pensato per ambienti OLTP con workload variabile o difficile da profilare manualmente. Su database di produzione con schemi stabili e indici già ottimizzati, il rischio è che vengano creati indici ridondanti che aumentano l'overhead di INSERT/UPDATE/DELETE e consumano spazio tablespace.

**Raccomandazione pratica**: in ambienti di produzione critici, valutare l'esecuzione in modalità `REPORT ONLY` prima di abilitare `IMPLEMENT`. Disabilitare esplicitamente con `OFF` se il DBA gestisce la strategia degli indici manualmente.

```sql
-- Modalità report: analizza ma non crea indici
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'REPORT ONLY');

-- Report degli indici gestiti automaticamente
SELECT INDEX_NAME, STATUS, AUTO
FROM DBA_INDEXES
WHERE AUTO = 'YES';
```
