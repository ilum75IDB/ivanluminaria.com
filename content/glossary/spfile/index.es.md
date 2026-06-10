---
title: "SPFILE"
description: "SPFILE (Server Parameter File) es el archivo binario de Oracle con los parámetros de configuración de la instancia, modificable en caliente sin reiniciar la base de datos."
translationKey: "glossary_spfile"
aka: "Server Parameter File"
articles:
  - "/posts/oracle/quali-sono-i-files-critici-di-un-db-oracle"
---

El SPFILE es el archivo binario que Oracle lee al arrancar para inicializar los parámetros de la instancia: `db_name`, `control_files`, `memory_target`, `sga_target` y muchos otros. A diferencia de su predecesor en texto plano PFILE (`init.ora`), el SPFILE no se edita manualmente con un editor de texto; los cambios se realizan mediante comandos SQL.

## Cómo funciona

Al arrancar, Oracle busca el SPFILE en una ubicación predeterminada (`$ORACLE_HOME/dbs/spfile<SID>.ora` en Linux). Si no lo encuentra, recurre al PFILE. Los cambios en los parámetros se realizan con `ALTER SYSTEM SET`, que escribe directamente en el archivo binario:

```sql
-- Cambio persistente (sobrevive al reinicio)
ALTER SYSTEM SET memory_target = 2G SCOPE = SPFILE;

-- Solo en memoria (se pierde al reiniciar)
ALTER SYSTEM SET memory_target = 2G SCOPE = MEMORY;

-- Tanto en memoria como en el archivo
ALTER SYSTEM SET memory_target = 2G SCOPE = BOTH;
```

El parámetro `SCOPE` controla dónde se aplica el cambio: `SPFILE`, `MEMORY` o `BOTH`.

## Contexto operativo

El SPFILE es la fuente de referencia para la configuración persistente de la instancia. Debe incluirse en los backups de RMAN, que lo gestiona de forma nativa. En entornos RAC (Real Application Clusters), un único SPFILE compartido en ASM gobierna todos los nodos, con la posibilidad de definir valores por instancia mediante el prefijo `SID.*`.

Un error frecuente es editar manualmente el archivo binario: la instancia no arrancará. Si el SPFILE se corrompe, se restaura desde un backup de RMAN o se recrea a partir de un PFILE con `CREATE SPFILE FROM PFILE`.
