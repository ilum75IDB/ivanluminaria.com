---
title: "ENUM in PostgreSQL: il contesto in cui la scelta paga, e quello in cui te la fa pesare"
seoTitle: "PostgreSQL ENUM vs CHECK vs lookup: la scelta giusta"
description: "PostgreSQL ENUM vs CHECK vs lookup table: ALTER TYPE ADD VALUE costa zero, rimuovere un valore costa una migration. Tre strade, un caso reale telco."
date: "2026-06-09T08:03:00+01:00"
draft: false
translationKey: "enum_postgresql_paga_o_pesa"
tags: ["enum", "data-modeling", "schema-design", "alter-type", "check-constraint"]
categories: ["postgresql"]
image: "enum-postgresql-paga-o-pesa.cover.jpg"
---

La domanda è la stessa di [quella che ci siamo posti per MySQL](/it/posts/mysql/enum-mysql-semplifica-o-complica/): una colonna `status` o `type` con un set chiuso di valori, e tre strade davanti — tipo enumerativo nativo, CHECK constraint, tabella di lookup. Cambia il database, cambia la filosofia, e cambia anche dove cade il prezzo.

PostgreSQL ha un suo ENUM, dichiarato come tipo a sé stante con `CREATE TYPE ... AS ENUM` [1] [2]. È pensato in modo diverso da quello di MySQL: type-safe come un domain, transazionale come tutto il resto del DDL, e con un dettaglio che fa inciampare quasi tutti al primo passaggio — è **case-sensitive**. Per chi viene da MySQL la cosa è scomoda, per chi ha sempre lavorato con PostgreSQL è naturale.

Vale la pena entrare nel merito, perché PostgreSQL ENUM non è "MySQL ENUM con un'altra sintassi". È un'altra cosa. Va capita per quella che è.

---

## Le tre strade, in due righe ciascuna

Useremo l'esempio di una tabella `abbonamenti` con uno stato che assume un set chiuso di valori.

**ENUM nativo**:

```sql
CREATE TYPE stato_abbonamento AS ENUM (
  'ATTIVO','SOSPESO','TERMINATO','SCADUTO'
);

CREATE TABLE abbonamenti (
  id     BIGINT PRIMARY KEY,
  stato  stato_abbonamento NOT NULL
);
```

In PostgreSQL il tipo è un **oggetto di prima classe**: lo crei una volta, lo riusi su tante colonne, lo modifichi con `ALTER TYPE`. Internamente la colonna occupa 4 byte (un `OID` interno), il valore è validato dal motore, e la lettura restituisce la stringa originale (case-sensitive).

**CHECK constraint**:

```sql
CREATE TABLE abbonamenti (
  id     BIGINT PRIMARY KEY,
  stato  VARCHAR(20) NOT NULL,
  CONSTRAINT chk_stato 
    CHECK (stato IN ('ATTIVO','SOSPESO','TERMINATO','SCADUTO'))
);
```

Approccio SQL standard. Più verboso, in cambio più flessibile (le condizioni di `CHECK` possono essere arbitrariamente complesse). In PostgreSQL i `CHECK` constraint sono pienamente applicati da sempre [3] — niente "silenziosamente ignorati" come accadeva in MySQL prima della 8.0.16.

**Tabella di lookup con FK**:

```sql
CREATE TABLE stati_abbonamento (
  codice    VARCHAR(20) PRIMARY KEY,
  etichetta VARCHAR(100) NOT NULL,
  attivo    BOOLEAN DEFAULT TRUE
);

CREATE TABLE abbonamenti (
  id            BIGINT PRIMARY KEY,
  stato_codice  VARCHAR(20) NOT NULL,
  CONSTRAINT fk_stato 
    FOREIGN KEY (stato_codice) REFERENCES stati_abbonamento(codice)
);
```

La via "database-puro". Più tabelle, più JOIN, e in cambio più flessibilità: attributi aggiuntivi, etichette localizzate, ordine di display, attivazione/disattivazione a runtime [4].

---

## Cosa cambia rispetto a MySQL: tre cose, da sapere prima

Se arrivi da MySQL, ci sono tre dettagli che faresti bene a tenere in tasca prima di scrivere il primo `CREATE TYPE`.

**Case-sensitive**. `'ATTIVO'` e `'attivo'` sono due valori diversi. In MySQL erano lo stesso valore — un design choice che a molti sembrava "comodo" e ad altri "scivoloso". PostgreSQL prende la strada opposta: se hai dichiarato `'ATTIVO'`, dovrai sempre scrivere `'ATTIVO'`. Le query non normalizzate falliranno con un *invalid input value*. È rigore, e una volta che ci si abitua si apprezza; il primo giorno è una sorpresa che costa qualche minuto.

