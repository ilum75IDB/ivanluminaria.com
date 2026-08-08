---
categories:
- oracle
date: 2099-12-31
description: Cómo tres tipos de índice Oracle Text transformaron búsquedas de 90 segundos
  en menos de 700 ms en un archivo legal con décadas de documentos.
draft: true
image: oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente.cover.jpg
seoTitle: 'Oracle Text: índices CONTEXT, CATSEARCH y CTXXPATH en producción'
tags:
- oracle-text
- full-text-search
- oracle-19c
- indexing
- performance-tuning
title: 'La frustración de Alberto: Oracle Text y la búsqueda full-text en un archivo
  legal de treinta años'
translationKey: oracle_text_indicizzare_e_ricercare_testo_in_modo_efficiente
webo_generated_at: 2026-08-08
webo_status: da_tradurre
---

## La frustración de Alberto

Alberto no abrió un ticket. Llamó directamente, en mitad de una tarde, y lo primero que dijo fue: "Los tiempos de búsqueda son inaceptables. No puedo esperar un minuto cada vez que busco un contrato."

Treinta años de documentos sedimentados en un archivo Oracle. Contratos, dictámenes, escritos procesales, correspondencia con clientes y contrapartes. El esquema `LEGAL_ARCHIVE` en `oracle-legal-prod-01` contenía dos tablas principales: `DOCUMENTS`, con una columna `DOC_CONTENT` de tipo CLOB que acumulaba cientos de gigabytes de texto, y `EMAILS`, con `SENDER`, `SUBJECT` y `BODY`. Millones de filas en ambas.

El cuello de botella no era la lentitud genérica del sistema. Era la búsqueda textual: consultas `LIKE '%término%'` sobre columnas CLOB, sin índices específicos para ese tipo de carga. Treinta segundos para encontrar un contrato, cuarenta y cinco para buscar un correo por asunto y contenido. Noventa en los peores momentos.

Lo primero que hicimos, antes de tocar ninguna configuración, fue sentarnos con Alberto y con dos de sus colaboradores más operativos y preguntarles cómo buscan de verdad. No "qué buscáis", sino *cómo*: ¿fragmentos de texto libre? ¿Combinaciones de remitente más palabra clave en el cuerpo? ¿Cláusulas específicas en documentos XML estructurados? La respuesta cambió completamente el enfoque.

Nadie había hecho esa pregunta antes.

## Oracle Text: no un complemento, una componente integrada

Oracle Text está incluido en Oracle Database sin licencia adicional [1]. No es un motor externo que integrar, no es un Elasticsearch que mantener en paralelo: es un sistema de indexación full-text que vive dentro de la base de datos, con acceso directo a los datos, a las transacciones y al control de acceso ya existente.

La distinción respecto a un índice B-tree estándar es sustancial. Un B-tree sobre una columna `VARCHAR2` funciona para igualdades y prefijos (`LIKE 'término%'`), y al mismo tiempo no sirve para búsquedas en mitad del texto (`LIKE '%término%'`) sobre columnas CLOB de cientos de gigabytes — en ese caso Oracle ejecuta un escaneo completo de la columna, fila a fila. Oracle Text construye en cambio una estructura invertida: para cada token (palabra) mantiene la lista de documentos que lo contienen, con información de posición. La consulta no escanea los datos, consulta el índice.

Tres tipos de índice cubren escenarios distintos:

- **CONTEXT** — texto libre, documentos, artículos
- **CATSEARCH** — archivos mixtos con atributos estructurados y texto libre
- **CTXXPATH** — documentos XML o JSON almacenados en CLOB/BLOB

La elección entre los tres no es arbitraria: depende exactamente de cómo buscan los usuarios. Por eso la conversación con Alberto vino antes que el código.

## Índice CONTEXT: la base para los documentos libres

Para `LEGAL_ARCHIVE.DOCUMENTS` el caso era claro: búsqueda full-text sobre texto no estructurado. Contratos en formato texto, dictámenes legales, escritos. El índice CONTEXT es la elección natural [1].

