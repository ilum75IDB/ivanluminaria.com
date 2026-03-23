---
title: "SCAN Listener"
description: "Single Client Access Name — componenta Oracle RAC care ofera un punct unic de acces catre cluster, distribuind conexiunile intre nodurile disponibile."
translationKey: "glossary_scan_listener"
aka: "Single Client Access Name"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

**SCAN Listener** (Single Client Access Name) este componenta Oracle RAC care ofera un singur nume DNS pentru accesul la cluster. Aplicatiile se conecteaza la SCAN name fara a fi nevoie sa cunoasca nodurile individuale: listener-ul distribuie automat conexiunile intre nodurile active.

## Cum functioneaza

SCAN este un nume DNS care se rezolva la trei adrese IP virtuale (VIP), distribuite intre nodurile clusterului. Cand un client se conecteaza la SCAN name, DNS-ul returneaza una dintre cele trei IP-uri, iar listener-ul de pe acel IP redirectioneaza conexiunea catre nodul cel mai potrivit in functie de serviciul solicitat si de sarcina.

Avantajul este ca connection string-urile aplicatiei nu se schimba niciodata: daca un nod este adaugat sau eliminat din cluster, SCAN gestioneaza totul in mod transparent.

## Configuratie tipica

Un connection string care foloseste SCAN:

    jdbc:oracle:thin:@//scan-name.example.com:1521/service_name

Cele trei SCAN VIP ruleaza pe orice nod al clusterului. Intr-un cluster cu doua noduri, un nod gazduieste doua VIP-uri si celalalt unul (sau invers).

## In migrari

In migrarile catre OCI, SCAN listener-ul este reconfigurat cu DNS-ul noii infrastructuri. Este unul dintre pasii cutover-ului: actualizarea connection string-urilor pentru a indica noul SCAN name pe OCI. Daca naming-ul este bine gestionat, este o modificare intr-un singur punct (connection pool-ul aplicatiei), nu in zeci de fisiere de configurare imprastiate.
