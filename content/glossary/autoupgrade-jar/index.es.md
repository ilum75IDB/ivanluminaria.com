---
title: "autoupgrade.jar"
description: "Herramienta Oracle de línea de comandos que automatiza el upgrade de bases de datos. En modo analyze examina la instancia origen y genera un informe de compatibilidad sin realizar cambios."
translationKey: "glossary_autoupgrade_jar"
aka: "Oracle AutoUpgrade Utility"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

`autoupgrade.jar` es la utilidad Oracle distribuida como JAR ejecutable que automatiza el ciclo completo de upgrade de una base de datos, desde la verificación previa a la migración hasta la finalización. Reemplaza los antiguos scripts manuales `dbupgrade` y reduce drásticamente el riesgo de error humano en operaciones de upgrade a gran escala.

## Cómo funciona

La herramienta se invoca mediante `java -jar autoupgrade.jar` con un archivo de configuración que describe el entorno origen y destino. Soporta tres modos principales:

```bash
# Modo analyze: solo lectura, sin modificaciones en la instancia
java -jar autoupgrade.jar -config upgrade.cfg -mode analyze

# Modo fixups: aplica las correcciones pre-upgrade identificadas
java -jar autoupgrade.jar -config upgrade.cfg -mode fixups

# Modo deploy: ejecuta el upgrade completo
java -jar autoupgrade.jar -config upgrade.cfg -mode deploy
```

En modo `analyze`, la herramienta consulta las vistas del sistema, verifica la compatibilidad de los objetos, valida los parámetros de inicialización y genera un informe en HTML/texto con los problemas detectados y las acciones recomendadas. No se realiza ninguna escritura sobre la base de datos origen.

## Cuándo se usa

El modo `analyze` es el instrumento de referencia durante la fase de **assessment pre-migración**: permite ejecutar múltiples pasadas de análisis sobre entornos de producción sin downtime ni riesgo. Es especialmente relevante cuando la base de datos origen está en versión 11g o 12c y el destino es 19c, ya que la distancia entre versiones amplía el número de deprecaciones e incompatibilidades a gestionar.

En entornos financieros con tablespaces de varios TB, el informe generado se convierte en entrada directa para el plan de ROLLBACK y para la estimación de las ventanas de mantenimiento.
