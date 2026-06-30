---
title: "De rivales a co-autores: cómo Booch, Rumbaugh y Jacobson inventaron UML (y lo que queda hoy)"
seoTitle: "Three Amigos, UML y RUP: la historia y lo que queda hoy"
description: "La historia de los Three Amigos de UML y RUP: cómo Booch, Rumbaugh y Jacobson, de rivales, unificaron el object-oriented modeling. Y lo que queda hoy."
date: "2026-06-30T08:03:00+01:00"
draft: false
translationKey: "da_rivali_a_co_autori_uml_rup"
tags: ["methodology"]
categories: ["project-management"]
image: "da-rivali-a-co-autori-uml-rup.cover.jpg"
---

El otro día, en un aula de formación interna de un cliente del sector asegurador, abrí un documento de proyecto del 2003 para mostrar un ejemplo de arquitectura aplicativa. Diagramas UML, fases RUP con sus puntos coloreados, use cases esquemáticos, secuencias de interacción entre actores y sistemas. Una colega más joven de algunos años se acercó a la pizarra y me preguntó, sin rodeos: *"¿Qué son estas siglas? Las he visto en algún curso pero nunca las he entendido realmente."*

La pregunta me hizo sonreír — no porque fuera extraña, sino porque era la misma que habría hecho yo veinte años atrás si alguien me hubiera puesto delante ese póster. **UML y RUP son dos siglas que hicieron época**, y que hoy viven una doble vida: marginales en la conversación actual sobre project management, pero todavía vivas en nichos precisos donde el rigor documental es obligatorio. Y detrás de esas siglas se esconde una de las historias más curiosas de la ingeniería del software de los últimos treinta años — la historia de **tres rivales que eligieron estar en la misma habitación**.

Vale la pena contarla.

---

## Los años '90: tres tribus, tres vocabularios

Para entender UML hay que dar un paso atrás hasta finales de los años '80, cuando el object-oriented se estaba volviendo el paradigma dominante de programación. Pero había un problema: cada grupo de investigación y cada empresa de tooling había inventado **su propio modo de representar visualmente las clases, las relaciones, los objetos**. Y los tres enfoques principales, cada uno con su profeta, se miraban de reojo.

**Grady Booch**, americano, trabajaba desde mediados de los años '80 en **Rational Software** (la misma empresa fundada por Mike Devlin y Paul Levy en 1981). Había publicado el *Booch Method* a principios de los años '90: una notación muy rica en símbolos — nubes, flechas, etiquetas — que se volvía difícil de dibujar a mano pero extraordinariamente expresiva cuando estaba soportada por una herramienta gráfica. Estaba pensada para developers.

**James Rumbaugh**, americano también, trabajaba en los laboratorios de investigación de **General Electric**. En 1991 publicó *Object Modeling Technique* (OMT), un enfoque más seco y más orientado al modeling de los datos que a la representación del comportamiento. Funcionaba bien en contextos donde el database era el centro del sistema. Estaba pensado para arquitectos.

**Ivar Jacobson**, sueco, había trabajado en **Ericsson** antes de fundar su propia empresa, *Objectory AB*. Su contribución original era el concepto de **use case**: describir el sistema desde el punto de vista del actor que lo usa, no del objeto que lo compone. Estaba pensado para quien hablaba con el negocio.

Tres tribus, tres vocabularios, **tres simbologías diferentes para dibujar la misma clase**. Conferencias separadas, libros concurrentes, customers que tenían que elegir qué tribu seguir. La competición, en las palabras de quien vivió ese período, era a veces feroz — había informes técnicos de un campo que criticaban abiertamente las elecciones de los otros dos. Nada personal, pero tres community que se miraban desde el otro lado del río.

---

## El punto de inflexión: octubre de 1994

A mediados de 1994, Rational Software hace el movimiento que cambia todo. Mike Devlin, el CEO, ha entendido que la fragmentación se está volviendo un freno para la adopción enterprise del object-oriented — y que ninguno de los tres métodos ganará nunca solo. Decide entonces **juntar a los protagonistas**.

