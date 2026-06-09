---
title: "Replica logica in PostgreSQL: le domande di un collega che chiariscono l'argomento"
date: 2099-12-31
draft: true
section: postgresql
webo_status: da_tradurre
webo_generated_at: 2026-06-08
---

## Un însoțire care nu era o lecție

Claudio era acolo ca să observe, nu să învețe în sens formal. Însoțirea era muncă reală: un sistem de gestionare a daunelor și polițelor în producție, un mare grup de asigurări italian, și necesitatea concretă de a migra de la PostgreSQL 13 la PostgreSQL 15 fără a întrerupe operațiunile. În paralel, echipa de analiză a fraudelor aștepta un flux de date spre data warehouse pentru a-și alimenta propriile modele.

Nu era contextul ideal pentru a explica replica logică de la zero. Totuși, Claudio a pus exact întrebările pe care le-ar pune oricine pentru prima dată — și a răspunde la acele întrebări cu voce tare, într-un mod care să reziste, a consolidat fiecare alegere pe care o făcusem deja în tăcere.

Acest articol urmează acea secvență: mai întâi întrebările, apoi conceptele, apoi configurarea concretă.

---

## Replicare fizică și replicare logică: dilema inițială

Prima întrebare a lui Claudio a venit înainte să deschidem un terminal: «De ce nu folosim replicarea fizică? Nu asta se folosește de obicei?»

Este întrebarea corectă. Replicarea fizică — streaming replication — este alegerea consacrată pentru înaltă disponibilitate și disaster recovery. Funcționează la nivel de bloc: serverul primar transmite WAL-urile (Write-Ahead Log) către replică, care le aplică identic. Rezultatul este o copie byte cu byte a clusterului. Simplu de configurat, fiabil, bine documentat [1].

Limita este exact forța sa: replică *totul*, în același format, la aceeași versiune de PostgreSQL. Nu poți replica doar anumite tabele. Nu poți replica spre o versiune diferită a motorului. Nu poți folosi replica ca sursă pentru un sistem extern care vorbește un protocol diferit.

Replicarea logică operează la nivel de rând, nu de bloc. Publisher-ul decodifică modificările din WAL-uri și le transmite ca operații logice — `INSERT`, `UPDATE`, `DELETE` — spre unul sau mai mulți subscriberi. Asta deschide trei posibilități pe care replicarea fizică nu le oferă:

- replicarea unui subset de tabele sau rânduri
- replicarea între versiuni diferite de PostgreSQL (din versiunea 10 în sus, cu limitări)
- alimentarea sistemelor eterogene precum data warehouse sau message broker prin Change Data Capture (CDC)

În cazul nostru, toate cele trei necesități erau prezente simultan.

---

## Cele trei scenarii și întrebările lui Claudio

### Migrare cross-versiune fără downtime

«Dar nu pot face un `pg_upgrade`?» a întrebat Claudio, privind documentația pe monitorul din față.

Da, `pg_upgrade` funcționează. Dar necesită oprirea sistemului, executarea upgrade-ului, verificarea, și abia apoi redeschiderea traficului. Cu 100 de milioane de rânduri în `claim_events.claims` și 300 de milioane în `claim_events.claim_details`, timpul de inactivitate ar fi fost de ordinul orelor — inacceptabil pentru un sistem care gestionează lichidări active.

Replicarea logică permite o abordare diferită: se pregătește noul cluster PostgreSQL 15 (`pg-claims-new-01`), se alimentează prin subscription, și când lag-ul de replicare se reduce la secunde se execută switchover-ul. Downtime-ul se reduce la timpul necesar pentru redirecționarea conexiunilor — minute, nu ore.

### Integrare CDC spre data warehouse

«E ca un trigger distribuit?» a întrebat Claudio, cu o anumită satisfacție pentru analogie.

Nu — și diferența este substanțială. Un trigger se execută în tranzacție, adaugă latență și scalează prost la volume mari. Replicarea logică citește WAL-urile *după* ce tranzacția a fost deja confirmată: niciun impact pe calea critică a scrierilor, niciun lock suplimentar, niciun overhead pe publisher în afara decodificării WAL.

