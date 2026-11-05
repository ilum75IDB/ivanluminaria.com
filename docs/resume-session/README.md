# Resume operativo delle sessioni

Cartella contenente i **resume operativi** sintetici delle sessioni, prodotti dalla skill `/handoff` in parallelo all'handoff completo (vedi `docs/handoff/`).

Ogni file di resume è un estratto operativo del corrispondente handoff: pensato per il **riavvio rapido** della sessione successiva (lettura in ~30 secondi), non per ricostruire la cronaca della sessione precedente.

Convenzione naming: `RESUME_YYYY-MM-DD[-NN].md` — simmetrico al naming degli handoff, stesso suffisso progressivo giornaliero. Il resume valido della giornata è quello col suffisso più alto (o il `-rollup` se consolidato).

Letto automaticamente dalla skill `/handoff-read` all'inizio di una nuova sessione.
