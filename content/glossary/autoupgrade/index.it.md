---
title: "AutoUpgrade"
description: "Utility Java (autoupgrade.jar) che da Oracle 21c è lo strumento unico per analisi pre-upgrade, correzioni e upgrade del database. Sostituisce preupgrade.jar, non più distribuito."
translationKey: "glossary_autoupgrade"
aka: "AutoUpgrade Utility (autoupgrade.jar)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

AutoUpgrade è l'utility Java distribuita con Oracle Database che a partire dalla 21c è diventata lo strumento unico per gestire l'intero ciclo di vita dell'upgrade: analisi pre-upgrade, correzione automatica dei problemi rilevati, esecuzione dell'upgrade e post-upgrade fix-up. Sostituisce definitivamente `preupgrade.jar`, non più distribuito nelle release recenti.

## Come funziona

AutoUpgrade opera in quattro modalità principali, controllate dal parametro `-mode`:

- **`analyze`** — sola lettura, produce un report di compatibilità senza modificare nulla. È la modalità da usare in produzione settimane prima della finestra di upgrade.
- **`fixups`** — applica le correzioni automatiche ai problemi risolvibili senza intervento umano (es. ricompilazione oggetti invalidi, rimozione componenti deprecati).
- **`deploy`** — esegue l'upgrade completo dal source al target database.
- **`upgrade`** — esegue solo la fase di upgrade del dizionario, saltando fixups e post-upgrade tasks.

```bash
# Analisi pre-upgrade (sola lettura, safe in produzione)
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -preupgrade "target_version=21,dir=/tmp/preupg" -mode analyze

# Upgrade completo da un config file
java -jar $ORACLE_HOME_21C/rdbms/admin/autoupgrade.jar \
  -config upgrade.cfg -mode deploy
```

## Quando si usa

In ogni scenario di upgrade Oracle da versione 12.2 o superiore verso 19c, 21c, 23ai. Il caso d'uso più comune è la modalità `analyze` come primo step di ogni progetto di migrazione: produce un report dettagliato di oggetti invalidi, parametri obsoleti, componenti da rimuovere e incompatibilità applicative. Il report va letto e discusso con gli sviluppatori applicativi prima di pianificare la finestra di downtime — molti dei fix richiedono modifiche al codice cliente che non possono essere applicate durante il weekend di cutover.
