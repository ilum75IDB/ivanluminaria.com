---
title: "Enumerazioni in Oracle: vent'anni di workaround, e la strada che si è aperta con la 23ai"
seoTitle: "Oracle SQL Domains 23ai: enum, CHECK e lookup table"
description: "Oracle non ha mai avuto ENUM nativo. CHECK constraint, lookup table e SQL Domains 23ai: tre strade, un caso reale banking, e cosa arriverà con la 26ai."
date: "2026-06-16T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_workaround_fino_a_23ai"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-workaround-fino-a-23ai.cover.jpg"
---

La domanda è la stessa di [quella che ci siamo posti per MySQL](/it/posts/mysql/enum-mysql-semplifica-o-complica/) e poi [per PostgreSQL](/it/posts/postgresql/enum-postgresql-paga-o-pesa/): una colonna `status` o `type` con un set chiuso di valori, e tre strade davanti. Cambia il database, cambia la filosofia, e cambia anche **quello che il database mette a disposizione**. Su Oracle, fino a poco fa, mancava proprio la prima opzione delle altre due puntate — il tipo ENUM nativo. Per vent'anni la modellazione di un'enumerazione in Oracle è stata un esercizio di workaround, due strade praticabili e una terza che non era mai davvero un'enumerazione.

Con la 23ai è arrivata una risposta strutturale: i **SQL Domains** [1]. Vale la pena entrare nel merito, perché Oracle ci è arrivato per ultimo ma è arrivato bene — e nel mentre la cultura "lookup table" che si è formata sul campo non perde il suo posto.

---

## Le tre strade, in due righe ciascuna

Useremo l'esempio di una tabella `transazioni` con uno stato che assume un set chiuso di valori. Settore banking — il terreno classico di Oracle in Italia, dove un piano dei conti e una tassonomia di stati è normata, audited, raramente improvvisata.

**CHECK constraint**:

```sql
CREATE TABLE transazioni (
  id       NUMBER PRIMARY KEY,
  importo  NUMBER(15,2) NOT NULL,
  stato    VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_stato CHECK (stato IN
    ('IN_ATTESA','AUTORIZZATA','COMPLETATA','STORNATA','RIFIUTATA'))
);
```

Approccio SQL standard. Oracle applica i `CHECK` constraint da decenni — niente sorprese sulla validità del vincolo come accadeva su MySQL prima della 8.0.16. Semplice, leggibile, e per progetti piccoli risolve subito. Il prezzo, su un sistema reale, lo si scopre dopo: la stessa lista di valori va replicata su ogni tabella che ha la stessa colonna `stato`, e ogni modifica diventa un `ALTER TABLE` per ciascuna. Vedremo perché conta.

**Tabella di lookup con foreign key**:

```sql
CREATE TABLE stati_transazione (
  codice     VARCHAR2(20) PRIMARY KEY,
  etichetta  VARCHAR2(100) NOT NULL,
  ordine     NUMBER,
  attivo     CHAR(1) DEFAULT 'Y' CHECK (attivo IN ('Y','N'))
);

CREATE TABLE transazioni (
  id            NUMBER PRIMARY KEY,
  importo       NUMBER(15,2) NOT NULL,
  stato_codice  VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_stato
    FOREIGN KEY (stato_codice) REFERENCES stati_transazione(codice)
);
```

La via "database-puro" e — non è un caso — la scelta culturale dominante nei progetti Oracle enterprise. Una tabella in più, un JOIN in più, e in cambio un'enumerazione che è **un oggetto del database con vita propria**: ci puoi attaccare etichette localizzate, ordine di display, flag attivo/disattivo, audit trail su `MODIFY` della tassonomia, e regole di business più ricche di un semplice "ammesso/non ammesso". Sui sistemi che ho visto in banking, telco e PA italiana negli ultimi vent'anni, **otto volte su dieci la scelta era questa** — e con buona ragione.

**Pseudo-pattern (SUBTYPE, COLLECTION, type-object)**:

```sql
-- Sconsigliato come "enumerazione" per una colonna persistente:
CREATE OR REPLACE TYPE stato_transazione_t AS OBJECT (
  codice VARCHAR2(20)
);
/
```

