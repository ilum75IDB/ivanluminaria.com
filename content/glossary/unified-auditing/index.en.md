---
title: "Unified Auditing"
description: "Oracle auditing framework (12c+) that centralizes all audit logs into a single AUDSYS structure, replacing the legacy AUDIT_TRAIL parameter."
translationKey: "glossary_unified_auditing"
aka: "Unified Audit Trail"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Unified Auditing is the framework introduced in Oracle 12c to consolidate all audit records into a single destination — the `AUDSYS` structure — covering standard audit, fine-grained auditing (FGA), SYSDBA/SYSOPER operations, and Recovery Manager events. Starting with Oracle 21c the framework is mandatory; the legacy `AUDIT_TRAIL` parameter has no effect.

## How it works

Records are written to the internal table `UNIFIED_AUDIT_TRAIL` (exposed through the view of the same name) via declarative policies created with `CREATE AUDIT POLICY`. A policy can filter by action, object, user, or boolean condition.

```sql
-- Audit policy for sensitive SELECT statements
CREATE AUDIT POLICY audit_select_emp
  ACTIONS SELECT ON hr.employees
  WHEN 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''HR'''
  EVALUATE PER SESSION;

AUDIT POLICY audit_select_emp;
```

Records are written asynchronously to a dedicated tablespace managed by `AUDSYS`; the periodic flush is controlled by the `UNIFIED_AUDIT_SGA_QUEUE_SIZE` parameter.

## When to use it

Unified Auditing is relevant in any context requiring regulatory compliance (GDPR, PCI-DSS, SOX) or operational traceability on Oracle 12c and later environments. Compared to the legacy audit trail, it provides:

- **a single read point** for all event types;
- **granular policies** that can be enabled/disabled without a restart;
- **reduced overhead** thanks to asynchronous writes.

The main limitation is that `UNIFIED_AUDIT_TRAIL` grows rapidly on high-traffic systems: a purge policy via `DBMS_AUDIT_MGMT` must be planned accordingly.
