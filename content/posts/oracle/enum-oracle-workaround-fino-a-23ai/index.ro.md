---
title: "Enumerări în Oracle: douăzeci de ani de workaround, și drumul care s-a deschis cu 23ai"
seoTitle: "Oracle SQL Domains 23ai: enum, CHECK și lookup tables"
description: "Oracle nu a avut niciodată ENUM nativ. CHECK constraints, lookup tables și SQL Domains 23ai: trei drumuri, un caz real banking, și ce va veni cu 26ai."
date: "2026-06-16T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_workaround_fino_a_23ai"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-workaround-fino-a-23ai.cover.jpg"
---

Întrebarea este aceeași pe care ne-am pus-o [pentru MySQL](/ro/posts/mysql/enum-mysql-semplifica-o-complica/) și apoi [pentru PostgreSQL](/ro/posts/postgresql/enum-postgresql-paga-o-pesa/): o coloană `status` sau `type` cu un set închis de valori, și trei drumuri în față. Se schimbă baza de date, se schimbă filozofia, și se schimbă și **ce pune la dispoziție baza de date**. Pe Oracle, până nu demult, lipsea tocmai prima opțiune a celorlalte două părți — tipul ENUM nativ. Timp de douăzeci de ani, modelarea unei enumerări în Oracle a fost un exercițiu de workaround: două drumuri practicabile și un al treilea care nu a fost niciodată cu adevărat o enumerare.

Cu 23ai a venit un răspuns structural: **SQL Domains** [1]. Merită să intrăm în detaliu, pentru că Oracle a ajuns ultimul dar a ajuns bine — iar între timp cultura "lookup table" care s-a format pe teren nu și-a pierdut locul.

---

## Cele trei drumuri, în două rânduri fiecare

Vom folosi exemplul unui tabel `tranzactii` cu un status care ia un set închis de valori. Sector banking — terenul clasic al Oracle în Italia, unde un plan de conturi și o taxonomie de stări sunt reglementate, auditate, rareori improvizate.

**CHECK constraint**:

```sql
CREATE TABLE tranzactii (
  id      NUMBER PRIMARY KEY,
  suma    NUMBER(15,2) NOT NULL,
  stare   VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_stare CHECK (stare IN
    ('IN_ASTEPTARE','AUTORIZATA','COMPLETATA','STORNATA','RESPINSA'))
);
```

Abordare SQL standard. Oracle aplică `CHECK` constraint de zeci de ani — nicio surpriză privind validitatea constrângerii cum se întâmpla în MySQL înainte de 8.0.16. Simplu, citibil, și pentru proiecte mici rezolvă imediat. Prețul, pe un sistem real, se descoperă mai târziu: aceeași listă de valori este replicată pe fiecare tabel care are aceeași coloană `stare`, și fiecare modificare devine un `ALTER TABLE` per tabel. Vom vedea de ce contează.

**Lookup table cu foreign key**:

```sql
CREATE TABLE stari_tranzactie (
  cod        VARCHAR2(20) PRIMARY KEY,
  eticheta   VARCHAR2(100) NOT NULL,
  ordine     NUMBER,
  activ      CHAR(1) DEFAULT 'Y' CHECK (activ IN ('Y','N'))
);

CREATE TABLE tranzactii (
  id          NUMBER PRIMARY KEY,
  suma        NUMBER(15,2) NOT NULL,
  stare_cod   VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_stare
    FOREIGN KEY (stare_cod) REFERENCES stari_tranzactie(cod)
);
```

Drumul "database pur" și — nu întâmplător — alegerea culturală dominantă în proiectele Oracle enterprise. Un tabel în plus, un JOIN în plus, și în schimb o enumerare care este **un obiect al bazei de date cu viață proprie**: poți atașa etichete localizate, ordine de display, flag activ/inactiv, audit trail pe `MODIFY`-ul taxonomiei, și reguli de business mai bogate decât un simplu "admis/neadmis". Pe sistemele pe care le-am văzut în banking, telco și administrația publică italiană în ultimii douăzeci de ani, **de opt ori din zece alegerea a fost aceasta** — și cu temei.

**Pseudo-pattern (SUBTYPE, COLLECTION, type-object)**:

```sql
-- Descurajat ca "enumerare" pentru o coloană persistentă:
CREATE OR REPLACE TYPE stare_tranzactie_t AS OBJECT (
  cod VARCHAR2(20)
);
/
```

