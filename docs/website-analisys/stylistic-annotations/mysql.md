# Annotazioni stilistiche — Sezione MySQL

**Data**: 2026-05-14
**Articoli analizzati**: 6 (esclusi `enum-mysql-semplifica-o-complica` e `mysql-pre-upgrade-assessment`, gia' revisionati)
**Scopo**: lista delle modifiche stilistiche da applicare in batch a tutti gli articoli MySQL, secondo `docs/STILE_LINGUISTICO.md`. Le modifiche NON sono ancora applicate.

**Criteri applicati**:
- Sono lasciate intatte le occorrenze di "ma" in opposizione retorica tecnica reale (es. "funziona, ma scala malissimo", "leggibile, ma problematico"): strumento narrativo legittimo nel registro tecnico-argomentativo.
- Sono lasciate intatte le occorrenze in citazioni dirette tra virgolette, codice e commenti di shell.
- Sono lasciati intatti i "problema" usati come termine tecnico ricorrente nel paragrafo di apertura ed eventuali catene retoriche dove la sostituzione spezza il ritmo.
- Sono modificati: i "Ma" puramente narrativi a inizio frase/paragrafo, gli "errore di sintassi" generici quando "messaggio di errore" non c'entra, i "problema" generici sostituibili con "criticità"/"punto"/"situazione", i "devi" rivolti al lettore quando "ti conviene"/"serve" funziona, i "disastro" come catastrofismo gratuito.

---

## binary-log-mysql

**File**: `content/posts/mysql/binary-log-mysql/index.it.md`
**Modifiche proposte**: 7

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                               | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 15   | "...niente di straordinario. Ma nella directory dei dati c'erano 180 GB..."         | "...niente di straordinario. Solo che nella directory dei dati c'erano 180 GB..."     | Connessione positiva  | "Ma" narrativo a inizio frase, non opposizione tecnica vera: scopre semplicemente un dettaglio inaspettato.            |
| 2  | 118  | "La tentazione di fare un bel `rm -f mysql-bin.*` è forte. Ma è sbagliata..."        | "La tentazione di fare un bel `rm -f mysql-bin.*` è forte. Solo che è una scelta da evitare..." | Comunicazione non aggressiva / Connessione positiva | Doppia sostituzione: "Ma" narrativo + "sbagliata" come giudizio identitario verso la scelta tecnica. |
| 3  | 191  | "Dipende. Ma ecco le mie regole pratiche:"                                          | "Dipende. Però ecco le mie regole pratiche:" — meglio ancora: "Dipende. Ecco comunque le mie regole pratiche:" | Connessione positiva  | "Ma" puramente avversativo di transizione, eliminabile senza perdita.                                                  |
| 4  | 202  | "...stava per crashare il server riempiendo il disco."                              | *(lasciare)*                                                                            | —                     | "Crashare" è descrizione tecnica concreta, non drammatizzazione. Resta.                                                |
| 5  | 277  | "Ogni tanto qualcuno suggerisce di risolvere il problema 'alla radice'..."           | "Ogni tanto qualcuno suggerisce di risolvere la criticità 'alla radice'..."             | Frame mentale         | "Problema" generico narrativo, "criticità" mantiene il senso.                                                          |
| 6  | 284  | "Sì, risolve il problema del disco. Ma elimina:"                                     | "Sì, risolve la criticità del disco. Solo che elimina:"                                 | Frame mentale + Connessione positiva | Doppia: "problema" generico + "Ma" narrativo che introduce un elenco.                                          |
| 7  | 291  | "I binlog non sono un problema. I binlog **non gestiti** sono un problema."          | "I binlog non sono una criticità. I binlog **non gestiti** sono una criticità."         | Frame mentale         | Frase chiave dell'articolo: la sostituzione "criticità" funziona e mantiene il contrasto retorico (gestiti vs no).      |

**Da LASCIARE (motivate)**:
- Riga 30: "quasi sempre sbagliato" — descrizione di un istinto operativo errato in senso tecnico (l'azione produce danno), accettabile come constatazione, non come etichetta identitaria. Alternative possibili: "quasi sempre da evitare". Segnalato per discussione.
- Riga 96: "qualcuno esegue un DROP TABLE sbagliato" — descrizione di fatto (DDL sulla tabella sbagliata), resta.
- Riga 104: "Riapplicare i binlog fino al momento prima del disastro" — commento di codice in blocco bash; in contesto recovery, "disastro" è il termine tecnico (disaster recovery). Resta.
- Riga 136, 178, 187, 212, 220, 236, 271: "ma" in opposizione retorica tecnica reale (verifica vs comando, semplice vs grossolano, stessa logica vs granularità, leggibile vs problematico, pesante vs deterministico, soluzione vs spezzare, non bellissimo vs leggibile). Restano.

**STATO**: in attesa di approvazione

---

## galera-cluster-3-nodi

**File**: `content/posts/mysql/galera-cluster-3-nodi/index.it.md`
**Modifiche proposte**: 6

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                                | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 2    | "...come ho risolto un problema di disponibilità su MySQL"                          | "...come ho risolto una criticità di disponibilità su MySQL"                            | Frame mentale         | Titolo dell'articolo: "problema" generico, "criticità" è il termine tecnico-aziendale standard.                        |
| 2  | 13   | "...quando il problema è grave..."                                                  | "...quando la situazione è grave..."                                                    | Frame mentale         | Frase di apertura, "problema" generico.                                                                                |
| 3  | 15   | "Ogni volta che il server aveva un problema..."                                     | "Ogni volta che il server aveva una criticità..."                                       | Frame mentale         | "Problema" generico sostituibile; "criticità" o "anomalia" rendono bene.                                              |
| 4  | 17   | "...la prossima volta che un server ha un problema..."                              | "...la prossima volta che un server ha un'anomalia..."                                  | Frame mentale         | Coerenza con la sostituzione di riga 15. Variare "criticità" / "anomalia" per non ripetere.                            |
| 5  | 143  | "...hai un problema architetturale da risolvere a monte."                           | "...hai una criticità architetturale da risolvere a monte."                             | Frame mentale         | Sostituibile senza perdita di senso.                                                                                   |
| 6  | 304  | "Potrebbe essere un problema di I/O disco, CPU, o un nodo sottodimensionato."        | "Potrebbe essere una criticità di I/O disco, CPU, o un nodo sottodimensionato."         | Frame mentale         | Lista diagnostica: "criticità" suona tecnicamente corretto.                                                            |

**Da LASCIARE (motivate)**:
- Riga 70: `# Abilitare ma NON avviare ancora il servizio` — commento all'interno di blocco codice bash, intoccabile.
- Riga 147: "Ma in un cluster Galera, la durabilità è già garantita..." — opposizione retorica tecnica reale (default sicuro vs contesto cluster). Resta.
- Riga 190: "il cluster si forma ma non sincronizza" — opposizione tecnica vera (forma sì, sincronizza no). Resta.
- Riga 333: "## Il problema dello split-brain" — titolo di sezione dove "problema" è collegato a un termine tecnico documentato (lo split-brain è un problema noto e nominato così in letteratura). Potenzialmente sostituibile con "## Lo split-brain: perché tre nodi e non due" — segnalato per discussione.
- Riga 341: "ma è come disattivare l'allarme antincendio..." — opposizione retorica con metafora forte, asse del paragrafo. Resta.
- Riga 351: "Nessun errore, nessun timeout" — descrizione tecnica (assenza di error log/timeout), non identitaria. Resta.

**STATO**: in attesa di approvazione

---

## mysql-group-replication-binlog-migration

**File**: `content/posts/mysql/mysql-group-replication-binlog-migration/index.it.md`
**Modifiche proposte**: 7

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 15   | "Ma è la domanda sbagliata. Quella giusta è..."                                     | "Solo che è la domanda sbagliata. Quella giusta è..."                                 | Connessione positiva  | "Ma" narrativo a inizio frase.                                                                                         |
| 2  | 27   | "Ma la cosa che non andava era il path:"                                            | "Solo che la cosa che non andava era il path:"                                        | Connessione positiva  | "Ma" narrativo che introduce la scoperta tecnica.                                                                      |
| 3  | 49   | "...quindi il problema si moltiplicava su tutti e tre i nodi."                       | "...quindi la criticità si moltiplicava su tutti e tre i nodi."                       | Frame mentale         | "Problema" generico, sostituibile.                                                                                     |
| 4  | 51   | "Il problema era chiaro: i binary log stavano mangiando..."                          | "La causa era chiara: i binary log stavano mangiando..."                              | Frame mentale         | "Problema" qui è la diagnosi: "causa" o "criticità" rende meglio.                                                      |
| 5  | 55   | "## Ma che cluster è, esattamente?"                                                  | "## E che cluster è, esattamente?"                                                    | Connessione positiva  | Titolo di sezione: "Ma" qui ha funzione interrogativa, "E" preserva il tono colloquiale.                              |
| 6  | 57   | "...devi sapere cosa hai davanti."                                                   | "...ti conviene sapere cosa hai davanti."                                              | Persuasione           | "Devi" obbligo verso lettore: "ti conviene" mantiene il consiglio senza ordine.                                       |
| 7  | 267  | "Il problema vero non era lo spazio disco, era una scelta architetturale..."         | "La causa vera non era lo spazio disco, era una scelta architetturale..."             | Frame mentale         | "Problema" qui è inteso come "causa profonda": esplicitare la sostituzione.                                            |

**Da LASCIARE (motivate)**:
- Riga 67: "ma su MySQL 8.0.20 quel comando non esiste ancora" — opposizione retorica tecnica (tentativo vs disponibilità del comando). Resta.
- Riga 67: "un errore di sintassi che non è un errore" — descrizione tecnica precisa (sembra syntax error ma è una versione mancante). Resta come gioco di parole funzionale.
- Riga 104: "Ma saltare la diagnosi su un cluster è come operare senza la TAC" — opposizione retorica con metafora forte. Resta.
- Riga 104: "puoi fare un disastro" — qui "disastro" funziona da iperbole colloquiale che chiude un paragrafo, e collega al tono "operare senza la TAC". Borderline ma resta. Alternativa più morbida: "puoi fare danni seri" — segnalato per discussione.
- Riga 134: "MySQL non parte se non può scrivere..." — descrizione tecnica con "non può" che è constatazione di fatto. Resta (vedi eccezioni del file STILE_LINGUISTICO.md).
- Riga 140: "ma non è il massimo lato sicurezza" — opposizione retorica reale (funziona vs non massimo). Resta.
- Riga 156: "il problema è dello storage o dei permessi" — diagnostica tecnica con catena causa→effetto, accettabile. Resta. Alternativa: "il guasto è dello storage" — segnalato.
- Riga 175: "Ma è un disservizio." — opposizione retorica essenziale (breve vs comunque presente). Resta.
- Riga 245: "Breve disservizio, come previsto." — descrizione di fatto neutra. Resta.
- Riga 259: "Ma non fare subito `rm -rf...`" — opposizione retorica tecnica (non sarà più usato vs non cancellare). Resta.
- Riga 261: "MySQL può partire ma non rientrare nel gruppo" — opposizione tecnica vera. Resta. "Devi verificare tre cose" — istruzione tecnica diretta in checklist, registro istruttivo legittimo. Resta.

**STATO**: in attesa di approvazione

---

## mysql-multi-istanza-secure-file-priv

**File**: `content/posts/mysql/mysql-multi-istanza-secure-file-priv/index.it.md`
**Modifiche proposte**: 7

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 19   | "Il primo problema non era la query. Il primo problema era..."                       | "Il primo punto non era la query. Il primo punto era..."                              | Frame mentale         | Doppia occorrenza, sostituibile in coppia. "Punto" mantiene il ritmo retorico.                                          |
| 2  | 27   | "...finché non devi fare manutenzione."                                             | "...finché non serve fare manutenzione."                                              | Persuasione           | "Devi" generico verso lettore.                                                                                          |
| 3  | 110  | "E l'errore lo scopri solo quando i dati che esporti..."                            | "E te ne accorgi solo quando i dati che esporti..."                                   | Feedback costruttivo  | "Errore" come fatto vago e identitario (lo scopri = ti accorgi); riformulazione mantiene il senso.                     |
| 4  | 188  | "Ma c'era un altro problema. La directory `/var/lib/mysql-files/`..."                | "Solo che c'era un altro punto. La directory `/var/lib/mysql-files/`..."              | Connessione positiva + Frame mentale | Doppia: "Ma" narrativo + "problema" generico.                                                                          |
| 5  | 190  | "Ma a quel punto stavo già perdendo tempo."                                          | "Solo che a quel punto stavo già perdendo tempo."                                     | Connessione positiva  | "Ma" puramente avversativo, sostituibile.                                                                              |
| 6  | 236  | "Il problema è che quella protezione esiste per un motivo preciso."                  | "Il punto è che quella protezione esiste per un motivo preciso."                      | Frame mentale         | "Problema" generico, "punto" rende il senso.                                                                            |
| 7  | 259  | "Ma è così che funzionano i ticket..."                                              | "Però è così che funzionano i ticket..."                                              | Riduzione conflitto   | Chiusura di articolo, "ma" puramente narrativo. "Però" più leggero.                                                    |

**Da LASCIARE (motivate)**:
- Riga 39: "ma il ticket parlava del 'gestionale' senza specificare" — opposizione retorica reale (nomi indicativi vs mancanza di dettaglio). Resta.
- Riga 72: "ma in un ambiente multi-istanza fa la differenza" — opposizione retorica reale. Resta.
- Riga 72: "ti colleghi a quella sbagliata senza nemmeno accorgertene" — descrizione di fatto (connessione errata = istanza diversa). "Sbagliata" come attributo di una connessione errata, non identitario. Resta.
- Riga 110: "ma non lo è" — opposizione retorica forte (sembra paranoia, non lo è). Resta.
- Riga 166: "ma solo dentro quella directory" — opposizione tecnica vera. Resta.
- Riga 188: "una directory che non esisteva e che nessuno aveva mai creato" — descrizione di fatto. Resta.
- Riga 230: "ma almeno non avevo riavviato nessuna istanza" — opposizione retorica reale (45 min vs 5 min ma senza restart). Resta.
- Riga 253: "Sembra ovvio, ma la quantità di errori..." — opposizione retorica reale. "Errori" qui è plurale generico, accettabile come constatazione. Resta.
- Riga 257: "Ma funziona sempre" — opposizione retorica reale (meno elegante vs funziona sempre). Resta.
- Riga 257: "forse" qui ha funzione di concessione retorica ("È meno elegante, forse") interna a una frase argomentativa: resta, ma è caso limite da segnalare. Alternativa: "È un po' meno elegante, è vero" — segnalato per discussione.

**STATO**: in attesa di approvazione

---

## mysql-users-and-hosts

**File**: `content/posts/mysql/mysql-users-and-hosts/index.it.md`
**Modifiche proposte**: 4

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 78   | "Il problema del `'%'` è che accetta connessioni da **qualsiasi IP**."              | "Il punto del `'%'` è che accetta connessioni da **qualsiasi IP**."                   | Frame mentale         | "Problema" generico in apertura paragrafo.                                                                              |
| 2  | 120  | "Il problema classico è questo: crei `'mario'@'%'`..."                              | "La situazione classica è questa: crei `'mario'@'%'`..."                              | Frame mentale         | "Problema" generico narrativo, sostituibile.                                                                            |
| 3  | 130  | "Se non lo fai prima, lo farai dopo. Con più urgenza e meno calma."                  | *(lasciare)*                                                                            | —                     | Chiusura forte, descrizione di una conseguenza temporale, non un giudizio. Resta. (segnalato come caso borderline)     |
| 4  | 181  | "...in script automatizzati può generare errori sintattici."                         | *(lasciare)*                                                                            | —                     | "Errori sintattici" è descrizione tecnica precisa (syntax error), resta come termine tecnico.                          |

**Modifiche effettive proposte**: 2 (le voci 3 e 4 sono note di "Da LASCIARE").

**Da LASCIARE (motivate)**:
- Riga 61: "Ma se non lo capisci, ti morde." — opposizione retorica forte e idiomatica (modello potente vs rischio). Resta.
- Riga 136: "Ma ci sono differenze nell'implementazione" — opposizione retorica tecnica reale (identico vs differenze). Resta.
- Riga 157: "(ma è deprecato)" — annotazione tecnica tra parentesi all'interno di commento di codice. Resta.
- Riga 165: "ma con sintassi leggermente diversa" — opposizione tecnica vera. Resta.
- Riga 181: "ma in script automatizzati può generare errori sintattici" — opposizione retorica reale. Resta.
- Riga 228: "Ma è anche una fonte di errori subdoli" — opposizione retorica chiave del paragrafo finale (potente vs rischio). Resta. "Errori subdoli" è plurale descrittivo, non giudizio identitario.

**STATO**: in attesa di approvazione

---

## mysqldump-mysqlpump-mydumper

**File**: `content/posts/mysql/mysqldump-mysqlpump-mydumper/index.it.md`
**Modifiche proposte**: 9

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Il problema è che il database nel frattempo era cresciuto."                         | "Il punto è che il database nel frattempo era cresciuto."                             | Frame mentale         | "Problema" come constatazione narrativa, sostituibile.                                                                  |
| 2  | 23   | "## Il problema vero: mysqldump è single-threaded"                                   | "## Il punto vero: mysqldump è single-threaded"                                        | Frame mentale         | Titolo di sezione: "punto vero" mantiene l'enfasi senza dramma.                                                          |
| 3  | 37   | "Se devi spostare una tabellina da 500 righe..."                                    | "Se ti serve spostare una tabellina da 500 righe..."                                  | Persuasione           | "Devi" verso lettore, "ti serve" più morbido.                                                                            |
| 4  | 37   | "Se devi fare il backup di un database da 60 GB in produzione — no."                | "Se ti serve fare il backup di un database da 60 GB in produzione — no."              | Persuasione           | Stessa logica, coerenza con voce 3.                                                                                      |
| 5  | 54   | "Un miglioramento importante. Ma poi ho guardato meglio."                            | "Un miglioramento importante. Solo che poi ho guardato meglio."                       | Connessione positiva  | "Ma" puramente narrativo a inizio frase.                                                                                |
| 6  | 56   | "Il problema è che quando hai una tabella da 30 GB..."                              | "Il punto è che quando hai una tabella da 30 GB..."                                   | Frame mentale         | "Problema" generico narrativo.                                                                                          |
| 7  | 58   | "Ma il problema più serio è un altro."                                              | "Solo che il punto più serio è un altro."                                              | Connessione positiva + Frame mentale | Doppia: "Ma" narrativo + "problema" generico.                                                                          |
| 8  | 123  | "## Le opzioni critiche che non devi dimenticare"                                    | "## Le opzioni critiche da non dimenticare"                                            | Persuasione           | "Devi" rivolto al lettore in titolo di sezione: riformulazione impersonale mantiene il senso.                          |
| 9  | 187  | "Non c'è di che. Ma la prossima volta, non aspettare..."                            | "Non c'è di che. Però la prossima volta, non aspettare..."                            | Riduzione conflitto   | Chiusura ironica dell'articolo, "ma" sostituibile con "però" per tono più leggero.                                       |

**Da LASCIARE (motivate)**:
- Riga 32: `# Il backup classico — funziona, ma scala malissimo` — commento all'interno di blocco bash, intoccabile.
- Riga 39: "performance che sulla carta promettono molto ma che nella realtà vanno testate" — opposizione retorica reale (promessa vs verifica). Resta.
- Riga 64: "Per un backup di produzione... No. Assolutamente no." — descrizione di fatto, registro deciso da DBA senior, intenzionale. Resta. "Disastro" qui è il termine standard del disaster recovery (collegato al concetto di "restore in caso di disastro"). Resta.
- Riga 72: "Ma fa una cosa che né mysqldump né mysqlpump fanno" — opposizione retorica forte (non incluso, va installato vs ha questa funzionalità). Resta.
- Riga 91: "Ma il vero vantaggio di mydumper non è solo la velocità del dump" — opposizione retorica strutturale del paragrafo (velocità dump vs velocità restore). Resta.
- Riga 125: "ci sono opzioni che devi includere sempre" — istruzione tecnica diretta in registro di checklist operativa. Borderline. Alternativa: "ci sono opzioni da includere sempre" — segnalato per discussione.
- Riga 125: "conseguenze che vanno dal fastidio al disastro" — qui "disastro" è polo retorico di una climax stilistica (fastidio→disastro). Funziona, resta.
- Riga 131: "ma quelle verranno comunque lockate" — opposizione tecnica vera. Resta.
- Riga 135: "Li devi chiedere esplicitamente" — istruzione tecnica diretta in registro operativo. Resta. Alternativa: "vanno chiesti esplicitamente" — segnalato.
- Riga 139: "Se usi la replica basata su GTID — e dovresti" — "dovresti" qui è un consiglio professionale forte ma giustificato dal contesto (GTID è oggettivamente la scelta moderna). Borderline ma resta. Alternativa: "e ti conviene" — segnalato.
- Riga 139: "ti faranno impazzire" — iperbole colloquiale che chiude il paragrafo. Resta.
- Riga 164: "fa tutto, lentamente, ma lo fa" — opposizione retorica essenziale (lento vs funziona). Resta.
- Riga 166: "mydumper fa tutto quello che mysqlpump prometteva ma meglio" — opposizione retorica reale (stesso scopo vs migliore). Resta.
- Riga 168: "Richiede un'installazione separata, ma il tempo che risparmi..." — opposizione retorica costo/beneficio, asse del paragrafo. Resta.
- Riga 180: "in caso di disastro totale" — termine tecnico standard del DR. Resta.
- Riga 183: "Ma per un database da 60 GB..." — opposizione retorica reale (portabilità vs velocità restore). Resta.
- Riga 185: "Ma questa volta il messaggio era diverso" — opposizione retorica narrativa essenziale (richiamo vs richiamo positivo). Resta.

**STATO**: in attesa di approvazione

---

## Riepilogo

| Articolo                                          | Modifiche proposte |
|---------------------------------------------------|-------------------:|
| binary-log-mysql                                  | 7                  |
| galera-cluster-3-nodi                             | 6                  |
| mysql-group-replication-binlog-migration          | 7                  |
| mysql-multi-istanza-secure-file-priv              | 7                  |
| mysql-users-and-hosts                             | 2                  |
| mysqldump-mysqlpump-mydumper                      | 9                  |
| **Totale**                                         | **38**             |

- Articoli analizzati: 6 (esclusi `enum-mysql-semplifica-o-complica` e `mysql-pre-upgrade-assessment`, gia' revisionati)
- Modifiche totali proposte: **38**
- Articoli piu' carichi (in ordine): `mysqldump-mysqlpump-mydumper` (9), `binary-log-mysql` / `mysql-group-replication-binlog-migration` / `mysql-multi-istanza-secure-file-priv` (7 ciascuno)
- Articolo piu' leggero: `mysql-users-and-hosts` (2 modifiche reali — l'articolo e' gia' molto pulito stilisticamente)

**Pattern dominante MySQL**: ricorre con altissima frequenza la coppia "Ma..." narrativo a inizio frase + "problema" generico. Sono i due interventi standard che valgono la maggior parte delle modifiche. Restano numerosi "ma" come opposizione retorica tecnica autentica (default vs eccezione, costo vs beneficio, formale vs reale) che sono parte legittima del registro tecnico-argomentativo di Ivan e non vanno toccati.

**Casi borderline segnalati per discussione**:
- "puoi fare un disastro" (group-replication, r.104): iperbole colloquiale o catastrofismo da rivedere?
- "devi includere sempre", "devi chiedere", "dovresti" (mysqldump-mysqlpump-mydumper, rr. 125/135/139): registro istruttivo legittimo o "devi/dovresti" da sostituire?
- "il guasto/problema è dello storage" (group-replication, r.156): "problema" qui e' diagnosi tecnica concreta — modificare o lasciare?
- "## Il problema dello split-brain" (galera, r.333): "problema" agganciato a un termine tecnico documentato — modificare il titolo?