En octubre de 1994, **James Rumbaugh deja General Electric y se traslada a Rational**. La noticia hace ruido: dos de los tres profetas del object-oriented modeling ahora trabajan en la misma empresa. Booch y Rumbaugh, que hasta el día anterior firmaban artículos que se respondían mutuamente en las revistas especializadas, ahora tienen las oficinas en el mismo pasillo.

Un año después, en 1995, Rational adquiere **Objectory AB**, e **Ivar Jacobson** se une al grupo. Está hecho: los tres hombres que habían dominado el debate sobre el object-oriented durante cinco años están en la misma empresa. La prensa especializada, con una mezcla de curiosidad e ironía, los bautiza **los Three Amigos** — no sin un toque de escepticismo: ¿realmente tres personas tan diferentes lograrán trabajar juntas?

Los tres, entrevistados años después, contaron los comienzos sin énfasis. *"Durante los primeros meses cada uno defendía su propia notación. Después, gradualmente, entendimos que ninguno de los tres enfoques, solo, era suficiente. Y era obvio que el mercado no toleraría para siempre tres estándares concurrentes."*

---

## UML, noviembre de 1997

Entre 1995 y 1997 los Three Amigos trabajan en la fusión de los tres métodos. Booch aporta la riqueza simbólica para el modeling estructural, Rumbaugh aporta la disciplina del modeling de los datos y de los estados, Jacobson aporta los use case como puente hacia el negocio. Nace así **UML — Unified Modeling Language**.

El camino de estandarización pasa a través de **OMG (Object Management Group)** [1], el consorcio no-profit que ya administraba otros estándares del mundo object-oriented (como CORBA). UML 1.0 se somete a OMG en enero de 1997; **UML 1.1 se adopta como estándar formal OMG en noviembre de 1997**.

En esa primera versión UML ofrecía **nueve tipos de diagramas** organizados en dos familias: **estructurales** (class diagram, object diagram, component diagram, deployment diagram) para describir la estructura estática, y **comportamentales** (use case, sequence, collaboration, statechart, activity) para describir el comportamiento dinámico. Desde entonces la especificación ha crecido — UML 2.5 (la actual) tiene trece tipos de diagramas — pero el núcleo ha permanecido.

Un estándar se mide no por quien lo crea, sino por quien lo usa. Y **UML fue adoptado rápidamente** — en los tres años sucesivos se convirtió en el lenguaje de documentación arquitectural dominante en banca, telco, administración pública y aseguradoras, donde los pliegos enterprise lo requerían explícitamente en sus especificaciones.

---

## RUP, 1998: el proceso enterprise

UML era el **lenguaje**, pero hacía falta un **proceso** que dijera cómo usarlo. Rational Software responde en 1998 con **RUP — Rational Unified Process** [2]. Un método de desarrollo software iterativo, basado en las contribuciones previas de Booch y Jacobson, organizado en **cuatro fases secuenciales con iteraciones internas** en cada fase:

- **Inception** — visión, business case, scope
- **Elaboration** — arquitectura, requisitos detallados, mitigación de los riesgos
- **Construction** — implementación iterativa
- **Transition** — deploy, beta, rollout

A diferencia del *waterfall* clásico, RUP era **iterativo**: no se terminaba una fase antes de empezar la siguiente, sino que se volvía atrás varias veces. A diferencia de los métodos *lightweight* que llegarían pocos años después, sin embargo, era **heavyweight** — un proyecto RUP enterprise típico preveía seis meses de Elaboration antes de escribir una línea de código de producción. Documentos formales, artefactos rastreados, milestone documentadas, auditorías posibles.

Era la respuesta correcta para el contexto en el que había nacido. En los años 1998-2005, RUP fue adoptado masivamente en banca europea, en administración pública, en sistemas de telecomunicaciones. **IBM adquiere Rational en 2003** por 2.100 millones de dólares — una operación que valía, de hecho, RUP como activo estratégico tanto como UML.

