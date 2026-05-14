# Annotazioni stilistiche — Sezione Data Warehouse

**Data**: 2026-05-14
**Articoli analizzati**: 5
**Scopo**: lista delle modifiche stilistiche da applicare in batch agli articoli Data Warehouse, secondo `docs/STILE_LINGUISTICO.md`. Le modifiche NON sono ancora applicate.

**Criteri applicati**:
- Sono lasciate intatte le occorrenze di "ma" in opposizione retorica tecnica reale (es. "sembra X, ma in realta' Y", "funziona, ma con costo Z"): strumento narrativo legittimo del registro tecnico-argomentativo.
- Sono lasciate intatte le occorrenze in citazioni dirette tra virgolette, codice e commenti SQL/bash.
- Sono lasciati intatti i "problema" usati come termine tecnico documentato (es. "split-brain", "problema fondante del dimensional modeling") o all'interno di catene retoriche dove la sostituzione spezza il ritmo.
- Sono modificati: i "Ma" puramente narrativi a inizio frase/paragrafo (dove la frase precedente non viene davvero contraddetta), i "problema" generici sostituibili con "criticita'"/"punto"/"situazione", i "devi" rivolti al lettore quando "ti conviene"/"serve" funziona, i "sbagliato/errore" come verdetto identitario, e i "difficile/impossibile" descrittivi che bloccano il framing positivo.

---

## bus-matrix-terreno-comune

**File**: `content/posts/data-warehouse/bus-matrix-terreno-comune/index.it.md`
**Modifiche proposte**: 9

| #  | Riga | Originale (frammento)                                                                                  | Proposto                                                                                                | Tema                                | Note                                                                                                                              |
|----|------|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Non un disastro scoperto da me, non un sistema da salvare."                                            | "Non un caos scoperto da me, non un sistema da salvare."                                                | Gestione emotiva                    | "Disastro" come catastrofismo gratuito in apertura narrativa; "caos" o "ingorgo" mantiene il senso senza dramma.                |
| 2  | 35   | "Il problema era che non si parlavano."                                                                 | "Il punto era che non si parlavano."                                                                    | Frame mentale                       | "Problema" generico in chiusura paragrafo, sostituibile.                                                                          |
| 3  | 37   | "## 🔍 Il CFO aveva visto il problema prima di noi"                                                      | "## 🔍 Il CFO aveva visto il punto prima di noi"                                                          | Frame mentale                       | Titolo di sezione: "problema" generico, "punto" mantiene l'enfasi senza framing negativo.                                         |
| 4  | 39   | "La cosa onesta da dire e' che il problema l'aveva messo in agenda il CFO..."                            | "La cosa da dire e' che il punto l'aveva messo in agenda il CFO..."                                      | Frame mentale + auto-affermazione   | Doppia: "problema" generico + "La cosa onesta da dire" è auto-affermazione di onestà (vedi CLAUDE.md regola 5).                  |
| 5  | 41   | "Nessuno sbaglia. Semplicemente rispondono a domande diverse."                                          | *(lasciare)*                                                                                            | —                                   | "Sbaglia" qui e' descrizione di fatto (nessun reparto e' in errore tecnico): mantiene il senso retorico. Resta.                  |
| 6  | 62   | "Non e' un problema di BI, e' un problema di anagrafica."                                               | "Non e' una criticita' di BI, e' una criticita' di anagrafica."                                         | Frame mentale                       | Doppio "problema" generico, frase chiave: "criticita'" mantiene il contrasto retorico (BI vs anagrafica).                          |
| 7  | 80   | "Sarebbe stato un progetto da due anni e nessuno ce l'avrebbe finanziato."                              | *(lasciare)*                                                                                            | —                                   | Descrizione di fatto economico, registro narrativo legittimo.                                                                     |
| 8  | 166  | "## 📊 La domanda che prima era impossibile"                                                              | "## 📊 La domanda che prima era irrisolvibile"                                                            | Apertura mentale                    | "Impossibile" descrittivo: la query era effettivamente non risolvibile, "irrisolvibile" o "fuori portata" mantiene il senso.       |
| 9  | 214  | "## Quello che ho imparato"                                                                              | *(lasciare)*                                                                                            | —                                   | Titolo standard di chiusura, registro narrativo legittimo.                                                                        |
| 10 | 216  | "La parte difficile e' stata portare tre reparti a concordare cosa vuol dire 'cliente'."                | "La parte impegnativa e' stata portare tre reparti a concordare cosa vuol dire 'cliente'."              | Percezione della realta'            | "Difficile" descrittivo: "impegnativa" o "delicata" suona piu' costruttivo nel registro post-mortem.                              |

**Modifiche effettive proposte**: 7 (le voci 5, 7 e 9 sono note "Da LASCIARE" inline).

