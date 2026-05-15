---
title: "ENUM in MySQL: când îți simplifică viața și când îți complică zilele"
seoTitle: "MySQL ENUM vs CHECK vs lookup: cele trei căi"
description: "MySQL ENUM vs CHECK constraint vs tabelă lookup: trei căi pentru modelarea unei enumerări. Avantaje, limite și caz real de tracking expedieri."
date: "2026-06-03T08:03:00+01:00"
draft: false
translationKey: "enum_mysql_semplifica_o_complica"
tags: ["schema-design"]
categories: ["mysql"]
image: "enum-mysql-semplifica-o-complica.cover.jpg"
---

E o scenă care se repetă în fiecare proiect, mai devreme sau mai târziu. Desenezi o tabelă nouă, trebuie să modelezi o coloană `status` sau `type` sau `category`, și întrebarea apare mereu la fel: "ENUM nativ, CHECK constraint sau tabelă de lookup?". Trei căi, trei filosofii, și trei rezultate foarte diferite în funcție de cum evoluează sistemul.

ENUM este una dintre acele feature-uri care caracterizează MySQL. Puține alte DBMS-uri mainstream au un tip enumerat nativ — PostgreSQL are unul, iar Oracle a ajuns la ceva similar doar cu SQL Domains din 23ai. Ani de zile, în MySQL, alegerea de a folosi ENUM a fost practic automată: câteva linii de DDL, lizibil, performant, fără JOIN. Funcționează. Până când te întorci, șase ani mai târziu, și acel `status` al tabelei a devenit un câmp minat.

---

## Cele trei căi, în două rânduri fiecare

Înainte de a intra în subiect, cele trei opțiuni schematizate. Vom folosi exemplul unei tabele `comenzi` cu un status care ia un set închis de valori.

**ENUM nativ**:

```sql
CREATE TABLE comenzi (
  id     INT PRIMARY KEY,
  status ENUM('NOU','IN_LUCRU','EXPEDIAT','LIVRAT') NOT NULL
);
```

Tipul `ENUM` este un șir cu constrângere: admite doar valorile declarate [1]. Intern MySQL stochează un întreg (1 sau 2 octeți, în funcție de câte valori) care servește ca index în listă. Rezultat: stocare compactă, citire lizibilă.

**CHECK constraint**:

```sql
CREATE TABLE comenzi (
  id     INT PRIMARY KEY,
  status VARCHAR(20) NOT NULL,
  CONSTRAINT chk_status CHECK (status IN ('NOU','IN_LUCRU','EXPEDIAT','LIVRAT'))
);
```

Abordarea SQL standard. Mai verboasă, în schimb mai flexibilă (condițiile CHECK pot fi arbitrare ca și complexitate). Atenție: înainte de MySQL 8.0.16, constrângerile CHECK erau parsate și ignorate în tăcere. Doar de la 8.0.16 sunt aplicate cu adevărat [2].

**Tabelă de lookup cu FK**:

```sql
CREATE TABLE statusuri_comanda (
  cod         VARCHAR(20) PRIMARY KEY,
  eticheta    VARCHAR(100) NOT NULL,
  activ       BOOLEAN DEFAULT TRUE
);

CREATE TABLE comenzi (
  id          INT PRIMARY KEY,
  status_cod  VARCHAR(20) NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_cod) REFERENCES statusuri_comanda(cod)
);
```

Calea "pur-bază-de-date". Mai multe tabele, mai multe JOIN-uri, și în schimb mai multă flexibilitate: poți adăuga atribute (etichete localizate, ordine de afișare, flag-uri activ/inactiv), modifica valorile fără a atinge schema tabelelor copii, și gestiona totul în runtime [3].

---

## Când ENUM este alegerea potrivită

ENUM strălucește într-un context specific: **set de valori stabil, semantică controlată la nivel de schemă**. Când ambele ingrediente sunt prezente, ENUM este alegerea cea mai curată.

Cazuri tipice unde stabilitatea există cu adevărat:

- **Zilele săptămânii** (`'LUN','MAR','MIE','JOI','VIN','SAM','DUM'`) — nu s-au schimbat niciodată și nici nu se vor schimba
- **Statusuri binare sau ternare fixe** (`'ACTIV','INACTIV'` sau `'PUBLIC','PRIVAT','CIORNA'`)
- **Tipuri de tranzacții contabile** unde planul de conturi este reglementat prin lege
- **Polaritate sau semn** în măsurători tehnice

