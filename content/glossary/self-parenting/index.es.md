---
title: "Self-parenting"
description: "Técnica de balanceo de jerarquías desequilibradas: quien no tiene padre se convierte en padre de sí mismo."
translationKey: "glossary_self_parenting"
aka: "Auto-referencia jerárquica"
articles:
  - "/posts/data-warehouse/ragged-hierarchies"
---

El **self-parenting** es una técnica de dimensional modeling usada para balancear las jerarquías desequilibradas (ragged hierarchies). El principio es simple: una entidad que no tiene un nivel jerárquico superior se convierte en su propio padre a ese nivel.

## Cómo funciona

En una jerarquía de tres niveles Top Group → Group → Client:

- Un Client sin Group usa su propio nombre/ID como Group
- Un Group sin Top Group usa su propio nombre/ID como Top Group

El resultado es una tabla dimensional sin NULLs en las columnas jerárquicas, con todos los niveles siempre poblados.

## Los flags de distinción

Para no perder la información sobre qué entidades fueron balanceadas artificialmente, se agregan flags a la dimensión:

- `is_direct_client = 'Y'`: el cliente no tenía un Group en la fuente
- `is_standalone_group = 'Y'`: el Group no tenía un Top Group en la fuente

Estos flags permiten al negocio filtrar los "verdaderos" top groups de los clientes promovidos.

## Por qué en el ETL y no en el reporte

El self-parenting se aplica una vez en el ETL, no en cada reporte individual. Un reporte debería hacer GROUP BY y JOIN, no decidir cómo gestionar los niveles faltantes. Si la lógica de balanceo está en el modelo, todos los reportes se benefician automáticamente.