I `TYPE` di Oracle (SUBTYPE PL/SQL, COLLECTION SQL, type-object) sono potenti, ma **non sono ENUM**. Non danno una validazione nativa sui valori persistiti, non hanno un meccanismo di lookup leggibile via SQL puro, e il dizionario dati non li vede come "tassonomia". Sono uno strumento di astrazione applicativa, non un meccanismo di vincolo. Chi li ha usati per simulare ENUM se n'è generalmente pentito quando il primo report di business ha chiesto di sapere "quanti stati attivi ci sono" — e dalla tabella non si riusciva a estrarli senza una query PL/SQL.

---

## Cosa cambia rispetto a MySQL e PostgreSQL

Se arrivi dalle due puntate precedenti della miniserie, tre cose vanno tenute in tasca prima di scrivere il primo `CREATE TABLE` su Oracle.

**Niente tipo ENUM nativo**. Su MySQL hai `ENUM('A','B','C')` come tipo di colonna; su PostgreSQL hai `CREATE TYPE ... AS ENUM` come oggetto a sé. Su Oracle, fino alla 23ai, queste due opzioni semplicemente non esistevano. Restavano `CHECK` e lookup table.

**`CHECK` è pienamente applicato da sempre**. A differenza di MySQL pre-8.0.16 (dove i `CHECK` venivano parsati e silenziosamente ignorati), Oracle valida i vincoli `CHECK` fin da prima del millennio. Un dettaglio storico ma rilevante: se vieni da MySQL, qui non c'è dubbio sulla loro efficacia.

**Cultura della lookup table radicata**. La community Oracle, per il tipo di clienti che la usano (banking, assicurativo, PA, telco), ha sempre preferito la lookup table al `CHECK`. Non per dogma, ma perché in quei contesti l'evoluzione del set di valori è frequente, l'audit è obbligatorio, la localizzazione delle etichette è uno standard. La lookup table è una palestra di flessibilità — il `CHECK` è una promessa di rigidità.

---

## Quando il `CHECK` basta

Restando dentro il pattern delle altre due puntate, i casi in cui `CHECK` su Oracle è davvero la scelta giusta sono pochi e precisi:

- **Set di valori che non cambierà mai**. Polarità di una misura (`'POS','NEG','ZERO'`), giorni della settimana, mesi dell'anno, polarità contabile (`'DARE','AVERE'`)
- **Tabelle con un solo riferimento al set**. Se la colonna esiste in **una** sola tabella, il prezzo dell'`ALTER TABLE` per aggiungere un valore è marginale
- **Progetti piccoli o monolitici**, dove il dominio del valore è chiaro nel codice e non serve esporlo come "configurazione" alle interfacce utente

Fuori da questi tre scenari, sulla mia esperienza, il `CHECK` invecchia male. Vedo emergere lo stesso pattern in fase di evoluzione: il business chiede di aggiungere un nuovo valore — diciamo `'IN_AUTORIZZAZIONE_MANUALE'` per le transazioni che richiedono intervento — e ci si accorge che la stringa è replicata in 14 tabelle. Quattordici `ALTER TABLE`, quattordici test di regressione, quattordici release note. La lookup table avrebbe richiesto un `INSERT`.

---

## La cultura della lookup table in Oracle (e perché c'è un motivo)

Su un progetto banking di qualche tempo fa — una piattaforma di pagamenti, Oracle 19c, circa 1.200 tabelle nello schema applicativo, team distribuito Italia/Romania — la tassonomia degli stati di transazione era stata modellata con due tabelle:

- `stati_transazione` (codice, etichetta_it, etichetta_en, ordine, attivo, gruppo)
- `stati_transazione_audit` (trigger di MODIFY che teneva storia di chi aveva cambiato cosa)

Niente `CHECK`. Una sola FK a `stati_transazione.codice` su ogni colonna di stato — `transazioni.stato_codice`, `transazioni_storico.stato_codice`, `movimenti.stato_codice`, e una dozzina di altre tabelle del modulo riconciliazione.

