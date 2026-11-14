---
categories:
- oracle
date: '2026-12-01'
description: 'Come Oracle SPM ha trasformato un report finanziario da 45 a 3 minuti:
  diagnosi di un piano subottimale, acquisizione della baseline e prevenzione delle
  regressioni.'
draft: false
image: oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire.cover.jpg
seoTitle: 'Oracle SQL Plan Management: stabilizzare i piani di esecuzione'
tags:
- oracle
- sql-plan-management
- performance-tuning
- optimizer
- oracle-19c
title: 'Oracle SQL Plan Management: stabilizzare i piani di esecuzione per prevenire
  regressioni in produzione'
translationKey: oracle_sql_plan_management_stabilizzare_i_piani_di_esecuzione_per_prevenire
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## La mattinata di Pietro e il report che "fa così da sempre"

Era una di quelle mattine rare in cui il telefono non squillava. Nessun alert, nessuna escalation, nessun DBA del cliente in panico. Pietro, un junior che lavora con me da qualche mese in un progetto presso un grande gruppo assicurativo italiano, si era avvicinato alla mia scrivania con quella curiosità un po' cauta che hanno i junior quando capiscono che l'esperto ha tempo.

"Posso chiederti una cosa su una query che mi ha incuriosito?"

La query in questione era il report del fatturato annuale — uno di quei report che il management board usa ogni settimana per monitorare i ricavi. Girava da anni. Quarantacinque minuti di esecuzione, ogni volta. Il team di sviluppo lo sapeva. Il PM lo sapeva. Il management lo sapeva. Era diventato parte del paesaggio, come il rumore del condizionatore in sala server: presente, accettato, ignorato.

Pietro aveva trovato la query nel repository e aveva notato che non sembrava particolarmente complessa. Quattro tabelle, qualche join, un aggregato. Perché ci volevano 45 minuti?

Ho risposto come rispondo sempre in questi casi: "Apriamo il piano di esecuzione e vediamo cosa sta facendo l'optimizer."

Non immaginavo che quella sessione didattica si sarebbe trasformata in una diagnosi operativa.

## Quello che l'optimizer stava facendo sotto il cofano

La query era questa, semplificata per leggibilità:

```sql
SELECT
    c.customer_name,
    SUM(il.amount) AS total_revenue
FROM
    FINANCE.CUSTOMERS c
JOIN
    SALES.INVOICES i ON c.customer_id = i.customer_id
JOIN
    SALES.INVOICE_LINES il ON i.invoice_id = il.invoice_id
WHERE
    i.invoice_date BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2025-12-31', 'YYYY-MM-DD')
GROUP BY
    c.customer_name
ORDER BY
    total_revenue DESC;
```

Le tabelle coinvolte non erano piccole: `SALES.INVOICES` aveva circa 150 milioni di righe, `SALES.INVOICE_LINES` circa 750 milioni, `FINANCE.CUSTOMERS` 5 milioni. Il filtro su `invoice_date` avrebbe dovuto ridurre drasticamente il dataset prima dei join — ma solo se l'optimizer avesse scelto il percorso giusto.

Ho estratto il piano corrente dalla cursor cache:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => '<sql_id>', format => 'ALLSTATS LAST'));
```

Il piano mostrava un Hash Join su `SALES.INVOICES` e `SALES.INVOICE_LINES` con Full Table Scan su entrambe le tabelle — prima ancora di applicare il filtro sulla data. L'optimizer stava leggendo 750 milioni di righe per poi scartarne la maggior parte.

"Perché fa così?" ha chiesto Pietro.

È una domanda giusta. L'optimizer non è stupido: ha scelto quel piano perché le statistiche che aveva a disposizione lo portavano a credere che fosse il percorso più efficiente. Il problema è che le statistiche erano cambiate — o meglio, erano state aggiornate in modo non rappresentativo dopo una raccolta massiva fatta durante una finestra di manutenzione, probabilmente con dati parziali. Il risultato: l'optimizer sovrastimava la selettività del filtro su `invoice_date` e sottostimava il costo del Full Table Scan sulle tabelle grandi.

Ho confrontato con gli snapshot AWR [1] delle settimane precedenti:

```sql
SELECT
    snap_id,
    plan_hash_value,
    elapsed_time_total / executions_total AS avg_elapsed_us
FROM
    DBA_HIST_SQLSTAT
