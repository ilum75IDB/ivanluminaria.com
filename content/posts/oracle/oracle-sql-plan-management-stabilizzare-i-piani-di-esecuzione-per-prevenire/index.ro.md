---
categories:
- oracle
date: '2026-12-01'
description: 'Cum Oracle SPM a transformat un raport financiar din 45 în 3 minute:
  diagnostic plan suboptimal, achiziție baseline și prevenirea regresiilor.'
draft: false
image: oracle-sql-plan-management-stabilizzare-i-piani-di-esecuzione-per-prevenire.cover.jpg
seoTitle: 'Oracle SPM: stabilizarea planurilor de execuție în producție'
tags:
- oracle
- sql-plan-management
- performance-tuning
- optimizer
- oracle-19c
title: 'Oracle SQL Plan Management: stabilizarea planurilor de execuție pentru a preveni
  regresiile în producție'
translationKey: oracle_sql_plan_management_stabilizzare_i_piani_di_esecuzione_per_prevenire
webo_generated_at: 2026-11-14
webo_status: scheduled
---

## Dimineața lui Pietro și raportul care „merge așa de mereu"

Era una din acele dimineți rare în care telefonul nu suna. Niciun alert, nicio escaladare, niciun DBA al clientului în panică. Pietro, un junior care lucrează cu mine de câteva luni într-un proiect la un mare grup de asigurări italian, se apropiase de biroul meu cu acea curiozitate ușor precaută pe care o au juniorii când înțeleg că expertul are timp.

„Pot să te întreb ceva despre o interogare care m-a intrigat?"

Interogarea în cauză era raportul de cifră de afaceri anuală — unul din acele rapoarte pe care consiliul de management le folosește în fiecare săptămână pentru a monitoriza veniturile. Rula de ani de zile. Patruzeci și cinci de minute de execuție, de fiecare dată. Echipa de dezvoltare știa. PM-ul știa. Managementul știa. Devenise parte din peisaj, ca zgomotul aerului condiționat din sala serverelor: prezent, acceptat, ignorat.

Pietro găsise interogarea în repository și observase că nu părea deosebit de complexă. Patru tabele, câteva join-uri, un agregat. De ce dura 45 de minute?

Am răspuns cum răspund mereu în astfel de cazuri: „Deschidem planul de execuție și vedem ce face optimizer-ul."

Nu bănuiam că acea sesiune didactică se va transforma într-un diagnostic operațional.

## Ce făcea optimizer-ul sub capotă

Interogarea era aceasta, simplificată pentru lizibilitate:

```sql
SELECT
    c.customer_name,
    SUM(il.amount) AS total_revenue
FROM
    FINANCE.CUSTOMERS c
JOIN
    SALES.INVOICES i ON c.customer_id = i.customer_id
JOIN
    SALES.INVOICE_LINES il ON i.invoice_id = il.invoice_id
WHERE
    i.invoice_date BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2025-12-31', 'YYYY-MM-DD')
GROUP BY
    c.customer_name
ORDER BY
    total_revenue DESC;
```

Tabelele implicate nu erau mici: `SALES.INVOICES` avea aproximativ 150 de milioane de rânduri, `SALES.INVOICE_LINES` aproximativ 750 de milioane, `FINANCE.CUSTOMERS` 5 milioane. Filtrul pe `invoice_date` ar fi trebuit să reducă drastic setul de date înainte de join-uri — dar numai dacă optimizer-ul ar fi ales calea corectă.

Am extras planul curent din cursor cache:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id => '<sql_id>', format => 'ALLSTATS LAST'));
```

Planul arăta un Hash Join pe `SALES.INVOICES` și `SALES.INVOICE_LINES` cu Full Table Scan pe ambele tabele — înainte chiar de a aplica filtrul pe dată. Optimizer-ul citea 750 de milioane de rânduri pentru a le elimina pe cele mai multe ulterior.

„De ce face asta?" a întrebat Pietro.

E o întrebare justă. Optimizer-ul nu e prost: a ales acel plan pentru că statisticile disponibile îl conduceau să creadă că era calea cea mai eficientă. Problema e că statisticile se schimbaseră — sau mai bine zis, fuseseră actualizate într-un mod nereprezentativ după o colectare masivă efectuată în timpul unei ferestre de mentenanță, probabil cu date parțiale. Rezultatul: optimizer-ul supraestima selectivitatea filtrului pe `invoice_date` și subestima costul Full Table Scan pe tabelele mari.

Am comparat cu snapshot-urile AWR [1] din săptămânile precedente:

```sql
SELECT
    snap_id,
    plan_hash_value,
    elapsed_time_total / executions_total AS avg_elapsed_us
