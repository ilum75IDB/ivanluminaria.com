---
title: "Switchover"
description: "Operazione pianificata di Data Guard che inverte i ruoli tra primary e standby senza perdita di dati, reversibile e controllata."
translationKey: "glossary_switchover"
articles:
  - "/posts/oracle/oracle-cloud-migration"
---

Lo **switchover** è un'operazione pianificata di Oracle Data Guard che inverte i ruoli tra il database primary e lo standby. Il primary diventa standby, lo standby diventa primary. Nessun dato viene perso, nessuna transazione va in errore — è un passaggio pulito e controllato.

## Switchover vs Failover

La distinzione è fondamentale:

| | Switchover | Failover |
|---|---|---|
| **Quando** | Pianificato (manutenzione, migrazione) | Emergenza (guasto del primary) |
| **Perdita dati** | Zero | Possibile (dipende dalla modalità) |
| **Reversibilità** | Sì, con un altro switchover | No, lo standby diventa primary in modo permanente |
| **Tempo** | Minuti (tipicamente 1-3) | Secondi-minuti |

## Come si esegue

Con Data Guard Broker, lo switchover è un singolo comando:

    DGMGRL> SWITCHOVER TO standby_db;

Il broker gestisce automaticamente la sequenza: arresto del redo transport, applicazione degli ultimi redo sullo standby, inversione dei ruoli, riavvio del redo transport nella direzione opposta.

## Uso nelle migrazioni

Lo switchover è la strategia preferita per le migrazioni Oracle cross-site. Si configura il Data Guard tra l'ambiente sorgente e quello di destinazione, si lascia sincronizzare, e al momento del cutover si esegue lo switchover. Se qualcosa va storto nella nuova infrastruttura, un secondo switchover riporta tutto al punto di partenza — una rete di sicurezza che Data Pump non può offrire.
