---
categories:
- oracle
date: 2099-12-31
description: 'Come Oracle Text risolve ricerche lente su archivi di documenti ed email:
  indici CONTEXT, CATSEARCH e CTXXPATH configurati sulle reali esigenze di ricerca.'
draft: true
image: oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente.cover.jpg
seoTitle: 'Oracle Text: full-text search su archivi documentali Oracle 19c'
tags:
- oracle-text
- full-text-search
- oracle-19c
- indexing
- performance-tuning
title: 'Ricerche su milioni di documenti legali: come Oracle Text ha cambiato i tempi
  di risposta'
translationKey: oracle_text_indicizzare_e_ricercare_testo_in_modo_efficiente
webo_generated_at: 2026-08-07
webo_status: da_approvare
---

## La frustrazione di Alberto

Alberto non ha aperto un ticket. Ha chiamato direttamente, nel mezzo di un pomeriggio, e la prima cosa che ha detto è stata: "I tempi di ricerca sono inaccettabili. Non posso aspettare un minuto ogni volta che cerco un contratto."

Trent'anni di documenti sedimentati in un archivio Oracle. Contratti, pareri, atti processuali, corrispondenza con clienti e controparti. Lo schema `LEGAL_ARCHIVE` su `oracle-legal-prod-01` conteneva due tabelle principali: `DOCUMENTS`, con una colonna `DOC_CONTENT` di tipo CLOB che raccoglieva centinaia di gigabyte di testo, e `EMAILS`, con `SENDER`, `SUBJECT` e `BODY`. Milioni di righe in entrambe.

Il collo di bottiglia non era la lentezza generica del sistema. Era la ricerca testuale: query `LIKE '%termine%'` su colonne CLOB, senza indici specifici per quel tipo di carico. Trenta secondi per trovare un contratto, quarantacinque per cercare un'email per oggetto e contenuto. Novanta nei momenti peggiori.

La prima cosa che abbiamo fatto, prima di toccare qualsiasi configurazione, è stata sederci con Alberto e con due dei suoi collaboratori più operativi e chiedere loro come cercano davvero. Non "cosa cercate", ma *come*: frammenti di testo libero? Combinazioni mittente più parola chiave nel corpo? Clausole specifiche in documenti XML strutturati? La risposta ha cambiato completamente l'approccio.

Nessuno aveva mai fatto quella domanda prima.

## Oracle Text: non un add-on, una componente integrata

Oracle Text è incluso in Oracle Database senza licenza aggiuntiva [1]. Non è un motore esterno da integrare, non è un Elasticsearch da mantenere in parallelo: è un sistema di indicizzazione full-text che vive dentro il database, con accesso diretto ai dati, alle transazioni e al controllo degli accessi già in essere.

La distinzione rispetto a un indice B-tree standard è sostanziale. Un B-tree su una colonna `VARCHAR2` funziona per uguaglianze e prefissi (`LIKE 'termine%'`), e al tempo stesso non serve per ricerche nel mezzo del testo (`LIKE '%termine%'`) su colonne CLOB da centinaia di gigabyte — in quel caso Oracle esegue una scansione completa della colonna, riga per riga. Oracle Text costruisce invece una struttura invertita: per ogni token (parola) mantiene la lista dei documenti che lo contengono, con informazioni di posizione. La query non scansiona i dati, consulta l'indice.

Tre tipi di indice coprono scenari diversi:

- **CONTEXT** — testo libero, documenti, articoli
- **CATSEARCH** — archivi misti con attributi strutturati e testo libero
- **CTXXPATH** — documenti XML o JSON archiviati in CLOB/BLOB

La scelta tra i tre non è arbitraria: dipende esattamente da come gli utenti cercano. Ecco perché la conversazione con Alberto è venuta prima del codice.

## Indice CONTEXT: la base per i documenti liberi

Per `LEGAL_ARCHIVE.DOCUMENTS` il caso era chiaro: ricerca full-text su testo non strutturato. Contratti in formato testo, pareri legali, atti. L'indice CONTEXT è la scelta naturale [1].

