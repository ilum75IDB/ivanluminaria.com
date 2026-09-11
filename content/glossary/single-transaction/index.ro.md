---
title: "--single-transaction"
description: "Opțiune mysqldump care deschide o tranzacție REPEATABLE READ pentru a exporta date InnoDB în mod consistent, fără a bloca tabelele."
translationKey: "glossary_single_transaction"
aka: null
articles:
  - "/posts/mysql/mysql-8-0-patching-gtid-rhel"
---

`--single-transaction` este o opțiune a `mysqldump` care deschide o tranzacție `REPEATABLE READ` înainte de a începe exportul. Izolarea asigurată de InnoDB garantează un snapshot consistent al datelor fără a bloca scrierile concurente.

## Cum funcționează

La pornirea dump-ului, MySQL emite implicit `START TRANSACTION WITH CONSISTENT SNAPSHOT`. Toate citirile ulterioare au loc în cadrul aceleiași tranzacții, văzând datele exact cum erau în momentul deschiderii snapshot-ului. Operațiunile DML concurente (INSERT, UPDATE, DELETE) continuă fără întrerupere, deoarece InnoDB le izolează prin MVCC.

```bash
mysqldump --single-transaction --routines --events \
  -u root -p my_database > backup.sql
```

Fișierul rezultat conține un dump logic consistent, echivalent cu un snapshot la un moment precis în timp.

## Când se folosește și limitări

`--single-transaction` este alegerea standard pentru bazele de date InnoDB în producție: evită lock-urile la nivel de tabelă care ar bloca aplicațiile. Nu se aplică tabelelor **MyISAM** sau **MEMORY**, care nu suportă tranzacții. Pentru aceste motoare se folosește `--lock-tables`, care achiziționează un lock partajat pe toată durata dump-ului.

Când schema conține motoare de stocare mixte, cele două flag-uri se exclud reciproc: `--single-transaction` dezactivează automat `--lock-tables`. Tabelele non-tranzacționale incluse în dump pot fi astfel inconsistente față de tabelele InnoDB.

## Note operaționale

Pentru dump-uri de dimensiuni mari, tranzacția deschisă poate acumula intrări semnificative în undo log-ul InnoDB. Monitorizarea `innodb_history_list_length` în timpul operațiunilor de backup prelungite este o practică recomandată pentru a evita presiunea asupra tablespace-ului de undo.
