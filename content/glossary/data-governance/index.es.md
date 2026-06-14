---
title: "Data Governance"
description: "Marco operativo continuo de procesos, políticas y estándares que garantizan la calidad, integridad, seguridad y cumplimiento normativo de los datos organizacionales."
translationKey: "glossary_data_governance"
aka: "Gobierno del dato"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

La Data Governance es el conjunto estructurado de procesos, políticas, estándares y métricas que regulan cómo una organización gestiona sus activos de datos. No es un proyecto con fecha de entrega: es un framework operativo continuo que abarca personas, tecnología y procesos.

## Cómo funciona

Un programa de Data Governance establece la propiedad del dato (quién es responsable de cada conjunto de datos), esquemas de clasificación, reglas de calidad y controles de acceso. Las herramientas operativas habituales incluyen un data catalog, trazabilidad de datos (data lineage), políticas de retención y controles de calidad automatizados integrados en los pipelines ETL/ELT.

En el contexto de un Data Warehouse, la governance se aplica en cada capa: desde la staging zone hasta los marts expuestos a los usuarios finales. Un control de calidad típico puede rechazar registros con valores nulos en columnas críticas o generar alertas cuando las distribuciones estadísticas de los KPI se desvían de los umbrales definidos.

## Contexto operativo

La Data Governance se vuelve innegociable cuando aplican normativas como GDPR, HIPAA o PCI-DSS: la trazabilidad completa de quién creó, modificó o consumió un dato debe ser demostrable en una auditoría. La gestión de la deuda de calidad del dato es igualmente relevante: sin governance, los problemas de calidad se acumulan silenciosamente hasta comprometer decisiones de negocio críticas.

El principal trade-off es entre rigor y velocidad: procesos de governance demasiado pesados ralentizan a los equipos de ingeniería. El enfoque práctico consiste en calibrar los controles según el perfil de riesgo real de cada dataset, en lugar de aplicar el mismo nivel de escrutinio a todas las tablas.
