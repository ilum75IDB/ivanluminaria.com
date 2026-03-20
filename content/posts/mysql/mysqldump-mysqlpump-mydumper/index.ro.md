---
title: "mysqldump vs mysqlpump vs mydumper: backup-ul care nu te lasă să dormi"
description: "O bază de date de 60 GB, un mysqldump care dura trei ore și bloca scrierile. Am testat mysqlpump și mydumper pe același mediu, cu timpi reali de dump și restore. Iată ce am descoperit — și de ce alegerea instrumentului de backup este o decizie arhitecturală, nu operațională."
date: "2026-04-14T10:00:00+01:00"
draft: false
translationKey: "mysqldump_mysqlpump_mydumper"
tags: ["backup", "mysqldump", "mydumper", "restore", "mariadb"]
categories: ["mysql"]
image: "mysqldump-mysqlpump-mydumper.cover.jpg"
---

Apelul a venit într-o vineri după-amiază — pentru că aceste lucruri se întâmplă întotdeauna vinerea. DBA-ul unui client din sectorul logistic îmi scrie pe Teams: "Backup-ul de aseară a durat trei ore și jumătate. Dimineață utilizatorii au găsit aplicația lentă la 8. Putem discuta?"

Puteam discuta, da. De fapt, ar fi trebuit să discutăm demult.

Setup-ul era un clasic: MySQL 8.0 pe Rocky Linux, bază de date de aproximativ 60 GB, un gestional cu vreo treizeci de tabele InnoDB din care patru sau cinci erau cu adevărat mari — tabela comenzilor, cea a mișcărilor de depozit, istoricul de tracking. Backup-ul se făcea în fiecare noapte cu un mysqldump lansat de cron la 2:00. Funcționase ani de zile. Problema era că baza de date între timp crescuse.

Trei ore de mysqldump înseamnă trei ore de `--lock-all-tables` — sau în cel mai bun caz trei ore de tranzacție consistentă cu `--single-transaction` care oricum ține un snapshot InnoDB deschis tot timpul. Și când dump-ul se termină la 5:00 și un restore de test (pe care nimeni nu-l făcea) ar fi durat încă patru ore, fereastra de backup pur și simplu nu mai există.

---

## Problema reală: mysqldump este single-threaded

Primul lucru de înțeles despre {{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}} este că face un singur lucru la un moment dat. O tabelă după alta, un rând după altul, un fișier SQL la ieșire. Atât.

Nu există paralelism. Nu există compresie nativă. Nu există nicio modalitate de a spune "folosește 4 thread-uri și termină mai repede". Este un program născut în anul 2000 — literal — și designul său reflectă o epocă în care 60 GB erau o cantitate de neconceput pentru o bază de date MySQL.

Dump-ul clientului producea un fișier SQL de 45 GB. Un singur fișier monolitic care conținea toate tabelele, toate procedurile stocate, toate trigger-ele. Pentru a face un restore era suficient să dai acel fișier la `mysql` — dar dura patru ore, pentru că și restore-ul este secvențial.

```bash
# Backup-ul clasic — funcționează, dar scalează prost
mysqldump --single-transaction --routines --triggers --events \
  --all-databases > /backup/full_backup.sql
```

Paradoxal, mysqldump are un avantaj enorm: este peste tot. Este inclus în fiecare instalare MySQL, nu necesită nimic suplimentar, produce SQL lizibil. Dacă trebuie să muți o tabelă de 500 de rânduri între două medii, este perfect. Dacă trebuie să faci backup la o bază de date de 60 GB în producție — nu.

I-am explicat clientului că aveam două alternative: mysqlpump și mydumper. Două instrumente cu filozofii diferite, limitări diferite și performanțe care pe hârtie promit mult dar în realitate trebuie testate.

---

## mysqlpump: promisiunea neîndeplinită a Oracle

{{< glossary term="mysqlpump" >}}mysqlpump{{< /glossary >}} a sosit cu MySQL 5.7 ca evoluția oficială a mysqldump. Promisiunea era clară: paralelism în dump, compresie nativă, gestionarea utilizatorilor. Pe hârtie, tot ce-i lipsea lui mysqldump.

L-am configurat — de fapt era deja acolo pentru că vine inclus în distribuția MySQL — și am lansat un prim test pe baza de date a clientului:

```bash
mysqlpump --single-transaction --default-parallelism=4 \
  --compress-output=zlib --all-databases > /backup/full_backup.sql.zlib
```

Rezultatul? 48 de minute pentru dump, față de trei ore și jumătate cu mysqldump. O îmbunătățire importantă. Dar apoi am privit mai atent.

Paralelismul lui mysqlpump funcționează la nivel de tabelă: dacă ai 4 thread-uri, face dump la 4 tabele simultan. Problema este că atunci când ai o tabelă de 30 GB și trei tabele de 50 MB, trei thread-uri termină în treizeci de secunde și apoi un singur thread se târăște patruzeci de minute pe tabela mare. Paralelismul este la fel de eficient pe cât de echilibrată este baza ta de date — și bazele de date de producție nu sunt niciodată echilibrate.

