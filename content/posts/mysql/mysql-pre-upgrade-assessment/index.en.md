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

**`{{< glossary term="mysqldump" >}}mysqldump{{< /glossary >}}` (logical, single-threaded):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob \
    --all-databases > /backup/mysql-03-full.sql
```

Result: 2 hours 47 minutes. Uncompressed SQL file: 189 GB. With real-time pipe to `gzip` (`| gzip -3 > ...gz`): 3 hours 22 minutes, compressed file 38 GB.

**`mysqldump` + `zstd` (my favorite for PA servers where CPU time matters less than the window):**

```bash
time mysqldump --single-transaction --quick --routines --triggers --events \
    --default-character-set=utf8mb4 --hex-blob --all-databases | \
    zstd -3 -T4 > /backup/mysql-03-full.sql.zst
```

Result: 2 hours 58 minutes, compressed file 42 GB. Slightly larger than gzip but **roughly twice as fast** to decompress during restore — which is the moment speed actually matters.

**`{{< glossary term="mydumper" >}}mydumper{{< /glossary >}}` (logical, parallel):**

```bash
time mydumper --host=localhost --user=backup --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --compress --rows=500000 \
    --outputdir=/backup/mysql-03-mydumper \
    --logfile=/backup/mysql-03-mydumper.log
```

Result: 47 minutes. Output: directory with 312 compressed files, total 41 GB. Nearly 4x faster than `mysqldump` thanks to chunk-level table parallelism.

**`xtrabackup` (physical, hot backup):**

```bash
time xtrabackup --backup --target-dir=/backup/mysql-03-xtra \
    --user=backup --password=*** --parallel=4 --compress --compress-threads=4
```

Result: 22 minutes. Output: 179 GB uncompressed / 48 GB compressed. It's the fastest because it copies InnoDB files at the physical level instead of regenerating `INSERT`s, but it has one important constraint: **leftover MyISAM tables get locked** for the duration of their copy. Fortunately on `mysql-03` they were residual and only read by a nightly batch, so no impact.

Summary I presented to the PM:

| Tool                    | Backup time | Output size | Notes                                           |
|-------------------------|------------:|------------:|-------------------------------------------------|
| `mysqldump` + gzip      | 3h 22m      | 38 GB       | baseline, single-thread, available everywhere   |
| `mysqldump` + zstd      | 2h 58m      | 42 GB       | faster on restore                               |
| `mydumper` + compress   | 47m         | 41 GB       | parallel, excellent time/space tradeoff         |
| `xtrabackup` + compress | 22m         | 48 GB       | physical, fastest, MyISAM constraints           |

In the assessment I proposed standardizing on **`mydumper` for periodic backup** (daily, low disk footprint, flexible schema-level restore) and **`xtrabackup` for the pre-upgrade snapshot** (very fast, ideal for the tight maintenance window).

## ⏱️ 4. How long the restore takes — the number the PM forgets to ask

Restore is where badly-done assessments fail. A backup can take 47 minutes, but restoring the same dataset may take hours — and in the maintenance window, that's what matters.

Again on `mysql-03`, empirical measurement of how long it takes to rebuild the database from scratch using the backups above, on a twin host (same CPU, same NVMe storage):

**From `mysqldump.sql.gz`:**

```bash
time gunzip -c /backup/mysql-03-full.sql.gz | \
    mysql --default-character-set=utf8mb4
```

Result: **5 hours 12 minutes**. Slow because logical restore regenerates every row with individual `INSERT`s, updates indexes transactionally, and cannot parallelize on a single table.

**From `mysqldump.sql.zst`:**

```bash
time zstd -dc /backup/mysql-03-full.sql.zst | \
    mysql --default-character-set=utf8mb4
```

Result: **4 hours 38 minutes**. Here you see the zstd decompression advantage (roughly 2x faster than gzip), which is the only element that differs from the previous test.

**From `mydumper` with `myloader`:**

```bash
time myloader --host=localhost --user=root --socket=/var/lib/mysql/mysql.sock \
    --threads=8 --directory=/backup/mysql-03-mydumper \
    --disable-redo-log --overwrite-tables
