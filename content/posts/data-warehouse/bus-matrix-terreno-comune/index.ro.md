---
title: "Trei data marts, trei adevăruri despre vânzări: bus matrix ca teren comun"
description: "Un grup de asigurări multi-țară cu trei departamente, trei data marts crescute autonom și trei numere diferite pentru polițele emise în februarie. Bus matrix nu a rezolvat totul într-o după-amiază — dar a dat un teren comun pe care să începem să discutăm."
date: "2026-05-12T08:03:00+01:00"
draft: false
translationKey: "bus_matrix_terreno_comune"
tags: ["data-warehouse", "bus-matrix", "conformed-dimensions", "kimball", "dimensional-modeling", "data-mart"]
categories: ["Data Warehouse"]
image: "bus-matrix-terreno-comune.cover.jpg"
---

Prima ședință a fost ciudată. În sală erau trei persoane — responsabilul comercial, marketing manager al rețelei de agenții, controllerul direcției administrative — și fiecare avea în față un Excel cu noile polițe emise în februarie într-un mare grup de asigurări italian care operează în mai multe țări europene. Totalurile nu coincideau. Diferențe de 9%, 12%, 16% în funcție de comparație. Niciunul dintre cei trei nu părea deosebit de surprins.

*"Așa facem dintotdeauna,"* a spus controllerul. *"Fiecare cu al lui. Apoi, când board-ul cere încasarea de prime, dăm numărul meu pentru că e cel care cadrează cu închiderea contabilă."*

Ăsta era punctul de plecare al proiectului. Nu un dezastru descoperit de mine, nu un sistem de salvat. O situație pe care cei trei o cunoșteau foarte bine și care devenise de negestionat când noul CFO, ajuns de câteva săptămâni, începuse să pună întrebări incomode. De genul: *de ce primele subscrise pe ramură sunt diferite între comercial și finance?* Sau: *câți asigurați activi avem de fapt în Italia, 420 de mii sau 510 mii?*

Nu aveam un răspuns. Aveam trei.

## 🧩 Trei data marts crescute pe cont propriu

Fiecare departament, de-a lungul anilor, își construise propriul {{< glossary term="data-mart" >}}data mart{{< /glossary >}}. Nu din rea-voință, nu din alegere strategică: din necesitate. IT-ul central era lent, proiectele durau luni, departamentele aveau nevoie de numere acum. Așa că fiecare și-a făcut al lui — uneori cu tool-uri BI diferite, alteori pe aceeași bază de date, dar în scheme separate.

Rezultatul, după ani, era acesta:

| Data mart   | Grain principal                          | Dimensiuni                                   | Sistem sursă                          |
|-------------|------------------------------------------|----------------------------------------------|---------------------------------------|
| Comercial   | Poliță × mișcare × zi                    | Asigurat, Produs, Agenție, Data              | Policy Management (mainframe)         |
| Marketing   | Client × campanie × lună                 | Client, Campanie, Canal, Lună                | CRM + platformă campaign management   |
| Finance     | Mișcare contabilă × poziție × lună       | Cont, Centru de cost, Ramură, Lună           | ERP contabilitate + reasigurare       |

Trei {{< glossary term="star-schema" >}}star schema{{< /glossary >}}, trei definiții de "client" (asiguratul persoană fizică, compania contractantă, contractantul cu titularitate comună), trei calendare diferite (marketing pe luna solară, finance pe luna contabilă cu închidere pe 25, comercial cu data de efect a poliței care poate fi cu luni în urmă față de data emiterii). Și mai ales trei concepte de "produs": policy management identifica polița cu codul de tarif intern, CRM cu macroprodusul comercial (Auto, Casă, Viață, Sănătate), finance o grupa după ramură pentru IVASS.

Fiecare dintre cele trei numere era *corect* în contextul lui. Problema era că nu își vorbeau între ele.

## 🔍 CFO-ul văzuse problema înaintea noastră

