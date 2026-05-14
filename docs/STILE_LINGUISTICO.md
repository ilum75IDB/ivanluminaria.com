# Stile Linguistico — termini da evitare

Vocabolario di frasi e parole da **evitare** nella scrittura degli articoli del blog (e nelle email/post collegati), con relative proposte di sostituzione e alternative. Il file è pensato per essere consultato prima di scrivere o revisionare un articolo.

## Come usare questo file

**Per Claude (consultazione automatica)**:

1. **Prima di scrivere** un nuovo articolo o una sezione importante, fare un grep su questo file per i termini che si stanno per usare. Esempio: `grep -i "magari\|forse\|spero" docs/STILE_LINGUISTICO.md`
2. **Durante la revisione**, leggere la tabella alfabetica completa e identificare termini da sostituire
3. **In caso di dubbio**, consultare la sezione **Tema linguistico** del termine: il "perché" della sostituzione spesso suggerisce un'alternativa adatta al contesto specifico
4. Non applicare le sostituzioni in modo meccanico — il contesto può giustificare un'eccezione. Quando l'eccezione esiste, segnalarla brevemente

**Eccezioni note**: le voci negative ("non fare", "non preoccuparti", ecc.) sono pensate per la comunicazione interpersonale e formativa. In un articolo tecnico, "non si possono rimuovere valori in modo nativo" è una **descrizione di fatto**, non un'auto-programmazione negativa — può restare. Il filtro va applicato ai passaggi narrativi e personali, non alle constatazioni tecniche.

## Come aggiungere nuovi termini

1. Aggiungere la riga alla **Tabella alfabetica completa** mantenendo l'ordine alfabetico per "Frase da evitare"
2. Aggiungere la stessa voce (solo il termine, senza ripetere la descrizione) sotto il **Tema linguistico** appropriato nell'indice. Se il tema non esiste, crearlo
3. Aggiornare il contatore "Totale voci" in fondo al file
4. Commit con messaggio nel formato: `STILE_LINGUISTICO: aggiunta voce "<termine>" (tema: <tema>)`

---

## Tabella alfabetica completa

