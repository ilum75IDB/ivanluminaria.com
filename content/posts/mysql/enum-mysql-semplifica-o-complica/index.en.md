---
title: "ENUM in MySQL: when it makes your day, and when it ruins your week"
seoTitle: "MySQL ENUM vs CHECK vs lookup: the three roads"
description: "MySQL ENUM vs CHECK constraint vs lookup table: three ways to model an enumeration. Pros, cons and real case of a shipment tracking system."
date: "2026-06-03T08:03:00+01:00"
draft: false
translationKey: "enum_mysql_semplifica_o_complica"
tags: ["enum", "data-modeling", "schema-design", "alter-table", "check-constraint"]
categories: ["mysql"]
image: "enum-mysql-semplifica-o-complica.cover.jpg"
---

There's a scene that plays out in every project, sooner or later. You're designing a new table, you need to model a `status` or `type` or `category` column, and the question always comes up the same way: "Native ENUM, CHECK constraint, or lookup table?". Three roads, three philosophies, and three very different outcomes depending on how the system evolves.

ENUM is one of those features that characterise MySQL. Few other mainstream DBMSes have a native enumerated type — PostgreSQL has one, and Oracle only got to something similar with the SQL Domains in 23ai. For years, in MySQL, choosing ENUM was practically automatic: a few lines of DDL, readable, fast, no JOIN. It works. Until you turn around six years later and realise that `status` column has become a minefield.

---

## The three roads, in two lines each

Before getting to the point, here are the three options sketched out. We'll use an `orders` table example with a status that takes a closed set of values.

**Native ENUM**:

```sql
CREATE TABLE orders (
  id     INT PRIMARY KEY,
  status ENUM('NEW','IN_PROGRESS','SHIPPED','DELIVERED') NOT NULL
);
```

The `ENUM` type is a string with a constraint: only the declared values are allowed. Internally MySQL stores an integer (1 or 2 bytes, depending on how many values) acting as an index into the list. Result: compact storage, readable queries.

**CHECK constraint**:

```sql
CREATE TABLE orders (
  id     INT PRIMARY KEY,
  status VARCHAR(20) NOT NULL,
  CONSTRAINT chk_status CHECK (status IN ('NEW','IN_PROGRESS','SHIPPED','DELIVERED'))
);
```

The SQL-standard approach. More verbose but more flexible (CHECK conditions can be arbitrarily complex). Heads up: before MySQL 8.0.16, CHECK constraints were parsed and silently ignored. They've only been actually enforced since 8.0.16.

**Lookup table with FK**:

```sql
CREATE TABLE order_statuses (
  code        VARCHAR(20) PRIMARY KEY,
  label       VARCHAR(100) NOT NULL,
  active      BOOLEAN DEFAULT TRUE
);

CREATE TABLE orders (
  id           INT PRIMARY KEY,
  status_code  VARCHAR(20) NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_code) REFERENCES order_statuses(code)
);
```

The "pure-database" way. More tables, more JOINs, but also more flexibility: you can add attributes (localised labels, display order, active/inactive flags), modify values without touching child schemas, and manage everything at runtime.

---

## When ENUM is the right call

ENUM shines in a specific context: **stable set of values, semantics controlled at schema level**. When both ingredients are there, ENUM is the cleanest choice.

Typical cases where stability is real:

- **Days of the week** (`'MON','TUE','WED','THU','FRI','SAT','SUN'`) — they've never changed and they're not going to
- **Fixed binary or ternary states** (`'ACTIVE','INACTIVE'` or `'PUBLIC','PRIVATE','DRAFT'`)
- **Accounting transaction types** where the chart of accounts is regulated by law
- **Polarity or sign** in technical measurements

In all these cases ENUM gives you three concrete advantages:

1. **Compact storage**: 1-2 bytes per row instead of the 4 of an INT FK. On a table with 200 million rows that's 400-600 MB saved. Not the main reason to choose ENUM, but a bonus
2. **Readable queries**: `WHERE status = 'SHIPPED'` with no JOIN, no extra table aliases. When you're debugging at three in the morning, that matters
3. **No extra migration**: the "lookup table" is the schema itself. No data seed, no synchronisation, no FK to manage at deploy time

