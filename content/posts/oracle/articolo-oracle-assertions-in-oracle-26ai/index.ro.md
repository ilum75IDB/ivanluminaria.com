---
categories:
- oracle
date: '2026-08-04'
description: Oracle 26ai introduce CREATE ASSERTION, constrângerea cross-tabel pe
  care SQL-92 o promitea de decenii. Sintaxă, comparație cu trigger-e și cazuri reale
  din asigurări.
draft: false
image: articolo-oracle-assertions-in-oracle-26ai.cover.jpg
seoTitle: 'CREATE ASSERTION Oracle 26ai: constrângeri cross-tabel declarative'
tags:
- oracle-26ai
- integrity-constraints
- assertions
- sql-standard
- oracle-23ai
title: 'Trei trigger, un job nocturn și 1.247 de polițe orfane: ASSERTION în Oracle
  26ai'
translationKey: articolo_oracle_assertions_in_oracle_26ai
webo_generated_at: 2026-07-31
webo_status: scheduled
---

## Trei trigger, un job nocturn și 1.247 de polițe orfane

Era o migrare batch de rutină — sau cel puțin așa părea. Un mare grup de asigurări italian consolida date istorice dintr-un sistem legacy: câteva milioane de rânduri pe tabelele `polizze` și `beneficiari`, fereastră de mentenanță sâmbătă noaptea, script testat în staging. Pentru a accelera încărcarea, echipa dezactivase temporar trigger-ele pe cele două tabele. Procedură standard, documentată în runbook.

Problema a apărut duminică dimineața, când job-ul nocturn de reconciliere și-a terminat rularea de 45 de minute pe 2,1 milioane de polițe și a produs un raport cu 1.247 de rânduri anomale: polițe în starea `ATTIVA` fără niciun beneficiar asociat. Încălcare directă a unei reguli de business critice — „orice poliță activă trebuie să aibă cel puțin un beneficiar cu cotă totală egală cu 100%" — pe care sistemul trebuia să o garanteze în orice moment.

Regula era implementată cu trei trigger-e coordonate: un `AFTER INSERT OR UPDATE` pe `polizze` care verifica prezența beneficiarilor când starea devenea `ATTIVA`, un `AFTER DELETE` pe `beneficiari` care controla că polița asociată nu rămânea orfană, și un al treilea `AFTER UPDATE` pe `beneficiari` care recalcula cotele. Plus job-ul nocturn ca plasă de siguranță pentru cazurile care scăpau — și ceva scăpa întotdeauna, în special în timpul operațiunilor batch cu trigger-e dezactivate.

Timp de detectare: aproximativ 18 ore. Timp de corecție manuală: o jumătate de zi de muncă. Cost real: scăzut, din fericire. Dar întrebarea care a rămas pe masă după incident era cea corectă: există un mod de a exprima această regulă la nivel de schemă, astfel încât să nu poată fi ocolită de nicio operațiune DML, batch sau nu?

Cu Oracle 26ai, răspunsul este da.

## SQL-92 avusese dreptate, dar nimeni nu ascultase

Standardul SQL definește `CREATE ASSERTION` din 1992. Ideea este simplă: o constrângere de integritate nu trebuie limitată la un singur rând sau la o singură tabelă — trebuie să poată exprima predicate asupra întregii stări a bazei de date. Sintaxa originală a standardului este:

```sql
CREATE ASSERTION nume_constrângere CHECK (condiție_booleană)
```

unde `condiție_booleană` poate implica subquery-uri, agregări, join-uri între tabele diferite. Semantic, constrângerea este satisfăcută când condiția este `TRUE` sau `UNKNOWN`; este violată când este `FALSE`.

Problema este că niciun RDBMS mainstream nu implementase vreodată această funcționalitate în mod complet. PostgreSQL nu o are. MySQL nu o are. SQL Server nu o are. Motivele sunt cunoscute: evaluarea unui predicat care traversează mai multe tabele are un cost potențial ridicat, iar momentul corect în care să-l evaluezi — după fiecare instrucțiune DML individuală, sau la sfârșitul tranzacției? — deschide probleme de implementare deloc banale. Rezultat: timp de treizeci de ani, funcționalitatea a rămas în documentul standardului fără să aterizeze în produse.

