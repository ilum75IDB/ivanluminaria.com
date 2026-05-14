# Annotazioni stilistiche — Sezione Oracle

**Data**: 2026-05-14
**Articoli analizzati**: 6
**Scopo**: lista delle modifiche stilistiche da applicare in batch a tutti gli articoli Oracle, secondo `docs/STILE_LINGUISTICO.md`. Le modifiche NON sono ancora applicate.

**Criteri applicati**:
- Sono lasciate intatte le occorrenze di "ma" in opposizione retorica tecnica (es. "sembra X, ma in realtà Y", "funziona, ma con un costo Y"): strumento narrativo legittimo nel registro tecnico-argomentativo.
- Sono lasciate intatte le occorrenze in citazioni dirette tra virgolette, codice e descrizioni tecniche neutre (es. "errore logico", "errore di permesso").
- Sono modificati i "ma" puramente avversativi narrativi all'inizio di frase, i "problema" generici (sostituibili con "criticità", "situazione", "punto"), gli "errore" usati come verdetto identitario e i "devi" rivolti al lettore in obbligo diretto.

---

## oracle-awr-ash

**File**: `content/posts/oracle/oracle-awr-ash/index.it.md`
**Modifiche proposte**: 4

| #  | Riga | Originale (frammento)                                          | Proposto                                                | Tema                  | Note                                                                                                       |
|----|------|----------------------------------------------------------------|---------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Ma il tono era diverso dal solito."                            | "Solo che il tono era diverso dal solito."              | Connessione positiva  | "Ma" narrativo a inizio frase: rinforza l'opposizione al ritmo della narrazione, sostituibile.            |
| 2  | 47   | "## AWR: la fotografia del problema"                            | "## AWR: la fotografia della situazione"                | Frame mentale         | Titolo di sezione: "problema" qui è etichetta generica, "situazione" mantiene la lettura senza dramma.    |
| 3  | 66   | "prima del problema visibile"                                   | "prima della criticità visibile"                        | Frame mentale         | Riferimento generico, sostituibile.                                                                        |
| 4  | 142  | "Il risultato mi ha fatto capire subito il problema:"           | "Il risultato mi ha fatto capire subito la criticità:"  | Frame mentale         | Frame narrativo, non descrizione tecnica vincolata.                                                       |

**Da LASCIARE (motivate)**:
- Riga 15: `"Ivan, abbiamo un problema..."` — citazione diretta del project manager, intoccabile.
- Riga 39, 166, 268, 272: "Ma..." in opposizione retorica tecnica (test che passano vs batch che esplode, deploy che fa drop, ecc.). Restano.
- Riga 100: "Ma avevo bisogno di capire **quando**..." — opposizione retorica tra "AWR mi aveva dato la fotografia" e necessità ulteriore: strumento di transizione narrativa, resta.
- Riga 212: "diagnosticare un problema" — descrizione di metodologia generica, accettabile.
- Riga 268: "devi verificare che indici..." — istruzione tecnica diretta al lettore DBA, ma in un contesto di "se rilasci in produzione, devi verificare": resta (registro istruttivo legittimo). Alternativa più morbida: "ti conviene verificare" — segnalato per discussione.

**STATO**: in attesa di approvazione

---

## oracle-cloud-migration

**File**: `content/posts/oracle/oracle-cloud-migration/index.it.md`
**Modifiche proposte**: 5

| #  | Riga | Originale (frammento)                                                                 | Proposto                                                                                       | Tema                  | Note                                                                                                                                          |
|----|------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 15   | "Qualcuno in alto decide che bisogna andare in cloud"                                  | "Qualcuno in alto decide di andare in cloud"                                                  | Coinvolgimento        | "Bisogna" impersonale; la riformulazione mantiene il senso senza dovere astratto.                                                            |
| 2  | 17   | "Il problema è che Oracle non è un'applicazione..."                                    | "Il punto è che Oracle non è un'applicazione..."                                              | Frame mentale         | Apertura paragrafo, "problema" generico narrativo.                                                                                            |
| 3  | 17   | "...con gli stessi problemi di prima — più qualcuno di nuovo."                         | "...con le stesse criticità di prima — più qualcuna di nuova."                                | Frame mentale         | Coerente con la sostituzione del termine in apertura.                                                                                         |
| 4  | 65   | "Ma ho voluto testare il worst case"                                                  | "E ho voluto testare il worst case"                                                            | Connessione positiva  | "Ma" puramente narrativo dopo punto: la frase precedente non viene contraddetta, anzi viene approfondita.                                    |
| 5  | 133  | "bisogna parlare con Oracle, ottenere conferme scritte"                                | "serve parlare con Oracle, ottenere conferme scritte"                                          | Coinvolgimento        | "Bisogna" → "serve" mantiene tono direttivo senza impersonalità.                                                                              |

