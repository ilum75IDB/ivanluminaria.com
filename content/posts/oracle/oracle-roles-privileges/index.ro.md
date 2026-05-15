---
title: "Utilizatori, roluri și privilegii în Oracle: de ce GRANT ALL nu este niciodată răspunsul"
seoTitle: "Securitate Oracle: roluri, privilegii și least privilege"
description: "Securitate Oracle: redesign al modelului GRANT cu roluri custom și Unified Audit, aplicând least privilege. Caz real cu SQL gata pentru copy-paste."
date: "2026-01-27T08:03:00+01:00"
draft: false
translationKey: "oracle_roles_privileges"
tags: ["security", "privileges"]
categories: ["oracle"]
image: "oracle-roles-privileges.cover.jpg"
---

Mi s-a întâmplat de mai multe ori: intru într-un mediu Oracle și găsesc aceeași situație. Toți utilizatorii aplicativi conectați ca schema owner, cu rolul DBA atribuit. Dezvoltatori, procese batch, instrumente de raportare — toți cu aceleași privilegii ca utilizatorul proprietar al tabelelor.

Când întrebi de ce, răspunsul este mereu o variantă a: „Așa funcționează totul fără probleme de permisiuni."

Sigur. Totul funcționează. Până în ziua în care un dezvoltator execută un `DROP TABLE` pe tabela greșită. Sau un batch de import face un `TRUNCATE` pe o tabelă de producție crezând că este în mediul de test. Sau cineva execută un `DELETE FROM clienti` fără clauza `WHERE`.

În ziua aceea criticitatea nu mai sunt permisiunile. Este că nu ai idee cine a făcut ce și nu ai niciun instrument pentru a preveni să se întâmple din nou.

---

## Contextul: un tipar care se repetă

Clientul era o companie de dimensiuni medii cu o aplicație de gestiune pe Oracle 19c. Aproximativ douăzeci de utilizatori — un mix de dezvoltatori, conturi aplicative și operatori. Schema aplicativă — să o numim `APP_OWNER` — conținea aproximativ 300 de tabele, vreo șaizeci de vizualizări și câteva zeci de proceduri PL/SQL.

Situația era ușor de descris:

- Toți se conectau ca `APP_OWNER`
- `APP_OWNER` avea rolul `DBA`
- Niciun audit configurat
- Nicio separare între cine citește și cine scrie
- Parolele erau partajate prin email

Nu era neglijență. Era inerție. Sistemul crescuse așa de-a lungul anilor, și nimeni nu se oprise să regândească modelul. Funcționa, și asta era suficient.

Până când un operator a șters din greșeală datele de facturare ale unui trimestru întreg. Niciun log, nicio urmă, niciun vinovat identificabil. Doar un backup de acum două zile și o gaură în date care a necesitat săptămâni de muncă pentru a fi acoperită.

---

## Cum funcționează securitatea în Oracle: modelul

Înainte de a povesti ce am făcut, trebuie înțeles cum structurează Oracle securitatea. Modelul este diferit de PostgreSQL și de MySQL, iar diferențele nu sunt cosmetice.

### Utilizator și schema: același lucru (aproape)

În Oracle, **crearea unui utilizator înseamnă crearea unei scheme**. Nu sunt două concepte separate: utilizatorul `APP_OWNER` este și schema `APP_OWNER`, iar obiectele create de acel utilizator trăiesc în acea schemă.

``` sql
CREATE USER app_read IDENTIFIED BY "ParolaSecura#2026"
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA 0 ON users;
```

`QUOTA 0` este intenționată: acest utilizator nu trebuie să creeze obiecte. Este un consumator, nu un proprietar.

### Privilegii de sistem vs privilegii de obiect

Oracle face o distincție clară între:

- **System privileges**: operațiuni globale precum `CREATE TABLE`, `CREATE SESSION`, `ALTER SYSTEM`
- **Object privileges**: operațiuni pe obiecte specifice precum `SELECT ON app_owner.clienti`, `EXECUTE ON app_owner.pkg_facturi`

