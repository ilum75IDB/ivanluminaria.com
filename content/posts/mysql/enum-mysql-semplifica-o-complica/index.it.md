---
title: "ENUM in MySQL: quando ti semplifica la vita e quando ti complica i giorni"
description: "Le tre strade per modellare un'enumerazione in MySQL — ENUM nativo, CHECK constraint, tabella di lookup. Una raccontata in coppia: dove ENUM è la scelta giusta, dove diventa una palla al piede. Con la storia di un sistema di tracking spedizioni che ha attraversato entrambe le fasi."
date: "2026-06-02T08:03:00+01:00"
draft: false
translationKey: "enum_mysql_semplifica_o_complica"
tags: ["enum", "data-modeling", "schema-design", "alter-table", "check-constraint"]
categories: ["mysql"]
image: "enum-mysql-semplifica-o-complica.cover.jpg"
---

C'è una scena che si ripete in ogni progetto, prima o poi. Stai disegnando una tabella nuova, devi modellare una colonna `status` o `type` o `category`, e la domanda arriva sempre uguale: "ENUM nativo, CHECK constraint, o tabella di lookup?". Tre strade, tre filosofie, e tre risultati molto diversi a seconda di come evolve il sistema.

ENUM è una di quelle feature che caratterizzano MySQL. Pochi altri DBMS mainstream hanno un tipo enumerativo nativo — PostgreSQL ce l'ha, Oracle è arrivato a qualcosa di simile solo con i SQL Domains della 23ai. Per anni, in MySQL, la scelta di usare ENUM è stata praticamente automatica: poche righe di DDL, leggibile, performante, niente JOIN. Funziona. Finché non ti volti, sei anni dopo, e il `status` di quella tabella è diventato un campo minato.

---

## Le tre strade, in due righe ciascuna

Prima di entrare nel merito, le tre opzioni schematizzate. Useremo l'esempio di una tabella `ordini` con uno stato che assume un set chiuso di valori.

**ENUM nativo**:

```sql
CREATE TABLE ordini (
  id     INT PRIMARY KEY,
  status ENUM('NUOVO','IN_LAVORAZIONE','SPEDITO','CONSEGNATO') NOT NULL
);
```

Il tipo `ENUM` è una stringa con vincolo: ammette solo i valori dichiarati. Internamente MySQL memorizza un intero (1 o 2 byte, a seconda di quanti valori) che funge da indice nella lista. Risultato: storage compatto, lettura leggibile.

**CHECK constraint**:

```sql
CREATE TABLE ordini (
  id     INT PRIMARY KEY,
  status VARCHAR(20) NOT NULL,
  CONSTRAINT chk_status CHECK (status IN ('NUOVO','IN_LAVORAZIONE','SPEDITO','CONSEGNATO'))
);
```

Approccio SQL standard. Più verboso ma più flessibile (le condizioni di CHECK possono essere arbitrariamente complesse). Attenzione: prima di MySQL 8.0.16 i CHECK venivano parsati e silenziosamente ignorati. Solo dalla 8.0.16 sono davvero applicati.

**Tabella di lookup con FK**:

```sql
CREATE TABLE stati_ordine (
  codice    VARCHAR(20) PRIMARY KEY,
  etichetta VARCHAR(100) NOT NULL,
  attivo    BOOLEAN DEFAULT TRUE
);

CREATE TABLE ordini (
  id            INT PRIMARY KEY,
  status_codice VARCHAR(20) NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_codice) REFERENCES stati_ordine(codice)
);
```

La via "database-puro". Più tabelle, più JOIN, ma anche più flessibilità: puoi aggiungere attributi (etichette localizzate, ordine di display, flag attivo/disattivo), modificare i valori senza toccare lo schema delle tabelle figlie, e gestire tutto a runtime.

---

## Quando ENUM è la scelta giusta