În toate aceste cazuri ENUM îți oferă trei avantaje concrete:

1. **Stocare compactă**: 1-2 octeți pe rând în loc de 4 ai unui INT care servește ca FK. Pe o tabelă cu 200 de milioane de rânduri sunt 400-600 MB economisiți. Nu este motivul principal pentru a alege ENUM; rămâne totuși un bonus
2. **Lizibilitate în query-uri**: `WHERE status = 'EXPEDIAT'` fără JOIN, fără alias-uri suplimentare de tabele. Când trebuie să debughezi la trei dimineața, contează
3. **Fără migrare suplimentară**: "tabela de lookup" este chiar schema în sine. Fără seed de date, fără sincronizare, fără FK de gestionat la deploy

Într-un sistem unde domeniul este cu adevărat închis, ENUM scoate complexitatea. O coloană, o constrângere declarată în CREATE TABLE, gata.

---

## Cazul concret: un sistem de tracking pentru expedieri

Cu ceva timp în urmă lucram cu echipa IT a unui mare operator poștal italian. Era vorba de a desena modelul de date pentru un sistem de tracking al expedierilor: pachete care intră în depozit, se preiau, se sortează, se livrează. `status` era o coloană centrală, prezentă în aproape orice query.

În prima versiune a sistemului, statusurile erau cinci, bine definite de business: `PRIMIT`, `IN_DEPOZIT`, `IN_LIVRARE`, `LIVRAT`, `RESPINS`. ENUM, fără doar și poate, era alegerea potrivită:

```sql
ALTER TABLE expedieri
  ADD COLUMN status ENUM('PRIMIT','IN_DEPOZIT','IN_LIVRARE','LIVRAT','RESPINS') 
  NOT NULL DEFAULT 'PRIMIT';
```

Timp de doi ani în producție a funcționat în liniște. Fără JOIN-uri în listele de livrare, fără tabele de statusuri de menținut, fiecare query cu `WHERE status = '...'` se citea ca o frază în proză. DBA-ul dormea liniștit.

Apoi au început problemele.

---

## Limitele, povestite cu onestitate

Primul semnal a venit ca un email de la product manager: trebuie adăugat un status `REZERVAT`, pentru gestionarea expedierilor anunțate dar încă nereceptionate la depozit. Operațiune aparent banală. Operațiune care necesită asta:

```sql
ALTER TABLE expedieri
  MODIFY COLUMN status 
  ENUM('REZERVAT','PRIMIT','IN_DEPOZIT','IN_LIVRARE','LIVRAT','RESPINS') 
  NOT NULL DEFAULT 'PRIMIT';
```

Pare un singur rând. În realitate, dacă vrei să adaugi `REZERVAT` **înainte** de `PRIMIT` (pentru coerență semantică în secvență), MySQL trebuie să rescrie tabela. Toată [4]. Pe `expedieri` cu o sută cincizeci de milioane de rânduri, în producție, cu `Online DDL` configurat bine [5], sunt totuși câteva ore de încărcare suplimentară pe storage și pe replication lag. A adăuga pur și simplu la final cu `MODIFY COLUMN status ENUM(...,'REZERVAT')` ar fi fost mai ușor — numai că ar fi creat un set de valori cu o ordonare pozițională absurdă: `LIVRAT` vine "înaintea" lui `REZERVAT` în sort? Tehnic da.

Iată-le, limitele lui ENUM, povestite fără milă:

**Case-insensitive**. `'ACTIV'` și `'activ'` sunt aceeași valoare. Pentru cine vine de la PostgreSQL poate fi o surpriză neplăcută. În MySQL este o alegere explicită de design; merită să o știi de la început.

**Ordonare după poziția de declarare**, nu alfabetică. Dacă query-ul face `ORDER BY status`, ordinea este cea în care ai declarat valorile în `CREATE TABLE`. Bug subtil: adaugi `'REZERVAT'` la final pentru a nu reface tabela, și deodată raportul tău ordonat după status arată `'REZERVAT'` după `'RESPINS'`. Nimeni nu se plânge până când cineva observă.