`TYPE`-urile Oracle (SUBTYPE PL/SQL, COLLECTION SQL, type-object) sunt puternice, dar **nu sunt ENUM-uri**. Nu dau o validare nativă pe valorile persistate, nu au un mecanism de lookup citibil prin SQL pur, și dicționarul de date nu le vede ca "taxonomie". Sunt un instrument de abstractizare la nivel aplicativ, nu un mecanism de constrângere. Cine le-a folosit pentru a simula ENUM-uri în general a regretat când primul raport de business a cerut să știe "câte stări active sunt" — și din tabel nu se puteau extrage fără o interogare PL/SQL.

---

## Ce se schimbă față de MySQL și PostgreSQL

Dacă vii din cele două părți anterioare ale miniseriei, trei lucruri ar fi bine să le ții în buzunar înainte de a scrie primul `CREATE TABLE` pe Oracle.

**Niciun tip ENUM nativ**. Pe MySQL ai `ENUM('A','B','C')` ca tip de coloană; pe PostgreSQL ai `CREATE TYPE ... AS ENUM` ca obiect de sine stătător. Pe Oracle, până la 23ai, aceste două opțiuni pur și simplu nu existau. Rămâneau `CHECK` și lookup tables.

**`CHECK` este aplicat în întregime dintotdeauna**. Spre deosebire de MySQL pre-8.0.16 (unde `CHECK`-urile erau parsate și silențios ignorate [2]), Oracle validează constrângerile `CHECK` de dinainte de mileniu. Un detaliu istoric dar relevant: dacă vii din MySQL, aici nu există nicio îndoială asupra eficacității lor.

**Cultură a lookup table înrădăcinată**. Comunitatea Oracle, prin tipul de clienți care o folosesc (banking, asigurări, administrația publică, telco), a preferat întotdeauna lookup table în detrimentul `CHECK`. Nu din dogmă, ci pentru că în acele contexte evoluția setului de valori este frecventă, auditul este obligatoriu, localizarea etichetelor este un standard. Lookup table este o sală de gimnastică a flexibilității — `CHECK`-ul este o promisiune de rigiditate.

---

## Când `CHECK`-ul este suficient

Rămânând în interiorul pattern-ului celorlalte două părți, cazurile în care `CHECK` pe Oracle este cu adevărat alegerea corectă sunt puține și precise:

- **Seturi de valori care nu se vor schimba niciodată**. Polaritatea unei măsurători (`'POS','NEG','ZERO'`), zilele săptămânii, lunile anului, polaritatea contabilă (`'DEBIT','CREDIT'`)
- **Tabele cu o singură referință la set**. Dacă coloana există într-**un** singur tabel, prețul `ALTER TABLE`-ului pentru a adăuga o valoare este marginal
- **Proiecte mici sau monolitice**, unde domeniul valorii este clar în cod și nu trebuie expus ca "configurație" interfețelor utilizatorilor

În afara acestor trei scenarii, după experiența mea, `CHECK`-ul îmbătrânește prost. Văd apărând același pattern în faza de evoluție: businessul cere să se adauge o valoare nouă — să zicem `'AUTORIZARE_MANUALA'` pentru tranzacțiile care necesită intervenție manuală — și îți dai seama că șirul este replicat în 14 tabele. Paisprezece `ALTER TABLE`-uri, paisprezece teste de regresie, paisprezece release note. Lookup table ar fi necesitat un `INSERT`.

---

## Cultura lookup table în Oracle (și de ce există un motiv)

Pe un proiect banking de ceva vreme — o platformă de plăți, Oracle 19c, în jur de 1.200 de tabele în schema aplicativă, echipă distribuită Italia/România — taxonomia stărilor de tranzacție fusese modelată cu două tabele:

- `stari_tranzactie` (cod, eticheta_it, eticheta_en, ordine, activ, grup)
- `stari_tranzactie_audit` (trigger de MODIFY care păstra istoricul cui ce a schimbat)

Niciun `CHECK`. O singură FK la `stari_tranzactie.cod` pe fiecare coloană de stare — `tranzactii.stare_cod`, `tranzactii_istoric.stare_cod`, `miscari.stare_cod`, și o duzină de alte tabele din modulul de reconciliere.