In a system where the domain is genuinely closed, ENUM removes complexity. One column, one constraint declared in the CREATE TABLE, done.

---

## The real case: a shipment tracking system

A while back I was working with the IT team of a major Italian postal operator. The job was to design the data model for a shipment tracking system: parcels coming into warehouses, getting picked up, sorted, delivered. The `status` was a central column, present in pretty much every query.

In the first version of the system, the statuses were five, clearly defined by the business: `RECEIVED`, `IN_WAREHOUSE`, `IN_DELIVERY`, `DELIVERED`, `REFUSED`. ENUM, hand on heart, was the right call:

```sql
ALTER TABLE shipments
  ADD COLUMN status ENUM('RECEIVED','IN_WAREHOUSE','IN_DELIVERY','DELIVERED','REFUSED') 
  NOT NULL DEFAULT 'RECEIVED';
```

It ran silently for two years in production. No JOINs in delivery dashboards, no seed tables of statuses to maintain, every query with `WHERE status = '...'` read like a line of plain prose. The DBA slept well.

Then the problems started.

---

## The limits, told honestly

The first signal came in as an email from the product manager: we need to add a `BOOKED` status, to handle shipments that the customer has announced but not yet delivered to the warehouse. Apparently trivial. Trivial operation that requires this:

```sql
ALTER TABLE shipments
  MODIFY COLUMN status 
  ENUM('BOOKED','RECEIVED','IN_WAREHOUSE','IN_DELIVERY','DELIVERED','REFUSED') 
  NOT NULL DEFAULT 'RECEIVED';
```

Looks like one line. But if you want to add `BOOKED` **before** `RECEIVED` (for semantic coherence in the sequence), MySQL has to rewrite the whole table. All of it. On `shipments` at one hundred fifty million rows, in production, with Online DDL configured properly, you still get hours of extra load on storage and replication lag. Simply tacking it on at the end with `MODIFY COLUMN status ENUM(...,'BOOKED')` would have been lighter — but it would have produced a value set with an absurd positional ordering: `DELIVERED` "comes before" `BOOKED` in the sort? Technically yes.

There they are, the limits of ENUM, told without pity:

**Case-insensitive**. `'ACTIVE'` and `'active'` are the same value. For someone coming from PostgreSQL this can be a nasty surprise. In MySQL it's an explicit design choice, but it's worth knowing up front.

**Ordering by declaration position**, not alphabetical. If a query does `ORDER BY status`, the order is the one in which you declared the values in the `CREATE TABLE`. Subtle bug: you add `'BOOKED'` at the end to avoid rebuilding the table, and suddenly your report sorted by status shows `'BOOKED'` after `'REFUSED'`. Nobody complains until somebody notices.

**Heavy changes on large tables**. Appending a value at the end is light. Changing position, renaming, removing — all require a rebuild. With Online DDL on MySQL 8 it's less painful than before, but it's not free.

**Table locks in certain scenarios**. The combinations of operations that require `ALGORITHM=COPY` still exist, and on critical tables they need to be evaluated carefully.

In the tracking system, six years on, twelve more statuses had been added. Every new one — because of a new courier, a new channel, a new return policy — was a midnight `ALTER` with the DBA standing in front of the monitor. ENUM had gone from making life easier to making it harder.

---

## When to move to CHECK or to lookup

So the question becomes: at what point is it worth dropping ENUM and taking another road?

Three red flags:

1. **Values change often**: if every quarter the business asks to add, rename or disable a value, the schema shouldn't be the "table" of enumerations. A real lookup table managed from an admin panel is the way
2. **You need extra attributes**: localised description in four languages, short label vs long, display order, active/inactive flag. None of this fits in ENUM. With a lookup table, every value is a row that can have as many columns as you like
3. **Many tens of values, growing**: past 20-30 values, ENUM becomes hard to read and to maintain in the `CREATE TABLE`. The `DDL` turns into an endless list

