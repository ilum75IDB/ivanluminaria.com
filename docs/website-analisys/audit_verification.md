# Audit Verification — verifica empirica delle analisi esterne

**Data inizio**: 2026-05-14
**Scopo**: verificare empiricamente i claim dei due audit esterni (`Analisi Sito Web e Strategia Digitale.md` + `audit_ivanluminaria.md`) per costruire una roadmap di interventi che diano valore reale, non "best practice generiche".

**Metodologia**:
- Verifica con strumenti (grep, curl, lettura codice, Read multimodal)
- Distinzione tra: **claim verificato**, **claim falso/datato**, **claim parziale**, **non verificabile**
- Per ciascun item: priorità (P0/P1/P2/Skip), effort stimato, eventuale issue GitHub da aprire
- Modifiche stilistiche per articolo annotate ma NON applicate (decisione utente: vediamo prima, applichiamo dopo in una botta)

**Convenzione del file**:
- Le sezioni vengono compilate progressivamente. Ogni sezione inizia con `## ` e finisce con `**STATO**: <da-fare|in-corso|completata>` per riprese post-timeout.

---

## 📋 Log attività

| # | Attività | Stato | Commit |
|---|---------|-------|--------|
| 0 | Setup framework | ✅ completato | (questo commit) |
| 1 | Verifica infra: tag bloat | ✅ completato (126 tag/35 art, 89 thin) | audit-verify: 1.1 |
| 2 | Verifica infra: carrello/shop orfano | ✅ completato (claim FALSO) | audit-verify: 1.2 |
| 3 | Verifica infra: structured data | ✅ completato (bug double-quoting) | audit-verify: 1.3 |
| 4 | Verifica infra: hreflang + canonical | ✅ completato (tutto OK) | audit-verify: 1.4 |
| 5 | Verifica infra: sitemap + robots.txt | ✅ completato (tutto OK) | audit-verify: 1.5 |
| 6 | Verifica P0 tech: Oracle Unified Audit | ✅ VERO, P0 | audit-verify: 2.1 |
| 7 | Verifica P0 tech: Galera durabilità | ✅ VERO, P0 | audit-verify: 2.2 |
| 8 | Verifica P0 tech: CSV con sed | ✅ VERO, P0 | audit-verify: 2.3 |
| 9 | Verifica P0 tech: Oracle partitioning CTAS | ✅ VERO, P0 | audit-verify: 2.4 |
| 10 | Verifica Media tech: expire_logs_days | ✅ parziale, P1 | audit-verify: 2.5 |
| 11 | Verifica Media tech: Data Guard / Active DG | ✅ parziale, P1 | audit-verify: 2.6 |
| 12 | Verifica Media tech: grants in stored proc | ✅ omissione, P2 | audit-verify: 2.7 |
| 13 | Verifica Media tech: anonymous user MySQL | ✅ VERO, P1 | audit-verify: 2.8 |
| 14 | Verifica Media tech: default_statistics_target | ✅ VERO, P0 | audit-verify: 2.9 |
| 15 | Verifica Media tech: CREATE INDEX CONCURRENTLY | ✅ basso impatto, P2 | audit-verify: 2.10 |
| 16 | Lista affermazioni assolute | ✅ parziale, P2 (mitigare solo titolo pg_stat_statements) | audit-verify: 3 |
| 17 | Revisione stilistica: section Oracle (annotazioni) | da fare | — |
| 18 | Revisione stilistica: section MySQL (annotazioni) | da fare | — |
| 19 | Revisione stilistica: section PostgreSQL (annotazioni) | da fare | — |
| 20 | Revisione stilistica: section Data Warehouse (annotazioni) | da fare | — |
| 21 | Revisione stilistica: section Project Management (annotazioni) | da fare | — |
| 22 | Tabella consolidata finale + roadmap | da fare | — |

**Convenzione stato**:
- `da fare` → non ancora iniziato
- `in-corso` → iniziato, non finito (se vedi questo dopo un timeout, riprendi da qui)
- `✅ completato` → fatto, risultati nella sezione corrispondente

---

## 1. Verifiche infrastrutturali

### 1.1 Tag bloat
**Claim Analista B**: "112 tag per 31 articoli" → rapporto 3.6 tag/articolo, troppi pagine sottili.

**Verifica empirica (2026-05-14)**:
- **126 tag unici** per **35 articoli IT** → rapporto 3.6 tag/articolo (confermato, peggiorato in valore assoluto perché il sito è cresciuto)
- **89 tag (71%)** hanno **un solo articolo** → ognuno produce una pagina `/tags/<slug>/` con 1 link → thin content perfetto
- **26 tag (21%)** hanno 2 articoli
- Solo **11 tag (8%)** hanno 3+ articoli (`performance` 9, `tuning` 5, `data-warehouse` 5, `oracle` 4, `mariadb` 4, `dimensional-modeling` 4, `security` 3, `query-tuning` 3, `privileges` 3, `kimball` 3, `consulting` 3)