**Da LASCIARE (motivate)**:
- Riga 13: "I totali non coincidevano. Scarti del 9%, del 12%, del 16%..." — descrizione di fatto, registro analitico legittimo. Resta.
- Riga 17: "una situazione che loro conoscevano benissimo e che era diventata ingestibile..." — "ingestibile" e' descrizione di fatto narrativa (loro la gestivano col workaround del controller), non auto-limitazione. Resta.
- Riga 19: "Non avevamo una risposta. Ne avevamo tre." — chiusura retorica forte, struttura narrativa intenzionale. Resta.
- Riga 41: "Nessuno sbaglia." — descrizione di fatto (i tre reparti non sbagliano tecnicamente, rispondono a domande diverse). Termine usato per smontare il giudizio, non come etichetta. Resta.
- Riga 80: "non abbiamo riscritto i tre data mart" / "Sarebbe stato un progetto da due anni" — opposizione retorica strutturale del paragrafo. Resta.
- Riga 162 (vista SQL): "Nessun reparto ha dovuto smettere di usare il proprio data mart." — descrizione di fatto. Resta.
- Riga 193: "Gli errori di matching erano nell'ordine del 20-30%" — descrizione tecnica precisa (matching error rate), termine documentato in data quality. Resta.
- Riga 208: "conformare dopo costa dieci volte di piu' che conformare prima" — affermazione netta che e' il cuore retorico del paragrafo. Resta.
- Riga 216: "Non l'ho risolta io: l'ha risolta il CFO con il suo peso politico, il comitato di governance..., e il DBA del cliente..." — chiusura collettiva esemplare (anti-eroe, vedi CLAUDE.md regola 6). Resta.
- Riga 218: "Se la salti, la paghi dopo con gli interessi." — chiusura forte con metafora finanziaria, registro narrativo legittimo. Resta.

**STATO**: in attesa di approvazione

---

## fatto-grana-sbagliata

**File**: `content/posts/data-warehouse/fatto-grana-sbagliata/index.it.md`
**Modifiche proposte**: 8

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 16   | "Poi qualcuno ha fatto la domanda sbagliata. O meglio, quella giusta."             | "Poi qualcuno ha fatto la domanda meno gradita. O meglio, quella giusta."             | Comunicazione non aggressiva | "Sbagliata" qui e' usata in un gioco retorico (sbagliata vs giusta): "meno gradita" mantiene la struttura senza giudizio identitario sulla domanda. |
| 2  | 33   | "Ma il grain determina le domande a cui il data warehouse puo' rispondere."         | "E il grain determina le domande a cui il data warehouse puo' rispondere."             | Connessione positiva   | "Ma" puramente narrativo a inizio frase: il paragrafo precedente non viene contraddetto, la frase introduce una conseguenza.    |
| 3  | 33   | "Non puoi fare drill-down per prodotto. Non puoi sapere..."                         | *(lasciare)*                                                                            | —                     | "Non puoi" qui e' descrizione di fatto (limite tecnico del grain mensile), constatazione strutturale. Resta.            |
| 4  | 38   | "## 📊 I numeri del problema"                                                       | "## 📊 I numeri della situazione"                                                       | Frame mentale         | Titolo di sezione: "problema" generico narrativo, "situazione" mantiene il senso.                                      |
| 5  | 58   | "Il problema? Le misure additive erano gia' aggregate."                             | "Il punto? Le misure additive erano gia' aggregate."                                  | Frame mentale         | "Problema" generico in chiusura, sostituibile.                                                                          |
| 6  | 58   | "Impossibile risalire alla composizione."                                            | *(lasciare)*                                                                            | —                     | "Impossibile" descrittivo: l'aggregazione e' tecnicamente irreversibile (vedi r.180 stessa logica). Resta.              |
| 7  | 62   | "La soluzione era una sola: cambiare il grain."                                      | *(lasciare)*                                                                            | —                     | Registro decisionale tecnico, chiusura retorica di sezione. Resta.                                                      |
| 8  | 110  | "Quindici minuti contro due. Un prezzo accettabile per un data warehouse che adesso rispondeva a domande reali." | *(lasciare)*                                                                            | —                     | Descrizione di fatto e bilancio costi/benefici. Resta.                                                                  |
| 9  | 174  | "Zero. Non era un problema di ottimizzazione o di indici — era un problema strutturale" | "Zero. Non era una criticita' di ottimizzazione o di indici — era una criticita' strutturale" | Frame mentale         | Doppia occorrenza, frase chiave dell'articolo: "criticita'" mantiene il contrasto (tuning vs struttura).               |
| 10 | 184  | "...era stata dettata dalla pigrizia progettuale, non da un vincolo tecnico."        | *(lasciare)*                                                                            | —                     | "Pigrizia" e' giudizio costruttivo sull'atteggiamento progettuale, non sull'identita'. Resta.                          |
| 11 | 196  | "Ma la regola e': parti dal dettaglio, poi aggrega."                                 | "Pero' la regola e': parti dal dettaglio, poi aggrega."                                 | Riduzione conflitto   | "Ma" narrativo a inizio frase: "Pero'" piu' leggero, mantiene la transizione.                                          |
| 12 | 204  | "Se la tua fact table non risponde alle domande del business, non e' colpa delle query. E' colpa del modello." | "Se la tua fact table non risponde alle domande del business, non sono le query. E' il modello." | Gestione conflitti / Responsabilita' | "E' colpa di..." e' frame di colpevolizzazione (vedi STILE r."e' colpa tua"); riformulazione neutra mantiene il punto. |

