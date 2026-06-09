---
title: "ORA-00205 alle tre di notte: capire i file critici Oracle prima di averne bisogno"
date: 2099-12-31
draft: true
section: oracle
webo_status: da_tradurre
webo_generated_at: 2026-06-09
---

## The call

[3:08] The phone vibrates on the nightstand. It's Paolo, DBA at the pharmaceutical client — Oracle 19c, batch traceability, regulatory compliance. The storage maintenance window had closed at 2:30. He'd tried the startup. The instance hadn't come back up.

He reads me the message from his phone, voice flat but with that subtle tension of someone who knows the system is down and doesn't yet know why:

```text
ORA-00205: error in identifying control file
  '/u01/app/oracle/oradata/PHARMDB/control01.ctl'
```

It's the first real on-call emergency he's handling. He's not unprepared: he knows Oracle, knows how to use the commands, has read the client documentation. The thing is, that documentation is written as a reference, not as a method. And in that moment, what he needs is a method.

---

## The MOUNT phase

[3:09] The first thing I ask him isn't "did you check the permissions?" or "is the listener up?". I ask: "which startup phase did Oracle stop at?".

It's not a rhetorical question. It's the starting point for any diagnosis on an instance that won't start.

Oracle brings up a database in three distinct phases [1]:

**`NOMOUNT`** — Oracle allocates the SGA and starts the background processes by reading the **parameter file** (SPFILE or PFILE). At this stage it doesn't yet know the physical database: it only knows how to configure the instance in memory.

**`MOUNT`** — Oracle reads the **control file**. Here the instance "discovers" the physical structure of the database: which datafiles exist, where they are, what the current SCN is, what the state of the redo logs is. Only after MOUNT does Oracle know what it's managing.

**`OPEN`** — Oracle verifies the consistency of the **online redo log files** and datafiles, applies recovery if necessary, and opens the database to users.

The practical consequence is direct: if the parameter file is corrupted or missing, Oracle doesn't even reach NOMOUNT. If the control file is inaccessible, the instance stops at MOUNT. If the redo logs are corrupted, the block happens at OPEN.

Knowing this sequence means that, reading an ORA code, you know which phase everything stopped at — and therefore which file to look for first, without guessing in the dark.

Paolo thinks for a second. "ORA-00205 is in MOUNT. So it's the control file."

Exactly.

---

## The control file and the remount

[3:11] I walk him through three checks to run in sequence, in this order:

**(a)** give me the exact path from the ORA-00205 message
**(b)** `ls -la` on that path and tell me the owner and permissions
**(c)** compare with the pre-maintenance runbook we'd written together the year before

While Paolo opens the terminal, I explain why the control file is the critical point at that phase.

The control file is a binary file that Oracle updates continuously during operation. It contains information that no other file can provide [3]:

- the database name (`db_name`)
- the list of all datafiles with their respective paths and status
- the list of online redo log files
- the current SCN (System Change Number) — the database's "logical timestamp"
- checkpoint information
- the RMAN backup catalog, when RMAN is used with the control file as its repository

Oracle cannot mount the database without the control file: it would have no way of knowing which datafiles belong to the instance, what their state is, or whether the database is consistent. It's a structural dependency.

To verify the control files on a running instance [4]:

```sql
SELECT name FROM v$controlfile;
```

On `oracle-node-01` with SID `PHARMDB`, the output with a multiplexed configuration is:

```text
NAME
--------------------------------------------------
/u01/app/oracle/oradata/PHARMDB/control01.ctl
/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl
```

Two copies, on physically separate paths. Multiplexing isn't optional: if the control file lives on a single disk and that disk has a problem, the database won't open and recovery becomes significantly more complex. It's configured in the parameter file:

```text
control_files = '/u01/app/oracle/oradata/PHARMDB/control01.ctl',
                '/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl'
```

Oracle writes synchronously to all copies. If one becomes inaccessible, it logs the error and continues operating with the remaining copies — as long as at least one is available.

**Note on ASM**: in environments using Automatic Storage Management, physical paths are replaced by logical paths of the form `+DATA/PHARMDB/CONTROLFILE/current.260.1234567890`. The concept remains identical — the same three critical file types — only the physical management changes, delegated to ASM. The SQL verification commands are the same; only the output differs.

[3:14] Paolo runs the `ls -la`. The permissions have changed: before the maintenance the owner was `oracle:oinstall`, now it's `root:root`. Oracle can't read the file.

The control file was physically intact. The storage team had remounted the `/u01` filesystem with different permissions after the maintenance, and Oracle couldn't open it.

I tell him straight away: "ok, we call storage. Don't touch anything yourself, no manual `chmod`." Not because he couldn't do it — he could — but because in a regulatory compliance system every manual change outside procedure becomes a documentation problem on top of a technical one. The fix has to go through the storage team, with a ticket opened and tracked.

