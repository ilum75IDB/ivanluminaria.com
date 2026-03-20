---
title: "mysqldump"
description: "Utilitar de backup logic inclus în fiecare instalare MySQL, produce un fișier SQL secvențial pentru recrearea schemei și datelor."
translationKey: "glossary_mysqldump"
aka: "MySQL dump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mysqldump** este utilitarul de backup logic inclus standard în fiecare instalare de MySQL și MariaDB. Produce un fișier SQL care conține toate instrucțiunile (CREATE TABLE, INSERT) necesare pentru a reconstrui complet schema și datele unei baze de date.

## Cum funcționează

mysqldump se conectează la serverul MySQL și citește tabelele una câte una, generând instrucțiunile SQL corespunzătoare la ieșire. Operația este strict single-threaded: o tabelă după alta, un rând după altul. Fișierul produs poate fi comprimat extern (gzip, zstd) dar instrumentul în sine nu oferă compresie nativă.

Cu opțiunea `--single-transaction`, dump-ul se desfășoară în interiorul unei tranzacții cu isolation level REPEATABLE READ, care garantează un snapshot consistent pe tabelele InnoDB fără a achiziționa lock-uri pe scrieri.

## La ce servește

mysqldump este instrumentul standard pentru:

- Backup logic al bazelor de date mici și medii
- Migrări între versiuni diferite de MySQL
- Exportul tabelelor individuale sau bazelor de date pentru transfer între medii
- Crearea de dump-uri lizibile și inspectabile manual

## Când devine o problemă

Pe baze de date peste 10-15 GB, dump-ul single-threaded devine un blocaj. O bază de date de 60 GB poate necesita 3-4 ore de dump și tot atât de restore. Lipsa paralelismului este limitarea structurală: nu există nicio modalitate de a accelera procesul decât trecând la instrumente precum mydumper.
