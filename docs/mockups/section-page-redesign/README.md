# Section page redesign — mockup

Riorganizzazione delle pagine sezione (`/posts/<sezione>/`) per allinearle allo stile di home e `/posts/`.

Contenuto esemplificativo: sezione **Project Management** (9 articoli).

## Proposte

- **Proposta A — Minimalista (stile /posts/)** [`proposal-a.html`](proposal-a.html)
  Hero image full-width 21:9 → titolo + tagline → intro centrato (max 760px) → grid D1 6 articoli + load more → pulsantiera "altre sezioni" a fondo pagina (pillole orizzontali)

- **Proposta B — Magazine con hero article** [`proposal-b.html`](proposal-b.html)
  Header compatto 2-col (cover 4:3 + titolo + descrizione + conteggio articoli) → intro centrato → hero card orizzontale dell'articolo più recente → grid D1 degli altri + load more

- **Proposta C — Split intro + sidebar siblings** [`proposal-c.html`](proposal-c.html)
  Hero full-width → titolo + tagline → split (intro a sinistra + sidebar "sezioni" sticky a destra con sezione attiva evidenziata) → hero card + grid D1 + load more

## Proposte D (iterazione dopo feedback utente)

Combinano gli elementi preferiti:
- hero card "In evidenza" dell'articolo più recente (da B)
- sidebar sezioni laterale con sezione attiva evidenziata (da C, riempie spazio a destra dell'intro)
- pulsantiera "esplora altre sezioni" a fondo pagina (da A)

Le due D differiscono solo nell'intestazione: la richiesta era mostrare l'immagine della sezione **intera** (3:2 nativo) ma abbastanza grande.

- **Proposta D1 — Header 2-col big** [`proposal-d1.html`](proposal-d1.html)
  Image 3:2 a sinistra (~50% della pagina, rounded + shadow) + testo a destra: eyebrow, titolo 3.5rem, tagline italic con border-bottom rosso, contatore articoli. Layout orizzontale editoriale.

- **Proposta D2 — Hero centrato magazine** [`proposal-d2.html`](proposal-d2.html)
  Image 3:2 centrata max 900px (più grande, rounded + shadow più marcata), sotto eyebrow + titolo gigante 4rem + tagline italic + pill "9 articoli pubblicati". Layout verticale, stile copertina magazine.

## Elementi condivisi

- Grid card = `article-card.html` già in uso (nessuna nuova classe CSS)
- Hero card = `home-hero-card.html` già in uso
- Load more = stesso pattern di `/posts/`
- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