| Frase / parola da evitare    | Motivo                                   | Sostituzione consigliata       | Alternative                          | Tema linguistico                 |
|------------------------------|------------------------------------------|--------------------------------|--------------------------------------|----------------------------------|
| appena posso                 | Indefinito                               | entro oggi                     | entro venerdì                        | Precisione temporale             |
| arrangiati                   | Chiusura relazionale                     | vediamo come fare              | troviamo un modo                     | Collaborazione                   |
| attenzione a non sbagliare   | Focus sull'errore                        | fai con precisione             | controlla bene i passaggi            | Focus mentale                    |
| bisogna                      | Linguaggio impersonale                   | scegliamo di                   | decidiamo di                         | Coinvolgimento                   |
| brancolo nel buio            | Smarrimento                              | sto raccogliendo chiarezza     | sto esplorando opzioni               | Metafore cognitive               |
| calmati                      | Aumenta tensione                         | prendiamoci un momento         | affrontiamolo con calma              | Gestione emotiva                 |
| cercherò                     | Debole commitment                        | mi attivo                      | procedo, organizzo                   | Determinazione                   |
| che fatica                   | Amplifica peso mentale                   | richiede energia               | richiede attenzione                  | Stato mentale                    |
| ci penso                     | Rinvia senza impegno                     | ti aggiorno entro domani       | valuto e ti confermo                 | Chiarezza                        |
| come ti ho già detto         | Frustrazione implicita                   | riprendo il punto              | ricapitoliamo                        | Comunicazione calma              |
| comando aggressivo ("fallo") | Resistenza psicologica                   | richiesta collaborativa        | "puoi occupartene?"                  | Leadership                       |
| credo che                    | Riduce impatto                           | sono convinto che              | vedo che, emerge che                 | Leadership linguistica           |
| criticare                    | Attiva difese                            | dare feedback                  | offrire osservazioni                 | Relazione                        |
| devi (obbligo verso altri)   | Attiva resistenza                        | puoi                           | ti conviene, sarebbe utile           | Persuasione                      |
| devi (obbligo verso sé)      | Peso obbligatorio                        | scelgo di                      | è importante per me                  | Motivazione                      |
| devi capire                  | Superiorità implicita                    | ti spiego il mio punto         | condivido la logica                  | Dialogo                          |
| difficile                    | Genera blocco mentale                    | impegnativo                    | sfidante, articolato                 | Percezione della realtà          |
| dovresti                     | Senso di colpa                           | potrebbe aiutarti              | sarebbe utile                        | Coaching                         |
| è colpa del destino          | Esternalizzazione                        | vediamo cosa posso influenzare | concentriamoci sulle azioni          | Responsabilità personale         |
| è colpa tua                  | Attacco diretto                          | analizziamo cosa è successo    | troviamo la causa                    | Gestione conflitti               |
| è ovvio                      | Svaluta l'altro                          | può sembrare evidente          | vediamolo insieme                    | Rispetto                         |
| è sempre così                | Generalizzazione                         | succede spesso                 | in alcuni casi                       | Precisione cognitiva             |
| è un casino                  | Caos emotivo                             | va riorganizzato               | è complesso                          | Ordine mentale                   |
| è un disastro                | Catastrofismo                            | ci sono criticità              | serve un intervento                  | Gestione emotiva                 |
| è urgente                    | Genera stress                            | è prioritario                  | serve attenzione immediata           | Gestione pressione               |
| errore                       | Attiva difesa e colpa                    | correzione                     | miglioria, revisione                 | Feedback costruttivo             |
| fai come vuoi                | Distacco aggressivo                      | valuta tu                      | decidiamo insieme                    | Relazione                        |
| fallimento                   | Etichetta negativa                       | esperienza                     | passaggio, apprendimento             | Crescita                         |
| forse                        | Incertezza                               | probabilmente                  | ritengo, è possibile                 | Sicurezza comunicativa           |
| giudicare                    | Polarizza                                | osservare                      | comprendere                          | Comunicazione consapevole        |
| hai dimenticato              | Colpevolizza                             | manca questo punto             | aggiungiamo anche                    | Cooperazione                     |
| hai sbagliato                | Colpevolizza                             | rivediamo questo punto         | possiamo correggere                  | Feedback                         |
| hai torto                    | Scontro diretto                          | vedo la cosa diversamente      | consideriamo anche questo            | Dialettica                       |
| ho il freno a mano tirato    | Auto-limitazione                         | sto riprendendo slancio        | sto accelerando gradualmente         | Metafore motivazionali           |
| impossibile                  | Chiude possibilità                       | complesso                      | richiede strategia, poco pratico ora | Apertura mentale                 |
| lamentarsi                   | Mantiene focus negativo                  | proporre                       | suggerire, costruire                 | Mentalità costruttiva            |
| ma                           | Cancella mentalmente ciò che precede     | e                              | inoltre, allo stesso tempo           | Connessione positiva             |
| magari                       | Vaghezza                                 | definiamo                      | valutiamo, scegliamo                 | Precisione                       |
| mi fai arrabbiare            | Scarico responsabilità                   | questa situazione mi irrita    | preferirei un altro approccio        | Responsabilità emotiva           |
| mi tocca                     | Subìto                                   | me ne occupo                   | lo gestisco                          | Responsabilità                   |
| nessuno capisce              | Isolamento                               | devo spiegarmi meglio          | cerco un confronto più chiaro        | Relazione                        |
| no                           | Chiusura immediata                       | vediamo alternative            | in questo modo no, ma…               | Negoziazione                     |
| no perché                    | Resistenza                               | sì, e possiamo anche…          | una soluzione alternativa è          | Comunicazione collaborativa      |
| non agitarti                 | Evoca agitazione                         | resta concentrato              | mantieni calma                       | Stato emotivo                    |
| non arrivare tardi           | Visualizza ritardo                       | arriva puntuale                | sii lì per le 9                      | Direzione positiva               |
| non capisci                  | Attacco personale                        | provo a spiegarmi meglio       | vediamolo insieme                    | Relazione                        |
| non cambia mai niente        | Disfattismo                              | il cambiamento richiede tempo  | vediamo cosa possiamo migliorare     | Mentalità evolutiva              |
| non ce la faccio             | Impotenza                                | devo riorganizzarmi            | mi serve supporto                    | Autoefficacia                    |
| non è giusto                 | Vittimismo                               | cerchiamo equilibrio           | rivediamo i criteri                  | Negoziazione                     |
| non fare                     | Il cervello visualizza l'azione negativa | fai così                       | concentrati su                       | Linguaggio positivo              |
| non funziona                 | Chiusura                                 | va ottimizzato                 | richiede revisione                   | Problem solving                  |
| non ho tempo                 | Scarico di responsabilità                | non è una priorità ora         | devo ripianificare                   | Gestione priorità                |
| non mi interessa             | Chiusura                                 | non è prioritario per me       | preferisco altro                     | Assertività                      |
| non posso                    | Impotenza                                | valuto alternative             | ora non è prioritario                | Linguaggio della possibilità     |
| non preoccuparti             | Attiva preoccupazione                    | siamo sotto controllo          | abbiamo un piano                     | Sicurezza                        |
| non riesco mai               | Auto-programmazione negativa             | sto imparando                  | non ci sono ancora riuscito          | Crescita personale               |
| non so                       | Chiusura cognitiva                       | verifico                       | controllo, approfondisco             | Problem solving                  |
| non va bene                  | Critica vaga                             | possiamo migliorarlo così      | ecco cosa ottimizzerei               | Feedback efficace                |
| odio questa cosa             | Polarizzazione                           | non mi convince                | preferisco altro                     | Comunicazione equilibrata        |
| pazienza                     | Rinuncia passiva                         | troviamo una soluzione         | valutiamo alternative                | Proattività                      |
| penso che                    | Indebolisce affermazione                 | ritengo                        | la mia analisi è, considero          | Autorevolezza                    |
| però                         | Introduce opposizione                    | e al tempo stesso              | contemporaneamente, insieme a questo | Riduzione conflitto              |
| prima o poi                  | Nessun commitment                        | entro una data precisa         | pianifico per                        | Affidabilità                     |
| problema                     | Evoca ostacolo e stress                  | situazione                     | aspetto, punto, elemento             | Frame mentale                    |
| provo                        | Comunica incertezza                      | faccio                         | verifico, me ne occupo               | Responsabilità                   |
| qualsiasi cosa               | Vaghezza                                 | scegliamo tra queste opzioni   | definiamo priorità                   | Precisione                       |
| sbagliato                    | Giudizio identitario                     | migliorabile                   | perfezionabile, rivedibile           | Comunicazione non aggressiva     |
| scusa il disturbo            | Auto-svalutazione                        | grazie del tempo               | apprezzo la disponibilità            | Autorevolezza                    |
| se riesco                    | Predispone fallimento                    | organizzo il necessario        | faccio il possibile entro            | Mentalità orientata al risultato |
| sei disordinato              | Etichetta identitaria                    | questa parte va riordinata     | possiamo organizzare meglio          | Identità vs comportamento        |
| sei in ritardo               | Accusa                                   | aggiorniamo le tempistiche     | riallineiamo i tempi                 | Collaborazione                   |
| sei negativo                 | Etichetta mentale                        | vedo delle preoccupazioni      | analizziamo i rischi                 | Comunicazione empatica           |
| sono bloccato                | Immobilità                               | sto cercando una soluzione     | sto ridefinendo l'approccio          | Metafore                         |
| sono costretto               | Perdita di controllo                     | è necessario                   | lo considero utile                   | Percezione del controllo         |
| sono fatto male              | Identità negativa                        | sto migliorando                | sto crescendo                        | Identità                         |
| sono incapace                | Auto-etichetta                           | devo allenarmi                 | posso migliorare                     | Autoefficacia                    |
| sono sfortunato              | Vittimismo identitario                   | sto cercando opportunità       | sto costruendo risultati             | Mentalità                        |
| sono stanco morto            | Drammatizzazione                         | ho bisogno di recuperare       | devo rallentare un attimo            | Energia personale                |
| spero                        | Mancanza di controllo                    | lavoriamo per                  | puntiamo a, costruiamo               | Orientamento al risultato        |
| subito                       | Pressione aggressiva                     | appena possibile               | con priorità                         | Collaborazione                   |
| te l'avevo detto             | Umiliazione                              | ora sappiamo come gestirlo     | facciamone tesoro                    | Gestione relazione               |
| ti disturbo?                 | Introduce fastidio                       | hai due minuti?                | quando puoi, ti aggiorno su una cosa | Apertura relazionale             |
| ti rubo un minuto            | Evoca perdita                            | vado rapido                    | sarò breve, sintesi veloce           | Linguaggio energetico            |
| ti sei spiegato male         | Colpa all'altro                          | voglio capire meglio           | approfondiamo questo punto           | Ascolto                          |
| tutti fanno così             | Generalizzazione sociale                 | molte persone                  | alcuni casi                          | Accuratezza                      |
| un attimo                    | Riduce importanza personale              | un momento                     | qualche minuto                       | Autorevolezza                    |
| urgentissimo                 | Amplifica ansia                          | molto importante               | alta priorità                        | Regolazione emotiva              |
| vediamo                      | Ambiguità                                | decidiamo                      | pianifichiamo                        | Azione                           |

