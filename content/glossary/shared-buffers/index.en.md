---
title: "shared_buffers"
description: "PostgreSQL's shared memory area serving as a cache for data blocks, the most important parameter for memory tuning."
translationKey: "glossary_shared-buffers"
aka: "Shared Buffer Cache"
articles:
  - "/posts/postgresql/pg-stat-statements"
---

**shared_buffers** is the parameter that controls the size of the shared memory area PostgreSQL uses as a cache for data blocks read from disk. Every time PostgreSQL reads a data page (8 KB), it keeps it in shared_buffers for subsequent reads.

## How it works

PostgreSQL allocates memory for shared_buffers at service startup. All backend processes share this memory area. When a process needs a data block, it first looks in shared_buffers. If it finds it (cache hit), the read is immediate. If not (cache miss), it must read from disk — an operation orders of magnitude slower.

## How much to allocate

The default value is 128 MB — inadequate for any production database. The rule of thumb is to set shared_buffers to 25% of available RAM. On a server with 64 GB of RAM, 16 GB is a good starting point. Values beyond 40% of RAM rarely bring benefits because PostgreSQL also relies on the operating system's cache.

## How to monitor it

The `pg_stat_bgwriter` view shows the ratio between `buffers_alloc` (newly allocated blocks) and the total blocks served. A cache hit ratio below 95% suggests that shared_buffers may be undersized.
