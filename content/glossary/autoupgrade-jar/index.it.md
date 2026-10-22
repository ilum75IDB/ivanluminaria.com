---
title: "autoupgrade.jar"
description: "Tool Oracle a riga di comando per automatizzare l'upgrade del database: in modalità analyze genera un report di compatibilità senza modificare l'istanza."
translationKey: "glossary_autoupgrade_jar"
aka: "Oracle AutoUpgrade Utility"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`autoupgrade.jar` è l'utility Oracle distribuita come JAR eseguibile che automatizza l'intero ciclo di upgrade di un database, dalla verifica pre-migrazione fino al completamento. Sostituisce i vecchi script manuali `dbupgrade` e riduce drasticamente il rischio di errore umano nelle operazioni di upgrade su larga scala.

## Come funziona

Lo strumento si invoca tramite `java -jar autoupgrade.jar` con un file di configurazione che descrive sorgente e destinazione. Supporta tre modalità principali:

```bash
# Modalità analyze: solo lettura, nessuna modifica all'istanza
java -jar autoupgrade.jar -config upgrade.cfg -mode analyze

# Modalità fixups: applica le correzioni pre-upgrade identificate
java -jar autoupgrade.jar -config upgrade.cfg -mode fixups

# Modalità deploy: esegue l'upgrade completo
java -jar autoupgrade.jar -config upgrade.cfg -mode deploy
```

In modalità `analyze`, il tool interroga le viste di sistema, verifica la compatibilità degli oggetti, controlla i parametri di inizializzazione e produce un report HTML/text con i problemi rilevati e le azioni consigliate. Nessuna scrittura viene effettuata sul database sorgente.

## Quando si usa

La modalità `analyze` è lo strumento di elezione nella fase di **assessment pre-migrazione**: permette di eseguire più passaggi di analisi su ambienti di produzione senza downtime e senza rischi. È particolarmente utile quando il database sorgente è ancora in versione 11g o 12c e la destinazione è 19c, perché la distanza di versione amplifica il numero di deprecazioni e incompatibilità da gestire.

In contesti finanziari con tablespace da diversi TB, il report generato diventa input diretto per il piano di rollback e per la stima delle finestre di manutenzione.
