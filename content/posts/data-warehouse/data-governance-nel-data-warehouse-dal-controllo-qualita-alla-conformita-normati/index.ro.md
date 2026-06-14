---
categories:
- data-warehouse
date: '2026-07-07'
draft: false
image: data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati.cover.jpg
tags: []
title: La pausa pranzo che ha rimandat o il go-live:Data Governance nel DWH
translationKey: data_governance_nel_data_warehouse_dal_controllo_qualita_alla_conformita_normati
webo_generated_at: 2026-06-14
webo_status: scheduled
---

```
---
title: "Masa din fața biroului: ce lipsește dintr-un DWH 'gata' înainte de go-live"
seoTitle: "Data governance DWH asigurări: TDE, Data Catalog, ownership"
description: "Ce nu include un Data Warehouse tehnic funcțional: ownership, calitate continuă, TDE Oracle 19c, Data Catalog. Un caz real din sectorul asigurărilor."
tags: ["data-governance", "data-warehouse", "oracle-19c", "data-quality", "gdpr"]
---
```

## Masa din fața biroului

Era una din acele zile de sfârșit de primăvară în care mănânci afară, în sfârșit. Carlo — senior data analyst la un mare grup de asigurări italian cu care colaborez de vreo doi ani — era vizibil mulțumit. DWH-ul era tehnic pregătit: datele încărcate, modelul dimensional ținea, primele query-uri pe rapoarte funcționau. Se gândea deja cum să prezinte succesul managerilor săptămâna viitoare.

«Aș zice că suntem pregătiți pentru go-live», mi-a spus, tăind pizza.

Am așteptat o secundă înainte să răspund. Nu pentru că voiam să-i temperez entuziasmul — munca făcută era solidă — ci pentru că acea frază, «suntem pregătiți», ascundea o serie de întrebări pe care nimeni nu le pusese încă cu voce tare. Iar gap-urile de governance care apar după go-live sunt aproape întotdeauna interpretate de manageri ca neatenție, nu ca complexitate intrinsecă a proiectului.

«Tehnic, da», am spus. «Dar ai răspuns deja la: cine este data owner-ul lui `policy_holder_data`? Ce se întâmplă dacă un raport arată o primă anormală — cine o corectează și în cât timp? Și GDPR-ul, cum îl gestionăm la nivel de storage?»

Carlo a pus furculița jos.

Conversația aceea a durat până la cafea, apoi a continuat în fața PC-ului după-amiaza. Articolul de față este încercarea de a pune în scris ce ne-am spus.

---

## Ce nu include un DWH „gata" în mod implicit

Un Data Warehouse tehnic funcțional — ETL care rulează, dimensiuni populate, fapte agregate corect — este o condiție necesară, dar nu suficientă pentru a merge în producție într-un context enterprise. Mai ales în sectoare reglementate precum cel al asigurărilor, unde datele includ date de identificare ale clienților, istoricul polițelor, plăți și — în unele produse — date medicale.

Așteptările implicite pe care managerii și utilizatorii de business le aduc în sala de ședințe în ziua go-live-ului privesc cel puțin patru domenii care apar rareori în cerințele funcționale inițiale.

### Calitatea datelor: nu e un control, e un proces

Calitatea datelor nu este o bifă de pus înainte de punerea în producție. Este un proces continuu. În DWH-ul de asigurări pe care îl discutam, tabelele `claims_history` și `premium_payments` veneau din sisteme sursă cu calitate eterogenă: unele companii din grup aveau codificări diferite pentru același tip de daună, câmpuri dată cu formate inconsistente, valori nule în coloane care ar fi trebuit să fie obligatorii.

În timpul încărcării implementasem deja câteva reguli de validare în ETL. Dar «a valida la intrare» și «a garanta calitatea în timp» sunt două lucruri diferite. Sunt necesare:

- **Praguri de alertă**: dacă numărul de înregistrări respinse la o încărcare depășește 2%, cineva trebuie să știe înainte ca rapoartele să fie distribuite
- **Procese de remediere**: cine corectează datele anormale? Cu ce prioritate? Cu ce urmă de audit?
- **Monitorizare longitudinală**: o dată care era corectă acum șase luni s-ar putea să nu mai fie dacă regulile de business se schimbă

