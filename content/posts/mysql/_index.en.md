---
title: "MySQL"
layout: "list"
description: "MySQL and MariaDB: security, performance and architecture on one of the world's most widely deployed databases."
image: "mysql.cover.jpg"
---

I have seen MySQL servers with 64GB of RAM and `innodb_buffer_pool_size` left at 128MB — "because it is the default and we did not touch anything". I have seen MyISAM tables still in production in 2026 because "we did not have time to convert them", with table-level locks that froze entire applications during backups. I have seen master-slave replicas lagging by 47,000 seconds with nobody noticing, because nobody was watching `Seconds_Behind_Master`.

And I have seen the exact opposite: MySQL estates with hundreds of instances run with discipline, where every decision — storage engine, charset, binlog format, topology — is taken consciously and not out of inertia.

The difference has never been the engine. It has always been **how seriously someone picked the options**.

------------------------------------------------------------------------

MySQL is the database that needs no introduction. It is the engine that powered the growth of the web for over twenty years.

Born in 1995 in Sweden, in 2008 it was acquired by Sun Microsystems — and when Oracle completed its acquisition of Sun in 2010, MySQL ended up in the portfolio of the world's largest commercial database vendor. **I was an Oracle employee at the time**, and I remember the atmosphere well: on one hand the curiosity of seeing how Oracle would manage such a popular open source product, on the other the concern that MySQL would be sidelined in favour of the proprietary database.

That concern drove Michael "Monty" Widenius — MySQL's original creator — to fork the project in 2009, giving birth to **MariaDB**. A project that shares its roots with MySQL but has taken its own path on storage engines, optimizer and advanced features.

History has shown that both projects have survived and evolved. But in the daily reality of those running real production systems, MySQL is still the one that *looks* simple and instead hides critical choices:

- **mixed storage engines** out of old habit — MyISAM, InnoDB and sometimes Archive coexisting without a reason
- **wrong charset** (latin1 instead of utf8mb4) quietly corrupting multilingual data
- **binlog in STATEMENT format** causing inconsistencies in replication for non-deterministic queries
- **permissive `sql_mode`** for "backwards compatibility" — queries returning different results every run
- **replication without active monitoring** — and when the master goes down, the slave is three days behind

------------------------------------------------------------------------

## 🔧 The choices that make the difference in production

There are five decisions that — done well — keep MySQL running for ten years, and — done poorly — force you to rewrite half the application. They are trivial to list, painfully hard to change later.

| Choice | What it decides | How I set it |
|---|---|---|
| **Storage engine** | Lock granularity, transactions, crash recovery | InnoDB always, except for rare justified cases — MyISAM is legacy, not a choice |
| **`innodb_buffer_pool_size`** | Memory for InnoDB data and index cache | 70-80% of RAM on a dedicated server, anything less is wasted for the engine |
| **Charset and collation** | Character encoding and sorting | `utf8mb4` + `utf8mb4_0900_ai_ci` — no `utf8` (which in MySQL is incomplete) |
| **`binlog_format`** | Format of binary logs for replication and PITR | `ROW` almost always — `STATEMENT` causes replication issues with non-deterministic queries |
| **`sql_mode`** | Which errors MySQL tolerates and which not | Strict mode on, `ONLY_FULL_GROUP_BY` included — a permissive MySQL is a MySQL that lies to you |

Five choices. Thirty minutes of discussion. Years of operation without major incidents.

------------------------------------------------------------------------

## 📚 What I talk about here

Real stories and operational decisions on MySQL and MariaDB in production. Security, user and privilege management, InnoDB tuning, master-slave replication and InnoDB Cluster, upgrade and migration strategies, consistent backups with `mysqldump` and physical tools, real differences between MySQL and MariaDB that only show up under load.

No generic recipes. Just what I have seen work in real environments — postal, telco, finance, public administration — where MySQL runs estates of instances in parallel and cannot afford choices made "out of inertia".

------------------------------------------------------------------------

Using MySQL is not just about running queries.

It is about understanding how the engine manages connections, privileges and resources under real load — and recognising that the apparent simplicity is, often, the most expensive trap.