Părea suprainginerie, până în ziua în care compliance-ul a cerut să poată "**îngheța**" temporar o stare (de exemplu `'STORNATA'`) în timpul unui audit, fără a o elimina din schemă — niciun rând nou cu acea valoare, dar rândurile istorice trebuiau să rămână citibile și interogabile. Cu lookup table a fost un `UPDATE stari_tranzactie SET activ = 'N' WHERE cod = 'STORNATA'` plus câteva check aplicative. **Trei rânduri de cod**. Dacă am fi avut `CHECK` cu lista de șiruri inlined în 18 tabele, ar fi fost o săptămână de muncă între DDL, regression test și fereastră de deploy.

Nu este povestea unui erou — este povestea unei alegeri arhitecturale făcute cu cinci ani înainte de echipa de design, și a unui compliance care a găsit schema gata pentru întrebarea pe care a pus-o. Cultura lookup table în Oracle a crescut din sute de episoade ca acesta.

---

## Sosirea SQL Domains în 23ai

Cu Oracle Database 23ai (lansată pe engineered system în aprilie 2024 și apoi în disponibilitate mai amplă) ajunge un construct care lipsea: **SQL Domain** [1]. Este pentru prima dată când Oracle dă un răspuns structural problemei "centralizarea domeniului unei coloane ca obiect al bazei de date".

```sql
CREATE DOMAIN stare_tranzactie AS VARCHAR2(20)
  CONSTRAINT chk_stare_tranzactie CHECK (VALUE IN
    ('IN_ASTEPTARE','AUTORIZATA','COMPLETATA','STORNATA','RESPINSA'))
  DEFAULT 'IN_ASTEPTARE'
  ANNOTATIONS (display 'Stare Tranzacție',
               description 'Starea ciclului de viață al unei tranzacții');

CREATE TABLE tranzactii (
  id     NUMBER PRIMARY KEY,
  suma   NUMBER(15,2) NOT NULL,
  stare  stare_tranzactie NOT NULL
);
```

`DOMAIN`-ul este un obiect al dicționarului de date (vizibil în `DBA_DOMAINS`), reutilizabil pe orice coloană, și aduce cu el tot pachetul: tipul de bază, constrângerea `CHECK`, un `DEFAULT`, și — caracteristică originală Oracle, neprezentă în `DOMAIN`-ul PostgreSQL — un sistem de **annotations** care pot fi citite de instrumentele BI, de raportare și de UI generation pentru a deriva etichete de display, descrieri, ordering, etc.

Punctul forte nu este sintaxa — este **ALTER DOMAIN**.

---

## `ALTER DOMAIN`: superputerea care lipsea

```sql
ALTER DOMAIN stare_tranzactie
  CONSTRAINT chk_stare_tranzactie CHECK (VALUE IN
    ('IN_ASTEPTARE','AUTORIZATA','COMPLETATA','STORNATA','RESPINSA',
     'AUTORIZARE_MANUALA'));
```

Acel singur statement actualizează constrângerea **pentru toate coloanele care folosesc `stare_tranzactie`** — în 18 tabele, în 50, nu contează. Oracle se ocupă să propage check-ul, și să valideze rândurile existente (cu `VALIDATE` sau `NOVALIDATE`, în funcție de cum preferi să gestionezi tranziția).

Este ceea ce lookup table dădea deja la nivel logic (un singur loc unde să schimbi valorile admise), acum dus la nivelul **catalogului de schemă**, fără a necesita un JOIN, fără a necesita un tabel în plus, și fără cei 4 octeți de OID ai unei FK numerice.

Pentru cine a lucrat douăzeci de ani cu Oracle, este una din acele feature care te fac să spui: "**în sfârșit**". Nu pentru că lookup table și-ar fi pierdut locul — domeniul nu înlocuiește lookup-ul când sunt necesare etichete localizate, ordering de display dinamic sau audit trail. Îl înlocuiește când erau necesare **doar** validare și default centralizate. Și acele cazuri sunt multe.

---

## Când să alegi ce, astăzi

Un ghid operativ, sintetic:

| Caz | Drum recomandat |
|-----|--------------------|
| Set fix, 1 tabel, domeniul valorii cunoscut și imuabil | `CHECK` constraint inline |
| Set fix, **mai multe** tabele, pe Oracle pre-23ai | Lookup table cu FK |
| Set fix, mai multe tabele, **pe Oracle 23ai+** | `SQL DOMAIN` |
| Set evolutiv + etichete localizate + ordering dinamic + audit | Lookup table cu FK (și pe 23ai+) |
| Validare cross-tabel (ex. suma de stări = N) | Trigger azi, `ASSERTION` (26ai, în curând) mâine |