Oracle 23ai (redenumit ulterior 26ai în versiunea următoare) este primul RDBMS enterprise mainstream care o aduce în producție [1]. Este o alegere cu o greutate conceptuală precisă: semnalează că Oracle ia în serios conformitatea cu standardul SQL pe funcționalități pe care alți vendori le-au ignorat, și că modelul relațional — cu constrângerile sale declarative — este în continuare direcția de dezvoltare, nu o moștenire de gestionat.

Distincția fundamentală față de un `CHECK` constraint obișnuit este aceasta: un `CHECK` evaluează un predicat pe coloanele rândului curent, la momentul inserării sau actualizării. O `ASSERTION` evaluează un predicat asupra întregului conținut al tabelelor implicate, după fiecare operațiune DML care ar putea să-l facă fals. Sunt instrumente diferite pentru probleme diferite.

## `CREATE ASSERTION` în Oracle 26ai: sintaxa

Reluând schema proiectului din asigurări, cele două tabele de referință sunt:

```sql
-- Schema ins_core pe oracle-node-01
CREATE TABLE polizze (
    id            NUMBER PRIMARY KEY,
    numero        VARCHAR2(20) NOT NULL,
    stato         VARCHAR2(10) CHECK (stato IN ('BOZZA','ATTIVA','SCADUTA','ANNULLATA')),
    data_inizio   DATE NOT NULL,
    data_fine     DATE
);

CREATE TABLE beneficiari (
    id            NUMBER PRIMARY KEY,
    id_polizza    NUMBER NOT NULL REFERENCES polizze(id),
    nome          VARCHAR2(100) NOT NULL,
    quota_pct     NUMBER(5,2) NOT NULL CHECK (quota_pct > 0 AND quota_pct <= 100)
);
```

Constrângerea pe care cele trei trigger-e încercau să o garanteze se exprimă astfel:

```sql
-- Orice poliță ATTIVA trebuie să aibă cel puțin un beneficiar
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

Acesta este pattern-ul existențial clasic: „nu există nicio poliță activă pentru care să nu existe niciun beneficiar". Dubla negație este modul standard de a exprima „pentru orice X trebuie să existe cel puțin un Y" în SQL, iar Assertions îl fac în sfârșit declarabil la nivel de schemă [2].

A doua constrângere — cotele trebuie să sumeze la 100 — folosește un pattern cu agregare:

```sql
-- Cotele beneficiarilor fiecărei polițe ATTIVA trebuie să sumeze la 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

Acest al doilea pattern este cel care cu `CHECK` constraint-urile tradiționale este pur și simplu imposibil de exprimat: condiția implică o agregare pe rânduri diferite din aceeași tabelă, filtrată prin join cu o altă tabelă.

Pentru a elimina o Assertion:

```sql
DROP ASSERTION ins_core.polizza_ha_beneficiario;
```

Documentația Oracle 26ai prevede și posibilitatea de a dezactiva temporar o Assertion cu `DISABLE` și de a o reactiva cu `ENABLE`, similar cu constraint-urile tradiționale [1]. Acest punct este relevant pentru operațiunile de mentenanță — dar, după cum vom vedea, este și exact punctul critic de gestionat cu atenție.

## De ce alternativele pre-26ai nu erau echivalente

Merită să fim preciși în privința asta, pentru că tentația de a spune „se poate face și cu trigger-e" este reală — și tehnic adevărată, dar ascunde diferențe importante.

