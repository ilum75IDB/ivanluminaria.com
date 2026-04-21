---
title: "Data Mart"
description: "Sottoinsieme del data warehouse focalizzato su un singolo processo di business o area funzionale. Spesso costruito in autonomia da un reparto."
translationKey: "glossary_data_mart"
aka: "Departmental Data Mart, Subject-Area Data Mart"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Data Mart** è un sottoinsieme di un data warehouse focalizzato su un singolo processo di business, un'area funzionale (vendite, marketing, finance) o un reparto aziendale. Contiene tipicamente una o poche fact table e le dimensioni ad esse collegate.

## Perché esistono i data mart

Nella realtà aziendale un DWH enterprise completo richiede anni di progetto. I data mart nascono come compromesso pragmatico: si costruisce prima il pezzo che serve subito a un reparto (es. un data mart vendite per il marketing), e lo si integra con gli altri in un secondo momento. È l'approccio bottom-up di Kimball.

## Rischio di divergenza

Quando più data mart vengono costruiti in autonomia dai singoli reparti — spesso con strumenti BI diversi, su sistemi sorgenti diversi, con tempistiche diverse — il rischio è che "cliente" significhi tre cose diverse nei tre data mart. I totali non coincidono, le analisi cross-reparto diventano impossibili o lente, e il CFO si ritrova con tre versioni della verità.

## Data mart conforme vs indipendente

La differenza critica è se il data mart condivide o no le dimensioni conformi:

- **Data mart conformi** (Kimball): condividono dimensioni conformi (cliente, prodotto, tempo, geografia) e quindi possono essere interrogati insieme in modo coerente
- **Data mart indipendenti**: costruiti senza governance comune, divergono nel tempo e generano i classici problemi di "tre versioni della verità"

La bus matrix è lo strumento di progettazione che previene il secondo scenario.

## Quando ha senso

Un data mart ha senso quando:

- Il perimetro funzionale è ben definito (un processo, un reparto)
- Le dimensioni conformi sono già disponibili o vanno costruite contestualmente
- Il costo di un DWH enterprise completo non è giustificato
- Serve un time-to-value rapido per un caso d'uso specifico

Non ha senso invece come "soluzione permanente isolata": o è il primo pezzo di una strategia integrata, o diventa debito tecnico nel giro di pochi anni.
