# Mockup hero card — homepage — issue #77

Tre formati di card per l'**articolo hero** in ogni sezione della homepage (sezione "Latest" + 5 sezioni categoria). Le card **grid** sono identiche in tutti e 3 i mockup (formato D1 già scelto per la pagina list in #76).

## Come aprirli

Doppio clic dal Finder, o nel browser con **File → Open**:

- `proposal-a.html` — **Horizontal 2-col card** (image sx + testo dx)
- `proposal-b.html` — **Vertical stack cinematic** (image wide sopra + testo sotto centrato)
- `proposal-c.html` — **Overlay magazine** (image di sfondo + testo in overlay con gradiente)

Ogni mockup mostra sia una sezione **Latest** che una sezione **categoria** (Oracle), così vedi come il formato hero convive con le grid card.

## Differenze chiave

| Proposta | Feel | Proporzione image hero | Testo sul hero |
|----------|------|------------------------|----------------|
| **A** | Elegante, "lettura-first", simile alla struttura attuale del category hero ma in forma card con bordo/shadow | 16:9, occupa 45% larghezza | A destra dell'immagine, leggibile con sfondo bianco |
| **B** | Pulito, consistency maxima con le grid card, semplicemente "più grande" | 3:1 cinematic, a tutta larghezza | Sotto l'immagine, centrato, come una card D1 ma più prominente |
| **C** | Drammatico, visivo-first, "magazine cover" stile | 21:9 ultra-wide, a tutta larghezza | Overlay bianco su gradiente scuro direttamente sopra l'immagine |

## Considerazioni tecniche

Tutti e 3 i formati:
- Rispettano le brand colors (rosso Oracle, blu Postgres)
- Usano `object-fit: cover` con `object-position: center` per preservare il focus delle cover 16:9 e 3:2
- Hanno hover state (lift + shadow o border rosso)
- Collassano su mobile (<900px): A → vertical, B → riduce l'altezza a 16:9, C → 4:3 più denso con descrizione nascosta
- Mantengono le grid card D1 immutate per consistency con la pagina list già implementata

## Dopo la scelta

Quando Ivan sceglie (o ibrida), il prossimo step è:
1. Modificare `layouts/_partials/home/custom.html`: sostituire il rendering attuale dell'hero (sia in Latest che nelle sezioni categoria) con il formato scelto
2. Estendere `assets/css/custom.css` con le nuove classi (probabilmente `.home-hero-card-*` per coerenza di naming)
3. Testare con `hservepreview` in tutte e 4 le lingue
4. Aggiornare CLAUDE.md (la regola attuale "category hero 2-column structure — Never modify" va aggiornata con il nuovo standard)
5. Merge + chiudere issue #77
