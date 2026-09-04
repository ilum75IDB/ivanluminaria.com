---
title: "Unified Auditing"
description: "Framework di auditing Oracle (12c+) che centralizza tutti i log in un'unica struttura AUDSYS, sostituendo il parametro AUDIT_TRAIL."
translationKey: "glossary_unified_auditing"
aka: "Unified Audit Trail"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Unified Auditing è il framework introdotto in Oracle 12c per consolidare in un'unica destinazione — la struttura `AUDSYS` — tutti i record di audit generati dal database: audit standard, fine-grained auditing (FGA), operazioni SYSDBA/SYSOPER e audit di Recovery Manager. In Oracle 21c il framework è obbligatorio e il vecchio parametro `AUDIT_TRAIL` non ha più effetto.

## Come funziona

I record vengono scritti nella tabella interna `UNIFIED_AUDIT_TRAIL` (visibile tramite la view omonima) attraverso policy dichiarative create con `CREATE AUDIT POLICY`. Una policy può filtrare per azione, oggetto, utente o condizione booleana.

```sql
-- Creazione di una policy di audit sulle SELECT sensibili
CREATE AUDIT POLICY audit_select_emp
  ACTIONS SELECT ON hr.employees
  WHEN 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''HR'''
  EVALUATE PER SESSION;

AUDIT POLICY audit_select_emp;
```

I record sono scritti in modo asincrono in un tablespace dedicato gestito da `AUDSYS`; il flush periodico è controllato dal parametro `UNIFIED_AUDIT_SGA_QUEUE_SIZE`.

## Quando si usa

Unified Auditing è rilevante in tutti i contesti che richiedono conformità normativa (GDPR, PCI-DSS, SOX) o tracciabilità operativa su ambienti Oracle 12c e successivi. Rispetto al vecchio audit trail, offre:

- **un solo punto di lettura** per tutti i tipi di evento;
- **policy granulari** attivabili/disattivabili senza riavvio;
- **riduzione dell'overhead** grazie alla scrittura asincrona.

Il limite principale è che la `UNIFIED_AUDIT_TRAIL` cresce rapidamente su sistemi ad alto traffico: è necessario pianificare una policy di purge tramite `DBMS_AUDIT_MGMT`.