**Modificări grele pe tabele mari**. A adăuga o valoare la final este ușor. A schimba poziția, redenumi o valoare, elimina o valoare — totul cere un rebuild. Cu Online DDL pe MySQL 8 este mai puțin dureros decât în trecut; nu e gratis.

**Lock de tabelă în anumite scenarii**. Combinațiile de operații care necesită `ALGORITHM=COPY` încă există, și pe tabele critice trebuie evaluate cu grijă.

În sistemul de tracking, șase ani mai târziu, fuseseră adăugate douăsprezece statusuri. Fiecare status nou — fiindcă un nou curier, fiindcă un nou canal, fiindcă o nouă politică de retur — era un ALTER nocturn cu DBA-ul în picioare în fața monitorului. ENUM trecuse de la a simplifica viața la a o complica.

---

## Când să treci la CHECK sau la lookup

Întrebarea devine: din ce punct începând conviene să lași ENUM și să iei o altă cale?

Steagurile roșii sunt trei:

1. **Valorile se schimbă des**: dacă în fiecare trimestru business-ul cere să adauge, redenumească sau dezactiveze o valoare, schema n-ar trebui să fie "tabela" enumerărilor. O adevărată tabelă de lookup gestionată dintr-un panou de admin este calea
2. **E nevoie de atribute suplimentare**: descriere localizată în 4 limbi, etichetă scurtă vs lungă, ordine de afișare, flag activ/inactiv. Tot acest lucru nu îl bagi în ENUM. Cu lookup table, fiecare valoare este un rând care poate avea câte coloane vrei
3. **Zeci de valori în creștere**: peste 20-30 de valori, ENUM devine incomod de citit și de întreținut în `CREATE TABLE`. `DDL`-ul devine o listă kilometrică

În aceste cazuri `CHECK` constraint este un compromis intermediar: mai flexibil decât ENUM (redenumirea unei valori este doar un `ALTER CONSTRAINT`), mai puțin structurat decât o adevărată lookup table. Merge pentru seturi de 5-15 valori care se ating din când în când, cu condiția să nu fie nevoie de atribute.

În cazul tracking-ului de expedieri, până la urmă rescrierea s-a îndreptat către lookup table. Merită spus: nu pentru că ENUM era "greșit" în versiunea 1. Era corect, șase ani mai devreme, pentru un domeniu care era cu adevărat mic și stabil. A devenit greșit când domeniul s-a schimbat, și nimeni nu prevăzuse asta. Ceea ce se întâmplă exact în multe proiecte reale.

---

## Lookup table făcută bine

Dacă decizi să mergi în direcția lookup, merită să o desenezi într-un mod care îți permite să crești în timp. Pattern-ul natural — cel pe care îl vedem în sisteme mature — separă două roluri pe care ENUM le ținea amestecate: **identificatorul** valorii și **descrierea** valorii.

```sql
CREATE TABLE statusuri_expediere (
  id           SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  cod          ENUM('PRIMIT','IN_DEPOZIT','IN_LIVRARE','LIVRAT','RESPINS') NOT NULL UNIQUE,
  descriere    VARCHAR(200) NOT NULL,
  ordine       SMALLINT NOT NULL DEFAULT 0,
  activ        BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO statusuri_expediere (cod, descriere, ordine) VALUES
  ('PRIMIT',     'Expediere primită la depozit',     10),
  ('IN_DEPOZIT', 'În așteptarea sortării',           20),
  ('IN_LIVRARE', 'Predată către curier',             30),
  ('LIVRAT',     'Livrată destinatarului',           40),
  ('RESPINS',    'Respinsă de destinatar',           50);

CREATE TABLE expedieri (
  id          INT PRIMARY KEY,
  status_id   SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES statusuri_expediere(id)
);
```

Ai observat surpriza? În lookup, câmpul `cod` este încă un **`ENUM`**. Nu un `VARCHAR(20)`, nu un șir liber. ENUM, același pe care tocmai am terminat să-l criticăm. Și este exact alegerea potrivită: toate contra-urile pe care le-am văzut mai devreme — rebuild-ul la modificare, ordonarea pozițională, efectul pe tabele mari — aici pur și simplu *nu dor*. Lookup-ul are 5, 20, cel mult 50 de rânduri. Un rebuild pe 50 de rânduri este o clipă. Constrângerea "admite doar aceste valori" o plătim la cost zero, fără a scrie un `CHECK` separat.

