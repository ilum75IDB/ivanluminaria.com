---
title: "Dimensional Modeling"
date: "2026-03-10T10:00:00+01:00"
description: "Modellazione dimensionale nella pratica: gerarchie, dimensioni, tabelle dei fatti e le decisioni di design che fanno la differenza tra un DWH che risponde e uno che arranca."
layout: "list"
---
La modellazione dimensionale sembra semplice.<br>
Fatti e dimensioni. Star schema. Snowflake. Concetti che si imparano in un pomeriggio.<br>

Poi arrivi in produzione e scopri che il diavolo è nei dettagli. Una gerarchia sbilanciata che rompe tutte le aggregazioni. Una slowly changing dimension gestita male che riscrive la storia. Una granularità sbagliata nella tabella dei fatti che rende impossibile un report che il business considera banale.<br>

In questa sezione racconto i problemi reali della modellazione dimensionale — quelli che i libri trattano in mezza pagina e che in produzione ti costano settimane.
