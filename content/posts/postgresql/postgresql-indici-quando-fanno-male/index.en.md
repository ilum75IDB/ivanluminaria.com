---
title: "When an index does more harm than good: cleaning PostgreSQL waste"
description: "A Ministry's central database, a table with 15 indexes (8 of them never used), a junior who wanted to understand everything. The cleanup that put the queries back on track, told as if it happened yesterday."
date: "2026-05-26T08:03:00+01:00"
draft: false
translationKey: "postgresql_indici_quando_fanno_male"
tags: ["indexes", "b-tree", "gin", "gist", "performance", "tuning", "query-tuning"]
categories: ["postgresql"]
image: "postgresql-indici-quando-fanno-male.cover.jpg"
---

The other day a colleague pinged me: "I've got a table with twelve indexes, it's painfully slow. I don't get it." I sent him a couple of lines back, but while rereading what I'd written, Marco came to mind. It was a few years ago. I was working on the central database of a Ministry — doesn't matter which one, the pattern shows up everywhere. And Marco was the junior they'd assigned to me.

He had two and a half years of PostgreSQL behind him, he could write decent queries, he knew `EXPLAIN`. But more importantly he had the one quality that, in this job, takes you far: he asked. Not out of laziness — out of wanting to know. He'd rephrase concepts out loud to make them stick, took notes, anticipated the next question with things like "wait, so if I do X I should expect Y, right?". The kind of junior every senior wishes they had next to them when a scary table opens on screen.

That day we opened one.

## The scary table

It was called `cittadini_servizi` (`citizens_services`). Not the real name — but the pattern is real.

Eighty million rows. A `cittadino_id` column, a `servizi_attivi` column that was an array of codes (a citizen could have multiple active services: civil registry, tax, healthcare, education, each with its numeric code), a geometry with the residence, an `attivo` boolean, a couple of dates, some metadata. Nothing exotic.

On top of it sat **fifteen indexes**.

Marco counted them slowly, scrolling through `\d cittadini_servizi`. "Fifteen. Bit much, isn't it?"

"Depends. Are they used?"

"How would I even know?"

And that's where it began.

## The five-minute diagnosis

PostgreSQL keeps track of how many times each index has actually been used. The view is called `pg_stat_user_indexes`. Marco had never opened it.

```sql
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'cittadini_servizi'
ORDER BY idx_scan ASC;
```

The output was brutal. Eight indexes with `idx_scan = 0`. Never — used — even — once.

Marco stared at the screen. "Never? Not even by accident?"

"Never. `idx_scan` starts from zero when the database boots and grows every time the planner picks that index. If it's still at zero after weeks of production, the planner has never considered it useful."

"So we drop them and move on."

"Hold on. First we need to understand why they're there."

That sentence right there — don't delete anything before you've understood why it exists — is the golden rule when you land on a system you didn't build. Those `CREATE INDEX` were written by someone. Maybe they had a reason. Maybe they thought they did. Maybe they didn't, period. Who knows.

Marco nodded and opened the git log of the DDL repo.

## "But if there are already 15 indexes, why is it slow?"

Right question. Wrong premise.

Because it starts from the assumption that "more indexes = faster", which is one of the most stubborn myths from the early years of PostgreSQL. The reality is that an index is only useful if the planner picks it, and the planner only picks indexes that are the **right type** for the query it's evaluating.

I opened one of the critical queries, one of those the monitoring kept flagging as slow:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT cittadino_id
FROM cittadini_servizi
WHERE servizi_attivi && ARRAY[42, 71]
  AND attivo = true;
```

The `&&` operator means "array overlap": find me all citizens who have at least one of services 42 or 71 active. A query the business asked for often, for targeted campaigns.

Time: **8.4 seconds**. Plan: `Seq Scan on cittadini_servizi`. Filter: all 80 million rows.

"But there is an index on `servizi_attivi`!"

"There is! It's a B-tree. The B-tree doesn't know what to do with `&&`."

## When B-tree is enough — and when it's not

The **B-tree** is the index 90% of developers know and use. It's a balanced tree that orders values. Works great for equality (`WHERE col = 'x'`), for ranges (`WHERE col BETWEEN ... AND ...`), for sorting (`ORDER BY col`), for `LIKE` with a prefix (`WHERE col LIKE 'ABC%'`).

What it doesn't work for:
- Array operators (`&&`, `<@`, `@>`)
- Substring search (`LIKE '%x%'`)
- JSONB containment (`@>`)
- Geometric ranges (`&&` on geometries, distances, bounding boxes)

For those you need other types.

"And we've got the array of services under a B-tree."

"Exactly. It's like having a paper filing system sorted by tax code and then asking the archivist to find every folder containing a particular keyword inside. The ordering doesn't help."

"So we need a different index type."

"We need GIN."

## GIN: the inverse of B-tree

GIN stands for *Generalized Inverted Index*. Inverse, because instead of indexing rows by the column's value, it indexes every element inside the column and keeps a list of rows that contain it.

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi);
```

`USING GIN` is the key. PostgreSQL builds a mapping: for each service code, a list of rows that contain it in the array. When the query with `&&` arrives, the index intersects the lists of the two values being searched and returns the union. No more seq scan.

Same query, after:

```
Bitmap Index Scan on idx_cittadini_servizi_attivi_gin
  ...
Execution Time: 240 ms
```