**Modifiche effettive proposte**: 6 (le voci 3, 6, 7, 8 e 10 sono note "Da LASCIARE" inline).

**Da LASCIARE (motivate)**:
- Riga 21: "Nessun dettaglio. Nessuna riga di fattura. Nessun prodotto." — anafora narrativa intenzionale (martellante), registro retorico legittimo. Resta.
- Riga 33: "Hai un totale. Punto." — chiusura forte e secca, ritmo voluto. Resta.
- Riga 58: "Come avere il totale di uno scontrino senza sapere cosa hai comprato." — metafora forte di chiusura. Resta.
- Riga 91: "che chi aveva scelto il grain aggregato aveva evitato di affrontare" — descrizione di fatto sull'atteggiamento progettuale, non identitario. Resta.
- Riga 178: "Ralph Kimball lo dice in modo chiaro: 'sempre modellare al livello di dettaglio piu' fine disponibile nel sistema sorgente'." — citazione diretta tra virgolette. Resta.
- Riga 180: "si puo' sempre aggregare dal dettaglio al totale, ma non si puo' mai disaggregare un totale nel suo dettaglio" — opposizione retorica forte (reversibile vs irreversibile), asse del paragrafo. Resta.
- Riga 182: "Come mescolare i colori: dal rosso e dal giallo puoi ottenere l'arancione, ma dall'arancione non torni piu' ai colori originali." — metafora di chiusura. Resta.
- Riga 186: "Il risultato? Un data warehouse che andava ricostruito da zero dopo sei mesi dal go-live." — descrizione di fatto, registro decisionale forte. Resta.
- Riga 196: "Le aggregate fact table sono un'ottimizzazione, non un sostituto della grana fine." — opposizione retorica tecnica reale. Resta.
- Riga 202: "Un ETL perfetto, indici calibrati, hardware potente — niente di tutto questo compensa un grain sbagliato." — "sbagliato" qui e' giudizio strutturale tecnico (il grain non risponde alle domande), termine consolidato in dimensional modeling. Borderline ma resta. Alternativa piu' morbida: "un grain mal scelto" — segnalato per discussione.

**STATO**: in attesa di approvazione

---

## partitioning-dwh