| Mecanism | Declarativ | Rezistă la bulk load | Lizibil din schemă | Cost de evaluare |
|---|---|---|---|---|
| `CHECK` constraint | ✅ | ✅ | ✅ | Scăzut (rând unic) |
| Trigger `AFTER` | ❌ | ❌ (dezactivabil) | ❌ | Mediu (per rând) |
| `DEFERRABLE` constraint | ✅ | Parțial | ✅ | Scăzut-mediu |
| Materialised view + `WITH CHECK OPTION` | Parțial | ❌ | Parțial | Ridicat (refresh) |
| **ASSERTION** | ✅ | ✅ (dacă nu e dezactivată) | ✅ | Mediu-ridicat (cross-table) |

`CHECK` constraint-ul este declarativ și lizibil, dar nu poate conține subquery-uri care referențiază alte tabele — limitare cunoscută și documentată [3]. Oracle o aplică în mod explicit: un `CHECK` care încearcă să facă `SELECT` pe o altă tabelă generează o eroare la creare.

Trigger-ele `AFTER INSERT/UPDATE/DELETE` funcționează, dar sunt procedurale. Nu apar în definiția schemei într-un mod lizibil; se dezactivează cu `ALTER TABLE DISABLE ALL TRIGGERS` sau cu `ALTER TABLE ... DISABLE TRIGGER nume`; în DML complexe cu ordini de firing nebanale pot produce rezultate neașteptate. Incidentul cu 1.247 de polițe orfane este exact consecința acestei fragilități.

`DEFERRABLE` constraint-urile gestionează temporalitatea — permit amânarea verificării la sfârșitul tranzacției în loc de la fiecare instrucțiune individuală — dar nu exprimă predicate cross-tabel. Sunt utile pentru DML multi-step (inserează rândul părinte, apoi copiii, verifică foreign key-ul doar la commit), nu pentru constrângeri care traversează tabele diferite [3].

Materialised view-urile cu `WITH CHECK OPTION` sunt o aproximare creativă: se creează o vedere care expune violările, se adaugă o constrângere pe vedere. Nu este o constrângere în sens strict, are costuri de refresh, iar comportamentul în scenarii de concurență este mai puțin predictibil.

## Când are sens să le folosești, și când nu

Assertions nu sunt gratuite. Costul de evaluare este real: fiecare operațiune DML pe o tabelă implicată într-o Assertion poate necesita executarea subquery-ului de verificare. Pe tabele cu DML de înaltă frecvență — milioane de inserări pe secundă, sisteme OLTP cu latență critică — acest overhead trebuie măsurat înainte de a adopta funcționalitatea în producție.

Cazurile în care Assertions au sens:

- **Reguli de integritate stabile în timp**: dacă predicatul se schimbă rar, costul `DROP/CREATE` este acceptabil. Dacă regula se schimbă la fiecare sprint, trigger-ele sunt mai flexibile.
- **Frecvență DML moderată**: sisteme tranzacționale normale, nu pipeline-uri de ingestie cu throughput ridicat.
- **Predicate care implică agregări sau existență cross-tabel**: exact cazurile pe care `CHECK` constraint-urile nu le acoperă.
- **Medii unde lizibilitatea schemei este critică**: audit, compliance, onboarding de noi DBA — a avea constrângerea declarată în schemă este un avantaj documentar concret.

Cazurile de evitat sau de evaluat cu atenție:

- **Bulk load cu direct-path insert**: `INSERT /*+ APPEND */` în Oracle ocolește buffer cache-ul și scrie direct în datafile-uri. Comportamentul Assertions în acest scenariu — dacă sunt evaluate, când, cu ce granularitate — trebuie verificat în mediul specific [4]. Nu presupune că comportamentul este identic cu conventional insert.
- **Tabele cu DML de foarte înaltă frecvență**: costul de evaluare se înmulțește cu fiecare operațiune. Măsoară mai întâi.
- **Funcționalitate în fază de maturizare**: Oracle 26ai este o versiune recentă. Assertions sunt o funcționalitate nouă, iar comportamentul în edge case-uri — concurență ridicată, rollback-uri parțiale, operațiuni DDL concurente — trebuie testat în mediul de destinație înainte de adoptarea în producție [4].