Rolul `DBA` include peste 200 de system privileges. A-l atribui unui utilizator aplicativ este ca și cum ai da cheile întregii clădiri cuiva care trebuie doar să intre într-o cameră.

### Rolurile: predefinite și personalizate

Oracle oferă roluri predefinite (`CONNECT`, `RESOURCE`, `DBA`) și permite crearea de roluri personalizate. Rolurile predefinite au un punct critic istoric: `CONNECT` și `RESOURCE` includeau privilegii excesive în versiunile mai vechi. De la Oracle 12c au fost reduse, dar obiceiul de a le atribui fără să te gândești este greu de eliminat.

Calea corectă este crearea de roluri personalizate calibrate la nevoile reale.

---

## Implementarea: trei roluri, zero ambiguitate

Am proiectat trei roluri: citire, scriere și administrare aplicativă.

### 1. Rol de citire

``` sql
CREATE ROLE app_read_role;

-- Privilegii pe tabele
GRANT SELECT ON app_owner.clienti       TO app_read_role;
GRANT SELECT ON app_owner.comenzi       TO app_read_role;
GRANT SELECT ON app_owner.facturi       TO app_read_role;
GRANT SELECT ON app_owner.produse       TO app_read_role;
GRANT SELECT ON app_owner.tranzactii    TO app_read_role;

-- Privilegii pe vizualizări
GRANT SELECT ON app_owner.v_raport_vanzari   TO app_read_role;
GRANT SELECT ON app_owner.v_stare_comenzi    TO app_read_role;
```

Într-un mediu cu 300 de tabele nu le enumerezi una câte una manual. Am folosit un bloc PL/SQL pentru a genera grant-urile:

``` sql
BEGIN
  FOR t IN (SELECT table_name FROM dba_tables
            WHERE owner = 'APP_OWNER') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON app_owner.'
      || t.table_name || ' TO app_read_role';
  END LOOP;
END;
/
```

Simplu, repetabil și mai ales: documentat. Pentru că peste șase luni cineva va trebui să înțeleagă ce s-a făcut și de ce.

### 2. Rol de citire și scriere

``` sql
CREATE ROLE app_write_role;

-- Moștenește totul din rolul de citire
GRANT app_read_role TO app_write_role;

-- Adaugă DML pe tabelele operaționale
GRANT INSERT, UPDATE, DELETE ON app_owner.comenzi      TO app_write_role;
GRANT INSERT, UPDATE, DELETE ON app_owner.tranzactii   TO app_write_role;
GRANT INSERT, UPDATE ON app_owner.clienti              TO app_write_role;

-- Permisiune de execuție pe procedurile aplicative
GRANT EXECUTE ON app_owner.pkg_comenzi   TO app_write_role;
GRANT EXECUTE ON app_owner.pkg_facturi   TO app_write_role;
```

Notă: niciun `DELETE` pe tabela `clienti`. Nu pentru că ar fi imposibil tehnic, ci pentru că procesul aplicativ prevede o dezactivare, nu o ștergere. Privilegiul reflectă procesul, nu comoditatea.

### 3. Rol de administrare aplicativă

``` sql
CREATE ROLE app_admin_role;

-- Moștenește rolul de scriere
GRANT app_write_role TO app_admin_role;

-- Adaugă DDL controlat
GRANT CREATE VIEW TO app_admin_role;
GRANT CREATE PROCEDURE TO app_admin_role;
GRANT CREATE SYNONYM TO app_admin_role;

-- Poate gestiona tabelele de configurare
GRANT INSERT, UPDATE, DELETE ON app_owner.parametri     TO app_admin_role;
GRANT INSERT, UPDATE, DELETE ON app_owner.lookup_tipuri TO app_admin_role;
```

Niciun `CREATE TABLE`, niciun `DROP ANY`, niciun `ALTER SYSTEM`. Admin-ul aplicativ gestionează logica, nu structura fizică.