```sql
-- Creación del índice CONTEXT sobre la columna DOC_CONTENT
BEGIN
  CTX_DDL.CREATE_PREFERENCE('legal_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('legal_lexer', 'MIXED_CASE', 'NO');

  CTX_DDL.CREATE_STOPLIST('legal_stoplist', 'BASIC_STOPLIST');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'il');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'la');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'di');
  CTX_DDL.ADD_STOPWORD('legal_stoplist', 'che');
END;
/

CREATE INDEX legal_doc_ctx_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CONTEXT
PARAMETERS ('LEXER legal_lexer STOPLIST legal_stoplist MEMORY 256M');
```

El `BASIC_LEXER` con `BASE_LETTER YES` gestiona la normalización de acentos — fundamental para el italiano, donde "è" y "e" no deben tratarse como tokens distintos en una búsqueda. La `STOPLIST` excluye del índice las palabras funcionales que no aportan significado semántico en las consultas legales.

Las consultas usan el operador `CONTAINS` [1]:

```sql
-- Búsqueda de documentos que contienen ambos términos
SELECT doc_id, doc_title, SCORE(1) AS relevance
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'responsabilità AND contrattuale', 1) > 0
ORDER BY SCORE(1) DESC;

-- Búsqueda por proximidad: los dos términos a menos de 5 palabras entre sí
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'NEAR((inadempimento, risarcimento), 5)', 1) > 0;
```

El resultado tras la implementación: de 30-60 segundos a menos de 500 ms. No es una estimación optimista, es el dato medido sobre consultas representativas de la carga real.

## Índice CATSEARCH: cuando el texto se mezcla con los metadatos

Los correos eran un caso distinto. Alberto y sus colaboradores no buscan solo en el cuerpo del mensaje: buscan por remitente, por asunto, por fecha, y luego filtran en el texto. Una consulta típica era: "todos los correos de ese consultor externo, con 'peritaje' en el asunto o en el cuerpo, en los últimos dos años".

Este es exactamente el escenario para el que existe CATSEARCH [1]: búsquedas que combinan predicados SQL sobre columnas estructuradas con búsqueda full-text sobre columnas de texto.

```sql
-- Definición del conjunto de columnas estructuradas incluidas en el índice
EXEC CTX_DDL.CREATE_INDEX_SET('legal_email_set');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SENDER');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'SUBJECT');
EXEC CTX_DDL.ADD_INDEX('legal_email_set', 'RECEIVED_DATE');

-- Creación del índice CATSEARCH sobre EMAILS
CREATE INDEX legal_email_cat_idx
ON LEGAL_ARCHIVE.EMAILS(BODY)
INDEXTYPE IS CTXSYS.CATSEARCH
PARAMETERS ('CTXCAT_INDEX_CLAUSE
  "CTXCAT_INDEX_SET legal_email_set"');
```

El orden importa: primero se define el conjunto de columnas estructuradas, luego se crea el índice que lo referencia.

La consulta usa el operador `CATSEARCH` con una cláusula estructurada separada [1]:

```sql
-- Búsqueda combinada: remitente específico + término en el cuerpo
SELECT email_id, sender, subject, received_date
FROM LEGAL_ARCHIVE.EMAILS
WHERE CATSEARCH(
  BODY,
  'perizia',
  'SENDER = ''consulente.esterno@example.com'' AND
   RECEIVED_DATE > DATE ''2024-01-01'''
) > 0
ORDER BY received_date DESC;
```

La diferencia respecto a CONTEXT es que los predicados sobre las columnas estructuradas se evalúan dentro del índice, no como filtros SQL posteriores. El optimizador no tiene que encontrar primero todos los documentos con "perizia" y luego filtrar por remitente: las dos condiciones se resuelven juntas. De 45-90 segundos a menos de 700 ms.

## Índice CTXXPATH: dentro de los documentos XML y JSON

Una parte del archivo contenía documentos en formato XML — escritos estructurados con secciones, referencias normativas, metadatos codificados. Buscar con `LIKE` sobre un CLOB que contiene XML es ineficiente por definición: no hay forma de limitar la búsqueda a un nodo específico sin parsear el documento en tiempo de ejecución.

CTXXPATH resuelve esta situación [1]: indexa el contenido XML preservando la estructura de los paths, y permite consultas que buscan un término solo dentro de un nodo específico.

