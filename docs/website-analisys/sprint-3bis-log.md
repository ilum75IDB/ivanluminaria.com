# Sprint 3-bis — Article TOC (sticky sidebar navigation)

**Data apertura**: 2026-05-15
**Branch**: `claude/plan-may-articles-YrcWA`
**Tipo**: UX/SEO enhancement
**Effort stimato**: M (~3-4 ore implementazione + 4 lingue di i18n labels)
**Rischio**: Basso (additive, non rompe layout esistente)

## Razionale

Articoli lunghi (8-12 H2, ~2.000+ parole) sono difficili da navigare. Un lettore senior che cerca una sezione specifica (es. "configurare auto-vacuum cost-delay") deve fare scroll lungo. Un TOC sticky nella sidebar sinistra, **tra badge autore e badge progress di lettura**, lo lascia atterrare direttamente sulla sezione.

Benefici:
- **UX senior**: skim+jump rapido per chi cerca un dettaglio specifico
- **SEO**: Google estrae i jump-link per i risultati ricchi ("In this article: jump to...")
- **Engagement**: tempo medio lettura ↑ (lettori che restano sull'articolo invece di lasciarlo)
- **Stessi articoli funzionano anche come reference**: ci si può tornare sopra direttamente da `https://ivanluminaria.com/it/posts/.../#explain-analyze`

## Implementazione (dopo scelta del mockup)

1. Nuovo partial `layouts/_partials/article-toc.html` — Hugo `replaceRE` o `findRE` sul `.Content` per estrarre tutti gli `<h2 id="...">`
2. Inserimento in `layouts/_partials/author-sidebar.html` o `single.html` tra `author-sidebar-card` e `reading-percent-sidebar`
3. CSS nuovo in `assets/css/custom.css` (sezione "TOC sidebar")
4. **Opzione C**: JS per scroll-spy con IntersectionObserver (~20 righe inline)
5. i18n: label "Indice articolo" → IT/EN/ES/RO in `i18n/{lang}.toml` (creare se non esiste)
6. Test responsive: mobile collassa o si sposta in alto?

## Mockup HTML stand-alone (per scelta)

| File | Variante | Caratteristica chiave |
|------|----------|------------------------|
| `option-a-clean.html` | Lista pulita | Solo H2, link sottolineato in rosso al hover |
| `option-b-numbered.html` | Numerata editoriale | 01, 02, 03... in blu PostgreSQL, stile rivista |
| `option-c-active-scroll.html` | Active scroll-spy | Pallino rosso "tu sei qui" che si sposta col scroll (richiede JS) |
| `option-d-compact.html` | Accordion compatto | Collassabile con badge contatore "8" |

Aprire ciascun file nel browser per vederlo (sono stand-alone, niente build Hugo).

## Decisione utente

- [ ] Mockup scelto: __________________
- [ ] Variante anche per mobile?
- [ ] Includere anche H3 (sotto-titoli) o solo H2?
- [ ] Label "Indice"/"In questo articolo"/"Indice articolo"?

## Stato

- [x] Mockup HTML generati (4 varianti) — commit `<prossimo>`
- [ ] Scelta variante (in attesa Ivan)
- [ ] Implementazione partial Hugo
- [ ] CSS + i18n labels
- [ ] Test su articoli lunghi (pg-stat-statements, vacuum-autovacuum) e corti (smartworking)
- [ ] Mobile responsive check
- [ ] Push + deploy