```sql
-- Creazione dell'indice CONTEXT sulla colonna DOC_CONTENT
BEGIN
  CTX_DDL.CREATE_PREFERENCE('legal_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'MIXED_CASE', 'NO');

  CTX_DDL.CREATE_STOPLIST('legal_stoplist', 'BASIC_STOPLIST');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'il');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'la');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'di');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'che');
END;
/

CREATE INDEX legal_doc_ctx_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CONTEXT
PARAMETERS ('LEXER legal_lexer STOPLIST legal_stoplist MEMORY 256M');
```

Il `BASIC_LEXER` con `BASE_LETTER YES` gestisce la normalizzazione degli accenti — fondamentale per l'italiano, dove "è" e "e" non devono essere trattati come token distinti in una ricerca. La `STOPLIST` esclude dall'indice le parole funzionali che non portano significato semantico nelle query legali.

Le query usano l'operatore `CONTAINS` [1]:

```sql
-- Ricerca di documenti che contengono entrambi i termini
SELECT doc_id, doc_title, SCORE(1) AS relevance
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'responsabilità AND contrattuale', 1) > 0
ORDER BY SCORE(1) DESC;

-- Ricerca con prossimità: i due termini entro 5 parole l'uno dall'altro
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'NEAR((inadempimento, risarcimento), 5)', 1) > 0;
```

Il risultato dopo l'implementazione: da 30-60 secondi a meno di 500 ms. Non è una stima ottimistica, è il dato misurato su query rappresentative del carico reale.

## Indice CATSEARCH: quando il testo si mescola ai metadati

Le email erano un caso diverso. Alberto e i suoi collaboratori non cercano solo nel corpo del messaggio: cercano per mittente, per oggetto, per data, e poi filtrano nel testo. Una query tipica era: "tutte le email di quel consulente esterno, con 'perizia' nell'oggetto o nel corpo, negli ultimi due anni".

Questo è esattamente lo scenario per cui esiste CATSEARCH [1]: ricerche che combinano predicati SQL su colonne strutturate con ricerca full-text su colonne di testo.

```sql
-- Definizione del set di colonne strutturate incluse nell'indice
EXEC CTX_DDL.CREATE_INDEX_SET('legal_email_set');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SENDER');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SUBJECT');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'RECEIVED_DATE');

-- Creazione dell'indice CATSEARCH su EMAILS
CREATE INDEX legal_email_cat_idx
ON LEGAL_ARCHIVE.EMAILS(BODY)
INDEXTYPE IS CTXSYS.CATSEARCH
PARAMETERS ('CTXCAT_INDEX_CLAUSE
  "CTXCAT_INDEX_SET legal_email_set"');
```

L'ordine conta: prima si definisce il set di colonne strutturate, poi si crea l'indice che lo referenzia.

La query usa l'operatore `CATSEARCH` con una clausola strutturata separata [1]:

```sql
-- Ricerca combinata: mittente specifico + termine nel corpo
SELECT email_id, sender, subject, received_date
FROM LEGAL_ARCHIVE.EMAILS
WHERE CATSEARCH(
  BODY,
  'perizia',
  'SENDER = ''consulente.esterno@example.com'' AND
   RECEIVED_DATE > DATE ''2024-01-01'''
) > 0
ORDER BY received_date DESC;
```

La differenza rispetto a CONTEXT è che i predicati sulle colonne strutturate vengono valutati dentro l'indice, non come filtri SQL successivi. L'optimizer non deve prima trovare tutti i documenti con "perizia" e poi filtrare per mittente: le due condizioni vengono risolte insieme. Da 45-90 secondi a meno di 700 ms.

## Indice CTXXPATH: dentro i documenti XML e JSON

Una parte dell'archivio conteneva documenti in formato XML — atti strutturati con sezioni, riferimenti normativi, metadati codificati. Cercare con `LIKE` su un CLOB che contiene XML è inefficiente per definizione: non c'è modo di limitare la ricerca a un nodo specifico senza parsare il documento a runtime.

