---
categories:
- oracle
date: '2026-08-11'
description: Cum am redus timpii de căutare de la 90 de secunde la sub un secundă
  pe un arhiv Oracle de 30 de ani, alegând indexul potrivit pentru fiecare pattern
  de căutare.
draft: false
image: oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente.cover.jpg
seoTitle: 'Oracle Text CONTEXT CATSEARCH CTXXPATH: full-text pe arhive juridice'
tags:
- oracle-text
- full-text-search
- oracle-19c
- clob
- indexing
title: 'Frustrarea lui Alberto: Oracle Text și cele trei tipuri de index pentru arhiva
  juridică'
translationKey: oracle_text_indicizzare_e_ricercare_testo_in_modo_efficiente
webo_generated_at: 2026-08-08
webo_status: scheduled
---

## Frustrarea lui Alberto

Alberto nu a deschis un tichet. A sunat direct, în mijlocul unei după-amiezi, și primul lucru pe care l-a spus a fost: „Timpii de căutare sunt inacceptabili. Nu pot să aștept un minut de fiecare dată când caut un contract."

Treizeci de ani de documente sedimentate într-un arhiv Oracle. Contracte, avize, acte procesuale, corespondență cu clienți și contrapărți. Schema `LEGAL_ARCHIVE` pe `oracle-legal-prod-01` conținea două tabele principale: `DOCUMENTS`, cu o coloană `DOC_CONTENT` de tip CLOB care aduna sute de gigabyți de text, și `EMAILS`, cu `SENDER`, `SUBJECT` și `BODY`. Milioane de rânduri în ambele.

Blocajul nu era o lentoare generică a sistemului. Era căutarea textuală: interogări `LIKE '%termen%'` pe coloane CLOB, fără indecși specifici pentru acel tip de sarcină. Treizeci de secunde pentru a găsi un contract, patruzeci și cinci pentru a căuta un e-mail după subiect și conținut. Nouăzeci în momentele cele mai grele.

Primul lucru pe care l-am făcut, înainte de a atinge vreo configurație, a fost să ne așezăm cu Alberto și cu doi dintre colaboratorii lui cei mai operaționali și să-i întrebăm cum caută cu adevărat. Nu „ce căutați", ci *cum*: fragmente de text liber? Combinații expeditor plus cuvânt-cheie în corp? Clauze specifice în documente XML structurate? Răspunsul a schimbat complet abordarea.

Nimeni nu pusese întrebarea asta înainte.

## Oracle Text: nu un add-on, o componentă integrată

Oracle Text este inclus în Oracle Database fără licență suplimentară [1]. Nu este un motor extern de integrat, nu este un Elasticsearch de menținut în paralel: este un sistem de indexare full-text care trăiește în interiorul bazei de date, cu acces direct la date, la tranzacții și la controlul accesului deja existent.

Distincția față de un index B-tree standard este substanțială. Un B-tree pe o coloană `VARCHAR2` funcționează pentru egalități și prefixuri (`LIKE 'termen%'`), și în același timp nu servește pentru căutări în mijlocul textului (`LIKE '%termen%'`) pe coloane CLOB de sute de gigabyți — în acel caz Oracle execută o scanare completă a coloanei, rând cu rând. Oracle Text construiește în schimb o structură inversată: pentru fiecare token (cuvânt) menține lista documentelor care îl conțin, cu informații de poziție. Interogarea nu scanează datele, consultă indexul.

Trei tipuri de index acoperă scenarii diferite:

- **CONTEXT** — text liber, documente, articole
- **CATSEARCH** — arhive mixte cu atribute structurate și text liber
- **CTXXPATH** — documente XML sau JSON arhivate în CLOB/BLOB

Alegerea dintre cele trei nu este arbitrară: depinde exact de modul în care utilizatorii caută. De aceea conversația cu Alberto a venit înaintea codului.

## Indexul CONTEXT: baza pentru documentele libere

Pentru `LEGAL_ARCHIVE.DOCUMENTS` cazul era clar: căutare full-text pe text nestructurat. Contracte în format text, avize juridice, acte. Indexul CONTEXT este alegerea naturală [1].

```sql
-- Crearea indexului CONTEXT pe coloana DOC_CONTENT
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

`BASIC_LEXER` cu `BASE_LETTER YES` gestionează normalizarea accentelor — esențial pentru italiană, unde „è" și „e" nu trebuie tratate ca tokeni diferiți într-o căutare. `STOPLIST` exclude din index cuvintele funcționale care nu aduc semnificație semantică în interogările juridice.

Interogările folosesc operatorul `CONTAINS` [1]:

```sql
-- Căutare de documente care conțin ambii termeni
SELECT doc_id, doc_title, SCORE(1) AS relevance
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'responsabilità AND contrattuale', 1) > 0
ORDER BY SCORE(1) DESC;

