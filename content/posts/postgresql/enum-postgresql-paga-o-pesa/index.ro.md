---
title: "ENUM în PostgreSQL: când alegerea merită, și când te costă scump"
seoTitle: "PostgreSQL ENUM vs CHECK vs lookup: alegerea corectă"
description: "PostgreSQL ENUM vs CHECK vs tabel lookup: ALTER TYPE ADD VALUE nu costă nimic, eliminarea unei valori costă o migrare. Trei drumuri, un caz telco real."
date: "2026-06-09T08:03:00+01:00"
draft: false
translationKey: "enum_postgresql_paga_o_pesa"
tags: ["enum", "data-modeling", "schema-design", "alter-type", "check-constraint"]
categories: ["postgresql"]
image: "enum-postgresql-paga-o-pesa.cover.jpg"
---

Întrebarea este aceeași pe care ne-am pus-o [pentru MySQL](/ro/posts/mysql/enum-mysql-semplifica-o-complica/): o coloană `status` sau `type` cu un set închis de valori, și trei drumuri în față — tip enumerativ nativ, CHECK constraint, tabel de lookup. Se schimbă baza de date, se schimbă filozofia, și se schimbă și locul unde cade prețul.

PostgreSQL are propriul său ENUM, declarat ca tip de sine stătător cu `CREATE TYPE ... AS ENUM` [1] [2]. Este gândit diferit față de cel al MySQL: type-safe ca un domain, tranzacțional ca tot restul DDL-ului, și cu un detaliu care îi pune piedică aproape tuturor la primul pas — este **case-sensitive**. Pentru cine vine de la MySQL este incomod, pentru cine a lucrat mereu cu PostgreSQL este firesc.

Merită să intrăm în detaliu, pentru că PostgreSQL ENUM nu este "MySQL ENUM cu altă sintaxă". Este altceva. Trebuie înțeles pentru ceea ce este.

---

## Cele trei drumuri, în două rânduri fiecare

Vom folosi exemplul unui tabel `abonamente` cu o stare care ia un set închis de valori.

**ENUM nativ**:

```sql
CREATE TYPE stare_abonament AS ENUM (
  'ACTIV','SUSPENDAT','TERMINAT','EXPIRAT'
);

CREATE TABLE abonamente (
  id      BIGINT PRIMARY KEY,
  stare   stare_abonament NOT NULL
);
```

În PostgreSQL tipul este un **obiect de primă clasă**: îl creezi o dată, îl refolosești pe multe coloane, îl modifici cu `ALTER TYPE`. Intern coloana ocupă 4 octeți (un `OID` intern), valoarea este validată de motor, și citirea returnează șirul original (case-sensitive).

**CHECK constraint**:

```sql
CREATE TABLE abonamente (
  id      BIGINT PRIMARY KEY,
  stare   VARCHAR(20) NOT NULL,
  CONSTRAINT chk_stare 
    CHECK (stare IN ('ACTIV','SUSPENDAT','TERMINAT','EXPIRAT'))
);
```

Abordare SQL standard. Mai verbos, în schimb mai flexibil (condițiile de `CHECK` pot fi arbitrar de complexe). În PostgreSQL `CHECK` constraint-urile sunt pe deplin aplicate dintotdeauna [3] — fără "ignorate în tăcere" cum se întâmpla în MySQL înainte de 8.0.16.

**Tabel de lookup cu FK**:

```sql
CREATE TABLE stari_abonament (
  cod         VARCHAR(20) PRIMARY KEY,
  eticheta    VARCHAR(100) NOT NULL,
  activ       BOOLEAN DEFAULT TRUE
);

CREATE TABLE abonamente (
  id          BIGINT PRIMARY KEY,
  stare_cod   VARCHAR(20) NOT NULL,
  CONSTRAINT fk_stare 
    FOREIGN KEY (stare_cod) REFERENCES stari_abonament(cod)
);
```

Calea "bază-de-date-pură". Mai multe tabele, mai multe JOIN, și în schimb mai multă flexibilitate: atribute suplimentare, etichete localizate, ordine de afișare, activare/dezactivare în timpul rulării [4].

---

## Ce se schimbă față de MySQL: trei lucruri, înainte de a începe

Dacă vii de la MySQL, sunt trei detalii pe care merită să le ai în buzunar înainte de a scrie primul `CREATE TYPE`.

**Case-sensitive**. `'ACTIV'` și `'activ'` sunt două valori diferite. În MySQL erau aceeași valoare — o decizie de design care unora le părea "comodă" și altora "alunecoasă". PostgreSQL ia calea opusă: dacă ai declarat `'ACTIV'`, va trebui mereu să scrii `'ACTIV'`. Interogările nenormalizate vor eșua cu *invalid input value*. Este rigurozitate, și odată ce te obișnuiești o apreciezi; prima zi este o surpriză care costă câteva minute.

