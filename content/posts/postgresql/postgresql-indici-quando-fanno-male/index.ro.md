---
title: "Când un index face mai mult rău decât bine: curățarea PostgreSQL de risipă"
description: "Baza de date centrală a unui Minister, un tabel cu 15 indici dintre care 8 nefolosiți, un junior care voia să înțeleagă tot. Curățarea care a readus interogările pe linia dreaptă, povestită ca și cum ar fi fost ieri."
date: "2026-05-26T08:03:00+01:00"
draft: false
translationKey: "postgresql_indici_quando_fanno_male"
tags: ["indexes", "b-tree", "gin", "gist", "performance", "tuning", "query-tuning"]
categories: ["postgresql"]
image: "postgresql-indici-quando-fanno-male.cover.jpg"
---

Zilele trecute un coleg mi-a scris: "Am un tabel cu douăsprezece indexuri, e foarte lent. Nu înțeleg." I-am răspuns două rânduri, dar în timp ce reciteam mi-a venit în minte Marco. Era acum câțiva ani, lucram la baza de date centrală a unui Minister — nu contează care, modelul îl găsești peste tot. Iar Marco era junior-ul pe care mi-l alocaseră.

Avea doi ani și jumătate de PostgreSQL în spate, știa să scrie interogări decente, cunoștea `EXPLAIN`. Dar mai presus de toate avea acea calitate care în meseria asta te duce departe: întreba. Nu din lene — din dorința de a ști. Reformula conceptele cu voce tare ca să le fixeze, lua notițe, anticipa următoarea întrebare cu chestii de genul "stai, deci dacă fac X mă aștept la Y, corect?". Junior-ul pe care orice senior și-l dorește alături când se deschide pe ecran un tabel care sperie.

Ziua aceea am deschis unul.

## Tabelul care speria

Se numea `cittadini_servizi` (`cetateni_servicii`). Nu e numele real — dar modelul este.

Optzeci de milioane de rânduri. O coloană `cittadino_id`, o coloană `servizi_attivi` care era un array de coduri (un cetățean putea avea mai multe servicii active: stare civilă, fiscal, sanitar, școlar, fiecare cu codul său numeric), o geometrie cu rezidența, un boolean `attivo`, câteva date, niște metadata. Nimic exotic.

Deasupra stăteau **cincisprezece indexuri**.

Marco le-a numărat încet, derulând `\d cittadini_servizi`. "Cincisprezece. Cam multe, nu?"

"Depinde. Sunt folosite?"

"De unde să știu?"

Și de aici a început.

## Diagnosticul în cinci minute

PostgreSQL ține socoteala câte ori a fost folosit fiecare index. View-ul se numește `pg_stat_user_indexes`. Marco nu îl deschisese niciodată.

```sql
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'cittadini_servizi'
ORDER BY idx_scan ASC;
```

Output-ul a ieșit brutal. Opt indexuri cu `idx_scan = 0`. Niciodată — folosite — măcar — o — dată.

Marco s-a uitat la ecran. "Niciodată? Nici măcar din greșeală?"

"Niciodată. `idx_scan` pleacă de la zero la pornirea bazei de date și crește de fiecare dată când planner-ul alege acel index. Dacă după săptămâni de producție e încă la zero, planner-ul nu l-a considerat util niciodată."

"Atunci le ștergem și gata."

"Stai. Întâi trebuie să înțelegem de ce sunt acolo."

Fraza aceea — nu șterge nimic înainte să fi înțeles de ce există — e regula de aur când aterizezi pe un sistem pe care nu l-ai construit tu. Acele `CREATE INDEX` cineva le scrisese. Poate avea un motiv. Poate credea că are. Poate nu avea unul deloc. Cine știe.

Marco a încuviințat și a deschis git log-ul repo-ului de DDL.

## "Dar dacă sunt deja 15 indexuri, de ce e lent?"

Întrebare bună. Premisă greșită.

Pentru că pleacă de la presupunerea că "mai multe indexuri = mai rapid", care e unul dintre miturile cele mai persistente din primii ani de PostgreSQL. Realitatea e că un index folosește doar dacă planner-ul îl alege, iar planner-ul alege doar indexurile care sunt de **tipul potrivit** pentru interogarea pe care o evaluează.

Am deschis una dintre interogările critice, una dintre cele pe care monitoring-ul le marca lente:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT cittadino_id
FROM cittadini_servizi
WHERE servizi_attivi && ARRAY[42, 71]
  AND attivo = true;
