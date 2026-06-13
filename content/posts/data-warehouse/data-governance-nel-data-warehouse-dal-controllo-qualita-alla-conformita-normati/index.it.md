---
title: "La pausa pranzo che ha rimandat o il go-live:Data Governance nel DWH"
date: 2099-12-31
draft: true
translationKey: "data_governance_nel_data_warehouse_dal_controllo_qualita_alla_conformita_normati"
tags: []
categories: ["data-warehouse"]
image: "data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati.cover.jpg"
webo_status: da_approvare
webo_generated_at: 2026-06-14
---

```markdown
---
seoTitle: "Data Governance nel DWH: qualità, GDPR e TDE in produzione"
description: "Da una pausa pranzo con un senior data analyst assicurativo emergono i gap di governance prima del go-live: data quality, lineage, ownership, GDPR e Transparent Data Encryption su Oracle 19c."
tags: ["data-governance", "data-warehouse", "oracle-19c", "gdpr", "transparent-data-encryption"]
---

## Il tavolo fuori dall'ufficio

Era una di quelle giornate di fine primavera in cui si mangia fuori, finalmente. Carlo — senior data analyst di un grande gruppo assicurativo italiano con cui collaboro da un paio d'anni — era visibilmente soddisfatto. Il DWH era tecnicamente pronto: i dati caricati, il modello dimensionale reggeva, le prime query sui report funzionavano. Stava già pensando a come presentare il successo ai manager la settimana successiva.

«Direi che siamo pronti per il go-live», mi ha detto, tagliando la pizza.

Ho aspettato un secondo prima di rispondere. Non perché volessi smorzare l'entusiasmo — il lavoro fatto era solido — ma perché quella frase, "siamo pronti", nascondeva una serie di domande che nessuno aveva ancora posto ad alta voce. E i gap di governance che emergono dopo il go-live vengono quasi sempre interpretati dai manager come disattenzione, non come complessità intrinseca del progetto.

«Tecnicamente sì», ho detto. «Ma hai già risposto a: chi è il data owner di `policy_holder_data`? Cosa succede se un report mostra un premio anomalo — chi lo corregge e in quanto tempo? E il GDPR, come lo gestiamo a livello di storage?»

Carlo ha posato la forchetta.

Quella conversazione è durata fino al caffè, poi è continuata davanti al PC nel pomeriggio. Questo articolo è il tentativo di mettere per iscritto quello che ci siamo detti.

---

## Quello che un DWH "pronto" non include per default

Un Data Warehouse tecnicamente funzionante — ETL che gira, dimensioni popolate, fatti aggregati correttamente — è una condizione necessaria ma non sufficiente per andare in produzione in un contesto enterprise. Soprattutto in settori regolamentati come quello assicurativo, dove i dati includono anagrafiche clienti, storico polizze, pagamenti e — in alcuni prodotti — dati sanitari.

Le aspettative implicite che i manager e gli utenti business portano in sala riunioni il giorno del go-live riguardano almeno quattro aree che raramente compaiono nei requisiti funzionali iniziali.

### Qualità dei dati: non è un controllo, è un processo

La qualità dei dati non è una checkbox da spuntare prima della messa in produzione. È un processo continuo. Nel DWH assicurativo che stavamo discutendo, le tabelle `claims_history` e `premium_payments` arrivavano da sistemi sorgente con qualità eterogenea: alcune compagnie del gruppo avevano codifiche diverse per lo stesso tipo di sinistro, campi data con formati inconsistenti, valori nulli in colonne che avrebbero dovuto essere obbligatorie.

Durante il caricamento avevamo già implementato alcune regole di validazione nell'ETL. Ma "validare in ingresso" e "garantire qualità nel tempo" sono due cose diverse. Servono:

- **Soglie di allerta**: se il numero di record rifiutati in un caricamento supera il 2%, qualcuno deve saperlo prima che i report vengano distribuiti
- **Processi di remediation**: chi corregge i dati anomali? Con quale priorità? Con quale traccia di audit?
- **Monitoraggio longitudinale**: un dato che era corretto sei mesi fa potrebbe non esserlo più se le regole di business cambiano

Carlo aveva gestito la validazione in ingresso. Il monitoraggio continuo e i processi di remediation erano ancora da definire.

### Ownership: la domanda scomoda

«Chi è il data owner di `policy_holder_data`?» avevo chiesto a pranzo.

Carlo aveva risposto: «Beh, la IT».

Questa risposta è quasi sempre sbagliata — o almeno incompleta. La IT gestisce l'infrastruttura e i processi tecnici, ma il dato appartiene al business. In un contesto assicurativo, il data owner di una tabella con dati anagrafici e contrattuali dei clienti dovrebbe essere una funzione di business (es. la direzione commerciale o la compliance), non il team tecnico.

La distinzione tra **Data Owner** (responsabilità di business sul dato), **Data Steward** (gestione operativa della qualità e delle regole) e **Data Custodian** (gestione tecnica dell'infrastruttura) non è burocrazia. È la risposta pratica alla domanda "chi chiamo quando questo dato è sbagliato?". Senza questa mappa, ogni anomalia diventa una riunione di tre ore per capire di chi è il problema.

### Glossario dati: quando "premio" non significa la stessa cosa per tutti

Nel gruppo assicurativo, il termine "premio" aveva almeno tre definizioni operative diverse a seconda della business unit. Il DWH le aveva consolidate in un'unica colonna `premium_amount` nella tabella `premium_payments`, ma senza documentare quale definizione fosse stata adottata e perché.

Un glossario dati condiviso — anche nella forma più semplice, un documento versionato con le definizioni concordate tra business e IT — è la differenza tra un report che genera fiducia e uno che genera discussioni. Non serve uno strumento enterprise da centinaia di migliaia di euro: serve una definizione scritta, concordata, accessibile.

### Data Lineage: la tracciabilità che salva gli audit

«Se un analista del risk management chiede da dove viene questo numero», ho detto a Carlo aprendo il PC, «riesci a rispondergli in meno di un'ora?»

Silenzio.

Il data lineage — la capacità di tracciare il percorso di un dato dalla sorgente al report finale, attraverso tutti i passaggi di trasformazione — è essenziale in due scenari: il troubleshooting quotidiano ("perché questo valore è cambiato rispetto al mese scorso?") e gli audit regolatori ("dimostrami che questo aggregato è calcolato correttamente secondo le regole X"). In un settore come quello assicurativo, il secondo scenario non è ipotetico.

---

## GDPR: da vincolo legale a scelta architetturale

Fino a questo punto della conversazione, Carlo stava annuendo con l'aria di chi riconosce i gap ma li vede come "cose da aggiungere dopo". Il punto di svolta è arrivato con il GDPR.

«Il GDPR lo gestiamo con la privacy policy e il consenso», ha detto Carlo. «La compliance è già coperta legalmente.»

«La compliance documentale sì», ho risposto. «Ma il GDPR all'articolo 32 parla esplicitamente di misure tecniche appropriate, inclusa la cifratura. Se qualcuno accede fisicamente ai file del database — un backup rubato, un disco dismesso male, un accesso non autorizzato allo storage — i dati di `policy_holder_data` sono leggibili in chiaro?»

Questa è la differenza tra compliance formale e implementazione architetturale. La prima protegge legalmente l'organizzazione finché non succede nulla. La seconda riduce la probabilità che succeda qualcosa, e riduce l'impatto se succede.

### Transparent Data Encryption su Oracle 19c

Oracle Database 19c include Transparent Data Encryption (TDE) [1], una funzionalità che cifra i dati a riposo — i file di dati, i file di redo log, i backup — senza richiedere modifiche alle applicazioni. Per il DWH assicurativo, questo significa che anche se qualcuno ottiene accesso fisico ai file su `oracle-dwh-prod-eu-01`, i dati rimangono illeggibili senza la chiave di cifratura gestita dal wallet Oracle.

L'abilitazione di TDE a livello di tablespace è relativamente semplice:

```sql
-- Creazione del wallet e impostazione della master key (da eseguire come SYSDBA)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/wallet' IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "wallet_password" WITH BACKUP;