**Type safety reală, nu simulată**. ENUM este un tip, nu o restricție pe un `VARCHAR`. Poți crea o funcție care acceptă `stare_abonament` ca parametru, și motorul va respinge la parse-time orice apel cu un șir liber. La fel pentru proceduri, view-uri, indecși parțiali. În MySQL această siguranță nu există — `ENUM` este o coloană `VARCHAR` decorată.

**ALTER TYPE este aproape gratis (și tranzacțional)**. Adăugarea unei valori la coada unui ENUM PostgreSQL este o operație de metadata [5]. Nici rebuild al tabelului, nici lock de scriere prelungit. Și ca tot DDL-ul PostgreSQL, este în interiorul tranzacției: dacă commit-ul eșuează, ENUM rămâne așa cum era. Aceasta este diferența cea mai tangibilă față de MySQL, unde `MODIFY COLUMN ENUM(...)` pe un tabel mare te poate ține treaz o noapte întreagă.

---

## Când ENUM este alegerea corectă în PostgreSQL

Același principiu ca în MySQL, aplicat contextului PostgreSQL: **set de valori stabil, semantică controlată prin schemă**. Când aceste două ingrediente sunt prezente, ENUM în PostgreSQL are chiar și niște avantaje în plus față de vărul MySQL:

1. **Type safety end-to-end**: ENUM este un tip care traversează funcții, proceduri, foreign data wrappers. Nu este doar o restricție pe o coloană, este o garanție de coerență pe care PostgreSQL o aplică pe tot stack-ul de cod SQL
2. **Stocare compactă**: 4 octeți per rând (la fel ca un `INT` care face de FK), comparabil cu MySQL. Pe tabele de sute de milioane de rânduri nu este driver-ul principal; rămâne totuși coerent
3. **ALTER TYPE ADD VALUE economic**: modificarea cea mai frecventă — adăugarea unei valori noi — costă practic zero
4. **DDL tranzacțional**: adăugarea unei valori într-o tranzacție care include și deploy-ul codului aplicativ este o garanție de atomicitate pe care puține alte DBMS-uri ți-o oferă

Într-un sistem unde domeniul este cu adevărat închis și bine definit, ENUM în PostgreSQL elimină complexitatea și adaugă siguranță. Un `CREATE TYPE`, o coloană, gata.

---

## Cazul concret: stări de abonament la un operator mobil

Ne-am trezit, cu câteva proiecte în urmă, să proiectăm modelul de date pentru gestionarea abonamentelor la un operator mobil european. Stack PostgreSQL, milioane de SIM-uri active, un tabel `abonamente` cu o `stare` citită practic de fiecare interogare a billing-ului.

În prima versiune stările erau patru, bine definite de business: `ACTIV`, `SUSPENDAT`, `TERMINAT`, `EXPIRAT`. ENUM era alegerea naturală:

```sql
CREATE TYPE stare_abonament AS ENUM (
  'ACTIV','SUSPENDAT','TERMINAT','EXPIRAT'
);

ALTER TABLE abonamente
  ADD COLUMN stare stare_abonament NOT NULL DEFAULT 'ACTIV';
```

Timp de un an și jumătate a funcționat în tăcere. Type-safe, lizibil, performant. Niciun tabel de lookup de seedat, nicio FK de menținut la deploy. Nimeni nu mai ținea minte de el — și acesta este cel mai bun compliment care se poate face unei scheme.

Apoi, cum este firesc, produsul a crescut.

Prima chemare a venit de la echipa antifraudă: era nevoie să se distingă între `SUSPENDAT_NEPLATA` și `SUSPENDAT_VOLUNTAR`. Operație ușoară în PostgreSQL — aici se vede diferența cu MySQL:

```sql
ALTER TYPE stare_abonament ADD VALUE 'SUSPENDAT_NEPLATA' AFTER 'SUSPENDAT';
ALTER TYPE stare_abonament ADD VALUE 'SUSPENDAT_VOLUNTAR' AFTER 'SUSPENDAT_NEPLATA';
```

Două `ALTER TYPE` de metadata. Milisecunde. Nici rebuild, nici blocaje semnificative pe un tabel `abonamente` cu zeci de milioane de rânduri. Aceeași operație în MySQL, îmi amintesc, ar fi cerut un `MODIFY COLUMN ENUM(...)` cu tot tabelul rescris în Online DDL, și un DBA în picioare în fața monitorului.

