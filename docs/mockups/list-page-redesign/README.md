# Mockup redesign pagina list "Database Strategy" — issue #76

Tre proposte HTML standalone per valutare visivamente il redesign della pagina `/<lang>/posts/` prima di implementare la scelta definitiva in Hugo (`layouts/list.html`).

## Come aprirle

Doppio clic sui file `.html` dal Finder, o nel browser con **File → Open**:

- `proposal-a.html` — **Section Grid Landing** (editorial magazine)
- `proposal-b.html` — **Two-column con Sidebar sticky**
- `proposal-c.html` — **Tabs + Cards Grid** (con filtro JS)
- `proposal-d1.html` — **Ibrida: Sezioni SX + Intro DX + Grid C** 🆕
- `proposal-d2.html` — **Ibrida: Intro SX + Sezioni DX + Grid C** 🆕

Nessun server Hugo necessario. I file sono autonomi, caricano Inter da Google Fonts e la cover image reale tramite path relativo.

## Cosa cambia tra le proposte

| Proposta | Highlight | JS | Above-the-fold |
|----------|-----------|----|----|
| **A** | 5 card di sezione orizzontali subito dopo l'hero | No | Hero + titolo + griglia sezioni |
| **B** | Sidebar sticky a sinistra con sezioni + contatori | No | Hero + due colonne (sidebar + articoli) |
| **C** | Barra tabs sticky con filtro client-side | Sì (filter) | Hero + titolo + tabs + grid articoli |
| **D1** | Sezioni SX + intro testuale DX + grid articoli stile C | No | Hero + tagline + blocco ibrido |
| **D2** | Intro testuale SX + sezioni DX + grid articoli stile C | No | Hero + tagline + blocco ibrido |

## Specifiche della famiglia D (mix tra A e C)

Ivan ha scelto questa direzione il 2026-04-23:
- Grid articoli come proposta **C** (3 colonne cards, senza tabs filter)
- "Esplora per sezione" e intro testuale come proposta **A**
- MA su schermi grandi il blocco A va diviso verticalmente in 2 colonne per dare spazio all'intro testuale più lungo che nei mockup iniziali
- Su mobile tutto collassa in una sola colonna (sezioni sempre sopra l'intro per usabilità)

La differenza tra D1 e D2 è solo l'ordine delle colonne:
- **D1**: sezioni a sinistra, intro a destra (flusso: navigazione → contenuto)
- **D2**: intro a sinistra, sezioni a destra (flusso: contenuto → call-to-action di navigazione)

Ogni sezione è resa come una "row tile" (icona + nome + contatore + freccia), impilata verticalmente nella sua colonna. Effetto pulsantiera chiara.

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