```

Result: **1 hour 52 minutes**. The `--disable-redo-log` flag (MySQL 8.0.21+) is the real game-changer: it skips redo log generation during initial load, reducing I/O overhead. Use ONLY on an empty instance during import, never in production.

**From `xtrabackup`:**

```bash
time xtrabackup --decompress --target-dir=/backup/mysql-03-xtra --parallel=4
time xtrabackup --prepare --target-dir=/backup/mysql-03-xtra
# then rsync of files to the new datadir + mysqld startup
```

Result: **34 minutes** (decompress) + **12 minutes** (prepare) + **6 minutes** (copy + restart) = **52 minutes total**. Physical restore: binary copy + crash recovery, no regenerated SQL. It's the only option that comes close to the backup time itself.

Restore summary:

| Strategy               | Restore time | Notes                                                   |
|------------------------|-------------:|---------------------------------------------------------|
| `mysqldump` + gzip     | 5h 12m       | to be avoided for datasets > 50 GB                      |
| `mysqldump` + zstd     | 4h 38m       | only if you have no alternatives                        |
| `mydumper` + myloader  | 1h 52m       | with `--disable-redo-log`, fast logical restore         |
| `xtrabackup`           | 52m          | physical, the only option compatible with tight windows |

## 📋 5. The response template for the PM

After measurements across the four servers, I consolidated everything into a single table — because what the PM needs is a page to attach to the cutover plan, not thirty slides.

| Server    | Current size | Estimated growth | Backup (`xtrabackup`) | Restore (`xtrabackup`) | Worst-case restore (`mysqldump+gz`) |
|-----------|-------------:|-----------------:|----------------------:|-----------------------:|------------------------------------:|
| mysql-01  |     172 GB   | +8 GB/month      |               18 min  |                45 min  |                          4h 10m     |
| mysql-02  |      95 GB   | +3 GB/month      |               11 min  |                28 min  |                          2h 25m     |
| mysql-03  |     219 GB   | +12 GB/month     |               22 min  |                52 min  |                          5h 12m     |
| mysql-04  |      46 GB   | +2 GB/month      |                6 min  |                15 min  |                          1h 20m     |
| **Total** |  **532 GB** | **+25 GB/month** |          **57 min**   |         **2h 20m**     |                    **13h 07m**      |

Based on this table, the six-hour maintenance window is **compatible with an `xtrabackup`-based rollback** (57-minute snapshot + 2h 20m restore = 3h 17m, with a 2h 43m margin for debugging and verification), but **incompatible with a `mysqldump`-based rollback** (more than 13 hours). Operational decision: `xtrabackup` as the primary rollback strategy, `mydumper` as a fallback for targeted schema-by-schema restores if specific problems surface during the cutover.

The PM asked for four numbers. I gave him twenty-four. But they're twenty-four measured numbers — not eyeballed estimates — and the difference is all there.

## What I learned

A pre-upgrade assessment isn't a technical document, it's a risk-governance tool. The customer asking "how long does the backup take" is actually asking *"if things go sideways in the maintenance window, can we get services back up before 6am?"*. If your answer is "about three hours, I think", that question is still unanswered and the risk hasn't been measured.

The technical part — the queries, the tools, the measurements — is the easy part. The hard part is making sure the measured numbers end up in the cutover plan, that the PM reads them, that the ops team uses them to calibrate the window. In our case the PM wanted to add one more slide to the meeting with the new storage vendor: *"look, these are the reference numbers; if your array can't sustain these restore throughputs, the plan doesn't work"*. Which is exactly what a good PM should do.

In the end the upgrade went through in four hours, not six. No rollback. The customer thanked us not for the short window, but for the fact that they had **always known what would happen if something went wrong**. Which is the real goal of a well-done pre-upgrade assessment.

------------------------------------------------------------------------

## Glossary

**[information_schema](/en/glossary/information-schema/)** — MySQL system schema (read-only) that exposes metadata about databases, tables, indexes, users and server state. The starting point for any assessment, sizing or structural analysis.

**[xtrabackup](/en/glossary/xtrabackup/)** — Hot physical backup tool for MySQL/MariaDB developed by Percona. Copies InnoDB files directly while the database is running, handling in-flight transactions via the redo log. Significantly faster than logical backups on large datasets.

**[Pre-upgrade assessment](/en/glossary/pre-upgrade-assessment/)** — Structured measurement of size, growth rate, backup times and restore times of a database before an upgrade. Used to size the maintenance window and define a realistic rollback strategy.

**[mysqldump](/en/glossary/mysqldump/)** — Logical backup utility included in every MySQL installation. Produces a sequential SQL file with all statements needed to recreate schema and data. Single-threaded, reliable but slow on large databases.

**[mydumper](/en/glossary/mydumper/)** — Open-source logical backup tool for MySQL/MariaDB with real chunk-level parallelism. It splits large tables into pieces and exports them with multiple threads, with parallel restore via myloader.
