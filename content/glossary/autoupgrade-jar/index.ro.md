---
title: "autoupgrade.jar"
description: "Unealtă Oracle în linie de comandă care automatizează upgrade-ul bazei de date. În modul analyze scanează instanța sursă și generează un raport de compatibilitate fără modificări."
translationKey: "glossary_autoupgrade_jar"
aka: "Oracle AutoUpgrade Utility"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`autoupgrade.jar` este utilitarul Oracle distribuit ca JAR executabil care automatizează întregul ciclu de upgrade al unei baze de date, de la verificările pre-migrare până la finalizare. Înlocuiește vechile scripturi manuale `dbupgrade` și reduce semnificativ riscul de eroare umană în operațiunile de upgrade la scară largă.

## Cum funcționează

Instrumentul se invocă prin `java -jar autoupgrade.jar` cu un fișier de configurare care descrie mediul sursă și cel destinație. Suportă trei moduri principale:

```bash
# Modul analyze: doar citire, fără modificări asupra instanței
java -jar autoupgrade.jar -config upgrade.cfg -mode analyze

# Modul fixups: aplică corecțiile pre-upgrade identificate
java -jar autoupgrade.jar -config upgrade.cfg -mode fixups

# Modul deploy: execută upgrade-ul complet
java -jar autoupgrade.jar -config upgrade.cfg -mode deploy
```

În modul `analyze`, instrumentul interoghează vederile de sistem, verifică compatibilitatea obiectelor, validează parametrii de inițializare și produce un raport HTML/text cu problemele detectate și acțiunile recomandate. Nu se efectuează nicio scriere asupra bazei de date sursă.

## Când se folosește

Modul `analyze` este instrumentul de referință în faza de **assessment pre-migrare**: permite rularea mai multor treceri de analiză pe medii de producție fără downtime și fără riscuri. Este deosebit de relevant când baza de date sursă se află pe versiunea 11g sau 12c, iar destinația este 19c, deoarece distanța dintre versiuni amplifică numărul de deprecări și incompatibilități de gestionat.

În medii financiare cu tablespace-uri de mai mulți TB, raportul generat devine input direct pentru planul de ROLLBACK și pentru estimarea ferestrelor de mentenanță.
