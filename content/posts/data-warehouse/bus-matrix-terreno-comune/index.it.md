---
title: "Tre data mart, tre verità sulle vendite: il bus matrix come terreno comune"
description: "Un gruppo assicurativo multi-paese con tre reparti, tre data mart cresciuti in autonomia e tre numeri diversi sulle polizze emesse a febbraio. Il bus matrix non l'ha risolto in un pomeriggio — ma ha dato un terreno condiviso su cui cominciare a parlare."
date: "2026-05-12T08:03:00+01:00"
draft: false
translationKey: "bus_matrix_terreno_comune"
tags: ["data-warehouse", "bus-matrix", "conformed-dimensions", "kimball", "dimensional-modeling", "data-mart"]
categories: ["Data Warehouse"]
image: "bus-matrix-terreno-comune.cover.jpg"
---

Il primo meeting è stato strano. In sala c'erano tre persone — il responsabile della direzione commerciale, la marketing manager della rete agenziale, il controller della direzione amministrativa — e ognuno aveva davanti un foglio Excel con le nuove polizze emesse a febbraio in un grande gruppo assicurativo italiano, operativo in più paesi europei. I totali non coincidevano. Scarti del 9%, del 12%, del 16% a seconda del confronto. E nessuno dei tre sembrava particolarmente sorpreso.

*"Facciamo così da sempre,"* ha detto il controller. *"Ognuno ha il suo. Poi quando il board chiede la raccolta premi, passiamo il mio perché è quello che torna con la chiusura contabile."*

Ecco il punto di partenza del progetto. Non un disastro scoperto da me, non un sistema da salvare. Una situazione che loro conoscevano benissimo e che era diventata ingestibile quando il nuovo CFO, arrivato da qualche settimana, aveva cominciato a fare domande scomode. Tipo: *perché la raccolta premi per ramo è diversa tra commerciale e finance?* Oppure: *quanti assicurati attivi abbiamo davvero in Italia, 420mila o 510mila?*

Non avevamo una risposta. Ne avevamo tre.

## 🧩 Tre data mart cresciuti per conto loro

Ogni reparto, negli anni, si era costruito il proprio {{< glossary term="data-mart" >}}data mart{{< /glossary >}}. Non per cattiveria, non per scelta strategica: per necessità. L'IT centrale era lento, i progetti duravano mesi, i reparti avevano bisogno di numeri adesso. Così ognuno si era fatto il suo — a volte con tool BI diversi, a volte appoggiandosi allo stesso database ma in schemi separati.

Il risultato, a distanza di anni, era questo:

| Data mart      | Grain principale                       | Dimensioni                              | Sistema sorgente                 |
|----------------|----------------------------------------|-----------------------------------------|----------------------------------|
| Commerciale    | Polizza × movimento × giorno           | Assicurato, Prodotto, Agenzia, Data     | Policy Management (mainframe)    |
| Marketing      | Cliente × campagna × mese              | Cliente, Campagna, Canale, Mese         | CRM + piattaforma campaign mgmt  |
| Finance        | Movimento contabile × voce × mese      | Conto, Centro di costo, Ramo, Mese      | ERP contabilità + riassicurazione|

Tre {{< glossary term="star-schema" >}}star schema{{< /glossary >}}, tre definizioni di "cliente" (l'assicurato privato, l'azienda contraente, il contraente cointestato), tre calendari diversi (marketing sul mese solare, finance sul mese contabile con chiusure al 25, commerciale con la data di effetto della polizza che può slittare di mesi rispetto alla data di emissione). E soprattutto tre concetti di "prodotto": il policy management system identificava la polizza col codice tariffa interno, il CRM col macro-prodotto commerciale (Auto, Casa, Vita, Salute), il finance la raggruppava per ramo ai fini IVASS.

Ognuno dei tre numeri era *corretto* nel suo contesto. Il problema era che non si parlavano.

## 🔍 Il CFO aveva visto il problema prima di noi

