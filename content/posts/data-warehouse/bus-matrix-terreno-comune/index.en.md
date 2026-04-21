---
title: "Three data marts, three truths about sales: the bus matrix as common ground"
description: "A multi-country insurance group with three departments, three data marts that grew in isolation and three different numbers for policies written in February. The bus matrix didn't fix it in an afternoon — but it gave us shared ground to start talking on."
date: "2026-05-12T08:03:00+01:00"
draft: false
translationKey: "bus_matrix_terreno_comune"
tags: ["data-warehouse", "bus-matrix", "conformed-dimensions", "kimball", "dimensional-modeling", "data-mart"]
categories: ["Data Warehouse"]
image: "bus-matrix-terreno-comune.cover.jpg"
---

The first meeting was awkward. Three people in the room — the head of commercial, the agency-network marketing manager, the administrative controller — and each one had in front of them an Excel sheet showing the new policies written in February across a large Italian insurance group operating in several European countries. The totals didn't match. Gaps of 9%, 12%, 16% depending on which two you compared. None of the three looked particularly surprised.

*"We've always done it this way,"* said the controller. *"Each of us has our own. Then when the board asks for written premium, we hand over mine because it's the one that ties with the accounting close."*

That was the starting point of the project. Not a disaster I discovered, not a system I had to save. A situation all three of them knew perfectly well, and that had become unmanageable when the new CFO — just a few weeks in — started asking uncomfortable questions. Things like: *why is premium written by line of business different between commercial and finance?* Or: *how many active policyholders do we actually have in Italy, 420 thousand or 510 thousand?*

We didn't have an answer. We had three.

## 🧩 Three data marts that grew on their own

Each department had built its own {{< glossary term="data-mart" >}}data mart{{< /glossary >}} over the years. Not out of malice, not as a strategic choice: out of necessity. Central IT was slow, projects took months, and the departments needed numbers now. So each of them built their own — sometimes with different BI tools, sometimes sitting on the same database but in separate schemas.

Years later, the picture looked like this:

| Data mart   | Main grain                             | Dimensions                                 | Source system                       |
|-------------|----------------------------------------|--------------------------------------------|-------------------------------------|
| Commercial  | Policy × movement × day                | Policyholder, Product, Agency, Date        | Policy Management (mainframe)       |
| Marketing   | Customer × campaign × month            | Customer, Campaign, Channel, Month         | CRM + campaign management platform  |
| Finance     | Accounting entry × line item × month   | Account, Cost center, Line of business, Month | Accounting ERP + reinsurance ledger |

Three {{< glossary term="star-schema" >}}star schemas{{< /glossary >}}, three definitions of "customer" (the individual policyholder, the corporate contract holder, the jointly-named contract holder), three different calendars (marketing on the solar month, finance on the accounting month with closes on the 25th, commercial on the policy effective date which can lag months behind the issue date). And above all, three different notions of "product": policy management identified the policy by its internal tariff code, the CRM by the commercial macro-product (Auto, Home, Life, Health), and finance grouped it by line of business for IVASS reporting.

Each of the three numbers was *correct* in its own context. The problem was that they didn't talk to each other.

## 🔍 The CFO had seen the problem before we did

The honest thing to say is that the problem was put on the agenda by the CFO, not by the IT team and not by me. He didn't want a new data warehouse. He wanted something much more mundane: one line of numbers that read the same on every dashboard. *"I don't care which of you is right. I care that February's written premium is a single number."*

Said like that it sounds obvious. In practice, when you ask three departments to align definitions, you discover that each of them has spent years reasoning on their own map of the territory and has no interest in redrawing it. Commercial counts gross premium at issue date; finance counts net of commissions at accounting date. Marketing considers an "active customer" anyone with at least one in-force policy in the last 12 months; finance counts anyone with an open premium position within the fiscal year. No one is wrong. They're simply answering different questions.

