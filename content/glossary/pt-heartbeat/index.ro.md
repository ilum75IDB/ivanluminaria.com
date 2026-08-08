---
title: "pt-heartbeat"
description: "Unealtă Percona Toolkit care măsoară lag-ul de replicare MySQL scriind timestamp-uri pe master și comparându-le pe slave. Mai fiabilă decât Seconds_Behind_Master."
translationKey: "glossary_pt_heartbeat"
aka: "Percona Toolkit Heartbeat"
articles:
  - "/posts/mysql/replica-mysql-quando-lo-slave-resta-indietro-e-nessuno-se-ne-accorge"
---

`pt-heartbeat` este un utilitar din Percona Toolkit conceput pentru a măsura lag-ul de replicare MySQL în mod direct și fiabil. Spre deosebire de metrica nativă `Seconds_Behind_Master` — care poate returna valori înșelătoare în caz de erori de replicare sau pierdere a conexiunii — `pt-heartbeat` măsoară întârzierea reală urmărind date scrise pe master și citite pe slave.

## Cum funcționează

Unealta rulează în două moduri distincte, de obicei ca procese separate cu rulare continuă:

```bash
# Pe master: scrie un timestamp într-un tabel dedicat la fiecare N secunde
pt-heartbeat --host=master-host --user=repl --password=secret \
  --database=percona --update --interval=1

# Pe slave: citește tabelul și calculează delta față de ora curentă
pt-heartbeat --host=slave-host --user=repl --password=secret \
  --database=percona --monitor --master-server-id=1
```

Tabelul `heartbeat` (creat automat la prima pornire) conține un timestamp actualizat de procesul `--update`. Procesul `--monitor` de pe slave citește acea valoare și calculează diferența față de ora locală: rezultatul este lag-ul efectiv în secunde, cu precizie la sutimi.

## Când se folosește

`pt-heartbeat` este instrumentul de referință pentru alerting în producție atunci când `Seconds_Behind_Master` nu este suficient. Scenariile tipice includ:

- **Replicare întreruptă**: `Seconds_Behind_Master` returnează `NULL`, în timp ce `pt-heartbeat` continuă să raporteze lag-ul în creștere.
- **Replicare multi-source sau cu filtre**: calculul nativ poate fi inexact; timestamp-ul scris pe master reprezintă sursa de adevăr.
- **Integrare cu sisteme de monitorizare**: ieșirea `--monitor` este parsabilă de Nagios, Prometheus (prin exporter) sau orice script bash.

Limitarea principală este dependența de un proces activ pe master: dacă procesul `--update` se oprește, lag-ul măsurat crește indefinit chiar dacă replicarea în sine funcționează corect.