**File**: `content/posts/data-warehouse/partitioning-dwh/index.it.md`
**Modifiche proposte**: 5

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Non e' un bug, non e' un errore di codice. E' il peso dei dati..."                  | "Non e' un bug, non e' una svista di codice. E' il peso dei dati..."                  | Feedback costruttivo  | "Errore di codice" qui e' generico (non ha riferimento a un syntax error preciso): "svista" o "anomalia" alleggerisce. |
| 2  | 21   | "## Il contesto: GDO e tre anni di scontrini"                                       | *(lasciare)*                                                                            | —                     | Titolo descrittivo. Resta.                                                                                              |
| 3  | 46   | "## 🔍 Il sintomo: full table scan su 800 milioni di righe"                          | *(lasciare)*                                                                            | —                     | Titolo tecnico descrittivo. Resta.                                                                                      |
| 4  | 66   | "Ma con 800 milioni, l'optimizer aveva deciso che l'indice non conveniva piu'."     | "Solo che con 800 milioni, l'optimizer aveva deciso che l'indice non conveniva piu'."  | Connessione positiva  | "Ma" narrativo a inizio frase: dopo "un anno prima, quando la tabella aveva 500 milioni di righe", introduce la svolta diagnostica. |
| 5  | 84   | "Dodici minuti."                                                                    | *(lasciare)*                                                                            | —                     | Chiusura secca a tre parole, ritmo voluto. Resta.                                                                       |
| 6  | 125  | "Migrare 800 milioni di righe non e' un'operazione che si fa con un semplice INSERT...SELECT." | *(lasciare)*                                                                            | —                     | Descrizione tecnica di scope. Resta.                                                                                    |
| 7  | 201  | "Non perche' l'hardware fosse piu' veloce, non perche' avessi riscritto le query. Solo perche' il database adesso sapeva dove *non* cercare." | *(lasciare)*                                                                            | —                     | Chiusura retorica forte, asse del paragrafo. Resta.                                                                     |
| 8  | 205  | "Il problema classico del partizionamento e': come carichi i nuovi dati..."          | "La sfida classica del partizionamento e': come carichi i nuovi dati..."              | Frame mentale         | "Problema classico" e' generico: "sfida" o "punto classico" sostituisce mantenendo il framing.                          |
| 9  | 257  | "Il partizionamento non e' una bacchetta magica. Non sostituisce gli indici..."     | *(lasciare)*                                                                            | —                     | Metafora di chiusura, registro narrativo legittimo. Resta.                                                              |
| 10 | 257  | "Ma per una fact table in un data warehouse..."                                      | *(lasciare)*                                                                            | —                     | "Ma" in opposizione retorica strutturale (cosa non risolve vs cosa risolve). Resta.                                    |
| 11 | 259  | "Ma per una fact table in un data warehouse — dove i dati sono cronologici... — il partizionamento range per data non e' un'opzione." | *(lasciare)*                                                                            | —                     | Stesso "ma" di r.257 nella prosa di chiusura: opposizione tecnica forte. Resta.                                        |
| 12 | 261  | "Aveva una tabella che era cresciuta oltre il punto in cui la mancanza di struttura fisica diventa un collo di bottiglia." | *(lasciare)*                                                                            | —                     | Descrizione di fatto. Resta.                                                                                            |
| 13 | 261  | "Il partizionamento ha rimesso le cose al loro posto: 40 secondi, e nessuna riga letta inutilmente." | *(lasciare)*                                                                            | —                     | Chiusura di articolo, registro narrativo legittimo. Resta.                                                              |
| 14 | 84   | "Quaranta gigabyte di I/O per una query trimestrale. In un ambiente dove il buffer pool era dimensionato a 16 GB..." | *(lasciare)*                                                                            | —                     | Descrizione tecnica, registro analitico. Resta.                                                                         |
| 15 | 144  | "Non male, considerando che ogni riga doveva essere distribuita nella partizione corretta in base alla data." | *(lasciare)*                                                                            | —                     | Bilancio di fatto, registro asciutto. Resta.                                                                            |
| 16 | 199  | "Da 12 minuti a 40 secondi."                                                        | *(lasciare)*                                                                            | —                     | Risultato secco, ritmo voluto. Resta.                                                                                   |

**Modifiche effettive proposte**: 3 (le voci 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16 sono note "Da LASCIARE" inline).

