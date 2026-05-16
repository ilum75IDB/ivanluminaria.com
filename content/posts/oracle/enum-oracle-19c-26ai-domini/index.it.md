---
title: "Oracle 19c, 21c, 23ai, 26ai: la riscrittura silenziosa dei domini di valori"
seoTitle: "Oracle 19c → 26ai: SQL Domain e Assertion in 7 anni"
description: "Sette anni di Oracle visti attraverso le enumerazioni: dal CHECK del 19c ai SQL Domains della 23ai, fino alle Assertion del 26ai. Una migrazione assicurativa."
date: "2026-06-23T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_19c_26ai_domini"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-19c-26ai-domini.cover.jpg"
---

Negli ultimi sette anni Oracle ha riscritto in silenzio come si modellano i **domini di valori** in uno schema. Senza annunci roboanti, senza la fanfara che PostgreSQL e MySQL hanno saputo costruirsi intorno al loro `ENUM`. Quattro major release — 19c, 21c, 23ai, 26ai — e una traiettoria che, vista dall'alto, racconta una storia precisa: Oracle è arrivato per ultimo, e ci è arrivato con una soluzione diversa.

Se cerchi il quadro orizzontale (Oracle vs MySQL vs PostgreSQL, le tre strade comparate fianco a fianco), è in [questo articolo della miniserie](/it/posts/oracle/enum-oracle-workaround-fino-a-23ai/). Qui prendiamo invece la lente verticale: una sola piattaforma, sette anni, quattro release. Cosa avevi a disposizione in ogni periodo, cosa cambia in quello che viene dopo.

---

## 19c (2019): il punto di partenza

Oracle Database 19c, rilasciata nel 2019, è ancora oggi la **long-term release di riferimento** per moltissimi sistemi enterprise — banking, assicurativo, PA italiana, dove gli upgrade hanno un ciclo lungo e prudente. Quando questa storia inizia, gli strumenti a disposizione per modellare un'enumerazione erano due, e nessuno dei due era "elegante":

```sql
-- Opzione 1: CHECK inline (Oracle 19c)
CREATE TABLE polizze (
  id          NUMBER PRIMARY KEY,
  numero      VARCHAR2(20) NOT NULL,
  stato       VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_stato_polizza CHECK (stato IN
    ('EMESSA','IN_VIGORE','SOSPESA','SCADUTA','ANNULLATA','STORNATA'))
);

-- Opzione 2: lookup table con FK (Oracle 19c)
CREATE TABLE stati_polizza (
  codice    VARCHAR2(20) PRIMARY KEY,
  etichetta VARCHAR2(100) NOT NULL,
  ordine    NUMBER,
  attivo    CHAR(1) DEFAULT 'Y' CHECK (attivo IN ('Y','N'))
);

CREATE TABLE polizze (
  id            NUMBER PRIMARY KEY,
  numero        VARCHAR2(20) NOT NULL,
  stato_codice  VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_stato FOREIGN KEY (stato_codice)
    REFERENCES stati_polizza(codice)
);
```

Il `CHECK` è leggero, applicato dal motore dal lato runtime e usato perfino dall'ottimizzatore per **eliminare condizioni impossibili** [1] — ma è locale alla colonna, e replicare lo stesso vincolo su venti tabelle che condividono lo stesso dominio è un esercizio di pazienza (e di disciplina sui code review). La lookup table è la via del database puro, dominante nei progetti enterprise: un JOIN in più, ma anche un'enumerazione che diventa un **oggetto del database con vita propria** — etichette localizzate, ordine di display, flag attivo/disattivo, audit trail.

In 19c **questo era tutto**. Nessun `CREATE TYPE ENUM` come PostgreSQL, nessun `ENUM` di colonna come MySQL. Per chi veniva da quei due mondi, la sensazione era: *"e quindi non c'è nulla di nativo?"*. Risposta: no. C'era il `CHECK`, c'era la lookup, e c'erano vent'anni di mestiere accumulato su come farli funzionare insieme.

---

## 21c (2021): un'innovazione che salta gli stati nei dati

Oracle Database 21c — la "innovation release", arrivata su Cloud nel 2020 e on-premises nel 2021 — porta in dote cose grosse: il **tipo JSON nativo** [2], le **blockchain table** e le **immutable table** per audit non manipolabile, i **SQL Macros** per riusare frammenti di SQL, l'integrazione AutoML in-DB. È una release piena di nuove idee.

