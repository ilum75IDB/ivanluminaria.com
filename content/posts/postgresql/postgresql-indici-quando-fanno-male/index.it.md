---
title: "Quando un indice fa più male che bene: pulire PostgreSQL dagli sprechi"
description: "Una banca dati di un Ministero, una tabella con 15 indici di cui 8 mai usati, un junior che voleva capire tutto. Il giro di vite che ha rimesso le query in carreggiata, raccontato come se fosse ieri."
date: "2026-05-26T08:03:00+01:00"
draft: false
translationKey: "postgresql_indici_quando_fanno_male"
tags: ["indexes", "b-tree", "gin", "gist", "performance", "tuning", "query-tuning"]
categories: ["postgresql"]
image: "postgresql-indici-quando-fanno-male.cover.jpg"
---

L'altro giorno un collega mi scrive: "Ho una tabella con dodici indici, è lentissima. Non capisco." Gli ho risposto due righe, ma mentre rileggevo mi è venuto in mente Marco. Era un po' di anni fa, lavoravo nella banca dati centrale di un Ministero — non importa quale, il pattern lo trovi ovunque. E Marco era il junior che mi avevano assegnato.

Aveva due anni e mezzo di PostgreSQL alle spalle, sapeva scrivere query decenti, conosceva `EXPLAIN`. Ma soprattutto aveva una qualità che in quel mestiere ti porta lontano: chiedeva. Non per pigrizia — per sapere. Riformulava i concetti a voce per fissarli, prendeva appunti, anticipava la domanda successiva con cose tipo "aspetta, allora se faccio X mi aspetto Y, giusto?". Il junior che ogni senior vorrebbe avere accanto quando si apre una tabella che fa paura.

Quel giorno ne abbiamo aperta una.

## La tabella che faceva paura

Si chiamava `cittadini_servizi`. Non è il nome vero — il pattern sì.

Ottanta milioni di righe. Una colonna `cittadino_id`, una colonna `servizi_attivi` che era un array di codici (un cittadino poteva avere più servizi attivi: anagrafe, tributario, sanitario, scolastico, ognuno con il suo codice numerico), una geometria con la residenza, un boolean `attivo`, un paio di date, qualche metadata. Niente di esotico.

Sopra ci stavano **quindici indici**.

Marco li ha contati piano, scorrendo `\d cittadini_servizi`. "Quindici. Un po' tanti, no?"

"Dipende. Sono usati?"

"Come si fa a saperlo?"

Ed è qui che è cominciato.

## La diagnosi in cinque minuti

PostgreSQL tiene il conto di quante volte ogni indice viene effettivamente usato. La vista si chiama `pg_stat_user_indexes`. Marco non l'aveva mai aperta.

```sql
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'cittadini_servizi'
ORDER BY idx_scan ASC;
```

L'output è uscito brutale. Otto indici con `idx_scan = 0`. Mai. Usati. Una. Volta.

Marco ha guardato lo schermo. "Mai? Nemmeno per sbaglio?"

"Mai. `idx_scan` parte da zero al boot del database e cresce ogni volta che il planner sceglie quell'indice. Se è ancora a zero dopo settimane di produzione, il planner non l'ha mai considerato utile."

"Allora si tolgono e via."

"Ferma. Prima dobbiamo capire perché ci sono."

Quella frase lì — non eliminare niente prima di aver capito perché esiste — è la regola d'oro quando arrivi su un sistema che non hai costruito tu. Quei `CREATE INDEX` qualcuno li aveva scritti. Magari aveva un motivo. Magari pensava di averlo. Magari non ce l'aveva proprio. Vai a sapere.

Marco ha annuito e ha aperto il git log della repo dei DDL.

## "Ma se ci sono già 15 indici, perché è lenta?"

Domanda giusta. Sbagliata.

Perché parte dal presupposto che "più indici = più veloce", che è uno dei miti più persistenti dei primi anni di PostgreSQL. La realtà è che un indice serve solo se il planner lo sceglie, e il planner sceglie solo gli indici che sono del **tipo giusto** per la query che sta valutando.

Ho aperto una delle query critiche, una di quelle che il monitoring segnalava come lenta:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT cittadino_id
FROM cittadini_servizi
WHERE servizi_attivi && ARRAY[42, 71]
  AND attivo = true;