-- Cifratura della tablespace che contiene i dati sensibili
ALTER TABLESPACE policy_data ENCRYPTION ONLINE USING 'AES256' ENCRYPT;
```

```sql
-- Verifica dello stato di cifratura delle tablespace
SELECT tablespace_name, encrypted
FROM dba_tablespaces
WHERE encrypted = 'YES';
```

Quello che TDE non fa: non protegge da un utente con accesso SQL legittimo al database. Non è un sostituto per la gestione degli accessi e dei privilegi. È uno strato di protezione specifico per il dato a riposo — esattamente quello che il GDPR considera una "misura tecnica appropriata" nel contesto della protezione contro accessi fisici non autorizzati o perdita di supporti [2].

La conversazione con Carlo si è spostata su un punto pratico: implementare TDE prima del go-live è un'operazione pianificabile con downtime controllato. Implementarla dopo, su un sistema in produzione con terabyte di dati storici già caricati, è un'operazione più complessa e rischiosa. La finestra di opportunità era quella.

---

## Un framework di qualità che regge nel tempo

Tornando alla qualità dei dati: quello che avevamo in piedi era una serie di controlli nell'ETL. Quello che serviva era un framework.

La differenza è sostanziale. I controlli nell'ETL bloccano o segnalano i record non conformi al momento del caricamento. Un framework di qualità aggiunge:

**Monitoraggio proattivo**: job schedulati che verificano periodicamente le condizioni di qualità sulle tabelle già caricate. Ad esempio, una query che controlla ogni mattina se esistono `policy_holder_data` con `fiscal_code` nullo o con formato non valido — dati che potrebbero essere entrati attraverso percorsi di caricamento non standard.

```sql
-- Esempio di controllo qualità schedulato su policy_holder_data
SELECT
    COUNT(*) AS anomalie_codice_fiscale,
    SYSDATE AS data_controllo
