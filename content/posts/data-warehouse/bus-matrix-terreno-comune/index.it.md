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

Ralph {{< glossary term="kimball" >}}Kimball{{< /glossary >}} descrive il bus matrix come una matrice due-dimensioni: sulle righe i **processi di business** (nel nostro caso emissione polizze, rinnovi, sinistri, incassi premi, campagne marketing, sottoscrizioni online…), sulle colonne le **dimensioni conformi** (cliente, polizza, intermediario, data, campagna, canale…). Nelle celle, una X se quel processo di business usa quella dimensione.

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

Una {{< glossary term="conformed-dimension" >}}dimensione conforme{{< /glossary >}} è una dimensione che ha la stessa struttura, la stessa semantica e la stessa chiave attraverso più data mart. Non vuol dire "una sola tabella fisica condivisa" — può essere replicata, può vivere in schemi diversi — ma vuol dire che se il contraente `IT_C00217654` compare nel data mart commerciale e in quello marketing, **è lo stesso contraente, con gli stessi attributi di classificazione, e i numeri che lo riguardano si possono sommare senza riserve**.

Conformare una dimensione significa concordare tre cose:

1. **La chiave naturale**: qual è l'identificativo unico del cliente? Il codice fiscale? La partita IVA? Il codice contraente del sistema polizze? Nei tre sistemi era diverso — il policy management usava il codice contraente del mainframe (con logiche di deduplica ereditate dagli anni '90), il CRM usava e-mail + codice fiscale, il finance usava il codice cliente dell'ERP con una propria numerazione. Senza una mappatura esplicita, tre contraenti "diversi" potevano essere la stessa persona — e peggio, in paesi diversi la chiave naturale cambiava: codice fiscale in Italia, NIF in Spagna, SIREN o numero fiscale individuale in Francia.

2. **Gli attributi condivisi**: quali colonne appartengono alla dimensione conforme? Paese, regione, provincia, tipo contraente (persona fisica / giuridica), fascia d'età, segmento di rischio, data primo contratto, canale di acquisizione. Tutto il resto resta in tabelle dimensionali *locali* al singolo data mart, ma non interferisce con le analisi cross-reparto.

3. **La grana**: la dimensione conforme ha una riga per contraente individuale, non una riga per "segmento clienti". Se il marketing vuole ragionare per segmento, aggiunge un attributo `segmento_marketing` alla dimensione conforme e lo valorizza con la propria logica.

Su queste tre cose ci abbiamo lavorato sei settimane. Non è stato divertente. Il marketing temeva di perdere il proprio modello di segmentazione comportamentale, il commerciale non voleva che l'anagrafica contraenti passasse "sotto controllo finance", e il finance pretendeva che la chiave naturale fosse la loro perché "è quella usata per la fatturazione e per IVASS". Il compromesso è stato: dimensione conforme gestita da un nuovo team dati centrale, con rappresentanti dei tre reparti nel comitato di governance e una chiave surrogata interna che fa da pivot tra le tre chiavi naturali diverse.

## 🛠️ Come abbiamo integrato senza riscrivere tutto

Qui c'è la parte tecnica che di solito passa in secondo piano rispetto alla narrazione del "progetto salvato". La verità è che non abbiamo riscritto i tre data mart. Sarebbe stato un progetto da due anni e nessuno ce l'avrebbe finanziato.

La strategia è stata a strati.

**Strato 1 — Dimensioni conformi centralizzate.** Abbiamo creato uno schema `dim_conformed` con le dimensioni condivise (`dim_customer`, `dim_policy`, `dim_intermediary`, `dim_date`, `dim_campaign`, `dim_channel`). La `dim_customer` è la più complessa: popolata da un processo di record matching tra policy management, CRM ed ERP, con regole esplicite per i collision (stesso codice fiscale, nazionalità diverse → merge se stesso paese di residenza; stessa e-mail, codici fiscali diversi → flag manuale).

```sql
CREATE TABLE dim_conformed.dim_customer (
    sk_customer         BIGINT PRIMARY KEY,      -- chiave surrogata centrale
    customer_code       VARCHAR(20) NOT NULL,    -- chiave naturale concordata
    country_code        CHAR(2)  NOT NULL,       -- IT, ES, FR, DE, ...
    tax_id              VARCHAR(20),             -- CF / NIF / SIREN / Steuer-ID
    email_primary       VARCHAR(120),
    party_type          VARCHAR(10),             -- person, company
    first_name          VARCHAR(80),
    last_name           VARCHAR(80),
    legal_name          VARCHAR(120),            -- per persone giuridiche
    birth_year          INT,                     -- NULL per aziende
    gender              CHAR(1),                 -- NULL per aziende
    region              VARCHAR(40),
    province            VARCHAR(40),
    risk_segment        VARCHAR(20),             -- low, medium, high
    acquisition_channel VARCHAR(30),             -- agency, broker, direct, online
    first_policy_date   DATE,                    -- data primo contratto nel gruppo
    status              VARCHAR(10),             -- active, dormant, churned
    valid_from          DATE NOT NULL,
    valid_to            DATE,                    -- SCD Tipo 2 su region, risk_segment, status
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    record_source       VARCHAR(20),             -- PMS, CRM, ERP, MERGE
    last_update_ts      TIMESTAMP NOT NULL
);

CREATE INDEX ix_dim_customer_natural ON dim_conformed.dim_customer(customer_code, is_current);
CREATE INDEX ix_dim_customer_tax_id  ON dim_conformed.dim_customer(country_code, tax_id) WHERE tax_id IS NOT NULL;
```