The first useful thing we did, before touching a line of code, was a series of two-hour workshops — one per candidate dimension — where each department explained what it meant. Minuted. The {{< glossary term="bus-matrix" >}}bus matrix{{< /glossary >}} we eventually drew didn't come from an architectural stroke of genius: it came from the transcript of those workshops.

## 🚌 The bus matrix, without the mythology

Ralph {{< glossary term="kimball" >}}Kimball{{< /glossary >}} describes the bus matrix as a two-dimensional grid: rows are **business processes** (in our case policy issuance, renewals, claims, premium collection, marketing campaigns, online subscriptions…), columns are the **conformed dimensions** (customer, policy, intermediary, date, campaign, channel…). In each cell, an X if that business process uses that dimension.

The matrix on its own does nothing. It doesn't generate code, doesn't create tables, doesn't resolve conflicts. It's for one thing only: forcing everyone to look at the same sheet of paper.

What we ended up drawing, after the workshops, looked like this (simplified):

| Business process            | Customer | Policy | Intermediary | Date | Campaign | Channel | Account |
|-----------------------------|:--------:|:------:|:------------:|:----:|:--------:|:-------:|:-------:|
| Policy issuance             |    X     |   X    |      X       |  X   |    X     |    X    |         |
| Renewals                    |    X     |   X    |      X       |  X   |          |    X    |         |
| Claims opening              |    X     |   X    |              |  X   |          |         |         |
| Campaigns on intermediaries |          |        |      X       |  X   |    X     |    X    |         |
| Premium collection          |    X     |   X    |      X       |  X   |          |         |    X    |
| Online subscriptions        |    X     |   X    |              |  X   |    X     |    X    |         |

Six rows, seven columns. Read that way, the sheet says something simple and uncomfortable at the same time: **the Customer dimension shows up in five out of six processes, Policy in five, Date in all of them, and Intermediary in four**. If the definition of Customer differs between commercial and marketing, five out of six processes will return inconsistent numbers. That's not a BI problem, it's a master-data problem.

## 🔗 What a conformed dimension is

A {{< glossary term="conformed-dimension" >}}conformed dimension{{< /glossary >}} is a dimension with the same structure, the same semantics and the same key across multiple data marts. It doesn't mean "one single shared physical table" — it can be replicated, it can live in different schemas — but it does mean that if customer `IT_C00217654` appears in both the commercial and the marketing data mart, **it is the same customer, with the same classification attributes, and the numbers about them can be summed without reservations**.

Conforming a dimension means agreeing on three things:

1. **The natural key**: what's the unique identifier for the customer? Tax ID? VAT number? The policyholder code from the policy system? In the three systems it was different — policy management used the mainframe policyholder code (with dedup logic inherited from the '90s), the CRM used email + tax ID, and finance used the ERP customer code with its own numbering. Without an explicit mapping, three "different" contract holders could turn out to be the same person — and worse still, across countries the natural key changed: tax code in Italy, NIF in Spain, SIREN or individual tax number in France.

2. **Shared attributes**: which columns belong to the conformed dimension? Country, region, province, party type (individual / legal entity), age bracket, risk segment, first contract date, acquisition channel. Everything else stays in dimension tables *local* to each single data mart, without interfering with cross-department analytics.

3. **The grain**: the conformed dimension has one row per individual customer, not one row per "customer segment". If marketing wants to reason by segment, it adds a `marketing_segment` attribute to the conformed dimension and populates it with its own logic.

We worked six weeks on these three things. It wasn't fun. Marketing was worried about losing its behavioral segmentation model, commercial didn't want the customer master to come "under finance's control", and finance insisted the natural key had to be theirs because "it's the one used for billing and for IVASS". The compromise was: conformed dimension owned by a new central data team, with representatives from the three departments on the governance committee, and an internal surrogate key acting as a pivot between the three different natural keys.

## 🛠️ How we integrated without rewriting everything

