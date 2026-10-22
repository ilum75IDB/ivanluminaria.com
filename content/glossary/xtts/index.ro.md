---
title: "XTTS (Cross-Platform Transportable Tablespaces)"
description: "Metodă Oracle pentru migrarea bazelor de date de mai mulți terabytes între versiuni diferite, minimizând downtime-ul prin backup-uri RMAN incrementale ciclice."
translationKey: "glossary_xtts"
aka: "Cross-Platform Transportable Tablespaces"
articles:
  - "/posts/oracle/oracle-11g-r2-19c-su-oci-8-tb-in-finanza-un-piano-di-upgrade-con-fasi-e-rollback"
---

XTTS (Cross-Platform Transportable Tablespaces) este tehnica Oracle care permite mutarea tablespace-urilor între platforme și versiuni diferite de baze de date — de exemplu de la Oracle 11gR2 pe Linux x86 la Oracle 19c pe OCI — prin transportul fizic al datafile-urilor în loc de un export/import logic. Pentru baze de date de ordinul terabyte-urilor, această abordare reduce downtime-ul cutover-ului final de la zile la câteva ore.

## Cum funcționează

Procesul este structurat în trei faze distincte:

1. **Backup RMAN level 0** — copie completă a datafile-urilor tablespace-urilor sursă, transferată la destinație și restaurată.
2. **Incrementale ciclice (level 1)** — executate de mai multe ori în săptămânile dinaintea cutover-ului, reduc progresiv delta dintre sursă și destinație.
3. **Cutover final** — ultimul incremental este aplicat cu tablespace-ul sursă în mod read-only; plug-in-ul pe destinație finalizează migrarea.

```bash
# Exemplu: generarea scriptului RMAN pentru backup level 0
$ORACLE_HOME/perl/bin/perl xttdriver.pl --backup_to_dest \
  --tablespaces USERS,FINANCE \
  --level 0
```

Scriptul `xttdriver.pl` (disponibil pe Oracle MOS) orchestrează backup-ul, conversia endianness și transferul fișierelor.

## Când se folosește

XTTS este alegerea potrivită atunci când:

- Baza de date depășește câteva sute de GB și un export Data Pump ar necesita ferestre de mentenanță inacceptabile.
- Migrarea traversează versiuni majore (ex. 11g → 19c) sau platforme cu endianness diferit.
- SLA-ul impune un downtime maxim măsurabil în ore, nu în zile.

Principala limitare este complexitatea operațională: necesită coordonare precisă între DBA-ii sursă și destinație, verificarea compatibilității character set-ului și gestionarea separată a obiectelor non-transportabile (secvențe, sinonime, granturi), care trebuie migrate independent prin Data Pump.