Onest este să spun că problema a fost pusă pe agendă de CFO, nu de echipa IT și nici de mine. El nu voia un data warehouse nou. Voia ceva mai simplu: o linie de numere care să fie aceeași pe toate dashboard-urile. *"Nu mă interesează cine dintre voi are dreptate. Mă interesează ca primele subscrise din februarie să fie un singur număr."*

Spus așa pare evident. În practică, când ceri la trei departamente să alinieze definițiile, descoperi că fiecare a raționat ani de zile pe propria hartă a teritoriului și nu are chef să o redeseneze. Comercialul numără primele brute la data emiterii, finance-ul le numără nete de comisioane la data devansării. Marketingul consideră "client activ" pe oricine cu cel puțin o poliță în vigoare în ultimele 12 luni, finance pe oricine cu o poziție de prime deschisă în exercițiul fiscal. Nimeni nu greșește. Pur și simplu răspund la întrebări diferite.

Primul lucru util pe care l-am făcut, înainte de a atinge o linie de cod, a fost o serie de ateliere de două ore — unul pentru fiecare dimensiune candidată — în care fiecare departament explica ce înțelegea. Cu proces-verbal. {{< glossary term="bus-matrix" >}}Bus matrix{{< /glossary >}}-ul pe care l-am desenat apoi nu s-a născut dintr-o idee arhitecturală genială: s-a născut din transcrierea acelor ateliere.

## 🚌 Bus matrix, fără mitologie

Ralph {{< glossary term="kimball" >}}Kimball{{< /glossary >}} descrie bus matrix ca o matrice bidimensională: pe rânduri **procesele de business** (în cazul nostru emitere polițe, reînnoiri, daune, încasări de prime, campanii de marketing, subscrieri online…), pe coloane **dimensiunile conforme** (client, poliță, intermediar, data, campanie, canal…). În celule, un X dacă acel proces de business folosește acea dimensiune.

Matricea, în sine, nu face nimic. Nu generează cod, nu creează tabele, nu rezolvă conflicte. Servește la un singur lucru: să oblige pe toți să privească aceeași foaie.

Ceea ce am ajuns să desenăm, după ateliere, arăta cam așa (simplificat):

| Proces de business              | Client | Poliță | Intermediar | Data | Campanie | Canal | Cont |
|---------------------------------|:------:|:------:|:-----------:|:----:|:--------:|:-----:|:----:|
| Emitere polițe                  |   X    |   X    |      X      |  X   |    X     |   X   |      |
| Reînnoiri                       |   X    |   X    |      X      |  X   |          |   X   |      |
| Daune deschise                  |   X    |   X    |             |  X   |          |       |      |
| Campanii pe intermediari        |        |        |      X      |  X   |    X     |   X   |      |
| Încasări prime                  |   X    |   X    |      X      |  X   |          |       |  X   |
| Subscrieri online               |   X    |   X    |             |  X   |    X     |   X   |      |

Șase rânduri, șapte coloane. Citită așa, foaia spune ceva simplu și incomod în același timp: **dimensiunea Client apare în cinci procese din șase, Polița în cinci, Data în toate și Intermediarul în patru**. Dacă definiția de Client este diferită între comercial și marketing, cinci procese din șase vor returna numere incoerente. Nu este o problemă de BI, este o problemă de master data.

## 🔗 Ce este o dimensiune conformă

O {{< glossary term="conformed-dimension" >}}dimensiune conformă{{< /glossary >}} este o dimensiune care are aceeași structură, aceeași semantică și aceeași cheie prin mai multe data marts. Nu înseamnă "un singur tabel fizic partajat" — poate fi replicată, poate trăi în scheme diferite — dar înseamnă că dacă clientul `IT_C00217654` apare în data mart-ul comercial și în cel de marketing, **este același client, cu aceleași atribute de clasificare, iar numerele referitoare la el se pot însuma fără rezerve**.

