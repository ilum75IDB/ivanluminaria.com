---
title: "Transportable Tablespaces (TTS)"
description: "Funcționalitate Oracle pentru mutarea tablespace-urilor între baze de date prin copierea datafile-urilor fizice și importul doar al metadatelor via Data Pump. Mult mai rapid decât un export complet."
translationKey: "glossary_transportable_tablespaces"
aka: "Transportable Tablespaces (Oracle TTS)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

Transportable Tablespaces (TTS) este o funcționalitate Oracle care permite mutarea unuia sau mai multor tablespace-uri între baze de date — inclusiv pe platforme diferite — prin copierea fizică a datafile-urilor și transportul exclusiv al metadatelor prin Data Pump. Pe volume de ordinul terabyților, economia de timp față de un export/import clasic este semnificativă.

## Cum funcționează

Procesul are trei etape principale:

1. **Setarea tablespace-ului sursă în read-only.**
2. **Exportul metadatelor** cu Data Pump (`TRANSPORT_TABLESPACES`).
3. **Copierea datafile-urilor** pe sistemul destinație și importul metadatelor.

```sql
-- Setare tablespace în read-only
ALTER TABLESPACE sales_data READ ONLY;

-- Export metadate (Data Pump)
-- expdp system/pwd TRANSPORT_TABLESPACES=sales_data \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_sales.log

-- După copierea datafile-urilor pe destinație:
-- impdp system/pwd TRANSPORT_DATAFILES='/u02/oradata/sales_data01.dbf' \
--   DUMPFILE=tts_sales.dmp LOGFILE=tts_import.log
```

La migrarea între platforme cu endianness diferit, este necesar un pas de conversie RMAN (`CONVERT TABLESPACE`) înainte de import. Compatibilitatea character set între sursă și destinație este de asemenea obligatorie.

## Când se folosește

TTS este alegerea firească atunci când:

- se migrează volume mari de date istorice sau tablespace-uri de data warehouse între medii Oracle;
- timpul de indisponibilitate tolerat este redus, iar un export/import complet ar dura ore sau zile;
- se consolidează mai multe baze de date într-o singură destinație (ex. upgrade la 21c pe Exadata).

Principala constrângere este că tablespace-ul sursă trebuie să rămână în `READ ONLY` pe toată durata copierii datafile-urilor. În scenarii cu cerințe de înaltă disponibilitate, TTS se combină frecvent cu RMAN Incremental Backup pentru a reduce fereastra de read-only la minimul necesar.