ENUM brilla in un contesto specifico: **set di valori stabile, semantica controllata da schema**. Quando questi due ingredienti ci sono, ENUM è la scelta più pulita.

Casi tipici dove la stabilità c'è davvero:

- **Giorni della settimana** (`'LUN','MAR','MER','GIO','VEN','SAB','DOM'`) — non sono mai cambiati e non cambieranno
- **Stati binari o ternari fissi** (`'ATTIVO','INATTIVO'` o `'PUBBLICO','PRIVATO','BOZZA'`)
- **Tipologie di transazione contabile** dove il piano dei conti è normato da legge
- **Polarità o segno** in misure tecniche

In tutti questi casi ENUM ti dà tre vantaggi concreti:

1. **Storage compatto**: 1-2 byte per riga contro i 4 di un INT che fa da FK. Su una tabella da 200 milioni di righe sono 400-600 MB risparmiati. Non è il motivo principale per scegliere ENUM, ma è un bonus
2. **Leggibilità nelle query**: `WHERE status = 'SPEDITO'` senza JOIN, senza alias di tabelle aggiuntive. Quando devi debuggare alle tre di notte, conta
3. **Niente migration extra**: la "tabella di lookup" è già lo schema stesso. Niente seed di dati, niente sincronizzazione, niente FK da gestire al deploy

In un sistema dove il dominio è davvero chiuso, ENUM toglie complessità. Una colonna, un vincolo dichiarato nel CREATE TABLE, fine.

---

## Il caso concreto: un sistema di tracking spedizioni

Qualche tempo fa stavo lavorando con il team IT di un grande operatore postale italiano. Si trattava di disegnare il modello dati per un sistema di tracking delle spedizioni: pacchi che entrano in deposito, vengono presi in carico, smistati, consegnati. Lo `status` era una colonna centrale, presente in pressoché ogni query.

Nella prima versione del sistema, gli stati erano cinque, ben definiti dal business: `RICEVUTO`, `IN_DEPOSITO`, `IN_CONSEGNA`, `CONSEGNATO`, `RESPINTO`. ENUM, mano sulla coscienza, era la scelta giusta:

```sql
ALTER TABLE spedizioni
  ADD COLUMN status ENUM('RICEVUTO','IN_DEPOSITO','IN_CONSEGNA','CONSEGNATO','RESPINTO') 
  NOT NULL DEFAULT 'RICEVUTO';
```

Per due anni di produzione ha funzionato in silenzio. Niente JOIN nei tracciati di consegna, niente seed di tabelle di stati da mantenere, ogni query con `WHERE status = '...'` era leggibile come una frase di prosa. Il DBA dormiva tranquillo.

Poi sono iniziati i problemi.

---

## I limiti, raccontati onestamente

Il primo segnale è arrivato con una mail dal product manager: serve aggiungere uno stato `PRENOTATO`, per gestire le spedizioni che il cliente ha annunciato ma non ancora consegnato al deposito. Operazione apparentemente banale. Operazione che richiede questo:

```sql
ALTER TABLE spedizioni
  MODIFY COLUMN status 
  ENUM('PRENOTATO','RICEVUTO','IN_DEPOSITO','IN_CONSEGNA','CONSEGNATO','RESPINTO') 
  NOT NULL DEFAULT 'RICEVUTO';
```

Sembra una riga sola. Ma se vuoi aggiungere `PRENOTATO` **prima** di `RICEVUTO` (per coerenza semantica nella sequenza), MySQL deve riscrivere la tabella. Tutta. Su `spedizioni` da centocinquanta milioni di righe, in produzione, con `Online DDL` configurato bene, sono comunque parecchie ore di carico extra sullo storage e sul replication lag. Aggiungere semplicemente in fondo `MODIFY COLUMN status ENUM(...,'PRENOTATO')` sarebbe stato più leggero — ma avrebbe creato un set di valori con un ordinamento posizionale assurdo: `CONSEGNATO` viene "prima" di `PRENOTATO` nel sort? Tecnicamente sì.

