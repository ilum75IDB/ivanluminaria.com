# Reading Progress Bar — Mockup di confronto

Mockup HTML autonomi per la issue #92. Apri ciascun file direttamente nel browser (doppio click) e scrolla il contenuto dell'articolo per vedere il comportamento della barra.

Ogni mockup riproduce la navbar fissa del sito (70px, z-index 9999), usa la palette del brand (`--ivan-red` `#F80000`, `--ivan-blue` `#336791`), il font Inter, e contiene lo stesso testo fittizio (estratto dall'articolo MySQL #86) per consentire un confronto a parità di contenuto.

## Le 5 varianti

| # | File | Posizione | Spessore | Colore | Extra |
|---|---|---|---|---|---|
| 1 | `01-thin-under-navbar.html` | sotto navbar (top: 70px) | 3px | rosso brand pieno | — |
| 2 | `02-bold-above-navbar.html` | sopra navbar (top: 0) | 5px | rosso brand pieno | navbar shiftata di 5px |
| 3 | `03-gradient-under-navbar.html` | sotto navbar | 4px | gradient rosso → blu | track grigio chiaro |
| 4 | `04-thin-with-percent-badge.html` | sotto navbar | 3px | rosso brand pieno | badge percentuale in basso a destra (appare > 5% e scompare > 98%) |
| 5 | `05-ultra-thin-track.html` | sotto navbar | 2px | blu Postgres | track blu chiaro 15% per contesto visivo |

## Cosa valutare confrontandoli

- **Visibilità**: una barra di 2px è discreta, una di 5px è in faccia. Quale serve al lettore senza distrarlo?
- **Posizione**: sotto la navbar si confonde col layout esistente, sopra la navbar è più visibile ma è la prima cosa che si vede
- **Colore**: rosso brand (energia), blu Postgres (calma), gradient (doppia identità). Coerenza con la voce del blog?
- **Track sì/no**: il track (#5 e #3) mostra "quanto manca", il fill puro (#1, #2, #4) mostra "quanto fatto". Diversa filosofia
- **Badge percentuale (#4)**: utile per articoli lunghi? Distrazione su mobile?

## Suggerimento di lettura

Ti consiglio di aprirli **uno dopo l'altro nello stesso ordine** (1, 2, 3, 4, 5), scrollando dall'inizio alla fine ogni volta. Dopo il quinto saprai quale dei cinque ti convince di più.

Quando hai scelto, fammi sapere e implemento la variante scelta direttamente nel sito (~50 righe di codice, 4 file modificati come da piano in #92).
