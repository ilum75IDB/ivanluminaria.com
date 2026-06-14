---
title: "Data Catalog"
description: "Inventario centralizado de activos de datos con metadatos, lineage y búsqueda integrada: hace la gobernanza accesible sin intervención técnica."
translationKey: "glossary_data_catalog"
aka: "Catálogo de Datos Empresarial"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Un Data Catalog es el inventario organizado de todos los activos de datos disponibles en una organización: tablas, vistas, datasets, informes, APIs, archivos. Cada activo incluye metadatos técnicos y de negocio, lineage, clasificaciones de calidad y un glosario compartido. El objetivo es que los datos sean localizables y comprensibles sin necesidad de abrir un ticket al equipo técnico ante cada consulta.

## Cómo funciona

El catalog recopila metadatos de fuentes heterogéneas mediante conectores (bases de datos relacionales, data lakes, herramientas BI, pipelines ETL). Para cada activo expone:

- **metadatos técnicos**: esquema, tipo de dato, cardinalidad, frecuencia de actualización
- **metadatos de negocio**: propietario, descripción en lenguaje natural, etiquetas de dominio
- **lineage**: grafo que muestra el origen de un dato y dónde se consume
- **data quality score**: métricas agregadas calculadas por los procesos de validación upstream

Los usuarios buscan activos mediante búsqueda full-text o navegación por dominio y etiquetas. Los data stewards enriquecen las entradas con anotaciones y aprobaciones.

## Cuándo se usa

El Data Catalog se vuelve necesario cuando el número de fuentes supera la capacidad de documentación manual — habitualmente a partir de 20-30 datasets activos — o cuando el cumplimiento normativo exige trazabilidad end-to-end (GDPR, HIPAA, SOX). También es el punto de entrada natural para los data contracts: el catalog expone las especificaciones de un dataset, mientras el contrato formaliza las garantías de calidad y los SLA.

Sin catalog, la gobernanza queda reducida a un documento Word raramente actualizado; con él, se convierte en un sistema vivo consultable por cualquier usuario con acceso.