Eccoli, i limiti di ENUM, raccontati senza pietà:

**Case-insensitive**. `'ATTIVO'` e `'attivo'` sono lo stesso valore. Per chi viene da PostgreSQL può essere una sorpresa amara. In MySQL è un design choice esplicito, ma è bene saperlo prima.

**Ordinamento per posizione di dichiarazione**, non alfabetico. Se la query fa `ORDER BY status`, l'ordine è quello in cui hai dichiarato i valori nel `CREATE TABLE`. Bug subdolo: aggiungi `'PRENOTATO'` in fondo per non rifare la tabella, e improvvisamente il tuo report ordinato per stato mostra `'PRENOTATO'` dopo `'RESPINTO'`. Nessuno si lamenta finché qualcuno non se ne accorge.

**Modifiche pesanti su tabelle grandi**. Aggiungere un valore in fondo è leggero. Modificare la posizione, rinominare un valore, rimuovere un valore — tutto richiede un rebuild. Con Online DDL su MySQL 8 è meno doloroso che in passato, ma non è gratis.

**Lock di tabella in alcuni scenari**. Le combinazioni di operazioni che richiedono `ALGORITHM=COPY` esistono ancora, e su tabelle critiche vanno valutate con cura.

Nel sistema di tracking, sei anni dopo, di stati ne erano stati aggiunti dodici. Ogni nuovo stato — perché un nuovo corriere, perché un nuovo canale, perché una nuova policy di reso — era un ALTER notturno con DBA in piedi davanti al monitor. ENUM era passato da semplificare la vita a complicarla.

---

## Quando passare a CHECK o a lookup

La domanda diventa: a partire da quale punto conviene mollare ENUM e prendere un'altra strada?

Le bandiere rosse sono tre:

1. **I valori cambiano spesso**: se ogni trimestre il business chiede di aggiungere, rinominare o disattivare un valore, lo schema non dovrebbe essere la "tabella" delle enumerazioni. Una vera tabella di lookup gestita da pannello admin è la strada
2. **Servono attributi aggiuntivi**: descrizione localizzata in 4 lingue, etichetta breve vs estesa, ordine di display, flag attivo/disattivo. Tutto questo in ENUM non lo metti. Con lookup table, ogni valore è una riga che può avere quante colonne vuoi
3. **Tante decine di valori in crescita**: oltre i 20-30 valori, ENUM diventa difficile da leggere e da mantenere nel `CREATE TABLE`. Il `DDL` diventa una lista chilometrica