---

## Febrero de 2001: el Manifiesto Ágil cambia el viento

Mientras RUP alcanzaba su pico de adopción, **al otro lado del río** estaba naciendo algo completamente diferente. Entre el 11 y el 13 de febrero de 2001, **diecisiete desarrolladores se reúnen en una estación de esquí de Utah** — Snowbird — y firman un póster de pocas líneas que se convertiría en el **Manifiesto Ágil** [3].

Cuatro pares de valores, cada uno en su forma original "X over Y" (con la traducción al español a continuación):

- *Individuals and interactions over processes and tools* — Individuos e interacciones sobre procesos y herramientas
- *Working software over comprehensive documentation* — Software funcionando sobre documentación exhaustiva
- *Customer collaboration over contract negotiation* — Colaboración con el cliente sobre negociación contractual
- *Responding to change over following a plan* — Respuesta al cambio sobre seguir un plan

Era exactamente lo contrario de RUP. Donde RUP ponía los procesos en el centro, Agile ponía las personas. Donde RUP pedía seis meses de documentos antes del código, Agile pedía código funcionando cada dos semanas. Donde RUP formalizaba los contratos, Agile pedía conversaciones continuas con el cliente.

Ninguno de los diecisiete firmantes, vale la pena decirlo, atacaba explícitamente a RUP. El Manifiesto no menciona ningún método concurrente. Pero el mensaje era claro, y en los diez años sucesivos el viento cambió. **Scrum**, **XP** (Extreme Programming), **Kanban** se convirtieron en el vocabulario estándar del team de desarrollo. RUP, en muchos contextos, dejó de proponerse en los nuevos proyectos.

Merece la pena mencionar que muchas ideas del Agile **no nacieron de cero**. Las **user story** son use case despojados del formalismo de Jacobson, los **sprint** breves son las Elaboration de RUP acortadas, e incluso la ceremonia BDD llamada *"Three Amigos meeting"* — desarrollador, tester y business analyst que discuten juntos una user story antes de empezarla — es un homenaje explícito al grupo de Booch, Rumbaugh y Jacobson. El Agile no tanto contradijo UML, **más bien liberó sus ideas del peso del proceso**. Es material que merece un artículo aparte, en el futuro.

No está muerto. Pero el viento cambió.

---

## Lo que queda hoy, veinte años después

Veinte años después del Manifiesto Ágil, ¿dónde nos encontramos?

**UML está todavía vivo**, pero de un modo diferente del que pensaban los Three Amigos. Ya no es el lenguaje universal para describir la arquitectura de un sistema — ese rol ha sido tomado a menudo por diagramas más libres, por architecture decision records (ADR) en markdown, por dibujos en Mermaid o draw.io que no respetan la sintaxis UML formal pero llevan su espíritu. **UML como notación formal sobrevive** en los pliegos de la administración pública, en los proyectos de certificación ISO, y en los contextos académicos donde enseñar object-oriented modeling sigue siendo parte del currículo.

**RUP, en cambio, ha encontrado su nicho** — y es un nicho de todo menos marginal. Sobrevive vivito y coleando en los sectores donde el **rigor documental es obligatorio por ley o por auditoría**:

- **Aviación y aeroespacial** — sistemas aviónicos certificados DO-178C, donde cada requisito debe ser rastreado desde la recogida hasta el test
- **Médico** — dispositivos bajo IEC 62304, donde el proceso de desarrollo software se certifica junto al producto
- **Patentes y R&D farmacéutico** — donde la trazabilidad del proceso de innovación tiene valor legal
- **Banca crítica** — sistemas core de pago donde la documentación formal es parte del contrato regulatorio

En estos contextos, **un método ágil puro no pasa la auditoría**. Hace falta poder demostrar a un auditor externo, años después del release, por qué se hizo una determinada elección arquitectural y qué alternativas se habían considerado. RUP — o un descendiente suyo directo — es todavía el modo estándar de hacerlo.