```sql
-- Creación del índice CTXXPATH sobre documentos XML
CREATE INDEX legal_xml_xpath_idx
ON LEGAL_ARCHIVE.DOCUMENTS(DOC_CONTENT)
INDEXTYPE IS CTXSYS.CTXXPATH;
```

La consulta usa `CTX_XPTH.CONTAINS` [1]:

```sql
-- Búsqueda del término 'inadempimento' solo en la sección <motivazione>
SELECT doc_id, doc_title
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CTX_XPTH.CONTAINS(
  DOC_CONTENT,
  '/atto/motivazione[. contains("inadempimento")]'
) = 1;
```

Antes: consulta `LIKE '%inadempimento%'` sobre CLOB XML, más de 120 segundos. Después: menos de un segundo. La diferencia es estructural: el índice sabe dónde se encuentran los tokens respecto a la jerarquía XML, y no tiene que releer el documento completo para responder.

## Operadores avanzados y relevancia

Una vez que los índices estaban activos, trabajamos con los colaboradores del despacho para afinar las consultas. Oracle Text ofrece un conjunto de operadores que van más allá de la simple búsqueda booleana [1][2].

`ACCUM` acumula las puntuaciones en lugar de exigir que todos los términos estén presentes — útil cuando se quiere ordenar por relevancia global sin excluir documentos que contienen solo algunos de los términos:

```sql
-- Documentos más relevantes para una combinación de términos
SELECT doc_id, doc_title, SCORE(1) AS score
FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(
  DOC_CONTENT,
  '(responsabilità ACCUM contrattuale ACCUM inadempimento)',
  1
) > 0
ORDER BY SCORE(1) DESC
FETCH FIRST 20 ROWS ONLY;
```

`FUZZY` gestiona las variaciones ortográficas y los errores tipográficos — especialmente útil en textos escaneados con OCR, donde la calidad del reconocimiento no es uniforme:

```sql
-- Búsqueda fuzzy para gestionar variantes ortográficas
SELECT doc_id FROM LEGAL_ARCHIVE.DOCUMENTS
WHERE CONTAINS(DOC_CONTENT, 'FUZZY(risarcimanto, 70, 6)', 1) > 0;
```

El parámetro `70` es el umbral de similitud (0-100), `6` el número máximo de expansiones. Hay que calibrarlo: umbrales demasiado bajos generan ruido, demasiado altos pierden las variantes relevantes.

Para presentar los resultados a los usuarios, `CTX_DOC.HIGHLIGHT` devuelve el texto con los términos encontrados marcados [1]:

```sql
-- Highlighting de los términos encontrados en el documento
DECLARE
  v_highlight CLOB;
BEGIN
  CTX_DOC.HIGHLIGHT(
    index_name  => 'LEGAL_DOC_CTX_IDX',
    textkey     => '12345',
    query       => 'responsabilità contrattuale',
    restab      => v_highlight,
    starttag    => '<b>',
    endtag      => '</b>'
  );
  DBMS_OUTPUT.PUT_LINE(DBMS_LOB.SUBSTR(v_highlight, 500, 1));
END;
/
```

## Sincronización y mantenimiento de los índices

Un aspecto frecuentemente subestimado: los índices Oracle Text no se actualizan automáticamente en tiempo real como un B-tree. Cuando se insertan nuevas filas, el índice debe sincronizarse de forma explícita [1].

```sql
-- Sincronización manual del índice
EXEC CTX_DDL.SYNC_INDEX('LEGAL_DOC_CTX_IDX', '256M');

-- Optimización periódica para compactar las estructuras internas
EXEC CTX_DDL.OPTIMIZE_INDEX('LEGAL_DOC_CTX_IDX', 'FULL');
```

Para un archivo en producción con inserciones continuas, la sincronización debe programarse. Un job `DBMS_SCHEDULER` cada 15-30 minutos es un punto de partida razonable; la frecuencia depende del volumen de inserciones y de la tolerancia al retraso de indexación. Para `LEGAL_ARCHIVE`, donde los documentos se cargan en lotes nocturnos, una sincronización post-carga era suficiente.