Ma per chi guardava al problema specifico della modellazione dei domini di valori, **21c non porta nulla**. Niente `CREATE DOMAIN`, niente revisione del `CHECK`, niente meta-tassonomia integrata nel dizionario dati. La scelta del DBA che migra da 19c a 21c, sul tema enumerazioni, non cambia: `CHECK` o lookup.

Vale comunque la pena nominarla, perché segna un passaggio: Oracle in quei due anni stava lavorando ad altro, e chi sperava in una risposta sul fronte schema-domain doveva aspettare. **L'attesa è durata due anni in più di quello che si pensava**, ed è finita con il salto numerico verso la 23ai — il primo segnale, non solo nominale, che Oracle stava per cambiare passo.

---

## 23ai (2024): SQL Domains, finalmente

Aprile 2024, Oracle Database 23ai rilasciata su engineered system (Exadata Cloud@Customer prima, poi disponibilità più ampia). Tra le decine di novità — e ce ne sono tante, dalla `JSON Relational Duality` agli `AI Vector Search` — il costrutto che riguarda la nostra storia è uno solo: il **SQL Domain** [3].

```sql
-- Oracle 23ai
CREATE DOMAIN stato_polizza AS VARCHAR2(20)
  CONSTRAINT chk_stato_polizza CHECK (VALUE IN
    ('EMESSA','IN_VIGORE','SOSPESA','SCADUTA','ANNULLATA','STORNATA'))
  DEFAULT 'EMESSA'
  ANNOTATIONS (
    display 'Stato Polizza',
    description 'Ciclo di vita di una polizza assicurativa',
    ordering 'EMESSA<IN_VIGORE<SOSPESA<SCADUTA<ANNULLATA<STORNATA'
  );

CREATE TABLE polizze (
  id      NUMBER PRIMARY KEY,
  numero  VARCHAR2(20) NOT NULL,
  stato   stato_polizza NOT NULL
);

CREATE TABLE storico_polizze (
  id_polizza   NUMBER,
  data_evento  DATE,
  stato        stato_polizza NOT NULL,
  CONSTRAINT fk_pol FOREIGN KEY (id_polizza) REFERENCES polizze(id)
);
```

Tre cose vale la pena leggere con calma in questo blocco.

**Primo**: il `DOMAIN` è un **oggetto del dizionario dati**. Lo si trova in `DBA_DOMAINS`, `USER_DOMAINS`, `ALL_DOMAINS`, con tanto di colonne che descrivono il tipo base, il vincolo, il default. Per la prima volta, su Oracle, l'**enumerazione esiste come entità nel catalogo dello schema** senza richiedere una seconda tabella di lookup. Il design review che chiedeva "dov'è documentato che `stato` può assumere solo questi sei valori?" trova ora una risposta diretta.

**Secondo**: le `ANNOTATIONS`. Sono coppie chiave/valore di metadati che gli strumenti BI, le procedure di UI generation e i framework di reporting possono leggere via `USER_ANNOTATIONS_USAGE` per derivare automaticamente etichette di display, descrizioni di campo, ordering di rappresentazione. Su PostgreSQL il `DOMAIN` ha solo tipo + vincolo; Oracle qui ha fatto un passo in più, ed è un passo che si nota quando un report Power BI o Tableau si appoggia direttamente al dizionario per costruire le sue mappe semantiche.

**Terzo**: una sola colonna `stato` di tipo `stato_polizza` può essere usata in **decine di tabelle**, e in tutte si applica lo stesso vincolo, lo stesso default, le stesse annotations. Quello che con il `CHECK` richiedeva venti `ALTER TABLE` per essere modificato, con il `DOMAIN` richiede un singolo `ALTER DOMAIN` [4].

---

## Una migrazione 19c → 23ai concreta

Lo schema di una compagnia di assicurazioni — multi-paese, settore Surety — su Oracle 19c, circa 1.800 tabelle nello schema applicativo, e una tassonomia di stati polizza replicata in **22 tabelle** del modulo gestione contratti. Ogni volta che compliance chiedeva di aggiungere un nuovo stato (ultima volta: `'IN_VERIFICA_ANTIRICICLAGGIO'` per una nuova policy normativa) erano 22 `ALTER TABLE` da pianificare, testare, deployare in finestra notturna.