```

L'operatore `&&` significa "intersezione di array": trovami i cittadini che hanno almeno uno dei servizi 42 o 71 attivo. Una query che il business chiedeva spesso, per campagne mirate.

Tempi: **8.4 secondi**. Plan: `Seq Scan on cittadini_servizi`. Filter: tutti gli 80 milioni di righe.

"Ma c'era un indice su `servizi_attivi`!"

"C'era. Era un B-tree. Il B-tree non sa cosa fare con `&&`."

## Quando il B-tree basta — e quando no

Il **B-tree** è l'indice che il 90% degli sviluppatori conosce e usa. È un albero bilanciato che ordina i valori. Funziona benissimo per uguaglianza (`WHERE col = 'x'`), per range (`WHERE col BETWEEN ... AND ...`), per ordinamento (`ORDER BY col`), per LIKE con prefisso (`WHERE col LIKE 'ABC%'`).

Non funziona invece su:
- Operatori di array (`&&`, `<@`, `@>`)
- Ricerche di sottostringa (`LIKE '%x%'`)
- Containment di JSONB (`@>`)
- Range geometrici (`&&` su geometrie, distanze, bounding box)

Per quello servono altri tipi.

"E noi abbiamo l'array dei servizi sotto un B-tree."

"Esatto. È come avere un sistema di archiviazione cartaceo ordinato per codice fiscale e poi chiedere all'archivista di trovarti tutte le pratiche con almeno una determinata parola chiave dentro. L'ordine non aiuta."

"Quindi serve un altro tipo di indice."

"Serve GIN."

## GIN: l'inverso del B-tree

GIN sta per *Generalized Inverted Index*. Inverso, perché invece di indicizzare le righe per il valore della colonna, indicizza ogni elemento dentro la colonna e tiene una lista di righe che lo contengono.

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi);
```

`USING GIN` è la chiave. PostgreSQL costruisce un mapping: per ogni codice servizio, una lista di righe che lo hanno nell'array. Quando arriva la query con `&&`, l'indice unisce le liste dei due valori cercati e restituisce l'unione. Niente seq scan.

Stessa query, dopo:

```
Bitmap Index Scan on idx_cittadini_servizi_attivi_gin
  ...
Execution Time: 240 ms
```

Da 8400 a 240 millisecondi. Un fattore 35.

Marco ha esultato sottovoce. Poi: "Ma se è così potente, perché non lo si usa sempre?"

"Perché su una scrittura ti costa caro. Ogni `INSERT` o `UPDATE` su quella colonna deve aggiornare tutti i posting in cui quel valore compare. È il prezzo del trovare velocemente — e le tabelle ad alto churn lo pagano caro."

"Quindi GIN sì, ma se la tabella è prevalentemente in lettura."

"Esatto. La nostra `cittadini_servizi` riceveva caricamenti notturni e poi tutto il giorno solo letture. Caso ideale."

## GiST: per quando i dati hanno una forma

L'altra query critica era sulle geometrie. Il Ministero faceva analisi territoriali: "trovami tutti i cittadini con residenza entro 5 km dal punto X, in provincia di Y, attivi". Una query del genere, con un B-tree spaziale finto (perché ne avevano messo uno, ma su quella colonna non era utilizzabile), girava in nested loop e ci metteva mezzo minuto.

GiST — *Generalized Search Tree* — è la famiglia di indici che gestisce dati con geometria, range, similarità. Non ordina i valori in modo lineare, perché alcuni dati non sono ordinabili linearmente (un punto sul piano non sta "prima" o "dopo" un altro). Indicizza invece per *bounding box* gerarchici.

"Ma scusa, perché non un B-tree composito su `(latitudine, longitudine)`?"

Bella domanda. Marco aveva colto il punto giusto.

"Perché il B-tree composito ordina prima per latitudine e poi per longitudine. Se ti serve trovare punti dentro un riquadro `(lat1, lon1, lat2, lon2)`, l'indice riesce a usare il vincolo sulla latitudine — ma poi su ogni riga che passa il filtro lat deve verificare anche lon. Su 80 milioni di righe diventa una mezza scansione."

"Mentre GiST?"

"GiST organizza i punti per regioni geografiche. Quando cerchi un riquadro, scarta intere regioni con un confronto di bounding box. È fatto per quel tipo di query."

```sql
CREATE INDEX idx_cittadini_residenza_gist
ON cittadini_servizi USING GIST (residenza);
```

