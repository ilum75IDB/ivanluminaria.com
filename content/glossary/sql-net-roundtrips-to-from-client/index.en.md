---
title: "SQL*Net roundtrips to/from client"
description: "Oracle session statistic counting network exchanges between client and database. High values indicate a chatty application sensitive to WAN latency."
translationKey: "glossary_sql_net_roundtrips_to_from_client"
aka: "SQL*Net message roundtrips"
articles:
  - "/posts/oracle/latenza-wan-e-change-control-gxp-il-costo-reale-del-lift-and-shift"
---

`SQL*Net roundtrips to/from client` is an Oracle session statistic that counts how many times the client and the database exchange a complete network message during a session. It does not measure bytes transferred — it counts request/response cycles over the SQL*Net channel. Every FETCH, every remote procedure call, every server acknowledgement increments the counter.

## How it works

Oracle exposes the value through `V$SESSTAT` (or `V$MYSTAT` for the current session), joined with `V$STATNAME`:

```sql
SELECT s.value AS roundtrips
FROM   v$mystat s
JOIN   v$statname n ON n.statistic# = s.statistic#
WHERE  n.name = 'SQL*Net roundtrips to/from client';
```

Each request/response cycle between the application layer and the Oracle listener counts as one roundtrip. With a low `arraysize` or row-by-row fetching, roundtrips grow linearly with the number of rows returned. Increasing `arraysize` — or using `BULK COLLECT` on the PL/SQL side — reduces roundtrips by packing more rows into each message.

## Operational context

The statistic becomes critical when the database is reached over a WAN or cloud VPN, where each roundtrip adds tens of milliseconds. An application performing 10,000 roundtrips on a 0.1 ms LAN accumulates roughly 1 second of latency; on a 30 ms WAN the same workload accumulates around 5 minutes. This is the classic unoptimised lift-and-shift profile: the queries are identical, but perceived response time collapses.

The ratio between `SQL*Net roundtrips` and the number of rows processed (or COMMIT operations) is the key indicator. A well-designed application keeps this ratio low through batch fetching, connection pooling, and eliminating unnecessary remote calls.
