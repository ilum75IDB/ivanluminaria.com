---
title: "Cutover"
description: "Momento critico di una migrazione in cui il sistema di produzione viene spostato definitivamente dalla vecchia alla nuova infrastruttura."
translationKey: "glossary_cutover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

Il **cutover** è il momento in cui un sistema di produzione viene spostato dalla vecchia infrastruttura alla nuova. È la fase più visibile di una migrazione — quella che tutti ricordano, nel bene o nel male.

## Anatomia di un cutover

Un cutover ben pianificato segue un runbook dettagliato con passi numerati, tempi stimati, criteri di successo e procedure di rollback per ogni passo. I componenti tipici:

1. **Stop applicativo** — chiusura delle connessioni e verifica che nessuna sessione sia attiva
2. **Sincronizzazione finale** — in una migrazione Data Guard, verifica che transport lag e apply lag siano a zero
3. **Switchover/migrazione** — l'operazione tecnica che trasferisce il servizio
4. **Validazione** — test di connettività, query di verifica, test funzionali
5. **Apertura graduale** — riammissione progressiva degli utenti

## Downtime e finestre

Il downtime di un cutover è il tempo tra la disconnessione dell'ultimo utente e la riconnessione del primo. Con Data Guard switchover, il downtime può essere dell'ordine di minuti. Con Data Pump, può essere di ore o giorni.

La finestra di cutover si pianifica nei momenti di minor utilizzo: notti, weekend, festività. Ma "minor utilizzo" non significa "zero utilizzo" — in aziende manifatturiere con turni h24, non esiste un momento in cui il database non serve a nessuno.

## Rollback

Ogni cutover deve avere un piano di rollback. Con Data Guard, il rollback è un secondo switchover — relativamente semplice. Con Data Pump, il rollback significa riavviare il database originale e accettare la perdita delle transazioni avvenute dopo l'inizio della migrazione. La qualità del piano di rollback è inversamente proporzionale alla probabilità di doverlo usare — ma guai a non averlo.