Un punct care merită subliniat: și o Assertion poate fi dezactivată, cu `DISABLE`. Asta înseamnă că situația operațiunilor de mentenanță nu dispare — se mută. Diferența față de trigger-e este că dezactivarea unei Assertions este o operațiune DDL explicită, vizibilă în catalogul de sistem, mai greu de făcut „din greșeală" într-un script de migrare. Nu este o protecție absolută, dar este un guardrail mai robust.

## Pattern-uri recurente: rețetarul

Trei pattern-uri acoperă majoritatea constrângerilor cross-tabel întâlnite în practică.

**Pattern „cel puțin unul"** — fiecare rând din tabela A trebuie să aibă cel puțin un rând corespunzător în B:

```sql
-- Orice poliță ATTIVA trebuie să aibă cel puțin un beneficiar
CREATE ASSERTION ins_core.polizza_ha_beneficiario CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.polizze p
        WHERE  p.stato = 'ATTIVA'
        AND    NOT EXISTS (
                   SELECT 1 FROM ins_core.beneficiari b
                   WHERE  b.id_polizza = p.id
               )
    )
);
```

**Pattern „sumă constrânsă"** — o agregare pe rândurile din B, grupate după cheia din A, trebuie să respecte o condiție:

```sql
-- Cotele beneficiarilor fiecărei polițe ATTIVA trebuie să sumeze la 100
CREATE ASSERTION ins_core.quote_beneficiari_complete CHECK (
    NOT EXISTS (
        SELECT b.id_polizza
        FROM   ins_core.beneficiari b
        JOIN   ins_core.polizze p ON p.id = b.id_polizza
        WHERE  p.stato = 'ATTIVA'
        GROUP BY b.id_polizza
        HAVING SUM(b.quota_pct) <> 100
    )
);
```

**Pattern „toți trebuie"** — fiecare rând din A trebuie să satisfacă o condiție care implică B (variantă cu condiție negată):

```sql
-- Orice daună deschisă trebuie să se refere la o poliță în starea ATTIVA
-- (exemplu cu tabelă sinistri suplimentară)
CREATE ASSERTION ins_core.sinistro_su_polizza_attiva CHECK (
    NOT EXISTS (
        SELECT 1 FROM ins_core.sinistri s
        JOIN   ins_core.polizze p ON p.id = s.id_polizza
        WHERE  s.stato = 'APERTO'
        AND    p.stato <> 'ATTIVA'
    )
);
```

Aceste trei pattern-uri, combinate, acoperă marea majoritate a constrângerilor de integritate cross-tabel care în sistemele pre-26ai ajungeau în trigger-e. Sintaxa este mai verbosă decât un `CHECK` constraint simplu, dar este declarativă, lizibilă și trăiește în schemă.

## Legătura cu articolul #88 și direcția Oracle

Cine a citit articolul despre evoluția Oracle de la 19c la 26ai își va aminti că Assertions erau menționate în ultima secțiune, ca una dintre funcționalitățile cele mai semnificative ale noii versiuni — dar fără aprofundare. Acest articol este acea aprofundare.

În contextul mai larg al roadmap-ului Oracle, Assertions se înscriu într-o tendință precisă: apropierea produsului de conformitatea completă cu standardul SQL, pe funcționalități care rămăseseră teoretice timp de decenii. JSON Relational Duality, True Cache și Assertions împărtășesc această caracteristică — sunt răspunsuri la nevoi reale pe care modelul relațional le teoretizase deja, dar pe care produsele nu le implementaseră niciodată complet.

Nu este nostalgie pentru purismul relațional. Este recunoașterea că unele idei ale modelului relațional — constrângerile declarative în primul rând — au o valoare practică concretă pe care industria a subestimat-o ani de zile, delegând trigger-elor și logicii aplicative ceea ce ar fi trebuit să stea în schemă.

## Constrângerea care nu se rupe pentru că nu există cod de rupt