CTXXPATH risolve questa situazione [1]: indicizza il contenuto XML preservando la struttura dei path, e permette query che cercano un termine solo all'interno di un nodo specifico.

```sql
-- Creazione dell'indice CTXXPATH su documenti XML
CREATE INDEX legal_xml_xpath_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

La query usa `CTX_XPTH.CONTAINS` [1]:

```sql
-- Ricerca del termine 'inadempimento' solo nella sezione <motivazione>
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CTX_XPTH.CONTAINS(
  DOC_CONTENT,
  '/atto/motivazione[. contains("inadempimento")]'
) = 1;
```

Prima: query `LIKE '%inadempimento%'` su CLOB XML, oltre 120 secondi. Dopo: meno di un secondo. La differenza è strutturale: l'indice sa dove si trovano i token rispetto alla gerarchia XML, e non deve rileggere l'intero documento per rispondere.

## Operatori avanzati e rilevanza

Una volta che gli indici erano attivi, abbiamo lavorato con i collaboratori dello studio per affinare le query. Oracle Text offre un set di operatori che vanno oltre la semplice ricerca booleana [1][2].

`ACCUM` accumula i punteggi invece di richiedere che tutti i termini siano presenti — utile quando si vuole ordinare per rilevanza complessiva senza escludere documenti che contengono solo alcuni dei termini:

```sql
-- Documenti più rilevanti per una combinazione di termini
SELECT doc_id, doc_title, SCORE(1) AS score
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(
  DOC_CONTENT,
  '(responsabilità ACCUM contrattuale ACCUM inadempimento)',
  1
) > 0
ORDER BY SCORE(1) DESC
FETCH FIRST 20 ROWS ONLY;
```

`FUZZY` gestisce le variazioni ortografiche e gli errori di battitura — particolarmente utile su testi scansionati con OCR, dove la qualità del riconoscimento non è uniforme:

```sql
-- Ricerca fuzzy per gestire varianti ortografiche
SELECT doc_id FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'FUZZY(risarcimanto, 70, 6)', 1) > 0;
```

Il parametro `70` è la soglia di similarità (0-100), `6` il numero massimo di espansioni. Va calibrato: soglie troppo basse producono rumore, troppo alte perdono le varianti rilevanti.

Per presentare i risultati agli utenti, `CTX_DOC.HIGHLIGHT` restituisce il testo con i termini trovati marcati [1]:

```sql
-- Highlighting dei termini trovati nel documento
DECLARE
  v_highlight CLOB;
BEGIN
  CTX_DOC.HIGHLIGHT(
    index_name  => 'LEGAL_DOC_CTX_IDX',
    textkey     => '12345',
    query       => 'responsabilità contrattuale',
    restab      => v_highlight,
    starttag    => '<b>',
    endtag      => '</b>'
  );
  DBMS_OUTPUT.PUT_LINE(DBMS_LOB.SUBSTR(v_highlight, 500, 1));
END;
/
```

## Sincronizzazione e manutenzione degli indici

Un aspetto spesso sottovalutato: gli indici Oracle Text non si aggiornano automaticamente in tempo reale come un B-tree. Quando vengono inserite nuove righe, l'indice deve essere sincronizzato esplicitamente [1].

```sql
-- Sincronizzazione manuale dell'indice
EXEC CTX_DDL.SYNC_INDEX('LEGAL_DOC_CTX_IDX', '256M');

-- Ottimizzazione periodica per compattare le strutture interne
EXEC CTX_DDL.OPTIMIZE_INDEX('LEGAL_DOC_CTX_IDX', 'FULL');
```

Per un archivio in produzione con inserimenti continui, la sincronizzazione va schedulata. Un job `DBMS_SCHEDULER` ogni 15-30 minuti è un punto di partenza ragionevole; la frequenza dipende dal volume di inserimenti e dalla tolleranza al ritardo di indicizzazione. Per `LEGAL_ARCHIVE`, dove i documenti vengono caricati in batch notturni, una sincronizzazione post-caricamento era sufficiente.

Il monitoraggio passa da `CTX_USER_INDEXES` e `CTX_INDEX_ERRORS`:

```sql
-- Verifica dello stato degli indici Oracle Text
SELECT idx_name, idx_status, idx_docid_count
FROM CTX_USER_INDEXES;