WHERE
    sql_id = '<sql_id>'
ORDER BY
    snap_id DESC;
```

Il piano era cambiato circa tre settimane prima. Prima di quel momento, la stessa query girava in meno di 4 minuti con un piano diverso — Nested Loops con Index Range Scan su `SALES.INVOICES` (indice su `invoice_date`) e successivo Index Scan su `SALES.INVOICE_LINES`. Un piano molto più efficiente per questo pattern di accesso.

Pietro ha guardato i numeri in silenzio per qualche secondo. "Quindi la query non è lenta. È il piano che è sbagliato."

Esatto.

## SQL Plan Management: il concetto di baseline come ancora di stabilità

A questo punto ho introdotto SQL Plan Management [1], che è esattamente lo strumento pensato per situazioni come questa.

L'idea di fondo è semplice: Oracle mantiene un repository di piani di esecuzione approvati per ogni SQL statement, chiamato **SQL Plan Baseline**. Quando l'optimizer genera un nuovo piano per una query, lo confronta con la baseline. Se il nuovo piano non è nella baseline, viene marcato come "non verificato" (*unaccepted*) e non viene usato automaticamente — anche se l'optimizer lo ritiene migliore. Solo i piani esplicitamente accettati nella baseline vengono utilizzati in produzione.

Questo meccanismo crea una separazione netta tra "l'optimizer trova un piano nuovo" e "il piano nuovo va in produzione". Quella separazione è preziosa: ti dà il tempo di valutare, testare e decidere consapevolmente.

SPM opera su tre concetti fondamentali:

- **SQL Plan Baseline**: il set di piani accettati per uno specifico SQL statement, identificato dal suo `sql_id` o dal testo normalizzato.
- **Piano accettato** (*accepted*): un piano nella baseline che l'optimizer può usare.
- **Piano candidato** (*unaccepted*): un piano che l'optimizer ha trovato ma che non è ancora stato verificato e accettato.

Il parametro di sistema `OPTIMIZER_USE_SQL_PLAN_BASELINES` (default `TRUE`) controlla se l'optimizer consulta le baseline. Il parametro `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES` [3] (default `FALSE`) controlla se Oracle cattura automaticamente i piani delle query ripetute.

## Acquisire il piano buono dalla cursor cache

Il piano ottimale — quello con Nested Loops e Index Scan — era ancora nella cursor cache, associato a un `plan_hash_value` diverso da quello corrente. L'obiettivo era caricarlo nella baseline come piano accettato.

Il metodo più diretto è `DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE` [2]:

```sql
DECLARE
    v_plans_loaded PLS_INTEGER;
BEGIN
    v_plans_loaded := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
        sql_id          => '<sql_id>',
        plan_hash_value => <plan_hash_value_buono>
    );
    DBMS_OUTPUT.PUT_LINE('Piani caricati: ' || v_plans_loaded);
END;
/
```

La funzione restituisce il numero di piani caricati. Il piano viene inserito nella baseline con stato `ACCEPTED = YES` — pronto per essere usato dall'optimizer.

Per verificare cosa è nella baseline:

```sql
SELECT
    sql_handle,
    plan_name,
    accepted,
    enabled,
    fixed,
    created,
    last_modified
FROM
    DBA_SQL_PLAN_BASELINES
WHERE
    sql_text LIKE '%FINANCE.CUSTOMERS%'
ORDER BY
    created DESC;
```

A questo punto avevamo due piani nella baseline: quello buono (appena caricato, `ACCEPTED = YES`) e quello subottimale che l'optimizer stava usando. Il piano subottimale non era ancora nella baseline — era semplicemente il piano che l'optimizer sceglieva liberamente in assenza di vincoli.

Il passo successivo era assicurarci che l'optimizer usasse il piano buono e non tornasse a quello cattivo in futuro.

## Il processo di evoluzione: come SPM valuta i nuovi piani

Prima di disabilitare il piano subottimale, vale la pena capire come funziona il meccanismo di evoluzione [1] — perché è qui che SPM mostra la sua vera utilità a lungo termine.

Quando l'optimizer trova un piano non presente nella baseline, lo aggiunge come piano candidato (*unaccepted*). Quel piano non viene usato, ma viene conservato per una valutazione successiva. La procedura `DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE` [2] esegue questa valutazione: esegue il piano candidato in modo controllato e lo confronta con il piano accettato corrente. Se il candidato è significativamente più efficiente (per default, almeno il 1,5% più veloce), viene promosso ad *accepted*.

```sql
SET SERVEROUTPUT ON
DECLARE
    v_report CLOB;