FROM
    DBA_HIST_SQLSTAT
WHERE
    sql_id = '<sql_id>'
ORDER BY
    snap_id DESC;
```

Planul se schimbase cu aproximativ trei săptămâni înainte. Înainte de acel moment, aceeași interogare rula în mai puțin de 4 minute cu un plan diferit — Nested Loops cu Index Range Scan pe `SALES.INVOICES` (index pe `invoice_date`) și ulterior Index Scan pe `SALES.INVOICE_LINES`. Un plan mult mai eficient pentru acest pattern de acces.

Pietro s-a uitat la cifre în tăcere câteva secunde. „Deci interogarea nu e lentă. Planul e cel greșit."

Exact.

## SQL Plan Management: conceptul de baseline ca ancoră de stabilitate

În acest punct am introdus SQL Plan Management [1], care este exact instrumentul gândit pentru situații ca aceasta.

Ideea de bază e simplă: Oracle menține un repository de planuri de execuție aprobate pentru fiecare SQL statement, numit **SQL Plan Baseline**. Când optimizer-ul generează un plan nou pentru o interogare, îl compară cu baseline-ul. Dacă noul plan nu se află în baseline, este marcat ca „neverificat" (*unaccepted*) și nu este folosit automat — chiar dacă optimizer-ul îl consideră mai bun. Numai planurile explicit acceptate în baseline sunt utilizate în producție.

Acest mecanism creează o separare clară între „optimizer-ul găsește un plan nou" și „planul nou intră în producție". Acea separare e prețioasă: îți oferă timp să evaluezi, să testezi și să decizi în cunoștință de cauză.

SPM operează pe trei concepte fundamentale:

- **SQL Plan Baseline**: setul de planuri acceptate pentru un SQL statement specific, identificat prin `sql_id` sau textul normalizat.
- **Plan acceptat** (*accepted*): un plan din baseline pe care optimizer-ul îl poate folosi.
- **Plan candidat** (*unaccepted*): un plan pe care optimizer-ul l-a găsit, dar care nu a fost încă verificat și acceptat.

Parametrul de sistem `OPTIMIZER_USE_SQL_PLAN_BASELINES` (implicit `TRUE`) controlează dacă optimizer-ul consultă baseline-urile. Parametrul `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES` [3] (implicit `FALSE`) controlează dacă Oracle capturează automat planurile interogărilor repetate.

## Achiziționarea planului bun din cursor cache

Planul optim — cel cu Nested Loops și Index Scan — se afla încă în cursor cache, asociat unui `plan_hash_value` diferit de cel curent. Obiectivul era să îl încărcăm în baseline ca plan acceptat.

Metoda cea mai directă este `DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE` [2]:

```sql
DECLARE
    v_plans_loaded PLS_INTEGER;
BEGIN
    v_plans_loaded := DBMS_SPM.LOAD_PLANS_FROM_CURSOR_CACHE(
        sql_id          => '<sql_id>',
        plan_hash_value => <plan_hash_value_buono>
    );
    DBMS_OUTPUT.PUT_LINE('Planuri încărcate: ' || v_plans_loaded);
END;
/
```

Funcția returnează numărul de planuri încărcate. Planul este inserat în baseline cu starea `ACCEPTED = YES` — gata să fie folosit de optimizer.

Pentru a verifica ce se află în baseline:

```sql
SELECT
    sql_handle,
    plan_name,
    accepted,
    enabled,
    fixed,
    created,
    last_modified
FROM
    DBA_SQL_PLAN_BASELINES
WHERE
    sql_text LIKE '%FINANCE.CUSTOMERS%'
ORDER BY
    created DESC;
```

În acel moment aveam două planuri în baseline: cel bun (tocmai încărcat, `ACCEPTED = YES`) și cel suboptimal pe care optimizer-ul îl folosea. Planul suboptimal nu se afla încă în baseline — era pur și simplu planul pe care optimizer-ul îl alegea liber în absența oricăror constrângeri.

Pasul următor era să ne asigurăm că optimizer-ul folosea planul bun și că nu revenea la cel rău în viitor.

## Procesul de evoluție: cum evaluează SPM planurile noi

Înainte de a dezactiva planul suboptimal, merită să înțelegem cum funcționează mecanismul de evoluție [1] — pentru că aici SPM își arată adevărata utilitate pe termen lung.

Când optimizer-ul găsește un plan care nu se află în baseline, îl adaugă ca plan candidat (*unaccepted*). Acel plan nu este folosit, dar este păstrat pentru o evaluare ulterioară. Procedura `DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE` [2] realizează această evaluare: execută planul candidat în mod controlat și îl compară cu planul acceptat curent. Dacă planul candidat este semnificativ mai eficient (implicit, cel puțin 1,5% mai rapid), este promovat la *accepted*.

```sql
SET SERVEROUTPUT ON
DECLARE
    v_report CLOB;
