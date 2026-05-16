---
title: "Annotations"
description: "Sistema di metadati Oracle 23ai che permette di associare coppie chiave/valore a oggetti dello schema (colonne, domain, tabelle), letti via USER_ANNOTATIONS_USAGE."
translationKey: "glossary_oracle_annotations"
aka: "Annotations (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

Le **Annotations** sono un sistema di metadati introdotto in Oracle Database 23ai che permette di associare **coppie chiave/valore** a oggetti dello schema: colonne, SQL Domain, tabelle, viste. Sono leggibili dal motore via le viste `USER_ANNOTATIONS_USAGE`, `DBA_ANNOTATIONS_USAGE`, `ALL_ANNOTATIONS_USAGE`.

## Come funziona

Si dichiarano direttamente nel `CREATE` (o `ALTER`) dell'oggetto, dentro la clausola `ANNOTATIONS (...)`. Ogni coppia ha la forma `nome 'valore'`. Esempio in un dominio:

```sql
CREATE DOMAIN stato_polizza AS VARCHAR2(20)
  CONSTRAINT chk CHECK (VALUE IN ('EMESSA','IN_VIGORE','SOSPESA'))
  ANNOTATIONS (
    display 'Stato Polizza',
    description 'Ciclo di vita di una polizza',
    ordering 'EMESSA<IN_VIGORE<SOSPESA'
  );
```

I valori vengono memorizzati nel dizionario dati senza essere interpretati dal motore — sono semantica, non vincolo. Una query su `USER_ANNOTATIONS_USAGE` permette di estrarli a runtime.

## A cosa servono

Centralizzare nel dizionario dello schema i metadati che fino a 23ai vivevano in tabelle applicative separate o in file di configurazione esterni. Strumenti BI (Power BI, Tableau), framework di UI generation e procedure di reportistica possono leggere direttamente le annotazioni del database per derivare etichette di display, descrizioni di campo, ordering logico — senza richiedere un mapping manuale.

## Cosa le distingue da COMMENT

`COMMENT ON COLUMN` (presente da decenni in Oracle) permette di associare una sola stringa di testo libero a un oggetto. Le `ANNOTATIONS` sono **strutturate**: chiavi distinte, valori interrogabili come campi tabulari, supporto a più annotazioni per oggetto. Un `COMMENT` resta utile per la documentazione testuale; le `ANNOTATIONS` sono adatte a metadati che gli strumenti devono leggere e usare automaticamente.