**Da LASCIARE (motivate)**:
- Riga 13: "Conoscevo gia' il copione." — registro colloquiale narrativo, asse di apertura. Resta.
- Riga 15: "Non e' un bug, non e' un errore di codice." (parte iniziale frase, gia' annotata in voce 1).
- Riga 17: "E' il peso dei dati che alla fine si fa sentire." — chiusura sezione di apertura. Resta.
- Riga 25: "In tre anni si erano accumulate 800 milioni di righe." — descrizione di fatto. Resta.
- Riga 51: "Il report trimestrale era questo:" — connettivo strutturale. Resta.
- Riga 122: "Quando l'optimizer elimina una partizione, elimina anche il segmento di indice corrispondente." — descrizione tecnica. Resta.
- Riga 144: "Con 8 processi paralleli e NOLOGGING, il caricamento ha impiegato 47 minuti per 800 milioni di righe." — descrizione tecnica. Resta.
- Riga 162: "La tabella originale l'ho tenuta per una settimana come rete di sicurezza, poi l'ho droppata." — descrizione di fatto + metafora "rete di sicurezza" intenzionale. Resta.
- Riga 239: "L'exchange partition e' un'operazione DDL che modifica solo il data dictionary — non sposta nemmeno un byte di dati." — descrizione tecnica. Resta.
- Riga 251: "Confrontalo con un DELETE FROM fact_vendite WHERE..." — istruzione tecnica diretta in registro di confronto comparativo, legittima. Resta.

**STATO**: in attesa di approvazione

---

## ragged-hierarchies

**File**: `content/posts/data-warehouse/ragged-hierarchies/index.it.md`
**Modifiche proposte**: 12

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 13   | "...qualsiasi tool di BI dovrebbe gestire senza problemi."                          | "...qualsiasi tool di BI dovrebbe gestire senza criticita'."                          | Frame mentale         | "Senza problemi" e' costruzione idiomatica: la sostituzione e' valutabile. Alternativa: lasciare. Segnalato.            |
| 2  | 15   | "...producono risultati sbagliati o incompleti perche' la gerarchia ha dei buchi." | "...producono risultati errati o incompleti perche' la gerarchia ha dei buchi."       | Comunicazione non aggressiva | "Sbagliati" come giudizio sui risultati: "errati" e' piu' tecnico/descrittivo. Borderline. Alternativa: "scorretti".  |
| 3  | 17   | "Nel mondo reale si chiama 'il problema che nessuno vede finche' non apre il report e i numeri non tornano.'" | "Nel mondo reale si chiama 'la situazione che nessuno vede finche' non apre il report e i numeri non tornano.'" | Frame mentale + clickbait | Doppia: "problema" generico + costruzione "che nessuno vede" e' formula clickbait (vedi CLAUDE.md regola 5). Riformulare: "la cosa che nessuno nota finche' non apre il report". |
| 4  | 65   | "## Il problema: i report non tornano"                                              | "## La situazione: i report non tornano"                                              | Frame mentale         | Titolo di sezione: "problema" generico, "situazione" mantiene il senso.                                                  |
| 5  | 67   | "Una richiesta ragionevole — il tipo di cosa che ti aspetti da qualsiasi DWH."     | *(lasciare)*                                                                            | —                     | Descrizione di aspettativa di business. Resta.                                                                          |
| 6  | 93   | "Cinque righe. E almeno tre problemi."                                              | "Cinque righe. E almeno tre criticita'."                                              | Frame mentale         | "Problemi" plurale generico, sostituibile. Mantiene il ritmo della frase secca.                                          |
| 7  | 99   | "Il totale per Top Group e' sbagliato perche' mancano le righe con NULL."          | "Il totale per Top Group e' errato perche' mancano le righe con NULL."                | Comunicazione non aggressiva | "Sbagliato" come giudizio sul risultato: "errato" o "scorretto" e' piu' tecnico.                                       |
| 8  | 115  | "Ma introduce problemi nuovi."                                                      | "Solo che introduce criticita' nuove."                                                | Frame mentale + Connessione positiva | Doppia: "Ma" narrativo a inizio frase + "problemi" generico.                                                          |
| 9  | 121  | "Non risolve il problema strutturale: la gerarchia e' incompleta..."                | "Non risolve la criticita' strutturale: la gerarchia e' incompleta..."                | Frame mentale         | "Problema" generico, sostituibile.                                                                                       |
| 10 | 131  | "...una tecnica standard nel dimensional modeling, descritta da Kimball..."         | *(lasciare)*                                                                            | —                     | Descrizione di fatto. Resta.                                                                                            |
| 11 | 329  | "## Perche' non basta la COALESCE nel report"                                        | *(lasciare)*                                                                            | —                     | Titolo descrittivo. Resta.                                                                                              |
| 12 | 331  | "'Ma la COALESCE nel report fa la stessa cosa...'"                                   | *(lasciare)*                                                                            | —                     | Citazione diretta dell'obiezione tra virgolette. Resta.                                                                  |
| 13 | 339  | "Su una tabella dimensionale con milioni di righe, la differenza si vede."           | *(lasciare)*                                                                            | —                     | Descrizione di fatto. Resta.                                                                                            |
| 14 | 367  | "## La regola che mi guida"                                                          | *(lasciare)*                                                                            | —                     | Titolo standard. Resta.                                                                                                 |
| 15 | 369  | "Se il report ha bisogno di logica condizionale per gestire la gerarchia, il problema e' nel modello, non nel report." | "Se il report ha bisogno di logica condizionale per gestire la gerarchia, il punto e' nel modello, non nel report." | Frame mentale         | Frase chiave dell'articolo: "punto" mantiene il contrasto (modello vs report).                                          |
| 16 | 371  | "E un report che fa il lavoro dell'ETL e' un report che prima o poi si rompe."      | "E un report che fa il lavoro dell'ETL e' un report che, presto o tardi, si rompe."   | Affidabilita'         | "Prima o poi" e' indefinito (vedi STILE_LINGUISTICO): "presto o tardi" e' simile ma piu' tecnico. Borderline. Alternativa: lasciare se ritmo. |
| 17 | 373  | "Non e' elegante. Non e' sofisticato. E' una soluzione che un informatico appena laureato potrebbe trovare brutta. Ma funziona..." | *(lasciare)*                                                                            | —                     | Anafora narrativa intenzionale + "Ma funziona" opposizione retorica forte (estetica vs utilita'). Resta.                |
| 18 | 373  | "...trasforma un problema che infesta ogni singolo report in un problema che si risolve una volta sola..." | "...trasforma una criticita' che infesta ogni singolo report in una criticita' che si risolve una volta sola..." | Frame mentale         | Doppia occorrenza di "problema" generico nella stessa frase. Sostituire entrambe per coerenza.                          |
| 19 | 17   | "Nel mondo reale si chiama 'il problema che nessuno vede...'"                       | *(vedi voce 3)*                                                                         | —                     | Gia' annotato in voce 3 — auto-affermazione "nessuno vede" e' formula tipo clickbait.                                  |
| 20 | 351  | "Il modello e' **OLTP** e il self-parenting creerebbe ambiguita' nelle logiche applicative" | *(lasciare)*                                                                            | —                     | Descrizione tecnica di vincolo. Resta.                                                                                  |

**Modifiche effettive proposte**: 10 (le voci 5, 10, 11, 12, 13, 14, 17, 19, 20 sono note "Da LASCIARE" inline o riferimenti incrociati; voce 1 segnalata come borderline).

**Da LASCIARE (motivate)**:
- Riga 13: "Tre livelli. Top Group, Group, Client." — apertura a frasi nominali, ritmo voluto. Resta.
- Riga 15: "Poi scopri che non tutti i clienti hanno un gruppo." — registro narrativo legittimo. Resta.
- Riga 17: "una gerarchia in cui non tutti i rami raggiungono la stessa profondita'" — definizione tecnica. Resta.
- Riga 67: "Il business chiedeva un report semplice" — descrizione di scenario. Resta.
- Riga 95: "Chiunque guardi questo report pensera' che Gruppo Centro abbia 67K di fatturato sotto la holding e 45K da qualche altra parte." — descrizione di scenario, registro narrativo. Resta.
- Riga 115: "Funziona? In un certo senso si' — riempie i buchi." — domanda retorica narrativa. Resta.
- Riga 119: "una logica di report talmente contorta che nessuno osava piu' toccarla" — descrizione di scenario, registro narrativo coloratamente legittimo. Resta.
- Riga 127: "Il principio e' semplice: **chi non ha un padre diventa padre di se' stesso**." — formulazione chiave dell'articolo, registro retorico legittimo. Resta.
- Riga 131: "Non e' un trucco. E' una tecnica standard..." — opposizione retorica forte, asse del paragrafo. Resta.
- Riga 184: "Ogni livello 'mancante' viene riempito dal livello immediatamente inferiore." — descrizione tecnica. Resta.
- Riga 331: "Ma la COALESCE nel report fa la stessa cosa" (in citazione virgolettata di obiezione retorica). Intoccabile, e' tra virgolette.
- Riga 333: "No. Fa qualcosa di simile, ma con tre differenze fondamentali." — opposizione retorica strutturale (sembra vs realta'). Resta.
- Riga 335-339: "Primo... Secondo... Terzo..." — anafora narrativa intenzionale, struttura argomentativa. Resta.
- Riga 343: "## Quando usare il self-parenting (e quando no)" — titolo descrittivo. Resta.
- Riga 359: "Sono strumenti potenti ma risolvono un problema diverso." — "ma" in opposizione retorica reale (potenti vs scope diverso). Borderline su "problema". Alternativa: "ma risolvono uno scenario diverso" — segnalato.
- Riga 361: "Il self-parenting risolve un problema specifico — gerarchie a livelli fissi con rami incompleti — e lo risolve nel modo piu' semplice possibile" — "problema" qui e' centrato sul dominio tecnico (la ragged hierarchy e' nominata come "il problema"), borderline. Alternativa: "il self-parenting risolve uno scenario specifico". Segnalato per discussione.
- Riga 375: "A volte la soluzione migliore e' la piu' semplice. Questa e' una di quelle volte." — chiusura retorica forte. Resta.

**STATO**: in attesa di approvazione

---

## scd-tipo-2

**File**: `content/posts/data-warehouse/scd-tipo-2/index.it.md`
**Modifiche proposte**: 9

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Ma era sbagliato."                                                                  | "Solo che era errato."                                                                | Connessione positiva + Comunicazione non aggressiva | Doppia: "Ma" narrativo a inizio frase + "sbagliato" come giudizio identitario sul dato (era errato perche' fuori contesto, non identita'). |
| 2  | 59   | "Semplice, pulito, veloce. E completamente sbagliato per un data warehouse."        | "Semplice, pulito, veloce. E completamente errato per un data warehouse."             | Comunicazione non aggressiva | "Sbagliato" come giudizio identitario sul modello: "errato" piu' tecnico. Borderline (in opposizione retorica forte). Alternativa: lasciare. |
| 3  | 63   | "Ma un data warehouse non e' un sistema transazionale."                              | *(lasciare)*                                                                            | —                     | "Ma" in opposizione retorica tecnica reale (OLTP vs DWH). Resta.                                                        |
| 4  | 63   | "E una macchina del tempo che sovrascrive il passato e' inutile."                    | *(lasciare)*                                                                            | —                     | Metafora forte, chiusura sezione. Resta.                                                                                |
| 5  | 71   | "*Quanti clienti sono passati...* — Impossibile. La classe precedente non esiste piu'." | *(lasciare)*                                                                            | —                     | Triplo "Impossibile" anaforico nelle righe 71-73, ritmo narrativo voluto. Resta (e' constatazione tecnica). |
| 6  | 77   | "Il risultato era inaffidabile perche' i dati di Q1 non c'erano piu'..."             | *(lasciare)*                                                                            | —                     | Descrizione di fatto tecnico. Resta.                                                                                    |
| 7  | 126  | "L'ordine e' importante — se inserisci prima di chiudere, hai un momento in cui esistono due versioni 'correnti' dello stesso cliente." | *(lasciare)*                                                                            | —                     | Avvertimento tecnico in registro istruttivo legittimo. Resta.                                                            |
| 8  | 156  | "Una nota pratica: il confronto con `!=` non gestisce i NULL."                       | *(lasciare)*                                                                            | —                     | Avvertimento tecnico, "non gestisce" e' constatazione di fatto. Resta (vedi eccezioni STILE_LINGUISTICO).               |
| 9  | 282  | "Un punto che spesso viene sottovalutato: la fact table deve usare la **chiave surrogata**" | *(lasciare)*                                                                            | —                     | Registro istruttivo legittimo. "Deve usare" e' istruzione tecnica diretta, non obbligo emotivo. Resta.                  |
| 10 | 322  | "Il costo della Tipo 2 e' la crescita della tabella dimensionale."                   | *(lasciare)*                                                                            | —                     | Descrizione di fatto. Resta.                                                                                            |
| 11 | 337  | "Il problema si pone quando hai milioni di clienti con alti tassi di cambio."        | "La situazione si pone quando hai milioni di clienti con alti tassi di cambio."       | Frame mentale         | "Problema" generico narrativo. "Situazione" mantiene il senso.                                                            |
| 12 | 337  | "Non tutti gli attributi meritano la Tipo 2."                                        | *(lasciare)*                                                                            | —                     | Affermazione tecnica netta. Resta.                                                                                      |
| 13 | 339  | "La scelta di quali attributi tracciare con Tipo 2 e' una decisione di business, non tecnica." | *(lasciare)*                                                                            | —                     | Opposizione retorica strutturale. Resta.                                                                                |
| 14 | 345  | "Ho visto progetti in cui ogni dimensione era Tipo 2 'per sicurezza' — il risultato era un modello inutilmente complesso, ETL lenti..." | *(lasciare)*                                                                            | —                     | Aneddoto narrativo, registro legittimo. Resta.                                                                          |
| 15 | 347  | "Se non ce l'ha, la Tipo 1 e' la scelta giusta."                                     | *(lasciare)*                                                                            | —                     | Affermazione tecnica netta. Resta.                                                                                      |
| 16 | 349  | "Ci sono anche casi in cui la Tipo 2 non basta."                                     | *(lasciare)*                                                                            | —                     | Descrizione di scope. Resta.                                                                                            |
| 17 | 351  | "Ma per le dimensioni con cambiamenti molto frequenti..."                            | *(lasciare)*                                                                            | —                     | "Ma" in opposizione retorica strutturale (caso generale vs caso limite). Resta.                                          |
| 18 | 353  | "Ma per il caso piu' comune... la Tipo 2 e' lo strumento giusto."                    | *(lasciare)*                                                                            | —                     | "Ma" in opposizione retorica strutturale di chiusura (eccezioni vs caso comune). Resta.                                  |
| 19 | 353  | "Funziona per i report del mese corrente, ma non risponde alla domanda che prima o poi qualcuno fara'..." | *(lasciare)* / "*ma* tecnico opposto"                                                  | —                     | "Ma" in opposizione retorica tecnica reale (cosa fa vs cosa non fa). Resta. "Prima o poi" e' borderline (vedi STILE): nel contesto narrativo di chiusura, e' essenziale al ritmo. Alternativa: lasciare. |
| 20 | 363  | "La domanda arriva sempre. La questione e' se il tuo DWH e' pronto a rispondere."   | *(lasciare)*                                                                            | —                     | Chiusura di articolo, registro narrativo legittimo. Resta.                                                              |

**Modifiche effettive proposte**: 3 (le voci 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20 sono note "Da LASCIARE" inline).

**Da LASCIARE (motivate)**:
- Riga 13: "Quanti clienti avevamo nella regione Nord a giugno scorso?" — citazione diretta del direttore commerciale, intoccabile.
- Riga 19: "Un cliente che a giugno era in regione Nord e a settembre si e' spostato in regione Centro? Per il DWH, quel cliente e' sempre stato in regione Centro. La storia non esiste." — chiusura di apertura, registro narrativo forte. Resta.
- Riga 41: "Semplice, pulito, veloce." (parte di voce 2) — tricolon narrativo. Resta.
- Riga 63: "Per un sistema OLTP e' perfetto" — opposizione retorica strutturale (OLTP vs DWH). Resta.
- Riga 71-73: tre "Impossibile." anaforici — registro narrativo intenzionale, descrizione di fatto tecnico (assenza dato storico). Restano (la voce 5 li annota tutti).
- Riga 75: "Il sistema non tiene la storia." — citazione interna tra virgolette. Resta.
- Riga 77: "Il report confrontava Q2 con Q2 travestito da Q1." — chiusura forte. Resta.
- Riga 79: "E' stato quel momento che ha fatto scattare il progetto di ristrutturazione." — chiusura sezione. Resta.
- Riga 85: "La Tipo 2 non sovrascrive. Versiona." — chiusura secca, ritmo voluto. Resta.
- Riga 119: "La `cliente_id` e' la chiave naturale — serve per collegare le diverse versioni dello stesso cliente." — descrizione tecnica. Resta.
- Riga 154: "Se anche uno solo e' diverso, il record corrente viene chiuso" — descrizione tecnica. Resta.
- Riga 316: "Nessuna clausola temporale. Il JOIN sulla chiave surrogata fa tutto il lavoro." — chiusura forte di sezione. Resta.
- Riga 359: "Il direttore commerciale non sapeva di avere bisogno della storia finche' non gli e' servita. E quando gli e' servita, il DWH non ce l'aveva." — chiusura articolo, registro narrativo legittimo. Resta.
- Riga 363: "La domanda arriva sempre." — chiusura finale forte. Resta.

**STATO**: in attesa di approvazione

---

## Riepilogo

| Articolo                            | Modifiche proposte |
|-------------------------------------|-------------------:|
| bus-matrix-terreno-comune           | 7                  |
| fatto-grana-sbagliata               | 6                  |
| partitioning-dwh                    | 3                  |
| ragged-hierarchies                  | 10                 |
| scd-tipo-2                          | 3                  |
| **Totale**                          | **29**             |

- Articoli analizzati: **5**
- Modifiche totali proposte: **29**
- Articolo piu' carico: **`ragged-hierarchies`** (10 modifiche reali) — l'articolo usa "problema" in modo molto frequente come framing del tema centrale (ragged hierarchy = "il problema delle gerarchie sbilanciate"), e contiene una formula sospetta tipo clickbait al r.17 ("il problema che nessuno vede").
- Articolo piu' pulito: **`scd-tipo-2`** e **`partitioning-dwh`** (3 modifiche ciascuno) — testi tecnicamente molto curati, con "ma"/"problema" usati quasi sempre in opposizione retorica tecnica legittima.

**Pattern dominante Data Warehouse**: ricorre con altissima frequenza la coppia **"problema" generico narrativo** (titoli di sezione, frasi di apertura paragrafo) + **"Ma..." narrativo a inizio frase** (introduzione di una svolta narrativa o di un'obiezione fittizia). Sono i due interventi standard che valgono la maggior parte delle modifiche. Restano numerosi "ma" come opposizione retorica tecnica autentica (sorgente vs DWH, OLTP vs DWH, COALESCE nel report vs nel modello, grain mensile vs riga di fattura) che sono parte legittima del registro tecnico-argomentativo di Ivan e non vanno toccati.

Pattern secondario: l'uso di **"sbagliato"** come giudizio identitario su dati/modelli/scelte (ricorrente in `scd-tipo-2`, `fatto-grana-sbagliata`, `ragged-hierarchies`): sostituibile con "errato"/"scorretto"/"non adatto" mantenendo il senso tecnico senza il framing identitario.

Pattern terziario: presenza di **"impossibile"** descrittivo per limiti tecnici reali (es. drill-down con grain aggregato, query temporali con SCD Tipo 1): in molti casi e' constatazione di fatto e resta; in altri (titolo di sezione "La domanda che prima era impossibile" in `bus-matrix-terreno-comune`) e' sostituibile con "irrisolvibile" o "fuori portata" per attenuare il blocco mentale.

**Casi borderline segnalati per discussione**:
- `fatto-grana-sbagliata` (titolo articolo): contiene "grana sbagliata" — termine retorico chiave dell'articolo, asse semantico dell'intero pezzo (Kimball "grain"), non sostituibile senza riscrivere il titolo. Lasciare.
- `fatto-grana-sbagliata` r.202: "niente di tutto questo compensa un grain sbagliato" — "sbagliato" come giudizio strutturale tecnico sul modello, borderline tra giudizio identitario e descrizione tecnica. Segnalato.
- `ragged-hierarchies` r.17: "il problema che nessuno vede finche' non apre il report" — costruzione tipo clickbait ("che nessuno vede") che cade sotto CLAUDE.md regola 5. Riformulare per evitare la generalizzazione.
- `ragged-hierarchies` r.359 e r.361: "problema" nominale del dominio (la ragged hierarchy *e'* "il problema"), borderline tra termine tecnico documentato e framing negativo. Segnalato.
- `ragged-hierarchies` r.371: "prima o poi si rompe" — formula indefinita (vedi STILE r."prima o poi"), ma in registro narrativo di chiusura il ritmo non sopporta la formulazione precisa. Segnalato.
- `scd-tipo-2` r.353: "non risponde alla domanda che prima o poi qualcuno fara'" — stesso caso: borderline, registro narrativo. Segnalato.
- `bus-matrix-terreno-comune` r.39: "La cosa onesta da dire e' che..." — auto-affermazione di onesta' (CLAUDE.md regola 5): formula da rivedere, riformulazione gia' proposta in voce 4.