Un punct în favoarea PostgreSQL. Real.

Apoi, peste câteva trimestre, au apărut problemele.

---

## Limitele, povești din experiență

Limitele PostgreSQL ENUM există. Nu sunt mai rele decât cele ale MySQL — sunt **diferite**, și se manifestă în puncte diferite ale ciclului de viață.

**Nu se elimină o valoare în mod nativ**. Pare un detaliu; este limitarea cea mai mare. Dacă business-ul decide să "retragă" starea `EXPIRAT` (pentru că de exemplu în noul model comercial este absorbită de `TERMINAT`), în PostgreSQL nu ai un `ALTER TYPE DROP VALUE`. Trebuie să:

1. Creezi un tip nou cu valorile reduse
2. Actualizezi toate rândurile tabelului pentru a le migra la noul set
3. Schimbi tipul coloanei (`ALTER COLUMN ... TYPE`)
4. Dropezi tipul vechi

Toate acestea, pe un tabel mare, sunt exact migrarea grea pe care în MySQL ai fi plătit-o pentru a **adăuga** o valoare — aici o plătești pentru a **scoate** una. Simetria este simpatică doar pe hârtie: în producție, rămâne tot multă încărcare.

**Redenumirea unei valori este ușoară, deși tranzacțională**. `ALTER TYPE ... RENAME VALUE 'X' TO 'Y'` există din PostgreSQL 10. Operație rapidă și curată. Există însă o subtilitate: ALTER TYPE este în interiorul tranzacției, da, și dacă redenumirea are loc într-o tranzacție pe care alte sesiuni au deschisă pe acel tip, poți întâlni lock-uri. Pe sisteme cu concurență mare nu este atât de banal cât pare.

**Ordonare pe poziție**. Ca și în MySQL, ordinea în care ai declarat valorile contează pentru `ORDER BY`. Dacă ai adăugat `SUSPENDAT_NEPLATA` `AFTER 'SUSPENDAT'`, ordinea este coerentă. Dar dacă uiți și faci `ALTER TYPE ... ADD VALUE 'NOU'` fără să specifici poziția, valoarea merge la coadă. Sort-ul dashboard-urilor te poate surprinde.

**Indecșii GIN/GiST nu îl tratează ca șir**. Avantaj sau dezavantaj în funcție de cazul de utilizare; dacă te-ai gândit să faci deasupra o full text search, amintește-ți că ENUM nu este `text`. Trebuie cast-at, și cast-ul împiedică uneori folosirea indexului.

În sistemul abonamentelor, după doi ani stările deveniseră unsprezece, și o cerere de "curățare" a domeniului (să se elimine trei, să se redenumească două) a transformat o aparentă "modificare banală" într-o migrare de un weekend, cu dump-restore parțial al unor tabele satelit care foloseau tipul. Prețul venise — doar într-un alt punct al ciclului de viață față de MySQL.

---

## Când să treci la CHECK sau la lookup

Steagurile roșii sunt aceleași ca în MySQL — baza de date se schimbă, logica proiectului nu:

1. **Valorile se schimbă des** — nu doar se adaugă, ci sunt redenumite sau retrase. Dacă vocabularul este în evoluție activă, schema nu este locul potrivit să-l țină
2. **Sunt necesare atribute suplimentare** — descrieri multilingve, etichetă scurtă/extinsă, ordine de afișare, flag activ. ENUM nu le găzduiește
3. **Zeci de valori în creștere** — peste 20-30, `CREATE TYPE` devine o listă kilometrică incomodă de citit

`CHECK` constraint în PostgreSQL este un compromis intermediar curat: mai ușor de modificat decât un ENUM (e de ajuns un `ALTER TABLE ... DROP CONSTRAINT ... ADD CONSTRAINT ...`), mai puțin structurat decât un lookup adevărat. Merge pentru seturi de 5-15 valori care se ating din când în când.

În cazul abonamentelor, primul val de evoluție (4 → 11 stări) l-am digerat cu `ALTER TYPE ADD VALUE`. Al doilea val — cel care cerea eliminări și redenumiri multiple — a fost ocazia pentru rescrierea către un tabel lookup. Nu pentru că ENUM ar fi fost "greșit" de la început. Era corect pentru un domeniu mic și stabil, și a devenit incomod când domeniul a încetat să fie stabil.

---

## Tabel lookup făcut bine, cu un ENUM înăuntru

Și aici tiparul este analog cu cel pe care l-am văzut pentru MySQL, și — surpriză până la un anumit punct — un ENUM în interiorul tabelului lookup are sens și în PostgreSQL.