BEGIN
    v_report := DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        time_limit  => 60,   -- secondi massimi per il test
        verify      => 'YES',
        commit      => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE(v_report);
END;
/
```

Il parametro `verify => 'YES'` fa sì che Oracle esegua effettivamente il piano candidato per misurarne le prestazioni. Con `commit => 'YES'`, se il piano supera la soglia, viene automaticamente accettato.

In questo caso specifico non avevamo bisogno di evoluzione automatica — il piano buono era già stato caricato come accettato. Ma è importante conoscere il meccanismo per i casi in cui si lavora con acquisizione automatica (`OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE`), dove i piani candidati si accumulano e vanno periodicamente valutati.

## Stabilizzare il piano ottimale e bloccare le regressioni future

Con il piano buono nella baseline, abbiamo fatto un ulteriore passo: marcarlo come `FIXED`. Un piano fixed ha precedenza assoluta — l'optimizer lo usa sempre, indipendentemente da qualsiasi altro piano nella baseline o da eventuali nuovi piani trovati.

```sql
DECLARE
    v_plans_modified PLS_INTEGER;
BEGIN
    v_plans_modified := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        plan_name   => '<plan_name_buono>',
        attribute_name  => 'fixed',
        attribute_value => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE('Piani modificati: ' || v_plans_modified);
