---
title: "Oracle 19c, 21c, 23ai, 26ai: rescrierea silențioasă a domeniilor de valori"
seoTitle: "Oracle 19c → 26ai: SQL Domains și Assertions în 7 ani"
description: "Șapte ani de Oracle văzuți prin enumerări: de la CHECK-ul 19c la SQL Domains 23ai, până la Assertions 26ai. O migrare în sectorul asigurări."
date: "2026-06-23T08:03:00+01:00"
draft: false
translationKey: "enum_oracle_19c_26ai_domini"
tags: ["schema-design"]
categories: ["oracle"]
image: "enum-oracle-19c-26ai-domini.cover.jpg"
---

În ultimii șapte ani Oracle a rescris în silențiu cum se modelează **domeniile de valori** într-o schemă. Fără anunțuri răsunătoare, fără fanfara pe care PostgreSQL și MySQL au știut să o construiască în jurul `ENUM`-ului lor. Patru major release — 19c, 21c, 23ai, 26ai — și o traiectorie care, văzută de sus, povestește o istorie precisă: Oracle a ajuns ultimul, și a ajuns cu o soluție diferită.

Dacă cauți tabloul orizontal (Oracle vs MySQL vs PostgreSQL, cele trei drumuri comparate alături), este în [acest articol al miniseriei](/ro/posts/oracle/enum-oracle-workaround-fino-a-23ai/). Aici luăm în schimb lentila verticală: o singură platformă, șapte ani, patru release-uri. Ce aveai la dispoziție în fiecare perioadă, ce se schimbă în ceea ce vine după.

---

## 19c (2019): punctul de plecare

Oracle Database 19c, lansată în 2019, este și astăzi **long-term release de referință** pentru foarte multe sisteme enterprise — banking, asigurări, administrația publică italiană, unde upgrade-urile au un ciclu lung și prudent. Când această istorie începe, instrumentele la dispoziție pentru modelarea unei enumerări erau două, și niciuna dintre ele nu era "elegantă":

```sql
-- Opțiunea 1: CHECK inline (Oracle 19c)
CREATE TABLE polite (
  id          NUMBER PRIMARY KEY,
  numar       VARCHAR2(20) NOT NULL,
  stare       VARCHAR2(20) NOT NULL,
  CONSTRAINT chk_stare_polita CHECK (stare IN
    ('EMISA','IN_VIGOARE','SUSPENDATA','EXPIRATA','ANULATA','STORNATA'))
);

-- Opțiunea 2: lookup table cu FK (Oracle 19c)
CREATE TABLE stari_polita (
  cod       VARCHAR2(20) PRIMARY KEY,
  eticheta  VARCHAR2(100) NOT NULL,
  ordine    NUMBER,
  activ     CHAR(1) DEFAULT 'Y' CHECK (activ IN ('Y','N'))
);

CREATE TABLE polite (
  id         NUMBER PRIMARY KEY,
  numar      VARCHAR2(20) NOT NULL,
  stare_cod  VARCHAR2(20) NOT NULL,
  CONSTRAINT fk_stare FOREIGN KEY (stare_cod)
    REFERENCES stari_polita(cod)
);
```

`CHECK`-ul este ușor, aplicat de motor la runtime și folosit chiar de optimizator pentru a **elimina condiții imposibile** [1] — dar este local coloanei, și replicarea aceleiași constrângeri pe douăzeci de tabele care împart același domeniu este un exercițiu de răbdare (și de disciplină la code review). Lookup table este calea bazei de date pure, dominantă în proiectele enterprise: un JOIN în plus, dar și o enumerare care devine un **obiect al bazei de date cu viață proprie** — etichete localizate, ordine de display, flag activ/inactiv, audit trail.

În 19c **asta era tot**. Niciun `CREATE TYPE ENUM` ca în PostgreSQL, niciun `ENUM` de coloană ca în MySQL. Pentru cine venea din aceste două lumi, senzația era: *"deci nu există nimic nativ?"*. Răspunsul: nu. Era `CHECK`, era lookup-ul, și erau douăzeci de ani de meserie acumulată despre cum să-i facă să funcționeze împreună.

---

## 21c (2021): un innovation release care sare peste domeniile de valori

Oracle Database 21c — "innovation release"-ul, ajuns pe Cloud în 2020 și on-premises în 2021 — aduce lucruri mari: **tipul JSON nativ** [2], **blockchain table** și **immutable table** pentru audit ne-manipulabil, **SQL Macros** pentru reutilizarea fragmentelor de SQL, integrarea AutoML in-DB. Este un release plin de idei noi.