**Da LASCIARE (motivate)**:
- Riga 21: "fattura parecchio ma ha un IT snello" — opposizione retorica legittima (grande fatturato vs IT piccolo). Resta.
- Riga 43: "Ma il Partitioning lo usavano solo su tre tabelle" — opposizione vera (RAC e Data Guard pervasivi vs Partitioning marginale). Resta.
- Riga 47: "...ma il batch notturno faceva un join massiccio..." — opposizione tecnica reale (accettabile per interattive, non per batch). Resta.
- Riga 47: "Un passaggio in più, ma il batch è passato da sei ore a due" — opposizione legittima costo/beneficio. Resta.
- Riga 57: "Funziona, ma aggiunge un layer di automazione" — opposizione tecnica reale. Resta.
- Riga 104: "tecnicamente riuscita ma tutti si lamentano" — opposizione tra successo formale e percezione utente, parte centrale del messaggio. Resta.
- Riga 106: "orari sbagliati" — descrizione tecnica di un fatto (timezone errato), non identitario. Resta.
- Riga 106: "Fix in due ore, ma poteva essere evitato" — opposizione retorica legittima. Resta.
- Riga 110: "sono riallineate, ma tre job che usavano `SYSTIMESTAMP`..." — opposizione tecnica vera. Resta.
- Riga 125: "Ma il numero che ha colpito di più il CFO non era il totale" — opposizione retorica forte e funzionale al paragrafo. Resta.
- Riga 127: "ma era reale" — opposizione retorica essenziale (non appariva ma esisteva). Resta.
- Riga 135: "sono cose noiose, ma sono la differenza..." — opposizione retorica di valore, asse del paragrafo. Resta.
- Riga 15: "errore" assente come termine.

**STATO**: in attesa di approvazione

---

## oracle-data-guard

**File**: `content/posts/oracle/oracle-data-guard/index.it.md`
**Modifiche proposte**: 3

| #  | Riga | Originale (frammento)                                                              | Proposto                                                                              | Tema                  | Note                                                                                                                                  |
|----|------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 186  | "significa che c'è un problema di rete, di configurazione o di permessi"            | "significa che c'è una criticità di rete, di configurazione o di permessi"            | Frame mentale         | "Problema" generico, sostituibile.                                                                                                    |
| 2  | 222  | "Ma ci sono cose che la documentazione Oracle non enfatizza abbastanza."            | "E ci sono cose che la documentazione Oracle non enfatizza abbastanza."               | Connessione positiva  | "Ma" puramente avversativo di paragrafo che apre un elenco; "E" mantiene il flow senza opposizione.                                  |
| 3  | 253  | "Il disaster recovery non è un problema tecnico. È un problema di percezione..."   | "Il disaster recovery non è una questione tecnica. È una questione di percezione..." | Frame mentale         | Doppia occorrenza nello stesso passaggio, sostituibile in coppia per coerenza.                                                       |