---

## Crearea utilizatorilor și atribuirea rolurilor

``` sql
-- Utilizator pentru rapoarte (doar citire)
CREATE USER srv_report IDENTIFIED BY "RptSecure#2026"
DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp
QUOTA 0 ON users;
GRANT CREATE SESSION TO srv_report;
GRANT app_read_role TO srv_report;

-- Utilizator aplicativ (citire și scriere)
CREATE USER srv_app IDENTIFIED BY "AppSecure#2026"
DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp
QUOTA 0 ON users;
GRANT CREATE SESSION TO srv_app;
GRANT app_write_role TO srv_app;

-- DBA aplicativ (administrare)
CREATE USER dba_app IDENTIFIED BY "DbaSecure#2026"
DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp
QUOTA 10M ON users;
GRANT CREATE SESSION TO dba_app;
GRANT app_admin_role TO dba_app;
```

Fiecare utilizator are propria parolă, un rol specific și o cotă de disc coerentă cu scopul său. `srv_report` nu are cotă pentru că nu trebuie să creeze nimic. `dba_app` are 10 MB pentru că trebuie să poată crea vizualizări și proceduri.

---

## Revocarea rolului DBA

Pasul cel mai delicat: eliminarea `DBA` de la `APP_OWNER`.

``` sql
REVOKE DBA FROM app_owner;
```

O linie. Dar înainte de a o executa, am verificat că `APP_OWNER` mai avea privilegiile necesare pentru a-și deține obiectele:

``` sql
SELECT privilege FROM dba_sys_privs WHERE grantee = 'APP_OWNER';
SELECT granted_role FROM dba_role_privs WHERE grantee = 'APP_OWNER';
```

Și am acordat doar privilegiile strict necesare:

``` sql
GRANT CREATE SESSION TO app_owner;
GRANT CREATE TABLE TO app_owner;
GRANT CREATE VIEW TO app_owner;
GRANT CREATE PROCEDURE TO app_owner;
GRANT CREATE SEQUENCE TO app_owner;
GRANT UNLIMITED TABLESPACE TO app_owner;
```

`APP_OWNER` rămâne proprietarul obiectelor dar nu mai are puterea de a face orice pe baza de date. Este un proprietar, nu un zeu.

---

## ⚠️ Avertisment: privilegii prin role și stored procedure cu definer-rights

Există o capcană care merită cunoscută înainte de a scrie cod PL/SQL împotriva acestui model de roluri. O regulă Oracle peste care se împiedică aproape orice DBA junior:

> **Privilegiile acordate prin role NU sunt vizibile în stored procedures compilate cu definer-rights (default).**

Exemplu concret. Acord `SELECT` pe tabelul `app_owner.facturi` rolului `app_read_role`, apoi acord rolul utilizatorului `app_user`:

```sql
GRANT SELECT ON app_owner.facturi TO app_read_role;
GRANT app_read_role TO app_user;
```

În sesiune interactivă totul funcționează — `app_user` poate executa `SELECT * FROM app_owner.facturi`. Dar dacă `app_user` are o stored procedure care execută același SELECT, la runtime Oracle returnează `ORA-00942: table or view does not exist`. Același utilizator, aceeași query — un caz funcționează interactiv, celălalt nu.

Motivul: implicit, stored procedures Oracle sunt compilate cu **definer-rights** (`AUTHID DEFINER`, comportament implicit). La runtime, motorul evaluează doar privilegiile **directe**, nu pe cele moștenite prin role. Este o decizie de design Oracle existentă de zeci de ani și care nu se schimbă pentru retrocompatibilitate.

Cele două soluții:

**Opțiunea 1 — Privilegiu direct către owner-ul procedurii**:

```sql
-- Fără role, GRANT direct utilizatorului individual
GRANT SELECT ON app_owner.facturi TO app_user;
```

Funcționează, dar anulează avantajul modelului de roluri pentru acel privilegiu specific.