Dar pentru cine privea la problema specifică a modelării domeniilor de valori, **21c nu aduce nimic**. Niciun `CREATE DOMAIN`, nicio revizuire a `CHECK`-ului, nicio meta-taxonomie integrată în dicționarul de date. Alegerea DBA-ului care migrează de la 19c la 21c, pe subiectul enumerări, nu se schimbă: `CHECK` sau lookup.

Merită totuși numită, pentru că marchează o trecere: Oracle în acei doi ani lucra la altceva, iar cine spera la un răspuns pe frontul schema-domain trebuia să aștepte. **Așteptarea a durat doi ani mai mult decât se credea**, și s-a încheiat cu saltul numeric spre 23ai — primul semnal, nu doar nominal, că Oracle urma să schimbe pasul.

---

## 23ai (2024): SQL Domains, în sfârșit

Aprilie 2024, Oracle Database 23ai lansată pe engineered system (Exadata Cloud@Customer mai întâi, apoi disponibilitate mai amplă). Printre zecile de noutăți — și sunt multe, de la `JSON Relational Duality` la `AI Vector Search` — constructul care contează pentru istoria noastră este unul singur: **SQL Domain** [3].

```sql
-- Oracle 23ai
CREATE DOMAIN stare_polita AS VARCHAR2(20)
  CONSTRAINT chk_stare_polita CHECK (VALUE IN
    ('EMISA','IN_VIGOARE','SUSPENDATA','EXPIRATA','ANULATA','STORNATA'))
  DEFAULT 'EMISA'
  ANNOTATIONS (
    display 'Stare Polița',
    description 'Ciclul de viață al unei polițe de asigurare',
    ordering 'EMISA<IN_VIGOARE<SUSPENDATA<EXPIRATA<ANULATA<STORNATA'
  );

CREATE TABLE polite (
  id     NUMBER PRIMARY KEY,
  numar  VARCHAR2(20) NOT NULL,
  stare  stare_polita NOT NULL
);

CREATE TABLE istoric_polite (
  id_polita    NUMBER,
  data_eveniment DATE,
  stare        stare_polita NOT NULL,
  CONSTRAINT fk_pol FOREIGN KEY (id_polita) REFERENCES polite(id)
);
```

Trei lucruri merită citite cu calm în acest bloc.

**Primul**: `DOMAIN`-ul este un **obiect al dicționarului de date**. Se găsește în `DBA_DOMAINS`, `USER_DOMAINS`, `ALL_DOMAINS`, cu coloane care descriu tipul de bază, constrângerea, default-ul. Pentru prima dată, în Oracle, **enumerarea există ca entitate în catalogul schemei** fără a necesita o a doua tabelă de lookup. Design review-ul care întreba "unde este documentat că `stare` poate lua doar aceste șase valori?" găsește acum un răspuns direct.

**Al doilea**: `ANNOTATIONS`. Sunt perechi cheie/valoare de metadate pe care instrumentele BI, procedurile de UI generation și framework-urile de raportare le pot citi prin `USER_ANNOTATIONS_USAGE` pentru a deriva automat etichete de display, descrieri de câmp, ordering de reprezentare. Pe PostgreSQL `DOMAIN`-ul are doar tip + constrângere; Oracle a făcut aici un pas în plus, și este un pas care se observă când un raport Power BI sau Tableau se sprijină direct pe dicționar pentru a construi hărțile sale semantice.

**Al treilea**: o singură coloană `stare` de tip `stare_polita` poate fi folosită în **zeci de tabele**, și în toate se aplică aceeași constrângere, același default, aceleași annotations. Ceea ce cu `CHECK` necesita douăzeci de `ALTER TABLE` pentru a fi modificat, cu `DOMAIN` necesită un singur `ALTER DOMAIN` [4].

---

## O migrare 19c → 23ai concretă

Schema unei companii de asigurări — multi-țară, sector Surety — pe Oracle 19c, în jur de 1.800 de tabele în schema aplicativă, și o taxonomie de stări polițe replicată în **22 de tabele** ale modulului de gestiune contracte. De fiecare dată când compliance-ul cerea să se adauge o stare nouă (ultima dată: `'IN_VERIFICARE_ANTILAUNDERING'` pentru o nouă policy normativă) erau 22 de `ALTER TABLE` de planificat, testat, deployat în fereastră nocturnă.

Upgrade-ul la 23ai nu a fost făcut **pentru** această problemă — a fost făcut din alte motive (consolidare infrastructurală, sfârșitul suportului Premier pe 19c). Dar odată ajuns pe 23ai, echipa arhitecturală a pus în plan un mic refactor: să convertească taxonomia stărilor polițelor într-un SQL Domain unic.