Dar problema mai gravă este alta. mysqlpump cu `--single-transaction` nu garantează un backup consistent între tabele diferite. O spune documentația însăși, într-o notă pe care majoritatea oamenilor nu o citesc:

> *mysqlpump does not guarantee consistency of the dumped data across tables when using parallelism. Tables dumped in different threads may be at different points in time.*

Recitiți acea frază. Dacă folosești paralelismul — care este singurul motiv să folosești mysqlpump — pierzi garanția de consistență între tabele. Într-o bază de date relațională. Unde tabelele au foreign key-uri între ele.

Pentru un mediu de dezvoltare sau test, poate fi acceptabil. Pentru un backup de producție din care ar putea trebui să faci restore în caz de dezastru? Nu. Absolut nu.

Încă o notă: Oracle a declarat mysqlpump **depreciat în MySQL 8.0.34** și l-a eliminat în MySQL 8.4. Ceea ce spune totul despre încrederea pe care Oracle însăși o avea în acest instrument.

---

## mydumper: instrumentul care face ce promite

{{< glossary term="mydumper" >}}mydumper{{< /glossary >}} este un proiect open source născut în 2009 din comunitatea MySQL — în special din munca lui Domas Mituzas, Andrew Hutchings și apoi întreținut de Max Bubenick. Nu este un instrument Oracle. Nu este inclus în distribuția MySQL. Trebuie instalat separat. Dar face ceva ce nici mysqldump nici mysqlpump nu fac: paralelism adevărat, la nivel de chunk în interiorul aceleiași tabele.

```bash
# Instalare pe Rocky Linux / CentOS
yum install https://github.com/mydumper/mydumper/releases/download/v0.16.9-1/mydumper-0.16.9-1.el8.x86_64.rpm
```

mydumper ia o tabelă mare, o împarte în chunk-uri (implicit bazat pe primary key) și atribuie fiecare chunk unui thread diferit. Așadar, acea tabelă de 30 GB nu este exportată de un singur thread — este spartă în bucăți și descărcată în paralel.

Dump-ul pe care l-am lansat pe baza de date a clientului:

```bash
mydumper --threads 8 --compress --trx-consistency-only \
  --outputdir /backup/mydumper_full/ \
  --logfile /var/log/mydumper.log
```

22 de minute. Față de trei ore și jumătate cu mysqldump și 48 de minute cu mysqlpump.

Dar adevăratul avantaj al mydumper nu este doar viteza dump-ului — este viteza restore-ului. mydumper produce un fișier pentru fiecare tabelă (sau pentru fiecare chunk), iar companionul său `myloader` le încarcă în paralel:

```bash
myloader --threads 8 --directory /backup/mydumper_full/ \
  --overwrite-tables --compress-protocol
```

Restore-ul care cu mysqldump ar fi durat patru ore, cu myloader a durat o oră și douăzeci de minute. Pe o bază de date de 60 GB. Cu opt thread-uri.

---

## Numerele: teste pe mediu real

Am făcut testele pe același server al clientului — nu pe un mediu de laborator cu discuri NVMe și RAM infinit. Server real, sarcină reală, discuri SATA în RAID 10.

| Operație | mysqldump | mysqlpump (4 thread-uri) | mydumper (8 thread-uri) |
|----------|-----------|-------------------------|------------------------|
| **Dump** | 3h 25min | 48 min | 22 min |
| **Dimensiune output** | 45 GB (SQL) | 12 GB (comprimat) | 9.8 GB (comprimat) |
| **Restore** | ~4h (estimat) | ~3h (estimat) | 1h 20min |
| **Consistență între tabele** | Da | Nu (cu paralelism) | Da |
| **Blocare scrieri** | Nu* | Nu* | Nu* |

*Cu `--single-transaction` pe InnoDB.

Câteva note despre numere:
- Restore-ul mysqldump și mysqlpump este estimat pentru că nu am făcut testul complet în producție — prea riscant. Timpii sunt calculați din teste parțiale pe un subset de tabele
- Compresia mydumper (`--compress`) folosește zstd implicit, care comprimă mai bine și mai rapid decât zlib
- Restore-ul cu myloader dezactivează verificările de foreign key și reconstruiește indexurile la sfârșit, ceea ce accelerează enorm încărcarea

---

## Opțiunile critice pe care nu trebuie să le uiți

Oricare instrument ai alege, există opțiuni pe care trebuie să le incluzi întotdeauna. Le-am văzut uitate de prea multe ori, cu consecințe care variază de la neplăceri la dezastre.

### --single-transaction

Obligatoriu pe InnoDB. Fără această opțiune, dump-ul achiziționează lock-uri care blochează scrierile. Cu `--single-transaction`, dump-ul folosește o tranzacție cu isolation level REPEATABLE READ pentru a obține un snapshot consistent fără a bloca pe nimeni.

Atenție: funcționează doar pe tabele InnoDB. Dacă ai tabele MyISAM (și da, în 2026 încă le găsesc), acelea vor fi blocate oricum.

### --routines --triggers --events

