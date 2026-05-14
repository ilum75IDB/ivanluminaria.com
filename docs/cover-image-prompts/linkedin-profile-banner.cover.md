# Cover image prompt — linkedin-profile-banner.cover.jpg

## Profilo di riferimento

- **Destinazione**: cover image profilo LinkedIn di Ivan Luminaria
- **Stile editoriale**: coerente con `ivanluminaria.com` (illustrazione retrò anni '50, palette seppia/ocra/marrone con accenti rosso Oracle `#F80000` e blu Postgres `#336791`)
- **Riferimento visivo principale**: `docs/cover-image-prompts/database-strategy.cover.md` (banner panoramico esistente per la macro-sezione)

## Descrizione della scena

Composizione editoriale **panoramica** in formato banner ultra-largo (ratio 4:1), su carta beige invecchiata con grana di stampa offset visibile. La scena è una **cover da magazine business vintage degli anni '50** — tipo *Time/Fortune cover* — divisa visivamente in tre zone orizzontali fluidamente connesse. La zona del volto è **fotorealistica**; le zone tipografica e degli strumenti restano in **stile illustrato**, collegate al volto tramite trattamento cromatico e grana di stampa uniforme.

**Zona sinistra (~30% della larghezza)** — *Il ritratto*: **ritratto fotorealistico** di Ivan Luminaria (foto sorgente fornita dall'utente), mezzo busto, posa frontale leggermente di 3/4, sguardo rivolto verso destra (verso il centro della scena, in direzione del testo). Indossa **giacca scura su gilet rosso ruggine e cravatta scura**, coerente con il personaggio ricorrente del sito. **Trattamento cromatico critico**: la foto deve essere **virata in toni caldi seppia/ocra/marrone** (LUT vintage in stile cover magazine anni '50), con saturazione moderata, grana di stampa offset sovrapposta per integrarla nel resto dell'illustrazione, leggero vignetting ai bordi. Il bilanciamento del bianco è caldo, il contrasto morbido. L'effetto finale è un **ritratto editoriale d'epoca**: riconoscibile come fotografia reale, contemporaneamente parte coerente del manifesto. Sfondo dietro al ritratto: tinta uniforme color carta beige con leggera trama, oppure libreria sfocata in seppia.

**Zona centrale (~40% della larghezza)** — *Il nome e il claim*: in carattere serif robusto bicolore (rosso Oracle `#F80000` sopra, blu Postgres `#336791` sotto) la scritta su due righe **`IVAN LUMINARIA`** (rossa, più grande) e sotto **`DATABASE STRATEGY`** (blu, leggermente più piccola). Una piccola **stella decorativa** a cinque punte sopra la scritta. Sotto le due righe, una **fascetta orizzontale stretta** in carattere sans-serif sottile maiuscoletto: **`ORACLE DBA  ·  DWH ARCHITECT  ·  POSTGRESQL  ·  MYSQL  ·  PROJECT MANAGEMENT`**, in marrone scuro su sfondo carta. Tipografia tipo manifesto litografico anni '50.

**Zona destra (~30% della larghezza)** — *Gli strumenti del mestiere*: **illustrazione editoriale** in stile coerente con le cover del sito. Una composizione di oggetti simbolici distribuiti naturalmente, non in griglia: una fila di tre piccoli **rack server** stilizzati con LED rossi, connessi a un piccolo macchinario a ingranaggi (rimando alla cover `database-strategy`); accanto un **piccolo monitor CRT** che mostra un grafico lineare ascendente; sopra una **lampada da scrivania** in ottone con paralume nero che illumina la scena lateralmente; in primo piano, un piccolo **manometro analogico** e una **lente d'ingrandimento** dal manico rosso appoggiata su un foglio di appunti tecnici con la scritta *"OBSERVE. MEASURE. UNDERSTAND."* in caratteri rosso e nero (richiamo alla cover #87). Tra i due piani, un piccolo **disco cilindrico stratificato** (database stilizzato) emette delicati raggi luminosi.

**Sullo sfondo della zona destra**, sfumato in tinta seppia, si intuisce una **facciata classica con due colonne ioniche** (richiamo alla cover Oracle) — appena accennata, non dominante.

**Trattamento di "ponte" tra fotorealistico e illustrato**: tutta la composizione condivide la stessa **palette cromatica calda** (seppia/ocra/marrone con accenti rosso Oracle e blu Postgres), la stessa **grana di stampa offset** sovrapposta uniformemente sull'intera immagine, e la stessa **luce laterale calda** (provenienza apparente: lampada da scrivania a destra). Il volto fotografico è "filtrato dall'epoca" — sembra deliberatamente uno scatto degli anni '50, non una foto contemporanea incollata su un disegno.

## Metafora visiva

Il **profilo professionale come cover di magazine business vintage**: il consulente al lavoro (volto reale, riconoscibile), il suo nome come titolo della testata, gli strumenti del mestiere come iconografia editoriale a contorno. Nessuna posa eroica, nessun "tech rockstar" — il ritratto è composto, l'espressione è quella di un artigiano che presenta i suoi attrezzi, non quella di un guru che si auto-celebra.

Il mix **volto fotorealistico + ambiente illustrato + palette unificante** comunica una doppia natura: la persona reale dietro al blog (la foto rende riconoscibili, "ci metto la faccia") e la coerenza con l'identità visiva del sito (stessa palette, stessi strumenti, stesso personaggio narrativo). La doppia bicromia **rosso Oracle / blu Postgres** nel naming visualizza la doppia anima del consulente (Oracle storico + open-source moderno), mentre la fascetta sotto enumera in modo sobrio le competenze senza enfasi.

## Note operative per la generazione

- **Foto sorgente richiesta**: ritratto frontale o leggermente di 3/4 di Ivan Luminaria, illuminazione naturale o da studio, sfondo neutro (verrà sostituito), risoluzione minima ~1500 px sul lato lungo
- **Outfit consigliato nella foto**: giacca scura su camicia chiara, eventualmente cravatta scura. Se la foto sorgente ha un altro outfit, il generatore può adattare i colori del vestito alla palette in fase di trattamento
- **Espressione**: composta, leggero sorriso accennato o sguardo concentrato (no risata aperta — manterrebbe il tono no-eroe)
- **Trattamento richiesto**: virare l'intera immagine generata (volto + sfondo + illustrazione) con la stessa LUT cromatica unificante, applicare grana di stampa offset uniforme su tutta la cover

## File output

- **Nome file**: `linkedin-profile-banner.cover.jpg`
- **Dimensioni**: **1968 × 492 px** (ratio 4:1, stesso del banner LinkedIn attuale)
- **Formato**: JPG, qualità alta (≥ 90%)
- **Path archiviazione locale** (opzionale, se vuoi tenere il file nel repo): `static/img/linkedin-profile-banner.jpg`
- **Destinazione di pubblicazione**: profilo LinkedIn di Ivan Luminaria, sezione "cover image"