---

## Indice per tema linguistico

Le voci sono raggruppate per macro-area. Cliccando il termine si trova la riga corrispondente nella tabella alfabetica.

### Accuratezza e precisione
- Accuratezza: `tutti fanno così`
- Affidabilità: `prima o poi`
- Azione: `vediamo`
- Chiarezza: `ci penso`
- Precisione: `magari`, `qualsiasi cosa`
- Precisione cognitiva: `è sempre così`
- Precisione temporale: `appena posso`

### Autorevolezza e responsabilità
- Assertività: `non mi interessa`
- Autorevolezza: `penso che`, `scusa il disturbo`, `un attimo`
- Determinazione: `cercherò`
- Leadership: `comando aggressivo ("fallo")`
- Leadership linguistica: `credo che`
- Responsabilità: `mi tocca`, `provo`
- Responsabilità emotiva: `mi fai arrabbiare`
- Responsabilità personale: `è colpa del destino`
- Sicurezza comunicativa: `forse`

### Comunicazione costruttiva
- Comunicazione calma: `come ti ho già detto`
- Comunicazione collaborativa: `no perché`
- Comunicazione consapevole: `giudicare`
- Comunicazione empatica: `sei negativo`
- Comunicazione equilibrata: `odio questa cosa`
- Comunicazione non aggressiva: `sbagliato`
- Connessione positiva: `ma`
- Frame mentale: `problema`
- Linguaggio positivo: `non fare`
- Mentalità costruttiva: `lamentarsi`
- Riduzione conflitto: `però`