In these cases `CHECK` constraint is an intermediate compromise: more flexible than ENUM (renaming a value is just an `ALTER CONSTRAINT`), less structured than a real lookup table. Fine for sets of 5-15 values that get touched occasionally, but without the need for extra attributes.

In the tracking shipments case, the rewrite ended up going the lookup table direction. Worth saying: not because ENUM was "wrong" in version 1. It was right, six years earlier, for a domain that was genuinely small and stable. It became wrong when the domain changed, and nobody had foreseen it. Which is exactly what happens in many real projects.

---

## Lookup table done right

If you decide to go the lookup route, it's worth designing it in a way that lets you grow over time. The natural pattern — the one you see in mature systems — separates two roles that ENUM kept mixed: the **identifier** of the value and the **description** of the value.

```sql
CREATE TABLE shipment_statuses (
  id            SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  code          ENUM('RECEIVED','IN_WAREHOUSE','IN_DELIVERY','DELIVERED','REFUSED') NOT NULL UNIQUE,
  description   VARCHAR(200) NOT NULL,
  display_order SMALLINT NOT NULL DEFAULT 0,
  active        BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO shipment_statuses (code, description, display_order) VALUES
  ('RECEIVED',     'Shipment received at warehouse',     10),
  ('IN_WAREHOUSE', 'Awaiting sorting',                   20),
  ('IN_DELIVERY',  'Handed off to courier',              30),
  ('DELIVERED',    'Delivered to recipient',             40),
  ('REFUSED',      'Refused by recipient',               50);

CREATE TABLE shipments (
  id         INT PRIMARY KEY,
  status_id  SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES shipment_statuses(id)
);
```

Did you catch the surprise? In the lookup, the `code` field is still an **`ENUM`**. Not a `VARCHAR(20)`, not a free string. ENUM, the same one we've just finished criticising. And it's exactly the right choice: all the cons we saw earlier — the rebuild on change, positional ordering, the impact on large tables — here simply *don't hurt*. The lookup has 5, 20, at most 50 rows. A rebuild on 50 rows is the blink of an eye. The "only these values allowed" constraint costs us nothing, with no separate `CHECK` to write.

Three interesting things emerge from this schema.

**The master only carries the id**, not the code. Two bytes per row (`SMALLINT`) versus 20+ for a `VARCHAR(20)`. On a table with 150 million rows that's 2-3 GB difference between data and indexes, plus faster JOINs thanks to integer comparison.

**Code and description are attributes of the lookup, not the key**. Renaming a status — going from "Delivered" to "Delivered to recipient" — is an `UPDATE` on one row of the lookup. No migration, no rebuild, no `ALTER` on the master. Child schemas are not touched. Having the `code` as a natural key seemed elegant four years ago, but the first time the business asks to change a label's text you understand why surrogate ids existed.

**Extra attributes cost nothing to add**: a `short_description` column for SMS notifications, a `display_order` column for visual sorting in dashboards, a linked table for multilingual translations. All this was impossible with pure ENUM, and it's normal with a well-designed lookup table.

The price you pay is that ad-hoc queries need a JOIN to read the status name in plain text:

```sql
SELECT s.id, ss.code
FROM shipments s
JOIN shipment_statuses ss ON ss.id = s.status_id
WHERE ss.code = 'IN_DELIVERY';
```

More verbose than a `WHERE status = 'IN_DELIVERY'` on ENUM, but that's the price of flexibility. And on the most frequent reports the JOIN is optimised with a composite index and a `view` that wraps the complexity, leaving application queries clean.

### Adding a value and reordering the ENUM

Let's see how the two "delicate" operations work on this pattern. The business asks to add a `BOOKED` status, for shipments announced but not yet received.

**Case 1 — append to the end of the ENUM, with logical `display_order` controlled by the column**:

```sql
-- Extend the ENUM by adding the value at the end (fast operation)
ALTER TABLE shipment_statuses
  MODIFY COLUMN code 
    ENUM('RECEIVED','IN_WAREHOUSE','IN_DELIVERY','DELIVERED','REFUSED','BOOKED') NOT NULL;

-- Insert the new row; logical order is 5 (before RECEIVED=10)
INSERT INTO shipment_statuses (code, description, display_order, active) VALUES
  ('BOOKED', 'Shipment announced, not yet received', 5, TRUE);
```

Notice the separation of responsibilities: the **declaration order of the ENUM** doesn't necessarily correspond to the **logical order** of the status in the workflow. The latter is handled by the `display_order` column, which is explicit and sortable as we wish. The internal numeric value of the ENUM is an implementation detail we ignore.

**Case 2 — actually reordering the ENUM** (if we really want `BOOKED` to be first internally too):

```sql
ALTER TABLE shipment_statuses
  MODIFY COLUMN code 
    ENUM('BOOKED','RECEIVED','IN_WAREHOUSE','IN_DELIVERY','DELIVERED','REFUSED') NOT NULL;
```

On a 6-row table, MySQL rebuilds in milliseconds. Existing row `id`s stay identical (the AUTO_INCREMENT sequence isn't touched by the rebuild), the ENUM value gets remapped internally by the engine, and referential integrity from the master `shipments` stays intact. The master knows none of this: it keeps containing `status_id = 3` and through the FK still resolves to the right row in the lookup.

This is the real point: **the stable lookup ids are the anchor of referential integrity**. Whatever we change in the lookup — ENUM reorder, code rename, description edit — the master keeps working. The 150 million rows never get touched.

ENUM, in this place, is back to being the right tool. The same tool that was a problem on the master is an advantage on the lookup. Change the context, change the verdict.

---

## The golden rule

The takeaway I bring away from this story, and that I repeat to teams when the "ENUM or lookup?" question comes up, is simple:

> If the values will never change, ENUM is the right call. If they will change — even just "every now and then" — don't tie the vocabulary to the schema.

That's all. The hard part isn't picking among the three roads. The hard part is honestly figuring out, at decision time, which of the two worlds you're in. And usually you only get that by looking at how the domain has changed in the last two or three years — not by reading the requirements of the next sprint.

---

## The cross-DB mini-series

This is the first of four articles on enumerations across different DBMSes. The "ENUM or lookup?" question isn't only a MySQL thing — every database has its own philosophy, and it's interesting to see how the same choice changes shape moving from one world to another.

Up next:

- **PostgreSQL** — `CREATE TYPE ... AS ENUM`, `ALTER TYPE ADD VALUE`, and the surprise: in PostgreSQL ENUM is *case-sensitive*
- **Oracle** — `CHECK` constraint, the SQL Domains from 23ai, and why Oracle got to this topic "late"
- **Oracle, vertical deep-dive** — how enumerations were modelled in 19c, what changed in 21c, 23ai, and 26ai, all the way to the new Assertions

Same question, three philosophies. The best part is in the comparison.

------------------------------------------------------------------------

## Glossary

**[ENUM (MySQL)](/en/glossary/mysql-enum/)** — MySQL data type that allows a predefined set of string values, stored internally as a 1-2 byte numeric index. One of MySQL's characteristic features.

**[CHECK constraint](/en/glossary/check-constraint/)** — Standard SQL constraint that restricts the values allowed in a column via a boolean expression. In MySQL it's only really enforced from version 8.0.16.

**[Lookup table](/en/glossary/lookup-table/)** — Reference table linked via foreign key that stores the valid values of an enumeration, with any descriptive attributes (label, order, active flag).

**[Online DDL](/en/glossary/mysql-online-ddl/)** — MySQL/InnoDB mechanism that allows ALTER TABLE without blocking concurrent writes, with three algorithms (`INSTANT`, `INPLACE`, `COPY`) chosen automatically based on the operation.

**[Surrogate key](/en/glossary/chiave-surrogata/)** — Numeric identifier generated by the database (typically an `AUTO_INCREMENT`) distinct from the natural key. On the lookup table it's the anchor of referential integrity, because it stays stable even when code or description change.