Lookup table **nu a murit** odată cu SQL Domains. A rămas alegerea corectă când enumerarea este o **entitate de business** — cu atributele ei, cu evoluția ei, cu guvernanța ei. SQL Domain este complementul ideal când enumerarea este o **constrângere de schemă** — un domeniu pur, fără atribute, reutilizat pe multe coloane.

---

## Ce va veni cu 26ai: Assertions

Oracle 26ai (anunțată ca următoarea major release) aduce — printre altele — suportul formal pentru **`ASSERTION`** [3]: un construct SQL standard, prezent pe hârtie de zeci de ani și niciodată cu adevărat implementat de niciun DBMS mainstream, care permite exprimarea constrângerilor **cross-tabel**. Constrângeri pe care astăzi trebuie să le codifici ca trigger sau ca check aplicativ, cu toate riscurile aferente (trigger uitate, tranzacții care ocolesc constrângerea, race condition cu isolation level relaxat).

Exemplu posibil:

```sql
CREATE ASSERTION cel_putin_unul_activ CHECK (
  (SELECT COUNT(*) FROM stari_tranzactie WHERE activ = 'Y') >= 1
);
```

Ideea este ca motorul bazei de date să garanteze această constrângere **la nivel tranzacțional** — fără trigger, fără cod aplicativ, validare centralizată. Pentru enumerările gestionate cu lookup table, `ASSERTION` deschid un scenariu nou: integritatea întregii taxonomii (nu doar a coloanei individuale) devine exprimabilă în DDL.

Este material pe care îl vom dezvolta când 26ai va fi disponibilă în test, pe workload-uri reale. Pentru moment, merită să o știm pe drum și să ne pregătim — designul unei taxonomii de stări astăzi poate deja să țină cont de unde constrângerile cross-tabel vor trăi mai bine mâine.

---

## Întrebarea pe care o iau cu mine din miniserie

Trei baze de date, trei filozofii, trei drumuri — și o întrebare care rămâne valabilă pretutindeni: **cât de stabil este setul tău de valori?**

- Dacă este cu adevărat stabil și local → `CHECK` (și pe Oracle 23ai+ → `DOMAIN`).
- Dacă are atribute proprii și o guvernanță → lookup table, pe orice DB.
- Dacă este o evoluție frecventă de valori "nomenclator" → lookup table, întotdeauna.

Restul sunt detalii de sintaxă și de motor. Ce contează — și ce am învățat în trei decenii de schema design, pe clienți care mergeau de la compania de asigurări multi-țară la banca comercială italiană — este că **rigiditatea unei scheme se plătește la evoluție, și flexibilitatea se plătește la integritate**. Alegerea este întotdeauna unde vrei să plătești prețul. Oracle 23ai, în sfârșit, îți dă un alt punct unde să-l plătești — mai convenabil, în multe cazuri, decât înainte.

---

## Surse oficiale

1. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
2. MySQL 8.0 Reference Manual — [CHECK Constraints (8.0.16+)](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
3. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glosar

- **[SQL Domain](/ro/glossary/oracle-sql-domain/)** — Construct introdus în Oracle 23ai care permite definirea unui tip de bază + constrângeri + default + annotations ca obiect al dicționarului de date, reutilizabil pe multe coloane. Echivalentul conceptual al `DOMAIN`-ului PostgreSQL, dar mai bogat în feature de metadate.
- **[CHECK constraint](/ro/glossary/check-constraint/)** — Constrângere SQL care limitează valorile admisibile într-o coloană sau un rând printr-o condiție booleană. Validată de motorul bazei de date în momentul INSERT sau UPDATE.
- **[Lookup table](/ro/glossary/lookup-table/)** — Tabel auxiliar care conține setul de valori admise pentru o coloană de tipologie, referențiat prin foreign key din tabelele "principale". Permite evoluția runtime a setului de valori fără modificări la schemă.
- **[ALTER DOMAIN](/ro/glossary/oracle-alter-domain/)** — Comandă Oracle 23ai+ care modifică constrângerea unui `SQL DOMAIN` propagând schimbarea la toate coloanele care folosesc domeniul. Înlocuiește multiple `ALTER TABLE` cu o singură operație.
- **[ASSERTION](/ro/glossary/sql-assertion/)** — Construct SQL standard (încă neimplementat de aproape niciun DBMS mainstream) pentru exprimarea constrângerilor cross-tabel validate la nivel tranzacțional. Anunțat în Oracle 26ai.