**Da LASCIARE (motivate)**:
- Riga 15: "nessuno vuole spendere soldi per proteggersi da problemi che non si sono mai visti" — il senso è "rischi/eventi non visti", ma "problemi" qui è idiomatico e coerente con la voce narrativa. Segnalato per discussione.
- Riga 19: "Non un errore logico, non una corruzione recuperabile" — descrizione tecnica precisa (tipologia di guasto). Resta.
- Riga 21: "problemi tecnici, richiamate più tardi" — citazione tra virgolette del call center, intoccabile.
- Riga 77: "non è documentata in modo chiarissimo, ma l'ho imparata a spese mie" — opposizione retorica tra documentazione carente ed esperienza diretta. Resta.
- Riga 116: "errori criptici che ti fanno perdere mezza giornata" — descrizione tecnica concreta (messaggi di errore reali). Resta.
- Riga 142: "Non velocissima, ma è un'operazione che si fa una volta sola" — opposizione retorica di compromesso. Resta.
- Riga 146: "Senza il Broker puoi fare tutto a mano, ma non vuoi farlo a mano quando..." — opposizione retorica chiave del paragrafo. Resta.
- Riga 190: "ma con il CEO presente" — opposizione narrativa (sabato chiuso vs presenza CEO). Resta.
- Riga 224: "Ma a 100 km sarebbe stata 5-8 ms" — opposizione tecnica (12 km accettabili vs 100 km no). Resta.
- Riga 226: "Nessun errore evidente, solo un gap che cresce" — descrizione tecnica del sintomo. Resta.
- Riga 228: "errori che non c'entrano niente con il vero problema" — descrizione tecnica di sintomatologia diagnostica. Resta (e qui "problema" è il "vero problema" tecnico contrapposto al sintomo, intoccabile).
- Riga 235: "Il switchover funzionerà, ma dopo potresti avere corruzioni silenziose" — opposizione retorica tecnica essenziale. Resta.
- Riga 255: "È cinico, ma è così che funziona" — opposizione retorica tra ammissione e realtà. Resta.

**STATO**: in attesa di approvazione

---

## oracle-linux-kernel

**File**: `content/posts/oracle/oracle-linux-kernel/index.it.md`
**Modifiche proposte**: 3

| #  | Riga | Originale (frammento)                                          | Proposto                                                              | Tema                  | Note                                                                                                                |
|----|------|----------------------------------------------------------------|-----------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------|
| 1  | 27   | "Ecco il problema. Non era Oracle."                            | "Ecco il punto. Non era Oracle."                                      | Frame mentale         | "Problema" narrativo generico, "punto" mantiene impatto.                                                            |
| 2  | 72   | "Quasi tutto era sbagliato. Non per errore — per omissione."   | "Quasi tutto era da rivedere. Non per errore — per omissione."        | Comunicazione non aggressiva | "Sbagliato" come verdetto identitario sulla configurazione: "da rivedere" è più costruttivo. "Errore" qui resta perché è in coppia retorica con "omissione" (struttura "non X — Y"). |
| 3  | 302  | "Ma nessuno lo fa, perché il wizard non lo chiede..."           | "Solo che nessuno lo fa, perché il wizard non lo chiede..."           | Connessione positiva  | "Ma" puramente avversativo a inizio frase di chiusura sezione.                                                      |

**Da LASCIARE (motivate)**:
- Riga 15: "Le lamentele erano vaghe ma persistenti" — opposizione retorica vaghezza/persistenza, perfettamente funzionale. Resta.
- Riga 129: "l'istanza non riesce ad allocare la memoria richiesta — o peggio, frammenta l'allocazione" — descrizione tecnica neutra. "Riesce" qui è in negazione tecnica (non identitaria). Resta.
- Riga 173: "Ma Oracle non ha bisogno di equità" — opposizione retorica tecnica forte (desktop vs server DB). Resta.
- Riga 312: "ma che causa latenze imprevedibili" — opposizione tecnica vera (promessa vs realtà THP). Resta.

**STATO**: in attesa di approvazione

---

## oracle-partitioning

**File**: `content/posts/oracle/oracle-partitioning/index.it.md`
**Modifiche proposte**: 6