**Type safety vera, non simulata**. ENUM è un tipo, non un vincolo su `VARCHAR`. Puoi creare una funzione che accetta `stato_abbonamento` come parametro, e il motore rifiuterà al parse-time qualunque chiamata con una stringa libera. Lo stesso vale per le procedure, per le view, per gli indici parziali. In MySQL questa sicurezza non esiste — `ENUM` è una colonna `VARCHAR` decorata.

**ALTER TYPE è quasi gratis (e transazionale)**. Aggiungere un valore in coda a un ENUM PostgreSQL è un'operazione di metadata [5]. Niente rebuild della tabella, niente lock di scrittura prolungato. E come tutto il DDL di PostgreSQL, è dentro la transazione: se il commit fallisce, l'ENUM resta com'era. Questa è la differenza più tangibile rispetto a MySQL, dove `MODIFY COLUMN ENUM(...)` su una tabella grande può tenerti sveglio una notte intera.

---

## Quando ENUM è la scelta giusta in PostgreSQL

Lo stesso principio di MySQL, calato nel contesto PostgreSQL: **set di valori stabile, semantica controllata da schema**. Quando questi due ingredienti ci sono, ENUM in PostgreSQL ha persino qualche vantaggio in più rispetto al cugino MySQL:

1. **Type safety end-to-end**: ENUM è un tipo che attraversa funzioni, procedure, foreign data wrapper. Non è solo un vincolo su una colonna, è una garanzia di coerenza che PostgreSQL applica a tutto lo stack di codice SQL
2. **Storage compatto**: 4 byte per riga (come un `INT` che fa da FK), confrontabile con MySQL. Su tabelle da centinaia di milioni di righe non è il driver principale; resta comunque coerente
3. **ALTER TYPE ADD VALUE economico**: la modifica più frequente — aggiungere un nuovo valore — costa praticamente zero
4. **DDL transazionale**: aggiungere un valore dentro una transazione che comprende anche il deploy del codice applicativo è una garanzia di atomicità che pochi altri DBMS ti regalano

In un sistema dove il dominio è davvero chiuso e ben definito, ENUM in PostgreSQL toglie complessità e aggiunge sicurezza. Una `CREATE TYPE`, una colonna, fine.

---

## Il caso concreto: stati di abbonamento in un operatore mobile

Ci siamo trovati, qualche progetto fa, a disegnare il modello dati per la gestione degli abbonamenti di un operatore mobile europeo. Stack PostgreSQL, milioni di SIM attive, una tabella `abbonamenti` con uno `stato` letto da praticamente ogni query del billing.

Nella prima versione gli stati erano quattro, ben definiti dal business: `ATTIVO`, `SOSPESO`, `TERMINATO`, `SCADUTO`. ENUM era la scelta naturale:

```sql
CREATE TYPE stato_abbonamento AS ENUM (
  'ATTIVO','SOSPESO','TERMINATO','SCADUTO'
);

ALTER TABLE abbonamenti
  ADD COLUMN stato stato_abbonamento NOT NULL DEFAULT 'ATTIVO';
```

Per un anno e mezzo ha funzionato in silenzio. Type-safe, leggibile, performante. Nessuna lookup table da seedare, nessuna FK da mantenere al deploy. Nessuno se ne ricordava più, ed è il complimento migliore che si possa fare a uno schema.

Poi, com'è normale, il prodotto è cresciuto.

Il primo richiamo è arrivato dal team antifrode: serviva distinguere fra `SOSPESO_PER_MOROSITA` e `SOSPESO_VOLONTARIO`. Operazione facile in PostgreSQL — è qui che la differenza con MySQL si vede:

```sql
ALTER TYPE stato_abbonamento ADD VALUE 'SOSPESO_PER_MOROSITA' AFTER 'SOSPESO';
ALTER TYPE stato_abbonamento ADD VALUE 'SOSPESO_VOLONTARIO'   AFTER 'SOSPESO_PER_MOROSITA';
```

Due `ALTER TYPE` di metadata. Millisecondi. Niente rebuild, niente lock significativi sulla tabella `abbonamenti` da decine di milioni di righe. La stessa operazione in MySQL, ricordo, avrebbe richiesto un `MODIFY COLUMN ENUM(...)` con tutta la tabella riscritta in Online DDL, e un DBA in piedi davanti al monitor.