La cosa onesta da dire è che il problema l'aveva messo in agenda il CFO, non il team IT e non io. Lui non voleva un data warehouse nuovo. Voleva una cosa più banale: una riga di numeri che fosse la stessa su tutti i cruscotti. *"Non mi importa chi ha ragione tra di voi. Mi importa che la raccolta premi di febbraio sia un numero solo."*

Detto così sembra ovvio. In pratica, quando chiedi a tre reparti di allineare le definizioni, scopri che ognuno ha ragionato per anni su una sua mappa del territorio e non ha voglia di ridisegnarla. Il commerciale conta i premi lordi alla data di emissione, il finance li conta netti da commissioni alla data di competenza. Il marketing considera "cliente attivo" chi ha almeno una polizza in vigore negli ultimi 12 mesi, il finance chi ha una posizione premi aperta nell'esercizio. Nessuno sbaglia. Semplicemente rispondono a domande diverse.

La prima cosa utile che abbiamo fatto, prima ancora di toccare una riga di codice, è stata una serie di workshop di due ore — uno per ogni dimensione candidata — in cui ciascun reparto spiegava cosa intendeva. A verbale. Il {{< glossary term="bus-matrix" >}}bus matrix{{< /glossary >}} che abbiamo poi disegnato non è nato da una genialata architetturale: è nato dalla trascrizione di quei workshop.

## 🚌 Il bus matrix, spiegato senza mitologia

Ralph {{< glossary term="kimball" >}}Kimball{{< /glossary >}} descrive il bus matrix come una matrice due-dimensioni: sulle righe i **processi di business** (vendite in negozio, campagne marketing, ciclo attivo di fatturazione, resi, movimenti di magazzino…), sulle colonne le **dimensioni conformi** (cliente, prodotto, negozio, data, geografia…). Nelle celle, una X se quel processo di business usa quella dimensione.

La matrice, da sola, non fa nulla. Non genera codice, non crea tabelle, non risolve conflitti. Serve a una cosa sola: costringere tutti a guardare lo stesso foglio.

Quello che siamo arrivati a disegnare, dopo i workshop, era una cosa del genere (semplificata):

| Processo di business        | Cliente | Polizza | Intermediario | Data | Campagna | Canale | Conto |
|-----------------------------|:-------:|:-------:|:-------------:|:----:|:--------:|:------:|:-----:|
| Emissione polizze           |   X     |    X    |      X        |  X   |    X     |   X    |       |
| Rinnovi                     |   X     |    X    |      X        |  X   |          |   X    |       |
| Sinistri aperti             |   X     |    X    |               |  X   |          |        |       |
| Campagne su intermediari    |         |         |      X        |  X   |    X     |   X    |       |
| Incassi premi               |   X     |    X    |      X        |  X   |          |        |   X   |
| Sottoscrizioni online       |   X     |    X    |               |  X   |    X     |   X    |       |

Sei righe, sette colonne. Letto così, il foglio dice una cosa semplice e scomoda insieme: **la dimensione Cliente appare in cinque processi su sei, la Polizza in cinque, la Data in tutti e l'Intermediario in quattro**. Se la definizione di Cliente è diversa tra commerciale e marketing, cinque processi su sei restituiranno numeri incoerenti. Non è un problema di BI, è un problema di anagrafica.

## 🔗 Cos'è una dimensione conforme

Una {{< glossary term="conformed-dimension" >}}dimensione conforme{{< /glossary >}} è una dimensione che ha la stessa struttura, la stessa semantica e la stessa chiave attraverso più data mart. Non vuol dire "una sola tabella fisica condivisa" — può essere replicata, può vivere in schemi diversi — ma vuol dire che se il cliente `C_00217654` compare nel data mart commerciale e in quello marketing, **è lo stesso cliente, con gli stessi attributi di classificazione, e i numeri che lo riguardano si possono sommare senza riserve**.

Conformare una dimensione significa concordare tre cose:

1. **La chiave naturale**: qual è l'identificativo unico del cliente? Il codice fiscale? L'e-mail? Il numero tessera fedeltà? Nei tre sistemi era diverso — il POS usava la tessera fedeltà (ma solo per chi la usava in cassa), il CRM usava l'e-mail, il finance usava il codice cliente dell'ERP. Senza una mappatura esplicita, tre clienti "diversi" potevano essere la stessa persona.

2. **Gli attributi condivisi**: quali colonne appartengono alla dimensione conforme? Regione, provincia, fascia d'età, data iscrizione programma fedeltà, canale di acquisizione. Tutto il resto resta in tabelle dimensionali *locali* al singolo data mart, ma non interferisce con le analisi cross-reparto.

3. **La grana**: la dimensione conforme ha una riga per cliente individuale, non una riga per "segmento di clienti". Se il marketing vuole ragionare per segmento, aggiunge un attributo `segmento_marketing` alla dimensione conforme e lo valorizza con la propria logica.

Su queste tre cose ci abbiamo lavorato sei settimane. Non è stato divertente. Il marketing temeva di perdere il proprio modello di segmentazione, il commerciale non voleva che l'anagrafica passasse "sotto controllo finance". Il compromesso è stato: dimensione conforme gestita da un nuovo team dati centrale, con rappresentanti dei tre reparti nel comitato di governance.

## 🛠️ Come abbiamo integrato senza riscrivere tutto

Qui c'è la parte tecnica che di solito passa in secondo piano rispetto alla narrazione del "progetto salvato". La verità è che non abbiamo riscritto i tre data mart. Sarebbe stato un progetto da due anni e nessuno ce l'avrebbe finanziato.

La strategia è stata a strati.

**Strato 1 — Dimensioni conformi centralizzate.** Abbiamo creato uno schema `dim_conformed` con le dimensioni condivise (`dim_customer`, `dim_product`, `dim_store`, `dim_date`, `dim_promotion`, `dim_channel`). La `dim_customer` è la più complessa: popolata da un processo di record matching tra POS, CRM ed ERP, con regole esplicite per i collision (stesso codice fiscale, e-mail diverse → merge; stessa e-mail, codici fiscali diversi → flag manuale).

```sql
CREATE TABLE dim_conformed.dim_customer (
    sk_customer         BIGINT PRIMARY KEY,      -- chiave surrogata
    customer_code       VARCHAR(20) NOT NULL,    -- chiave naturale concordata
    loyalty_card_id     VARCHAR(20),
    email_primary       VARCHAR(120),
    fiscal_code         VARCHAR(16),
    first_name          VARCHAR(80),
    last_name           VARCHAR(80),
    birth_year          INT,
    gender              CHAR(1),
    region              VARCHAR(40),             -- attributo geografico conforme
    province            VARCHAR(40),
    acquisition_channel VARCHAR(30),             -- store, web, app, campagna
    loyalty_tier        VARCHAR(20),
    loyalty_since       DATE,
    status              VARCHAR(10),             -- active, dormant, churned
    valid_from          DATE NOT NULL,
    valid_to            DATE,                    -- SCD Tipo 2 su region, tier, status
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    record_source       VARCHAR(20),             -- POS, CRM, ERP, MERGE
    last_update_ts      TIMESTAMP NOT NULL
);

CREATE INDEX ix_dim_customer_natural ON dim_conformed.dim_customer(customer_code, is_current);
CREATE INDEX ix_dim_customer_loyalty ON dim_conformed.dim_customer(loyalty_card_id) WHERE loyalty_card_id IS NOT NULL;
```

Circa 1,9 milioni di righe per 1,2 milioni di clienti distinti (la differenza è lo storico delle versioni in {{< glossary term="scd" >}}SCD Tipo 2{{< /glossary >}}).

**Strato 2 — Bridge tra vecchie chiavi e nuove chiavi.** I tre data mart esistenti continuavano a funzionare con le loro chiavi locali. Abbiamo creato una tabella di mappatura per ciascuno:

