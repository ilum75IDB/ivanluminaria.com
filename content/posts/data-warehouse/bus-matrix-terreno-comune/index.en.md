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
