---
title: "pt-heartbeat"
description: "Tool di Percona Toolkit che misura il lag di replica MySQL scrivendo timestamp sul master e confrontandoli sullo slave. Più affidabile di Seconds_Behind_Master."
translationKey: "glossary_pt_heartbeat"
aka: "Percona Toolkit Heartbeat"
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

`pt-heartbeat` è uno strumento di Percona Toolkit progettato per misurare il lag di replica MySQL in modo diretto e affidabile. A differenza della metrica nativa `Seconds_Behind_Master`, che può restituire valori fuorvianti in presenza di errori di replica o di connessione interrotta, `pt-heartbeat` misura il ritardo reale osservando dati scritti sul master e letti sullo slave.

## Come funziona

Il tool opera in due modalità distinte, tipicamente avviate come processi separati:

```bash
# Sul master: scrive un timestamp in una tabella dedicata ogni N secondi
pt-heartbeat --host=master-host --user=repl --password=secret \
  --database=percona --update --interval=1

# Sullo slave: legge la tabella e calcola il delta rispetto all'ora corrente
pt-heartbeat --host=slave-host --user=repl --password=secret \
  --database=percona --monitor --master-server-id=1
```

La tabella `heartbeat` (creata automaticamente al primo avvio) contiene un timestamp aggiornato dal processo `--update`. Il processo `--monitor` sullo slave legge quel valore e calcola la differenza rispetto all'orario locale: il risultato è il lag effettivo in secondi, con precisione al centesimo.

## Quando si usa

`pt-heartbeat` è lo strumento di riferimento per l'alerting in produzione quando `Seconds_Behind_Master` non è sufficiente. I casi tipici sono:

- **Replica interrotta**: `Seconds_Behind_Master` restituisce `NULL`, mentre `pt-heartbeat` continua a mostrare il lag crescente.
- **Replica multi-source o con filtri**: il calcolo nativo può essere impreciso; il timestamp scritto sul master non mente.
- **Integrazione con sistemi di monitoraggio**: l'output di `--monitor` è parsabile da Nagios, Prometheus (via exporter) o qualsiasi script bash.

Il limite principale è la necessità di un processo attivo sul master: se il processo `--update` si ferma, il lag misurato cresce indefinitamente anche se la replica è sana.