| #  | Riga | Originale (frammento)                                                                          | Proposto                                                                                                | Tema                  | Note                                                                                                                                  |
|----|------|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 17   | "Non è un bug. Non è un problema di rete o di storage lento."                                   | "Non è un bug. Non è una questione di rete o di storage lento."                                         | Frame mentale         | "Problema" generico narrativo.                                                                                                        |
| 2  | 25   | "La tabella al centro del problema si chiamava `TXN_MOVIMENTI`."                                | "La tabella al centro della situazione si chiamava `TXN_MOVIMENTI`."                                    | Frame mentale         | Frame narrativo, sostituibile.                                                                                                        |
| 3  | 249  | "Ma devi sapere quando funziona e quando no."                                                   | "E devi sapere quando funziona e quando no."                                                            | Connessione positiva  | "Ma" puramente avversativo. "Devi" qui resta: è istruzione tecnica al lettore in registro didattico, accettabile.                    |
| 4  | 307  | "...significa un job schedulato o un DBA che se lo ricorda. Con interval Oracle le crea da solo. Un problema in meno." | "...significa un job schedulato o un DBA che se lo ricorda. Con interval Oracle le crea da solo. Una preoccupazione in meno." | Frame mentale         | Frase di chiusura, "problema" qui è etichetta narrativa.                                                                              |
| 5  | 315  | "...senza indice è comunque un problema."                                                       | "...senza indice è comunque una criticità."                                                             | Frame mentale         | Frame narrativo di chiusura paragrafo.                                                                                                |
| 6  | 330  | "Il mio errore più grande con il partitioning?"                                                 | "La mia svista più grande con il partitioning?"                                                         | Feedback costruttivo  | "Errore" autoreferenziale; "svista" è più morbido e meno identitario, in coerenza con il tono autoironico del paragrafo.             |