```sql
CREATE TABLE dim_conformed.xref_customer (
    source_system   VARCHAR(10) NOT NULL,   -- POS | CRM | ERP
    source_key      VARCHAR(50) NOT NULL,   -- chiave locale nel sistema di origine
    sk_customer     BIGINT NOT NULL,        -- puntatore alla dim_customer conforme
    mapping_quality VARCHAR(20),            -- exact_match, fuzzy_match, manual
    mapping_ts      TIMESTAMP NOT NULL,
    PRIMARY KEY (source_system, source_key)
);
```

La xref è popolata da un job notturno che legge le anagrafiche sorgenti, confronta con la dimensione conforme, applica le regole di matching e logga i casi ambigui in una tabella di anomalie gestita manualmente dal team dati.

**Strato 3 — Viste di integrazione.** Sopra i tre {{< glossary term="fact-table" >}}fact table{{< /glossary >}} originali, abbiamo creato viste che sostituiscono la chiave locale con la chiave surrogata conforme:

```sql
CREATE OR REPLACE VIEW vw_fact_sales_conformed AS
SELECT
    f.sale_id,
    xc.sk_customer,           -- chiave conforme, non più quella POS locale
    xp.sk_product,
    xs.sk_store,
    xd.sk_date,
    f.quantity,
    f.gross_amount,
    f.discount_amount,
    f.net_amount,
    f.cost_amount
FROM sales_dm.fact_sales f
LEFT JOIN dim_conformed.xref_customer xc
       ON xc.source_system = 'POS' AND xc.source_key = f.pos_customer_code
LEFT JOIN dim_conformed.xref_product  xp
       ON xp.source_system = 'POS' AND xp.source_key = f.pos_product_ean
LEFT JOIN dim_conformed.xref_store    xs
       ON xs.source_system = 'POS' AND xs.source_key = f.pos_store_code
JOIN dim_conformed.dim_date xd
       ON xd.calendar_date = f.sale_date;
```

Nessun reparto ha dovuto smettere di usare il proprio data mart. Chi voleva analisi mono-reparto, continuava a farle sul proprio. Chi aveva bisogno di cross-reparto, usava le viste conformi.

## 📊 La domanda che prima era impossibile

La prima query davvero cross-mart che abbiamo lanciato — e che prima del lavoro sulle dimensioni conformi sarebbe uscita con tre risposte diverse — era banale a vedersi:

```sql
-- Clienti che hanno ricevuto una campagna e hanno comprato nei 30 giorni successivi
SELECT
    dc.region,
    dc.loyalty_tier,
    COUNT(DISTINCT dc.sk_customer)       AS targeted_customers,
    COUNT(DISTINCT vs.sk_customer)       AS converted_customers,
    ROUND(100.0 * COUNT(DISTINCT vs.sk_customer)
          / NULLIF(COUNT(DISTINCT dc.sk_customer), 0), 1) AS conversion_rate_pct,
    SUM(vs.net_amount)                   AS revenue_from_campaign
FROM vw_fact_campaign_conformed cm
JOIN dim_conformed.dim_customer dc
     ON dc.sk_customer = cm.sk_customer AND dc.is_current
LEFT JOIN vw_fact_sales_conformed vs
     ON vs.sk_customer = cm.sk_customer
    AND vs.sk_date BETWEEN cm.sk_date AND cm.sk_date + 30
WHERE cm.campaign_code = 'SPRING_2026_RUN'
GROUP BY dc.region, dc.loyalty_tier
ORDER BY conversion_rate_pct DESC;
```

Prima, questa query si faceva esportando due CSV, caricandoli in Excel e facendo CERCA.VERT sul codice cliente — che nei due sistemi era scritto diverso. Gli errori di matching erano nell'ordine del 20-30%, e nessuno li misurava.

Dopo, la query gira in circa 4 secondi su Postgres con i dati di un trimestre e produce **un solo numero** per combinazione regione × tier fedeltà. Il marketing lo confronta con finance, finance lo confronta con commerciale, e se c'è discrepanza si va a guardare il join: non il concetto di cliente.

