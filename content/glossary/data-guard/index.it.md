---
title: "Data Guard"
description: "Tecnologia Oracle per la replica in tempo reale di un database su un server standby, garantendo alta disponibilità e disaster recovery."
translationKey: "glossary_data_guard"
aka: "Oracle Active Data Guard"
articles:
  - "/posts/oracle/oracle-data-guard"
  - "/posts/oracle/oracle-cloud-migration"
---

**Data Guard** è la tecnologia Oracle che mantiene una o più copie sincronizzate (standby) di un database di produzione (primario). Lo standby riceve e applica continuamente i redo log generati dal primario, rimanendo allineato in tempo reale o quasi.

## Come funziona

Il primario genera redo log con ogni transazione. Questi log vengono trasmessi allo standby via rete, dove vengono applicati in due modi possibili:

- **Physical standby**: applica i redo a livello di blocco (replica esatta, byte per byte)
- **Logical standby**: ricostruisce le istruzioni SQL dai redo e le riesegue

In caso di guasto del primario, lo standby può diventare il nuovo primario tramite **switchover** (pianificato) o **failover** (di emergenza).

## Active Data Guard

La variante Active Data Guard permette di aprire lo standby in sola lettura mentre continua ad applicare i redo. Questo consente di usarlo per report, backup e query analitiche, alleggerendo il carico del primario.

## Modalità di protezione

| Modalità | Comportamento | Data loss |
|----------|--------------|-----------|
| MaxPerformance | Replica asincrona, nessun impatto sulle performance del primario | Possibile (pochi secondi) |
| MaxAvailability | Replica sincrona, degrada a MaxPerformance se lo standby non è raggiungibile | Zero in condizioni normali |
| MaxProtection | Replica sincrona, il primario si ferma se lo standby non conferma | Zero garantito |