### Feedback e relazione
- Apertura relazionale: `ti disturbo?`
- Ascolto: `ti sei spiegato male`
- Collaborazione: `arrangiati`, `sei in ritardo`, `subito`
- Cooperazione: `hai dimenticato`
- Dialettica: `hai torto`
- Dialogo: `devi capire`
- Feedback: `hai sbagliato`
- Feedback costruttivo: `errore`
- Feedback efficace: `non va bene`
- Gestione conflitti: `è colpa tua`
- Gestione relazione: `te l'avevo detto`
- Negoziazione: `no`, `non è giusto`
- Relazione: `criticare`, `fai come vuoi`, `nessuno capisce`, `non capisci`
- Rispetto: `è ovvio`

### Gestione emotiva e energia
- Energia personale: `sono stanco morto`
- Focus mentale: `attenzione a non sbagliare`
- Gestione emotiva: `calmati`, `è un disastro`
- Gestione pressione: `è urgente`
- Gestione priorità: `non ho tempo`
- Linguaggio energetico: `ti rubo un minuto`
- Ordine mentale: `è un casino`
- Percezione del controllo: `sono costretto`
- Percezione della realtà: `difficile`
- Regolazione emotiva: `urgentissimo`
- Sicurezza: `non preoccuparti`
- Stato emotivo: `non agitarti`
- Stato mentale: `che fatica`

### Identità, crescita e mindset
- Apertura mentale: `impossibile`
- Autoefficacia: `non ce la faccio`, `sono incapace`
- Coaching: `dovresti`
- Crescita: `fallimento`
- Crescita personale: `non riesco mai`
- Identità: `sono fatto male`
- Identità vs comportamento: `sei disordinato`
- Mentalità: `sono sfortunato`
- Mentalità evolutiva: `non cambia mai niente`
- Motivazione: `devi` (obbligo verso sé)

### Persuasione e direzione
- Coinvolgimento: `bisogna`
- Direzione positiva: `non arrivare tardi`
- Linguaggio della possibilità: `non posso`
- Mentalità orientata al risultato: `se riesco`
- Orientamento al risultato: `spero`
- Persuasione: `devi` (obbligo verso altri)
- Proattività: `pazienza`
- Problem solving: `non funziona`, `non so`

### Metafore
- Metafore: `sono bloccato`
- Metafore cognitive: `brancolo nel buio`
- Metafore motivazionali: `ho il freno a mano tirato`

---

**Ultimo aggiornamento**: 2026-05-13
**Totale voci**: 88
**Totale temi linguistici**: 51