Pașii, pe scurt, au fost aceștia:

```sql
-- 1) Crearea domain-ului cu valorile istorice deja prezente în producție
CREATE DOMAIN stare_polita AS VARCHAR2(20)
  CONSTRAINT chk_stare_polita CHECK (VALUE IN
    ('EMISA','IN_VIGOARE','SUSPENDATA','EXPIRATA','ANULATA','STORNATA',
     'IN_VERIFICARE_ANTILAUNDERING'))
  DEFAULT 'EMISA';

-- 2) Pe tabela principală, declararea domain-ului pe coloana existentă
ALTER TABLE polite MODIFY (stare stare_polita);

-- 3) Același lucru pentru fiecare dintre cele 21 de tabele dependente
ALTER TABLE istoric_polite MODIFY (stare stare_polita);
ALTER TABLE polite_prime   MODIFY (stare stare_polita);
-- ... etc.

-- 4) Drop al vechilor CHECK inline redundante (acum domain-ul le înlocuiește)
ALTER TABLE polite        DROP CONSTRAINT chk_stare_polita;
ALTER TABLE istoric_polite DROP CONSTRAINT chk_stare_istoric;
-- ... etc.
```

Cele 22 de tabele au fost migrate într-o fereastră de mentenanță de puțin peste o oră — aproape tot timpul a fost consumat de **validarea rândurilor existente** (`VALIDATE`, default în Oracle), care a citit fiecare tabel pentru a confirma că nicio valoare istorică nu viola constrângerea domain-ului. Pentru tabelele cele mai mari (istoric polițe, ~340 de milioane de rânduri) s-a ales `NOVALIDATE` cu un cleanup ulterior prin batch: în producție integritatea înainte era garantată de domain, iar datele istorice fuseseră deja controlate cu un script de pre-flight.

Rezultatul final, după refactor: o singură linie de DDL pentru a modifica taxonomia. Următoarea cerere de compliance — va fi una, întotdeauna — va costa un `ALTER DOMAIN`, nu o săptămână de planificare.

Nu este o istorie de eroism. Este istoria unei echipe care a recunoscut o oportunitate la momentul potrivit și a luat-o — Oracle în sfârșit dăduse instrumentul, mai rămânea doar să-l ia în mână.

---

## 26ai (2026): ASSERTION și ce se vede la orizont

Oracle 26ai (anunțată ca următoarea major release) aduce pe masă, printre altele, **`ASSERTION`**: un construct SQL standard pe hârtie de zeci de ani, niciodată cu adevărat implementat de niciun DBMS mainstream, care permite exprimarea constrângerilor **cross-tabel** validate la nivel tranzacțional de motorul bazei de date.

Pentru istoria noastră, `ASSERTION` sunt piesa care închide un cerc. Cu SQL Domain-ul din 23ai am rezolvat problema "aceeași constrângere pe multe coloane". Cu `ASSERTION` din 26ai se deschide o altă posibilitate: constrângeri care implică **mai multe tabele împreună**, garantate de baza de date fără a fi nevoie să intervină un trigger sau un check aplicativ.

```sql
-- Exemplu (sintaxă indicativă bazată pe standardul SQL):
CREATE ASSERTION cel_putin_o_stare_activa CHECK (
  (SELECT COUNT(*) FROM stari_polita WHERE activ = 'Y') >= 1
);

CREATE ASSERTION istoric_coerent CHECK (
  NOT EXISTS (
    SELECT 1 FROM polite p
    LEFT JOIN istoric_polite h ON h.id_polita = p.id
    WHERE p.stare = 'STORNATA' AND h.stare IS NULL
  )
);
```

Astfel de constrângeri astăzi se scriu ca trigger — cu toate problemele aferente: trigger uitate în deploy-uri ulterioare, tranzacții care ocolesc check-ul din cauza isolation level-ului, race condition greu de diagnosticat. `ASSERTION` ar deplasa responsabilitatea către motor. Când 26ai va fi disponibilă în test și pe workload-uri reale, va fi material de aprofundat — dar designul unei taxonomii astăzi poate deja să țină cont de unde constrângerile cross-tabel vor trăi mai bine mâine.

---

## Ce Oracle încă nu are

Există un lucru pe care, încă de astăzi, Oracle nu îl oferă: un **tip enumerativ nativ** ca cel din PostgreSQL (`CREATE TYPE ... AS ENUM`) sau din MySQL (`ENUM(...)`). Merită spus deschis, pentru că cineva s-ar putea întreba.