Para el resto, **Scrum y Kanban dominan**. Las [stand-up diarias de 15 minutos](/es/posts/project-management/standup-meeting-15-minuti/) que conté en otro artículo son el ritual Agile por excelencia, y no existirían si en 2001 esos diecisiete en Utah no hubieran firmado ese póster.

---

## La lección que me llevo de los Three Amigos

La lección que me queda de esta historia — la que intenté explicar a la colega delante de la pizarra, ese día — no es UML, y no es RUP.

Es que **tres personas que hacían la misma cosa de modo competitivo decidieron, en un cierto punto, estar en la misma habitación**. Dejaron de publicar artículos que se respondían mutuamente, dejaron de defender cada detalle de su propia notación, y buscaron el trozo de valor común. No fue indoloro — hicieron falta dos años de confrontaciones dentro de Rational antes de que UML 1.0 estuviera listo. Pero sucedió.

Y es una lección que vale, en el project management de hoy, mucho más que cualquier detalle sintáctico de UML. Cuando un team de desarrollo se divide en facciones que defienden cada una su framework preferido — Scrum vs Kanban, microservicios vs monolito, REST vs GraphQL — la lección de los Three Amigos es que el valor de un método no se mide en su superioridad teórica, sino en su **capacidad de estar en la misma habitación con otros métodos diferentes** y producir algo nuevo.

No hay un método superior. Hay contextos diferentes, y métodos adecuados a contextos diferentes. UML y RUP son adecuados donde el rigor documental es obligatorio. Scrum y Kanban son adecuados donde la velocidad de iteración es obligatoria. Ambos sobreviven, lado a lado, porque ambos sirven.

Y las historias como la de los Three Amigos sirven para recordárnoslo, de vez en cuando.

---

## Fuentes oficiales

1. Object Management Group — [Unified Modeling Language (UML) specification](https://www.omg.org/spec/UML/)
2. Rational Unified Process — [overview y fases (IBM/Rational documentation archive)](https://www.ibm.com/docs/en/rational-soft-arch/9.7.0?topic=overview-rational-unified-process)
3. Beck, Beedle, van Bennekum et al. — [Manifesto for Agile Software Development (febrero 2001)](https://agilemanifesto.org/)

---

## Glosario

- **[Three Amigos](/es/glossary/three-amigos/)** — Apodo dado por la prensa especializada a Grady Booch, James Rumbaugh e Ivar Jacobson, los tres creadores de UML que trabajaban en Rational Software entre 1994 y 1998. De rivales se convirtieron en co-autores de un estándar unificado.
- **[UML](/es/glossary/uml/)** — Unified Modeling Language. Lenguaje estándar de modelado object-oriented, adoptado por OMG en noviembre de 1997 a partir de la fusión de tres métodos previos (Booch Method, OMT, Objectory). Incluye diagramas estructurales y comportamentales.
- **[RUP](/es/glossary/rup/)** — Rational Unified Process. Método de desarrollo software iterativo liberado por Rational en 1998, organizado en cuatro fases (Inception, Elaboration, Construction, Transition). Heavyweight y documento-intensivo, hoy vive en nichos regulados (aviación, médico, banca crítica).
- **[Use Case](/es/glossary/use-case/)** — Técnica de análisis de requisitos introducida por Ivar Jacobson que describe el sistema desde el punto de vista del actor que lo usa, no de los objetos que lo componen. Uno de los tres pilares que alimentaron UML.
- **[Manifiesto Ágil](/es/glossary/agile-manifesto/)** — Documento de pocas líneas firmado en Snowbird, Utah, el 11-13 de febrero de 2001 por diecisiete desarrolladores. Cuatro pares de valores que desplazaron el foco del desarrollo software de las prácticas heavyweight (RUP-like) a las prácticas lightweight (Scrum, XP, Kanban).