END;
/
```

Dopo questa operazione, abbiamo eseguito la query in ambiente di test. Il piano scelto dall'optimizer era quello con Nested Loops e Index Range Scan su `invoice_date`. Tempo di esecuzione: poco meno di 3 minuti, contro i 45 minuti precedenti.

La variazione nel piano era netta: invece di leggere l'intera tabella `SALES.INVOICE_LINES` (750 milioni di righe) con un Full Table Scan, l'optimizer accedeva prima a `SALES.INVOICES` tramite l'indice su `invoice_date` — riducendo il dataset a qualche centinaio di migliaia di righe per l'anno selezionato — e poi eseguiva il join con `SALES.INVOICE_LINES` tramite Index Scan sull'`invoice_id`. Il filtro veniva applicato prima del join, non dopo.

Abbiamo lasciato il piano subottimale nella baseline con stato `ENABLED = NO` invece di eliminarlo, per conservare la storia e poterlo riabilitare in caso di necessità. Una scelta conservativa, ma sensata in produzione.

## Quando usare SPM: scenari e trade-off

Pietro ha fatto la domanda giusta a questo punto: "Ma se funziona così bene, perché non lo usiamo su tutte le query?"

La risposta onesta è che SPM ha un costo di gestione che non è trascurabile.

**Scenari in cui SPM è particolarmente utile**:

- **Pre e post upgrade di Oracle Database**: un upgrade può cambiare il comportamento dell'optimizer in modo significativo. Caricare le baseline prima dell'upgrade e verificarle dopo è una pratica consolidata.
- **Post-applicazione di patch**: le patch dell'optimizer (incluse nelle PSU/RU) possono alterare i piani. SPM permette di congelare i piani critici prima della patch.
- **Dopo raccolta massiva di statistiche**: come nel nostro caso. Una raccolta di statistiche non rappresentativa può degradare decine di query contemporaneamente.
- **Query critiche con SLA stringenti**: report finanziari, batch notturni, query di chiusura mensile — qualsiasi query per cui una regressione ha impatto diretto sul business.

**Trade-off da considerare**:

- Le baseline vanno manutenute. Se la struttura delle tabelle cambia (nuovi indici, partizioni, colonne), i piani nella baseline potrebbero diventare subottimali rispetto alla nuova struttura. Serve un processo di revisione periodica.
- Con `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE` a livello di sistema, i piani candidati si accumulano rapidamente. Senza un processo di evoluzione regolare, la baseline diventa un archivio ingestibile.
- SPM non è un sostituto delle statistiche corrette. È uno strumento di stabilizzazione, non di ottimizzazione. Il piano buono deve esistere e deve essere identificato: SPM lo conserva, non lo crea.

La strategia che abbiamo adottato è selettiva: baseline solo sulle query critiche identificate, con revisione trimestrale. Non acquisizione automatica a livello di sistema.

## Il report del lunedì mattina

Nei giorni successivi, il report del fatturato ha iniziato a girare in circa 3 minuti. Nessun annuncio, nessuna comunicazione preventiva al team di sviluppo.

Il primo a notarlo è stato uno degli analisti finanziari, che ha scritto in chat: "Il report del fatturato è già pronto? Di solito lo lancio e vado a prendere il caffè."

Il team di sviluppo ha chiesto cosa fosse cambiato. Abbiamo spiegato l'analisi, il piano subottimale, il meccanismo di SPM. È stata una conversazione utile — non perché il fix fosse complicato, ma perché ha aperto una discussione su come gestire le query critiche in modo proattivo, non solo reattivo.

Il management board ha notato il miglioramento nel report settimanale successivo. Nessun intervento eroico, nessuna emergenza risolta all'ultimo minuto. Solo un'analisi fatta in una mattinata tranquilla, grazie a una domanda di un junior curioso.

Pietro, da parte sua, ha capito qualcosa che i libri non insegnano facilmente: che spiegare un concetto a qualcuno ti costringe a guardarlo con occhi diversi. Mentre gli mostravo il piano di esecuzione, ho visto la lentezza con la stessa freschezza con cui la vedeva lui. Senza quella domanda, probabilmente avrei aperto un altro tab e sarei passato ad altro.

## Quello che resta nel runbook del team

Dopo quella mattinata, abbiamo aggiunto tre pratiche al runbook del team:

1. **Revisione trimestrale delle baseline SPM** sulle query critiche — verifica che i piani accettati siano ancora ottimali rispetto alla struttura corrente delle tabelle.
2. **Controllo dei piani AWR** prima e dopo ogni raccolta massiva di statistiche — confronto dei `plan_hash_value` per le query monitorate.
3. **Procedura di caricamento baseline pre-upgrade** — prima di qualsiasi upgrade o patch Oracle, le query critiche vengono identificate e i loro piani correnti caricati nella baseline come piano di fallback.

SPM non elimina il lavoro di tuning. Elimina la sorpresa: quella mattina in cui arrivi in ufficio e scopri che una query critica ha smesso di funzionare come ieri, senza che nessuno abbia toccato nulla.

## Fonti ufficiali

1. Oracle Database SQL Tuning Guide 19c — [Managing SQL Plan Baselines](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlad/managing-sql-plan-baselines.html)
2. Oracle Database PL/SQL Packages and Types Reference 19c — [DBMS_SPM](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPM.html)
3. Oracle Database Reference 19c — [OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES.html)
4. Oracle-Base (Tim Hall) — [SQL Plan Management (SPM) in Oracle Database](https://oracle-base.com/articles/11g/sql-plan-management-11gr1)

## Glossario
- **[SQL Plan Management (SPM)](/it/glossary/sql-plan-management/)** — Funzionalità di Oracle Database che permette di controllare e stabilizzare i piani di esecuzione delle query tramite un repository di piani approvati (baseline), prevenendo regressioni di performance dovute a variazioni dell'optimizer.

- **[SQL Plan Baseline](/it/glossary/awr/)** — Set di uno o più piani di esecuzione accettati per uno specifico SQL statement, memorizzato nel repository SPM. L'optimizer utilizza solo i piani presenti nella baseline, ignorando piani alternativi non ancora verificati.

- **[Piano fixed](/it/glossary/hash-join/)** (SPM) — Piano di esecuzione marcato con attributo `FIXED = YES` nella SQL Plan Baseline. Ha precedenza assoluta su tutti gli altri piani della baseline: l'optimizer lo seleziona sempre, indipendentemente da eventuali piani alternativi trovati.

- **[AWR](/it/glossary/sql-plan-management/)** (Oracle) — Automatic Workload Repository: snapshot periodici di metriche di workload, base degli AWR report e di ADDM. Conserva la storia dei piani di esecuzione tramite `DBA_HIST_SQLSTAT`, utile per identificare variazioni di piano nel tempo.

- **[Hash Join](/it/glossary/sql-plan-baseline/)** — Algoritmo di join utilizzato dall'optimizer Oracle per unire due tabelle costruendo una hash table in memoria sulla tabella minore e scansionando la tabella maggiore. Efficiente per grandi dataset senza indici selettivi; costoso quando applicato prima dei filtri selettivi.