In questi casi `CHECK` constraint è un compromesso intermedio: più flessibile di ENUM (rinominare un valore è solo un'`ALTER CONSTRAINT`), meno strutturato di una vera lookup table. Va bene per insiemi di 5-15 valori che ogni tanto si toccano, ma senza la necessità di attributi.

Nel caso del tracking spedizioni, alla fine la riscrittura è andata in direzione lookup table. Vale la pena dirlo: non perché ENUM fosse "sbagliato" nella versione 1. Era giusto, sei anni prima, per un dominio che era davvero piccolo e stabile. È diventato sbagliato quando il dominio è cambiato, e nessuno l'aveva previsto. Che è esattamente quello che succede in molti progetti reali.

---

## Lookup table fatta bene

Se decidi di andare in direzione lookup, vale la pena disegnarla nel modo che ti permette di crescere nel tempo. Il pattern naturale — quello che vediamo nei sistemi maturi — separa due ruoli che ENUM teneva mescolati: l'**identificatore** del valore e la **descrizione** del valore.

```sql
CREATE TABLE stati_spedizione (
  id          SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  codice      VARCHAR(20) NOT NULL UNIQUE,
  descrizione VARCHAR(200) NOT NULL,
  ordine      SMALLINT NOT NULL DEFAULT 0,
  attivo      BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO stati_spedizione (codice, descrizione, ordine) VALUES
  ('RICEVUTO',    'Spedizione ricevuta in deposito',  10),
  ('IN_DEPOSITO', 'In attesa di smistamento',         20),
  ('IN_CONSEGNA', 'Affidata al corriere',             30),
  ('CONSEGNATO',  'Consegnata al destinatario',       40),
  ('RESPINTO',    'Respinta dal destinatario',        50);

CREATE TABLE spedizioni (
  id        INT PRIMARY KEY,
  stato_id  SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_stato FOREIGN KEY (stato_id) REFERENCES stati_spedizione(id)
);
```

Tre cose interessanti emergono da questo schema.

**La master porta solo l'id**, non il codice. Due byte per riga (`SMALLINT`) invece dei 20+ di un `VARCHAR(20)`. Su una tabella da 150 milioni di righe sono 2-3 GB di differenza tra dati e indici, oltre a JOIN più veloci grazie al confronto su intero.

**Il codice e la descrizione sono attributi della lookup, non chiave**. Questo significa che rinominare uno stato — passare da "Consegnato" a "Consegnato al destinatario" — è una `UPDATE` su una sola riga della lookup. Nessuna migrazione, nessun rebuild, nessun `ALTER`. Lo schema delle tabelle figlie non viene toccato. Avere il `codice` come chiave naturale sembrava elegante quattro anni fa, ma alla prima volta che il business chiede di cambiare il testo di un'etichetta capisci perché l'id surrogato esisteva.

**Gli attributi extra costano niente da aggiungere**: una colonna `descrizione_breve` per i tracciati SMS, una colonna `ordine` per il sort visuale nelle dashboard, una tabella collegata per le traduzioni multilingua. Tutto questo era impossibile con ENUM, ed è normale con una lookup table ben disegnata.

Il prezzo da pagare è che le query ad-hoc richiedono un JOIN per leggere il nome dello stato in chiaro:

```sql
SELECT s.id, ss.codice
FROM spedizioni s
JOIN stati_spedizione ss ON ss.id = s.stato_id
WHERE ss.codice = 'IN_CONSEGNA';
```

Più verbose di un `WHERE status = 'IN_CONSEGNA'` su ENUM, ma è il prezzo della flessibilità. E sui report più frequenti il JOIN si ottimizza con un indice composto e una `view` che incapsula la complessità, lasciando le query applicative leggibili.

---

## La regola d'oro

La sintesi che porto via da questa storia, e che ripeto ai team quando arriva la domanda "ENUM o lookup?", è semplice:

> Se i valori non cambieranno mai, ENUM è la scelta giusta. Se cambieranno — anche solo "ogni tanto" — non legare il vocabolario allo schema.

Tutto qui. Il difficile non è scegliere tra le tre strade. Il difficile è capire onestamente, al momento della scelta, in quale dei due mondi ti trovi. E quello, di solito, lo capisci solo guardando come è cambiato il dominio negli ultimi due o tre anni — non leggendo i requisiti del prossimo sprint.

---

## La mini-serie cross-DB

Questo è il primo di quattro articoli sulle enumerazioni nei diversi DBMS. La domanda "ENUM o lookup?" non riguarda solo MySQL — ogni database ha la sua filosofia, ed è interessante vedere come la stessa scelta cambi forma passando da un mondo all'altro.

I prossimi appuntamenti:

- **PostgreSQL** — `CREATE TYPE ... AS ENUM`, `ALTER TYPE ADD VALUE`, e la sorpresa: in PostgreSQL ENUM è *case-sensitive*
- **Oracle** — `CHECK` constraint, le SQL Domains della 23ai, e perché Oracle è arrivato "tardi" su questo tema
- **Oracle, deep-dive verticale** — come si modellavano le enumerazioni in 19c, cosa è cambiato in 21c, 23ai e 26ai, fino alle nuove Assertions

Stessa domanda, tre filosofie. Il bello è proprio nel confronto.
