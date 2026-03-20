---
title: "mydumper"
description: "Instrument open source de backup logic pentru MySQL/MariaDB cu paralelism real la nivel de chunk, cu restore paralel prin myloader."
translationKey: "glossary_mydumper"
aka: "myloader"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mydumper** este un instrument open source de backup logic pentru MySQL și MariaDB care implementează paralelism adevărat: nu doar între tabele diferite, ci și în interiorul aceleiași tabele, împărțind-o în chunk-uri bazate pe primary key.

## Cum funcționează

mydumper se conectează la serverul MySQL, achiziționează un snapshot consistent cu `FLUSH TABLES WITH READ LOCK` (sau `--trx-consistency-only` pentru a evita lock-urile globale pe InnoDB), apoi distribuie munca între thread-uri multiple. Fiecare tabelă mare este spartă în chunk-uri — implicit bazate pe range-urile primary key-ului — și fiecare chunk este exportat de un thread separat.

Output-ul nu este un singur fișier SQL ci un director cu un fișier pentru fiecare tabelă (sau pentru fiecare chunk), plus fișierele de metadate, schemă și proceduri stocate.

## Restore-ul cu myloader

Companionul lui mydumper este `myloader`, care încarcă fișierele în paralel dezactivând verificările de foreign key și reconstruind indexurile la sfârșit. Această abordare face restore-ul semnificativ mai rapid comparativ cu încărcarea secvențială a unui singur fișier SQL.

## Când se folosește

mydumper este opțiunea recomandată pentru baze de date de producție peste 10 GB unde viteza de dump și restore este critică. Pe o bază de date de 60 GB cu 8 thread-uri, un dump care cu mysqldump necesită 3-4 ore se completează în 20-25 de minute.
