---
categories:
- data-warehouse
date: '2026-07-07'
description: "A lunch conversation about what a technically ready Data Warehouse still lacks: data ownership, quality framework, GDPR, TDE on Oracle 19c."
draft: false
image: data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati.cover.jpg
seoTitle: "DWH Data Governance: quality, ownership, TDE before go-live"
tags:
- data-governance
- data-warehouse
- oracle-19c
- data-quality
- gdpr
title: 'The lunch break that delayed go-live: Data Governance in the DWH'
translationKey: data_governance_nel_data_warehouse_dal_controllo_qualita_alla_conformita_normati
webo_generated_at: 2026-06-14
webo_status: scheduled
---

## The table outside the office

It was one of those late spring days when you finally eat outside. Carlo — senior data analyst at a large Italian insurance group I've been working with for a couple of years — was visibly pleased. The DWH was technically ready: data loaded, the dimensional model was holding up, the first report queries were working. He was already thinking about how to present the success to management the following week.

"I'd say we're ready for go-live," he told me, cutting his pizza.

I waited a second before answering. Not because I wanted to dampen the enthusiasm — the work done was solid — but because that phrase, "we're ready," was hiding a series of questions nobody had yet asked out loud. And the governance gaps that surface after go-live are almost always interpreted by managers as carelessness, not as the inherent complexity of the project.

"Technically, yes," I said. "But have you already answered: who is the data owner of `policy_holder_data`? What happens if a report shows an anomalous premium — who corrects it and in how long? And GDPR — how are we handling it at the storage level?"

Carlo put down his fork.

That conversation lasted through coffee, then continued in front of the PC that afternoon. This article is an attempt to write down what we said to each other.

---

## What a "ready" DWH doesn't include by default

A technically functioning Data Warehouse — ETL running, dimensions populated, facts correctly aggregated — is a necessary but not sufficient condition for going to production in an enterprise context. Especially in regulated sectors like insurance, where data includes customer records, policy history, payments, and — in some products — health data.

The implicit expectations that managers and business users bring into the meeting room on go-live day cover at least four areas that rarely appear in the initial functional requirements.

### Data quality: not a check, a process

Data quality is not a checkbox to tick before going to production. It's a continuous process. In the insurance DWH we were discussing, the `claims_history` and `premium_payments` tables came from source systems with heterogeneous quality: some companies in the group had different codings for the same type of claim, date fields with inconsistent formats, null values in columns that should have been mandatory.

During loading we had already implemented some validation rules in the ETL. But "validating on ingestion" and "guaranteeing quality over time" are two different things. You need:

- **Alert thresholds**: if the number of rejected records in a load exceeds 2%, someone needs to know before the reports are distributed
- **Remediation processes**: who corrects the anomalous data? With what priority? With what audit trail?
- **Longitudinal monitoring**: data that was correct six months ago might no longer be if business rules change

Carlo had handled ingestion validation. Continuous monitoring and remediation processes were still to be defined.

### Ownership: the uncomfortable question

"Who is the data owner of `policy_holder_data`?" I had asked at lunch.

Carlo had answered: "Well, IT."

This answer is almost always wrong — or at least incomplete. IT manages the infrastructure and technical processes, but the data belongs to the business. In an insurance context, the data owner of a table containing customer personal and contractual data should be a business function (e.g., the commercial or compliance directorate), not the technical team.

The distinction between **Data Owner** (business responsibility for the data), **Data Steward** (operational management of quality and rules), and **Data Custodian** (technical management of the infrastructure) is not bureaucracy. It's the practical answer to the question "who do I call when this data is wrong?" Without this map, every anomaly becomes a three-hour meeting to figure out whose problem it is.

### Data glossary: when "premium" doesn't mean the same thing to everyone

In the insurance group, the term "premium" had at least three different operational definitions depending on the business unit. The DWH had consolidated them into a single `premium_amount` column in the `premium_payments` table, but without documenting which definition had been adopted and why.

A shared data glossary — even in its simplest form, a versioned document with definitions agreed between business and IT — is the difference between a report that generates trust and one that generates arguments. You don't need an enterprise tool costing hundreds of thousands of euros: you need a written definition, agreed upon, accessible.