Pentru echipa antifraudă, necesitatea era să primească în timp aproape real noile cereri de despăgubire (`fraud_detection_audit.new_claims_for_analysis`) pe `pg-dw-subscriber-01`. Publication dedicată `fraud_audit_pub` a rezolvat exact această cerință, fără a atinge logica aplicativă.

### Replicare selectivă

«Și dacă vreau doar datele clienților activi?» a întrebat Claudio, gândindu-se deja la un caz de utilizare viitor.

Aici răspunsul este mai articulat. Replicarea logică permite selectarea tabelelor de inclus într-o publication. Începând cu PostgreSQL 15, este posibil să adaugi și o clauză `WHERE` pentru filtrarea rândurilor [2]. Limitarea principală privește DDL-urile: modificările de schemă nu se replică automat — punct la care revin în secțiunea despre monitorizare.

---

## Concepte cheie: publication, subscription și slot de replicare

Înainte de a trece la configurare, trei concepte de reținut.

**Publication** — definește *ce* se replică pe publisher. Poate include tabele specifice, toate tabelele dintr-o bază de date (`FOR ALL TABLES`), sau — din versiunea 15 — secvențe. Fiecare publication are un nume și poate fi referențiată de mai mulți subscriberi.

**Subscription** — definește *cine* primește datele și *de unde*. Subscription-ul se creează pe subscriber și specifică șirul de conexiune la publisher și numele publication-ului la care se abonează. La momentul creării, PostgreSQL execută o copie inițială a datelor (initial snapshot) și apoi aplică modificările ulterioare în streaming.

**Slot de replicare logică** — este mecanismul care garantează persistența. Publisher-ul păstrează segmentele WAL necesare până când subscriberul le-a consumat. Acest lucru este fundamental pentru consistență, dar introduce un risc: dacă un subscriber se deconectează pentru mult timp, WAL-urile se acumulează și spațiul pe disc al publisher-ului poate fi epuizat. Monitorizarea slot-urilor este obligatorie în producție.

---

## Configurare practică

### Publisher: `pg-claims-primary-01` (PostgreSQL 13.10)

Cel mai important parametru este `wal_level`, care trebuie setat la `logical`. Ceilalți parametri dimensionează resursele pentru slot-uri și worker-i.

```sql
-- Pe pg-claims-primary-01
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = '10';
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();
```

`wal_level = 'logical'` necesită un restart al serverului pentru a fi activ. Ceilalți parametri pot fi aplicați cu `pg_reload_conf()`, dar este bine să verifici valorile efective după reload:

```sql
SHOW wal_level;
SHOW max_replication_slots;
```

După restart, se creează publication-urile. Pentru migrare, tabelele principale:

```sql
CREATE PUBLICATION claims_pub
  FOR TABLE insurance_policies.policies,
             claim_events.claims;
```

Pentru integrarea cu data warehouse, o publication separată și dedicată:

```sql
CREATE PUBLICATION fraud_audit_pub
  FOR TABLE fraud_detection_audit.new_claims_for_analysis;
```

Separarea publication-urilor pe caz de utilizare este o alegere deliberată: permite gestionarea permisiunilor, monitorizării și ciclului de viață în mod independent.

**Utilizator de replicare** — subscriberul se conectează cu un utilizator dedicat care trebuie să aibă rolul `REPLICATION` și permisiunile `SELECT` pe tabelele publicate:

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '...';
GRANT SELECT ON insurance_policies.policies TO replicator;
GRANT SELECT ON claim_events.claims TO replicator;
GRANT SELECT ON fraud_detection_audit.new_claims_for_analysis TO replicator;
```

Verifică și că `pg_hba.conf` permite conexiunea de la IP-ul subscriberului cu metoda de autentificare corespunzătoare (preferabil `scram-sha-256`).

### Subscriber pentru migrare: `pg-claims-new-01` (PostgreSQL 15.3)

```sql
-- Pe pg-claims-new-01
ALTER SYSTEM SET max_worker_processes = '10';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION claims_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION claims_pub;
```

La momentul `CREATE SUBSCRIPTION`, PostgreSQL pornește snapshot-ul inițial: copiază toate rândurile existente din tabelele publicate, apoi trece la replicarea modificărilor în streaming. Cu 150 de milioane de rânduri între `policies` și `claims`, acest snapshot a necesitat câteva ore — planificat într-un moment de activitate redusă.

### Subscriber pentru data warehouse: `pg-dw-subscriber-01` (PostgreSQL 15.3)

```sql
-- Pe pg-dw-subscriber-01
ALTER SYSTEM SET max_worker_processes = '5';
SELECT pg_reload_conf();