**Opțiunea 2 — Stored procedure cu invoker-rights** (`AUTHID CURRENT_USER`):

```sql
CREATE OR REPLACE PROCEDURE citeste_facturi
  AUTHID CURRENT_USER
AS
BEGIN
  FOR r IN (SELECT * FROM app_owner.facturi) LOOP
    -- ...
  END LOOP;
END;
/
```

Cu `AUTHID CURRENT_USER`, la runtime procedura folosește privilegiile **apelantului** (inclusiv rolurile active în sesiune). Păstrează modelul de roluri intact. Dezavantajul: schimbă semantica accesului la obiecte (procedura rezolvă numele în contextul apelantului, nu al proprietarului), așa că evaluează caz cu caz.

Regula practică: pentru **proceduri de citire/scriere aplicative** care lucrează pe datele unui proprietar centralizat, `AUTHID CURRENT_USER` este aproape întotdeauna alegerea corectă. Pentru **proceduri administrative** care trebuie să opereze cu privilegiile specifice ale owner-ului, lasă default-ul `AUTHID DEFINER` și acordă privilegiile direct.

---

## Audit: a ști cine ce a făcut

A avea rolurile corecte nu este suficient. Trebuie să știi cine ce a făcut, mai ales pentru operațiunile critice.

Oracle de la versiunea 12c oferă **Unified Audit**, care înlocuiește vechiul audit tradițional cu un sistem centralizat.

Sintaxa cere două statement distincte: `CREATE AUDIT POLICY` pentru a declara policy-ul, și `AUDIT POLICY` pentru a-l activa [1]. O eroare frecventă este folosirea `ALTER AUDIT POLICY ... ENABLE`: `ALTER AUDIT POLICY` există, dar este pentru a **modifica** un policy deja definit (adăuga sau elimina acțiuni), nu pentru a-l activa.

``` sql
-- Audit pe operațiuni DDL critice
CREATE AUDIT POLICY pol_ddl_critic
ACTIONS CREATE TABLE, DROP TABLE, ALTER TABLE,
        TRUNCATE TABLE, CREATE USER, DROP USER,
        ALTER USER, GRANT, REVOKE;

AUDIT POLICY pol_ddl_critic;

-- Audit pe accesul la date sensibile
CREATE AUDIT POLICY pol_acces_date
ACTIONS SELECT ON app_owner.clienti,
        DELETE ON app_owner.facturi,
        UPDATE ON app_owner.facturi;

AUDIT POLICY pol_acces_date;

-- Audit pe autentificări eșuate
CREATE AUDIT POLICY pol_login_esuat
ACTIONS LOGON;
AUDIT POLICY pol_login_esuat WHENEVER NOT SUCCESSFUL;
```

Pentru a dezactiva un policy se folosește `NOAUDIT POLICY nume_policy`.

Pentru a verifica ce se înregistrează, se interoghează view-ul `UNIFIED_AUDIT_TRAIL` [2]:

``` sql
SELECT * FROM unified_audit_trail
WHERE event_timestamp > SYSDATE - 7
ORDER BY event_timestamp DESC;
```

Auditul nu este paranoia. Este singura modalitate de a răspunde la întrebarea „cine ce a făcut?" fără a te baza pe intuiție.

---

## Comparația cu PostgreSQL și MySQL

Acest articol este al treilea dintr-o serie despre gestionarea securității în bazele de date relaționale. Primele două acoperă [PostgreSQL](/ro/posts/postgresql/security/postgresql_roles_and_users/) și [MySQL](/ro/posts/mysql/security/mysql-users-and-hosts/).

Diferențele dintre cele trei sisteme sunt substanțiale:

| Aspect | Oracle | PostgreSQL | MySQL |
|---|---|---|---|
| Utilizator = schemă? | Da | Nu (independente) | Da (baze de date separate) |
| Model de roluri | Predefinite + custom | Totul este un ROLE | Roluri de la MySQL 8.0 |
| Identitate | Nume utilizator | Nume utilizator | Pereche utilizator@host |
| Audit nativ | Unified Audit (12c+) | pgAudit (extensie) | Audit plugin |
| Privilegii granulare | System + Object | Database/Schema/Object | Global/DB/Table/Column |
| GRANT ALL | Există dar periculos | Există, nerecomandat | Există, nerecomandat |

În PostgreSQL totul este un ROLE, iar simplitatea modelului este punctul său forte. În MySQL identitatea este legată de host-ul de origine, ceea ce adaugă un nivel de complexitate (și securitate) pe care celelalte nu îl au. În Oracle modelul este cel mai bogat și cel mai granular, dar și cel mai ușor de configurat greșit din cauza numărului mare de opțiuni.

Principiul rămâne același peste tot: **dă fiecăruia doar ce are nevoie, niciun privilegiu în plus**.

---

## Ce s-a schimbat după

Tranziția a fost graduală — două săptămâni pentru implementarea completă, cu teste pe fiecare aplicație și procedură. Câteva scripturi au încetat să funcționeze pentru că presupuneau privilegii care nu le aparțineau. Fiecare eșec era de fapt o criticitate ascunsă care înainte era invizibilă.

Rezultatul:

- **20 utilizatori nominali** în locul unui singur schema partajat
- **3 roluri personalizate** în locul rolului DBA
- **Audit activ** pe DDL și operațiuni sensibile
- **Zero incidente** de ștergere accidentală în lunile următoare

Clientul nu a observat îmbunătățiri de performanță. Nu acesta era obiectivul. A observat că atunci când cineva greșea, paguba era limitată și trasabilă. Și asta, într-un mediu de producție, valorează mai mult decât orice optimizare.

---

## Concluzie

`GRANT ALL PRIVILEGES` și rolul `DBA` sunt scurtături. Funcționează în sensul că elimină erorile de permisiuni. Dar elimină și orice strat de protecție.

Securitatea în Oracle nu este o problemă de instrumente — instrumentele există, și sunt puternice. Este o problemă de proiectare: a decide cine poate face ce, a documenta, a implementa și apoi a verifica că funcționează.

Nu este munca cea mai glamuroasă din lume. Dar este cea care face diferența între o bază de date care doar supraviețuiește și una care este cu adevărat sub control.

------------------------------------------------------------------------

## Surse oficiale

1. Oracle Database SQL Language Reference 19c — [AUDIT (Unified Auditing)](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/AUDIT-Unified-Auditing.html) și [CREATE AUDIT POLICY](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-AUDIT-POLICY-Unified-Auditing.html)
2. Oracle Database Reference 19c — [UNIFIED_AUDIT_TRAIL](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/UNIFIED_AUDIT_TRAIL.html)

------------------------------------------------------------------------

## Glosar

**[System Privilege](/ro/glossary/system-privilege/)** — Privilegiu Oracle care autorizează operațiuni globale pe baza de date precum CREATE TABLE, CREATE SESSION sau ALTER SYSTEM, independente de orice obiect specific.

**[Object Privilege](/ro/glossary/object-privilege/)** — Privilegiu Oracle care autorizează operațiuni pe un obiect specific al bazei de date precum SELECT, INSERT sau EXECUTE pe o tabelă, vizualizare sau procedură.

**[REVOKE](/ro/glossary/revoke/)** — Comandă SQL pentru eliminarea privilegiilor sau rolurilor acordate anterior unui utilizator sau rol, complementară comenzii GRANT.

**[Unified Audit](/ro/glossary/unified-audit/)** — Sistem de audit centralizat introdus în Oracle 12c care unifică toate tipurile de audit într-o singură infrastructură, înlocuind vechiul audit tradițional.

**[Least Privilege](/ro/glossary/least-privilege/)** — Principiu de securitate care prevede atribuirea fiecărui utilizator doar a permisiunilor strict necesare pentru îndeplinirea funcției sale.
