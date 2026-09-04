---
title: "RMAN Incremental Backup"
description: "Strategie de backup Oracle RMAN care copiază doar blocurile modificate față de ultimul backup de nivel egal sau superior. Level 0 este baza, level 1 este delta-ul."
translationKey: "glossary_rman_incremental_backup"
aka: "RMAN Incremental Backup (Oracle Recovery Manager)"
articles:
  - "/posts/oracle/oracle-12c-21c-su-12-tb-transportable-tablespaces-rman-incremental-e-la"
---

RMAN Incremental Backup copiază doar blocurile de date modificate față de ultimul backup de nivel egal sau superior, fără a duplica datafile-urile în întregime. Aceasta reduce semnificativ atât fereastra de backup, cât și volumul de date transferat, făcând din această tehnică instrumentul standard pentru sincronizarea bazelor de date de mari dimensiuni în timpul migrărilor.

## Cum funcționează

Mecanismul se bazează pe două niveluri:

- **Level 0**: echivalent funcțional cu un backup complet, servind drept bază a lanțului incremental. Toate blocurile sunt copiate.
- **Level 1**: copiază doar blocurile modificate după cel mai recent backup de level 0 sau level 1.

RMAN urmărește blocurile modificate prin intermediul **Change Tracking File** (când este activat), evitând scanarea completă a datafile-urilor la fiecare rulare.

```bash
# Backup incremental level 0 (baza)
rman target /
BACKUP INCREMENTAL LEVEL 0 DATABASE;

# Backup incremental level 1 (delta)
BACKUP INCREMENTAL LEVEL 1 DATABASE;

# Aplicarea delta-ului pe o copie imagine
RECOVER COPY OF DATABASE WITH TAG 'incr_merge';
```

## Când se utilizează

În scenarii de migrare — cum ar fi trecerea de la Oracle 12c la 21c pe o bază de date de 12 TB — fluxul tipic este:

1. Realizarea unui backup level 0 (sau a unei copii fizice inițiale) pe sistemul sursă.
2. Aplicarea de backup-uri level 1 succesive pentru a reduce gap-ul de date pe măsură ce fereastra de cutover se apropie.
3. La momentul downtime-ului, aplicarea ultimului incremental și deschiderea bazei de date destinație.

Această abordare comprimă downtime-ul final la câteva minute, indiferent de dimensiunea bazei de date. Principala constrângere este dependența de lanț: un backup level 1 nu poate fi aplicat fără un level 0 valid în prealabil.