Punto a favore di PostgreSQL. Vero.

Poi, dopo qualche trimestre, sono arrivati i problemi.

---

## I limiti, racconti dall'esperienza

I limiti di PostgreSQL ENUM esistono. Non sono peggio di quelli di MySQL — sono **diversi**, e si manifestano in punti diversi del ciclo di vita.

**Non si rimuove un valore in modo nativo**. Sembra un dettaglio; è il limite più grosso. Se il business decide di "ritirare" lo stato `SCADUTO` (perché ad esempio nel nuovo modello commerciale viene assorbito da `TERMINATO`), in PostgreSQL non hai un `ALTER TYPE DROP VALUE`. Devi:

1. Creare un nuovo tipo con i valori ridotti
2. Aggiornare tutte le righe della tabella per migrarle al nuovo set
3. Cambiare il tipo della colonna (`ALTER COLUMN ... TYPE`)
4. Droppare il tipo vecchio

Tutto questo, su una tabella grande, è esattamente la migration pesante che in MySQL avresti pagato per **aggiungere** un valore — qui la paghi per **toglierne** uno. La simmetria è simpatica solo a parole: in produzione, è comunque tanto carico.

**Rinominare un valore è facile, anche se transazionale**. `ALTER TYPE ... RENAME VALUE 'X' TO 'Y'` esiste da PostgreSQL 10. Operazione veloce e pulita. C'è però una sottigliezza: l'ALTER TYPE è dentro la transazione, sì, e se la rinomina avviene in una transazione che altre sessioni hanno aperto su quel tipo, potresti incontrare lock. Su sistemi con alta concorrenza non è banale come sembra.

**Ordinamento per posizione**. Come in MySQL, l'ordine in cui hai dichiarato i valori conta per `ORDER BY`. Se hai aggiunto `SOSPESO_PER_MOROSITA` `AFTER 'SOSPESO'`, l'ordine è coerente. Ma se ti scordi e fai `ALTER TYPE ... ADD VALUE 'NUOVO'` senza specificare la posizione, il valore va in coda. Il sort delle dashboard può sorprenderti.

**Indici GIN/GiST non lo trattano come stringa**. Vantaggio o svantaggio a seconda del caso d'uso; se hai pensato di farci sopra una full text search, ricordati che ENUM non è `text`. Va casted, e il cast a volte impedisce l'uso dell'indice.

Nel sistema degli abbonamenti, dopo due anni gli stati erano diventati undici, e una richiesta di "pulizia" del dominio (rimuoverne tre, rinominarne due) ha trasformato un'apparente "modifica banale" in una migration di un weekend, con dump-restore parziale di alcune tabelle satellite che usavano il tipo. Il prezzo era arrivato — solo a un punto diverso del ciclo di vita rispetto a MySQL.

---

## Quando passare a CHECK o a lookup

Le bandiere rosse sono le stesse di MySQL — il database cambia, la logica del progetto no:

1. **I valori cambiano spesso** — non solo aggiunti, ma rinominati o ritirati. Se il vocabolario è in evoluzione attiva, lo schema non è il posto giusto per tenerlo
2. **Servono attributi aggiuntivi** — descrizioni multilingua, etichetta breve/estesa, ordine di display, flag attivo. ENUM non li ospita
3. **Decine di valori in crescita** — oltre i 20-30, il `CREATE TYPE` diventa una lista chilometrica scomoda da leggere

`CHECK` constraint in PostgreSQL è un compromesso intermedio pulito: più facile da modificare di un ENUM (basta un `ALTER TABLE ... DROP CONSTRAINT ... ADD CONSTRAINT ...`), meno strutturato di una vera lookup. Va bene per insiemi di 5-15 valori che ogni tanto si toccano.

Nel caso degli abbonamenti, la prima ondata di evoluzione (4 → 11 stati) l'avevamo digerita con `ALTER TYPE ADD VALUE`. La seconda ondata — quella che chiedeva rimozioni e rinomine multiple — è stata l'occasione per la riscrittura verso una lookup table. Non perché ENUM fosse "sbagliato" dall'inizio. Era giusto per un dominio piccolo e stabile, è diventato scomodo quando il dominio ha smesso di essere stabile.

---

## Lookup table fatta bene, con un ENUM dentro

Anche qui il pattern è analogo a quello che abbiamo visto per MySQL, e — sorpresa fino a un certo punto — un ENUM dentro la lookup table ha senso anche in PostgreSQL.

