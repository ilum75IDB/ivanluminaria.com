---
title: "Churn"
description: "Măsură a cât de mult se modifică o tabelă de baze de date după inserarea inițială a datelor, în termeni de UPDATE și DELETE. Determină costul de mentenanță al indexurilor."
translationKey: "glossary_churn"
articles:
  - "/posts/postgresql/like-optimization-postgresql"
---

**Churn-ul** unei tabele este măsura a cât de mult se modifică datele sale după inserare. O tabelă cu churn ridicat suportă frecvente UPDATE-uri și DELETE-uri; o tabelă cu churn scăzut este predominant append-only (doar INSERT).

## Cum funcționează

În PostgreSQL, fiecare UPDATE creează o versiune nouă a rândului (datorită modelului MVCC) iar versiunea veche devine un dead tuple. DELETE-urile creează de asemenea dead tuples. Cu cât churn-ul este mai mare, cu atât mai multă muncă trebuie să facă VACUUM și indexurile pentru a menține performanța. Un index GIN pe o tabelă cu churn ridicat poate degrada semnificativ performanța la scriere.

## La ce folosește

Evaluarea churn-ului înainte de a crea un index este esențială pentru a evita rezolvarea unei probleme de citire prin crearea uneia de scriere. Pe o tabelă append-only (zero UPDATE, zero DELETE, zero dead tuples), un index GIN are impact minim asupra scrierilor. Pe o tabelă cu churn ridicat, același index ar putea deveni un blocaj.

## Când se folosește

Churn-ul se analizează verificând statisticile tabelei: numărul de UPDATE-uri și DELETE-uri zilnice, dead tuples, frecvența VACUUM. În PostgreSQL, `pg_stat_user_tables` furnizează aceste metrici. Decizia de a adăuga un index GIN sau trigram ar trebui să pornească întotdeauna de la această analiză.