Here's the technical part that usually gets second billing compared to the "saved the project" narrative. The truth is we didn't rewrite the three data marts. It would have been a two-year project and no one would have funded it.

The strategy was layered.

**Layer 1 — Centralized conformed dimensions.** We created a `dim_conformed` schema with the shared dimensions (`dim_customer`, `dim_policy`, `dim_intermediary`, `dim_date`, `dim_campaign`, `dim_channel`). `dim_customer` is the most complex: populated by a record-matching process across policy management, CRM and ERP, with explicit rules for collisions (same tax ID, different nationalities → merge if same country of residence; same email, different tax IDs → manual flag).

```sql
CREATE TABLE dim_conformed.dim_customer (
    sk_customer         BIGINT PRIMARY KEY,      -- central surrogate key
    customer_code       VARCHAR(20) NOT NULL,    -- agreed natural key
    country_code        CHAR(2)  NOT NULL,       -- IT, ES, FR, DE, ...
    tax_id              VARCHAR(20),             -- CF / NIF / SIREN / Steuer-ID
    email_primary       VARCHAR(120),
    party_type          VARCHAR(10),             -- person, company
    first_name          VARCHAR(80),
    last_name           VARCHAR(80),
    legal_name          VARCHAR(120),            -- for legal entities
    birth_year          INT,                     -- NULL for companies
    gender              CHAR(1),                 -- NULL for companies
    region              VARCHAR(40),
    province            VARCHAR(40),
    risk_segment        VARCHAR(20),             -- low, medium, high
    acquisition_channel VARCHAR(30),             -- agency, broker, direct, online
    first_policy_date   DATE,                    -- date of first contract with the group
    status              VARCHAR(10),             -- active, dormant, churned
    valid_from          DATE NOT NULL,
    valid_to            DATE,                    -- SCD Type 2 on region, risk_segment, status
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    record_source       VARCHAR(20),             -- PMS, CRM, ERP, MERGE
    last_update_ts      TIMESTAMP NOT NULL
);

CREATE INDEX ix_dim_customer_natural ON dim_conformed.dim_customer(customer_code, is_current);
CREATE INDEX ix_dim_customer_tax_id  ON dim_conformed.dim_customer(country_code, tax_id) WHERE tax_id IS NOT NULL;
```

Around 3.1 million rows for 1.8 million distinct contract holders across the four main countries (the difference is the version history in {{< glossary term="scd" >}}SCD Type 2{{< /glossary >}}).

**Layer 2 — Bridge between old and new keys.** The three existing data marts kept running with their own local keys. We created a mapping table for each:

```sql
CREATE TABLE dim_conformed.xref_customer (
    source_system   VARCHAR(10) NOT NULL,   -- PMS | CRM | ERP
    country_code    CHAR(2)     NOT NULL,   -- to disambiguate same names across countries
    source_key      VARCHAR(50) NOT NULL,   -- local key in the source system
    sk_customer     BIGINT      NOT NULL,   -- pointer to the conformed dim_customer
    mapping_quality VARCHAR(20),            -- exact_match, fuzzy_match, manual
    mapping_ts      TIMESTAMP   NOT NULL,
    PRIMARY KEY (source_system, country_code, source_key)
);
```

The xref is populated by a nightly job that reads the source masters, compares against the conformed dimension, applies the matching rules and logs the ambiguous cases into an exceptions table handled manually by the data team. Across the four countries, the ambiguous queue sat around 1.5% — a workload two people could clear in a couple of hours a day.

**Layer 3 — Integration views.** On top of the three original {{< glossary term="fact-table" >}}fact tables{{< /glossary >}}, we created views that replace the local key with the conformed surrogate key:

```sql
CREATE OR REPLACE VIEW vw_fact_new_business_conformed AS
SELECT
    f.policy_id,
    xc.sk_customer,           -- conformed key, no longer the local PMS one
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

No department had to stop using its own data mart. Whoever wanted single-department analytics kept doing them on their own. Whoever needed cross-department analytics used the conformed views.

## 📊 The question that used to be impossible

The first truly cross-mart query we ran — the kind that, before the conformed-dimension work, would have come back with three different answers — looked trivial:

```sql
-- Intermediaries reached by a campaign and new policies issued in the next 60 days
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