```sql
CREATE TYPE codice_stato_abbonamento AS ENUM (
  'ATTIVO','SOSPESO','TERMINATO','SCADUTO'
);

CREATE TABLE stati_abbonamento (
  id          SMALLSERIAL PRIMARY KEY,
  codice      codice_stato_abbonamento NOT NULL UNIQUE,
  descrizione TEXT NOT NULL,
  ordine      SMALLINT NOT NULL DEFAULT 0,
  attivo      BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO stati_abbonamento (codice, descrizione, ordine) VALUES
  ('ATTIVO',     'Abbonamento attivo e funzionante',     10),
  ('SOSPESO',    'Sospeso, riattivabile',                20),
  ('TERMINATO',  'Disdetta dal cliente',                 30),
  ('SCADUTO',    'Naturale scadenza contratto',          40);

CREATE TABLE abbonamenti (
  id        BIGINT PRIMARY KEY,
  stato_id  SMALLINT NOT NULL,
  CONSTRAINT fk_stato 
    FOREIGN KEY (stato_id) REFERENCES stati_abbonamento(id)
);
```

I tre vantaggi sono gli stessi che avevamo visto in MySQL:

**La master porta solo l'id**, non il codice. Due byte (`SMALLINT`) invece dei 4 dell'OID dell'ENUM diretto, su tabelle da centinaia di milioni di righe sono GB risparmiati.

**Codice e descrizione sono attributi della lookup, non chiave**. Rinominare la descrizione di uno stato — passare da "Sospeso, riattivabile" a "Sospensione temporanea, riattivabile" — è una `UPDATE` su una sola riga. Niente ALTER TYPE, niente migration sulla master.

**Attributi extra costano niente**: un campo per la descrizione breve, una tabella collegata per le traduzioni, un flag `valido_dal/valido_al` per gestire stati validi solo in certi periodi. Tutto questo, con ENUM "puro" sulla master, era inaccessibile.

E sull'ENUM interno alla lookup, **tutti i limiti che abbiamo elencato prima diventano irrilevanti**: la tabella `stati_abbonamento` ha 11 righe, un rebuild su 11 righe è invisibile, una migration è banale. Il vincolo "ammette solo questi valori" lo paghiamo a costo zero, senza scrivere un `CHECK` separato.

### Aggiungere e ritirare valori sul pattern lookup

Sul pattern lookup, le due operazioni "delicate" diventano leggere.

