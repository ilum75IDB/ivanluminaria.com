# Handoff sessioni di lavoro

Cartella contenente i recap strutturati delle sessioni con Claude, prodotti dalla skill `/handoff` (`~/.claude/skills/handoff/`).

Convenzione naming: `HANDOFF_YYYY-MM-DD[-NN].md` per handoff individuali, `HANDOFF_YYYY-MM-DD-rollup.md` per i consolidamenti giornalieri prodotti da `/handoff-rollup`.

## Storico

> Ordine **cronologico inverso**: l'handoff più recente è la prima riga della tabella.
> Per una giornata con più handoff, quello valido è quindi il **più in alto** della catena `↳ supersede`.

| File | Tema |
|---|---|
| [`HANDOFF_2026-09-17.md`](./HANDOFF_2026-09-17.md) | Fix link glossario articolo Oracle 12c→21c (5 link errati × 3 lingue + RO Glosar con link + traduzione titoli/note) + 8 mini-pagine glossario nuove (autoupgrade, foreign-datafile-copy × 4 lingue). Riposizionamento titolo ruolo Technical Leader esteso a "per database e Data Warehouse mission-critical" in 4 lingue × 44 file (config, about, posts _index, resumes _index, CV technical-leader, 4 CV pilastri, i18n, cta_copy, CV Markdown EN, prompt setup). Fix 32 seoTitle: rimosso "Ivan Luminaria" duplicato (il layout lo aggiungeva già automaticamente), tutti ora ≤65 chars. Nuova memoria progetto: mai lavorare su `publication-workflow` (branch di web-orchestrator). |
| [`HANDOFF_2026-09-14.md`](./HANDOFF_2026-09-14.md) | Applicato prompt Technical Leader (Passi A→G + extra): brand-bar con ruolo/tagline, pagina Know-How ristrutturata con Technical Leader in evidenza + 4 pilastri, nuova pagina `/resumes/technical-leader/` × 4 lingue, CV EN 2 pagine PDF, sezione `project-management` rinominata "Leadership tecnica e progetti" (slug invariato), CTA fine articolo aggiornata, description sito + card autore + About allineate. Commit unico + merge su main + deploy live triggered. |
| [`HANDOFF_2026-09-12.md`](./HANDOFF_2026-09-12.md) | Allineamento repo iMac alla storia riscritta con `git filter-repo` post-rewrite MacBook (rimozione trailer `Co-Authored-By`/`Claude-Session` + hostname reali + UUID cluster) |
| [`HANDOFF_2026-07-25.md`](./HANDOFF_2026-07-25.md) | Risync `scripts/shell/config/zshrc.txt` per propagazione del nuovo `~/.zshrc` v7.1 (merge cross-Mac iMac v7.0 + MacBook v6.8) — manutenzione dell'ambiente shell, non del dominio funzionale del sito. Quadro completo della sessione multi-progetto in `~/Development/APPLE-MACOS/docs/handoff/HANDOFF_2026-07-25.md` |
| [`HANDOFF_2026-06-26.md`](./HANDOFF_2026-06-26.md) | Health-check ambiente locale (Hugo + Bonjour) + produzione dashboard editoriale con segnalazione 2 anomalie (date duplicate `2026-07-07` su #102/#103 + doppio stato issue #102) |
| [`HANDOFF_2026-06-18-02.md`](./HANDOFF_2026-06-18-02.md) | ↳ supersede `HANDOFF_2026-06-18.md` — pubblicazione live 4 PDF v2026-06 in `static/downloads/`, riallineamento 48 link, chiusura branch `claude/resumes-refactor`, audit branch globale |
| [`HANDOFF_2026-06-18.md`](./HANDOFF_2026-06-18.md) | Bonjour LAN per Hugo + refactor completo 4 CV (PM/DWH/DBA/PL/SQL) × 4 lingue + 8 PDF v2026-06 std+Randstad |
| [`HANDOFF_2026-06-05.md`](./HANDOFF_2026-06-05.md) | Nuova skill `blog-idea-to-issue` (idea→issue blog-article rich) + addendum strategico web-orchestrator #19 |
| [`HANDOFF_2026-06-04.md`](./HANDOFF_2026-06-04.md) | Risync zshrc.txt + merge su main |