Procedurile stocate, trigger-ele și evenimentele programate nu sunt incluse în dump implicit. Trebuie să le ceri explicit. Am văzut restore-uri care "funcționau perfect" — cu excepția că lipseau toate trigger-ele de audit și aplicația scria date fără trasabilitate.

### --set-gtid-purged (MySQL) sau --gtid (mydumper)

Dacă folosești replicare bazată pe GTID — și ar trebui — dump-ul trebuie să gestioneze corect GTID-urile. Dacă nu o face, restore-ul pe o replică generează conflicte de replicare care te vor înnebuni.

### Verificarea restore-ului

Aceasta nu este o opțiune — este o practică. Backup-ul pe care nu-l verifici este backup-ul pe care nu-l ai. Am un client care făcea backup-uri în fiecare noapte de trei ani. În ziua în care a trebuit să facă un restore, a descoperit că fișierul era corupt de săptămâna trecută. Trei ani de backup-uri, zero teste de restore.

```bash
# Verificare minimă cu mydumper: restore pe instanță de test
myloader --threads 4 --directory /backup/mydumper_full/ \
  --host test-mysql-server --overwrite-tables

# Numără rândurile tabelelor principale
mysql -h test-mysql-server -e "
  SELECT table_name, table_rows
  FROM information_schema.tables
  WHERE table_schema = 'production_db'
  ORDER BY table_rows DESC LIMIT 10;"
```

---

## Când să folosești ce

După treizeci de ani de baze de date, regula mea este simplă:

**mysqldump** — pentru baze de date sub 5 GB, migrări punctuale, dump-uri de tabele individuale, medii de dezvoltare unde viteza nu este critică. Este cuțitul elvețian: face totul, încet, dar face.

**mysqlpump** — nu-l mai recomand. Depreciat de Oracle, consistență negarantată cu paralelismul, iar mydumper face tot ce promitea mysqlpump dar mai bine. Dacă îl folosești, planifică migrarea la mydumper.

**mydumper/myloader** — pentru orice bază de date de producție peste 10 GB. Paralelism adevărat, consistență garantată, restore-uri rapide. Necesită instalare separată, dar timpul pe care-l economisești la primul backup compensează din plin.

---

## Strategia completă: nu doar logical backup

Ceva ce le spun mereu clienților: backup-ul logic (mysqldump, mydumper) este **o** componentă a strategiei, nu strategia întreagă.

Pentru clientul din logistică am pus la punct acest plan:

1. **mydumper în fiecare noapte** — backup logic complet, 8 thread-uri, compresie zstd, retenție 7 zile
2. **Binary log continuu** — cu `binlog_expire_logs_seconds` la 7 zile, pentru {{< glossary term="pitr" >}}point-in-time recovery{{< /glossary >}}
3. **Percona XtraBackup săptămânal** — backup fizic la cald, pentru cel mai rapid restore posibil în caz de dezastru total
4. **Test automat de restore** — un script care în fiecare duminică face restore-ul backup-ului mydumper pe o instanță de test și verifică numărarea rândurilor

Backup-ul logic este comod pentru că este portabil — poți face restore pe orice versiune de MySQL, pe orice arhitectură. Dar pentru o bază de date de 60 GB, un backup fizic cu XtraBackup îți permite un restore în 15-20 de minute în loc de o oră și jumătate. Când baza de date de producție este jos și telefonul sună, acea oră de diferență contează.

Vinerea următoare, DBA-ul clientului mi-a scris din nou pe Teams. Dar de data aceasta mesajul era diferit: "Backup terminat în 23 de minute. Niciun impact asupra utilizatorilor. Mulțumesc."

Cu plăcere. Dar data viitoare, nu aștepta ca backup-ul să dureze trei ore ca să-mi ceri ajutorul.

------------------------------------------------------------------------

## Glosar

**[mysqldump](/ro/glossary/mysqldump/)** — Utilitar de backup logic inclus în fiecare instalare MySQL. Produce un fișier SQL secvențial cu toate instrucțiunile pentru recrearea schemei și datelor. Single-threaded, fiabil dar lent pe baze de date mari.

**[mysqlpump](/ro/glossary/mysqlpump/)** — Evoluție a mysqldump introdusă în MySQL 5.7, cu suport pentru paralelism la nivel de tabelă și compresie nativă. Depreciat de Oracle în MySQL 8.0.34 pentru probleme de consistență.

**[mydumper](/ro/glossary/mydumper/)** — Instrument open source de backup logic pentru MySQL/MariaDB cu paralelism real la nivel de chunk. Împarte tabelele mari în bucăți și le exportă cu thread-uri multiple, cu restore paralel prin myloader.

**[PITR](/ro/glossary/pitr/)** — Point-in-Time Recovery: tehnică care combină un backup complet cu binary log-urile pentru a readuce baza de date la orice moment în timp, nu doar la ora backup-ului.

**[GTID](/ro/glossary/gtid/)** — Global Transaction Identifier: identificator unic atribuit fiecărei tranzacții în MySQL, care simplifică gestionarea replicării și urmărirea tranzacțiilor între master și replică.