Trei lucruri interesante reies din această schemă.

**Master-ul poartă doar id-ul**, nu codul. Doi octeți pe rând (`SMALLINT`) în loc de 20+ ai unui `VARCHAR(20)`. Pe o tabelă cu 150 de milioane de rânduri sunt 2-3 GB diferență între date și indexuri, plus JOIN-uri mai rapide datorită comparației pe întreg.

**Codul și descrierea sunt atribute ale lookup-ului, nu cheie**. Asta înseamnă că redenumirea unui status — trecerea de la "Livrat" la "Livrat destinatarului" — este un `UPDATE` pe un singur rând al lookup-ului. Fără migrare, fără rebuild, fără `ALTER` pe master. Schema tabelelor copii nu este atinsă. A avea `cod`-ul drept cheie naturală la începutul proiectului părea elegant; la prima dată când business-ul cere să schimbi textul unei etichete înțelegi de ce existau id-urile surogate.

**Atributele extra costă nimic de adăugat**: o coloană `descriere_scurta` pentru tracciatele SMS, o coloană `ordine` pentru sortarea vizuală în dashboard-uri, o tabelă legată pentru traducerile multilingve. Tot acest lucru nu se putea face cu ENUM "pur", și este normal cu o lookup table bine desenată.

Prețul de plătit este că query-urile ad-hoc cer un JOIN pentru a citi numele status-ului în clar:

```sql
SELECT e.id, se.cod
FROM expedieri e
JOIN statusuri_expediere se ON se.id = e.status_id
WHERE se.cod = 'IN_LIVRARE';
```

Mai verboasă decât un `WHERE status = 'IN_LIVRARE'` pe ENUM — acesta este prețul flexibilității. Și pe rapoartele cele mai frecvente JOIN-ul se optimizează cu un index compus și o `view` care încapsulează complexitatea, lăsând query-urile aplicative lizibile.

### Adăugarea unei valori și reordonarea ENUM-ului

Iată cum se fac cele două operațiuni "delicate" pe acest pattern. Business-ul cere să se adauge statusul `REZERVAT`, pentru expedierile anunțate dar încă neprimite.

**Cazul 1 — adăugare la finalul ENUM-ului, cu `ordine` logică controlată de coloană**:

```sql
-- Extinde ENUM-ul adăugând valoarea la final (operațiune rapidă)
ALTER TABLE statusuri_expediere
  MODIFY COLUMN cod 
    ENUM('PRIMIT','IN_DEPOZIT','IN_LIVRARE','LIVRAT','RESPINS','REZERVAT') NOT NULL;

-- Inserează noul rând; ordinea logică este 5 (înainte de PRIMIT=10)
INSERT INTO statusuri_expediere (cod, descriere, ordine, activ) VALUES
  ('REZERVAT', 'Expediere anunțată, încă neprimită', 5, TRUE);
```

Observă separarea de responsabilități: **ordinea de declarare a ENUM-ului** nu corespunde neapărat cu **ordinea logică** a status-ului în workflow. Aceasta din urmă este gestionată de coloana `ordine`, care este explicită și sortabilă cum vrem. Valoarea numerică internă a ENUM-ului este un detaliu de implementare pe care îl ignorăm.

**Cazul 2 — reordonarea propriu-zisă a ENUM-ului** (dacă într-adevăr vrem ca `REZERVAT` să fie pe prima poziție și intern):

```sql
ALTER TABLE statusuri_expediere
  MODIFY COLUMN cod 
    ENUM('REZERVAT','PRIMIT','IN_DEPOZIT','IN_LIVRARE','LIVRAT','RESPINS') NOT NULL;
```

Pe o tabelă cu 6 rânduri, MySQL face rebuild în milisecunde. `id`-urile rândurilor existente rămân identice (sequence-ul AUTO_INCREMENT nu este atins de rebuild), valoarea ENUM este remapată intern de motor, și integritatea referențială de la master-ul `expedieri` rămâne intactă. Master-ul nu știe nimic despre toate astea: continuă să conțină `status_id = 3` și prin FK rezolvă mereu la rândul corect din lookup.