Carlo gestionase validarea la intrare. Monitorizarea continuă și procesele de remediere rămâneau de definit.

### Ownership: întrebarea incomodă

«Cine este data owner-ul lui `policy_holder_data`?» întrebasem la prânz.

Carlo răspunsese: «Păi, IT-ul.»

Acest răspuns este aproape întotdeauna greșit — sau cel puțin incomplet. IT-ul gestionează infrastructura și procesele tehnice, dar data-ul aparține business-ului. Într-un context de asigurări, data owner-ul unei tabele cu date de identificare și contractuale ale clienților ar trebui să fie o funcție de business (de exemplu, direcția comercială sau compliance), nu echipa tehnică.

Distincția dintre **Data Owner** (responsabilitate de business asupra datei), **Data Steward** (gestionarea operațională a calității și regulilor) și **Data Custodian** (gestionarea tehnică a infrastructurii) nu este birocrație. Este răspunsul practic la întrebarea «pe cine sun când această dată este greșită?». Fără această hartă, fiecare anomalie devine o ședință de trei ore pentru a stabili al cui este problema.

### Glosarul de date: când „primă" nu înseamnă același lucru pentru toți

În grupul de asigurări, termenul «primă» avea cel puțin trei definiții operaționale diferite în funcție de business unit. DWH-ul le consolidase într-o singură coloană `premium_amount` în tabela `premium_payments`, dar fără a documenta ce definiție fusese adoptată și de ce.

Un glosar de date comun — chiar și în forma cea mai simplă, un document versionat cu definițiile agreate între business și IT — face diferența dintre un raport care generează încredere și unul care generează discuții. Nu e nevoie de un instrument enterprise de sute de mii de euro: e nevoie de o definiție scrisă, agreată, accesibilă.

### Data Lineage: trasabilitatea care salvează auditurile

«Dacă un analist de risk management întreabă de unde vine acest număr», i-am spus lui Carlo deschizând PC-ul, «reușești să-i răspunzi în mai puțin de o oră?»

Tăcere.

Data lineage — capacitatea de a urmări parcursul unei date de la sursă până la raportul final, prin toate etapele de transformare — este esențial în două scenarii: troubleshooting-ul zilnic («de ce s-a schimbat această valoare față de luna trecută?») și auditurile de reglementare («demonstrează-mi că acest agregat este calculat corect conform regulilor X»). Într-un sector precum cel al asigurărilor, al doilea scenariu nu este ipotetic.

---

## GDPR: de la constrângere legală la alegere arhitecturală

Până în acest punct al conversației, Carlo dădea din cap cu aerul celui care recunoaște gap-urile, dar le vede ca «lucruri de adăugat după». Punctul de cotitură a venit cu GDPR-ul.

«GDPR-ul îl gestionăm cu politica de confidențialitate și consimțământul», a spus Carlo. «Compliance-ul este deja acoperit legal.»

«Compliance-ul documentar, da», am răspuns. «Dar GDPR-ul la articolul 32 vorbește explicit despre măsuri tehnice adecvate, inclusiv criptarea. Dacă cineva accesează fizic fișierele bazei de date — un backup furat, un disc scos din uz prost, un acces neautorizat la storage — datele din `policy_holder_data` sunt lizibile în clar?»

Aceasta este diferența dintre compliance formal și implementare arhitecturală. Prima protejează legal organizația atâta timp cât nu se întâmplă nimic. A doua reduce probabilitatea că se întâmplă ceva și reduce impactul dacă se întâmplă.

### Transparent Data Encryption pe Oracle 19c

Oracle Database 19c include Transparent Data Encryption (TDE) [1], o funcționalitate care criptează datele în repaus — fișierele de date, fișierele redo log, backup-urile — fără a necesita modificări ale aplicațiilor. Pentru DWH-ul de asigurări, asta înseamnă că chiar dacă cineva obține acces fizic la fișierele de pe `oracle-dwh-prod-eu-01`, datele rămân ilizibile fără cheia de criptare gestionată de wallet-ul Oracle.

Activarea TDE la nivel de tablespace este relativ simplă:

```sql
-- Crearea wallet-ului și setarea master key (de executat ca SYSDBA)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/wallet' IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "wallet_password" WITH BACKUP;

-- Criptarea tablespace-ului care conține datele sensibile
ALTER TABLESPACE policy_data ENCRYPTION ONLINE USING 'AES256' ENCRYPT;
```