### Data lineage: the traceability that saves audits

"If a risk management analyst asks where this number comes from," I said to Carlo, opening the laptop, "can you answer in under an hour?"

Silence.

Data lineage — the ability to trace the path of a piece of data from the source to the final report, through all the transformation steps — is essential in two scenarios: day-to-day troubleshooting ("why did this value change compared to last month?") and regulatory audits ("prove to me that this aggregate is calculated correctly according to rules X"). In a sector like insurance, the second scenario is not hypothetical.

---

## GDPR: from legal constraint to architectural choice

Up to this point in the conversation, Carlo was nodding with the air of someone who recognizes the gaps but sees them as "things to add later." The turning point came with GDPR.

"We handle GDPR with the privacy policy and consent," Carlo said. "Legal compliance is already covered."

"The documentary compliance, yes," I replied. "But GDPR Article 32 explicitly talks about appropriate technical measures, including encryption. If someone physically accesses the database files — a stolen backup, a poorly decommissioned disk, unauthorized access to storage — is the data in `policy_holder_data` readable in plain text?"

This is the difference between formal compliance and architectural implementation. The former protects the organization legally as long as nothing happens. The latter reduces the probability that something happens, and reduces the impact if it does.

### Transparent Data Encryption on Oracle 19c

Oracle Database 19c includes Transparent Data Encryption (TDE) [1], a feature that encrypts data at rest — data files, redo log files, backups — without requiring changes to applications. For the insurance DWH, this means that even if someone gains physical access to the files on `oracle-dwh-prod-eu-01`, the data remains unreadable without the encryption key managed by the Oracle wallet.

Enabling TDE at the tablespace level is relatively straightforward:

```sql
-- Wallet creation and master key setup (run as SYSDBA)
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE '/opt/oracle/wallet' IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEYSTORE OPEN IDENTIFIED BY "wallet_password";
ADMINISTER KEY MANAGEMENT SET KEY IDENTIFIED BY "wallet_password" WITH BACKUP;

-- Encrypt the tablespace containing sensitive data
ALTER TABLESPACE policy_data ENCRYPTION ONLINE USING 'AES256' ENCRYPT;
```

```sql
-- Verify encryption status of tablespaces
SELECT tablespace_name, encrypted
FROM dba_tablespaces
WHERE encrypted = 'YES';
```

What TDE does not do: it does not protect against a user with legitimate SQL access to the database. It is not a substitute for access management and privilege control. It is a specific protection layer for data at rest — exactly what GDPR considers an "appropriate technical measure" in the context of protection against unauthorized physical access or loss of storage media [2].

The conversation with Carlo shifted to a practical point: implementing TDE before go-live is a plannable operation with controlled downtime. Implementing it afterward, on a production system with terabytes of historical data already loaded, is a more complex and risky operation. The window of opportunity was right then.

---

## A quality framework that holds over time

Getting back to data quality: what we had in place was a series of checks in the ETL. What was needed was a framework.

The difference is substantial. ETL checks block or flag non-conforming records at load time. A quality framework adds:

**Proactive monitoring**: scheduled jobs that periodically verify quality conditions on already-loaded tables. For example, a query that checks every morning whether `policy_holder_data` records exist with a null `fiscal_code` or an invalid format — data that might have entered through non-standard loading paths.

```sql
-- Example of scheduled quality check on policy_holder_data
SELECT
    COUNT(*) AS fiscal_code_anomalies,
    SYSDATE AS check_date
FROM policy_holder_data
WHERE fiscal_code IS NULL
   OR NOT REGEXP_LIKE(fiscal_code, '^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$');
```

**Thresholds and notifications**: if the anomaly count exceeds a defined threshold (e.g., more than 50 records with an invalid fiscal code in a day), the system notifies the responsible Data Steward before reports are distributed.

**Remediation trail**: every manual correction to the data must be documented — who corrected it, when, why, what the original value was. In an insurance context, this trail is relevant both for internal audits and for any regulatory inspections.

---

## The Data Catalog: where governance becomes navigable

A Data Catalog [3] is the infrastructure that makes everything we've discussed so far navigable. It's not an optional tool for large teams: it's the difference between governance that exists only in documents and governance that business users can actually use.

