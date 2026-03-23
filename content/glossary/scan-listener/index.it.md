---
title: "SCAN Listener"
description: "Single Client Access Name — componente Oracle RAC che fornisce un unico punto di accesso al cluster, distribuendo le connessioni tra i nodi disponibili."
translationKey: "glossary_scan_listener"
aka: "Single Client Access Name"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

Lo **SCAN Listener** (Single Client Access Name) è il componente di Oracle RAC che fornisce un unico nome DNS per l'accesso al cluster. Le applicazioni si connettono allo SCAN name senza dover conoscere i singoli nodi: il listener distribuisce automaticamente le connessioni tra i nodi attivi.

## Come funziona

Lo SCAN è un nome DNS che risolve a tre indirizzi IP virtuali (VIP), distribuiti tra i nodi del cluster. Quando un client si connette allo SCAN name, il DNS restituisce uno dei tre IP, e il listener su quell'IP redirige la connessione al nodo più appropriato in base al servizio richiesto e al carico.

Il vantaggio è che i connection string dell'applicativo non cambiano mai: se un nodo viene aggiunto o rimosso dal cluster, lo SCAN gestisce tutto in modo trasparente.

## Configurazione tipica

Un connection string che usa lo SCAN:

    jdbc:oracle:thin:@//scan-name.example.com:1521/service_name

I tre SCAN VIP girano su qualsiasi nodo del cluster. In un cluster a due nodi, un nodo ospita due VIP e l'altro uno (o viceversa).

## Nelle migrazioni

Nelle migrazioni a OCI, lo SCAN listener viene riconfigurato con il DNS della nuova infrastruttura. È uno dei passaggi del cutover: aggiornare i connection string per puntare al nuovo SCAN name su OCI. Se il naming è gestito bene, è una modifica in un punto solo (il connection pool dell'applicativo), non in decine di file di configurazione sparsi.