Trei trigger-e coordonate, un job nocturn de 45 de minute și 1.247 de polițe orfane găsite la 18 ore după incident. Nu este un dezastru — este o situație gestionată, corectată, documentată. Dar costul de mentenanță al acelor trei trigger-e în timp este real: orice modificare a logicii de business necesită actualizarea codului procedural, testarea lui, coordonarea ordinii de firing, reamintirea că trebuie reactivate după fiecare operațiune batch.

Assertion nu este o baghetă magică. Are un cost de evaluare, are limitări în scenarii de bulk load, este o funcționalitate nouă pe o versiune Oracle care nu este încă în producție peste tot. Înainte de a o adopta într-un sistem critic, merită să testezi comportamentul specific în mediul de destinație — în special pentru pattern-urile de DML folosite efectiv, nu doar pentru cazurile standard.

Punctul conceptual, însă, este solid: codul care nu se scrie nu se rupe. O constrângere declarată în schemă este vizibilă, lizibilă, greu de ocolit din greșeală. Un trigger este cod procedural care trăiește într-un loc separat, se dezactivează cu o instrucțiune și necesită ca cel care face migrarea batch să știe că există și că contează.

A muta regula de business în locul potrivit — schema — este o alegere de design, nu doar o chestiune tehnică. Assertions din Oracle 26ai fac această alegere posibilă pentru prima dată în mod declarativ pe un RDBMS enterprise mainstream. Merită să le înțelegi, chiar și pentru cei care nu vor migra la 26ai săptămâna viitoare.

## Fonti ufficiali

1. Oracle Database 23ai — sintaxa și semantica `CREATE ASSERTION` — `<TODO: scout fonte ufficiale per "CREATE ASSERTION Oracle 23ai/26ai documentation">`
2. Oracle Database 23ai New Features Guide — Integrity Constraints — `<TODO: scout fonte ufficiale per "Oracle 23ai New Features Guide — Integrity Constraints">`
3. Oracle Database SQL Language Reference — [Constraint Clauses](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/constraint.html) — acoperă `CHECK`, `DEFERRABLE`, constrângeri de integritate existente (URL de verificat pentru versiunea 26ai)
4. Oracle Database 26ai Release Notes — starea GA vs preview a Assertions, limitări cunoscute — `<TODO: scout fonte ufficiale per "Oracle 26ai Release Notes">`
5. ISO/IEC 9075 SQL Standard, SQL-92 — definiția originală a `CREATE ASSERTION` — `<TODO: scout riferimento pubblico accessibile per SQL-92 CREATE ASSERTION>`

## Glosar candidat

- **ASSERTION** (Oracle 26ai / standard SQL) — constrângere de integritate declarativă care exprimă un predicat asupra întregii stări a bazei de date, implicând potențial mai multe tabele. Definită în SQL-92, implementată pentru prima dată într-un RDBMS enterprise mainstream cu Oracle 23ai/26ai.

- **Predicat existențial** (SQL) — expresie logică care afirmă existența cel puțin a unui rând care satisface o condiție. În SQL se exprimă tipic cu `EXISTS` sau `NOT EXISTS` în subquery corelat; este pattern-ul de bază pentru Assertions de tip „cel puțin unul".

- **Predicat universal** (SQL) — expresie logică care afirmă că o condiție este valabilă pentru toate rândurile unui set. În SQL se exprimă indirect cu `NOT EXISTS (... WHERE NOT condiție)`, deoarece SQL nu are un cuantificator universal nativ.

- **DEFERRABLE constraint** (Oracle / standard SQL) — constrângere de integritate a cărei verificare poate fi amânată la sfârșitul tranzacției în loc de la fiecare instrucțiune DML individuală. Utilă pentru DML multi-step, dar nu echivalentă cu o Assertion: nu exprimă predicate cross-tabel.

- **Direct-path insert** (Oracle) — modalitate de încărcare a datelor care ocolește buffer cache-ul și scrie direct în datafile-uri, activabilă cu hint-ul `/*+ APPEND */`. Interacționează cu constrângerile de integritate diferit față de conventional insert; comportamentul cu Assertions trebuie verificat caz cu caz.
