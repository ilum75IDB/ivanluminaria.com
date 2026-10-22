---
title: "SQL*Net roundtrips to/from client"
description: "Statistica Oracle che conta gli scambi di rete tra client e database. Valori elevati segnalano applicazioni chatty penalizzate da latenze WAN."
translationKey: "glossary_sql_net_roundtrips_to_from_client"
aka: "SQL*Net message roundtrips"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

`SQL*Net roundtrips to/from client` è una statistica di sessione Oracle che conta quante volte client e database si scambiano un messaggio di rete completo durante l'esecuzione di una sessione. Non misura byte trasferiti, ma il numero di viaggi di andata e ritorno sul canale SQL*Net — ogni FETCH, ogni chiamata di procedura, ogni risposta del server incrementa il contatore.

## Come funziona

Oracle espone il valore tramite la vista `V$SESSTAT` (o `V$MYSTAT` per la sessione corrente), unita a `V$STATNAME`:

```sql
SELECT s.value AS roundtrips
FROM   v$mystat s
JOIN   v$statname n ON n.statistic# = s.statistic#
WHERE  n.name = 'SQL*Net roundtrips to/from client';
```

Ogni ciclo request/response tra il layer applicativo e il listener Oracle conta come un roundtrip. Con `arraysize` basso o fetch riga per riga, il numero di roundtrips cresce linearmente con le righe restituite. Aumentare `arraysize` (o usare `BULK COLLECT` lato PL/SQL) riduce i roundtrips aggregando più righe per messaggio.

## Contesto operativo

Il valore diventa critico quando il database è raggiunto via WAN o cloud VPN, dove ogni roundtrip aggiunge decine di millisecondi. Un'applicazione che esegue 10 000 roundtrips su una LAN da 0,1 ms accumula 1 secondo di latenza; sulla stessa WAN a 30 ms accumula 5 minuti. Questo è il profilo tipico di un lift-and-shift non ottimizzato: le query sono identiche, ma il tempo di risposta percepito crolla.

Il rapporto tra `SQL*Net roundtrips` e il numero di righe elaborate (o di transazioni COMMIT) è l'indicatore chiave: un'applicazione ben progettata mantiene il rapporto basso tramite batch fetch, connection pooling e riduzione delle chiamate remote superflue.
