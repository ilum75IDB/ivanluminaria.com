# Annotazioni stilistiche — Sezione PostgreSQL

**Data**: 2026-05-14
**Articoli analizzati**: 4
**Scopo**: lista delle modifiche stilistiche da applicare in batch agli articoli PostgreSQL non ancora revisionati, secondo `docs/STILE_LINGUISTICO.md`. Le modifiche NON sono ancora applicate.

**Articoli esclusi (gia' revisionati)**: `enum-postgresql-paga-o-pesa`, `like-optimization-postgresql`, `postgresql-indici-quando-fanno-male`.

**Criteri applicati**:
- Sono lasciate intatte le occorrenze di "ma" in opposizione retorica tecnica (es. "tempo medio basso, ma volume alto", "funziona, ma con un costo Y"): strumento narrativo legittimo nel registro tecnico-argomentativo.
- Sono lasciate intatte le occorrenze in citazioni dirette tra virgolette, codice e descrizioni tecniche neutre (es. "scelto per errore dall'optimizer", "stima sbagliata di 4 ordini di grandezza" come descrizione di scostamento numerico).
- Sono modificati i "ma" puramente avversativi narrativi a inizio frase, i "problema" generici (sostituibili con "criticità", "situazione", "punto", "questione"), e i casi di `magari` / `forse` / `bisogna` che indeboliscono o impersonalizzano l'affermazione.

---

## explain-analyze-postgresql

**File**: `content/posts/postgresql/explain-analyze-postgresql/index.it.md`
**Modifiche proposte**: 5

| #  | Riga | Originale (frammento)                                                                                                            | Proposto                                                                                                                              | Tema                  | Note                                                                                                                                                  |
|----|------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 110  | "Il problema? Le statistiche si aggiornano con `ANALYZE`..."                                                                      | "Il punto critico? Le statistiche si aggiornano con `ANALYZE`..."                                                                     | Frame mentale         | Frame narrativo di apertura paragrafo, "problema" sostituibile.                                                                                       |
| 2  | 142  | "Ma non mi sono fermato qui. Se il problema si è presentato una volta, si ripresenterà."                                          | "E non mi sono fermato qui. Se la criticità si è presentata una volta, si ripresentera."                                              | Frame mentale + Connessione positiva | "Ma" a inizio frase puramente narrativo + "problema" generico nella stessa frase. Doppia sostituzione per coerenza.                            |
| 3  | 177  | "...hai confermato che il problema era la scelta del join."                                                                      | "...hai confermato che la criticita era la scelta del join."                                                                          | Frame mentale         | Frame narrativo, sostituibile.                                                                                                                        |
| 4  | 198  | "...se `shared read` è molto alto rispetto a `shared hit`, il problema potrebbe essere I/O, non il piano."                       | "...se `shared read` è molto alto rispetto a `shared hit`, il collo di bottiglia potrebbe essere I/O, non il piano."                  | Frame mentale         | "Problema" qui è meglio sostituito con un termine tecnico ("collo di bottiglia") che è piu specifico al contesto.                                     |
| 5  | 216  | "Ma per quel restante 30%, devi leggere. Riga per riga..."                                                                       | "E per quel restante 30%, devi leggere. Riga per riga..."                                                                             | Connessione positiva  | "Ma" a inizio frase di chiusura sezione: la frase precedente non viene contraddetta. "Devi leggere" resta: istruzione tecnica diretta al lettore DBA. |

**Da LASCIARE (motivate)**:
- Riga 15: `"Ho fatto EXPLAIN ANALYZE, ma non capisco cosa c'è che non va. Il piano sembra corretto."` — citazione diretta del collega su Teams, intoccabile.
- Riga 17: "ma la ragione era banale" — opposizione retorica tecnica (problema diagnosticato vs causa banale). Resta.
- Riga 17: "Ma per arrivarci ho dovuto leggere il piano riga per riga" — opposizione retorica forte di paragrafo. Resta.
- Riga 19: "EXPLAIN ANALYZE è uno strumento di diagnostica, non un verdetto. Bisogna saperlo leggere." — qui "bisogna" e' usato con valore enfatico-didattico generale e in chiusura di paragrafo manifesto: segnalato per discussione, ma propendo per lasciarlo (riformulare appiattisce la voce narrativa).
- Riga 27: "L'optimizer decide cosa farebbe, ma non esegue nulla" — opposizione retorica tecnica reale (decide vs esegue). Resta.
- Riga 36: "Ora vedi quanto ha impiegato ogni nodo... Ma manca un pezzo." — opposizione retorica tecnica forte (cosa vedi vs cosa manca). Resta.
- Riga 45: "Senza BUFFERS stai guidando di notte senza fari." — descrizione metaforica, non identitaria. Resta.
- Riga 72: "Se c'è un ordine di grandezza di differenza, hai trovato il problema." — qui "problema" e' il termine tecnico del paragrafo successivo ("problema di statistiche"): resta come segnale diagnostico concreto.
- Riga 91: "Quando la stima è sbagliata di 4 ordini di grandezza, il piano è inevitabilmente sbagliato." — "sbagliata"/"sbagliato" descrivono un fatto numerico (scostamento di 4 ordini di grandezza, piano non funzionante): descrizione tecnica neutra, non giudizio identitario. Restano. Stessa frase: "Su 2 milioni è un disastro" — opposizione retorica tecnica costo/scala, resta.
- Riga 93: "Ma l'optimizer non poteva saperlo con le statistiche che aveva." — opposizione retorica tecnica chiave del paragrafo (scelta corretta in astratto vs limite informativo reale). Resta.
- Riga 95: "hai un problema di statistiche" / "il piano è quasi certamente sbagliato" — descrizioni diagnostiche concrete in registro tecnico. Restano.
- Riga 110: "Ma l'autovacuum lancia ANALYZE solo quando..." — opposizione retorica tecnica reale (esiste vs scatta solo a soglia). Resta.
- Riga 163: "ma oltre raramente porta benefici e rallenta l'ANALYZE stesso" — opposizione retorica tecnica reale (su, ma con limite). Resta.
- Riga 177: "Ma non puoi lasciare `enable_nestloop = off` in produzione..." — opposizione retorica tecnica essenziale (utile in diagnostica vs vietato in produzione). Resta.
- Riga 181: "per confermare quale strategia di join è il problema" — qui "problema" e' termine tecnico-diagnostico specifico (la strategia errata): resta.
- Riga 182: "quando il business è fermo e devi far ripartire una query critica..." — "devi" istruzione tecnica al lettore DBA, registro didattico legittimo. Resta.
- Riga 200: "il piano è ancora sbagliato" — descrizione tecnica neutra (piano non ottimale). Resta.
- Riga 208: `"Ma allora bastava un ANALYZE?"` — citazione diretta del collega, intoccabile.
- Riga 210: "Ma il punto non è il comando." — opposizione retorica chiave del paragrafo. Resta.
- Riga 212: "Sì, ma da cosa dipende?" — opposizione retorica didattica (parallelismo paziente/febbre). Resta.
- Riga 224 (glossario): "scelta per errore dall'optimizer" — locuzione "per errore" = inavvertitamente, idiomatica. Resta.

**STATO**: in attesa di approvazione

---

## pg-stat-statements

**File**: `content/posts/postgresql/pg-stat-statements/index.it.md`
**Modifiche proposte**: 6

| #  | Riga | Originale (frammento)                                                                                                                              | Proposto                                                                                                                                                                                | Tema                  | Note                                                                                                                                                                                                                                              |
|----|------|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 21   | (inserimento nuova frase a chiusura del paragrafo di apertura, dopo "...finisci nel fosso.")                                                       | (aggiungere) "Con qualche eccezione di nicchia — un PgBouncer in modalità multi-tenant aggressiva, una replica logica downstream che riceve solo traffico filtrato — è la prima cosa da installare." | Frame mentale         | **(mitigazione assolutismo titolo)** — il titolo "...la prima cosa da installare su qualsiasi PostgreSQL" è un assolutismo. Aggiungere nelle prime righe del corpo una mitigazione che riconosca i casi limite, senza svuotare il messaggio. |
| 2  | 13   | `"Il database è lento da qualche giorno, ma non sappiamo quale query sia il problema."`                                                              | (LASCIARE — citazione diretta del ticket)                                                                                                                                               | —                     | Citazione tra virgolette dal ticket cliente. Resta intatta.                                                                                                                                                                                       |
| 3  | 62   | "...è un costo che si ripaga al primo problema diagnosticato."                                                                                      | "...è un costo che si ripaga alla prima criticità diagnosticata."                                                                                                                       | Frame mentale         | "Problema" generico narrativo, sostituibile.                                                                                                                                                                                                      |
| 4  | 129  | "...quelle che magari vengono eseguite poche volte ma ciascuna impiega secondi."                                                                    | "...quelle che vengono eseguite poche volte ma ciascuna impiega secondi."                                                                                                               | Precisione            | "Magari" indebolisce l'affermazione. La frase funziona meglio senza, mantenendo solo l'osservazione concreta. (Il "ma" successivo è opposizione retorica tecnica vera — basso volume vs alta durata — e resta.)                              |
| 5  | 172  | "...che potrebbe nascondere un problema recente."                                                                                                   | "...che potrebbe nascondere una criticità recente."                                                                                                                                     | Frame mentale         | Frame narrativo di chiusura paragrafo, "problema" generico.                                                                                                                                                                                       |
| 6  | 200  | "pg_stat_statements ti dice *quale* query è il problema. EXPLAIN ti dice *perché* è un problema."                                                   | "pg_stat_statements ti dice *quale* query è la criticità. EXPLAIN ti dice *perché* è una criticità."                                                                                    | Frame mentale         | Doppia occorrenza di "problema" in struttura parallela: sostituzione coerente in entrambe per non rompere il parallelismo retorico.                                                                                                              |

**Da LASCIARE (motivate)**:
- Riga 13: vedi sopra (citazione ticket).
- Riga 21: "finché la strada è dritta non ti accorgi di nulla, ma alla prima curva finisci nel fosso" — opposizione retorica metaforica forte (apparente normalità vs crisi). Resta.
- Riga 27: "inclusa nella distribuzione ufficiale ma non attiva di default" — opposizione retorica tecnica reale (esiste vs non abilitata). Resta.
- Riga 52: "Il default è 5000, ma su database con molte query diverse conviene alzarlo" — opposizione retorica tecnica (default vs caso reale). Resta.
- Riga 96: "Il tempo medio era basso (1,46 ms) ma il volume la rendeva la più costosa in assoluto" — opposizione retorica tecnica essenziale (tempo unitario vs totale). Resta.
- Riga 100: "...ma l'indice esistente era solo su `created_at`" — opposizione retorica tecnica reale (filtro doppio vs indice singolo). Resta.
- Riga 226: "L'overhead di pg_stat_statements è trascurabile, ma il progetto preferisce non imporre nulla" — opposizione retorica forte (potrebbe vs sceglie di no). Resta. Stessa riga: "un valore ridicolo per qualsiasi produzione, ma il progetto non vuole presumere..." — opposizione retorica funzionale al paragrafo. Resta.
- Riga 230: "Puoi fare tuning quanto vuoi, ma stai indovinando dove intervenire." — opposizione retorica di chiusura sezione. Resta.
- Riga 238: `"Ma perché nessuno ci aveva detto di installare questa estensione?"` — citazione diretta del DBA, intoccabile.
- Riga 240: "Ma se non la installi, non sai cosa non sai." — opposizione retorica chiave del paragrafo (è noto e raccomandato vs senza installarla). Resta.
- Riga 240: "tutto sembra funzionare — finché non funziona più" — uso retorico legittimo (non identitario), descrive il fenomeno della cecità diagnostica. Resta.

**STATO**: in attesa di approvazione

---

## postgresql_roles_and_users

**File**: `content/posts/postgresql/postgresql_roles_and_users/index.it.md`
**Modifiche proposte**: 0

L'articolo è già stilisticamente molto pulito. Nessuna occorrenza di `problema`, `errore`, `magari`, `forse`, `bisogna`, `spero`, `provo`, `cercherò`. Le occorrenze di `ma` non sono presenti come connettori avversativi narrativi (gli unici contesti dove appaiono sono dentro codice o termini come "mario" usato come username di esempio nel `CREATE USER mario;`).

**Eventuali punti di attenzione (segnalati ma non modificati)**:
- Riga 93: "il monitoraggio inizia a lanciare errori" — descrizione tecnica del sintomo (errori SQL applicativi). Resta.
- Riga 103: "Se salti un pezzo, prima o poi paghi il conto." — "prima o poi" e' in elenco della tabella STILE_LINGUISTICO come termine senza commitment temporale. Qui peraltro non si tratta di un commitment dell'autore ma di una **conseguenza inevitabile** descritta al lettore in registro didattico, quindi propendo per lasciarlo. Segnalato per discussione.

**STATO**: in attesa di approvazione (0 modifiche, articolo gia' pulito)

---

## vacuum-autovacuum-postgresql

**File**: `content/posts/postgresql/vacuum-autovacuum-postgresql/index.it.md`
**Modifiche proposte**: 5

| #  | Riga | Originale (frammento)                                                                            | Proposto                                                                                                          | Tema                  | Note                                                                                                                                  |
|----|------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 16   | "lunedì va bene, venerdì è un disastro"                                                          | "lunedì va bene, venerdì la situazione si era degradata pesantemente"                                             | Gestione emotiva      | "Disastro" catastrofismo identitario, sostituibile con descrizione tecnica del degrado.                                              |
| 2  | 31   | "Per capire il problema serve un passo indietro."                                                 | "Per capire la dinamica serve un passo indietro."                                                                 | Frame mentale         | Frame narrativo di apertura sezione, "problema" generico.                                                                            |
| 3  | 103  | "l'autovacuum si attiva forse ogni 4 giorni"                                                     | "l'autovacuum si attiva all'incirca ogni 4 giorni"                                                                | Sicurezza comunicativa | "Forse" indebolisce una stima tecnica derivata da calcolo. "All'incirca" mantiene il senso di approssimazione senza incertezza.    |
| 4  | 106  | "Ecco perché lunedì andava tutto bene e venerdì era un disastro."                                 | "Ecco perché lunedì andava tutto bene e venerdì il sistema era al limite."                                        | Gestione emotiva      | Coerente con la sostituzione #1, chiusura del paragrafo.                                                                              |
| 5  | 112  | "La prima cosa da fare quando sospetti un problema di vacuum..."                                  | "La prima cosa da fare quando sospetti una criticità di vacuum..."                                                | Frame mentale         | Frame narrativo, sostituibile.                                                                                                        |

**Da segnalare (riga 210)**:
- Riga 210: "la tabella ha un problema serio" — frame narrativo di chiusura paragrafo. Sostituibile con "la tabella ha una criticita seria" oppure "la tabella ha un bloat serio". La seconda è più precisa tecnicamente. Segnalato per discussione: se si vuole essere conservativi, lasciare; se si applica il pattern, **"la tabella ha un bloat serio"** è la scelta più informativa.
- Riga 255: "hai un problema" — chiusura del primo punto della lista finale (`Controlla pg_stat_user_tables regolarmente. Se n_dead_tup cresce piu velocemente di quanto l'autovacuum riesca a pulire, hai un problema.`). Qui "problema" è in registro diagnostico molto diretto: propendo per lasciarlo perché la sostituzione ("hai una criticita") suona meno naturale in una takeaway list. Segnalato per discussione.

**Da LASCIARE (motivate)**:
- Riga 141: "L'autovacuum girava, ma troppo raramente per tenere il passo" — opposizione retorica tecnica reale. Resta.
- Riga 212: "Un'alternativa meno precisa ma più leggera..." — opposizione retorica tecnica (compromesso). Resta.
- Riga 222: "...non recupera tutto. Libera i dead tuples, ma lo spazio frammentato resta" — opposizione retorica tecnica essenziale. Resta.
- Riga 225: "VACUUM FULL funziona, ma blocca tutto" — opposizione retorica tecnica fondamentale del paragrafo. Resta.
- Riga 274 (glossario): "ma non ancora rimossa fisicamente dal disco" — opposizione tecnica descrittiva. Resta.
- Riga 242: "Disabilitare l'autovacuum è la peggior cosa che puoi fare a un PostgreSQL in produzione." — affermazione forte di apertura sezione "Il principio", funzionale al messaggio. Non c'e' "ma" / "problema" / "errore" / "devi" da modificare. Resta.

**STATO**: in attesa di approvazione

---

## Riepilogo

| Articolo                            | Modifiche proposte |
|-------------------------------------|--------------------|
| explain-analyze-postgresql          | 5                  |
| pg-stat-statements                  | 6 (di cui 1 mitigazione assolutismo titolo) |
| postgresql_roles_and_users          | 0                  |
| vacuum-autovacuum-postgresql        | 5                  |
| **Totale**                          | **16**             |

**Articolo più "pulito"** (0 modifiche): `postgresql_roles_and_users` — l'articolo era già stato scritto con grande controllo lessicale, nessuna occorrenza dei pattern da evitare.
**Articolo con più modifiche** (6): `pg-stat-statements`, di cui 1 è l'inserimento di una frase di mitigazione per il titolo assolutista (richiesto esplicitamente dall'audit SEO).

**Pattern dominante**: come nella sezione Oracle, la stragrande maggioranza delle modifiche riguarda il tema **Frame mentale** (`problema` generico narrativo da sostituire con `criticità` / `punto critico` / `situazione`) e il tema **Connessione positiva** (`Ma` puramente avversativo a inizio frase narrativa, da sostituire con `E` / `Solo che`).

**Osservazioni trasversali**:
- Gli articoli PostgreSQL presentano lo stesso stile maturo della sezione Oracle: la maggior parte delle occorrenze di `ma` sono opposizioni retoriche tecniche legittime (tempo basso ma volume alto, default ma caso reale, ecc.) che restano intatte.
- Il termine `errore` compare quasi esclusivamente in contesto tecnico-descrittivo (errori SQL, "scelta per errore dall'optimizer" come locuzione idiomatica) e non va sostituito.
- Compaiono `bisogna` (1 occorrenza in `explain-analyze-postgresql` riga 19, in chiusura di paragrafo manifesto: segnalato per discussione, propendo per lasciare), `forse` (1 occorrenza tecnica in `vacuum-autovacuum`, sostituita), `magari` (1 occorrenza in `pg-stat-statements`, sostituita).
- Nessun caso di `spero`, `provo`, `cercherò`, `dovresti`, `penso che`, `credo che`, `non riesco`, `non posso`, `non funziona`, `sono bloccato`, `fallimento`, `difficile`, `impossibile` (in forma identitaria), `sbagliato` (in forma identitaria).
- I `devi` presenti sono tutti istruzioni tecniche al lettore DBA in registro didattico (es. "devi leggere riga per riga", "devi far ripartire una query critica"): lasciati.
- Caso speciale: **`pg-stat-statements`** ha un titolo che contiene un assolutismo ("...su qualsiasi PostgreSQL"), già segnalato dall'audit. La modifica #1 di quell'articolo non è una sostituzione lessicale ma un'**aggiunta** di una frase di mitigazione nelle prime righe del corpo, che ridimensiona l'assolutismo del titolo senza riscriverlo.
