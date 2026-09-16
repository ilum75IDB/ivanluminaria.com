---
categories:
- project-management
date: '2026-09-22'
description: 'Un Commodore 64, un programa modificado para insultar al padre y una
  puerta cerrada con llave: cómo empieza una carrera de 30 años en ingeniería de bases
  de datos.'
draft: false
image: il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire.cover.jpg
seoTitle: 'De veterinario a DBA: 30 años de bases de datos desde un Commodore 64'
tags:
- career
- personal
- database-engineering
- origin-story
title: 'Un niño como tantos: de veterinario a ingeniero de bases de datos'
translationKey: il_dottore_tutto_pazzo_un_commodore_64_una_porta_chiusa_e_il_mestiere_di_capire
webo_generated_at: 2026-09-16
webo_status: scheduled
---

## Un niño como tantos

De niño, como tantos, quería ser veterinario. Me gustaban los animales y la naturaleza, y cuidarlos me parecía el trabajo más bonito del mundo.

Probablemente tú también, a esa edad, tenías una respuesta preparada para la pregunta «¿qué quieres ser de mayor?». Y probablemente la tuya también, en algún momento, tomó otro camino.

La mía lo tomó en 1983, cuando mi padre compró un Commodore 64.

## READY.

Si tienes más o menos mi edad, lo recuerdas: el ladrillo color avellana enchufado al televisor, las teclas que sonaban como una máquina de escribir, la pantalla azul con el borde celeste y el mensaje que toda una generación todavía sabe de memoria.

```text
    **** COMMODORE 64 BASIC V2 ****

 64K RAM SYSTEM  38911 BASIC BYTES FREE

READY.
```

Debajo, un cursor que parpadeaba esperando instrucciones.

Quien tenía el casete recuerda PRESS PLAY ON TAPE, las franjas de colores en el borde de la pantalla y la esperanza de que el juego arrancara al primer intento. Quien pasaba por el quiosco recuerda los casetes con diez juegos dentro y los títulos traducidos a un español de lo más peculiar. Estábamos todos en el mismo barco, y el barco cargaba en cinco minutos.

Mi padre, junto con el ordenador, tenía unos libros llenos de programas en BASIC para copiar. Páginas de líneas numeradas de diez en diez y, al final, cuando habías copiado bien, un juego. Cuando habías copiado mal, después de dos horas de tecleo, el Commodore te lo decía con una franqueza muy suya: `?SYNTAX ERROR IN 340`. La línea 340 era perfecta, idéntica al libro. La causa estaba en la 330, donde un punto y coma se había convertido en dos puntos. Sin saberlo, aprendía la primera regla de todo diagnóstico: el síntoma aparece en un sitio, la causa suele estar un poco más arriba.

La regla del juego era clara: el listado se copia idéntico, y el veterinario sigue siendo el plan para el futuro.

## El doctor chiflado

Uno de esos programas se llamaba «El doctor chiflado». Te hacía una serie de preguntas, una especie de anamnesis, y al final, según las respuestas, emitía un diagnóstico jocoso y divertido.

Un día, tendría unos diez años, estaba enfadado con mi padre. En lugar de dar un portazo, abrí el programa y lo modifiqué: cuando respondía él, el doctor concluía siempre que era «malo y antipático». El listado original no puedo mostrártelo; esto es una reconstrucción, para dar una idea:

```basic
500 REM EL DIAGNOSTICO
510 IF N$="PAPA'" THEN PRINT "ERES MALO Y ANTIPATICO": END
520 PRINT "TIENES UN ATAQUE AGUDO DE..."
```

El apóstrofo en lugar del acento es auténtico espíritu de la época: el Commodore no tenía letras acentuadas. El respeto, aquella tarde, también escaseaba en el código.

Mi padre no podía enfadarse, porque quien hablaba era el doctor. Una inmunidad diplomática perfecta, construida en BASIC por un niño que ni siquiera sabía lo que era la inmunidad diplomática. Y sobre todo estaba contento: había hecho algo que en el libro no estaba. Había entendido el programa de otra persona lo suficiente como para cambiarlo.

Desde ese día sus libros dejaron de ser páginas para copiar y se convirtieron en compañeros de viaje. Cada listado era un mecanismo que desmontar para entender cómo funcionaba.

## Se hace resolver los problemas en vez de estudiar

En la secundaria escribía programas propios. Resolvían problemas de geometría y álgebra: introducías los datos, y el programa desarrollaba y mostraba todos los pasos hasta el resultado.

La profesora no le veía el sentido, y tenía sus razones. Eran los primeros años en que los ordenadores entraban en los hogares, y para muchos adultos seguían siendo objetos misteriosos. Le dijo a mi padre que me quitara el ordenador, porque si no nunca aprendería matemáticas. Su comentario fue: «Se hace resolver los problemas en vez de estudiar».