BEGIN
    v_report := DBMS_SPM.EVOLVE_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        time_limit  => 60,   -- secunde maxime pentru test
        verify      => 'YES',
        commit      => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE(v_report);
END;
/
```

Parametrul `verify => 'YES'` face ca Oracle să execute efectiv planul candidat pentru a-i măsura performanțele. Cu `commit => 'YES'`, dacă planul depășește pragul, este acceptat automat.

În acest caz specific nu aveam nevoie de evoluție automată — planul bun fusese deja încărcat ca acceptat. Dar e important să cunoaștem mecanismul pentru cazurile în care se lucrează cu capturare automată (`OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE`), unde planurile candidat se acumulează și trebuie evaluate periodic.

## Stabilizarea planului optim și blocarea regresiilor viitoare

Cu planul bun în baseline, am făcut un pas în plus: l-am marcat ca `FIXED`. Un plan fixed are prioritate absolută — optimizer-ul îl folosește întotdeauna, indiferent de orice alt plan din baseline sau de eventuale planuri noi găsite.

```sql
DECLARE
    v_plans_modified PLS_INTEGER;
BEGIN
    v_plans_modified := DBMS_SPM.ALTER_SQL_PLAN_BASELINE(
        sql_handle  => '<sql_handle>',
        plan_name   => '<plan_name_buono>',
        attribute_name  => 'fixed',
        attribute_value => 'YES'
    );
    DBMS_OUTPUT.PUT_LINE('Planuri modificate: ' || v_plans_modified);