| Metrica                             | Prima                      | Dopo                         |
|--------------------------------------|----------------------------|------------------------------|
| Definizioni di "cliente"             | 3                          | 1 (più attributi specifici)  |
| Scarti tra cruscotti reparto         | 8-15% a seconda del KPI    | < 0,5% (solo timing ETL)     |
| Tempo per analisi cross-reparto      | 1-2 giorni di Excel        | query diretta su viste       |
| Costo del re-platforming             | stimato 18-24 mesi         | 4 mesi + governance continua |

Il tempo del re-platforming totale non l'abbiamo mai pagato perché non è stato necessario. Il bus matrix e le dimensioni conformi non sostituiscono un refactoring: danno il tempo per farlo con calma quando serve davvero, un processo alla volta.

## 🧠 Perché il bus matrix va fatto prima di codificare

Il motivo per cui questa cosa va fatta all'inizio — e non dopo che tre data mart sono cresciuti per conto loro — è banale: conformare dopo costa dieci volte di più che conformare prima.

Quando parti da zero, la dimensione conforme è un documento di una pagina e mezza scritto in una riunione di due ore. Quando parti da tre data mart in produzione da sei anni, è un progetto di sei mesi con un comitato di governance, un team dati centrale, un processo di matching da costruire, tabelle di mappatura da mantenere e lock organizzativi da negoziare.

Kimball ha scritto il bus matrix negli anni '90 con questa esatta intenzione: dare ai team un foglio di carta da mettere al muro prima di aprire l'editor SQL. È un esercizio di allineamento, non di architettura. L'architettura viene dopo, e viene molto meglio se il foglio di carta è stato fatto.

## Quello che ho imparato

Il lavoro tecnico — la dim_customer, le xref, le viste — è stato la parte più semplice. La parte difficile è stata portare tre reparti a concordare cosa vuol dire "cliente". E quella parte non l'ho risolta io: l'ha risolta il CFO con il suo peso politico, il comitato di governance con sei settimane di pazienza, e il DBA del cliente che aveva una memoria storica impressionante di ogni scelta fatta negli anni precedenti e perché.

Quando vedo un progetto di DWH che parte senza un bus matrix disegnato e condiviso, oggi alzo la mano prima di iniziare. Non per fare il saggio — per ricordarmi che quella fase là, quella di allineare le definizioni, non si può saltare. Se la salti, la paghi dopo con gli interessi. Se la fai, il resto del progetto diventa quasi noioso. Ed è esattamente come dovrebbe essere.

------------------------------------------------------------------------

## Glossario

**[Bus Matrix](/it/glossary/bus-matrix/)** — Matrice bidimensionale Kimball con i processi di business sulle righe e le dimensioni conformi sulle colonne. Serve ad allineare i reparti sulle definizioni prima di iniziare la progettazione fisica del data warehouse.

**[Conformed Dimension](/it/glossary/conformed-dimension/)** — Dimensione condivisa con la stessa struttura, semantica e chiave tra più data mart. Permette di sommare misure provenienti da processi di business diversi senza ambiguità.

**[Data Mart](/it/glossary/data-mart/)** — Sottoinsieme del data warehouse focalizzato su un singolo processo di business o area funzionale (vendite, marketing, finance). Può essere costruito in autonomia da un reparto ma rischia di divergere dagli altri se manca la conformità delle dimensioni.

**[Kimball](/it/glossary/kimball/)** — Ralph Kimball, metodologia di progettazione data warehouse basata su dimensional modeling, star schema e bus matrix. Approccio bottom-up che parte dai processi di business e costruisce data mart integrati tramite dimensioni conformi.

**[Star Schema](/it/glossary/star-schema/)** — Modello di dati con una fact table al centro collegata a più tabelle dimensionali. È il pattern base di ogni data mart Kimball e il terreno naturale su cui agiscono le dimensioni conformi.