Before, this query was done by exporting two CSVs, loading them into Excel and running VLOOKUP on the agent/customer code — which was written differently in the two systems (the CRM used the internal broker code, the PMS the RUI code). Matching errors were in the 20-30% range, and no one was measuring them. Country handling added more pain: a broker operating in both Italy and Spain showed up twice.

After, the query runs in about 5 seconds on Oracle Exadata over one quarter of data across the four countries and returns **a single number** per country × risk segment combination. Marketing compares it with finance, finance compares it with commercial, and if there's a discrepancy you go look at the join: not at the concept of customer.

| Metric                              | Before                     | After                         |
|--------------------------------------|----------------------------|-------------------------------|
| Definitions of "contract holder"     | 3                          | 1 (with department-specific attributes) |
| Gaps between department dashboards   | 9-16% depending on the KPI | < 0.5% (only ETL timing)      |
| Time for cross-department analysis   | 1-2 days of Excel          | direct query on views         |
| Cost of full re-platforming          | estimated 18-24 months     | 4 months + ongoing governance |

We never paid the full re-platforming cost because it wasn't necessary. The bus matrix and the conformed dimensions don't replace a refactor: they buy you the time to do one calmly when it's actually needed, one process at a time.

## 🧠 Why the bus matrix has to come before coding

The reason this work has to happen at the start — not after three data marts have grown on their own — is straightforward: conforming after the fact costs ten times more than conforming up front.

When you start from scratch, the conformed dimension is a page-and-a-half document written in a two-hour meeting. When you start from three data marts that have been in production for six years, it's a six-month project with a governance committee, a central data team, a matching process to build, mapping tables to maintain, and organizational locks to negotiate.

Kimball wrote about the bus matrix in the '90s for exactly this reason: to give teams a sheet of paper to put on the wall before opening the SQL editor. It's an alignment exercise, not an architectural one. The architecture comes later, and it comes out much better if the sheet of paper has been done first.

## What I learned

The technical work — `dim_customer`, the xrefs, the views — was the easy part. The hard part was getting three departments to agree on what "customer" means. And that part wasn't solved by me: it was solved by the CFO with his political weight, by the governance committee with six weeks of patience, and by the customer's DBA who had an impressive long memory of every choice made over the previous years and why.

When I see a DWH project starting today without a bus matrix drawn and shared, I raise my hand before we begin. Not to play the wise one — to remind myself that that phase, the one of aligning definitions, can't be skipped. If you skip it, you pay for it later with interest. If you do it, the rest of the project becomes almost boring. Which is exactly how it should be.

------------------------------------------------------------------------

## Glossary

**[Bus Matrix](/en/glossary/bus-matrix/)** — Two-dimensional Kimball matrix with business processes as rows and conformed dimensions as columns. Used to align departments on definitions before starting the physical design of the data warehouse.

**[Conformed Dimension](/en/glossary/conformed-dimension/)** — A shared dimension with the same structure, semantics and key across multiple data marts. Allows summing measures coming from different business processes without ambiguity.

**[Data Mart](/en/glossary/data-mart/)** — A subset of the data warehouse focused on a single business process or functional area (sales, marketing, finance). Can be built independently by a department but risks diverging from the others when dimensional conformity is missing.

**[Kimball](/en/glossary/kimball/)** — Ralph Kimball, methodology for designing data warehouses based on dimensional modeling, star schema and bus matrix. Bottom-up approach starting from business processes and building integrated data marts via conformed dimensions.

**[Star Schema](/en/glossary/star-schema/)** — A data model with a central fact table linked to multiple dimension tables. The base pattern of every Kimball data mart and the natural ground on which conformed dimensions operate.
