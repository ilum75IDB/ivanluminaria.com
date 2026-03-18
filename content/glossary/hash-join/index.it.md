---
title: "Hash Join"
description: "Hash Join — strategia di join ottimizzata per grandi volumi di dati, basata su una hash table costruita in memoria."
translationKey: "glossary_hash_join"
aka: "Hash Join"
articles:
  - "/posts/postgresql/explain-analyze-postgresql"
---

**Hash join** è una strategia di join progettata per grandi volumi di dati. Funziona in due fasi: prima costruisce una struttura dati in memoria, poi la usa per trovare le corrispondenze in modo efficiente.

## Come funziona

Il database legge la tabella più piccola (build side) e costruisce una hash table in memoria, indicizzando le righe per la colonna di join. Poi scansiona la tabella più grande (probe side) e per ogni riga cerca la corrispondenza nella hash table con un lookup O(1).

La complessità è lineare — proporzionale alla somma delle righe delle due tabelle, non al prodotto come nel nested loop. Non servono indici: la hash table sostituisce temporaneamente l'indice.

## Quando è la scelta giusta

L'optimizer sceglie l'hash join quando entrambe le tabelle sono grandi e non ci sono indici utili, oppure quando le statistiche indicano che il numero di righe da combinare è troppo alto per un nested loop efficiente. È una delle strategie più comuni nei data warehouse e nei report che aggregano milioni di righe.

## Cosa può andare storto

Il punto debole è la memoria. La hash table deve stare in `work_mem`: se la tabella più piccola non ci sta, il database scrive batch su disco (batched hash join), con un degrado significativo delle performance.

- **work_mem troppo basso**: la hash table viene spezzata in batch su disco, moltiplicando l'I/O
- **Stime errate**: l'optimizer sceglie come build side la tabella sbagliata perché le statistiche indicano meno righe di quelle reali
- **Skew nei dati**: se un valore nella colonna di join domina la maggior parte delle righe, un bucket della hash table diventa enorme mentre gli altri restano vuoti