While we wait for storage to connect, I point something out: if the `ls -la` had shown the file intact and accessible, the next step would have been to go back one phase, to the parameter file. Different error, different phase: typically `ORA-01078` (failure in processing system parameters) or `LRM-00109` (could not open parameter file), and in that case Oracle wouldn't have reached NOMOUNT at all.

The parameter file is the absolute starting point: Oracle reads it before anything else to know how to configure the instance in memory, and above all to know where the control files are. The `control_files` parameter that specifies the paths lives right there.

There are two variants [2]:

**PFILE** (`init<SID>.ora`) — a text file, editable with any editor. Requires a restart to apply changes. Useful in development environments or as a human-readable backup of the parameters.

**SPFILE** (`spfile<SID>.ora`) — a binary file, managed by Oracle. Allows live changes with `ALTER SYSTEM SET` without restarting the instance. In production, SPFILE is almost always what you'll find.

Oracle's search order is precise: it looks first for the SPFILE at the default path, then the PFILE. On Linux/Unix:

```bash
# SPFILE (default)
$ORACLE_HOME/dbs/spfilePHARMDB.ora

# PFILE (fallback)
$ORACLE_HOME/dbs/initPHARMDB.ora
```

To verify which parameter file is in use on a running instance:

```sql
-- If VALUE is empty, Oracle is using a PFILE
SHOW PARAMETER spfile;
```

Paolo takes note. In our case the parameter file was fine — the problem was one phase further along — and the mental model is now complete.

---

## The full startup

[3:23] Storage applies `chmod 640` and restores `oracle:oinstall` as owner on the `/u01` files. Paolo restarts the instance.

[3:38] The instance clears MOUNT. Then it stops at OPEN with a warning on the redo logs.

I explain what he's looking at.

The online redo log files are the last element of the critical triad. Every change that happens in the database — an `INSERT`, an `UPDATE`, a `DELETE` — is written to the redo logs first, and only afterwards (asynchronously) to the datafiles. This mechanism is called **write-ahead logging**: if the system crashes before the data is written to the datafiles, Oracle can reconstruct the changes by reading the redo logs. Without redo logs, Oracle can't guarantee database consistency in the event of a crash — which is why, if they're corrupted or missing, the database won't open [5].

The redo logs are organized into **groups**. Oracle writes in a circular fashion: it fills group 1, moves to group 2, then group 3, then back to group 1. Each group can contain one or more **members** — identical copies of the log on different paths, for redundancy.

```sql
-- Redo log group status
SELECT group#, members, status, bytes/1024/1024 AS mb
FROM v$log;

-- Physical paths of members
SELECT group#, member
FROM v$logfile
ORDER BY group#;
```

The output for `PHARMDB` with three 200MB groups:

```text
GROUP#  MEMBERS  STATUS    MB
------  -------  --------  ---
     1        1  INACTIVE  200
     2        1  CURRENT   200
     3        1  INACTIVE  200
```

`CURRENT` is the group Oracle is currently writing to. `INACTIVE` indicates groups that have already been cycled through, no longer needed for recovery of the current instance. `ACTIVE` would flag a group still needed for recovery but no longer current — a status that requires attention before any operations on the logs.

The physical paths on `oracle-node-01`:

```bash
/u01/app/oracle/oradata/PHARMDB/redo01.log   # GROUP 1, 200MB
/u01/app/oracle/oradata/PHARMDB/redo02.log   # GROUP 2, 200MB
/u01/app/oracle/oradata/PHARMDB/redo03.log   # GROUP 3, 200MB
```

Typical errors when redo logs are inaccessible or corrupted:

```text
ORA-00313: open failed for members of log group 1 of thread 1
ORA-00312: online log 1 thread 1: '/u01/app/oracle/oradata/PHARMDB/redo01.log'
```

In this case it wasn't a real issue. The remount of `/u01` had also touched the redo log directory, and Oracle had logged a warning during the first open attempt. Paolo checks the group status with `v$log`, verifies the permissions on the physical files: everything fine after the `chmod` storage had applied. The warning had already cleared.

[3:42] Database OPEN. Batch traceability back online.

---

## Reference sheet

Paolo calls me back straight after. "Ivan, thank you, I'd never have got there in time on my own. I read the client documentation but it's written as a reference, not as a method. Now I understand the sequence, and I understand why we need the runbook."

I tell him to write down two tables in his notebook — the ones we should have put in the runbook from the start.

**Standard paths and OFA conventions**

Oracle recommends a layout convention called **OFA** (Optimal Flexible Architecture) that organizes instance files in a predictable way. Following it isn't mandatory, and in production it makes routine maintenance and recovery significantly more manageable.

