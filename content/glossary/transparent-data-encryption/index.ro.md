---
title: "Transparent Data Encryption (TDE)"
description: "Funcționalitate Oracle care criptează datele la repaus — fișiere de date, redo log-uri, backup-uri — fără modificări aplicative, protejând suporturile fizice de accesul neautorizat."
translationKey: "glossary_transparent_data_encryption"
aka: "TDE, criptare transparentă a datelor"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Transparent Data Encryption (TDE) este o funcționalitate Oracle Database care criptează datele la repaus — fișiere de date, redo log-uri, fișiere temporare și backup-uri — la nivelul stocării, fără a necesita modificări în codul aplicațiilor. Motorul de criptare operează transparent între buffer cache și disc: datele sunt decriptate la citirea în memorie și criptate la scrierea pe disc.

## Cum funcționează

TDE utilizează o arhitectură cu două niveluri de chei: o **Master Encryption Key (MEK)** stocată în wallet-ul Oracle (fișierul `ewallet.p12`) sau într-un HSM extern, și o **Table/Tablespace Encryption Key** generată pentru fiecare obiect criptat. MEK nu rezidă niciodată în fișierele de date, ceea ce face inutilizabile fișierele sustrase fizic fără acces la wallet.

Activarea TDE pe o tablespace existentă necesită o reorganizare online:

```sql
-- Creare tablespace criptată (AES256)
CREATE TABLESPACE sensitive_data
  DATAFILE '/u01/oradata/ORCL/sensitive01.dbf' SIZE 500M
  ENCRYPTION USING 'AES256'
  DEFAULT STORAGE (ENCRYPT);

-- Criptarea unei tablespace existente online (Oracle 12.2+)
ALTER TABLESPACE users ENCRYPTION ONLINE ENCRYPT;
```

## Când se folosește

TDE este mecanismul standard pentru îndeplinirea cerințelor normative precum GDPR, PCI-DSS și HIPAA care impun criptarea datelor la repaus. Este deosebit de relevant în mediile de data warehouse unde backup-urile pe bandă sau în cloud object storage ies din perimetrul de control fizic al datacenter-ului. Nu protejează împotriva utilizatorilor cu acces legitim la baza de date: un DBA cu privilegii `SYSDBA` citește datele în clar. Protecția vizează furtul fizic al suporturilor sau accesul neautorizat la sistemul de fișiere subiacent.

Impactul asupra performanței este în general redus (2–7% pe workload-uri OLTP tipice), dar trebuie măsurat pe workload-uri intensive în I/O, cum ar fi full table scan pe fact table-uri de dimensiuni mari.
