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
| 1 | Verifica infra: tag bloat | da fare | — |
| 2 | Verifica infra: carrello/shop orfano | da fare | — |
| 3 | Verifica infra: structured data | da fare | — |
| 4 | Verifica infra: hreflang + canonical | da fare | — |
| 5 | Verifica infra: sitemap + robots.txt | da fare | — |
| 6 | Verifica P0 tech: Oracle Unified Audit | da fare | — |
| 7 | Verifica P0 tech: Galera durabilità | da fare | — |
| 8 | Verifica P0 tech: CSV con sed | da fare | — |
| 9 | Verifica P0 tech: Oracle partitioning CTAS | da fare | — |
| 10 | Verifica Media tech: expire_logs_days | da fare | — |
| 11 | Verifica Media tech: Data Guard / Active DG | da fare | — |
| 12 | Verifica Media tech: grants in stored proc | da fare | — |
| 13 | Verifica Media tech: anonymous user MySQL | da fare | — |
| 14 | Verifica Media tech: default_statistics_target | da fare | — |
| 15 | Verifica Media tech: CREATE INDEX CONCURRENTLY | da fare | — |
| 16 | Lista affermazioni assolute | da fare | — |
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

**STATO**: da fare

---

### 1.2 Carrello / Shop orfano
**Claim Analista A**: "presenza di un'icona del carrello o riferimenti a uno 'Shop' senza prodotti".

**STATO**: da fare

---

### 1.3 Structured data (JSON-LD)
**Claim Analista B**: implementare/validare `BlogPosting`, `Person`, `ProfilePage`, `BreadcrumbList`, `Organization`, `WebSite`, `ImageObject`.

**STATO**: da fare

---

### 1.4 Hreflang reciproci e canonical
**Claim Analista B**: verificare che ogni pagina abbia hreflang reciproci self-referencing.

**STATO**: da fare

---

### 1.5 Sitemap + robots.txt
**Claim Analista B**: verificare che sitemap esista, sia raggiungibile, contenga tutte le lingue, sia citata in robots.txt.

**STATO**: da fare

---

## 2. Verifiche errori tecnici (P0/Media secondo Analista B)

### 2.1 Oracle Unified Audit — `ALTER AUDIT POLICY ENABLE` vs `AUDIT POLICY`
**File da verificare**: `content/posts/oracle/oracle-roles-privileges/index.it.md`
**Claim**: la sintassi corretta è `AUDIT POLICY nome_policy` (Oracle docs CREATE AUDIT POLICY).

**STATO**: da fare

---

### 2.2 Galera Cluster — durabilità con `innodb_flush_log_at_trx_commit=2`
**File**: `content/posts/mysql/galera-cluster-3-nodi/index.it.md`
**Claim**: dire che è "garantita dalla replica sincrona" è troppo forte; va espresso come trade-off.

**STATO**: da fare

---

### 2.3 MySQL CSV con sed
**File**: `content/posts/mysql/mysql-multi-istanza-secure-file-priv/index.it.md`
**Claim**: `sed 's/\t/,/g'` non è CSV-safe se i campi contengono virgole/newline/quote.

**STATO**: da fare

---

### 2.4 Oracle partitioning — CTAS + rename con DML concorrente
**File**: `content/posts/oracle/oracle-partitioning/index.it.md`
**Claim**: CTAS + rename non è consistente senza freeze scritture o DBMS_REDEFINITION.

**STATO**: da fare

---

### 2.5 MySQL binary log — `expire_logs_days` vs `binlog_expire_logs_seconds`
**File**: `content/posts/mysql/binary-log-mysql/index.it.md` (+ `mysql-pre-upgrade-assessment`)
**Claim**: `expire_logs_days` legacy/deprecato in MySQL 8.

**STATO**: da fare

---

### 2.6 Oracle Data Guard vs Active Data Guard
**File**: `content/posts/oracle/oracle-data-guard/index.it.md` (+ `oracle-cloud-migration`)
**Claim**: real-time query con standby aperto in read-only mentre applica redo richiede licenza Active Data Guard.

**STATO**: da fare

---

### 2.7 Oracle grants tramite role in stored proc definer-rights
**File**: `content/posts/oracle/oracle-roles-privileges/index.it.md`
**Claim**: i privilegi via role non sono disponibili in stored proc definer-rights.

**STATO**: da fare

---

### 2.8 MySQL anonymous user
**File**: `content/posts/mysql/mysql-users-and-hosts/index.it.md`
**Claim**: l'anonymous user non è "sempre" creato, dipende dall'installazione.

**STATO**: da fare

---

### 2.9 PostgreSQL `default_statistics_target`
**File**: `content/posts/postgresql/explain-analyze-postgresql/index.it.md`
**Claim**: non è "100 righe campione" ma target per MCV/histogram bounds.

**STATO**: da fare

---

### 2.10 `CREATE INDEX CONCURRENTLY` in transazione
**File**: `content/posts/postgresql/like-optimization-postgresql/index.it.md` (+ altri)
**Claim**: non può essere eseguito dentro una transazione esplicita.

**STATO**: da fare

---

## 3. Affermazioni assolute

**Claim Analista B**: contare le occorrenze di `sempre`, `mai`, `qualsiasi`, `non c'è scelta`, ecc. negli articoli per mitigarle.

**STATO**: da fare

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
