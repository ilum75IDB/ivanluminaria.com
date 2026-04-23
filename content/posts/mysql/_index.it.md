---
title: "MySQL"
layout: "list"
description: "MySQL e MariaDB: sicurezza, performance e architettura su uno dei database più diffusi al mondo."
image: "mysql.cover.jpg"
---

Ho visto server MySQL con 64GB di RAM e `innodb_buffer_pool_size` lasciato a 128MB — "perché è il default e non abbiamo toccato niente". Ho visto tabelle MyISAM ancora in produzione nel 2026 perché "non abbiamo tempo di convertirle", con lock a livello di tabella che bloccavano interi applicativi durante i backup. Ho visto repliche master-slave con 47.000 secondi di ritardo e nessuno che se ne accorgeva, perché `Seconds_Behind_Master` non lo guardava nessuno.

E ho visto l'esatto contrario: parchi MySQL con centinaia di istanze gestite con disciplina, dove ogni decisione — storage engine, charset, binlog format, topology — è presa con consapevolezza e non per inerzia.

La differenza non è mai stata il motore. È sempre stata **la serietà con cui qualcuno ha scelto le opzioni**.

------------------------------------------------------------------------

MySQL è il database che non ha bisogno di presentazioni. È il motore che ha alimentato la crescita del web per oltre vent'anni.

Nato nel 1995 in Svezia, nel 2008 fu acquisito da Sun Microsystems — e quando nel 2010 Oracle completò l'acquisizione di Sun, MySQL finì nel portafoglio del più grande vendor di database commerciali al mondo. **Ero dipendente Oracle in quel periodo**, e ricordo bene il clima: da un lato la curiosità di vedere come Oracle avrebbe gestito un prodotto open source così popolare, dall'altro il timore che MySQL venisse marginalizzato a favore del database proprietario.

Quel timore spinse Michael "Monty" Widenius — il creatore originale di MySQL — a fare il fork nel 2009, dando vita a **MariaDB**. Un progetto che condivide le radici con MySQL ma ha preso strade proprie su storage engine, ottimizzatore e funzionalità avanzate.

La storia ha dimostrato che entrambi i progetti sono sopravvissuti e si sono evoluti. Ma nella quotidianità di chi gestisce produzioni reali, MySQL è ancora quello che *sembra* semplice e invece nasconde scelte critiche:

- **storage engine misti** per vecchia abitudine — MyISAM, InnoDB e a volte Archive convivono senza un motivo
- **charset sbagliato** (latin1 al posto di utf8mb4) che corrompe i dati multilingua in silenzio
- **binlog in formato STATEMENT** che causa inconsistenze in replica su query non deterministiche
- **`sql_mode`** permissivo per "retrocompatibilità" — query che restituiscono risultati diversi a ogni esecuzione
- **replica senza monitoring attivo** — e quando il master cade, lo slave ha tre giorni di ritardo

------------------------------------------------------------------------

## 🔧 Le scelte che fanno la differenza in produzione

Ci sono cinque decisioni che — prese bene — fanno funzionare MySQL per dieci anni, e — prese male — ti fanno riscrivere mezzo applicativo. Sono decisioni banali da elencare, scomodissime da cambiare dopo.

| Scelta | Cosa decide | Come la imposto |
|---|---|---|
| **Storage engine** | Lock granularity, transazionalità, crash recovery | InnoDB sempre, salvo casi marginali e motivati — MyISAM è un retaggio, non una scelta |
| **`innodb_buffer_pool_size`** | Memoria per cache dati e indici InnoDB | 70-80% della RAM su server dedicato, il resto è sprecato per il motore |
| **Charset e collation** | Encoding dei caratteri e ordinamento | `utf8mb4` + `utf8mb4_0900_ai_ci` — niente `utf8` (che in MySQL è incompleto) |
| **`binlog_format`** | Formato dei log binari per replica e PITR | `ROW` quasi sempre — `STATEMENT` causa problemi in replica con query non deterministiche |
| **`sql_mode`** | Quali errori MySQL tollera e quali no | Strict mode attivo, `ONLY_FULL_GROUP_BY` incluso — un MySQL permissivo è un MySQL che ti mente |

Cinque scelte. Trenta minuti di discussione. Anni di operatività senza incidenti grossi.

------------------------------------------------------------------------

## 📚 Di cosa parlo qui

Storie vere e scelte operative su MySQL e MariaDB in produzione. Sicurezza, gestione utenti e privilegi, tuning di InnoDB, replica master-slave e InnoDB Cluster, strategie di upgrade e migrazione, backup consistenti con `mysqldump` e strumenti fisici, differenze reali tra MySQL e MariaDB che emergono solo sotto carico.

Niente ricette generiche. Solo quello che ho visto funzionare su ambienti veri — postale, telco, finance, pubblica amministrazione — dove MySQL regge parchi di istanze in parallelo e non può permettersi scelte fatte "per inerzia".

------------------------------------------------------------------------

Usare MySQL non significa solo lanciare query.

Significa capire come il motore gestisce connessioni, privilegi e risorse sotto carico reale — e riconoscere che la semplicità apparente è, spesso, la trappola più costosa.
