---
title: "Slot di replica logica"
draft: false
type: glossary
section_hint: postgresql
---

struttura persistente sul publisher che traccia la posizione di consumo dei WAL per ogni subscriber. Garantisce che nessuna modifica venga persa in caso di disconnessione temporanea, al costo di trattenere i segmenti WAL fino al consumo.
