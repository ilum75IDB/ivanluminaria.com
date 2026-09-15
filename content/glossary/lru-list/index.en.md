---
title: "LRU list"
description: "InnoDB's two-zone structure that manages buffer pool page eviction, shielding hot data from occasional full scan pollution."
translationKey: "glossary_lru_list"
aka: "LRU list (young list + old list)"
articles:
  - "/posts/mysql/innodb-buffer-pool-dimensionamento-hit-ratio-e-warm-up-dopo-restart"
---

The LRU list is the data structure InnoDB uses to decide which pages to keep in the buffer pool and which to evict when memory is full. Unlike a classic single-linked LRU, InnoDB implements a two-zone variant that separates frequently accessed ("hot") pages from newly loaded ones, limiting the risk that a large scan flushes out data that is regularly needed.

## How it works

The list is split into two contiguous sub-zones:

- **Young list** (head, ~5/8 of the list): holds pages that have been accessed multiple times recently. These are the hot pages InnoDB tries to retain in cache as long as possible.
- **Old list** (tail, ~3/8 of the list): the entry point for every page loaded from disk for the first time. A page stays in the old list for at least `innodb_old_blocks_time` milliseconds (default 1000 ms) before it can be promoted to the young list.

When the buffer pool is full, InnoDB evicts pages from the tail of the old list (the coldest ones). Promotion from old to young only happens if the page is accessed again after the configured waiting period has elapsed.

## Operational context

The two-zone mechanism protects the young list during full scans: pages read sequentially enter the old list but, if not re-accessed within the timeout, are evicted without ever displacing hot data. This matters most in scenarios such as:

- nightly reports or ETL jobs running `SELECT` over large tables
- `mysqldump` or logical backups reading entire tables
- occasional analytical queries on OLTP instances

The key parameters to monitor and tune are `innodb_old_blocks_pct` (percentage reserved for the old list, default 37) and `innodb_old_blocks_time`. A value of `innodb_old_blocks_time` that is too low makes the protection ineffective; one that is too high can delay promotion of genuinely hot pages.
