# Mockup redesign pagina list "Database Strategy" — issue #76

Tre proposte HTML standalone per valutare visivamente il redesign della pagina `/<lang>/posts/` prima di implementare la scelta definitiva in Hugo (`layouts/list.html`).

## Come aprirle

Doppio clic sui file `.html` dal Finder, o nel browser con **File → Open**:

- `proposal-a.html` — **Section Grid Landing** (editorial magazine)
- `proposal-b.html` — **Two-column con Sidebar sticky**
- `proposal-c.html` — **Tabs + Cards Grid** (con filtro JS)

Nessun server Hugo necessario. I file sono autonomi, caricano Inter da Google Fonts e la cover image reale tramite path relativo.

## Cosa cambia tra le tre proposte

| Proposta | Highlight | JS | Above-the-fold |
|----------|-----------|----|----|
| **A** | 5 card di sezione orizzontali subito dopo l'hero | No | Hero + titolo + griglia sezioni |
| **B** | Sidebar sticky a sinistra con sezioni + contatori | No | Hero + due colonne (sidebar + articoli) |
| **C** | Barra tabs sticky con filtro client-side | Sì (filter) | Hero + titolo + tabs + grid articoli |

## Cosa NON è nei mockup

Per semplicità i mockup rappresentano solo la pagina list. Sono simulati in versione light:

- Navbar top (simulata con link fake)
- Footer (solo un placeholder testuale)
- Immagini degli articoli (thumbnail placeholder grigio)
- Interattività: solo la proposta C ha JS reale per il filtering dei tag

Il resto del sito (dark mode, responsive mobile, menu completo, animazioni fine) verrà implementato quando Ivan sceglierà il modello e passeremo al file Hugo reale.

## Dopo la scelta

Quando Ivan sceglie (es. "proposta A" o un ibrido), il prossimo step è:

1. Tradurre il modello HTML in `layouts/list.html` (Hugo template)
2. Adattare i selettori CSS compatibili col resto di `assets/css/custom.css` (evitando conflitti con la regola globale `a, a:visited`)
3. Aggiungere eventuali `i18n/*.yaml` per label ("Esplora per sezione", "Ultimi articoli", ecc.)
4. Dark mode + responsive
5. Testare con `hservepreview` in tutte e 4 le lingue
6. Merge + chiudere issue #76
