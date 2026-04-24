# Tags page redesign — mockup

Redesign della pagina `/it/tags/` (taxonomy listing — lista di tutti i tag) per sostituire il layout legacy del tema Congo, attualmente illeggibile (5 colonne strette, conteggi che escono dalla colonna, ~80+ tag impilati senza gerarchia visiva, mobile a una colonna sprecata).

## Proposte

### Desktop

- **Proposta A — Tag cloud editoriale** [`proposal-a.html`](proposal-a.html)
  Pillole rosse con dimensione proporzionale alla popolarità del tag. Header minimo + cloud centrato. Ordinamento per frequenza. Pattern classico tag cloud, immediato visivamente. Hover effect con leggera scala.

- **Proposta B — Raggruppato per sezione** [`proposal-b.html`](proposal-b.html)
  Tag classificati in 6 gruppi tematici (Oracle, PostgreSQL, MySQL, Data Warehouse, Project Management, Misc). Ogni gruppo con header colorato sulla scia delle sezioni del sito. Tag come pillole all'interno. Navigabile per dominio.

- **Proposta C — Indice alfabetico** [`proposal-c.html`](proposal-c.html)
  Layout a 3 colonne con header alfabetici A, B, C... e jump-bar laterale per scorrere rapidamente. Pattern stile rubrica/glossario: scalabile a 200+ tag senza perdere ordine. Più pulito.

### Mobile

- **Proposta A mobile — Pillole responsive** [`mobile-proposal-a.html`](mobile-proposal-a.html)
  Le stesse pillole della Proposta A desktop in modalità wrap fluido (2-3 per riga in base alla lunghezza del tag), touch target ≥ 44px, ordinamento per popolarità.

- **Proposta B mobile — Sezioni collassabili** [`mobile-proposal-b.html`](mobile-proposal-b.html)
  Stessa classificazione per sezione della B desktop, ma con sezioni in accordion: tap su un gruppo apre/chiude la lista di tag. Evita di sopraffare lo schermo con 80 tag tutti aperti.

- **Proposta C mobile — Indice con quick-jump A-Z** [`mobile-proposal-c.html`](mobile-proposal-c.html)
  Lista a una colonna con header alfabetici e barra laterale verticale A-Z (stile Contatti iOS) che scrolla all'inizio della sezione corrispondente.

## Raccomandazione

**Proposta B (raggruppato per sezione)** è la più coerente col resto del sito (lo stesso pattern delle sezioni Oracle/MySQL/PG/DWH/PM è già presente in homepage, search, menu). Aiuta il lettore a trovare tag per dominio invece che doverli scorrere alfabeticamente. Il costo: serve una classificazione manuale o euristica (es. associare ogni tag alla categoria più frequente tra gli articoli che lo usano).

**Proposta C (indice alfabetico)** è la più pulita e scalabile a lungo termine — ottima se il numero di tag crescerà a 200+ nei prossimi 2 anni.

**Proposta A (cloud)** è quella visivamente più di impatto ma con il range attuale (1-8 articoli per tag) la differenza tra "popolare" e "raro" è poca.

## Elementi condivisi

- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
- Font: Inter (già in uso)
- Conteggio articoli sempre visibile nel chip
- Cliccando un tag si va a `/tags/<slug>/` (term page già redesignata, layout card D1)
- Mobile: target touch ≥ 44px, no hover state (only :active)