```sql
CREATE TYPE cod_stare_abonament AS ENUM (
  'ACTIV','SUSPENDAT','TERMINAT','EXPIRAT'
);

CREATE TABLE stari_abonament (
  id          SMALLSERIAL PRIMARY KEY,
  cod         cod_stare_abonament NOT NULL UNIQUE,
  descriere   TEXT NOT NULL,
  ordine      SMALLINT NOT NULL DEFAULT 0,
  activ       BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO stari_abonament (cod, descriere, ordine) VALUES
  ('ACTIV',     'Abonament activ și funcțional',         10),
  ('SUSPENDAT', 'Suspendat, poate fi reactivat',         20),
  ('TERMINAT',  'Reziliat de client',                    30),
  ('EXPIRAT',   'Expirare naturală a contractului',      40);

CREATE TABLE abonamente (
  id        BIGINT PRIMARY KEY,
  stare_id  SMALLINT NOT NULL,
  CONSTRAINT fk_stare 
    FOREIGN KEY (stare_id) REFERENCES stari_abonament(id)
);
```

Cele trei avantaje sunt aceleași pe care le-am văzut în MySQL:

**Master-ul poartă doar id-ul**, nu codul. Doi octeți (`SMALLINT`) în loc de cei 4 ai OID-ului ENUM-ului direct — pe tabele cu sute de milioane de rânduri sunt GB economisiți.

**Codul și descrierea sunt atribute ale lookup-ului, nu cheie**. Redenumirea descrierii unei stări — trecerea de la "Suspendat, poate fi reactivat" la "Suspensie temporară, poate fi reactivat" — este un `UPDATE` pe un singur rând. Niciun ALTER TYPE, nicio migrare pe master.

**Atributele extra nu costă nimic**: un câmp pentru descrierea scurtă, un tabel legat pentru traduceri, un flag `valid_de_la/valid_pana_la` pentru a gestiona stări valide doar în anumite perioade. Toate acestea, cu ENUM "pur" pe master, erau inaccesibile.

Și pe ENUM-ul intern lookup-ului, **toate limitele pe care le-am enumerat înainte devin irelevante**: tabelul `stari_abonament` are 11 rânduri, un rebuild pe 11 rânduri este invizibil, o migrare este banală. Restricția "admite doar aceste valori" o plătim la cost zero, fără să scriem un `CHECK` separat.

### Adăugarea și retragerea de valori pe tiparul lookup

Pe tiparul lookup, cele două operații "delicate" devin ușoare.

**Adăugarea unei stări** (`REZERVAT`, pentru că acum abonamentele pot fi "rezervate" înainte de activare):

```sql
-- Extinde ENUM-ul în lookup (operație de metadata, milisecunde)
ALTER TYPE cod_stare_abonament ADD VALUE 'REZERVAT' BEFORE 'ACTIV';

-- Inserează noul rând
INSERT INTO stari_abonament (cod, descriere, ordine, activ) VALUES
  ('REZERVAT', 'Abonament rezervat, încă neactiv', 5, TRUE);
```

**Retragerea unei stări** (`EXPIRAT` absorbit de `TERMINAT`): aici în PostgreSQL nu există `DROP VALUE`. Dar pe un lookup de câteva rânduri, recrearea tipului este o operație de câteva secunde chiar și în producție:

```sql
-- 1. Migrează rândurile lookup-ului care folosesc valoarea "veche"
UPDATE stari_abonament SET cod = 'TERMINAT' WHERE cod = 'EXPIRAT';
-- (Un singur rând; sub FK master-ul rămâne să indice spre același id)

-- 2. Creează noul tip cu vocabularul actualizat
CREATE TYPE cod_stare_abonament_v2 AS ENUM (
  'REZERVAT','ACTIV','SUSPENDAT','TERMINAT'
);

-- 3. Schimbă tipul coloanei în lookup
ALTER TABLE stari_abonament 
  ALTER COLUMN cod TYPE cod_stare_abonament_v2 
  USING cod::text::cod_stare_abonament_v2;

-- 4. Dropează tipul vechi
DROP TYPE cod_stare_abonament;
ALTER TYPE cod_stare_abonament_v2 RENAME TO cod_stare_abonament;
```

Patru pași, toți pe un tabel mic. Master-ul `abonamente` — cel cu sute de milioane de rânduri — nu se atinge niciodată. Continuă să referențieze `stare_id`, și FK rezolvă mereu la rândul corect al lookup-ului. **Integritatea este ancorată în id-ul surogat**, nu în codul ENUM, și aceasta este cheia tiparului.

---

## Regula de aur

