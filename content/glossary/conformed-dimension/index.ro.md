---
title: "Conformed Dimension"
description: "Dimensiune partajată între mai multe data marts cu aceeași structură, semantică și cheie. Permite analize cross-proces coerente și însumabile."
translationKey: "glossary_conformed_dimension"
aka: "Dimensiune Conformă, Shared Dimension"
articles:
  - "/posts/data-warehouse/bus-matrix-terreno-comune"
---

**Conformed Dimension** (dimensiune conformă) este o dimensiune folosită în mai mult de o fact table sau un data mart cu aceeași structură, aceeași semantică și aceeași cheie. Este pilonul bus architecture-ului lui Kimball.

## Ce înseamnă "a conforma"

A conforma o dimensiune înseamnă a conveni asupra a trei elemente:

- **Cheia naturală unică**: ce identificator reprezintă entitatea (cod fiscal, cod client, cod produs, CUI)
- **Atributele partajate**: ce coloane sunt comune tuturor data marts-urilor care folosesc dimensiunea (țară, regiune, categorie, etc.)
- **Grain-ul**: nivelul de detaliu al dimensiunii (un rând per client, nu per segment)

Atributele specifice unui singur departament pot rămâne în tabele dimensionale locale, dar nu trebuie să intre în partea conformă a dimensiunii.

## La ce servește

Fără dimensiuni conforme, măsurile provenind din fact tables diferite nu se pot compara în mod fiabil. Cu dimensiuni conforme, o interogare care combină vânzări și campanii de marketing pe același client returnează un rezultat coerent pentru că "client" înseamnă același lucru în cele două procese.

## Implementare fizică

O dimensiune conformă nu trebuie să fie neapărat un singur tabel fizic partajat. Poate fi:

- **Replicată** în mai multe scheme (alegere pragmatică atunci când data marts-urile sunt pe baze de date diferite)
- **Centralizată** într-o schemă dedicată (ex. `dim_conformed`) cu viste sau sinonime în data marts
- **Virtualizată** prin instrumente de data virtualization

Ce contează este ca cele trei proprietăți — structură, semantică, cheie — să fie identice în fiecare copie.

## Când este nevoie de guvernanță

Menținerea conformității în timp necesită un comitet de guvernanță cu reprezentanți ai departamentelor care folosesc dimensiunea. Fiecare modificare (un atribut nou, o regulă de deduplicare nouă, un canal de achiziție nou) trebuie convenită și propagată în mod coordonat — altfel dimensiunile conforme divergă și întreaga construcție se prăbușește.
