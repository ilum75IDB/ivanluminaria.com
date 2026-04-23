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

## Elementi condivisi

- Grid card = `article-card.html` già in uso (nessuna nuova classe CSS)
- Hero card = `home-hero-card.html` già in uso
- Load more = stesso pattern di `/posts/`
- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
