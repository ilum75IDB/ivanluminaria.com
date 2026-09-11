---
title: "Transparent Data Encryption (TDE)"
description: "Funzionalità Oracle che cifra dati a riposo — file di dati, redo log, backup — senza modifiche applicative, proteggendo i supporti fisici da accessi non autorizzati."
translationKey: "glossary_transparent_data_encryption"
aka: "TDE, cifratura trasparente dei dati"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Transparent Data Encryption (TDE) è una funzionalità di Oracle Database che cifra i dati a riposo — file di dati, redo log, temp file e backup — a livello di storage, senza richiedere alcuna modifica al codice applicativo. Il motore di cifratura opera in modo trasparente tra il buffer cache e il disco: i dati vengono decifrati al momento della lettura in memoria e cifrati al momento della scrittura su disco.

## Come funziona

TDE utilizza un'architettura a due livelli di chiavi: una **Master Encryption Key (MEK)** custodita nel wallet Oracle (file `ewallet.p12`) o in un HSM esterno, e una **Table/Tablespace Encryption Key** generata per ogni oggetto cifrato. La MEK non risiede mai nei file di dati, rendendo inutilizzabili i file sottratti fisicamente senza accesso al wallet.

Abilitare TDE su una tablespace esistente richiede una riorganizzazione online:

```sql
-- Creazione tablespace cifrata (AES256)
CREATE TABLESPACE sensitive_data
  DATAFILE '/u01/oradata/ORCL/sensitive01.dbf' SIZE 500M
  ENCRYPTION USING 'AES256'
  DEFAULT STORAGE (ENCRYPT);

-- Cifratura di una tablespace esistente (online, Oracle 12.2+)
ALTER TABLESPACE users ENCRYPTION ONLINE ENCRYPT;
```

## Quando si usa

TDE è lo strumento standard per soddisfare requisiti normativi come GDPR, PCI-DSS e HIPAA che impongono la cifratura dei dati a riposo. È particolarmente rilevante in ambienti data warehouse dove i backup su nastro o cloud object storage escono dal perimetro di controllo fisico del datacenter. Non protegge da utenti con accesso legittimo al database: un DBA con privilegi `SYSDBA` legge i dati in chiaro. La protezione è contro il furto fisico dei supporti o l'accesso non autorizzato ai file system sottostanti.

L'overhead di performance è generalmente contenuto (2-7% su workload OLTP tipici), ma va misurato su workload I/O intensivi come full table scan su fact table di grandi dimensioni.
