# Search page redesign — mockup

Redesign dell'overlay di ricerca del sito per risolvere i problemi emersi dallo screenshot di produzione:

1. **Markdown srotolato come testo** — l'indice Fuse.js contiene il body markdown grezzo (`#`, `**`, newline) stampato come testo.
2. **Data `1 gennaio 0001`** su voci glossario senza date valida.
3. **Tutti i risultati hanno lo stesso peso visivo** — articoli, glossario e tag indistinguibili.
4. **Descrizioni troppo lunghe** che rompono la scannability.
5. **Freccia → in fondo ad ogni card** decorativa, confusa (tutta la card è cliccabile).

## Proposte

- **Proposta A — Editoriale raggruppato** [`proposal-a.html`](proposal-a.html)
  Risultati raggruppati per tipo (Articoli → Glossario → Tag), ognuno con intestazione + conteggio. Articoli: card D1 con thumbnail, sezione, data, reading time, excerpt 1 riga. Glossario: riga sottile (titolo + descrizione tagliata). Tag: chip orizzontali in una sola riga. **Molto coerente col resto del sito** (lista D1, section-page, home).

- **Proposta B — Command palette (stile Spotlight/Raycast)** [`proposal-b.html`](proposal-b.html)
  Densissima, 1 riga per risultato, icona tipo a sinistra. Navigazione da tastiera con footer scorciatoie (↑↓ Naviga, ↵ Apri, Esc Chiudi). Ordine: Articoli → Glossario → Tag. **Veloce per power user**, ma cambia linguaggio visivo rispetto al resto del sito.

- **Proposta C — Split column (lista + preview)** [`proposal-c.html`](proposal-c.html)
  Lista stretta a sinistra (1 riga per risultato) + preview card a destra che cambia in hover/focus con cover image, metadati e excerpt dell'articolo evidenziato. Mobile collassa a colonna singola. **Esperienza ricca**, ma richiede JS aggiuntivo e il valore aggiunto c'è solo su desktop.

## Bug funzionali da fixare (indipendenti dal layout scelto)

Tutti e tre i mockup presuppongono che l'indice Fuse.js venga ripulito prima dell'indicizzazione:

1. **Sostituire `content` con `summary` o `plainify`** nel template dell'index (rimuovere markdown grezzo).
2. **Nascondere la data** quando `Date.IsZero` (voci glossario e tag).
3. **Esporre il tipo di risultato** come campo strutturato nell'index (es. `kind: article | glossary | tag`) per permettere alle proposte A/B/C di raggruppare/filtrare.

## Raccomandazione

**Proposta A** — è la più coerente col redesign recente (sezioni, tag page, Know-How, Chi Sono tutti usano lo stile editoriale raggruppato con intestazione + conteggio). Il salto da B/C al resto del sito sarebbe troppo netto.

## Elementi condivisi

- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
- Overlay semi-trasparente con backdrop-blur
- Modal centrato, max-width 900px
- Input search in cima con icona lente + bottone chiusura
- Font: Inter (già in uso sul sito)
- Simulazione query: "bin" (stessa query dello screenshot di produzione per confronto diretto)