FROM policy_holder_data
WHERE fiscal_code IS NULL
   OR NOT REGEXP_LIKE(fiscal_code, '^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$');
```

**Soglie e notifiche**: se il conteggio delle anomalie supera una soglia definita (es. più di 50 record con codice fiscale non valido in un giorno), il sistema notifica il Data Steward responsabile prima che i report vengano distribuiti.

**Traccia di remediation**: ogni correzione manuale sui dati deve essere documentata — chi ha corretto, quando, perché, qual era il valore originale. In un contesto assicurativo, questa traccia è rilevante sia per gli audit interni sia per eventuali verifiche regolamentari.

---

## Il Data Catalog: dove la governance diventa navigabile

Un Data Catalog [3] è l'infrastruttura che rende navigabile tutto quello che abbiamo discusso fino a qui. Non è uno strumento opzionale per i team grandi: è la differenza tra una governance che esiste solo nei documenti e una governance che gli utenti business riescono effettivamente a usare.

Nel contesto del DWH assicurativo, un Data Catalog minimo dovrebbe rispondere a queste domande senza richiedere una telefonata al team tecnico:

- Cosa contiene la tabella `claims_history`? Quali colonne? Con quali regole di business?
- Da dove arrivano i dati di `premium_payments`? Attraverso quali trasformazioni?
- Chi è il data owner di `policy_holder_data`? Chi contatto se trovo un'anomalia?
- Quali tabelle contengono dati personali soggetti a GDPR?

Strumenti enterprise come Apache Atlas, Collibra o Alation gestiscono questo in modo strutturato. Per un primo go-live, anche una soluzione più leggera — un wiki strutturato, un foglio condiviso con le definizioni concordate — è infinitamente meglio di niente. L'importante è che esista, che sia aggiornato e che gli utenti sappiano dove trovarlo.

L'integrazione con il glossario dati è naturale: le definizioni concordate (es. la definizione di "premio" adottata nel DWH) vivono nel catalog e sono referenziate dalla documentazione delle colonne. Il lineage, idealmente, è visualizzabile dallo stesso strumento.

---

## Chi fa cosa: i tre ruoli che non si possono ignorare

Prima di chiudere la conversazione con Carlo, abbiamo messo per iscritto una mappa dei ruoli. Non come esercizio formale, ma come risposta pratica alla domanda: quando qualcosa va storto, chi chiamo?

**Data Owner**: è una figura di business, non tecnica. Decide le regole di utilizzo del dato, approva le modifiche alle definizioni, è responsabile della qualità dal punto di vista del business. Per `policy_holder_data`, il Data Owner naturale era la direzione compliance del gruppo.

**Data Steward**: è il ponte tra business e IT. Gestisce operativamente le regole di qualità, monitora le anomalie, coordina la remediation. Può essere una figura tecnica con forte sensibilità di business, o viceversa. Nel nostro caso, Carlo era il candidato naturale per questo ruolo su alcune delle tabelle chiave.

**Data Custodian**: è il team tecnico. Gestisce l'infrastruttura, implementa le regole tecniche definite dal Data Owner e dal Data Steward, garantisce disponibilità e sicurezza. La responsabilità della TDE, dei backup, degli accessi al database — tutto questo è scope del Data Custodian.

La distinzione non è burocrazia. È la risposta operativa alla domanda "chi è responsabile di cosa". Senza questa mappa, ogni problema diventa una discussione su chi dovrebbe risolvere il problema, invece di una discussione su come risolverlo.

---

## "Ora so cosa manca"

Verso le cinque del pomeriggio, Carlo si è alzato dalla sedia e ha detto una cosa che mi è rimasta: «Okay. Ora so cosa manca. E so come presentarlo ai manager senza sembrare che abbiamo fatto un lavoro a metà.»

Questa è la differenza tra arrivare a una riunione di go-live con i gap nascosti e arrivare con i gap mappati e un piano per chiuderli. I manager non si aspettano la perfezione — si aspettano che il team sappia dove si trova e dove sta andando.

Abbiamo rimandato il go-live di tre settimane. In quel tempo: definito i Data Owner per le tabelle principali, implementato TDE sulla tablespace che conteneva i dati personali, scritto un glossario dati minimo per i termini critici, impostato i primi controlli di qualità schedulati e abbozzato la struttura del Data Catalog.

Non era tutto. Ma era abbastanza per arrivare alla riunione con i manager con le risposte giuste alle domande giuste. Il merito non era di una singola intuizione — era di una conversazione franca tra due persone con prospettive diverse che lavoravano verso lo stesso obiettivo.

---

## Fonti ufficiali

1. Oracle Database Security Guide 19c — [Configuring Transparent Data Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-transparent-data-encryption.html)
2. Regolamento (UE) 2016/679 — [Articolo 32: Sicurezza del trattamento](https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32016R0679)
3. DAMA International — [DAMA-DMBOK2: Data Management Body of Knowledge](https://www.dama.org/dama-dm-bok-2) — copre Data Governance, Data Quality, Data Lineage, Data Catalog, Data Stewardship

---

## Glossario candidato

- **Data Governance** — L'insieme di processi, politiche, standard e metriche che assicurano uso efficace delle informazioni, garantendone qualità, integrità, sicurezza e conformità normativa. Non è un progetto con una data di fine: è un framework operativo continuo.

- **Data Lineage** — La capacità di tracciare il percorso di un dato dalla sorgente attraverso tutti i sistemi e le trasformazioni, fino alla destinazione finale. Essenziale per troubleshooting, audit regolatori e verifica della correttezza dei calcoli.

- **Transparent Data Encryption (TDE)** (Oracle) — Funzionalità di Oracle Database che cifra i dati a riposo — file di dati, redo log, backup — senza modifiche alle applicazioni. Protegge contro accessi fisici non autorizzati ai supporti di storage.

- **Data Quality** — La misura in cui i dati sono accurati, completi, coerenti, validi e tempestivi. Non è un controllo una-tantum ma un processo continuo di monitoraggio, allerta e remediation che garantisce l'affidabilità delle analisi nel tempo.

- **Data Catalog** — Inventario organizzato di tutti i dati disponibili in un'organizzazione, con metadati, glossario, lineage e strumenti di ricerca. Rende la governance navigabile dagli utenti business senza richiedere intervento tecnico per ogni domanda sui dati.
```