```sql
-- Verificarea stării de criptare a tablespace-urilor
SELECT tablespace_name, encrypted
FROM dba_tablespaces
WHERE encrypted = 'YES';
```

Ce nu face TDE: nu protejează împotriva unui utilizator cu acces SQL legitim la baza de date. Nu este un substitut pentru gestionarea accesurilor și privilegiilor. Este un strat de protecție specific pentru data în repaus — exact ceea ce GDPR-ul consideră o «măsură tehnică adecvată» în contextul protecției împotriva accesurilor fizice neautorizate sau pierderii suporturilor [2].

Conversația cu Carlo s-a mutat pe un punct practic: implementarea TDE înainte de go-live este o operațiune planificabilă cu downtime controlat. Implementarea ei după, pe un sistem în producție cu terabytes de date istorice deja încărcate, este o operațiune mai complexă și mai riscantă. Fereastra de oportunitate era aceea.

---

## Un framework de calitate care rezistă în timp

Revenind la calitatea datelor: ce aveam în funcțiune era o serie de controale în ETL. Ce era necesar era un framework.

Diferența este substanțială. Controalele din ETL blochează sau semnalează înregistrările neconforme la momentul încărcării. Un framework de calitate adaugă:

**Monitorizare proactivă**: job-uri programate care verifică periodic condițiile de calitate pe tabelele deja încărcate. De exemplu, o query care verifică în fiecare dimineață dacă există `policy_holder_data` cu `fiscal_code` nul sau cu format nevalid — date care ar fi putut intra prin căi de încărcare nestandard.

```sql
-- Exemplu de control de calitate programat pe policy_holder_data
SELECT
    COUNT(*) AS anomalii_cod_fiscal,
    SYSDATE AS data_control
FROM policy_holder_data
WHERE fiscal_code IS NULL
   OR NOT REGEXP_LIKE(fiscal_code, '^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$');
```

**Praguri și notificări**: dacă numărul de anomalii depășește un prag definit (de exemplu, mai mult de 50 de înregistrări cu cod fiscal nevalid într-o zi), sistemul notifică Data Steward-ul responsabil înainte ca rapoartele să fie distribuite.

**Urmă de remediere**: fiecare corecție manuală pe date trebuie documentată — cine a corectat, când, de ce, care era valoarea originală. Într-un context de asigurări, această urmă este relevantă atât pentru auditurile interne, cât și pentru eventualele verificări de reglementare.

---

## Data Catalog-ul: unde governance devine navigabil

Un Data Catalog [3] este infrastructura care face navigabil tot ce am discutat până acum. Nu este un instrument opțional pentru echipele mari: este diferența dintre o governance care există doar în documente și una pe care utilizatorii de business reușesc efectiv să o folosească.

În contextul DWH-ului de asigurări, un Data Catalog minim ar trebui să răspundă la aceste întrebări fără a necesita un telefon către echipa tehnică:

- Ce conține tabela `claims_history`? Ce coloane? Cu ce reguli de business?
- De unde vin datele din `premium_payments`? Prin ce transformări?
- Cine este data owner-ul lui `policy_holder_data`? Pe cine contactez dacă găsesc o anomalie?
- Ce tabele conțin date personale supuse GDPR-ului?

Instrumente enterprise precum Apache Atlas, Collibra sau Alation gestionează asta în mod structurat. Pentru un prim go-live, chiar și o soluție mai ușoară — un wiki structurat, un document partajat cu definițiile agreate — este infinit mai bine decât nimic. Important este să existe, să fie actualizat și ca utilizatorii să știe unde să-l găsească.

Integrarea cu glosarul de date este naturală: definițiile agreate (de exemplu, definiția «primei» adoptată în DWH) trăiesc în catalog și sunt referențiate de documentația coloanelor. Lineage-ul, ideal, este vizualizabil din același instrument.

---

## Cine face ce: cele trei roluri care nu pot fi ignorate

Înainte de a încheia conversația cu Carlo, am pus pe hârtie o hartă a rolurilor. Nu ca exercițiu formal, ci ca răspuns practic la întrebarea: când ceva merge prost, pe cine sun?