Circa 3,1 milioni di righe per 1,8 milioni di contraenti distinti sui quattro paesi principali (la differenza è lo storico delle versioni in {{< glossary term="scd" >}}SCD Tipo 2{{< /glossary >}}).

**Strato 2 — Bridge tra vecchie chiavi e nuove chiavi.** I tre data mart esistenti continuavano a funzionare con le loro chiavi locali. Abbiamo creato una tabella di mappatura per ciascuno:

```sql
CREATE TABLE dim_conformed.xref_customer (
    source_system   VARCHAR(10) NOT NULL,   -- PMS | CRM | ERP
    country_code    CHAR(2)     NOT NULL,   -- per distinguere le omonimie tra paesi
    source_key      VARCHAR(50) NOT NULL,   -- chiave locale nel sistema di origine
    sk_customer     BIGINT      NOT NULL,   -- puntatore alla dim_customer conforme
    mapping_quality VARCHAR(20),            -- exact_match, fuzzy_match, manual
    mapping_ts      TIMESTAMP   NOT NULL,
    PRIMARY KEY (source_system, country_code, source_key)
);
```

La xref è popolata da un job notturno che legge le anagrafiche sorgenti, confronta con la dimensione conforme, applica le regole di matching e logga i casi ambigui in una tabella di anomalie gestita manualmente dal team dati. Sui quattro paesi, i casi ambigui in coda erano intorno all'1,5% — un volume gestibile da due persone in due ore al giorno.

**Strato 3 — Viste di integrazione.** Sopra i tre {{< glossary term="fact-table" >}}fact table{{< /glossary >}} originali, abbiamo creato viste che sostituiscono la chiave locale con la chiave surrogata conforme:

```sql
CREATE OR REPLACE VIEW vw_fact_new_business_conformed AS
SELECT
    f.policy_id,
    xc.sk_customer,           -- chiave conforme, non più quella PMS locale
    xp.sk_policy,
    xi.sk_intermediary,
    xd.sk_date,
    f.gross_premium,
    f.net_premium,
    f.commission_amount,
    f.policy_duration_months
FROM pms_dm.fact_new_business f
LEFT JOIN dim_conformed.xref_customer      xc
       ON xc.source_system = 'PMS'
      AND xc.country_code  = f.country_code
      AND xc.source_key    = f.pms_customer_code
LEFT JOIN dim_conformed.xref_policy        xp
       ON xp.source_system = 'PMS'
      AND xp.source_key    = f.pms_tariff_code
LEFT JOIN dim_conformed.xref_intermediary  xi
       ON xi.source_system = 'PMS'
      AND xi.country_code  = f.country_code
      AND xi.source_key    = f.pms_agent_code
JOIN dim_conformed.dim_date xd
       ON xd.calendar_date = f.effective_date;
```

Nessun reparto ha dovuto smettere di usare il proprio data mart. Chi voleva analisi mono-reparto, continuava a farle sul proprio. Chi aveva bisogno di cross-reparto, usava le viste conformi.

## 📊 La domanda che prima era impossibile

La prima query davvero cross-mart che abbiamo lanciato — e che prima del lavoro sulle dimensioni conformi sarebbe uscita con tre risposte diverse — era banale a vedersi:

```sql
-- Contraenti intermediari raggiunti da una campagna e nuove polizze emesse nei 60 giorni successivi
SELECT
    dc.country_code,
    dc.risk_segment,
    COUNT(DISTINCT cm.sk_intermediary)   AS targeted_intermediaries,
    COUNT(DISTINCT nb.sk_customer)       AS converted_customers,
    SUM(nb.gross_premium)                AS new_business_premium,
    ROUND(100.0 * COUNT(DISTINCT nb.sk_customer)
          / NULLIF(COUNT(DISTINCT cm.sk_intermediary), 0), 1) AS conversion_ratio_pct
FROM vw_fact_campaign_conformed cm
JOIN dim_conformed.dim_intermediary di
     ON di.sk_intermediary = cm.sk_intermediary AND di.is_current
LEFT JOIN vw_fact_new_business_conformed nb
     ON nb.sk_intermediary = cm.sk_intermediary
    AND nb.sk_date BETWEEN cm.sk_date AND cm.sk_date + 60
LEFT JOIN dim_conformed.dim_customer dc
     ON dc.sk_customer = nb.sk_customer AND dc.is_current
WHERE cm.campaign_code = 'Q1_2026_AUTO_BROKER_PUSH'
GROUP BY dc.country_code, dc.risk_segment
ORDER BY new_business_premium DESC NULLS LAST;
```

Prima, questa query si faceva esportando due CSV, caricandoli in Excel e facendo CERCA.VERT sul codice agente/contraente — che nei due sistemi era scritto diverso (il CRM usava il codice broker interno, il PMS il codice RUI). Gli errori di matching erano nell'ordine del 20-30%, e nessuno li misurava. Aggiungeva fatica anche la gestione del paese: un broker con operatività in Italia e Spagna compariva due volte.

Dopo, la query gira in circa 5 secondi su Oracle Exadata con i dati di un trimestre sui quattro paesi e produce **un solo numero** per combinazione paese × segmento di rischio. Il marketing lo confronta con finance, finance lo confronta con commerciale, e se c'è discrepanza si va a guardare il join: non il concetto di cliente.

| Metrica                              | Prima                      | Dopo                         |
|--------------------------------------|----------------------------|------------------------------|
| Definizioni di "contraente"          | 3                          | 1 (più attributi specifici)  |
| Scarti tra cruscotti reparto         | 9-16% a seconda del KPI    | < 0,5% (solo timing ETL)     |
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
