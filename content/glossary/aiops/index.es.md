---
title: "AIOps"
description: "AIOps aplica IA y machine learning a las operaciones de TI para detectar anomalías y correlaciones en logs y métricas, sin reconstruir automáticamente la cadena causal."
translationKey: "glossary_aiops"
aka: "Artificial Intelligence for IT Operations"
articles:
  - "/posts/oracle/ai-mostra-sintomo-board-chiede-causa"
---

AIOps (Artificial Intelligence for IT Operations) es la aplicación de algoritmos de machine learning y análisis estadístico a los datos operativos de un sistema de TI: métricas de rendimiento, logs de aplicaciones, eventos de infraestructura. El objetivo es reducir el ruido de las alertas y hacer visibles patrones anómalos que un operador humano difícilmente detectaría de forma manual en volúmenes elevados de datos.

## Cómo funciona

Una plataforma AIOps ingiere flujos continuos de datos — métricas de CPU, query time, error rate, logs estructurados — y aplica modelos de detección de anomalías, típicamente basados en clustering, series temporales o redes neuronales, para identificar desviaciones respecto a la baseline. Cuando dos anomalías se solapan temporalmente, el sistema las correlaciona y las presenta como un único evento agregado.

El resultado es una alerta enriquecida: en lugar de recibir cincuenta notificaciones separadas, el equipo recibe un único incident con las señales correlacionadas y una ventana temporal común.

## Límites operativos

La correlación temporal no equivale a causalidad. AIOps puede señalar que un pico de latencia en Oracle coincide con un aumento de I/O en almacenamiento, pero no determina automáticamente cuál es la causa y cuál el efecto — ni identifica la root cause de origen (por ejemplo, una query no optimizada, un lock contention o un batch nocturno fuera de control).

En un incident complejo, reconstruir la cadena causal sigue requiriendo la intervención de un DBA o de un ingeniero con contexto sobre la aplicación. AIOps reduce el tiempo de triage, no lo elimina.