El monitoreo pasa por `CTX_USER_INDEXES` y `CTX_INDEX_ERRORS`:

```sql
-- Verificación del estado de los índices Oracle Text
SELECT idx_name, idx_status, idx_docid_count
FROM CTX_USER_INDEXES;

-- Verificación de los errores de indexación
SELECT err_index_name, err_timestamp, err_text
FROM CTX_INDEX_ERRORS
ORDER BY err_timestamp DESC;
```

## El alivio de Alberto, no la sorpresa

Cuando mostramos los resultados a Alberto, su reacción no fue asombro. Fue alivio. "Por fin", dijo. No "increíble" — *por fin*.

Esa palabra lo dice todo sobre el enfoque que funcionó. No hubo un momento heroico en el que alguien encontró la solución mágica. Hubo una conversación en la que dejamos de mirar los logs y preguntamos a los usuarios cómo trabajan de verdad. De esa conversación emergió que hacían falta tres índices distintos para tres patrones de búsqueda distintos, no un índice genérico aplicado a todo.

Oracle Text ya estaba disponible en la instancia 19c. Las funcionalidades estaban documentadas. Lo que faltaba era el mapeo entre las necesidades reales de búsqueda y las capacidades de la herramienta.

El equipo del despacho contribuyó de forma determinante: sin su disposición a describir los flujos de trabajo reales — no los teóricos, los cotidianos — habríamos configurado índices razonables sobre el papel pero no óptimos para ese contexto específico. La tecnología es una herramienta; entender el problema es el trabajo de verdad.

Los índices Oracle Text no se construyen desde la documentación hacia los datos. Se construyen desde las necesidades de quien busca hacia la estructura de los datos, y luego la documentación ayuda a encontrar el tipo de índice y los operadores adecuados. En ese orden.

## Fuentes oficiales

1. Oracle Text Reference 19c — [Oracle Text Indextype Reference (CONTEXT, CATSEARCH, CTXXPATH, CONTAINS, CATSEARCH operator, CTX_XPTH.CONTAINS, WORDLIST, STOPLIST, LEXER, CTX_DDL.SYNC_INDEX, CTX_DOC.HIGHLIGHT)](https://docs.oracle.com/en/database/oracle/oracle-database/19/textr/index.html)
2. Oracle Text Application Developer's Guide 19c — [Conceptos avanzados, tuning y buenas prácticas](https://docs.oracle.com/en/database/oracle/oracle-database/19/texta/toc.htm)
3. Oracle-Base (Tim Hall) — [Oracle Text Articles: ejemplos prácticos](https://oracle-base.com/articles/misc/oracle-text)

## Glosario
- **[Oracle Text](/es/glossary/oracle-text/)** — Componente integrada de Oracle Database para la indexación y búsqueda full-text sobre datos textuales. No requiere licencia separada y opera directamente sobre las estructuras de datos de la base de datos, incluidas columnas CLOB, BLOB y VARCHAR2.

- **[Índice CONTEXT](/es/glossary/oracle-text/)** — Tipo de índice Oracle Text para la búsqueda full-text sobre texto no estructurado (documentos, artículos, dictámenes). Construye una estructura invertida token→documento que evita el escaneo completo de la columna CLOB en cada consulta.

- **[Índice CATSEARCH](/es/glossary/indice-context/)** — Tipo de índice Oracle Text optimizado para archivos que combinan atributos estructurados (remitente, fecha, categoría) con texto libre. Los predicados SQL y la búsqueda textual se resuelven juntos dentro del índice, no en fases separadas.

- **Índice CTXXPATH** — Tipo de índice Oracle Text para documentos XML o JSON almacenados en CLOB/BLOB. Preserva la estructura jerárquica de los paths XML durante la indexación, permitiendo consultas que limitan la búsqueda a nodos específicos del documento.

- **Lexer** (Oracle Text) — Componente que analiza el texto durante la fase de indexación, dividiéndolo en tokens y aplicando reglas de normalización específicas para el idioma y el formato. El `BASIC_LEXER` con `BASE_LETTER YES` gestiona, por ejemplo, la normalización de acentos para el italiano.