CREATE SUBSCRIPTION fraud_audit_sub
  CONNECTION 'host=pg-claims-primary-01 port=5432 user=replicator password=...'
  PUBLICATION fraud_audit_pub;
```

---

## Monitorizare și troubleshooting

«Cum știu dacă funcționează?» — cea mai utilă întrebare a lui Claudio.

### Lag de replicare

Vista `pg_replication_slots` pe publisher arată starea slot-urilor active și volumul de WAL reținut:

```sql
SELECT
  slot_name,
  active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS replication_lag_bytes
FROM pg_replication_slots
WHERE slot_type = 'logical';
```

Un `replication_lag_bytes` în creștere constantă semnalează un subscriber în dificultate. Dacă `active` este `false` și lag-ul continuă să crească, slot-ul acumulează WAL-uri fără să le consume: situație de rezolvat rapid.

Pe subscriber, `pg_stat_subscription` și `pg_stat_subscription_stats` arată starea aplicării:

```sql
SELECT
  subname,
  subenabled,
  subconninfo,
  subslotname,
  substate,
  subbinary
FROM pg_subscription;

SELECT
  subid,
  relid,
  last_applied_lsn,
  last_received_lsn,
  pg_wal_lsn_diff(last_received_lsn, last_applied_lsn) AS apply_lag_bytes
