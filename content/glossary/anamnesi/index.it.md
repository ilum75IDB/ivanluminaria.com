---
title: "Anamnesi"
description: "Raccolta sistematica di informazioni su sintomi, eventi recenti e configurazione di un sistema, punto di partenza per la diagnosi di un problema tecnico."
translationKey: "glossary_anamnesi"
aka: "Raccolta della storia del sistema"
articles:
  - "/posts/project-management/il-dottore-tutto-pazzo-un-commodore-64-una-porta-chiusa-e-il-mestiere-di-capire"
---

In medicina, l'anamnesi è la raccolta della storia clinica del paziente prima di formulare una diagnosi. Nel contesto della diagnostica di sistemi informatici, il termine indica lo stesso processo applicato a macchine, database e applicazioni: raccogliere in modo sistematico sintomi osservati, eventi recenti, modifiche alla configurazione e contesto operativo, prima di avanzare qualsiasi ipotesi sulla causa del problema.

## Come funziona

L'anamnesi tecnica si articola in domande precise e sequenziali:

- **Cosa è cambiato di recente?** Deploy, aggiornamenti di pacchetti, modifiche a parametri di configurazione, interventi di manutenzione.
- **Quando è comparso il sintomo?** Timestamp precisi, correlazione con eventi schedulati (backup, batch, picchi di carico).
- **Chi ha accesso e cosa ha fatto?** Log di accesso, history dei comandi, ticket aperti nelle ore precedenti.
- **Qual è la configurazione attuale?** Versione del software, risorse hardware, topologia di rete, dipendenze esterne.

Solo dopo aver raccolto queste informazioni ha senso formulare ipotesi diagnostiche. Saltare questo passaggio porta quasi sempre a inseguire cause sbagliate.

## Quando si usa

L'anamnesi è il primo passo ogni volta che si affronta un problema non immediatamente riproducibile o con causa non ovvia: rallentamenti improvvisi, errori intermittenti, comportamenti anomali dopo un aggiornamento. È particolarmente critica negli ambienti di produzione, dove il tempo di diagnosi ha un costo diretto, e nei sistemi legacy dove la documentazione è scarsa e la memoria storica è distribuita tra persone diverse.

Un'anamnesi ben condotta riduce il rischio di applicare fix che risolvono il sintomo senza toccare la causa radice.
