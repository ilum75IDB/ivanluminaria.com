---
title: "Transparent Data Encryption (TDE)"
description: "Oracle feature that encrypts data at rest — data files, redo logs, backups — with no application changes required, protecting storage media from unauthorized physical access."
translationKey: "glossary_transparent_data_encryption"
aka: "TDE"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Transparent Data Encryption (TDE) is an Oracle Database feature that encrypts data at rest — data files, redo logs, temp files, and backups — at the storage layer, with no changes required to application code. The encryption engine operates transparently between the buffer cache and disk: data is decrypted on read into memory and encrypted on write to disk.

## How it works

TDE uses a two-tier key architecture: a **Master Encryption Key (MEK)** stored in the Oracle wallet (file `ewallet.p12`) or an external HSM, and a **Table/Tablespace Encryption Key** generated per encrypted object. The MEK never resides in the data files themselves, making stolen files unreadable without wallet access.

Enabling TDE on an existing tablespace requires an online reorganization:

```sql
-- Create an encrypted tablespace (AES256)
CREATE TABLESPACE sensitive_data
  DATAFILE '/u01/oradata/ORCL/sensitive01.dbf' SIZE 500M
  ENCRYPTION USING 'AES256'
  DEFAULT STORAGE (ENCRYPT);

-- Encrypt an existing tablespace online (Oracle 12.2+)
ALTER TABLESPACE users ENCRYPTION ONLINE ENCRYPT;
```

## When to use it

TDE is the standard mechanism for meeting regulatory requirements such as GDPR, PCI-DSS, and HIPAA that mandate encryption of data at rest. It is especially relevant in data warehouse environments where tape or cloud object storage backups leave the physical control perimeter of the datacenter. It does not protect against users with legitimate database access: a DBA holding `SYSDBA` privileges reads data in plaintext. The protection target is physical media theft or unauthorized access to the underlying file system.

Performance overhead is generally low (2–7% on typical OLTP workloads) but should be benchmarked on I/O-intensive workloads such as full table scans over large fact tables.