SQL Domain este **conceptual mai puternic** decât un ENUM tradițional (este o constrângere reutilizabilă, nu un tip "închis"), dar este și **mai verbose** de declarat și are un overhead de indirecție în dicționarul de date. Pentru cazul de utilizare cel mai simplu — o coloană într-o singură tabelă, set de valori foarte mic, nicio metadată — `CHECK`-ul inline rămâne mai concis. Oracle 23ai, cu alte cuvinte, nu a înlocuit `CHECK`-ul: i-a oferit un companion pentru când `CHECK`-ul nu mai era suficient.

Este coerent cu filozofia Oracle: a oferi instrumente puternice și generale, lăsând designerului responsabilitatea de a alege nivelul corect de abstractizare. PostgreSQL și MySQL au făcut alegerea opusă — a da un tip gata făcut și specific — și pentru multe cazuri acea alegere este mai imediată. Sunt două culturi diferite, ambele legitime.

---

## Traiectoria, văzută de la sfârșitul lui 2026

Șapte ani, patru release-uri, și o linie care din exterior pare continuă dar privită din interior este făcută din pauze și din salturi. 19c era punctul de plecare: două drumuri cunoscute și niciun al treilea. 21c a adus alte lucruri, rămânând nemișcată pe acest teren. 23ai a deschis **drumul structural** care lipsea de zeci de ani. 26ai închide cercul asupra constrângerilor care depășesc o singură tabelă.

Nu este o istorie eroică. Oracle a ajuns după PostgreSQL (care are `DOMAIN` din anii '90 târzii) și după MySQL (care are `ENUM` dintotdeauna). Dar când a ajuns, a ajuns cu o idee diferită — mai generală, mai integrată în dicționar, mai extensibilă prin annotations — și acea idee devine modul standard de a modela domeniile de valori pe noile scheme Oracle pe care le văd născându-se în producție astăzi.

Întrebarea de luat cu tine, pentru cine modelează scheme enterprise pe Oracle: **nu mai "ce drum aleg", ci "când `CHECK`-ul inline îmi este suficient, și când merită să declar un `DOMAIN`"**. Cele două opțiuni coexistă, iar a ști când să treci de la una la cealaltă este astăzi adevăratul discrimen.

---

## Surse oficiale

1. Oracle Database 19c SQL Language Reference — [constraint_clause (CHECK și alte constrângeri)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/constraint.html)
2. Oracle Database 21c Database New Features Guide — [Innovation Release overview](https://docs.oracle.com/en/database/oracle/oracle-database/21/nfcoa/index.html)
3. Oracle Database 23ai SQL Language Reference — [CREATE DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/CREATE-DOMAIN.html)
4. Oracle Database 23ai SQL Language Reference — [ALTER DOMAIN](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/ALTER-DOMAIN.html)

---

## Glosar

- **[SQL Domain](/ro/glossary/oracle-sql-domain/)** — Construct introdus în Oracle 23ai care permite definirea unui domeniu reutilizabil (tip de bază + CHECK + DEFAULT + annotations) ca obiect al dicționarului de date. Pentru prima dată în Oracle, o enumerare există în catalogul de schemă fără a necesita o tabelă de lookup.
- **[Annotations (Oracle 23ai)](/ro/glossary/oracle-annotations/)** — Perechi cheie/valoare de metadate atașabile obiectelor de schemă (coloane, domain, tabele), citibile prin `USER_ANNOTATIONS_USAGE`. Folosite de instrumentele BI și UI generation pentru a deriva automat etichete de display, descrieri, ordering.
- **[VALIDATE / NOVALIDATE](/ro/glossary/oracle-validate-novalidate/)** — Moduri de aplicare a unei constrângeri Oracle la crearea sau modificarea ei: `VALIDATE` citește toate rândurile existente pentru a verifica conformitatea (default), `NOVALIDATE` sare peste verificare pentru a nu bloca tabelele mari în fereastră de mentenanță.
- **[Major release Oracle](/ro/glossary/oracle-major-release/)** — Versiune principală a Database server-ului cu schimbări semnificative de feature, ciclu de suport Premier dedicat și numerotare proprie (19c, 21c, 23ai, 26ai). Diferite de patch set-uri și release update-urile intermediare.
- **[ASSERTION](/ro/glossary/sql-assertion/)** — Construct SQL standard pentru exprimarea constrângerilor cross-tabel validate la nivel tranzacțional de motorul bazei de date. Anunțat în Oracle 26ai.
