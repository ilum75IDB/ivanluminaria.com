---
title: "DEFERRABLE constraint"
description: "Restricción de integridad cuya verificación puede posponerse al COMMIT en lugar de ejecutarse tras cada instrucción DML. Útil en transacciones multi-paso."
translationKey: "glossary_deferrable_constraint"
aka: "restricción diferible"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un DEFERRABLE constraint es una restricción de integridad referencial o de dominio cuya comprobación puede posponerse hasta el momento del COMMIT, en lugar de ejecutarse inmediatamente tras cada instrucción DML. Esto permite que una transacción atraviese estados intermedios temporalmente inconsistentes, siempre que la consistencia quede restaurada antes de cerrar la transacción.

## Cómo funciona

Una restricción declarada `DEFERRABLE` puede operar en dos modos:

- `INITIALLY IMMEDIATE` — verificada tras cada DML por defecto; puede diferirse explícitamente con `SET CONSTRAINT`.
- `INITIALLY DEFERRED` — diferida al COMMIT por defecto.

```sql
ALTER TABLE pedidos
  ADD CONSTRAINT fk_cliente
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
  DEFERRABLE INITIALLY DEFERRED;

-- Dentro de la transacción:
SET CONSTRAINT fk_cliente DEFERRED;
INSERT INTO pedidos (id, cliente_id) VALUES (1, 999); -- el cliente 999 aún no existe
INSERT INTO clientes (id) VALUES (999);               -- ahora sí existe
COMMIT;                                               -- verificación superada
```

## Cuándo se usa

El caso de uso más habitual es la carga de datos con dependencias circulares o la inserción de filas vinculadas por claves foráneas en un orden no determinista. También es frecuente en pipelines de replicación y procesos ETL donde el orden de llegada de los registros no está garantizado.

**Limitación fundamental**: un DEFERRABLE constraint no es una Assertion. Actúa sobre filas individuales o relaciones entre tablas ya definidas en el esquema, pero no puede expresar predicados arbitrarios entre tablas como `CHECK (SELECT COUNT(*) FROM ...)`. Para ese nivel de expresividad, Oracle 23ai introduce las SQL Assertions nativas.