**Aggiungere uno stato** (`PRENOTATO`, perché ora gli abbonamenti possono essere "prenotati" prima dell'attivazione):

```sql
-- Estendi l'ENUM nella lookup (operazione di metadata, millisecondi)
ALTER TYPE codice_stato_abbonamento ADD VALUE 'PRENOTATO' BEFORE 'ATTIVO';

-- Inserisci la nuova riga
INSERT INTO stati_abbonamento (codice, descrizione, ordine, attivo) VALUES
  ('PRENOTATO', 'Abbonamento prenotato, non ancora attivo', 5, TRUE);
```

**Ritirare uno stato** (`SCADUTO` viene assorbito da `TERMINATO`): qui in PostgreSQL non c'è `DROP VALUE`. Ma su una lookup di poche righe, ricreare il tipo è un'operazione di pochi secondi anche in produzione:

```sql
-- 1. Migra le righe della lookup che usano il valore "vecchio"
UPDATE stati_abbonamento SET codice = 'TERMINATO' WHERE codice = 'SCADUTO';
-- (Su una sola riga, sotto FK la master continua a puntare allo stesso id)

-- 2. Crea il nuovo tipo con il vocabolario aggiornato
CREATE TYPE codice_stato_abbonamento_v2 AS ENUM (
  'PRENOTATO','ATTIVO','SOSPESO','TERMINATO'
);

-- 3. Cambia il tipo della colonna nella lookup
ALTER TABLE stati_abbonamento 
  ALTER COLUMN codice TYPE codice_stato_abbonamento_v2 
  USING codice::text::codice_stato_abbonamento_v2;

-- 4. Droppa il tipo vecchio
DROP TYPE codice_stato_abbonamento;
ALTER TYPE codice_stato_abbonamento_v2 RENAME TO codice_stato_abbonamento;
```

Quattro passaggi, tutti su una tabella piccola. La master `abbonamenti` — quella con centinaia di milioni di righe — non viene mai toccata. Continua a referenziare `stato_id`, e la FK risolve sempre alla riga giusta della lookup. **L'integrità è ancorata all'id surrogato**, non al codice ENUM, e questa è la chiave del pattern.

---

## La regola d'oro

Il messaggio che porto via dal caso degli abbonamenti — e che vale, identico, sia in PostgreSQL che in MySQL — è:

> Se i valori del dominio non cambieranno mai, ENUM è la scelta giusta. Se cambieranno — anche solo "ogni tanto" — non legare il vocabolario allo schema.

La differenza tra i due database non è in questa regola. È in **dove cade il prezzo** quando il dominio cambia:

- **In MySQL**, aggiungere un valore in posizione specifica costa un rebuild della tabella. Aggiungerlo in coda è economico; corrompe però l'ordinamento.
- **In PostgreSQL**, aggiungere è sempre economico (anche in posizione specifica). Rimuovere o riorganizzare è la migration pesante.

Capire il proprio caso d'uso vuol dire capire **quale tipo di evoluzione probabilmente subirà il dominio**. Solo aggiunte? PostgreSQL ENUM è un alleato. Aggiunte e rimozioni? Meglio una lookup table fin dall'inizio.

---

## La mini-serie cross-DB

Questo è il secondo di una mini-serie sulle enumerazioni nei diversi DBMS. La domanda "ENUM o lookup?" non ha una risposta universale — cambia volto a seconda del database. Il primo articolo, su MySQL, è disponibile qui:

- **[ENUM in MySQL: quando ti semplifica la vita e quando ti complica i giorni](/it/posts/mysql/enum-mysql-semplifica-o-complica/)** — la stessa domanda, una filosofia diversa, e il caso reale di un sistema di tracking spedizioni

I prossimi appuntamenti:

- **Oracle** — `CHECK` constraint, le SQL Domains della 23ai, e perché Oracle è arrivato "tardi" a questo tema
- **Oracle, deep-dive verticale** — come si modellavano le enumerazioni in 19c, cosa è cambiato in 21c, 23ai e 26ai, fino alle nuove Assertions

> 📖 **Se sei capitato qui per primo**: ti consiglio di leggere anche il primo articolo della mini-serie, [quello su MySQL](/it/posts/mysql/enum-mysql-semplifica-o-complica/). Molti dei pattern di cui parliamo qui — le tre strade, la lookup table fatta bene, l'ENUM dentro la lookup — sono introdotti là. Il confronto rende tutto più chiaro.

------------------------------------------------------------------------

## Fonti ufficiali

1. PostgreSQL Documentation — [Enumerated Types](https://www.postgresql.org/docs/current/datatype-enum.html)
2. PostgreSQL Documentation — [`CREATE TYPE`](https://www.postgresql.org/docs/current/sql-createtype.html)
3. PostgreSQL Documentation — [Constraints (CHECK)](https://www.postgresql.org/docs/current/ddl-constraints.html)
4. PostgreSQL Documentation — [`CREATE TABLE` (FOREIGN KEY)](https://www.postgresql.org/docs/current/sql-createtable.html)
5. PostgreSQL Documentation — [`ALTER TYPE` (ADD VALUE)](https://www.postgresql.org/docs/current/sql-altertype.html)

------------------------------------------------------------------------

## Glossario

**[CREATE TYPE AS ENUM](/it/glossary/postgresql-create-type-enum/)** — Statement DDL di PostgreSQL che crea un tipo enumerativo come oggetto di prima classe. A differenza di MySQL, il tipo esiste indipendentemente dalle colonne che lo usano e può essere riutilizzato.

**[ALTER TYPE ADD VALUE](/it/glossary/postgresql-alter-type-add-value/)** — Comando PostgreSQL che aggiunge un valore a un ENUM esistente. Operazione di metadata, transazionale, senza rebuild della tabella. Disponibile da PostgreSQL 9.1, con posizionamento `BEFORE`/`AFTER` da 9.6.

**[OID (Object Identifier)](/it/glossary/postgresql-oid/)** — Identificatore numerico interno usato da PostgreSQL per riferirsi a oggetti di sistema (tabelle, tipi, funzioni). Per gli ENUM, il valore è memorizzato come OID interno di 4 byte.

**[Type safety](/it/glossary/type-safety/)** — Proprietà di un sistema di tipi che impedisce, a parse-time o compile-time, l'uso di valori incompatibili. ENUM in PostgreSQL è un tipo a sé stante, non un vincolo su `VARCHAR`, e questo abilita type safety end-to-end nelle funzioni e procedure.

**[Lookup table](/it/glossary/lookup-table/)** — Tabella di riferimento collegata via foreign key che memorizza i valori validi di un'enumerazione, con eventuali attributi descrittivi (etichetta, ordine, flag attivo). Pattern preferito quando il dominio evolve nel tempo.
