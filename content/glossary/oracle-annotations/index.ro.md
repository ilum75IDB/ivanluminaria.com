---
title: "Annotations"
description: "Sistem de metadate introdus în Oracle 23ai care asociază perechi cheie/valoare obiectelor de schemă (coloane, domain, tabele), citibile prin USER_ANNOTATIONS_USAGE."
translationKey: "glossary_oracle_annotations"
aka: "Annotations (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**Annotations** sunt un sistem de metadate introdus în Oracle Database 23ai care permite atașarea de **perechi cheie/valoare** obiectelor de schemă: coloane, SQL Domain, tabele, view-uri. Sunt citibile de motor prin view-urile `USER_ANNOTATIONS_USAGE`, `DBA_ANNOTATIONS_USAGE`, `ALL_ANNOTATIONS_USAGE`.

## Cum funcționează

Se declară direct în `CREATE` (sau `ALTER`)-ul obiectului, în interiorul clauzei `ANNOTATIONS (...)`. Fiecare pereche are forma `nume 'valoare'`. Exemplu pe un domain:

```sql
CREATE DOMAIN stare_polita AS VARCHAR2(20)
  CONSTRAINT chk CHECK (VALUE IN ('EMISA','IN_VIGOARE','SUSPENDATA'))
  ANNOTATIONS (
    display 'Stare Polița',
    description 'Ciclul de viață al unei polițe',
    ordering 'EMISA<IN_VIGOARE<SUSPENDATA'
  );
```

Valorile sunt stocate în dicționarul de date fără a fi interpretate de motor — sunt semantică, nu constrângere. O interogare pe `USER_ANNOTATIONS_USAGE` permite extragerea lor la runtime.

## La ce servesc

Centralizarea în dicționarul schemei a metadatelor care până la 23ai trăiau în tabele aplicative separate sau în fișiere de configurare externe. Instrumente BI (Power BI, Tableau), framework-uri de UI generation și proceduri de raportare pot citi direct anotările bazei de date pentru a deriva etichete de display, descrieri de câmp, ordering logic — fără a necesita un mapping manual.

## Ce le distinge de COMMENT

`COMMENT ON COLUMN` (prezent de zeci de ani în Oracle) permite asocierea unui singur șir de text liber unui obiect. `ANNOTATIONS` sunt **structurate**: chei distincte, valori interogabile ca câmpuri tabelare, suport pentru multiple anotări per obiect. Un `COMMENT` rămâne util pentru documentația textuală; `ANNOTATIONS` sunt potrivite pentru metadate pe care instrumentele trebuie să le citească și să le folosească automat.
