# Reading Progress Bar — Mockup di confronto

Mockup HTML autonomi per la issue #92. Apri ciascun file direttamente nel browser (doppio click) e scrolla il contenuto dell'articolo per vedere il comportamento della barra.

Tutti i mockup ora riproducono il **layout reale del sito**:
- Navbar fissa con brand "IVAN LUMINARIA" + menu (CHI SONO, DATABASE STRATEGY, KNOW-HOW E IMPATTO) + selettore lingua + search icon
- Layout a due colonne: **sidebar 160px** con badge autore (foto + nome + ruoli) + **colonna articolo 1fr**
- Cover image, breadcrumbs, titolo, data + reading time, tag chips
- Container max-width 1280px centrato
- Contenuto identico in tutti i mockup (estratto dall'articolo MySQL #86) per confronto a parità di scroll

## Le 8 varianti

| # | File | Linea | Spessore | Posizione | Colore | Extra |
|---|---|---|---|---|---|---|
| 1 | `01-thin-under-navbar.html` | linea piena | 3px | sotto navbar | rosso brand | — |
| 2 | `02-bold-above-navbar.html` | linea piena | 5px | sopra navbar | rosso brand | navbar shiftata di 5px |
| 3 | `03-gradient-under-navbar.html` | linea piena | 4px | sotto navbar | gradient rosso→blu | track grigio chiaro |
| 4 | `04-thin-with-percent-badge.html` | linea piena | 3px | sotto navbar | rosso brand | badge % bottom-right, **width variabile** (mostra il jitter) |
| 5 | `05-ultra-thin-track.html` | linea piena | 2px | sotto navbar | blu Postgres | track blu 15% |
| 6 | `06-percent-bottom-right.html` | linea piena | 3px | sotto navbar | rosso brand | **badge % width fissa (56px) bottom-right** |
| 7 | `07-percent-top-right.html` | linea piena | 3px | sotto navbar | rosso brand | **badge % width fissa (56px) top-right** (sotto navbar) |
| 8 | `08-percent-under-author.html` | linea piena | 3px | sotto navbar | rosso brand | **4 varianti di sfondo** del badge nella sidebar (A grigio chiaro / B rosso / C blu / D grigio scuro) |
| 9 | `09-combo-bottomright-sidebar.html` | linea piena | 3px | sotto navbar | rosso brand | **combo finale**: badge grigio scuro bottom-right + badge rosso nella sidebar autore — i due badge si aggiornano sincronizzati |

## Cosa cambia tra 4, 6, 7, 8

Tutti partono dalla stessa base (linea 3px rosso sotto navbar, variante 01 preferita).

- **#4**: badge auto-width per mostrare il problema del jitter (la larghezza cambia da "5%" a "10%" a "100%"). Barra wide-screen.
- **#6**: badge a width fissa 56px + `font-variant-numeric: tabular-nums` → zero jitter, bottom-right discreto. **Barra container-width (1280px centrata), badge persistente fino a fine pagina**
- **#7**: stesso badge fisso, ma in alto a destra (allineato al bordo del container 1280px) → più visibile, segue la lettura naturale. **Barra container-width, badge persistente**
- **#8**: badge integrato nella sidebar autore con label "LETTO" → niente overlay sul contenuto, segue la sticky della sidebar. **Barra container-width, badge persistente**

### Due fix applicati ai mockup 6, 7, 8 (rispetto ai precedenti)

1. **Barra container-width (1280px centrata)** invece di wide-screen — coerente col layout del sito che ha già un `max-width` definito. Sotto i 1280px di viewport, la barra si comporta naturalmente come full-width (perché coincide col viewport)
2. **Badge persistente da 5% in poi** — niente sparizione a 98%. Il "100%" resta visibile come feedback di completamento, sparisce solo se l'utente torna proprio all'inizio della pagina

Sui mockup 1-5 lascio il comportamento "wide + badge che spariva a 98%" come reference storica delle prime versioni.

## Cosa valutare confrontando 6, 7, 8

- **#6 bottom-right**: discreto, fuori dal flusso di lettura. Vantaggio: non distrae. Svantaggio: l'utente potrebbe non accorgersene
- **#7 top-right**: in linea con la barra fissa, più visibile. Vantaggio: vicino alla barra, contesto chiaro. Svantaggio: occupa angolo importante che potrebbe servire per future features
- **#8 sidebar**: integrato visivamente nel layout, niente floating. Vantaggio: pulizia totale, niente overlay. Svantaggio: visibile solo su desktop (la sidebar scompare su mobile)

## Suggerimento di lettura

Aprili nell'ordine 1→8, scrollando dall'inizio alla fine ogni volta. Le varianti più importanti per la decisione finale sono **6, 7, 8** (le tre posizioni del badge fisso).

Quando hai scelto, fammi sapere e implemento la variante scelta direttamente nel sito reale.