A conforma o dimensiune înseamnă a te pune de acord pe trei lucruri:

1. **Cheia naturală**: care este identificatorul unic al clientului? Codul fiscal? CUI-ul? Codul contractant din sistemul de polițe? În cele trei sistem era diferit — policy management folosea codul contractant al mainframe-ului (cu logici de deduplicare moștenite din anii '90), CRM folosea email + cod fiscal, finance folosea codul client al ERP-ului cu propria sa numerotare. Fără o mapare explicită, trei "contractanți" diferiți puteau fi aceeași persoană — și mai rău, în țări diferite cheia naturală se schimba: codice fiscale în Italia, NIF în Spania, SIREN sau număr fiscal individual în Franța.

2. **Atributele partajate**: ce coloane aparțin dimensiunii conforme? Țară, regiune, provincie, tip contractant (persoană fizică / juridică), categorie de vârstă, segment de risc, data primului contract, canal de achiziție. Tot restul rămâne în tabele dimensionale *locale* fiecărui data mart, fără să interfereze cu analizele cross-departament.

3. **Grain-ul**: dimensiunea conformă are un rând per contractant individual, nu un rând per "segment de clienți". Dacă marketingul vrea să raționeze pe segmente, adaugă un atribut `segment_marketing` la dimensiunea conformă și îl completează cu propria sa logică.

La aceste trei lucruri am lucrat șase săptămâni. Nu a fost distractiv. Marketingul se temea să nu piardă propriul model de segmentare comportamentală, comercialul nu voia ca baza de contractanți să ajungă "sub controlul finance-ului", iar finance-ul pretindea ca cheia naturală să fie a lor pentru că "este cea folosită pentru facturare și pentru IVASS". Compromisul a fost: dimensiune conformă gestionată de o nouă echipă centrală de date, cu reprezentanți ai celor trei departamente în comitetul de guvernanță și o cheie surogat internă care servește ca pivot între cele trei chei naturale diferite.

## 🛠️ Cum am integrat fără să rescriem tot

Aici e partea tehnică, care de obicei rămâne pe planul doi față de narativa "proiectului salvat". Adevărul este că nu am rescris cele trei data marts. Ar fi fost un proiect de doi ani și nimeni nu l-ar fi finanțat.

Strategia a fost pe straturi.

**Stratul 1 — Dimensiuni conforme centralizate.** Am creat o schemă `dim_conformed` cu dimensiunile partajate (`dim_customer`, `dim_policy`, `dim_intermediary`, `dim_date`, `dim_campaign`, `dim_channel`). `dim_customer` este cea mai complexă: populată printr-un proces de record matching între policy management, CRM și ERP, cu reguli explicite pentru coliziuni (același cod fiscal, naționalități diferite → merge dacă aceeași țară de rezidență; același email, coduri fiscale diferite → flag manual).

```sql
CREATE TABLE dim_conformed.dim_customer (
    sk_customer         BIGINT PRIMARY KEY,      -- cheie surogat centrală
    customer_code       VARCHAR(20) NOT NULL,    -- cheie naturală agreată
    country_code        CHAR(2)  NOT NULL,       -- IT, ES, FR, DE, ...
    tax_id              VARCHAR(20),             -- CF / NIF / SIREN / Steuer-ID
    email_primary       VARCHAR(120),
    party_type          VARCHAR(10),             -- person, company
    first_name          VARCHAR(80),
    last_name           VARCHAR(80),
    legal_name          VARCHAR(120),            -- pentru persoane juridice
    birth_year          INT,                     -- NULL pentru companii
    gender              CHAR(1),                 -- NULL pentru companii
    region              VARCHAR(40),
    province            VARCHAR(40),
    risk_segment        VARCHAR(20),             -- low, medium, high
    acquisition_channel VARCHAR(30),             -- agency, broker, direct, online
    first_policy_date   DATE,                    -- data primului contract în grup
    status              VARCHAR(10),             -- active, dormant, churned
    valid_from          DATE NOT NULL,
    valid_to            DATE,                    -- SCD Tip 2 pe region, risk_segment, status
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    record_source       VARCHAR(20),             -- PMS, CRM, ERP, MERGE
    last_update_ts      TIMESTAMP NOT NULL
);

CREATE INDEX ix_dim_customer_natural ON dim_conformed.dim_customer(customer_code, is_current);
CREATE INDEX ix_dim_customer_tax_id  ON dim_conformed.dim_customer(country_code, tax_id) WHERE tax_id IS NOT NULL;
```

Circa 3,1 milioane de rânduri pentru 1,8 milioane de contractanți distincți în cele patru țări principale (diferența este istoricul versiunilor în {{< glossary term="scd" >}}SCD Tip 2{{< /glossary >}}).

**Stratul 2 — Bridge între chei vechi și chei noi.** Cele trei data marts existente continuau să funcționeze cu cheile lor locale. Am creat un tabel de mapare pentru fiecare:

```sql
CREATE TABLE dim_conformed.xref_customer (
    source_system   VARCHAR(10) NOT NULL,   -- PMS | CRM | ERP
    country_code    CHAR(2)     NOT NULL,   -- pentru a distinge omonimiile între țări
    source_key      VARCHAR(50) NOT NULL,   -- cheia locală în sistemul sursă
    sk_customer     BIGINT      NOT NULL,   -- pointer către dim_customer conformă
    mapping_quality VARCHAR(20),            -- exact_match, fuzzy_match, manual
    mapping_ts      TIMESTAMP   NOT NULL,
    PRIMARY KEY (source_system, country_code, source_key)
);
```

Xref-ul este populat de un job nocturn care citește master-ele sursă, compară cu dimensiunea conformă, aplică regulile de matching și înregistrează cazurile ambigue într-un tabel de anomalii gestionat manual de echipa de date. În cele patru țări, coada cazurilor ambigue era în jurul de 1,5% — un volum gestionabil de două persoane în două ore pe zi.

**Stratul 3 — Viste de integrare.** Peste cele trei {{< glossary term="fact-table" >}}fact tables{{< /glossary >}} originale am creat viste care înlocuiesc cheia locală cu cheia surogat conformă:

```sql
CREATE OR REPLACE VIEW vw_fact_new_business_conformed AS
SELECT
    f.policy_id,
    xc.sk_customer,           -- cheie conformă, nu cea locală PMS
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

Niciun departament nu a fost nevoit să renunțe la propriul data mart. Cine voia analize mono-departament continua să le facă pe al lui. Cine avea nevoie de analize cross-departament folosea vistele conforme.

## 📊 Întrebarea care înainte era imposibilă

Prima interogare cu adevărat cross-mart pe care am lansat-o — cea care înainte de munca pe dimensiunile conforme ar fi ieșit cu trei răspunsuri diferite — părea banală:

```sql
-- Intermediari atinși de o campanie și polițe noi emise în următoarele 60 de zile
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

Înainte, această interogare se făcea exportând două CSV-uri, încărcându-le în Excel și făcând VLOOKUP pe codul agentului/contractantului — care în cele două sisteme era scris diferit (CRM folosea codul intern de broker, PMS codul RUI). Erorile de matching erau în ordinul 20-30% și nimeni nu le măsura. Gestionarea pe țări adăuga complicații: un broker care opera atât în Italia cât și în Spania apărea de două ori.

După, interogarea rulează în circa 5 secunde pe Oracle Exadata cu datele unui trimestru în cele patru țări și produce **un singur număr** per combinație țară × segment de risc. Marketingul îl compară cu finance, finance îl compară cu comercial, iar dacă există discrepanță se uită la join: nu la conceptul de client.

| Metrică                               | Înainte                    | După                          |
|---------------------------------------|----------------------------|-------------------------------|
| Definiții de "contractant"            | 3                          | 1 (cu atribute specifice pe departament) |
| Diferențe între dashboard-urile de departament | 9-16% în funcție de KPI | < 0,5% (doar timing ETL)   |
| Timp pentru analize cross-departament | 1-2 zile de Excel          | interogare directă pe viste   |
| Costul re-platforming-ului complet    | estimat 18-24 luni         | 4 luni + guvernanță continuă  |

Costul re-platforming-ului complet nu l-am plătit niciodată pentru că nu a fost necesar. Bus matrix și dimensiunile conforme nu înlocuiesc un refactor: îți cumpără timpul să îl faci cu calm atunci când chiar este nevoie, un proces pe rând.

## 🧠 De ce bus matrix se face înainte de codificare

Motivul pentru care această muncă se face la început — și nu după ce trei data marts au crescut pe cont propriu — este simplu: a conforma după costă de zece ori mai mult decât a conforma înainte.

Când pleci de la zero, dimensiunea conformă este un document de o pagină și jumătate scris într-o ședință de două ore. Când pleci de la trei data marts în producție de șase ani, este un proiect de șase luni cu un comitet de guvernanță, o echipă centrală de date, un proces de matching de construit, tabele de mapare de întreținut și blocaje organizaționale de negociat.

Kimball a scris despre bus matrix în anii '90 cu exact această intenție: să dea echipelor o foaie de hârtie de pus pe perete înainte de a deschide editorul SQL. Este un exercițiu de aliniere, nu de arhitectură. Arhitectura vine după, și iese mult mai bine dacă foaia de hârtie a fost făcută.

## Ce am învățat

Munca tehnică — `dim_customer`, xref-urile, vistele — a fost partea ușoară. Partea dificilă a fost să aduci trei departamente la un acord pe ceea ce înseamnă "client". Și acea parte nu am rezolvat-o eu: a rezolvat-o CFO-ul cu greutatea sa politică, comitetul de guvernanță cu șase săptămâni de răbdare și DBA-ul clientului care avea o memorie istorică impresionantă a fiecărei decizii luate în anii anteriori și de ce.

Când văd astăzi un proiect de DWH care pornește fără un bus matrix desenat și împărtășit, ridic mâna înainte de a începe. Nu ca să mă dau înțelept — ca să îmi amintesc că acea fază, cea de aliniere a definițiilor, nu poate fi sărită. Dacă o sari, o plătești după cu dobândă. Dacă o faci, restul proiectului devine aproape plictisitor. Și este exact cum ar trebui să fie.

------------------------------------------------------------------------

## Glosar

**[Bus Matrix](/ro/glossary/bus-matrix/)** — Matrice bidimensională Kimball cu procesele de business pe rânduri și dimensiunile conforme pe coloane. Servește la alinierea departamentelor pe definiții înainte de a începe proiectarea fizică a data warehouse-ului.

**[Conformed Dimension](/ro/glossary/conformed-dimension/)** — Dimensiune partajată cu aceeași structură, semantică și cheie între mai multe data marts. Permite însumarea măsurilor provenind din procese de business diferite fără ambiguitate.

**[Data Mart](/ro/glossary/data-mart/)** — Submulțime a data warehouse-ului focalizată pe un singur proces de business sau arie funcțională (vânzări, marketing, finance). Poate fi construit autonom de un departament, dar riscă să diverge de celelalte dacă lipsește conformitatea dimensiunilor.

**[Kimball](/ro/glossary/kimball/)** — Ralph Kimball, metodologie de proiectare a data warehouse-ului bazată pe modelare dimensională, star schema și bus matrix. Abordare bottom-up care pleacă de la procesele de business și construiește data marts integrate prin dimensiuni conforme.

**[Star Schema](/ro/glossary/star-schema/)** — Model de date cu o fact table centrală legată de mai multe tabele dimensionale. Este pattern-ul de bază al oricărui data mart Kimball și terenul natural pe care acționează dimensiunile conforme.
