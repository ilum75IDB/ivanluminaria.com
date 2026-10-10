---
categories:
- project-management
date: '2026-10-13'
description: Un incident que se cierra sin causa reconstruida no es un episodio aislado.
  Cómo leer AWR, ASH y change log en frío antes de que llegue el segundo fallo.
draft: false
image: il-restart-ha-risolto-il-problema-e-ancora-li.cover.jpg
seoTitle: 'Incident cerrado sin causa: el problema sigue ahí'
tags:
- incident-management
- post-mortem
- database
- observability
- reliability
title: El reinicio lo resolvió. El problema sigue ahí.
translationKey: il_restart_ha_risolto_il_problema_e_ancora_li
webo_generated_at: 2026-10-10
webo_status: scheduled
---

# El reinicio lo resolvió. El problema sigue ahí.

*Por qué un incident que se cierra sin una cadena causal reconstruida no es un episodio aislado — y qué queda realmente en el sistema para analizar en frío.*

---
## Viernes, 19:40

Hay un momento que un CIO conoce bien, y que no aparece en los informes. El incident empezó el jueves por la noche a las 02:17 — una ralentización en un servicio crítico, latencias fuera de umbral, algunas sesiones en timeout, pocos clientes afectados. El equipo de guardia se conectó, observó durante cuarenta minutos, tomó algunas trazas, no entendió nada. A las 03:11 la curva volvió a la normalidad. Sola. El equipo esperó otros treinta minutos por precaución, vio el sistema estabilizarse y cerró el puente. Por la mañana, el daily stand-up lo mencionó tres minutos: *«ha vuelto a la normalidad, lo seguimos de cerca»*. Por la tarde del viernes, con tres reuniones de negocio en la agenda, nadie volvió a hablar del tema.

A las 19:40 el CIO sale de la oficina. El sistema aguanta. Empieza el fin de semana. El incident entra, sin que nadie haya decidido ponerlo ahí, en la categoría mental **«episodio ocasional»**. No es una decisión formal — es una decisión por omisión: nadie escribe, nadie pregunta, el hilo de Slack dedicado deja de actualizarse, no se convoca el post-mortem. El lunes por la mañana el sistema aguanta. El martes también. Al final de la semana siguiente, en el debrief operativo, el tema ya no aparece ni como una línea.

El momento en que se pierde la ventana de reconstrucción no es el momento del incident. **Es el viernes por la noche.** No cuando se rompió, sino cuando se dejó de mirar.

## Lo que el sistema todavía tiene, aunque nadie haya ido a verlo

Existe una convicción extendida, casi una obviedad del oficio, que reza: *«una vez resuelto el incident, sin los logs del momento, ya no se puede reconstruir la causa»*. Es cierta en un único caso — cuando *ninguna* traza ha sido conservada. En casi todos los demás, el sistema tiene más memoria de la que quienes lo operan creen, y la ventana de investigación es mucho más larga de lo que las dinámicas de urgencia sugieren.

En una base de datos Oracle, el **AWR** (Automatic Workload Repository) conserva snapshots cada hora, con una retención por defecto de ocho días y configurable hasta cinco semanas. Dentro de cada snapshot están los wait events dominantes, los planes de ejecución de las queries más costosas, las estadísticas de I/O, las sesiones activas, los segmentos más disputados. El **ASH** (Active Session History) conserva una muestra de las sesiones activas por segundo, en forma circular, utilizable a posteriori para reconstruir *qué estaba haciendo exactamente* cada sesión en el minuto del incident. El **alert log** registra errores, locks y cambios de estado. El sistema operativo conserva métricas de CPU, memoria e I/O. El almacenamiento conserva patrones de latencia y queue depth. El **repositorio de cambios** — si existe, y debería existir siempre — registra cada modificación de configuración, cada release de aplicación, cada parche de infraestructura. La observabilidad moderna, tratada en otro artículo de esta serie, conserva series temporales de semanas o meses.

Reunir estas fuentes setenta y dos horas después requiere método — pero es una reconstrucción *más precisa*, no menos, que la realizada en caliente en plena emergencia. **En caliente se busca para detener el síntoma. En frío se lee para entender la cadena.** Son dos actos distintos, con propósitos distintos; el segundo se ve dificultado por la presión del primero, no por el paso del tiempo.

## Un caso, y lo que ocurrió tres semanas después

Un entorno bancario, servicio de autorización de pagos sobre Oracle en alta disponibilidad, carga de pico en torno a 1.400 transacciones por segundo en las franjas comerciales. Un sábado por la tarde, durante cuarenta y dos minutos, la latencia media del servicio subió de 180 ms a más de 2 segundos, con una fracción de transacciones en timeout. El monitoring alertó, el equipo de guardia se conectó, vio un *enqueue wait* dominante sobre una tabla de sesión de usuario. Antes de que se decidiera una contramedida, la curva volvió a la normalidad. En cuarenta y dos minutos el sistema estaba de nuevo dentro de umbral.

