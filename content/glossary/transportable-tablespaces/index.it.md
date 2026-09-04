---
title: "Transportable Tablespaces (TTS)"
description: "Tecnica Oracle per spostare tablespace tra database copiando i datafile fisici e importando solo i metadati via Data Pump. Molto più veloce di un export completo."
translationKey: "glossary_transportable_tablespaces"
aka: "Transportable Tablespaces (Oracle TTS)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

I Transportable Tablespaces (TTS) sono una funzionalità Oracle che consente di migrare uno o più tablespace tra database — anche su piattaforme diverse — copiando fisicamente i datafile e trasportando solo i metadati tramite Data Pump. Su volumi nell'ordine dei terabyte, il risparmio di tempo rispetto a un export/import tradizionale è sostanziale.

## Come funziona

Il processo si articola in tre fasi principali:

1. **Messa in read-only** del tablespace sorgente.
2. **Export dei metadati** con Data Pump (`TRANSPORT_TABLESPACES`).
3. **Copia fisica dei datafile** sul sistema di destinazione e successivo import dei metadati.

```sql
-- Messa in read-only
ALTER TABLESPACE sales_data READ ONLY;

-- Export metadati (Data Pump)
-- expdp system/pwd TRANSPORT_TABLESPACES=sales_data \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_sales.log

-- Dopo la copia dei datafile sul target:
-- impdp system/pwd TRANSPORT_DATAFILES='/u02/oradata/sales_data01.dbf' \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_import.log
```

Il database di destinazione deve avere un character set compatibile e, per piattaforme diverse, può essere necessaria una conversione endian tramite RMAN (`CONVERT TABLESPACE`).

## Quando si usa

TTS è la scelta naturale quando:

- si migrano grandi volumi di dati storici o data warehouse tra ambienti Oracle;
- il downtime tollerabile è ridotto e un export/import completo richiederebbe ore o giorni;
- si consolida più database in un unico target (es. upgrade a 21c su Exadata).

Il limite principale è che il tablespace sorgente deve restare in `READ ONLY` per tutta la durata della copia dei datafile. In scenari con requisiti di alta disponibilità, TTS si combina spesso con RMAN Incremental Backup per ridurre la finestra di read-only al minimo indispensabile.