**Data Owner**: este o figură de business, nu tehnică. Decide regulile de utilizare a datei, aprobă modificările la definiții, este responsabil de calitate din perspectiva business-ului. Pentru `policy_holder_data`, Data Owner-ul natural era direcția de compliance a grupului.

**Data Steward**: este puntea dintre business și IT. Gestionează operațional regulile de calitate, monitorizează anomaliile, coordonează remedierea. Poate fi o figură tehnică cu sensibilitate puternică de business, sau invers. În cazul nostru, Carlo era candidatul natural pentru acest rol pe câteva dintre tabelele cheie.

**Data Custodian**: este echipa tehnică. Gestionează infrastructura, implementează regulile tehnice definite de Data Owner și Data Steward, garantează disponibilitatea și securitatea. Responsabilitatea pentru TDE, backup-uri, accesuri la baza de date — totul este în scope-ul Data Custodian-ului.

Distincția nu este birocrație. Este răspunsul operațional la întrebarea «cine este responsabil de ce». Fără această hartă, fiecare problemă devine o discuție despre cine ar trebui să rezolve problema, în loc de o discuție despre cum să o rezolve.

---

## „Acum știu ce lipsește"

Spre ora cinci după-amiaza, Carlo s-a ridicat de pe scaun și a spus ceva care mi-a rămas în minte: «Okay. Acum știu ce lipsește. Și știu cum să le prezint managerilor fără să pară că am făcut o muncă pe jumătate.»

Aceasta este diferența dintre a ajunge la o ședință de go-live cu gap-urile ascunse și a ajunge cu gap-urile cartografiate și un plan pentru a le închide. Managerii nu se așteaptă la perfecțiune — se așteaptă ca echipa să știe unde se află și unde se îndreaptă.

Am amânat go-live-ul cu trei săptămâni. În acel timp: am definit Data Owner-ii pentru tabelele principale, am implementat TDE pe tablespace-ul care conținea datele personale, am scris un glosar de date minim pentru termenii critici, am configurat primele controale de calitate programate și am schițat structura Data Catalog-ului.

Nu era totul. Dar era suficient pentru a ajunge la ședința cu managerii cu răspunsurile corecte la întrebările corecte. Meritul nu aparținea unei singure intuiții — era al unei conversații sincere între două persoane cu perspective diferite care lucrau spre același obiectiv.

---

## Surse oficiale

1. Oracle Database Security Guide 19c — [Configuring Transparent Data Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-transparent-data-encryption.html)
2. Regulamentul (UE) 2016/679 — [Articolul 32: Securitatea prelucrării](https://eur-lex.europa.eu/legal-content/RO/TXT/?uri=CELEX:32016R0679)
3. DAMA International — [DAMA-DMBOK2: Data Management Body of Knowledge](https://www.dama.org/dama-dm-bok-2) — acoperă Data Governance, Data Quality, Data Lineage, Data Catalog, Data Stewardship

---

## Glosar candidat

- **Data Governance** — Ansamblul de procese, politici, standarde și metrici care asigură utilizarea eficientă a informațiilor, garantând calitatea, integritatea, securitatea și conformitatea normativă a acestora. Nu este un proiect cu o dată de sfârșit: este un framework operațional continuu.

- **Data Lineage** — Capacitatea de a urmări parcursul unei date de la sursă, prin toate sistemele și transformările, până la destinația finală. Esențial pentru troubleshooting, audituri de reglementare și verificarea corectitudinii calculelor.

- **Transparent Data Encryption (TDE)** (Oracle) — Funcționalitate Oracle Database care criptează datele în repaus — fișiere de date, redo log, backup-uri — fără modificări ale aplicațiilor. Protejează împotriva accesurilor fizice neautorizate la suporturile de stocare.

- **Data Quality** — Măsura în care datele sunt exacte, complete, coerente, valide și actuale. Nu este un control unic, ci un proces continuu de monitorizare, alertare și remediere care garantează fiabilitatea analizelor în timp.

- **Data Catalog** — Inventar organizat al tuturor datelor disponibile într-o organizație, cu metadate, glosar, lineage și instrumente de căutare. Face governance navigabil pentru utilizatorii de business fără a necesita intervenție tehnică pentru fiecare întrebare despre date.