Stessa query "trova tutti entro 5 km da X", da 28 secondi a 380 ms.

Marco prendeva appunti veloci. "Quindi: B-tree per ordinamento ed equivalenza, GIN per containment di array e jsonb, GiST per geometria e range. C'è altro?"

"Per il momento basta. Esistono BRIN, SP-GiST, hash, ma sono casi più di nicchia. Quando ti serviranno te li ricorderai."

## Bonus: gli indici parziali

C'era un'ultima cosa, prima di tornare alla domanda iniziale (che indici buttare). I cittadini "attivi" erano circa il 35% del totale. Tutto il resto era storico, pratiche chiuse, archiviati. Le query operative filtravano sempre per `attivo = true`.

"Quindi ogni indice contiene il 65% di righe che non vengono mai cercate."

"Esatto. Spreco di spazio e di lavoro per il VACUUM. Soluzione: indice parziale."

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi)
WHERE attivo = true;
```

Quel `WHERE` lì cambia tutto. L'indice contiene solo le righe attive. Sui dati reali, lo spazio occupato si è dimezzato e la velocità è migliorata di un altro 15-20% perché l'indice era più piccolo da scorrere.

"E le query con `attivo = false`?"

"Vanno in seq scan, ma succede una volta a settimana per i report dell'archivio. Lì il seq scan va benissimo."

## La pulizia

A questo punto avevamo:

- Capito perché 8 indici non erano usati (erano duplicati di altri, o B-tree su colonne dove il planner preferiva un seq scan, o riferimenti a vecchie query rimosse)
- Sostituito 2 B-tree inadatti con un GIN e un GiST
- Trasformato 2 indici "completi" in indici parziali

Risultato netto:

| Voce | Prima | Dopo |
|------|------:|-----:|
| Indici totali | 15 | 7 |
| Spazio indici | 42 GB | 18 GB |
| Tempo medio query operative | 4.1 s | 0.4 s |
| Tempo INSERT batch notturno | 38 min | 22 min |

Marco ha guardato la tabella, poi me. "Cioè abbiamo migliorato sia la lettura che la scrittura, semplicemente togliendo cose."

"E mettendo le tre giuste al posto giusto. Ma sì, prevalentemente togliendo. Ogni indice è un costo. Su ogni write. Per sempre."

## La frase che gli ho ripetuto tre volte

Quel giorno gli ho detto la stessa cosa in tre modi diversi, perché volevo che la portasse via:

> Un indice non è "in più che male non fa". Un indice è un costo permanente su ogni `INSERT`, `UPDATE`, `DELETE` — più disco, più WAL, più VACUUM, più contention. Esiste solo se serve. Se non serve, va via.

Marco lo ha scritto nel suo quaderno. Anni dopo è diventato lui il senior in un altro progetto. Mi è arrivato un messaggio: *"Mi è capitata una tabella con ventidue indici. Otto a zero. Ho fatto la pulizia. Pensavo a te."*

Quella è la cosa più bella che un junior ti possa dire.

------------------------------------------------------------------------

## Glossario

**[B-tree](/it/glossary/b-tree/)** — La struttura ad albero bilanciato usata per la maggior parte degli indici. Funziona benissimo per uguaglianza, range e ordinamento. Non sa gestire array, sottostringhe interne, geometrie.

**[GIN Index](/it/glossary/gin-index/)** — *Generalized Inverted Index*. Indicizza singoli elementi dentro valori composti (array, JSONB, full-text). Veloce in lettura su containment, lento in scrittura su tabelle ad alto churn.

**[GiST Index](/it/glossary/gist-index/)** — *Generalized Search Tree*. Indicizza dati con struttura geometrica o di range usando bounding box gerarchici. Indispensabile per geometrie, range temporali, similarità.

**[pg_stat_user_indexes](/it/glossary/pg-stat-user-indexes/)** — Vista di sistema PostgreSQL che traccia quante volte ogni indice è stato usato (`idx_scan`). Lo strumento principe per identificare indici inutili in produzione.

**[Indice Parziale](/it/glossary/indice-parziale/)** — Indice che copre solo un sottoinsieme delle righe della tabella, definito con `WHERE` nella `CREATE INDEX`. Riduce spazio e tempo di manutenzione quando le query filtrano sistematicamente per una condizione.
