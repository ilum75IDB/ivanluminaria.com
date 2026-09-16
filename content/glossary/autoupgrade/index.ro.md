---
title: "AutoUpgrade"
description: "Utilitar Java (autoupgrade.jar) care din Oracle 21c este instrumentul unic pentru analiza pre-upgrade, corecții și upgrade-ul bazei de date. Înlocuiește preupgrade.jar, care nu mai este distribuit."
translationKey: "glossary_autoupgrade"
aka: "AutoUpgrade Utility (autoupgrade.jar)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

AutoUpgrade este utilitarul Java distribuit împreună cu Oracle Database care începând cu 21c a devenit instrumentul unic pentru gestionarea întregului ciclu de viață al upgrade-ului: analiza pre-upgrade, corectarea automată a problemelor detectate, execuția upgrade-ului și fix-up-ul post-upgrade. Înlocuiește definitiv `preupgrade.jar`, care nu mai este distribuit în release-urile recente.

## Cum funcționează

AutoUpgrade operează în patru moduri principale, controlate de parametrul `-mode`:

- **`analyze`** — doar citire, produce un raport de compatibilitate fără să modifice nimic. Este modul de folosit în producție cu săptămâni înainte de fereastra de upgrade.
- **`fixups`** — aplică corecțiile automate pentru problemele rezolvabile fără intervenție umană (ex. recompilarea obiectelor invalide, eliminarea componentelor depreciate).
- **`deploy`** — execută upgrade-ul complet de la source la target database.
- **`upgrade`** — execută doar faza de upgrade a dicționarului, sărind peste fixups și post-upgrade tasks.

```bash
# Analiză pre-upgrade (doar citire, safe în producție)
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze

# Upgrade complet dintr-un config file
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -config upgrade.cfg -mode deploy
```

## Când se utilizează

În fiecare scenariu de upgrade Oracle de la versiunea 12.2 sau superioară către 19c, 21c, 23ai. Cel mai comun caz de utilizare este modul `analyze` ca prim pas al fiecărui proiect de migrare: produce un raport detaliat de obiecte invalide, parametri obsoleți, componente de eliminat și incompatibilități aplicative. Raportul trebuie citit și discutat cu dezvoltatorii aplicativi înainte de planificarea ferestrei de downtime — multe dintre corecții necesită modificări ale codului client care nu pot fi aplicate în timpul weekend-ului de cutover.
