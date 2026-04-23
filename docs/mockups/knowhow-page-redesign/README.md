# Know-How e Impatto page redesign — mockup

Riorganizzazione della pagina `/resumes/` (menu "Know-How e Impatto") per allinearla allo stile card del sito (home, `/posts/`, `/posts/<sezione>/`, `/about/`).

Tutte e 3 le proposte condividono:
- **Header 2-col stile section-page**: cover image 3:2 a sinistra + eyebrow + titolo + tagline + contatore "4 profili" a destra
- **Intro manifesto** con il testo narrativo ("Ho cambiato profondità...")
- **4 profili**: Data Warehouse Architect · Project Manager · Oracle DBA · Oracle PL/SQL
- Per ciascun profilo: narrativa, chip dei settori reali (Telco, Banking, Assicurazioni, ecc.), CTA "Leggi la roadmap" + "Scarica PDF"

## Proposte

- **Proposta A — Grid 2×2 role cards** [`proposal-a.html`](proposal-a.html)
  I 4 profili in griglia 2 colonne, ciascuna card con icona colorata, titolo, narrativa, chip settori e 2 CTA pill (rosso primary per roadmap + outline per PDF). Layout compatto, moderno, tutto visibile above-the-fold su desktop largo.

- **Proposta B — Card orizzontali con sidebar colorata** [`proposal-b.html`](proposal-b.html)
  I 4 profili impilati verticalmente, ciascuno come card 2-col: **sidebar colorata a sinistra** (gradient specifico per ruolo: blu DWH / grigio PM / rosso Oracle / rosso scuro PLSQL) con numero 01-04, icona grande, titolo e **bottone PDF in glass-morphism**; corpo principale a destra con narrativa, chip settori e CTA "Leggi la roadmap →" in fondo. Stile editoriale con colori forti.

- **Proposta C — Timeline verticale "approfondimento"** [`proposal-c.html`](proposal-c.html)
  Concept tematico: "approfondimento verticale" reso graficamente come timeline. Linea rossa centrale verticale, i 4 profili alternati sinistra/destra con pallino colorato sul connettore. Pattern narrativo: il lettore scorre la pagina e "scende in profondità" insieme al racconto. Su mobile la timeline collassa a colonna singola con linea a sinistra.

## Elementi condivisi

- Colori brand: `--ivan-blue #336791`, `--ivan-red #F80000`
- Colori per ruolo: DWH `#1E3A5F` · PM `#4a4a4a` · Oracle `#F80000` · PLSQL `#b30000`
- Cover image 3:2 (formato nativo 1536×1024)
- Pattern hero + intro + profili (stessa sequenza di tutte le altre pagine del sito)
- Responsive: header collassa a 1 col < 1024px, grid/timeline a 1 col < 900px