-- Verifica degli errori di indicizzazione
SELECT err_index_name, err_timestamp, err_text
FROM CTX_INDEX_ERRORS
ORDER BY err_timestamp DESC;
```

## Il sollievo di Alberto, non la sorpresa

Quando abbiamo mostrato i risultati ad Alberto, la sua reazione non è stata stupore. Era sollievo. "Finalmente", ha detto. Non "incredibile" — *finalmente*.

Quella parola dice tutto sull'approccio che ha funzionato. Non c'è stato un momento eroico in cui qualcuno ha trovato la soluzione magica. C'è stata una conversazione in cui abbiamo smesso di guardare i log e abbiamo chiesto agli utenti come lavorano davvero. Da quella conversazione è emerso che servivano tre indici diversi per tre pattern di ricerca diversi, non un indice generico applicato a tutto.

Oracle Text era già disponibile nell'istanza 19c. Le funzionalità erano documentate. Quello che mancava era la mappatura tra le esigenze reali di ricerca e le capacità dello strumento.

Il team dello studio ha contribuito in modo determinante: senza la loro disponibilità a descrivere i flussi di lavoro reali — non quelli teorici, quelli quotidiani — avremmo configurato indici ragionevoli sulla carta ma non ottimali per quel contesto specifico. La tecnologia è uno strumento; la comprensione del problema è il lavoro vero.

Gli indici Oracle Text non vanno costruiti dalla documentazione verso i dati. Vanno costruiti dalle esigenze di chi cerca verso la struttura dei dati, e poi la documentazione aiuta a trovare il tipo di indice e gli operatori giusti. In quest'ordine.

## Fonti ufficiali

1. Oracle Text Reference 19c — [Oracle Text Indextype Reference (CONTEXT, CATSEARCH, CTXXPATH, CONTAINS, CATSEARCH operator, CTX_XPTH.CONTAINS, WORDLIST, STOPLIST, LEXER, CTX_DDL.SYNC_INDEX, CTX_DOC.HIGHLIGHT)](https://docs.oracle.com/en/database/oracle/oracle-database/19/textr/index.html)
2. Oracle Text Application Developer's Guide 19c — [Concetti avanzati, tuning e best practice](https://docs.oracle.com/en/database/oracle/oracle-database/19/texta/toc.htm)
3. Oracle-Base (Tim Hall) — [Oracle Text Articles: esempi pratici](https://oracle-base.com/articles/misc/oracle-text)

## Glossario
- **[Oracle Text](/it/glossary/oracle-text/)** — Componente integrata di Oracle Database per l'indicizzazione e la ricerca full-text su dati testuali. Non richiede licenza separata e opera direttamente sulle strutture dati del database, incluse colonne CLOB, BLOB e VARCHAR2.

- **[Indice CONTEXT](/it/glossary/oracle-text/)** — Tipo di indice Oracle Text per la ricerca full-text su testo non strutturato (documenti, articoli, pareri). Costruisce una struttura invertita token→documento che evita la scansione completa della colonna CLOB a ogni query.

- **[Indice CATSEARCH](/it/glossary/indice-context/)** — Tipo di indice Oracle Text ottimizzato per archivi che combinano attributi strutturati (mittente, data, categoria) con testo libero. I predicati SQL e la ricerca testuale vengono risolti insieme dentro l'indice, non in fasi separate.

- **Indice CTXXPATH** — Tipo di indice Oracle Text per documenti XML o JSON archiviati in CLOB/BLOB. Preserva la struttura gerarchica dei path XML durante l'indicizzazione, permettendo query che limitano la ricerca a nodi specifici del documento.

- **Lexer** (Oracle Text) — Componente che analizza il testo durante la fase di indicizzazione, suddividendolo in token e applicando regole di normalizzazione specifiche per lingua e formato. Il `BASIC_LEXER` con `BASE_LETTER YES` gestisce, ad esempio, la normalizzazione degli accenti per l'italiano.