L'upgrade a 23ai non è stato fatto **per** questo problema — è stato fatto per altre ragioni (consolidamento infrastrutturale, fine del supporto Premier su 19c). Ma una volta su 23ai, il team architetturale ha messo in piano un piccolo refactor: convertire la tassonomia stati polizza in un SQL Domain unico.

I passi, in sintesi, sono stati questi:

```sql
-- 1) Creazione del domain con i valori storici già presenti in produzione
CREATE DOMAIN stato_polizza AS VARCHAR2(20)
  CONSTRAINT chk_stato_polizza CHECK (VALUE IN
    ('EMESSA','IN_VIGORE','SOSPESA','SCADUTA','ANNULLATA','STORNATA',
     'IN_VERIFICA_ANTIRICICLAGGIO'))
  DEFAULT 'EMESSA';

-- 2) Sulla tabella principale, dichiarazione del domain sulla colonna esistente
ALTER TABLE polizze MODIFY (stato stato_polizza);

-- 3) Stessa cosa per ognuna delle 21 tabelle dipendenti
ALTER TABLE storico_polizze MODIFY (stato stato_polizza);
ALTER TABLE polizze_premi   MODIFY (stato stato_polizza);
-- ... ecc.

-- 4) Drop dei vecchi CHECK inline ridondanti (ora il domain li sostituisce)
ALTER TABLE polizze        DROP CONSTRAINT chk_stato_polizza;
ALTER TABLE storico_polizze DROP CONSTRAINT chk_stato_pol_storico;
-- ... ecc.
```

Le 22 tabelle sono state migrate in una finestra di manutenzione di poco più di un'ora — quasi tutto il tempo è stato consumato dalla **validazione delle righe esistenti** (`VALIDATE`, default in Oracle), che ha letto ogni tabella per confermare che nessun valore storico violasse il vincolo del domain. Per le tabelle più grandi (storico polizze, ~340 milioni di righe) si è scelto `NOVALIDATE` con un cleanup successivo via batch: in produzione l'integrità in avanti era garantita dal domain, e i dati storici erano già stati controllati con uno script di pre-flight.

Il risultato finale, dopo il refactor: una sola riga di DDL per modificare la tassonomia. La prossima richiesta di compliance — ce ne sarà una, sempre — costerà un `ALTER DOMAIN`, non una settimana di pianificazione.

Non è una storia di eroismo. È una storia di un team che ha riconosciuto un'opportunità nel momento giusto e l'ha colta — Oracle aveva finalmente dato lo strumento, restava solo da prenderlo in mano.

---

## 26ai (2026): ASSERTION e quello che si vede all'orizzonte

Oracle 26ai (annunciata come la prossima major release) porta sul tavolo, tra le altre cose, le **`ASSERTION`**: un costrutto SQL standard sulla carta da decenni, mai veramente implementato da nessun DBMS mainstream, che permette di esprimere vincoli **cross-tabella** validati a livello transazionale dal motore del database.

Per la nostra storia, le `ASSERTION` sono il pezzo che chiude un cerchio. Con il SQL Domain del 23ai abbiamo risolto il problema "stesso vincolo su molte colonne". Con le `ASSERTION` del 26ai si apre un'altra possibilità: vincoli che coinvolgono **più tabelle insieme**, garantiti dal database senza che debba intervenire un trigger o una check applicativa.

```sql
-- Esempio (sintassi indicativa basata sullo standard SQL):
CREATE ASSERTION almeno_uno_stato_attivo CHECK (
  (SELECT COUNT(*) FROM stati_polizza WHERE attivo = 'Y') >= 1
);

CREATE ASSERTION storico_coerente CHECK (
  NOT EXISTS (
    SELECT 1 FROM polizze p
    LEFT JOIN storico_polizze s ON s.id_polizza = p.id
    WHERE p.stato = 'STORNATA' AND s.stato IS NULL
  )
);
```

Vincoli del genere oggi si scrivono come trigger — con tutti i problemi del caso: trigger che si dimenticano in deploy successivi, transazioni che bypassano il check per via dell'isolation level, race condition difficili da diagnosticare. Le `ASSERTION` sposterebbero la responsabilità sul motore. Quando 26ai sarà disponibile in test e su workload reali, sarà materia da approfondire — ma il design di una tassonomia oggi può già tener conto di dove i vincoli cross-tabella vivranno meglio domani.

---

