---
title: "Transient Ischemic Attack"
description: "Un TIA (Transient Ischemic Attack) è un episodio neurologico transitorio che, in ambito IT, descrive un'interruzione breve ma rivelatrice di un sistema."
translationKey: "glossary_transient_ischemic_attack"
aka: "TIA, mini-ictus, attacco ischemico transitorio"
articles:
  - "/posts/project-management/il-restart-ha-risolto-il-problema-e-ancora-li"
---

In medicina, un Transient Ischemic Attack (TIA) è un episodio di deficit neurologico che si risolve spontaneamente entro 24 ore, senza lasciare danni permanenti rilevabili. In ambito di project management e gestione dei sistemi IT, il termine viene usato come metafora per descrivere quei malfunzionamenti brevi, apparentemente autorisolti, che in realtà segnalano un problema strutturale sottostante.

## Il meccanismo della metafora

Come il TIA clinico precede spesso un ictus vero e proprio, un "TIA di sistema" — un crash risolto con un restart, un timeout sparito da solo, un picco di latenza rientrato senza intervento — è un segnale di allarme, non una risoluzione. Il sistema ha recuperato, ma la causa radice è ancora presente. Ignorare l'episodio perché "si è risolto da solo" è esattamente l'errore che trasforma un warning in un'emergenza.

## Contesto operativo

Nei progetti IT, i TIA si manifestano come:

- riavvii applicativi notturni che "sistemano tutto" senza che nessuno sappia perché
- query lente che tornano veloci dopo un restart del connection pool
- errori intermittenti su code di messaggi che scompaiono prima che qualcuno apra un ticket

La gestione corretta non è celebrare il ripristino, ma aprire un'analisi post-mortem anche quando il sistema è tornato operativo. Un TIA non diagnosticato è un debito tecnico con scadenza ignota.

## Note

Il termine è volutamente provocatorio: usarlo in una retrospettiva o in un incident report aiuta il team a spostare il focus dal "è tornato su" al "perché è caduto".
