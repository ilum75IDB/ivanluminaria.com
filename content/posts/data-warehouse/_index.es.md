---
title: "Data Warehouse"
date: "2026-03-10T08:03:00+01:00"
description: "Arquitectura Data Warehouse en la práctica: modelado dimensional, jerarquías, ETL y estrategias de carga. Cuando los datos no solo deben funcionar, sino servir para decidir."
image: "data-warehouse.cover.jpg"
layout: "list"
---

He visto data warehouses construidos con granularidad diaria porque "al negocio le basta así" — y volverse inútiles al día siguiente, cuando marketing pidió el análisis horario de las conversiones. He visto dimensiones de cliente sin historización, sobrescribiendo el código postal cada vez que alguien se mudaba — y reportes del año anterior que ya no cuadraban. He visto ETLs cargando 200 millones de filas en full cada noche porque nadie había tenido nunca el valor de rediseñar el delta.

Y he visto exactamente lo contrario: data marts pequeños, bien modelados, con el bus matrix bien dibujado — que responden a preguntas que nadie había pensado aún en hacer, sin tocar una sola línea de código.

La diferencia nunca ha sido la tecnología. Siempre ha sido **el modelo**.

------------------------------------------------------------------------

Un data warehouse no es una base de datos con tablas más grandes. Es **una forma distinta de pensar los datos** — orientada al análisis, a la historia, a las decisiones.

En las bases de datos transaccionales lo que cuenta es el *momento presente*: el pedido que estás insertando, el saldo actual, la fila que estás actualizando. En un data warehouse lo que cuenta es el *recorrido*: cómo era ese cliente hace seis meses, cómo ha cambiado el producto en el tiempo, qué versión del maestro era válida cuando se emitió ese contrato.

Casi siempre, el DWH que no aguanta se reconoce por estas cosas:

- **granularidad equivocada** en la tabla de hechos — demasiado gruesa pierdes detalle, demasiado fina lo ralentizas todo
- **dimensiones planas** sin gestión SCD — historia perdida, análisis "as-was" imposibles
- **jerarquías no balanceadas** que rompen las agregaciones en cuanto el negocio pide un drill-down
- **bus matrix nunca dibujado** — data marts que no se hablan, mismas entidades modeladas de forma distinta en cada departamento
- **ETLs diseñados como copia** en vez de como transformación — la suciedad del transaccional llegando intacta al análisis

Son problemas que en desarrollo no se ven. Explotan seis meses después, cuando el negocio pide reportes que el modelo no puede soportar.

------------------------------------------------------------------------

## 📊 Qué le pregunto al negocio antes de tocar el modelo

Antes incluso de dibujar una tabla de hechos, hay cinco preguntas que le hago al negocio. No son opcionales — son la diferencia entre un data warehouse que dura diez años y uno que hay que reescribir a los dos.

| Pregunta | Qué intento entender | Por qué es crítica |
|---|---|---|
| **¿A qué grano necesitas el dato?** | Diario, horario, transacción individual | Elegir siempre el grano mínimo útil — agregar luego se puede, desagregar no |
| **¿Cuánto atrás en el tiempo?** | Historia requerida, profundidad analítica | Define volúmenes, almacenamiento, estrategias de particionamiento y archivado |
| **¿Qué pasa cuando cambia un maestro?** | Cliente que se muda, producto que cambia de categoría | Determina el tipo de SCD (1, 2, 3, 6) para cada dimensión |
| **¿Qué jerarquías debe soportar?** | Drill-down, roll-up, caminos alternativos | Evita dimensiones ragged, snowflake injustificados, joins lentos en agregaciones |
| **¿Cuál es la latencia aceptable?** | Batch nocturno, intraday, near real-time | Lo cambia todo: ETL, modelo, infraestructura, coste |

Cinco preguntas. Veinte minutos de reunión. Semanas de reescrituras evitadas.

------------------------------------------------------------------------

## 📚 De qué hablo aquí

Historias reales de diseño y reestructuración de data warehouses en producción. Modelado dimensional (Kimball leído en serio, no por eslóganes), slowly changing dimensions, bus matrix, jerarquías, estrategias de carga incremental y rendimiento analítico.

Nada de recetas de manual. Solo soluciones aplicadas a sistemas reales — seguros, finance, administración pública, telco, postal — que sirven decisiones empresariales reales.

------------------------------------------------------------------------

Un data warehouse no se construye para contener datos.

Se construye para responder preguntas — y esas preguntas, inevitablemente, cambian.