END;
/
```

După această operațiune, am executat interogarea în mediul de test. Planul ales de optimizer era cel cu Nested Loops și Index Range Scan pe `invoice_date`. Timp de execuție: puțin sub 3 minute, față de cele 45 de minute anterioare.

Diferența de plan era clară: în loc să citească întreaga tabelă `SALES.INVOICE_LINES` (750 de milioane de rânduri) cu un Full Table Scan, optimizer-ul accesa mai întâi `SALES.INVOICES` prin indexul pe `invoice_date` — reducând setul de date la câteva sute de mii de rânduri pentru anul selectat — și apoi executa join-ul cu `SALES.INVOICE_LINES` prin Index Scan pe `invoice_id`. Filtrul era aplicat înainte de join, nu după.

Am lăsat planul suboptimal în baseline cu starea `ENABLED = NO` în loc să îl ștergem, pentru a păstra istoricul și a-l putea reactiva dacă era necesar. O alegere conservatoare, dar sensată în producție.

## Când să folosești SPM: scenarii și compromisuri

Pietro a pus întrebarea potrivită în acel moment: „Dar dacă funcționează atât de bine, de ce nu îl folosim pe toate interogările?"

Răspunsul sincer e că SPM are un cost de administrare care nu e neglijabil.

**Scenarii în care SPM este deosebit de util**:

- **Pre și post upgrade Oracle Database**: un upgrade poate schimba semnificativ comportamentul optimizer-ului. Încărcarea baseline-urilor înainte de upgrade și verificarea lor după este o practică consolidată.
- **Post-aplicare patch**: patch-urile optimizer-ului (incluse în PSU/RU) pot modifica planurile. SPM permite înghețarea planurilor critice înainte de patch.
- **După colectare masivă de statistici**: ca în cazul nostru. O colectare de statistici nereprezentativă poate degrada zeci de interogări simultan.
- **Interogări critice cu SLA stricte**: rapoarte financiare, batch-uri nocturne, interogări de închidere lunară — orice interogare pentru care o regresie are impact direct asupra businessului.

**Compromisuri de luat în considerare**:

- Baseline-urile trebuie întreținute. Dacă structura tabelelor se schimbă (indecși noi, partiții, coloane), planurile din baseline pot deveni suboptimale față de noua structură. E nevoie de un proces de revizuire periodică.
- Cu `OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES = TRUE` la nivel de sistem, planurile candidat se acumulează rapid. Fără un proces regulat de evoluție, baseline-ul devine un arhiv imposibil de gestionat.
- SPM nu înlocuiește statisticile corecte. Este un instrument de stabilizare, nu de optimizare. Planul bun trebuie să existe și să fie identificat: SPM îl conservă, nu îl creează.

Strategia adoptată de noi este selectivă: baseline-uri doar pe interogările critice identificate, cu revizuire trimestrială. Fără capturare automată la nivel de sistem.

## Raportul de luni dimineața

În zilele următoare, raportul de cifră de afaceri a început să ruleze în aproximativ 3 minute. Niciun anunț, nicio comunicare prealabilă către echipa de dezvoltare.

Primul care a observat a fost unul dintre analiștii financiari, care a scris în chat: „Raportul de cifră de afaceri e deja gata? De obicei îl lansez și mă duc să-mi iau cafeaua."

Echipa de dezvoltare a întrebat ce se schimbase. Am explicat analiza, planul suboptimal, mecanismul SPM. A fost o conversație utilă — nu pentru că fix-ul era complicat, ci pentru că a deschis o discuție despre cum să gestionăm interogările critice în mod proactiv, nu doar reactiv.

Consiliul de management a observat îmbunătățirea în raportul săptămânal următor. Nicio intervenție eroică, nicio urgență rezolvată în ultimul moment. Doar o analiză făcută într-o dimineață liniștită, datorită întrebării unui junior curios.

Pietro, la rândul lui, a înțeles ceva ce cărțile nu predau ușor: că a explica un concept cuiva te obligă să îl privești cu ochi diferiți. În timp ce îi arătam planul de execuție, am văzut lentoarea cu aceeași prospețime cu care o vedea el. Fără acea întrebare, probabil aș fi deschis un alt tab și aș fi trecut mai departe.

## Ce rămâne în runbook-ul echipei

După acea dimineață, am adăugat trei practici în runbook-ul echipei:

1. **Revizuire trimestrială a baseline-urilor SPM** pe interogările critice — verificarea că planurile acceptate sunt încă optime față de structura curentă a tabelelor.
2. **Controlul planurilor AWR** înainte și după fiecare colectare masivă de statistici — compararea `plan_hash_value` pentru interogările monitorizate.
3. **Procedura de încărcare baseline pre-upgrade** — înainte de orice upgrade sau patch Oracle, interogările critice sunt identificate și planurile lor curente sunt încărcate în baseline ca plan de rezervă.

SPM nu elimină munca de tuning. Elimină surpriza: acea dimineață în care ajungi la birou și descoperi că o interogare critică a încetat să funcționeze ca ieri, fără ca nimeni să fi atins nimic.

## Surse oficiale

1. Oracle Database SQL Tuning Guide 19c — [Managing SQL Plan Baselines](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlad/managing-sql-plan-baselines.html)
2. Oracle Database PL/SQL Packages and Types Reference 19c — [DBMS_SPM](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SPM.html)
3. Oracle Database Reference 19c — [OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/OPTIMIZER_CAPTURE_SQL_PLAN_BASELINES.html)
4. Oracle-Base (Tim Hall) — [SQL Plan Management (SPM) in Oracle Database](https://oracle-base.com/articles/11g/sql-plan-management-11gr1)

## Glosar
- **[SQL Plan Management (SPM)](/ro/glossary/sql-plan-management/)** — Funcționalitate a Oracle Database care permite controlul și stabilizarea planurilor de execuție ale interogărilor printr-un repository de planuri aprobate (baseline), prevenind regresiile de performanță cauzate de variațiile optimizer-ului.

- **[SQL Plan Baseline](/ro/glossary/awr/)** — Set de unul sau mai multe planuri de execuție acceptate pentru un SQL statement specific, stocat în repository-ul SPM. Optimizer-ul utilizează doar planurile prezente în baseline, ignorând planurile alternative neverificate.

- **[Plan fixed](/ro/glossary/hash-join/)** (SPM) — Plan de execuție marcat cu atributul `FIXED = YES` în SQL Plan Baseline. Are prioritate absolută față de toate celelalte planuri din baseline: optimizer-ul îl selectează întotdeauna, indiferent de eventualele planuri alternative găsite.

- **[AWR](/ro/glossary/sql-plan-management/)** (Oracle) — Automatic Workload Repository: snapshot-uri periodice de metrici de workload, baza rapoartelor AWR și a ADDM. Păstrează istoricul planurilor de execuție prin `DBA_HIST_SQLSTAT`, util pentru identificarea variațiilor de plan în timp.

- **[Hash Join](/ro/glossary/sql-plan-baseline/)** — Algoritm de join utilizat de optimizer-ul Oracle pentru a uni două tabele construind o hash table în memorie pe tabela mai mică și scanând tabela mai mare. Eficient pentru seturi mari de date fără indecși selectivi; costisitor când este aplicat înainte de filtrele selective.
