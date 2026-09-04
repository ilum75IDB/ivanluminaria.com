---
title: "dbupgrade"
description: "Oracle utility that upgrades the data dictionary during a version upgrade, replacing the legacy catupgrd.sql script from 12c onwards."
translationKey: "glossary_dbupgrade"
aka: "dbupgrade (catupgrd.sql successor)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

`dbupgrade` is the shell script introduced by Oracle in version 12c to replace `catupgrd.sql`. It brings the system data dictionary up to the level of the newly installed Oracle version, recompiling internal components and updating views, packages, and system metadata.

## How it works

`dbupgrade` is run by the DBA after starting the database in upgrade mode (`STARTUP UPGRADE`). Internally it orchestrates the same sequence of SQL scripts that `catupgrd.sql` used to run manually, but with built-in error handling, configurable parallelism, and structured per-component logs.

```bash
# Start the database in upgrade mode
sqlplus / as sysdba <<EOF
STARTUP UPGRADE;
EXIT;
EOF

# Run the data dictionary upgrade
cd $ORACLE_HOME/bin
./dbupgrade -n 4 -l /u01/upgrade_logs
```

The `-n` parameter controls the number of parallel worker processes; `-l` sets the log directory. Once complete, the database is restarted in normal mode and `utlrp.sql` is executed to recompile invalid objects.

## When to use it

`dbupgrade` is mandatory in any in-place Oracle upgrade path, or after restoring a database onto a higher-version `ORACLE_HOME`. It is a core step in the DBUA (Database Upgrade Assistant) workflow and can also be invoked manually for unattended or scripted upgrades. In large-database scenarios — such as a 12c-to-21c upgrade on 12 TB tablespaces — the parallelism degree directly affects total upgrade duration.
