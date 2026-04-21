---
title: "Before upgrading MySQL: the numbers the customer actually asks for — and how to find them"
description: "Four MySQL 8.0 production servers, an infrastructure lead planning the maintenance window, and four direct questions: how big are they, how fast do they grow, how long does a full backup take, how long does a full restore take. How to answer with measured numbers instead of eyeballed estimates."
date: "2026-05-05T08:03:00+01:00"
draft: false
translationKey: "mysql_pre_upgrade_assessment"
tags: ["mysql", "upgrade", "backup", "restore", "assessment", "information-schema", "mysqldump", "mydumper", "xtrabackup"]
categories: ["MySQL"]
image: "mysql-pre-upgrade-assessment.cover.jpg"
---

The email from the infrastructure lead landed on a Monday morning, three dry lines. *"Hi, by Friday I need four numbers to plan the maintenance window on the MySQLs: how big are they today, how fast do they grow per month, how long does a full backup take, how long do we need to rebuild them from scratch if something goes wrong. Thanks."*

Classic scenario in an IT unit of an Italian Public Administration. Four MySQL 8.0 servers backing internal applications and a user portal, versions slightly out of sync (8.0.32, 8.0.33, 8.0.34) because they've been patched at different times. Planned infrastructure upgrade: new hosts, updated operating system, same MySQL major version, with a six-hour night maintenance window.

The PM didn't want an academic assessment. He wanted four real numbers to put in the rollback plan. And the temptation, when you're in a hurry, is to answer off the top of your head: *"They're around 300 GB, backup takes a couple of hours, restore maybe three."* Plausible numbers, maybe even correct — but not measured, and if you miss the restore estimate by a factor of two, the window isn't enough and the cutover fails.

I took half a day. Here's the method I used.

## 📏 1. How big they really are — `information_schema`

The first number is the simplest to find and the trickiest to interpret. In MySQL 8.0 the {{< glossary term="information-schema" >}}`information_schema`{{< /glossary >}} exposes everything you need, but you have to know what to ask.

```sql
-- Total size per schema (data + indexes)
SELECT
    table_schema                            AS schema_name,
    ROUND(SUM(data_length)  / 1024 / 1024 / 1024, 2) AS data_gb,
    ROUND(SUM(index_length) / 1024 / 1024 / 1024, 2) AS index_gb,
    ROUND(SUM(data_length + index_length) / 1024 / 1024 / 1024, 2) AS total_gb,
    COUNT(*)                                AS num_tables
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema')
GROUP BY table_schema
ORDER BY total_gb DESC;
```

Typical output on one of the four servers:

| schema_name           | data_gb | index_gb | total_gb | num_tables |
|-----------------------|--------:|---------:|---------:|-----------:|
| user_portal           |   58.34 |    21.07 |    79.41 |        142 |
| case_management       |   31.12 |    14.88 |    46.00 |         97 |
| audit_log             |   28.45 |     9.20 |    37.65 |         12 |
| shared_master         |    4.18 |     1.32 |     5.50 |         24 |
| *(other schemas)*     |    2.70 |     0.90 |     3.60 |         38 |
| **Server total**      |**124.79**|**47.37**|**172.16**|       313 |

It looks like a closed-form answer, but it's not. Two important things:

- **`data_length` and `index_length` are estimates** that InnoDB refreshes periodically and that depend on the last `ANALYZE TABLE`. On very volatile tables they can underestimate by 10-15%. For critical data, cross-check with the physical size of `.ibd` files in the datadir (`du -sh /var/lib/mysql/user_portal/*.ibd`).
- **The server total isn't the backup size.** The dump file (logical) is more compact because it doesn't replicate InnoDB fragmentation, but it contains textual `INSERT`s that weigh more than the binary data. In practice, the uncompressed dump weighs 70-90% of `data_length + index_length`. With standard `gzip` you get down to 15-25%, with `zstd -3` around 18-28% but much faster.

Running the query across the four servers, the total sizing I took to the PM was:

| Server    | MySQL  | Schemas | Total data + index | .ibd files on disk |
|-----------|:------:|--------:|-------------------:|-------------------:|
| mysql-01  | 8.0.34 |       7 |           172.2 GB |            181 GB  |
| mysql-02  | 8.0.33 |       5 |            94.7 GB |             98 GB  |
| mysql-03  | 8.0.32 |       9 |           218.5 GB |            229 GB  |
| mysql-04  | 8.0.34 |       4 |            46.1 GB |             49 GB  |
| **Total** |        |      25 |         **531.5 GB** |       **557 GB** |

The gap between "data + index" and "physical files" is the cost of fragmentation and the `ibtmp1` tablespace. It's worth highlighting to the PM because on the new environment you can plan a post-migration `OPTIMIZE TABLE` that reclaims that 5-6% of space.

## 📈 2. How fast they grow — periodic snapshots and binary log reads

The growth number is trickier. The PM asks "how much per month", but the useful answer is: *how much do you expect it to grow over the next three to six months, that is, until the next assessment?* There are two approaches, both valid, which I use together.

**Approach 1 — periodic snapshots.** If you have monitoring history available (Prometheus + `mysqld_exporter`, Zabbix, or even just the folder of historical backups), you can reconstruct the size curve. If you have nothing, start now: a weekly cron job that runs the query above and writes the result to an `ops.sizing_history` table — after 6-8 weeks you have a solid number.

```sql
-- History table (run once)
CREATE TABLE ops.sizing_history (
    captured_at   TIMESTAMP NOT NULL,
    server_name   VARCHAR(50) NOT NULL,
    schema_name   VARCHAR(64) NOT NULL,
    data_bytes    BIGINT,
    index_bytes   BIGINT,
    num_tables    INT,
    PRIMARY KEY (captured_at, server_name, schema_name)
);

-- Weekly snapshot via cron
INSERT INTO ops.sizing_history (captured_at, server_name, schema_name, data_bytes, index_bytes, num_tables)
SELECT
    NOW(),
    @@hostname,
    table_schema,
    SUM(data_length),
    SUM(index_length),
    COUNT(*)
FROM information_schema.TABLES
WHERE table_schema NOT IN ('mysql', 'sys', 'performance_schema', 'information_schema', 'ops')
GROUP BY table_schema;
```

**Approach 2 — estimate from the {{< glossary term="binary-log" >}}binary log{{< /glossary >}}.** This is the trick many people don't use. The binlog records every write, and its daily size is an excellent proxy for the data growth rate (net of updates and deletes, which generate traffic but not net growth). With `expire_logs_days=7` you have a week of history ready to read.

```bash
# Daily binlog volume (last 7 days)
ls -la /var/lib/mysql/binlog.* | awk '{print substr($6" "$7,1,6), $5}' | \
    sort | awk '{a[$1]+=$2} END {for (k in a) printf "%s  %.2f GB\n", k, a[k]/1024/1024/1024}'
```

Typical output on one of the servers:

```
Apr 14   3.87 GB
Apr 15   4.12 GB
Apr 16   3.95 GB
Apr 17   4.44 GB
Apr 18   2.18 GB   # Saturday
Apr 19   1.02 GB   # Sunday
Apr 20   3.78 GB
```

Weekday average ~4 GB/day of write traffic. Net tablespace growth rate is typically 20% to 40% of the binlog volume, depending on the insert/update/delete mix. In our case, cross-referencing with the few snapshots available, we arrived at an estimate of **+8-12 GB per month per server**, with peaks on `mysql-03` (the user portal one, more dynamic).

## 💾 3. How long the backup takes — `mysqldump`, `mydumper`, `xtrabackup`

Here the PM expects a single number. The honest answer: it depends on which tool you use, and the times can differ by an order of magnitude.

On the same server (`mysql-03`, 218 GB of data + indexes, InnoDB tables with some leftover MyISAM that nobody has touched since 2014), I empirically measured four strategies.
