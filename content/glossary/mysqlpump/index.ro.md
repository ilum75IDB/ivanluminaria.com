---
title: "mysqlpump"
description: "Evoluție a mysqldump introdusă în MySQL 5.7 cu paralelism la nivel de tabelă, depreciată de Oracle în MySQL 8.0.34."
translationKey: "glossary_mysqlpump"
aka: "MySQL pump"
articles:
  - "/posts/mysql/mysqldump-mysqlpump-mydumper"
---

**mysqlpump** este utilitarul de backup logic introdus de Oracle în MySQL 5.7 ca evoluție a mysqldump. Diferența principală este suportul pentru paralelism la nivel de tabelă și compresia nativă a output-ului (zlib, lz4, zstd).

## Cum funcționează

mysqlpump poate face dump la mai multe tabele simultan folosind thread-uri paralele, configurabile cu `--default-parallelism`. Compresia se aplică direct în timpul dump-ului, fără a necesita pipe-uri externe către gzip. Suportă și dump-ul selectiv al utilizatorilor și conturilor MySQL.

Totuși, paralelismul operează doar la nivel de tabelă întreagă: dacă o singură tabelă este mult mai mare decât celelalte, un thread se târăște singur în timp ce restul au terminat deja.

## Problema consistenței

Cu paralelismul activ, mysqlpump nu garantează consistența între tabele diferite — tabelele exportate de thread-uri diferite pot reflecta momente diferite în timp. Aceasta este o limitare critică pentru backup-urile de producție pe baze de date relaționale cu foreign key-uri.

## Starea actuală

Oracle a declarat mysqlpump depreciat în MySQL 8.0.34 și l-a eliminat complet în MySQL 8.4. Pentru cei care caută paralelism în backup-ul logic, mydumper este alternativa recomandată.