In the insurance DWH context, a minimal Data Catalog should answer these questions without requiring a phone call to the technical team:

- What does the `claims_history` table contain? Which columns? With what business rules?
- Where does the data in `premium_payments` come from? Through what transformations?
- Who is the data owner of `policy_holder_data`? Who do I contact if I find an anomaly?
- Which tables contain personal data subject to GDPR?

Enterprise tools like Apache Atlas, Collibra, or Alation handle this in a structured way. For a first go-live, even a lighter solution — a structured wiki, a shared spreadsheet with agreed definitions — is infinitely better than nothing. The important thing is that it exists, that it's kept up to date, and that users know where to find it.

Integration with the data glossary is natural: agreed definitions (e.g., the definition of "premium" adopted in the DWH) live in the catalog and are referenced by column documentation. Lineage, ideally, is viewable from the same tool.

---

## Who does what: the three roles you can't ignore

Before wrapping up the conversation with Carlo, we wrote down a role map. Not as a formal exercise, but as a practical answer to the question: when something goes wrong, who do I call?

**Data Owner**: a business figure, not a technical one. Decides the rules for data usage, approves changes to definitions, is responsible for quality from the business perspective. For `policy_holder_data`, the natural Data Owner was the group's compliance directorate.

**Data Steward**: the bridge between business and IT. Operationally manages quality rules, monitors anomalies, coordinates remediation. Can be a technical figure with strong business awareness, or vice versa. In our case, Carlo was the natural candidate for this role on some of the key tables.

**Data Custodian**: the technical team. Manages the infrastructure, implements the technical rules defined by the Data Owner and Data Steward, guarantees availability and security. Responsibility for TDE, backups, database access — all of this is the Data Custodian's scope.

The distinction is not bureaucracy. It's the operational answer to the question "who is responsible for what." Without this map, every problem becomes a discussion about who should solve the problem, instead of a discussion about how to solve it.

---

## "Now I know what's missing"

Around five in the afternoon, Carlo stood up from his chair and said something that stuck with me: "Okay. Now I know what's missing. And I know how to present it to management without looking like we did half a job."

That's the difference between arriving at a go-live meeting with the gaps hidden and arriving with the gaps mapped and a plan to close them. Managers don't expect perfection — they expect the team to know where it stands and where it's going.

We pushed the go-live back three weeks. In that time: we defined the Data Owners for the main tables, implemented TDE on the tablespace containing personal data, wrote a minimal data glossary for the critical terms, set up the first scheduled quality checks, and sketched out the Data Catalog structure.

It wasn't everything. But it was enough to walk into the management meeting with the right answers to the right questions. The credit wasn't down to a single insight — it came from a frank conversation between two people with different perspectives working toward the same goal.

---

## Official sources

1. Oracle Database Security Guide 19c — [Configuring Transparent Data Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-transparent-data-encryption.html)
2. Regulation (EU) 2016/679 — [Article 32: Security of processing](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679)
3. DAMA International — [DAMA-DMBOK2: Data Management Body of Knowledge](https://www.dama.org/dama-dm-bok-2) — covers Data Governance, Data Quality, Data Lineage, Data Catalog, Data Stewardship

---

## Glossary candidate

- **Data Governance** — The set of processes, policies, standards, and metrics that ensure effective use of information, guaranteeing its quality, integrity, security, and regulatory compliance. It is not a project with an end date: it is a continuous operational framework.

- **Data Lineage** — The ability to trace the path of a piece of data from its source through all systems and transformations to its final destination. Essential for troubleshooting, regulatory audits, and verifying the correctness of calculations.

- **Transparent Data Encryption (TDE)** (Oracle) — An Oracle Database feature that encrypts data at rest — data files, redo logs, backups — without application changes. Protects against unauthorized physical access to storage media.

- **Data Quality** — The degree to which data is accurate, complete, consistent, valid, and timely. Not a one-time check but a continuous process of monitoring, alerting, and remediation that guarantees the reliability of analyses over time.

- **Data Catalog** — An organized inventory of all data available in an organization, with metadata, glossary, lineage, and search tools. Makes governance navigable by business users without requiring technical intervention for every question about the data.