**Verdetto**: claim **VERIFICATO** e peggiore del segnalato. Le 89 tag-page con 1 solo articolo sono:
- SEO penalty (thin content)
- Diluiscono il PageRank interno
- Confondono l'utente nella navigazione `/tags/`

**Proposta intervento**:
- **P1**: ridurre a un set di ~25-30 tag strategici (gli 11 "forti" + 15-20 selezionati con cura)
- Tag con 1 articolo: o assorbire in tag esistente, o noindex (più conservativo)
- Mantenere le categorie come navigazione principale SEO (già fanno il lavoro)
- Issue da aprire: "Tag governance: consolidare i tag da 126 a ~30, applicare noindex ai residui"

**Effort**: M (3-4 ore — rivedere 35 articoli, scegliere tag canonici, aggiornare frontmatter)
**Rischio**: Basso (refactoring di metadati, non cambia contenuto)

**STATO**: ✅ completato

---

### 1.2 Carrello / Shop orfano
**Claim Analista A**: "presenza di un'icona del carrello o riferimenti a uno 'Shop' senza prodotti".

**Verifica empirica (2026-05-14)**:
- Grep su tutti i template `layouts/`, asset `assets/`, configurazione `config/`: nessun riferimento a `cart`, `shop`, `carrello`, `basket`, `checkout`, `shoppingcart`, `fa-shopping`, `bi-cart`.
- Curl sulla home live: nessun risultato per pattern shop/cart.