-- Căutare cu proximitate: cei doi termeni la cel mult 5 cuvinte distanță
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'NEAR((inadempimento, risarcimento), 5)', 1) > 0;
```

Rezultatul după implementare: de la 30-60 de secunde la sub 500 ms. Nu este o estimare optimistă, este cifra măsurată pe interogări reprezentative pentru sarcina reală.

## Indexul CATSEARCH: când textul se amestecă cu metadatele

E-mailurile erau un caz diferit. Alberto și colaboratorii lui nu caută doar în corpul mesajului: caută după expeditor, după subiect, după dată, și apoi filtrează în text. O interogare tipică era: „toate e-mailurile de la acel consultant extern, cu 'expertiză' în subiect sau în corp, din ultimii doi ani".

Acesta este exact scenariul pentru care există CATSEARCH [1]: căutări care combină predicate SQL pe coloane structurate cu căutare full-text pe coloane de text.

```sql
-- Definirea setului de coloane structurate incluse în index
EXEC CTX_DDL.CREATE_INDEX_SET('legal_email_set');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SENDER');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SUBJECT');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'RECEIVED_DATE');

-- Crearea indexului CATSEARCH pe EMAILS
CREATE INDEX legal_email_cat_idx
ON LEGAL_ARCHIVE.EMAILS(BODY)
INDEXTYPE IS CTXSYS.CATSEARCH
PARAMETERS ('CTXCAT_INDEX_CLAUSE
  "CTXCAT_INDEX_SET legal_email_set"');
```

Ordinea contează: mai întâi se definește setul de coloane structurate, apoi se creează indexul care îl referențiază.

Interogarea folosește operatorul `CATSEARCH` cu o clauză structurată separată [1]:

```sql
-- Căutare combinată: expeditor specific + termen în corp
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

Diferența față de CONTEXT este că predicatele pe coloanele structurate sunt evaluate în interiorul indexului, nu ca filtre SQL ulterioare. Optimizatorul nu trebuie să găsească mai întâi toate documentele cu „expertiză" și apoi să filtreze după expeditor: cele două condiții sunt rezolvate împreună. De la 45-90 de secunde la sub 700 ms.

## Indexul CTXXPATH: în interiorul documentelor XML și JSON

O parte din arhiv conținea documente în format XML — acte structurate cu secțiuni, referințe normative, metadate codificate. A căuta cu `LIKE` pe un CLOB care conține XML este ineficient prin definiție: nu există nicio modalitate de a limita căutarea la un nod specific fără a parsa documentul la runtime.

CTXXPATH rezolvă această situație [1]: indexează conținutul XML păstrând structura path-urilor și permite interogări care caută un termen doar în interiorul unui nod specific.

```sql
-- Crearea indexului CTXXPATH pe documente XML
CREATE INDEX legal_xml_xpath_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

Interogarea folosește `CTX_XPTH.CONTAINS` [1]:

```sql
-- Căutarea termenului 'inadempimento' doar în secțiunea <motivazione>
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CTX_XPTH.CONTAINS(
  DOC_CONTENT,
  '/atto/motivazione[. contains("inadempimento")]'
) = 1;
```

Înainte: interogare `LIKE '%inadempimento%'` pe CLOB XML, peste 120 de secunde. După: sub o secundă. Diferența este structurală: indexul știe unde se află tokenii în raport cu ierarhia XML și nu trebuie să recitească întregul document pentru a răspunde.

## Operatori avansați și relevanță

Odată ce indexurile erau active, am lucrat cu colaboratorii biroului pentru a rafina interogările. Oracle Text oferă un set de operatori care depășesc simpla căutare booleană [1][2].

`ACCUM` acumulează scorurile în loc să ceară ca toți termenii să fie prezenți — util când se dorește ordonarea după relevanță globală fără a exclude documentele care conțin doar unii dintre termeni:

```sql
-- Documentele cele mai relevante pentru o combinație de termeni
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

`FUZZY` gestionează variațiile ortografice și greșelile de tastare — deosebit de util pe texte scanate cu OCR, unde calitatea recunoașterii nu este uniformă:

```sql
-- Căutare fuzzy pentru a gestiona variante ortografice
SELECT doc_id FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'FUZZY(risarcimanto, 70, 6)', 1) > 0;
```

Parametrul `70` este pragul de similaritate (0-100), `6` numărul maxim de expansiuni. Trebuie calibrat: praguri prea mici produc zgomot, prea mari pierd variantele relevante.

Pentru a prezenta rezultatele utilizatorilor, `CTX_DOC.HIGHLIGHT` returnează textul cu termenii găsiți marcați [1]:

```sql
-- Evidențierea termenilor găsiți în document
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

## Sincronizarea și întreținerea indexurilor

Un aspect adesea subestimat: indexurile Oracle Text nu se actualizează automat în timp real ca un B-tree. Când sunt inserate rânduri noi, indexul trebuie sincronizat explicit [1].

```sql
-- Sincronizare manuală a indexului
EXEC CTX_DDL.SYNC_INDEX('LEGAL_DOC_CTX_IDX', '256M');

-- Optimizare periodică pentru compactarea structurilor interne
EXEC CTX_DDL.OPTIMIZE_INDEX('LEGAL_DOC_CTX_IDX', 'FULL');
```

Pentru un arhiv în producție cu inserări continue, sincronizarea trebuie programată. Un job `DBMS_SCHEDULER` la fiecare 15-30 de minute este un punct de plecare rezonabil; frecvența depinde de volumul inserărilor și de toleranța față de întârzierea indexării. Pentru `LEGAL_ARCHIVE`, unde documentele sunt încărcate în loturi nocturne, o sincronizare post-încărcare era suficientă.

Monitorizarea se face prin `CTX_USER_INDEXES` și `CTX_INDEX_ERRORS`:

```sql
-- Verificarea stării indexurilor Oracle Text
SELECT idx_name, idx_status, idx_docid_count
FROM CTX_USER_INDEXES;

-- Verificarea erorilor de indexare
SELECT err_index_name, err_timestamp, err_text
FROM CTX_INDEX_ERRORS
ORDER BY err_timestamp DESC;
```

## Ușurarea lui Alberto, nu surpriza

Când i-am arătat rezultatele lui Alberto, reacția lui nu a fost uimire. Era ușurare. „În sfârșit", a spus. Nu „incredibil" — *în sfârșit*.

Acel cuvânt spune totul despre abordarea care a funcționat. Nu a existat un moment eroic în care cineva a găsit soluția magică. A existat o conversație în care am încetat să ne uităm la log-uri și am întrebat utilizatorii cum lucrează cu adevărat. Din acea conversație a reieșit că erau necesare trei indexuri diferite pentru trei tipare de căutare diferite, nu un index generic aplicat la tot.

Oracle Text era deja disponibil în instanța 19c. Funcționalitățile erau documentate. Ceea ce lipsea era maparea dintre nevoile reale de căutare și capacitățile instrumentului.

Echipa biroului a contribuit în mod determinant: fără disponibilitatea lor de a descrie fluxurile de lucru reale — nu cele teoretice, cele zilnice — am fi configurat indexuri rezonabile pe hârtie, dar neoptimale pentru acel context specific. Tehnologia este un instrument; înțelegerea problemei este munca adevărată.

Indexurile Oracle Text nu se construiesc pornind de la documentație spre date. Se construiesc pornind de la nevoile celor care caută spre structura datelor, și apoi documentația ajută la găsirea tipului de index și a operatorilor potriviți. În această ordine.

## Fonti ufficiali

1. Oracle Text Reference 19c — [Oracle Text Indextype Reference (CONTEXT, CATSEARCH, CTXXPATH, CONTAINS, CATSEARCH operator, CTX_XPTH.CONTAINS, WORDLIST, STOPLIST, LEXER, CTX_DDL.SYNC_INDEX, CTX_DOC.HIGHLIGHT)](https://docs.oracle.com/en/database/oracle/oracle-database/19/textr/index.html)
2. Oracle Text Application Developer's Guide 19c — [Concepte avansate, tuning și bune practici](https://docs.oracle.com/en/database/oracle/oracle-database/19/texta/toc.htm)
3. Oracle-Base (Tim Hall) — [Oracle Text Articles: exemple practice](https://oracle-base.com/articles/misc/oracle-text)

## Glosar candidat

- **Oracle Text** — Componentă integrată a Oracle Database pentru indexarea și căutarea full-text pe date textuale. Nu necesită licență separată și operează direct pe structurile de date ale bazei de date, inclusiv coloane CLOB, BLOB și VARCHAR2.

- **Indexul CONTEXT** — Tip de index Oracle Text pentru căutarea full-text pe text nestructurat (documente, articole, avize). Construiește o structură inversată token→document care evită scanarea completă a coloanei CLOB la fiecare interogare.

- **Indexul CATSEARCH** — Tip de index Oracle Text optimizat pentru arhive care combină atribute structurate (expeditor, dată, categorie) cu text liber. Predicatele SQL și căutarea textuală sunt rezolvate împreună în interiorul indexului, nu în faze separate.

- **Indexul CTXXPATH** — Tip de index Oracle Text pentru documente XML sau JSON arhivate în CLOB/BLOB. Păstrează structura ierarhică a path-urilor XML în timpul indexării, permițând interogări care limitează căutarea la noduri specifice ale documentului.

- **Lexer** (Oracle Text) — Componentă care analizează textul în faza de indexare, împărțindu-l în tokeni și aplicând reguli de normalizare specifice limbii și formatului. `BASIC_LEXER` cu `BASE_LETTER YES` gestionează, de exemplu, normalizarea accentelor pentru italiană.
