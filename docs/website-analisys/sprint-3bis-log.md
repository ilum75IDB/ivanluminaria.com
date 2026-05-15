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

- [x] Mockup HTML generati (4 varianti) — commit `370300b`
- [x] Mockup arricchiti con contenuto reale articolo + voci Fonti/Glossario nel TOC — commit `a114370`, `c948225`
- [x] Scelta variante: **C (active scroll-spy)**
- [x] Implementazione partial Hugo `layouts/_partials/article-toc.html`
- [x] Integrazione in `author-sidebar.html` tra card autore e reading-progress
- [x] CSS `assets/css/custom.css` (sezione "Article TOC sidebar")
- [x] JS scroll-spy `static/js/article-toc-spy.js` (IntersectionObserver, vanilla)
- [x] Include JS in `baseof.html`
- [x] i18n labels in 4 lingue (`article_toc_title`)
- [ ] Test post-deploy: pg-stat-statements (lungo) + smartworking-consulenza-it (corto, < 3 H2 → no TOC)
- [ ] Mobile responsive check (display: none su <768px, ok)
- [ ] Push + deploy

## Logica di esposizione

Il TOC si mostra **solo** se:
- la pagina è in `Section: posts`
- il contenuto ha **>= 3 H2** (articoli corti tipo `pagamenti-60-90-120-giorni` non lo mostrano)
- viewport >= 768px (mobile lo nasconde, è già nascosta la sidebar autore stessa)

## File toccati

| File | Tipo | Linee |
|------|------|------:|
| `layouts/_partials/article-toc.html` | nuovo | 19 |
| `layouts/_partials/author-sidebar.html` | edit | +6 |
| `layouts/baseof.html` | edit | +1 |
| `assets/css/custom.css` | edit | +95 (sezione TOC) |
| `static/js/article-toc-spy.js` | nuovo | 90 |
| `i18n/{it,en,es,ro}.yaml` | edit | +1 ciascuno |
