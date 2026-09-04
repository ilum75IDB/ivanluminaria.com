---
title: "Unified Auditing"
description: "Framework de auditare Oracle (12c+) care centralizează toate jurnalele într-o singură structură AUDSYS, înlocuind parametrul AUDIT_TRAIL."
translationKey: "glossary_unified_auditing"
aka: "Unified Audit Trail"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Unified Auditing este framework-ul introdus în Oracle 12c pentru a consolida într-o singură destinație — structura `AUDSYS` — toate înregistrările de audit generate de baza de date: audit standard, fine-grained auditing (FGA), operațiuni SYSDBA/SYSOPER și evenimente Recovery Manager. Începând cu Oracle 21c, framework-ul este obligatoriu, iar parametrul moștenit `AUDIT_TRAIL` nu mai are efect.

## Cum funcționează

Înregistrările sunt scrise în tabela internă `UNIFIED_AUDIT_TRAIL` (accesibilă prin view-ul cu același nume) prin politici declarative create cu `CREATE AUDIT POLICY`. O politică poate filtra după acțiune, obiect, utilizator sau condiție booleană.

```sql
-- Politică de audit pentru SELECT-uri sensibile
CREATE AUDIT POLICY audit_select_emp
  ACTIONS SELECT ON hr.employees
  WHEN 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''HR'''
  EVALUATE PER SESSION;

AUDIT POLICY audit_select_emp;
```

Înregistrările sunt scrise asincron într-un tablespace dedicat gestionat de `AUDSYS`; flush-ul periodic este controlat de parametrul `UNIFIED_AUDIT_SGA_QUEUE_SIZE`.

## Când se utilizează

Unified Auditing este relevant în orice context care impune conformitate normativă (GDPR, PCI-DSS, SOX) sau trasabilitate operațională pe medii Oracle 12c și versiuni ulterioare. Față de audit trail-ul clasic, oferă:

- **un singur punct de citire** pentru toate tipurile de evenimente;
- **politici granulare** care pot fi activate/dezactivate fără repornire;
- **overhead redus** datorită scrierii asincrone.

Limitarea principală este că `UNIFIED_AUDIT_TRAIL` crește rapid pe sisteme cu trafic intens: este necesară planificarea unei politici de purjare prin `DBMS_AUDIT_MGMT`.