## Quello che Oracle continua a non avere

C'è una cosa che, ancora oggi, Oracle non offre: un **tipo enumerativo nativo** come quelli di PostgreSQL (`CREATE TYPE ... AS ENUM`) o MySQL (`ENUM(...)`). Vale la pena dirlo apertamente, perché qualcuno potrebbe chiederselo.

Il SQL Domain è **concettualmente più potente** di un ENUM tradizionale (è un vincolo riusabile, non un tipo "chiuso"), ma è anche **più verboso** da dichiarare e ha un overhead di indirezione nel dizionario dati. Per il caso d'uso più semplice — una colonna in una sola tabella, set di valori molto piccolo, niente metadati — il `CHECK` inline resta più asciutto. Oracle 23ai, in altre parole, non ha sostituito il `CHECK`: gli ha affiancato uno strumento per quando il `CHECK` non bastava più.

È coerente con la filosofia Oracle: dare strumenti potenti e generali, lasciando al designer la responsabilità di scegliere il livello giusto di astrazione. PostgreSQL e MySQL hanno fatto la scelta opposta — dare un tipo pronto e specifico — e per molti casi quella scelta è più immediata. Sono due culture diverse, entrambe legittime.

---

## La traiettoria, vista da fine 2026

Sette anni, quattro release, e una linea che da fuori sembra continua ma vista da dentro è fatta di pause e di scatti. La 19c era il punto di partenza: due strade conosciute e nessuna terza. La 21c ha portato altre cose, restando ferma su questo terreno. La 23ai ha aperto la **strada strutturale** che mancava da decenni. La 26ai chiude il cerchio sui vincoli che superano la singola tabella.

Non è una storia eroica. Oracle è arrivato dopo PostgreSQL (che ha i `DOMAIN` dalla fine degli anni '90) e dopo MySQL (che ha gli `ENUM` da sempre). Ma quando è arrivato, è arrivato con un'idea diversa — più generale, più integrata nel dizionario, più estendibile via annotazioni — e quell'idea sta diventando il modo standard di modellare i domini di valori sui nuovi schemi Oracle che vedo nascere in produzione oggi.

La domanda da portarsi via, per chi modella schemi enterprise su Oracle: **non più "quale strada uso", ma "quando il `CHECK` inline mi basta, e quando vale la pena dichiarare un `DOMAIN`"**. Le due opzioni convivono, e sapere quando passare dall'una all'altra è oggi il vero discrimine.

---

## Fonti ufficiali

1. Oracle Database 19c SQL Language Reference — [constraint_clause (CHECK e altri vincoli)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html)
2. Oracle Database 21c Database New Features Guide — [Innovation Release overview](https://docs.oracle.com/en/database/oracle/oracle-database/21/nfcoa/index.html)
3. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
4. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glossario

- **[SQL Domain](/it/glossary/oracle-sql-domain/)** — Costrutto introdotto in Oracle 23ai che permette di definire un dominio riusabile (tipo base + CHECK + DEFAULT + annotations) come oggetto del dizionario dati. Per la prima volta su Oracle, un'enumerazione esiste nel catalogo schema senza richiedere una tabella di lookup.
- **[Annotations (Oracle 23ai)](/it/glossary/oracle-annotations/)** — Coppie chiave/valore di metadati associabili a oggetti dello schema (colonne, domain, tabelle), leggibili via `USER_ANNOTATIONS_USAGE`. Usate da strumenti BI e UI generation per derivare automaticamente etichette di display, descrizioni, ordering.
- **[VALIDATE / NOVALIDATE](/it/glossary/oracle-validate-novalidate/)** — Modalità di applicazione di un vincolo Oracle al momento della creazione o modifica: `VALIDATE` legge tutte le righe esistenti per controllare conformità (default), `NOVALIDATE` salta il controllo per non bloccare grandi tabelle in finestra di manutenzione.
- **[Major release Oracle](/it/glossary/oracle-major-release/)** — Versione principale del Database server con cambiamenti significativi di feature, ciclo di supporto Premier dedicato e numerazione propria (19c, 21c, 23ai, 26ai). Diverse dai patch set e dalle release update intermedie.
- **[ASSERTION](/it/glossary/sql-assertion/)** — Costrutto SQL standard per esprimere vincoli cross-tabella validati a livello transazionale dal motore del database. Annunciato in Oracle 26ai.