Hoy la entiendo. Ante una tecnología que conocía poco, quería proteger mi aprendizaje, y desde fuera un chico con un ordenador que resuelve ecuaciones parece alguien que ha encontrado un atajo.

El atajo no existía. El Commodore no sabía nada de triángulos: cada paso tenía que enseñárselo yo. Saber resolver un problema de geometría en el cuaderno es una cosa; saber explicárselo a una máquina, paso a paso, sin dejar nada a la intuición, es otra, y requiere haber entendido el tema mucho más a fondo. Pensándolo bien, vale también cuando quien tiene que entenderlo es una persona.

## La puerta cerrada con llave

Mi padre volvió de la reunión y se tomó en serio a la profesora. Puso el Commodore en el dormitorio de él y de mi madre, y cerró la puerta con llave.

Una puerta cerrada con llave dice dos cosas: que dentro hay algo valioso, y que alguien ha decidido que no es para ti. Mi padre quería decir lo segundo. Yo solo escuché lo primero.

Casi en crisis de abstinencia, estudié la situación como un listado que no arrancaba. Hacían falta tres cosas: una tarde sin padres, un cómplice y una llave. Las tardes las había, porque mis padres salían y en casa nos quedábamos mi hermano y yo. Al cómplice lo sobornó un helado: mi primera negociación, y todavía hoy una de las más rentables. La llave la compré en la ferretería: una llave maestra.

La puerta se abrió. Cada vez que mis padres estaban fuera montaba el Commodore, y el cursor volvía a parpadear. Antes de que volvieran lo desmontaba todo y dejaba cada cosa en su sitio. Mi padre lo descubrió solo meses después.

No lo cuento como una hazaña que imitar. Lo cuento por las tres lecciones que encontré dentro, de mayor. La llave cerraba el ordenador; la curiosidad seguía libre. Una llave maestra abre muchas puertas porque nace de alguien que ha entendido cómo están hechas las cerraduras. Y quien abre una puerta se hace responsable de lo que encuentra dentro.

## El paciente ha cambiado

A los trece años le dije a mi padre que sería programador de videojuegos. Videojuegos nunca he escrito. En 1994 me matriculé en Ingeniería Informática en Roma Tre, y desde ahí llegaron treinta años de bases de datos y sistemas que sostienen bancos, aseguradoras y telecomunicaciones.

El niño que quería cuidar animales, a su manera, encontró su oficio. Un sistema que ralentiza o se detiene manda síntomas, raramente explicaciones. El trabajo empieza por una anamnesis, como la del doctor chiflado, y llega a un diagnóstico que hay que explicar paso a paso, como en los programas de geometría, a quien tiene que tomar una decisión.

Detrás de cada sistema hay personas: el equipo que lo mantiene en pie, quien recibe la llamada de noche, quien al día siguiente tiene que responder ante un consejo de administración. Cuidar un sistema significa, ante todo, permitir que ellos trabajen tranquilos.

Puertas cerradas sigo encontrando. La llave maestra sigue siendo la misma: entender cómo está hecha la cerradura. Con una diferencia importante: hoy las llaves me las entregan los clientes, y custodiarlas es la parte del trabajo que me tomo más en serio.

Hay una frase que, en el trabajo de cada día, me señala una puerta cerrada más que cualquier alarma: «siempre se ha hecho así». La escucho delante de un batch que nadie toca desde hace años, de una configuración heredada, de un control que se repite sin recordar ya por qué. Es una frase comprensible, dicha a menudo por personas competentes y cansadas. Y es precisamente ahí donde suele esconderse la línea 330.

El doctor, mientras tanto, se ha vuelto bastante menos chiflado.

## Igual que tú

El mérito de este camino es de personas normales.

Ante todo de mi padre. En 1983 trajo a casa un ordenador cuando pocos sabían qué hacer con él. Dejó que su hijo metiera las manos en los programas de sus libros, e incasó un «malo y antipático» con cierta satisfacción, porque había visto algo que el libro no contenía. E incluso cerrando aquella puerta con llave, sin quererlo, me enseñó cuánto valía lo que había dentro, y a no detenerme ante un «no» antes de haber entendido el porqué.

Luego de una profesora que, con las herramientas de aquellos años, quería proteger mi aprendizaje. Y de un hermano que guardó un secreto durante meses, al precio de un helado.

Si tú también empezaste delante de un cursor que parpadeaba, sabes de qué hablo. Y si hoy tienes delante una línea 340 que parece perfecta, la pregunta útil es una sola: ¿dónde está la línea 330?

## Glosario
**[BASIC](/es/glossary/basic/)** — BASIC es un lenguaje de programación interpretado de los años 80, diseñado para ordenadores domésticos con líneas numeradas y sintaxis legible para usuarios no especializados.