**Da LASCIARE (motivate)**:
- Riga 43: "Ma quando la tabella supera una certa dimensione..." — opposizione retorica tecnica reale (indici vs volume). Resta.
- Riga 49: "I problemi non si sono presentati tutti insieme" — uso narrativo specifico ("problemi" come elenco di sintomi numerati). Segnalato per discussione, ma propendo per lasciare: "Le criticità non si sono presentate" suona più freddo.
- Riga 51: "ma il numero di blocchi letti era mostruoso" — opposizione retorica tecnica (indice c'è ma costoso). Resta.
- Riga 51, 274, 313: "execution plan mostrava... ma il numero..." / "questo è l'errore più comune..." / "una singola TRUNC() nel predicato sbagliato" — "errore" qui è "errore di programmazione/SQL", descrizione tecnica neutra. Resta.
- Riga 80: "ma poi Oracle doveva andare a pescare..." — opposizione tecnica vera. Resta.
- Riga 95: "Non range partitioning classico, dove devi creare manualmente..." — descrizione tecnica neutra, "devi" descrittivo della tecnologia. Resta.
- Riga 143: "ma qualsiasi operazione DDL sulla partizione invalida l'indice intero" — opposizione tecnica reale (efficiente per query vs fragile su DDL). Resta.
- Riga 211: "potrebbe prendere decisioni sbagliate" — descrizione tecnica di un comportamento dell'optimizer. Resta.
- Riga 247: "Non è qualcosa che devi configurare" — descrizione tecnica neutra (non c'è da configurare). Resta.
- Riga 305: "Sembra ovvio, ma ho visto tabelle..." — opposizione retorica forte. Resta.
- Riga 309: "ma qualsiasi operazione DDL sulla partizione li invalida" — opposizione tecnica reale. Resta.
- Riga 313: "Non fidarti: verifica..." — istruzione tecnica diretta in registro didattico, "devi" non presente esplicitamente. OK.
- Riga 315: "Riduce il volume di dati da esaminare, ma dentro la partizione hai ancora bisogno..." — opposizione retorica tecnica. Resta.
- Riga 328: "Ma il momento giusto..." — opposizione retorica forte di chiusura sezione. Resta.

**STATO**: in attesa di approvazione

---

## oracle-roles-privileges

**File**: `content/posts/oracle/oracle-roles-privileges/index.it.md`
**Modifiche proposte**: 4

| #  | Riga | Originale (frammento)                                                                  | Proposto                                                                                          | Tema                  | Note                                                                                                                              |
|----|------|----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1  | 19   | "Quel giorno il problema non sono più i permessi."                                      | "Quel giorno la criticità non sono più i permessi."                                              | Frame mentale         | Frame narrativo, sostituibile.                                                                                                    |
| 2  | 27   | "Il problema era semplice da descrivere:"                                               | "La situazione era semplice da descrivere:"                                                       | Frame mentale         | Frame narrativo di apertura elenco, non descrizione tecnica.                                                                      |
| 3  | 69   | "I ruoli predefiniti hanno un problema storico:"                                        | "I ruoli predefiniti hanno un punto critico storico:"                                             | Frame mentale         | Frame narrativo.                                                                                                                  |
| 4  | 277  | "Ogni errore era in realtà un problema nascosto che prima era invisibile."              | "Ogni mancato funzionamento era in realtà una criticità nascosta che prima era invisibile."       | Frame mentale         | Coppia "errore"+"problema" in una stessa frase: doppia sostituzione per coerenza. "Errore" qui è generalizzato narrativamente.    |

**Da LASCIARE (motivate)**:
- Riga 15: "senza problemi di permessi" — citazione tra virgolette ("Così funziona tutto senza problemi di permessi."), intoccabile.
- Riga 17: "sulla tabella sbagliata" — descrizione tecnica concreta (target sbagliato del DROP). Resta.
- Riga 37: "ha cancellato per errore i dati di fatturazione" — locuzione idiomatica "per errore" = inavvertitamente, sostituirla altererebbe il senso. Resta.
- Riga 129: "Ma il processo applicativo prevede una disattivazione" — opposizione retorica vera (tecnicamente possibile vs processo). Resta.
- Riga 190: "Ma prima di eseguirla, ho verificato..." — opposizione retorica forte (una riga sola vs verifica preventiva). Resta.
- Riga 208: "ma non ha più il potere di fare qualsiasi cosa" — opposizione retorica essenziale (proprietà vs onnipotenza). Resta.
- Riga 267: "Esiste ma pericoloso" — tabella comparativa, opposizione retorica condensata. Resta.
- Riga 269: "il più ricco e il più granulare, ma anche il più facile da configurare male" — opposizione retorica tecnica fondamentale. Resta.
- Riga 277: "Ogni errore..." — vedi modifica #4.
- Riga 292: "eliminano gli errori di permesso. Ma eliminano anche qualsiasi protezione." — opposizione retorica chiave del paragrafo. Resta. "Errori di permesso" è descrizione tecnica.
- Riga 296: "Ma è quello che fa la differenza" — opposizione retorica di chiusura forte (non glamour vs valore). Resta.

**STATO**: in attesa di approvazione

---

## Riepilogo

| Articolo                    | Modifiche proposte |
|-----------------------------|--------------------|
| oracle-awr-ash              | 4                  |
| oracle-cloud-migration      | 5                  |
| oracle-data-guard           | 3                  |
| oracle-linux-kernel         | 3                  |
| oracle-partitioning         | 6                  |
| oracle-roles-privileges     | 4                  |
| **Totale**                  | **25**             |

**Articoli più "puliti"** (3 modifiche): `oracle-data-guard`, `oracle-linux-kernel`.
**Articolo più "carico"** (6 modifiche): `oracle-partitioning`.

**Pattern dominante**: la stragrande maggioranza delle modifiche riguarda il tema **Frame mentale** (`problema` generico narrativo da sostituire con `criticità` / `situazione` / `punto` / `questione`) e il tema **Connessione positiva** (`Ma` puramente avversativo a inizio frase narrativa, da sostituire con `E` / `Solo che`).

**Osservazioni trasversali**:
- Gli articoli Oracle hanno uno stile maturo: molte occorrenze di `ma` sono opposizioni retoriche tecniche legittime (sembra X tecnicamente, ma in realtà Y), che restano intatte.
- Il termine `errore` compare quasi sempre in contesto tecnico-descrittivo (errore SQL, errore di permesso, errore logico) o in negazione esplicativa ("non per errore — per omissione") e non va sostituito.
- Non sono presenti: `forse`, `magari`, `spero`, `provo`, `cercherò`, `dovresti`, `non riesco`, `non posso`, `non funziona`, `non va bene`, `sono bloccato`, `fallimento`, `difficile`, `impossibile` (in forma identitaria).
- Compaiono `bisogna` (2 occorrenze in `oracle-cloud-migration`, sostituibili) e `devi` (più occorrenze, quasi tutte istruzioni tecniche legittime al lettore DBA: lasciate).
- Nessun caso di auto-affermazione di onestà (`raccontato`, `onestamente`), nessun ricorso a clichè AI.
