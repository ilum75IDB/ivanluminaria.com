---
title: "RPO"
description: "Recovery Point Objective — la quantità massima di dati che un'organizzazione può permettersi di perdere in caso di disastro, misurata in tempo."
translationKey: "glossary_rpo"
aka: "Recovery Point Objective"
articles:
  - "/posts/oracle/oracle-data-guard"
---

**RPO** (Recovery Point Objective) è la quantità massima di dati che un'organizzazione può permettersi di perdere in caso di guasto o disastro. Si misura in tempo: un RPO di 1 ora significa che si accetta di perdere al massimo l'ultima ora di transazioni.

## Come si determina

L'RPO dipende dalla strategia di backup e replica:

| Strategia | RPO tipico |
|-----------|-----------|
| Backup notturno su nastro | 12-24 ore |
| Backup + archived log su storage remoto | 1-4 ore |
| Data Guard asincrono (MaxPerformance) | Pochi secondi |
| Data Guard sincrono (MaxAvailability) | Zero |

## RPO vs RTO

RPO e RTO sono complementari ma distinti:

- **RPO**: quanti dati puoi perdere (guarda indietro nel tempo)
- **RTO**: quanto tempo ci vuole per ripristinare il servizio (guarda avanti nel tempo)

Un'organizzazione può avere RPO=0 (zero data loss) ma RTO=4 ore (ci vogliono 4 ore per ripartire), o viceversa.

## Perché conta

L'RPO determina l'investimento necessario in infrastruttura di replica. Passare da RPO=24 ore a RPO=0 può costare ordini di grandezza in più, ma il costo va confrontato con il valore dei dati persi — come nel caso di sei ore di polizze assicurative non emesse.