FROM pg_stat_subscription_stats;
```

`apply_lag_bytes` măsoară întârzierea dintre ceea ce subscriberul a primit și ceea ce a aplicat efectiv. O valoare stabilă și mică indică un sistem sănătos.

### Conflicte și primary key

Cel mai frecvent conflict în replicarea logică este violarea de primary key: subscriberul primește un `INSERT` pentru un rând care există deja local. Asta se întâmplă de obicei când subscriberul are date preexistente nealiniate cu publisher-ul.

PostgreSQL înregistrează conflictele în log-ul subscriberului cu mesaje de tipul:

```
ERROR: duplicate key value violates unique constraint "claims_pkey"
```

Replicarea se oprește până la rezolvare. Opțiunile sunt: eliminarea rândului conflictual pe subscriber, sau folosirea `ALTER SUBSCRIPTION ... SKIP` pentru a sări tranzacția problematică (cu conștiința implicațiilor asupra consistenței).

### Gestionarea DDL-urilor

«Dacă adaug o coloană pe publisher, subscriberul o vede?» a întrebat Claudio, și răspunsul a necesitat o pauză.

Nu — nu automat. Replicarea logică transportă datele, nu modificările de schemă. Dacă adaugi o coloană `NOT NULL` fără default pe publisher, replicarea se oprește pentru că subscriberul nu știe unde să pună valoarea.

Procedura corectă este:

1. Adaugă coloana pe subscriber înainte de publisher (cu un default sau ca `NULL`)
2. Adaugă coloana pe publisher
3. Verifică că replicarea reia corect

Pentru modificări de schemă frecvente sau complexe, instrumente precum `pg_logical` sau soluții CDC dedicate (Debezium, pgoutput cu consumatori externi) oferă gestionare mai sofisticată. În acest proiect, DDL-urile erau rare și planificate: procedura manuală era suficientă.

---

## Bune practici și considerații operaționale

**Spațiu WAL** — dimensionează `max_slot_wal_keep_size` (disponibil din versiunea 13) pentru a limita acumularea de WAL-uri în cazul subscriberilor inactivi. Fără acest parametru, un subscriber deconectat poate epuiza spațiul pe disc al publisher-ului.

**Securitate** — folosește întotdeauna `scram-sha-256` în `pg_hba.conf` pentru conexiunile de replicare. Evaluează SSL obligatoriu adăugând `sslmode=require` în șirul de conexiune al subscription-ului. Nu folosi utilizatorul `postgres` pentru replicare.

**Slot-uri orfane** — un slot de replicare care nu mai este utilizat dar nu a fost eliminat continuă să rețină WAL-uri. Monitorizează periodic `pg_replication_slots` și elimină slot-urile obsolete cu `SELECT pg_drop_replication_slot('nume_slot')`.

**Tabele fără primary key** — replicarea logică în modul `UPDATE` și `DELETE` necesită o primary key sau o replica identity configurată (`REPLICA IDENTITY FULL` ca alternativă, cu impact asupra performanței). Verifică toate tabelele înainte de a crea publication-ul.

**Switchover final** — în cazul migrării, momentul critic este tăierea: se dezactivează scrierea pe publisher (sau se redirecționează traficul), se așteaptă ca lag-ul să scadă la zero, se verifică consistența, se promovează noul cluster. Cu lag-ul monitorizat în zilele precedente și stabil sub 500ms, switchover-ul a necesitat mai puțin de trei minute.

---

## Întrebările lui Claudio

Sistemul a intrat în producție fără probleme. Nu a existat o situație de ultimă oră, nu a existat un moment de tensiune de povestit. Noul cluster PostgreSQL 15 a preluat traficul, data warehouse-ul a continuat să primească datele antifraudă, și grupul de asigurări și-a avut upgrade-ul fără ferestre de mentenanță vizibile utilizatorilor.

Claudio are o înțelegere mai concretă a ceea ce a observat. Eu am o înțelegere mai articulată a ceea ce știu — pentru că a trebuit să găsesc cuvintele potrivite, nu doar comenzile potrivite. A explica diferența dintre replicarea fizică și cea logică cuiva care nu o cunoaște înseamnă să o înțelegi suficient de bine pentru a alege exemplul corect, nu doar cel tehnic exact.

Întrebările lui Claudio nu au schimbat alegerile tehnice. Le-au consolidat.

---

## Surse oficiale

[1] PostgreSQL Documentation — [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — concepte generale, arhitectură, diferențe față de replicarea fizică.

[2] PostgreSQL Documentation — [CREATE PUBLICATION](https://www.postgresql.org/docs/current/sql-create-publication.html) — sintaxă completă, opțiuni de filtrare pe rând (PostgreSQL 15+), gestionarea secvențelor.

[3] PostgreSQL Documentation — [CREATE SUBSCRIPTION](https://www.postgresql.org/docs/current/sql-create-subscription.html) — sintaxă, opțiuni de conexiune, gestionarea snapshot-ului inițial.

[4] PostgreSQL Documentation — [Monitoring — pg_stat_replication_slots](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-SLOTS-VIEW) — viste de sistem pentru monitorizarea slot-urilor.

[5] PostgreSQL Documentation — [Replication Slots](https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS) — mecanismul slot-urilor, riscuri de acumulare WAL, `max_slot_wal_keep_size`.

---

## Glosar candidat

**Publication** — obiect PostgreSQL care definește mulțimea de tabele (și opțional rânduri, din versiunea 15) ale căror modificări sunt puse la dispoziție pentru replicarea logică. Creat pe publisher cu `CREATE PUBLICATION`, poate fi referențiat de mai mulți subscriberi independenți.

**Subscription** — obiect PostgreSQL creat pe subscriber care stabilește conexiunea la publisher, specifică publication-ul la care se abonează și gestionează ciclul de viață al replicării: snapshot inițial, streaming al modificărilor, reconectare automată.

**Slot de replicare logică** — structură persistentă pe publisher care urmărește poziția de consum a WAL-urilor pentru fiecare subscriber. Garantează că nicio modificare nu se pierde în caz de deconectare temporară, cu costul reținerii segmentelor WAL până la consum.

**WAL (Write-Ahead Log)** — registru secvențial al tuturor modificărilor aplicate bazei de date PostgreSQL, scris înainte ca modificările să fie aplicate fișierelor de date. Este sursa din care replicarea logică extrage operațiile de transmis subscriberilor prin procesul de decodificare logică.

**CDC (Change Data Capture)** — tehnică care interceptează și transmite în timp aproape real modificările datelor dintr-o sursă spre sisteme destinatare (data warehouse, message broker, aplicații). Replicarea logică a PostgreSQL implementează CDC nativ prin protocolul `pgoutput`.