Mesajul pe care îl iau din cazul abonamentelor — și care este valabil, identic, atât în PostgreSQL cât și în MySQL — este:

> Dacă valorile domeniului nu se vor schimba niciodată, ENUM este alegerea corectă. Dacă se vor schimba — chiar și "din când în când" — nu lega vocabularul de schemă.

Diferența dintre cele două baze de date nu este în această regulă. Este în **unde cade prețul** când domeniul se schimbă:

- **În MySQL**, adăugarea unei valori într-o poziție specifică costă un rebuild al tabelului. Adăugarea ei la coadă este economică; corupe însă ordonarea.
- **În PostgreSQL**, adăugarea este mereu economică (chiar și în poziție specifică). Eliminarea sau reorganizarea este migrarea grea.

A-ți înțelege cazul de utilizare înseamnă a înțelege **ce fel de evoluție va suferi probabil domeniul**. Doar adăugări? PostgreSQL ENUM este un aliat. Adăugări și eliminări? Mai bine un tabel lookup de la început.

---

## Miniserialul cross-DB

Acesta este al doilea din miniserialul despre enumerări în diferitele DBMS-uri. Întrebarea "ENUM sau lookup?" nu are un răspuns universal — își schimbă fața în funcție de baza de date. Primul articol, despre MySQL, este disponibil aici:

- **[ENUM în MySQL: când îți simplifică viața și când îți complică zilele](/ro/posts/mysql/enum-mysql-semplifica-o-complica/)** — aceeași întrebare, o filozofie diferită, și cazul real al unui sistem de tracking al expedierilor

Următoarele întâlniri:

- **Oracle** — `CHECK` constraint, SQL Domains din 23ai, și de ce Oracle a ajuns "târziu" la această temă
- **Oracle, deep-dive vertical** — cum se modelau enumerările în 19c, ce s-a schimbat în 21c, 23ai și 26ai, până la noile Assertions

> 📖 **Dacă ai ajuns aici primul**: îți recomand să citești și [primul articol al miniserialului, cel despre MySQL](/ro/posts/mysql/enum-mysql-semplifica-o-complica/). Multe dintre tiparele despre care vorbim aici — cele trei drumuri, tabelul lookup făcut bine, ENUM-ul în interiorul lookup-ului — sunt introduse acolo. Comparația face totul mai clar.

------------------------------------------------------------------------

## Surse oficiale

1. PostgreSQL Documentation — [Enumerated Types](https://www.postgresql.org/docs/current/datatype-enum.html)
2. PostgreSQL Documentation — [`CREATE TYPE`](https://www.postgresql.org/docs/current/sql-createtype.html)
3. PostgreSQL Documentation — [Constraints (CHECK)](https://www.postgresql.org/docs/current/ddl-constraints.html)
4. PostgreSQL Documentation — [`CREATE TABLE` (FOREIGN KEY)](https://www.postgresql.org/docs/current/sql-createtable.html)
5. PostgreSQL Documentation — [`ALTER TYPE` (ADD VALUE)](https://www.postgresql.org/docs/current/sql-altertype.html)

------------------------------------------------------------------------

## Glosar

**[CREATE TYPE AS ENUM](/ro/glossary/postgresql-create-type-enum/)** — Statement DDL PostgreSQL care creează un tip enumerativ ca obiect de primă clasă. Spre deosebire de MySQL, tipul există independent de coloanele care îl folosesc și poate fi reutilizat.

**[ALTER TYPE ADD VALUE](/ro/glossary/postgresql-alter-type-add-value/)** — Comandă PostgreSQL care adaugă o valoare la un ENUM existent. Operație de metadata, tranzacțională, fără rebuild al tabelului. Disponibilă din PostgreSQL 9.1, cu poziționare `BEFORE`/`AFTER` din 9.6.

**[OID (Object Identifier)](/ro/glossary/postgresql-oid/)** — Identificator numeric intern folosit de PostgreSQL pentru a se referi la obiecte de sistem (tabele, tipuri, funcții). Pentru ENUM-uri, valoarea este stocată ca OID intern de 4 octeți.

**[Type safety](/ro/glossary/type-safety/)** — Proprietate a unui sistem de tipuri care împiedică, la parse-time sau compile-time, utilizarea de valori incompatibile. ENUM în PostgreSQL este un tip de sine stătător, nu o restricție pe `VARCHAR`, și asta permite type safety end-to-end în funcții și proceduri.

**[Lookup table](/ro/glossary/lookup-table/)** — Tabel de referință legat prin foreign key care stochează valorile valide ale unei enumerări, cu eventuale atribute descriptive (etichetă, ordine, flag activ). Tipar preferat când domeniul evoluează în timp.