```

Operatorul `&&` înseamnă "intersecție de array-uri": adu-mi cetățenii care au cel puțin unul dintre serviciile 42 sau 71 active. O interogare pe care business-ul o cerea des, pentru campanii țintite.

Timp: **8.4 secunde**. Plan: `Seq Scan on cittadini_servizi`. Filter: toate cele 80 de milioane de rânduri.

"Dar exista un index pe `servizi_attivi`!"

"Există! E un B-tree. Și B-tree-ul nu știe ce să facă cu `&&`."

## Când e suficient B-tree-ul — și când nu

**B-tree** este indexul pe care 90% dintre dezvoltatori îl cunosc și îl folosesc. E un arbore echilibrat care ordonează valorile. Funcționează excelent pentru egalitate (`WHERE col = 'x'`), pentru intervale (`WHERE col BETWEEN ... AND ...`), pentru sortare (`ORDER BY col`), pentru `LIKE` cu prefix (`WHERE col LIKE 'ABC%'`).

Nu funcționează în schimb pe:
- Operatori de array (`&&`, `<@`, `@>`)
- Căutări de subșir (`LIKE '%x%'`)
- Containment de JSONB (`@>`)
- Intervale geometrice (`&&` pe geometrii, distanțe, bounding box)

Pentru asta sunt necesare alte tipuri.

"Și noi avem array-ul de servicii sub un B-tree."

"Exact. E ca și cum ai avea o arhivă pe hârtie ordonată după CNP și i-ai cere arhivarului să-ți găsească toate dosarele care conțin un anumit cuvânt cheie înăuntru. Ordinea nu ajută."

"Deci avem nevoie de alt tip de index."

"Avem nevoie de GIN."

## GIN: inversul B-tree-ului

GIN vine de la *Generalized Inverted Index*. Invers, pentru că în loc să indexeze rândurile după valoarea coloanei, indexează fiecare element din interiorul coloanei și ține o listă de rânduri care îl conțin.

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi);
```

`USING GIN` e cheia. PostgreSQL construiește un mapping: pentru fiecare cod de serviciu, o listă de rânduri care îl au în array. Când vine interogarea cu `&&`, indexul intersectează listele celor două valori căutate și returnează unirea. Fără seq scan.

Aceeași interogare, după:

```
Bitmap Index Scan on idx_cittadini_servizi_attivi_gin
  ...
Execution Time: 240 ms
```

De la 8400 la 240 milisecunde. Un factor 35.

Marco a sărbătorit pe șoptite. Apoi: "Dacă e atât de puternic, de ce nu se folosește mereu?"

"Pentru că la scriere te costă scump. Fiecare `INSERT` sau `UPDATE` pe acea coloană trebuie să actualizeze toate posting-urile unde apare valoarea respectivă. E prețul găsirii rapide — iar tabelele cu mult churn îl plătesc scump."

"Deci GIN da, dar doar dacă tabelul e predominant de citire."

"Exact. `cittadini_servizi` al nostru primea încărcări nocturne și apoi toată ziua doar citiri. Caz ideal."

## GiST: pentru când datele au o formă

Cealaltă interogare critică era pe geometrii. Ministerul făcea analize teritoriale: "găsește-mi toți cetățenii cu rezidența la 5 km de punctul X, în județul Y, activi". O interogare de genul ăsta, cu un B-tree spațial fals (pentru că cineva pusese unul, dar pe acea coloană nu era utilizabil), mergea în nested loop și dura jumătate de minut.

GiST — *Generalized Search Tree* — este familia de indexuri care gestionează date cu geometrie, intervale, similaritate. Nu ordonează valorile liniar, pentru că unele date nu sunt sortabile liniar (un punct pe plan nu vine "înaintea" sau "după" altul). Indexează în schimb prin *bounding box-uri* ierarhice.

"Stai, dar de ce nu un B-tree compus pe `(latitudine, longitudine)`?"

Întrebare bună. Marco prinsese punctul cheie.

"Pentru că B-tree-ul compus ordonează întâi după latitudine și apoi după longitudine. Dacă trebuie să găsești puncte într-un dreptunghi `(lat1, lon1, lat2, lon2)`, indexul reușește să folosească restricția pe latitudine — dar apoi pe fiecare rând care trece de filtrul lat trebuie să verifice și lon. Pe 80 de milioane de rânduri devine o jumătate de scanare."

"Și GiST?"

"GiST organizează punctele după regiuni geografice. Când cauți un dreptunghi, elimină regiuni întregi cu o comparație de bounding box. E făcut pentru acel tip de interogare."

```sql
CREATE INDEX idx_cittadini_residenza_gist
ON cittadini_servizi USING GIST (residenza);
```

Aceeași interogare "găsește toți la 5 km de X", de la 28 de secunde la 380 ms.

