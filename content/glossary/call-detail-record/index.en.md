---
title: "Call Detail Record (CDR)"
description: "A record documenting a single phone call: customer ID, timestamp, duration, call type, and cost. The primary operational data unit in telco systems."
translationKey: "glossary_call_detail_record"
aka: "CDR, Call Data Record"
articles:
  - "/posts/data-warehouse/la-demo-che-non-poteva-aspettare-materialized-views-e-un-dwh-telco-sotto"
---

A Call Detail Record (CDR) is the persistent trace a telephony system generates at the end of every call. It captures the minimum information needed to bill the service and analyze traffic: who called, when, for how long, over what type of connection, and at what cost. In telco systems it is the primary operational data unit — the equivalent of a transaction row in a banking system.

## Typical structure

A CDR includes at least the following fields:

| Field | Description |
|---|---|
| `caller_id` | Identifier of the calling customer |
| `callee_id` | Number or identifier of the recipient |
| `start_time` | Call start timestamp |
| `duration_sec` | Duration in seconds |
| `call_type` | Voice, SMS, data, roaming |
| `cost` | Cost calculated at call end |

The exact structure varies across operators and standards (3GPP, IPDR), but these fields are nearly universal.

## Operational context

CDRs accumulate at high velocity: a mid-size operator generates hundreds of GB per month. This makes them a classic use case for telco Data Warehouses, where they are loaded in batch or via streaming and then aggregated for billing, traffic analysis, and fraud detection. Typical analytical queries — total duration per customer, distribution by time slot, month-over-month comparison — benefit from techniques such as Materialized Views to avoid expensive recomputation over tables with billions of rows.

## Volume considerations

A single CDR is only a few bytes, but cardinality is extremely high. Designing the storage schema — date-based partitioning, columnar compression, partial indexes — is critical at modeling time, before query patterns are even finalized.
