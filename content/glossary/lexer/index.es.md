---
title: "Lexer"
description: "Componente de Oracle Text que divide el texto en tokens durante la indexación, aplicando reglas de normalización específicas por idioma y formato."
translationKey: "glossary_lexer"
aka: "Lexer (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

El Lexer es el componente de Oracle Text responsable del análisis textual durante la fase de indexación. Recibe el texto sin procesar de un documento o columna y lo divide en tokens — las unidades atómicas sobre las que se construye el índice invertido — aplicando reglas de normalización que varían según el idioma y el tipo de contenido.

## Cómo funciona

El Lexer actúa antes de que los tokens se escriban en el índice invertido. Sus responsabilidades principales son la tokenización (dónde dividir el texto), la normalización (cómo transformar cada token) y el tratamiento de caracteres especiales.

Oracle Text ofrece varios tipos de Lexer. El más habitual para texto en lenguaje natural es `BASIC_LEXER`, configurable mediante `CTX_DDL.SET_ATTRIBUTE`:

```sql
BEGIN
  CTX_DDL.CREATE_PREFERENCE('my_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'MIXED_CASE', 'NO');
END;
/
```

El atributo `BASE_LETTER YES` indica al Lexer que reduzca los caracteres acentuados a su forma base (p. ej. `è` → `e`, `ü` → `u`), haciendo las búsquedas insensibles a los acentos — comportamiento esencial para el español, el italiano y otras lenguas europeas.

## Cuándo se utiliza

La elección y configuración del Lexer afecta directamente a la calidad de las búsquedas de texto completo. Es necesario definir un Lexer personalizado cuando:

- el corpus contiene textos en idiomas con acentos o caracteres no ASCII (español, italiano, francés, alemán);
- se indexan URLs, códigos de producto o identificadores técnicos que no deben fragmentarse como palabras comunes;
- se necesita controlar explícitamente la sensibilidad a mayúsculas y minúsculas de los tokens.

El Lexer se asocia al índice en el momento de su creación mediante el parámetro `LEXER` en la cláusula `PARAMETERS` de `CREATE INDEX`. Una vez creado el índice, cambiar el Lexer requiere una reindexación completa.
