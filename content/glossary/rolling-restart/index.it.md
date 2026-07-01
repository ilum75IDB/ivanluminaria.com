---
title: "Rolling Restart"
description: "Procedura di riavvio sequenziale dei nodi di un cluster che mantiene il servizio attivo, applicando modifiche senza downtime."
translationKey: "glossary_rolling_restart"
aka: "Riavvio sequenziale, riavvio a rotazione"
articles:
  - "/posts/mysql/articolo-mysql-saturazione-swap-su-innodb-cluster-3-nodi-analisi-e-fix-dei-param"
---

Il **rolling restart** è la tecnica con cui si riavviano i nodi di un cluster uno alla volta, lasciando sempre attivi gli altri. Il servizio rimane disponibile per i client durante l'intera operazione, a patto che il cluster mantenga il quorum necessario per eleggere un primary e gestire le scritture.

## Come funziona

Su un InnoDB Cluster a 3 nodi, la sequenza tipica è:

1. Identificare il nodo da riavviare (preferibilmente un secondary).
2. Verificare che il cluster sia `ONLINE` e che tutti i membri siano sincronizzati.
3. Riavviare il nodo (`systemctl restart mysqld` o equivalente).
4. Attendere che il nodo rientri nel gruppo prima di procedere con il successivo.

```bash
# Verifica stato cluster prima di ogni step
mysqlsh -- cluster status
```

Il nodo riavviato si riconnetterà al gruppo tramite Group Replication e recupererà le transazioni mancanti via distributed recovery. Solo dopo aver confermato il suo stato `ONLINE` si procede con il nodo successivo.

## Quando si usa

Il rolling restart è la procedura standard ogni volta che occorre applicare modifiche ai parametri di configurazione di MySQL (`my.cnf`) che richiedono un riavvio del processo, come variazioni di `innodb_buffer_pool_size`, `innodb_log_file_size` o parametri Group Replication. È anche il metodo usato per applicare patch di sistema operativo o aggiornamenti di versione minori senza finestre di manutenzione programmate.

Il limite principale è il tempo: con nodi che hanno un backlog di transazioni significativo, il recovery del nodo riavviato può richiedere diversi minuti, allungando la finestra operativa complessiva.