Marco lua notițe rapid. "Deci: B-tree pentru sortare și egalitate, GIN pentru containment de array și JSONB, GiST pentru geometrie și intervale. Mai e ceva?"

"Pentru moment ajunge. Există BRIN, SP-GiST, hash, dar sunt cazuri mai de nișă. Când o să ai nevoie de ele, o să-ți amintești."

## Bonus: indexurile parțiale

Mai era un ultim lucru, înainte de a reveni la întrebarea inițială (ce indexuri de aruncat). Cetățenii "activi" erau circa 35% din total. Tot restul era istoric, dosare închise, arhivate. Interogările operative filtrau mereu pe `attivo = true`.

"Deci fiecare index conține 65% de rânduri care nu se caută niciodată."

"Exact. Risipă de spațiu și de muncă pentru VACUUM. Soluția: index parțial."

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi)
WHERE attivo = true;
```

Acel `WHERE` schimbă tot. Indexul conține doar rândurile active. Pe datele reale, spațiul ocupat s-a redus la jumătate, iar viteza s-a îmbunătățit cu încă 15-20% pentru că indexul era mai mic de parcurs.

"Și interogările cu `attivo = false`?"

"Merg în seq scan, dar se întâmplă o dată pe săptămână pentru rapoartele din arhivă. Acolo seq scan-ul merge perfect."

## Curățarea

În punctul ăsta aveam:

- Înțeles de ce 8 indexuri nu erau folosite (erau duplicate ale altora, sau B-tree pe coloane unde planner-ul prefera un seq scan, sau resturi de interogări care nu mai existau)
- Înlocuit 2 B-tree-uri inadecvate cu un GIN și un GiST
- Transformat 2 indexuri "complete" în indexuri parțiale

Rezultat net:

| Element | Înainte | După |
|---------|--------:|-----:|
| Indexuri totale | 15 | 7 |
| Spațiu indexuri | 42 GB | 18 GB |
| Timp mediu interogări operative | 4.1 s | 0.4 s |
| Timp INSERT batch nocturn | 38 min | 22 min |

Marco s-a uitat la tabel, apoi la mine. "Adică am îmbunătățit atât citirea cât și scrierea, pur și simplu eliminând lucruri."

"Și punând cele trei potrivite la locul potrivit. Dar da, mai ales eliminând. Fiecare index e un cost. La fiecare DML. Pentru totdeauna."

## Fraza pe care i-am repetat-o de trei ori

În ziua aceea i-am spus același lucru în trei feluri diferite, pentru că voiam să o ducă cu el:

> Când te gândești la un index de creat pe un tabel, nu te gândi "hai să mai pun unul, oricum nu strică". Un index e un cost permanent pe fiecare `INSERT`, `UPDATE`, `DELETE` — mai mult disc, mai mult WAL, mai mult VACUUM, mai multă contention. Îl creezi doar dacă e cu adevărat necesar. Și dacă există și nu e necesar, dispare.

Marco l-a notat în caietul lui. Ani mai târziu a devenit el senior pe alt proiect. Mi-a sosit un mesaj într-o zi: *"Mi-a picat un tabel cu douăzeci și două de indexuri. Opt la zero. Am făcut curățenia. M-am gândit la tine."*

Asta e cel mai frumos lucru pe care ți-l poate spune un junior.

------------------------------------------------------------------------

## Glosar

**[B-tree](/ro/glossary/b-tree/)** — Structura de arbore echilibrat folosită pentru majoritatea indexurilor. Funcționează excelent pentru egalitate, intervale și sortare. Nu știe să gestioneze array-uri, subșiruri interne, geometrii.

**[GIN Index](/ro/glossary/gin-index/)** — *Generalized Inverted Index*. Indexează elemente individuale din interiorul valorilor compuse (array-uri, JSONB, full-text). Rapid la citire pentru interogări de containment, lent la scriere pe tabele cu mult churn.

**[GiST Index](/ro/glossary/gist-index/)** — *Generalized Search Tree*. Indexează date cu structură geometrică sau de intervale folosind bounding box-uri ierarhice. Indispensabil pentru geometrii, intervale temporale, similaritate.

**[pg_stat_user_indexes](/ro/glossary/pg-stat-user-indexes/)** — View de sistem PostgreSQL care urmărește de câte ori a fost folosit fiecare index (`idx_scan`). Instrumentul principal pentru identificarea indexurilor inutile în producție.

**[Index Parțial](/ro/glossary/indice-parziale/)** — Index care acoperă doar o submulțime din rândurile tabelului, definit cu `WHERE` în `CREATE INDEX`. Reduce spațiul și timpul de mentenanță când interogările filtrează sistematic pe o condiție.