Sembrava sovrappensiero, fino al giorno in cui la compliance ha chiesto di poter "**congelare**" temporaneamente uno stato (es. `'STORNATA'`) durante un audit, senza eliminarlo dallo schema — niente nuove righe con quel valore, ma le righe storiche dovevano restare leggibili e queryabili. Con la lookup table è stato un `UPDATE stati_transazione SET attivo = 'N' WHERE codice = 'STORNATA'` più qualche check applicativo. **Tre righe di codice**. Se avessimo avuto un `CHECK` con la lista di stringhe inlined in 18 tabelle, sarebbe stata una settimana di lavoro tra DDL, regression test e finestra di deploy.

Non è la storia di un eroe — è la storia di una scelta architetturale fatta cinque anni prima dal team di design, e di una compliance che ha trovato lo schema pronto per la domanda che ha posto. La cultura lookup table in Oracle è cresciuta da centinaia di episodi così.

---

## L'arrivo dei SQL Domains in 23ai

Con Oracle Database 23ai (rilasciata su engineered system nell'aprile 2024 e poi in disponibilità più ampia) arriva un costrutto che mancava: il **SQL Domain** [1]. È la prima volta che Oracle dà una risposta strutturale al problema "centralizzare il dominio di una colonna come oggetto del database".

```sql
CREATE DOMAIN stato_transazione AS VARCHAR2(20)
  CONSTRAINT chk_stato_transazione CHECK (VALUE IN
    ('IN_ATTESA','AUTORIZZATA','COMPLETATA','STORNATA','RIFIUTATA'))
  DEFAULT 'IN_ATTESA'
  ANNOTATIONS (display 'Stato Transazione',
               description 'Stato del ciclo di vita di una transazione');

CREATE TABLE transazioni (
  id       NUMBER PRIMARY KEY,
  importo  NUMBER(15,2) NOT NULL,
  stato    stato_transazione NOT NULL
);
```

Il `DOMAIN` è un oggetto del dizionario dati (visibile in `DBA_DOMAINS`), riusabile su qualsiasi colonna, e porta con sé tutto il pacchetto: il tipo base, il vincolo `CHECK`, un `DEFAULT`, e — caratteristica originale Oracle, non presente nel `DOMAIN` di PostgreSQL — un sistema di **annotations** che possono essere lette dagli strumenti BI, di reportistica e di UI generation per derivare etichette di display, descrizioni, ordering, ecc.

Il punto forte non è la sintassi — è l'**ALTER DOMAIN**.

---

## `ALTER DOMAIN`: il superpotere che mancava

```sql
ALTER DOMAIN stato_transazione
  CONSTRAINT chk_stato_transazione CHECK (VALUE IN
    ('IN_ATTESA','AUTORIZZATA','COMPLETATA','STORNATA','RIFIUTATA',
     'IN_AUTORIZZAZIONE_MANUALE'));
```

Quel singolo statement aggiorna il vincolo **per tutte le colonne che usano `stato_transazione`** — in 18 tabelle, in 50, non importa. Oracle si fa carico di propagare il check, e di validare le righe esistenti (con `VALIDATE` o `NOVALIDATE`, secondo come preferisci gestire la transizione) [2].

È quello che la lookup table dava già a livello logico (un solo posto dove cambiare i valori ammessi), ora portato a livello del **catalogo schema**, senza richiedere un JOIN, senza richiedere una tabella in più, e senza i 4 byte di OID di una FK numerica.

Per chi ha lavorato vent'anni con Oracle, è una di quelle feature che fanno dire: "**finalmente**". Non perché la lookup table abbia perso il suo posto — il dominio non sostituisce la lookup quando servono etichette localizzate, ordering di display dinamico o audit trail. Lo sostituisce quando servivano **soltanto** validazione e default centralizzati. E quei casi sono molti.

---

## Quando scegliere quale, oggi

Una guida operativa, sintetica:

| Caso | Strada consigliata |
|------|--------------------|
| Set fisso, 1 tabella, dominio del valore noto e immutabile | `CHECK` constraint inline |
| Set fisso, **più** tabelle, su Oracle pre-23ai | Lookup table con FK |
| Set fisso, più tabelle, **su Oracle 23ai+** | `SQL DOMAIN` |
| Set evolutivo + etichette localizzate + ordering dinamico + audit | Lookup table con FK (anche su 23ai+) |
| Validazione cross-tabella (es. somma di stati = N) | Trigger oggi, `ASSERTION` (26ai, in arrivo) domani |

La lookup table **non è morta** con i SQL Domains. È rimasta la scelta giusta quando l'enumerazione è un'**entità di business** — con i suoi attributi, la sua evoluzione, la sua governance. Il SQL Domain è il complemento ideale quando l'enumerazione è un **vincolo di schema** — un dominio puro, senza attributi, riusato su molte colonne.

---

## Cosa arriva con la 26ai: le Assertions

Oracle 26ai (annunciata come prossima major release) porta — tra le altre cose — il supporto formale alle **`ASSERTION`**: un costrutto SQL standard, presente sulla carta da decenni e mai veramente implementato da nessun DBMS mainstream, che permette di esprimere vincoli **cross-tabella**. Vincoli che oggi devi codificare come trigger o come check applicativo, con tutti i rischi del caso (trigger che si scordano, transazioni che bypassano il vincolo, race condition con isolation level rilassati).

Esempio possibile:

```sql
CREATE ASSERTION almeno_uno_attivo CHECK (
  (SELECT COUNT(*) FROM stati_transazione WHERE attivo = 'Y') >= 1
);
```

L'idea è che il motore del database garantisca questo vincolo **a livello transazionale** — niente trigger, niente codice applicativo, validazione centralizzata. Per le enumerazioni gestite a lookup table, le `ASSERTION` aprono uno scenario nuovo: l'integrità dell'intera tassonomia (non solo della singola colonna) diventa esprimibile in DDL.

È materia che svilupperemo quando la 26ai sarà disponibile in test, sui workload reali. Per ora, vale la pena saperla in arrivo e farsi trovare pronti — il design di una tassonomia di stati oggi può già tener conto di dove i vincoli cross-tabella vivranno meglio domani.

---

## La domanda che porto via dalla miniserie

Tre database, tre filosofie, tre strade — e una domanda che resta valida ovunque: **quanto è stabile il tuo set di valori?**

- Se è davvero stabile e locale → `CHECK` (e su Oracle 23ai+ → `DOMAIN`).
- Se ha attributi propri e una governance → lookup table, su qualsiasi DB.
- Se è un'evoluzione frequente di valori "anagrafica" → lookup table, sempre.

Il resto sono dettagli di sintassi e di motore. Quello che conta — e che ho imparato in tre decenni di schema design, su clienti che andavano dalla compagnia assicurativa multi-paese alla banca commerciale italiana — è che **la rigidità di uno schema si paga sull'evoluzione, e la flessibilità si paga sull'integrità**. La scelta è sempre dove vuoi pagare il prezzo. Oracle 23ai, finalmente, ti dà un altro punto in cui pagarlo — più conveniente, in molti casi, di prima.

---

## Fonti ufficiali

1. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
2. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glossario

- **[SQL Domain](/it/glossary/oracle-sql-domain/)** — Costrutto introdotto in Oracle 23ai che permette di definire un tipo base + vincoli + default + annotations come oggetto del dizionario dati, riusabile su molte colonne. Equivalente concettuale del `DOMAIN` di PostgreSQL, ma più ricco di feature di metadati.
- **[CHECK constraint](/it/glossary/check-constraint/)** — Vincolo SQL che limita i valori ammissibili in una colonna o una riga tramite una condizione booleana. Validato dal motore del database al momento dell'INSERT o UPDATE.
- **[Lookup table](/it/glossary/lookup-table/)** — Tabella ausiliaria che contiene il set di valori ammessi per una colonna di tipologia, referenziata via foreign key dalle tabelle "principali". Permette evoluzione runtime del set di valori senza modifiche allo schema.
- **[ALTER DOMAIN](/it/glossary/oracle-alter-domain/)** — Comando Oracle 23ai+ che modifica il vincolo di un `SQL DOMAIN` propagando il cambiamento a tutte le colonne che usano il dominio. Sostituisce molteplici `ALTER TABLE` con un'unica operazione.
- **[ASSERTION](/it/glossary/sql-assertion/)** — Costrutto SQL standard (non ancora implementato da quasi nessun DBMS mainstream) per esprimere vincoli cross-tabella validati a livello transazionale. Annunciato in Oracle 26ai.