**Verdetto**: claim **FALSO**. Probabilmente l'Analista A ha confuso con un altro sito, o ha letto un'esempio del tema Congo (che è e-commerce-ready ma noi non l'abbiamo attivato).

**Proposta intervento**: **NESSUNO**. Skip.

**STATO**: ✅ completato

---

### 1.3 Structured data (JSON-LD)
**Claim Analista B**: implementare/validare `BlogPosting`, `Person`, `ProfilePage`, `BreadcrumbList`, `Organization`, `WebSite`, `ImageObject`.

**Verifica empirica (2026-05-14)** su `https://ivanluminaria.com/it/posts/postgresql/pg-stat-statements/`:

**Presenti**:
- ✅ `Article` (con `headline`, `description`, `datePublished`, `dateModified`, `inLanguage`)
- ✅ `ImageObject` (annidata in `image`, con `url`, `width`, `height`)
- ✅ `Person` (annidata in `author`, con `name`, `url`, `jobTitle`)
- ✅ `Organization` (annidata in `publisher`, con `name`, `url`)
- ✅ `WebPage` (annidata in `mainEntityOfPage` con `@id`)
- ✅ `BreadcrumbList` (separato, con 5 ListItem)

**🚨 BUG IMPORTANTE — Double-quoting nel JSON-LD**:
I valori sono wrappati con **doppi apici di troppo**:
```json
"headline":"\"pg_stat_statements: la prima cosa da installare su qualsiasi PostgreSQL\""
                ↑                                                                          ↑
                doppio quoting non corretto
```
Stesso problema per: `description`, `datePublished`, `dateModified`, `inLanguage`, `image.url`, `mainEntityOfPage.@id`, e tutti gli `ListItem.name/item` del BreadcrumbList.

**Conseguenze**:
- Il JSON è formalmente valido (le doppie virgolette sono escapate)
- MA Google Rich Results Test e Schema.org validator probabilmente registrano valori come stringhe con virgolette letterali — i metadati funzionano in modo degradato
- Non bloccante per l'indicizzazione, ma rich results potrebbero non apparire o apparire male

**Proposta intervento**: **P1** — fix dei template Hugo che generano JSON-LD (probabilmente `layouts/_partials/head.html` o un override Congo).

**Effort**: S (1 ora — trovare il template, togliere il quoting `printf "%q"` o `jsonify` ridondante, testare)
**Rischio**: Basso

**STATO**: ✅ completato

---

### 1.4 Hreflang reciproci e canonical
**Claim Analista B**: verificare che ogni pagina abbia hreflang reciproci self-referencing.

**Verifica empirica (2026-05-14)** su `https://ivanluminaria.com/it/posts/postgresql/pg-stat-statements/`:

**Hreflang trovati nella `<head>`**:
```html
<link rel=alternate hreflang=it href=https://ivanluminaria.com/it/posts/postgresql/pg-stat-statements/>
<link rel=alternate hreflang=en href=https://ivanluminaria.com/en/posts/postgresql/pg-stat-statements/>
<link rel=alternate hreflang=es href=https://ivanluminaria.com/es/posts/postgresql/pg-stat-statements/>
<link rel=alternate hreflang=ro href=https://ivanluminaria.com/ro/posts/postgresql/pg-stat-statements/>
<link rel=alternate hreflang=x-default href=https://ivanluminaria.com/en/posts/postgresql/pg-stat-statements/>
```

✅ Tutti i 4 hreflang presenti + `x-default` → EN
✅ La pagina IT include il **self-referencing** (`hreflang=it` punta a sé)

**Canonical trovato**:
```html
<link rel=canonical href=https://ivanluminaria.com/it/posts/postgresql/pg-stat-statements/>
```

✅ Canonical self-referencing per la versione IT (non punta erroneamente alla EN come temeva l'Analista B)

**Verdetto**: claim **NON CONFERMATO** (era una preoccupazione preventiva, in realtà tutto è già corretto). Skip.

**STATO**: ✅ completato

---

### 1.5 Sitemap + robots.txt
**Claim Analista B**: verificare che sitemap esista, sia raggiungibile, contenga tutte le lingue, sia citata in robots.txt.

**Verifica empirica (2026-05-14)**:

**robots.txt** (`https://ivanluminaria.com/robots.txt`):
```
User-agent: *
Allow: /
Sitemap: https://ivanluminaria.com/sitemap.xml
```
✅ Esiste, raggiungibile, contiene il riferimento al sitemap

**sitemap.xml root** (`https://ivanluminaria.com/sitemap.xml`):
- ✅ HTTP 200 + `content-type: application/xml`
- ✅ È un **sitemap index** con 4 sub-sitemap (uno per lingua: IT, EN, ES, RO), ciascuno con `<lastmod>` aggiornato

**sub-sitemap** (`https://ivanluminaria.com/it/sitemap.xml`):
- ✅ Ogni URL ha i 4 `xhtml:link rel="alternate" hreflang="..."` per le altre lingue + self-referencing

**Verdetto**: claim **NON CONFERMATO** (preoccupazione preventiva). Tutto già configurato correttamente da Hugo+Congo. Skip.

**STATO**: ✅ completato

---

## 2. Verifiche errori tecnici (P0/Media secondo Analista B)

### 2.1 Oracle Unified Audit — `ALTER AUDIT POLICY ENABLE` vs `AUDIT POLICY`
**File**: `content/posts/oracle/oracle-roles-privileges/index.it.md` (+ 3 traduzioni)
**Claim Analista B**: la sintassi corretta è `AUDIT POLICY nome_policy` (Oracle docs CREATE AUDIT POLICY).

**Verifica empirica (2026-05-14)**:
L'articolo usa 3 volte `ALTER AUDIT POLICY ... ENABLE` (righe 225, 233, 238):
```sql
ALTER AUDIT POLICY pol_ddl_critico ENABLE;       -- riga 225
ALTER AUDIT POLICY pol_accesso_dati ENABLE;      -- riga 233
ALTER AUDIT POLICY pol_login_falliti
ENABLE WHENEVER NOT SUCCESSFUL;                  -- righe 238-239
```

**Documentazione Oracle 19c**:
- [CREATE AUDIT POLICY](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-AUDIT-POLICY-Unified-Auditing.html): crea la policy
- [AUDIT (Unified)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/AUDIT-Unified-Auditing.html): la **abilita** — sintassi `AUDIT POLICY policy_name [BY user | EXCEPT user] [WHENEVER {SUCCESSFUL | NOT SUCCESSFUL}];`
- [ALTER AUDIT POLICY](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/ALTER-AUDIT-POLICY-Unified-Auditing.html): **modifica** la policy esistente (aggiungere/rimuovere azioni, privilegi, ruoli) — non ha clausola `ENABLE`

**Verdetto**: claim **VERO**. L'articolo contiene un errore di sintassi DDL Oracle. La forma corretta è:
```sql
AUDIT POLICY pol_ddl_critico;
AUDIT POLICY pol_accesso_dati;
AUDIT POLICY pol_login_falliti WHENEVER NOT SUCCESSFUL;
```

Per disabilitare si userebbe `NOAUDIT POLICY nome_policy`.

**Proposta intervento**: **P0** — correggere subito (errore tecnico in articolo già pubblicato dal 2026-01-27, target Oracle DBA → credibilità a rischio)
- Correzione in IT, EN, ES, RO
- Effort: S (15 minuti, sostituzione di 6 occorrenze totali su 4 lingue)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.2 Galera Cluster — durabilità con `innodb_flush_log_at_trx_commit=2`
**File**: `content/posts/mysql/galera-cluster-3-nodi/index.it.md` (riga 145-149)
**Claim Analista B**: dire che è "garantita dalla replica sincrona" è troppo forte; va espresso come trade-off.

**Verifica empirica (2026-05-14)**:

Riga 147 dell'articolo:
> Il valore 1 (default) garantisce durabilità totale — ogni commit viene scritto e fsynced sul disco. **Ma in un cluster Galera, la durabilità è già garantita dalla replica sincrona su tre nodi.** Il valore 2 scrive nel buffer del sistema operativo ad ogni commit e fa fsync solo ogni secondo, migliorando le performance di scrittura del 30-40% nei nostri test.

Riga 149:
> Se perdi un nodo, i dati sono sugli altri due. Se perdi il datacenter intero... beh, quello è un altro discorso.

**Analisi tecnica**:
- Con `innodb_flush_log_at_trx_commit=2`, i redo log vanno nel buffer OS ad ogni commit, ma l'`fsync` (flush al disco) avviene **una volta al secondo**
- In caso di **crash del SO / power loss su un nodo**, si possono perdere fino a 1 secondo di transazioni sul nodo locale (la replica Galera mitiga ma non risolve completamente — la certification è pre-commit, il flush sul disco no)
- Se TUTTI i 3 nodi hanno power loss contemporaneo (datacenter), si possono perdere transazioni — l'articolo accenna a questo a riga 149 ma in modo evasivo

**Verdetto**: claim **VERO ma con attenuazione**. L'articolo già accenna al limite ("quello è un altro discorso"), MA la frase "**la durabilità è già garantita**" è troppo assoluta per un lettore senior. Va riformulata come **trade-off**, non come equivalenza.

**Riformulazione proposta** (versione mitigata):
> Il valore 1 (default) garantisce durabilità totale anche su crash di OS o power loss del singolo nodo. In un cluster Galera, la replica sincrona su tre nodi **mitiga** il rischio: anche se un nodo perde l'ultimo secondo di transazioni in un crash, le altre due copie hanno i dati certificati prima del commit. Il valore 2 è quindi un **compromesso ragionevole** in questo contesto, non un equivalente di 1 — il margine di rischio resta sui crash simultanei (power loss del datacenter, manutenzione coordinata mal pianificata).

**Proposta intervento**: **P0** — correzione testuale di un paragrafo in 4 lingue.
- Effort: S (20 minuti, 4 traduzioni)
- Rischio: Nessuno (miglioramento della qualità tecnica)

**STATO**: ✅ completato

---

### 2.3 MySQL CSV con sed
**File**: `content/posts/mysql/mysql-multi-istanza-secure-file-priv/index.it.md` (righe 214-226)
**Claim Analista B**: `sed 's/\t/,/g'` non è CSV-safe se i campi contengono virgole/newline/quote.

**Verifica empirica (2026-05-14)**:

Riga 225 dell'articolo:
```bash
" gestionale_prod | sed 's/\t/,/g' > /tmp/export_ordini.csv
```

**Caso d'uso**: export tabella `ordini` da un gestionale (descrizioni cliente, indirizzi, importi, note di fattura).

**Problemi reali**:
1. **Virgole nei campi** (alta probabilità in indirizzi, ragioni sociali, descrizioni note): `Via Garibaldi, 12` diventa `Via Garibaldi","12"` — un campo si trasforma in due
2. **Newline nei campi** (rara ma possibile in note multi-riga): spezza la riga CSV
3. **Virgolette nei campi**: non vengono escapate
4. **Apostrofi nei campi** (es. `D'Angelo`): nessun problema con sed, ma niente quoting

**Verdetto**: claim **VERO**. Il `sed` produce un file con estensione `.csv` ma che **non è CSV RFC 4180 compliant** — apre male in Excel/LibreOffice se i campi contengono virgole.

**Soluzioni alternative** (in ordine di robustezza):
1. **Best**: usare `mysql --csv` (esiste? no, non c'è il flag nativo). Però `mysql --batch --raw` + tool csv: `mysql --batch | mlr --tsvlite --ocsv cat` (richiede miller)
2. **Buono**: pipe a Python con `csv.writer`:
   ```bash
   mysql -B -e "..." | python3 -c "import sys,csv; w=csv.writer(sys.stdout); [w.writerow(l.rstrip().split('\t')) for l in sys.stdin]"
   ```
3. **Buono**: tenere TSV come output e rinominare `.tsv`, segnalando al richiedente che è tab-separated (Excel apre i TSV correttamente con `Apri → da testo`)
4. **Server-side**: `SELECT ... INTO OUTFILE ... FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'`, ma è bloccato da secure_file_priv (è il problema centrale dell'articolo)

**Proposta intervento**: **P0** — l'articolo è pubblicato dal 2025-11-04, target enterprise. Un DBA che copia/incolla quel sed e poi ha dati sporcati passa una brutta giornata.
- Aggiungere caveat sul caso "campo contiene virgole/newline/quotes"
- Proporre la soluzione Python (poche righe, no dipendenze esterne)
- Mantenere il sed come "quick hack se sei sicuro dei dati"
- Effort: M (1 ora, 4 traduzioni con esempio Python)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.4 Oracle partitioning — CTAS + rename con DML concorrente
**File**: `content/posts/oracle/oracle-partitioning/index.it.md` (Step 1-3)
**Claim Analista B**: CTAS + rename non è consistente senza freeze scritture o DBMS_REDEFINITION.

**Verifica empirica (2026-05-14)**:

L'articolo (titolo: "Oracle Partitioning: quando 2 miliardi di righe non entrano più in una query") descrive:
- **Step 1**: `CREATE TABLE txn_movimenti_part ... AS SELECT ... FROM txn_movimenti` (CTAS con PARALLEL 8)
- **Step 3**: `ALTER TABLE txn_movimenti RENAME TO txn_movimenti_old; ALTER TABLE txn_movimenti_part RENAME TO txn_movimenti;`
- **Riga 194**: *"Il downtime effettivo è stato il tempo dei due `ALTER TABLE RENAME`: qualche secondo. Tutto il resto — la copia dei dati, la creazione degli indici — è **avvenuto in parallelo con il sistema attivo**."*

**Problema serio**:
Se "il sistema è attivo" durante il CTAS, la tabella sorgente riceve INSERT/UPDATE/DELETE. Conseguenze:
- Le **righe inserite** dopo l'inizio del CTAS sulla sorgente **NON** sono nella nuova tabella
- Gli **UPDATE** sulle righe già copiate (nella sorgente) **NON** sono propagati alla nuova tabella
- Le **DELETE** sulla sorgente **NON** sono propagate
- Al momento del rename, la nuova tabella ha lo **snapshot di T0** (inizio del CTAS), non il T1 (momento del rename) → **perdita dati** o **incoerenza** dal punto di vista applicativo

L'articolo a riga 101 dice *"non puoi fare ALTER TABLE ... PARTITION BY su una tabella esistente... non senza l'opzione Online Table Redefinition. E quella opzione, su una tabella di queste dimensioni, ha i suoi rischi."* — quindi **DBMS_REDEFINITION viene esplicitamente scartato senza spiegare come gestire l'incoerenza**.

**Verdetto**: claim **VERO e serio**. L'articolo descrive un approccio che funziona solo se la tabella è **read-only** durante il CTAS (es. tabella storica), ma il testo dà l'impressione che si possa fare con sistema in produzione attivo. Per un target Oracle DBA enterprise, questo è il tipo di errore che fa perdere credibilità.

**Strategie corrette** (da menzionare nell'articolo, anche solo per riferimento):
1. **DBMS_REDEFINITION** (Online Table Redefinition): l'opzione Oracle ufficiale per fare partitioning su tabelle attive (gestisce automaticamente i delta tramite Materialized View Log)
2. **Freeze applicativo + CTAS + cutover veloce**: se accettabile un breve downtime (es. weekend)
3. **CDC con Materialized View Log custom**: per chi non vuole/può usare DBMS_REDEFINITION
4. **Exchange Partition** (per tabelle già parzialmente partizionate): swap istantaneo

**Proposta intervento**: **P0** — articolo pubblicato dal 2025-12-09. Inserire box "⚠️ Avvertenza": chiarire che l'approccio descritto richiede **tabella sorgente in stato read-only** durante il CTAS, e elencare brevemente le alternative quando la tabella deve restare attiva.
- Effort: M (1 ora — paragrafo nuovo con riferimenti, 4 lingue)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.5 MySQL binary log — `expire_logs_days` vs `binlog_expire_logs_seconds`
**File**: `content/posts/mysql/binary-log-mysql/index.it.md` (+ `mysql-pre-upgrade-assessment`)
**Claim Analista B**: `expire_logs_days` legacy/deprecato in MySQL 8.

**Verifica empirica (2026-05-14)**:

**`binary-log-mysql/index.it.md` (righe 171-187)**: ✅ già corretto. L'articolo distingue esplicitamente:
- Sezione `### expire_logs_days (legacy)`
- Sezione `### binlog_expire_logs_seconds (MySQL 8.0+)`
- Nota chiara: *"Da MySQL 8.0, questo parametro ha priorità su expire_logs_days. Se le imposti entrambe, vince binlog_expire_logs_seconds."*

**`mysql-pre-upgrade-assessment/index.it.md` (riga 99)**: ⚠️ usa solo `expire_logs_days=7` senza menzionare l'evoluzione MySQL 8:
> Con `expire_logs_days=7` hai una settimana di storico pronta da leggere.

**Verdetto**: claim **VERO ma parziale**. L'articolo principale è già OK, va corretto solo `mysql-pre-upgrade-assessment`. Modifica minima.

**Proposta intervento**: **P1** (basso impatto, target spesso usa ancora 5.7).
- Aggiornare il riferimento in `mysql-pre-upgrade-assessment` con un breve inciso (es. "con `expire_logs_days=7`, o `binlog_expire_logs_seconds=604800` da MySQL 8.0").
- Effort: XS (5 minuti, 4 traduzioni di una sola frase)

**STATO**: ✅ completato

---

### 2.6 Oracle Data Guard vs Active Data Guard
**File**: `content/posts/oracle/oracle-data-guard/index.it.md` (+ `oracle-cloud-migration`)
**Claim Analista B**: real-time query con standby aperto in read-only mentre applica redo richiede licenza Active Data Guard.

**Verifica empirica (2026-05-14)**:

**`oracle-data-guard/index.it.md`**:
- Riga 33 (intro): *"lo standby si può anche usare in sola lettura — per report, per backup, per alleggerire il carico"* — frase ambigua, implica Active Data Guard senza dirlo
- Riga 228: cita "Active Data Guard" correttamente nel paragrafo sui temp tablespace
- Riga 245: tabella che distingue "Active Data Guard" come feature separata

**Stato**: la distinzione esiste già nell'articolo, ma non all'inizio. Un lettore che si ferma all'introduzione potrebbe pensare che lo standby read-only mentre applica redo sia incluso nel Data Guard base.

**Documentazione Oracle**:
- [Data Guard base](https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/getting-started-with-oracle-data-guard.html): standby in MOUNT (apply attivo, non query) **oppure** read-only ma con apply fermo
- **Active Data Guard** (opzione separata a pagamento): real-time query (read-only + apply concorrente), automatic block media recovery, Far Sync

**`oracle-cloud-migration/index.it.md`**:
- Riga 31-33, 121: il licensing OCI/BYOL è già trattato esplicitamente
- Riga 133: *"Il licensing Oracle in cloud è un campo minato... bisogna parlare con Oracle, ottenere conferme scritte"* → già un warning chiaro

**Verdetto**: claim **VERO ma parziale**. L'articolo `oracle-cloud-migration` è già a posto. L'articolo `oracle-data-guard` ha la distinzione, ma è "nascosta" nel testo, va spostata in apertura.

**Proposta intervento**: **P1** — aggiungere a inizio articolo Data Guard un box/inciso esplicito:
> ℹ️ **Nota su licensing**: il *real-time query* (standby aperto in read-only mentre applica redo) richiede l'opzione **Active Data Guard**, separata dal Data Guard base incluso in Enterprise Edition.
- Effort: S (15 minuti, 4 traduzioni)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.7 Oracle grants tramite role in stored proc definer-rights
**File**: `content/posts/oracle/oracle-roles-privileges/index.it.md`
**Claim Analista B**: i privilegi via role non sono disponibili in stored proc definer-rights.

**Verifica empirica (2026-05-14)**:

L'articolo descrive il modello GRANT/role/object privilege per separare letture/scritture/admin. Non parla mai esplicitamente di stored procedure con definer-rights.

**La regola Oracle**: i privilegi concessi tramite **role** sono attivi solo a livello di sessione interattiva. Dentro **stored procedure compilate con definer rights** (default), il motore considera solo i privilegi **diretti** concessi all'owner della proc. I privilegi via role **non funzionano**.

Esempio:
```sql
GRANT SELECT ON app_owner.tabella TO app_read_role;
GRANT app_read_role TO app_user;
-- app_user può fare SELECT in sessione interattiva: OK
-- ma se ha una stored proc che fa SELECT su tabella: ORA-00942
-- Soluzione: GRANT SELECT ON app_owner.tabella TO app_user (diretto)
-- Oppure: AUTHID CURRENT_USER (invoker-rights) sulla proc
```

**Verdetto**: claim **VERO ma non un errore, un'omissione**. L'articolo è corretto su quello che dice, ma manca un caveat importante per chi sviluppa PL/SQL.

**Proposta intervento**: **P2** — aggiungere paragrafo "⚠️ Avvertenza: privilegi via role e stored procedure" con esempio + spiegazione `AUTHID CURRENT_USER` come alternativa.
- Effort: M (45 minuti, 4 traduzioni)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.8 MySQL anonymous user
**File**: `content/posts/mysql/mysql-users-and-hosts/index.it.md` (righe 187-203)
**Claim Analista B**: l'anonymous user non è "sempre" creato, dipende dall'installazione.

**Verifica empirica (2026-05-14)**:

L'articolo a riga 187 afferma:
> MySQL **viene installato** con un utente anonimo: `''@'localhost'`. Nessun nome, nessuna password.

E nella mini-pagina del glossario (riga 244):
> Utente MySQL senza nome creato **automaticamente** durante l'installazione.

**Realtà tecnica**:
- **MySQL 5.7 e precedenti**: l'anonymous user veniva creato di default
- **MySQL 8.0+** (con `mysql_secure_installation` o pacchetti recenti): NON viene creato di default
- **MariaDB**: dipende dalla distribuzione (alcune lo creano, altre no)
- **Container Docker MySQL**: di solito non lo crea
- **`mysql_install_db --auth-root-authentication-method=normal`**: parametro che influenza

**Verdetto**: claim **VERO ma parziale**. L'affermazione "viene installato con un utente anonimo" è troppo assoluta. È vero come **tendenza storica**, falso in molti scenari moderni.

**Proposta intervento**: **P1** — mitigare l'affermazione.
- Modifica riga 187: *"MySQL può essere installato con un utente anonimo `''@'localhost'`, soprattutto in installazioni legacy o di sviluppo."*
- Aggiungere check di verifica prima del DROP: *"SELECT user, host FROM mysql.user WHERE user='';"*
- Mitigare anche il glossario
- Effort: S (15 minuti, 4 traduzioni)

**STATO**: ✅ completato

---

### 2.9 PostgreSQL `default_statistics_target`
**File**: `content/posts/postgresql/explain-analyze-postgresql/index.it.md` (righe 146-148, 230)
**Claim Analista B**: non è "100 righe campione" ma target per MCV/histogram bounds.

**Verifica empirica (2026-05-14)**:

Riga 148:
> PostgreSQL raccoglie **100 valori di campione per colonna** come default. Per tabelle piccole o con distribuzione uniforme, è sufficiente. Per tabelle grandi con distribuzione non uniforme, 100 campioni possono dare una rappresentazione distorta.

Glossario (riga 230):
> parametro PostgreSQL che definisce **quanti campioni raccogliere per colonna** durante l'ANALYZE. Il default è 100

**Realtà tecnica** ([PostgreSQL docs](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET)):
- `default_statistics_target` **non è** il numero di righe campionate
- È il **target per la dimensione di**:
  - **MCV (Most Common Values) list**: numero massimo di valori più frequenti tracciati
  - **Histogram bounds**: numero di "bucket" dell'istogramma di distribuzione
- Il **numero di righe campionate** è invece **300 × stats_target** (quindi con stats_target=100, ne campiona 30.000)

Esempio: con `default_statistics_target=100`:
- pg_stats tracerà fino a 100 most-common values
- L'istogramma avrà fino a 100 bucket
- ANALYZE camionerà ~30.000 righe (300 × 100)

**Verdetto**: claim **VERO**. L'articolo confonde un concetto importante: il target è sulla **qualità delle statistiche** (granularità MCV/histogram), non sul **numero di righe campionate**. Errore concettuale che un DBA PostgreSQL noterebbe.

**Proposta intervento**: **P0** — correggere il paragrafo + glossario.
- Effort: S (30 minuti, 4 traduzioni dell'articolo + 4 della mini-pagina glossario)
- Rischio: Nessuno

**STATO**: ✅ completato

---

### 2.10 `CREATE INDEX CONCURRENTLY` in transazione
**File**: `content/posts/postgresql/like-optimization-postgresql/index.it.md` (righe 137-145)
**Claim Analista B**: non può essere eseguito dentro una transazione esplicita.

**Verifica empirica (2026-05-14)**:

L'articolo presenta:
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX CONCURRENTLY idx_payment_report_reference_trgm
ON reporting.payment_report
USING gin (reference_code gin_trgm_ops);
```

E aggiunge precauzioni: off-peak, modalità CONCURRENTLY, monitoraggio I/O.

**Realtà tecnica** ([PostgreSQL docs](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)):
- `CREATE INDEX CONCURRENTLY` **non può** essere eseguito all'interno di una transazione esplicita (`BEGIN; ... COMMIT;`)
- Causa: il comando deve fare commit interni per gestire le fasi di build (snapshot, validation, swap)
- Se eseguito in transazione: errore `ERROR: CREATE INDEX CONCURRENTLY cannot run inside a transaction block`

**Quando emerge il problema**:
- ✅ Esecuzione interattiva in `psql`: nessun problema (no transazione esplicita)
- ✅ Script `psql -f file.sql` con singoli statement: nessun problema
- ❌ Migration tool che wrappa in transazione (Flyway, Liquibase, alembic, ecc.): errore
- ❌ Stored function PL/pgSQL: errore
- ❌ Bash script con `BEGIN; ... COMMIT;` esplicito: errore

**Verdetto**: claim **VERO ma di basso impatto** per il caso d'uso dell'articolo. L'articolo non sbaglia, omette solo un caveat operativo che diventa rilevante in CI/CD migration.

**Proposta intervento**: **P2** — aggiungere una nota sotto "Precauzioni": *"`CREATE INDEX CONCURRENTLY` non può essere wrappato in BEGIN/COMMIT — se usi migration tool come Flyway o Liquibase, verifica come gestiscono il comando."*
- Effort: XS (10 minuti, 4 traduzioni di una nota)
- Rischio: Nessuno

**STATO**: ✅ completato

---

## 3. Affermazioni assolute

**Claim Analista B**: contare le occorrenze di `sempre`, `mai`, `qualsiasi`, `non c'è scelta`, ecc. negli articoli per mitigarle.

**Verifica empirica (2026-05-14)**:

**Grep di superficie** sui pattern `sempre|mai|qualsiasi|nessun[oa]|tutti|sicuramente`:
- Numero totale di occorrenze nei 35 articoli IT: alto (>300 totali)
- Top 5 articoli per occorrenze: galera-cluster-3-nodi (22), binary-log-mysql (17), ai-github-project-management (14), pg-stat-statements (14), mysql-multi-istanza-secure-file-priv (14)

**Analisi qualitativa del campione**:
La maggior parte delle occorrenze NON sono assolutismi tecnici problematici. Sono:
- **Descrizioni di situazioni reali**: *"tutti gli utenti applicativi connessi come schema owner"* — descrive un caso visto, non un'affermazione universale
- **Uso retorico-narrativo**: *"la risposta è sempre una variante di..."* (drammatizzazione di un cliché)
- **Negazioni in contesto specifico**: *"non hai nessuno strumento per impedire"* (in un caso specifico)
- **Definizioni di glossario**: *"indipendenti da qualsiasi oggetto specifico"* (corretto descrittivamente)

**Vero claim assoluto problematico identificato**: il **titolo dell'articolo pg_stat_statements**:
- IT: *"pg_stat_statements: la prima cosa da installare su **qualsiasi** PostgreSQL"*
- EN: *"...the first thing to install on **any** PostgreSQL"*
- ES: *"...lo primero que instalar en **cualquier** PostgreSQL"*
- RO: *"...primul lucru de instalat pe **orice** PostgreSQL"*

Questo è esattamente l'esempio che l'Analista B cita: forte come titolo SEO ma tecnicamente troppo assoluto (ci sono scenari dove pg_stat_statements non è la prima priorità: PostgreSQL dietro PgBouncer multi-tenant, replica logica downstream, ecc.).

**Verdetto**: claim **parzialmente VERO**. L'audit B aveva ragione nel principio (mitigare gli assolutismi) ma la realtà operativa è che:
1. La **maggioranza** degli "assolutismi" rilevati dal grep sono usi retorici legittimi
2. **Il titolo `qualsiasi PostgreSQL` è l'unico caso veramente da rivedere** (lo segnala B esplicitamente)
3. Una rinominazione del titolo SEO comporta perdita di click + riscrittura della meta description

**Proposta intervento**: **P2** — non aggressivo, casi specifici:
- Lasciare i titoli SEO come sono (il valore di click vale lo "scivolone")
- All'interno del corpo dell'articolo `pg-stat-statements`, **mitigare nelle prime righe** con una frase tipo *"Con qualche eccezione (PgBouncer multi-tenant, replica logica downstream), è la prima cosa da installare"*
- Non fare grep+sostituzione di massa: rischia di togliere il sapore narrativo
- Effort: XS (10 minuti, 4 traduzioni di una frase)

**STATO**: ✅ completato

---

## 4. Revisione stilistica annotata per articolo

**Approccio**: per ogni articolo IT pubblicato, grep su `docs/STILE_LINGUISTICO.md` e annotare le occorrenze + sostituzioni proposte. NON applicare ancora — l'utente vuole vedere tutto prima e decidere insieme.

### Articoli Oracle
**STATO**: da fare

### Articoli MySQL
**STATO**: da fare

### Articoli PostgreSQL
**STATO**: da fare

### Articoli Data Warehouse
**STATO**: da fare

### Articoli Project Management
**STATO**: da fare

---

## 5. Roadmap consolidata finale

**STATO**: da fare (richiede tutte le sezioni precedenti)

---

## Note per ripresa dopo timeout

Se questo file viene letto da una sessione futura dopo un timeout:

1. Leggere il **Log attività** in alto per capire dove ci siamo fermati
2. Cercare sezioni con `**STATO**: in-corso` — quella è dove riprendere
3. Le sezioni con `**STATO**: ✅ completato` hanno i risultati direttamente sotto
4. Ogni commit ha la forma `audit-verify: <sezione completata>` per facile navigazione del git log