El post-mortem fue breve. La hipótesis de trabajo, formulada sin evidencias sólidas, fue *«un patrón de carga anómalo del sábado por la tarde, quizás relacionado con una campaña comercial»*. El equipo cerró el ticket, el fin de semana continuó, el lunes el sistema aguantaba. (Los números — carga, latencias, tiempos — son representativos de contextos similares; los detalles del caso específico están anonimizados por confidencialidad contractual.)

Tres semanas después, la misma combinación de eventos se repitió — esta vez un jueves por la noche, en plena ventana operativa, con un volumen de transacciones doble respecto al sábado anterior. El sistema no volvió a la normalidad por sí solo. El downtime duró dos horas y diez minutos. El board pidió una reconstrucción.

En ese momento, con la urgencia del segundo incident, se hizo el análisis que no se había hecho en frío tres semanas antes. El AWR del sábado tenía, en dos snapshots consecutivos, un cambio neto en el plan de ejecución de una query crítica — efecto de un recálculo de estadísticas automático activado cuando la tabla había superado un cierto umbral de crecimiento. El ASH mostraba la secuencia de sesiones que habían quedado en espera sobre esa query, con el contador de waiters que había subido progresivamente hasta el punto de desencadenar la escalada sobre el recurso interno de la base de datos. El registro de cambios mostraba que una nueva release de la aplicación, cuatro días antes del incident del sábado, había introducido una llamada adicional a esa query cada vez que un usuario abría una sesión — llamada que se volvía crítica solo cuando el volumen de apertura de sesión superaba cierta concurrencia.

Todo esto ya estaba en el sistema el sábado por la tarde. El hilo entre crecimiento de la tabla, recálculo de estadísticas, cambio de plan, nueva release y aumento de concurrencia no era *inferible a partir de los síntomas registrados*. Era *legible* para quien hubiera reunido las fuentes con un modelo causal en mente — incluso dos semanas después. La diferencia no fue de datos disponibles. **Fue de decisión de mirar.**

## El TIA es un predictor, no un episodio

En cardiología y neurología preventiva existe un concepto que vale la pena tener presente cuando se piensa en los incidents que se resuelven solos. Se llama **TIA — Ataque Isquémico Transitorio**. Es un evento neurológico que se manifiesta como un ictus — dificultades de habla, debilidad en un miembro, visión borrosa — y **remite espontáneamente en cuestión de minutos u horas**, sin secuelas permanentes. El paciente en urgencias, si llega, es dado de alta con pruebas dentro de la normalidad y la recomendación de controlar la tensión.

Quien conoce los números sabe que un TIA es uno de los **predictores más fuertes de ictus mayor en los noventa días siguientes**. La literatura especializada indica que aproximadamente uno de cada diez pacientes tendrá un ictus clínico en los tres meses posteriores al TIA, y la mitad de ellos en las primeras cuarenta y ocho horas — si no se reconstruye el mecanismo y no se establece la prevención. El TIA no es un episodio aislado: es el sistema que ha mostrado una vez, de forma reversible, cómo fallará de forma no reversible si nadie actúa sobre la causa. (Números de referencia epidemiológicos — *VERIFICAR* con guías ESO/AHA actualizadas para la cita pública.)

Un incident que se resuelve solo tiene la misma naturaleza. El sistema ha mostrado, de forma reversible, un mecanismo que — si la causa no se elimina — se manifestará de nuevo. No necesariamente en el mismo punto, no necesariamente con la misma carga, no necesariamente en el sábado por la tarde de baja presión comercial. **El segundo incident elige el peor momento con precisión estadística**: porque la causa no eliminada sigue actuando, y porque la carga operativa crece hasta que encuentra la ventana adecuada.

El TIA y el incident resuelto comparten también una segunda característica, más incómoda. Ambos **inducen alivio**. El paciente dado de alta con pruebas normales piensa que se ha librado, no que ha recibido un aviso. El equipo que ve la curva volver a la normalidad piensa que el sistema ha aguantado, no que el sistema ha hablado. El alivio no es una reacción equivocada — es humana, legítima, necesaria después de las horas de tensión. **El momento en que el alivio se convierte en un riesgo es aquel en que cierra la ventana de investigación antes de que la investigación haya sido siquiera abierta.**

## Las preguntas que preceden al cierre del ticket

Ninguna de estas preguntas pretende convencer a nadie de convertir cada incident en un proyecto de seis semanas. Todas sirven para decidir **si un rientro espontáneo cierra el caso o lo abre**, antes de que se cierre por omisión.

**1. ¿La causa que explicaría tanto el inicio como la resolución espontánea ha sido articulada, o estamos explicando solo el síntoma?**
Un incident que empieza porque «hubo un patrón de carga anómalo» no explica la resolución: la carga anómala no se apagó sola en exactamente cuarenta y dos minutos. Si no hay un modelo causal que dé cuenta *de ambos extremos* del intervalo, la investigación no ha cerrado — simplemente ha dejado de hacer preguntas.

