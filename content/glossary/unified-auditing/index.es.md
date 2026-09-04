---
title: "Unified Auditing"
description: "Framework de auditoría de Oracle (12c+) que centraliza todos los registros en una única estructura AUDSYS, reemplazando el parámetro AUDIT_TRAIL."
translationKey: "glossary_unified_auditing"
aka: "Unified Audit Trail"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Unified Auditing es el framework introducido en Oracle 12c para consolidar en un único destino — la estructura `AUDSYS` — todos los registros de auditoría generados por la base de datos: auditoría estándar, fine-grained auditing (FGA), operaciones SYSDBA/SYSOPER y eventos de Recovery Manager. En Oracle 21c el framework es obligatorio y el parámetro heredado `AUDIT_TRAIL` ya no tiene efecto.

## Cómo funciona

Los registros se escriben en la tabla interna `UNIFIED_AUDIT_TRAIL` (accesible a través de la vista homónima) mediante políticas declarativas creadas con `CREATE AUDIT POLICY`. Una política puede filtrar por acción, objeto, usuario o condición booleana.

```sql
-- Política de auditoría sobre SELECT sensibles
CREATE AUDIT POLICY audit_select_emp
  ACTIONS SELECT ON hr.employees
  WHEN 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''HR'''
  EVALUATE PER SESSION;

AUDIT POLICY audit_select_emp;
```

Los registros se escriben de forma asíncrona en un tablespace dedicado gestionado por `AUDSYS`; el flush periódico está controlado por el parámetro `UNIFIED_AUDIT_SGA_QUEUE_SIZE`.

## Cuándo se utiliza

Unified Auditing es relevante en cualquier contexto que requiera cumplimiento normativo (GDPR, PCI-DSS, SOX) o trazabilidad operativa en entornos Oracle 12c y posteriores. Frente al audit trail heredado, ofrece:

- **un único punto de lectura** para todos los tipos de evento;
- **políticas granulares** activables/desactivables sin reinicio;
- **menor overhead** gracias a la escritura asíncrona.

La limitación principal es que `UNIFIED_AUDIT_TRAIL` crece rápidamente en sistemas de alto tráfico: es necesario planificar una política de purga mediante `DBMS_AUDIT_MGMT`.
