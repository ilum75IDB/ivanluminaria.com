---
title: "Transparent Data Encryption (TDE)"
description: "Funcionalidad de Oracle que cifra datos en reposo — archivos de datos, redo logs, backups — sin cambios en las aplicaciones, protegiendo los soportes físicos de accesos no autorizados."
translationKey: "glossary_transparent_data_encryption"
aka: "TDE, cifrado transparente de datos"
articles:
  - "/posts/data-warehouse/data-governance-nel-data-warehouse-dal-controllo-qualita-alla-conformita-normati"
---

Transparent Data Encryption (TDE) es una funcionalidad de Oracle Database que cifra los datos en reposo — archivos de datos, redo logs, archivos temporales y backups — a nivel de almacenamiento, sin requerir ningún cambio en el código de las aplicaciones. El motor de cifrado opera de forma transparente entre el buffer cache y el disco: los datos se descifran al leerse en memoria y se cifran al escribirse en disco.

## Cómo funciona

TDE emplea una arquitectura de claves en dos niveles: una **Master Encryption Key (MEK)** custodiada en el wallet de Oracle (archivo `ewallet.p12`) o en un HSM externo, y una **Table/Tablespace Encryption Key** generada por cada objeto cifrado. La MEK nunca reside en los archivos de datos, lo que hace inútiles los archivos sustraídos físicamente sin acceso al wallet.

Habilitar TDE en una tablespace existente requiere una reorganización online:

```sql
-- Crear una tablespace cifrada (AES256)
CREATE TABLESPACE sensitive_data
  DATAFILE '/u01/oradata/ORCL/sensitive01.dbf' SIZE 500M
  ENCRYPTION USING 'AES256'
  DEFAULT STORAGE (ENCRYPT);

-- Cifrar una tablespace existente en línea (Oracle 12.2+)
ALTER TABLESPACE users ENCRYPTION ONLINE ENCRYPT;
```

## Cuándo se usa

TDE es el mecanismo estándar para cumplir requisitos normativos como GDPR, PCI-DSS e HIPAA que exigen el cifrado de datos en reposo. Resulta especialmente relevante en entornos de data warehouse donde los backups en cinta o en almacenamiento cloud salen del perímetro de control físico del datacenter. No protege frente a usuarios con acceso legítimo al base de datos: un DBA con privilegios `SYSDBA` lee los datos en texto claro. La protección apunta al robo físico de soportes o al acceso no autorizado al sistema de archivos subyacente.

El impacto en rendimiento es generalmente reducido (2–7% en cargas OLTP típicas), pero debe medirse en cargas intensivas en I/O como full table scan sobre fact tables de gran tamaño.