**2. ¿Qué fuente conserva todavía trazas del incident, y durante cuánto tiempo?**
AWR, ASH, alert log, logs de OS, métricas de almacenamiento, change log, telemetría de aplicación. Cada una tiene una retención diferente. Mapear la ventana residual de investigación antes de decidir si investigar cuesta treinta minutos y desplaza la decisión del plano emocional (*«ahora estamos cansados»*) al plano operativo (*«tenemos trece días»*).

**3. Si el mismo mecanismo se repitiera con el doble de carga, ¿el sistema aguantaría igualmente?**
Es la pregunta que un cardiólogo experto formula tras un TIA. El sistema aguantó una vez en condiciones favorables — baja presión comercial, ventana de descarga, concurrencia limitada. La pregunta no es *«¿volverá?»*. Es *«cuando vuelva, ¿volverá en condiciones que el sistema pueda absorber todavía?»*. Si la respuesta es *«no lo sabemos»*, el episodio no es ocasional: es una señal aún no leída.

**4. ¿Quién tendría la autoridad para convocar una reconstrucción en frío, y con qué ventana temporal?**
A menudo la investigación post-resolución no se abre no por decisión, sino por ausencia de propietario. El equipo operativo ha pasado al siguiente ticket, el arquitecto no tiene mandato explícito, la dirección ha visto el sistema estable. **Nombrar al propietario de la reconstrucción en frío antes del siguiente incident** es la intervención organizativa más infravalorada — y la más económica — de toda la gobernanza de la resiliencia.

## El valor de mirar cuando la urgencia ha pasado

Hay una paradoja que vale la pena explicitar, porque invierte una intuición común. **La reconstrucción en frío es más precisa, no menos, que la realizada en caliente** — cuando las fuentes están conservadas. En caliente se busca con la ansiedad de detener el síntoma, con el board pidiendo actualizaciones cada diez minutos, con las hipótesis que se atropellan. En frío se lee con tiempo para comparar fuentes distintas, verificar correlaciones, descartar pistas que en caliente parecían relevantes y que en frío resultan ser coincidencias.

Quien ha hecho muchas reconstrucciones *post-resolución* sabe también una segunda cosa: **la cadena causal que emerge casi nunca es la sospechada durante la tarde del incident**. La hipótesis del *«patrón de carga anómalo»* es plausible en caliente, donde todo lo que se ha visto es una curva anómala. Se vuelve evidentemente parcial en frío, cuando entran en juego el change log de la semana anterior, el crecimiento de la tabla, el recálculo de estadísticas, la nueva release de la aplicación.

El coste organizativo de una reconstrucción en frío — tres o cinco jornadas de tiempo de personas expertas, con el sistema ya estable y sin ninguna urgencia encima — es una fracción del coste del segundo incident, en jornadas de downtime, reuniones de board, conversaciones con clientes, renegociaciones de SLA. La comparación, para un CFO, se hace en veinte segundos. La resistencia, cuando existe, raramente es de presupuesto: es de **atención**. La organización que acaba de exhalar el suspiro de alivio está fisiológicamente poco dispuesta a convertir ese suspiro en un nuevo ciclo de análisis. Es precisamente por eso que, en muchos contextos, conviene que quien convoque la reconstrucción sea **una figura externa a la operativa** — que no ha vivido las cuarenta y dos horas de tensión y que puede proponer, con calma, mirar cuando mirar cuesta menos.

## Una pregunta para llevarse

No hay una regla universal sobre los incidents que se resuelven solos. Hay, para cada organización que gestiona incidents críticos, una pregunta que vale la pena hacerse la próxima vez que la curva vuelva a la normalidad sin intervención:

*«¿El mecanismo que explica cómo empezó explica también cómo terminó — o estamos explicando solo el hecho de que terminó?»*

Si la respuesta tiene alguna vacilación, el episodio no es todavía ocasional. Es un sistema que ha hablado una vez. La segunda vez elegirá el momento en que hablar cueste más.

## Glosario
**[AWR](/es/glossary/awr/)** — Automatic Workload Repository — herramienta de diagnostico integrada en Oracle Database para la recopilacion y analisis de estadisticas de rendimiento.

**[ASH](/es/glossary/ash/)** — Active Session History — componente Oracle que registra el estado de cada sesion activa una vez por segundo...

**[wait event](/es/glossary/wait-event/)** — Evento de espera registrado por Oracle cada vez que una sesion no puede continuar y debe esperar un recurso — I/O, lock, red o CPU.

**[piano di esecuzione](/es/glossary/piano-di-esecuzione/)** — Secuencia de operaciones elegida por el optimizador SQL para ejecutar una consulta: escaneos, joins, ordenaciones. Las estadísticas obsoletas lo degradan en silencio.

**[TIA](/es/glossary/tia/)**
