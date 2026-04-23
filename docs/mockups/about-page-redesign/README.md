# About page redesign — mockup

Riorganizzazione della pagina "Chi Sono" (`/about/`) per allinearla allo stile card del resto del sito (home, `/posts/`, `/posts/<sezione>/`).

**Vincolo**: la card in alto con avatar + info professionali è preservata nel formato attuale (stessa struttura interna). In tutte e 3 le proposte è wrappata in una card bianca con bordo + border-radius + shadow soft, coerente con le altre card del sito.

## Proposte

- **Proposta A — Profile card + split prose/TOC** [`proposal-a.html`](proposal-a.html)
  Header profile card. Sotto: split 2-col come nella section-page:
  - **Sinistra**: un'unica card prose con tutto il contenuto (manifesto narrativo + H2 sezioni + quote finale dentro un blockquote stile evidenziato)
  - **Destra**: sidebar sticky "In questa pagina" con link ancora alle 3 H2 sezioni
  Pattern molto coerente con l'esperienza delle pagine sezione.

- **Proposta B — Cards sequenziali con icone** [`proposal-b.html`](proposal-b.html)
  Header profile card. Sotto, sequenza di card separate:
  - Manifesto in card highlight (sfondo gradient + bordo sinistro rosso)
  - 3 section card bianche con icona emoji (🔧 Come lavoro / 🎯 Visione / 🎨 Fuori dal database)
  - In "Fuori dal database": griglia di "passion pill" (fotografia, sax, chitarra, cucina, scacchi)
  - Quote finale in hero quote card full-width (sfondo ivan-blue, testo bianco)

- **Proposta C — Minimal narrative** [`proposal-c.html`](proposal-c.html)
  Header profile card. Sotto: layout singolo, centrato (max 900px), no card:
  - Intro narrativa in stile editoriale (font più grande, colore titolo)
  - Testo scorre in narrativa continua
  - H2 sezioni con **accent strip** rosso verticale a sinistra (pattern tipografico minimal)
  - Quote finale con border top/bottom, virgolette rosse, testo blu
  - Separatori discreti (linea + puntino rosso) tra le macro-sezioni
  Approccio più letterario, meno "componentizzato".

## Elementi condivisi

- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
- Profile header card: bianca, bordo, shadow soft (coerente con section-page-header e home-hero-card)
- Avatar preservato (180px, rounded-full, border 4px #f1f5f9, shadow-xl)
- Responsive: a <900px la profile card collassa a singola colonna centrata
- Font: Inter (già in uso sul sito)