Acesta este adevăratul punct: **id-urile stabile ale lookup-ului sunt ancora integrității referențiale**. Orice schimbăm în lookup — reorder ENUM, redenumire cod, modificare descriere — master-ul continuă să funcționeze. Cele 150 de milioane de rânduri nu sunt niciodată atinse.

ENUM, în locul ăsta, a redevenit instrumentul potrivit. Același instrument care complica viața pe master este un avantaj pe lookup. Schimbi contextul, schimbi judecata.

---

## Regula de aur

Sinteza pe care o iau cu mine din această poveste, și pe care o repet echipelor când vine întrebarea "ENUM sau lookup?", este simplă:

> Dacă valorile nu se vor schimba niciodată, ENUM este alegerea potrivită. Dacă se vor schimba — chiar și doar "din când în când" — nu lega vocabularul de schemă.

Atât. Provocarea nu este să alegi între cele trei căi. Provocarea este să înțelegi, în momentul alegerii, în care dintre cele două lumi te afli cu adevărat. Și asta o înțelegi doar uitându-te la cum s-a schimbat domeniul în ultimii doi sau trei ani — nu citind cerințele următorului sprint.

---

## Mini-seria cross-DB

Acesta este primul din patru articole despre enumerări în diversele DBMS-uri. Întrebarea "ENUM sau lookup?" nu privește doar MySQL — fiecare bază de date are filosofia ei, și este interesant să vezi cum aceeași alegere își schimbă forma trecând dintr-o lume în alta.

Următoarele apariții:

- **PostgreSQL** — `CREATE TYPE ... AS ENUM`, `ALTER TYPE ADD VALUE`, și surpriza: în PostgreSQL ENUM este *case-sensitive*
- **Oracle** — `CHECK` constraint, SQL Domains din 23ai, și de ce Oracle a ajuns "târziu" la acest subiect
- **Oracle, deep-dive vertical** — cum se modelau enumerările în 19c, ce se schimbă în 21c, 23ai și 26ai, până la noile Assertions

Aceeași întrebare, trei filosofii. Frumusețea este chiar în comparație.

------------------------------------------------------------------------

## Surse oficiale

1. MySQL 8.0 Reference Manual — [The ENUM Type](https://dev.mysql.com/doc/refman/8.0/en/enum.html)
2. MySQL 8.0 Reference Manual — [CHECK Constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
3. MySQL 8.0 Reference Manual — [FOREIGN KEY Constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html)
4. MySQL 8.0 Reference Manual — [`ALTER TABLE` Statement](https://dev.mysql.com/doc/refman/8.0/en/alter-table.html)
5. MySQL 8.0 Reference Manual — [Online DDL Operations (INSTANT / INPLACE / COPY)](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)

------------------------------------------------------------------------

## Glosar

**[ENUM (MySQL)](/ro/glossary/mysql-enum/)** — Tip de date MySQL care admite un set predefinit de valori șir, stocat intern ca index numeric de 1-2 octeți. Una dintre feature-urile caracteristice MySQL.

**[CHECK constraint](/ro/glossary/check-constraint/)** — Constrângere SQL standard care limitează valorile admise într-o coloană printr-o expresie booleană. În MySQL este aplicată cu adevărat doar de la versiunea 8.0.16.

**[Lookup table](/ro/glossary/lookup-table/)** — Tabelă de referință conectată prin foreign key care stochează valorile valide ale unei enumerări, cu eventuale atribute descriptive (etichetă, ordine, flag activ).

**[Online DDL](/ro/glossary/mysql-online-ddl/)** — Mecanism MySQL/InnoDB care permite executarea ALTER TABLE fără a bloca scrierile concurente, cu trei algoritmi (`INSTANT`, `INPLACE`, `COPY`) aleși automat în funcție de operațiune.

**[Cheie surogat](/ro/glossary/chiave-surrogata/)** — Identificator numeric generat de baza de date (de obicei un `AUTO_INCREMENT`) distinct de cheia naturală. Pe lookup table este ancora integrității referențiale, deoarece rămâne stabil chiar și când codul sau descrierea se schimbă.
