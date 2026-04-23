---
title: "Oracle"
layout: "list"
date: "2026-03-10T08:03:00+01:00"
description: "Oracle Database: sicurezza, performance e architettura sul database enterprise più longevo e complesso del mercato."
image: "oracle.cover.jpg"
---

Ho visto un DBA spegnere una produzione con un `DROP TABLESPACE` lanciato sulla finestra sbagliata. Ho visto query da quattro secondi diventare quattro ore dopo un upgrade, perché qualcuno aveva toccato `optimizer_features_enable` "tanto era uguale". Ho visto backup che non si ripristinavano, audit disabilitati "temporaneamente" da cinque anni, e indici creati in produzione a mano libera di venerdì pomeriggio.

E ho visto l'esatto contrario: istanze Oracle che funzionano da vent'anni senza un minuto di downtime non programmato, reggono carichi enormi e sopravvivono a tre upgrade maggiori senza scosse.

La differenza non è mai stata la versione. È sempre stato **chi la gestiva**.

------------------------------------------------------------------------

Ci lavoro dal 1996. In quasi trent'anni ho visto passare Oracle 7, 8i, 9i, 10g, 11g, 12c, 19c, 21c, 23ai — e paradigmi, mode, consulenti che vendevano la feature del momento come la risposta a ogni problema.

Il cuore del motore, però, è rimasto quello: **solido, complesso, spietato con chi non lo conosce a fondo.**

Oracle non si impara sui tutorial. Si impara:

- sugli **incidenti in produzione** alle tre di notte, quando il manuale serve a poco e vale più un collega che ha già visto quel comportamento
- sulle **migrazioni** in cui il piano di esecuzione cambia il giorno dopo il go-live e nessuno capisce perché
- sui **piani di esecuzione** che diventano patologici dopo un `DBMS_STATS.GATHER_SCHEMA_STATS` lanciato con i parametri di default
- sulle **`v$`** che dicono la verità anche quando l'applicativo mente
- sui **tuning pack** che servono davvero, e su quelli che hai pagato e non accenderai mai

------------------------------------------------------------------------

## 🔧 Cosa guardo quando arrivo su un'istanza nuova

Quando un cliente mi chiama perché "il database va piano" o "c'è qualcosa che non va", ci sono cinque cose che guardo prima di toccare qualunque parametro. Non è una checklist da corso di certificazione — è quello che ho imparato a guardare dopo aver perso tempo troppe volte sui posti sbagliati.

| Cosa | Dove guardo | Perché |
|---|---|---|
| **Il carico reale** | AWR, ASH, `v$active_session_history` | Capire chi consuma davvero CPU, I/O e `db time` — spesso non è quello che sospetta il cliente |
| **Cosa ha toccato chi è venuto prima** | `v$parameter` con `ismodified`, `dba_hist_parameter` | I parametri "non standard" sono il primo indizio di debug passati senza documentazione |
| **Chi fa cosa** | `dba_audit_trail`, `unified_audit_trail`, job schedulati | Trovare i job notturni, le connessioni applicative reali, gli accessi DBA non tracciati |
| **Lo stato di Data Guard** | `v$dataguard_stats`, `v$archive_dest_status` | Se c'è uno standby, verificare che sia davvero allineato — non fidarsi dei dashboard |
| **Lo spazio e la crescita** | `dba_tablespaces`, `dba_hist_tbspc_space_usage` | Capire dove si sta andando a sbattere prima che succeda, non dopo |

Una volta lette queste cinque cose, ho il 70% del quadro. Le altre domande vengono dopo — e vengono mirate.

------------------------------------------------------------------------

## 📚 Di cosa parlo qui

Storie vere, numeri concreti e lezioni apprese su Oracle in produzione. Architettura, performance, sicurezza, migrazioni, tuning SQL, PL/SQL, gestione dello storage e scelte progettuali che separano un'installazione che funziona da una che sopravvive.

Niente teoria da brochure. Solo quello che ho visto funzionare — e quello che ho visto fallire — su ambienti veri: assicurazioni, telco, pubblica amministrazione, banche, farmaceutico.

------------------------------------------------------------------------

Con Oracle non basta sapere la sintassi.

Bisogna capire come ragiona il motore — e avere l'umiltà di ammettere che, a volte, ha ragione lui.