| File | Typical Linux path (OFA) | Verification command |
|---|---|---|
| SPFILE | `/u01/app/oracle/product/19.0.0/dbhome_1/dbs/spfilePHARMDB.ora` | `SHOW PARAMETER spfile` |
| Control file 1 | `/u01/app/oracle/oradata/PHARMDB/control01.ctl` | `SELECT name FROM v$controlfile` |
| Control file 2 | `/u02/app/oracle/fast_recovery_area/PHARMDB/control02.ctl` | `SELECT name FROM v$controlfile` |
| Redo log group 1 | `/u01/app/oracle/oradata/PHARMDB/redo01.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 2 | `/u01/app/oracle/oradata/PHARMDB/redo02.log` | `SELECT group#, member FROM v$logfile` |
| Redo log group 3 | `/u01/app/oracle/oradata/PHARMDB/redo03.log` | `SELECT group#, member FROM v$logfile` |

**Diagnostic map: what blocks what**

When an Oracle instance won't start, the first question is: which phase did it stop at? The answer is almost always in the alert log, and the ORA code points directly to which critical file is involved.

| Missing/corrupted file | Blocked phase | Typical ORA error | First action |
|---|---|---|---|
| SPFILE/PFILE | Pre-NOMOUNT | `ORA-01078`, `LRM-00109` | Check existence and permissions in `$ORACLE_HOME/dbs/` |
| Control file | MOUNT | `ORA-00205` | Check path in `control_files`, filesystem permissions, availability of multiplexed copies |
| Online redo log | OPEN | `ORA-00313`, `ORA-00312` | Check `v$logfile`, group status in `v$log`, physical integrity of files |

This isn't a recovery guide — that's a separate topic, one that requires distinguishing between a corrupted control file and a missing one, between a CURRENT redo log and an INACTIVE one, between RMAN recovery and manual recovery. It's a diagnostic map: it's there to stop you heading in the wrong direction in the first minutes of an emergency.

---

## The takeaway

Paolo wasn't unprepared because he was incompetent. He knew the syntax — he knew what `SHOW PARAMETER spfile` does, knew how to query `v$controlfile`. What he hadn't yet internalized was the startup sequence as a diagnostic method: which file Oracle reads at each phase, and therefore which file to look for first when something goes wrong.

The difference between twenty minutes spent on the network, the listener, and the OS versus three checks that go straight to the point isn't years of accumulated experience. It's having a mental model of the sequence — NOMOUNT, MOUNT, OPEN — and knowing what maps to what.

The value of that call wasn't solving the problem for him. It was transferring that model in thirty minutes, with a real case right in front of us. Now Paolo knows what to ask the storage team next time ("were the permissions on `/u01` changed during the maintenance?"), knows which lines in the alert log matter, knows what order to rule out hypotheses in.

The senior DBA who stops getting called in the middle of the night has invested in two things: a well-written runbook put together with the client's team, and the ability to guide remotely whoever is on-call — giving them the three right checks instead of sending them on a thirty-step hunt in the dark.

---

## Official sources

1. Oracle Database Concepts 19c — Startup and Shutdown: NOMOUNT/MOUNT/OPEN sequence and the role of critical files — `<TODO: scout exact URL for Oracle 19c Concepts, chapter "Starting Up a Database">`

2. Oracle Database Administrator's Guide 19c — Managing Initialization Parameters: SPFILE, PFILE, search order, `ALTER SYSTEM SET` — `<TODO: scout exact URL for chapter "Managing Initialization Parameters Using a Server Parameter File">`

3. Oracle Database Administrator's Guide 19c — [Managing the Online Redo Log](https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-the-online-redo-log.html) — groups, members, status, `v$log`, `v$logfile`, ORA-00313/ORA-00312 errors

4. Oracle Database Reference 19c — [V$CONTROLFILE](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-CONTROLFILE.html) — structure and verification queries for control files

5. Oracle Database Reference 19c — [V$LOG](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-LOG.html) — columns `GROUP#`, `MEMBERS`, `STATUS`, `BYTES`; interpreting CURRENT/ACTIVE/INACTIVE status

6. oracle-base.com (Tim Hall) — `<TODO: scout specific URL for "Oracle Database Startup and Shutdown" on oracle-base.com>` — startup sequence, common errors, practical examples

---

## Glossary candidate

- **SPFILE** (Oracle) — Server Parameter File: binary file read by Oracle at startup containing instance configuration parameters (`db_name`, `control_files`, `memory_target`, etc.). Can be modified live with `ALTER SYSTEM SET` without restarting the database.

- **Control File** (Oracle) — Binary file continuously updated by Oracle that records the physical structure of the database: datafile and redo log paths, current SCN, checkpoint information. Indispensable for the MOUNT phase; must be multiplexed across physically separate paths.

- **Online Redo Log** (Oracle) — Circular file that sequentially records all changes made to the database (redo entries) before they are written to the datafiles. Organized into groups with optional multiple members for redundancy; the foundation of the crash recovery mechanism.

- **SCN** (System Change Number) — Monotonically increasing sequential number that Oracle uses to identify a precise point in the life of the database. Present in the control file and datafiles; used to determine consistency and the recovery point.

- **OFA** (Optimal Flexible Architecture) — Naming and path layout convention recommended by Oracle for organizing instance files (datafiles, control files, redo logs, backups) in a predictable, maintainable, and portable way across different environments.