From 8400 to 240 milliseconds. A factor of 35.

Marco fist-pumped quietly. Then: "But if it's that powerful, why not use it always?"

"Because on writes it costs you. Every `INSERT` or `UPDATE` on that column has to update every posting where that value appears. It's the price of finding things fast — and high-churn tables pay that price dearly."

"So GIN yes, but only on tables that are mostly read."

"Exactly. Our `cittadini_servizi` got nightly loads and then read-only traffic all day. Ideal case."

## GiST: for when data has a shape

The other critical query was on the geometries. The Ministry ran territorial analyses: "find me all citizens with a residence within 5 km of point X, in the province of Y, active". A query like that, with a fake spatial B-tree (because someone had put one there, but it wasn't usable on that column), ran as a nested loop and took half a minute.

GiST — *Generalized Search Tree* — is the index family that handles data with geometry, ranges, similarity. It doesn't sort values linearly, because some data isn't linearly sortable (a point on a plane doesn't come "before" or "after" another). It indexes by hierarchical *bounding boxes* instead.

"But wait, why not a composite B-tree on `(latitude, longitude)`?"

Good question. Marco had hit on the right point.

"Because the composite B-tree sorts first by latitude and then by longitude. If you need to find points inside a box `(lat1, lon1, lat2, lon2)`, the index can use the latitude constraint — but then for every row that passes the lat filter it also has to check lon. On 80 million rows that becomes a half-scan."

"And GiST?"

"GiST organises points by geographic regions. When you search for a box, it discards entire regions with a bounding-box comparison. It's built for that kind of query."

```sql
CREATE INDEX idx_cittadini_residenza_gist
ON cittadini_servizi USING GIST (residenza);
```

Same query "find everyone within 5 km of X", from 28 seconds to 380 ms.

Marco was taking quick notes. "So: B-tree for sorting and equality, GIN for array and JSONB containment, GiST for geometry and ranges. Anything else?"

"For now that's enough. There's BRIN, SP-GiST, hash too, but those are more niche. When you'll need them, you'll remember."

## Bonus: partial indexes

There was one last thing before getting back to the original question (which indexes to drop). The "active" citizens were about 35% of the total. Everything else was historical, closed cases, archived. The operational queries always filtered on `attivo = true`.

"So every index contains 65% of rows that are never searched."

"Exactly. Wasted space, wasted VACUUM work. Solution: partial index."

```sql
CREATE INDEX idx_cittadini_servizi_attivi_gin
ON cittadini_servizi USING GIN (servizi_attivi)
WHERE attivo = true;
```

That `WHERE` changes everything. The index only contains active rows. On the real data, the disk space halved and queries got another 15-20% faster because the index was smaller to walk.

"And the queries with `attivo = false`?"

"They go to seq scan, but that happens once a week for the archive reports. There the seq scan does just fine."

## The cleanup

At this point we'd:

- Figured out why 8 indexes weren't used (they were duplicates of others, or B-trees on columns where the planner preferred a seq scan, or leftovers from queries that no longer existed)
- Replaced 2 inadequate B-trees with one GIN and one GiST
- Turned 2 "full" indexes into partial indexes

Net result:

| Item | Before | After |
|------|-------:|------:|
| Total indexes | 15 | 7 |
| Index disk space | 42 GB | 18 GB |
| Average operational query time | 4.1 s | 0.4 s |
| Nightly INSERT batch time | 38 min | 22 min |

Marco looked at the table, then at me. "So we improved both reads and writes, simply by removing things."

"And by putting the right three in the right place. But yes, mostly removing. Every index is a cost. On every DML. Forever."

## The line I told him three times

That day I told him the same thing in three different ways, because I wanted him to take it away with him:

> When you think about creating an index on a table, don't think "let's put one more, it can't hurt". An index is a permanent cost on every `INSERT`, `UPDATE`, `DELETE` — more disk, more WAL, more VACUUM, more contention. You create it only if it's really needed. And if it's there and isn't, it goes.

Marco wrote it in his notebook. Years later he became the senior on another project. A message reached me one day: *"I've got a table with twenty-two indexes here. Eight at zero. Did the cleanup. Thought of you."*

That's the best thing a junior can ever say to you.

------------------------------------------------------------------------

## Glossary

**[B-tree](/en/glossary/b-tree/)** — The balanced-tree structure used for most indexes. Works great for equality, ranges and sorting. Doesn't handle arrays, internal substrings, geometries.

**[GIN Index](/en/glossary/gin-index/)** — *Generalized Inverted Index*. Indexes individual elements inside composite values (arrays, JSONB, full-text). Fast on read for containment queries, slow on write for high-churn tables.

**[GiST Index](/en/glossary/gist-index/)** — *Generalized Search Tree*. Indexes data with geometric or range structure using hierarchical bounding boxes. Indispensable for geometries, time ranges, similarity.

**[pg_stat_user_indexes](/en/glossary/pg-stat-user-indexes/)** — PostgreSQL system view that tracks how many times each index has been used (`idx_scan`). The primary tool for identifying useless indexes in production.

**[Partial Index](/en/glossary/indice-parziale/)** — An index that covers only a subset of the table's rows, defined with `WHERE` in the `CREATE INDEX`. Reduces space and maintenance time when queries systematically filter on a condition.
