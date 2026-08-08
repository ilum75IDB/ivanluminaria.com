---
title: "Lexer"
description: "Componente Oracle Text che suddivide il testo in token durante l'indicizzazione, applicando regole di normalizzazione per lingua e formato."
translationKey: "glossary_lexer"
aka: "Lexer (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Il Lexer è il componente di Oracle Text responsabile dell'analisi testuale durante la fase di indicizzazione. Riceve il testo grezzo di un documento o di una colonna e lo suddivide in token — le unità atomiche su cui si costruisce l'indice — applicando regole di normalizzazione che variano in base alla lingua e al tipo di contenuto.

## Come funziona

Il Lexer opera prima che i token vengano scritti nell'indice invertito. Le sue responsabilità principali sono la tokenizzazione (dove spezzare il testo), la normalizzazione (come trasformare ogni token) e la gestione dei caratteri speciali.

Oracle Text mette a disposizione diversi tipi di Lexer. Il più comune per testi in linguaggio naturale è `BASIC_LEXER`, configurabile tramite `CTX_DDL.SET_ATTRIBUTE`:

```sql
BEGIN
  CTX_DDL.CREATE_PREFERENCE('my_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'MIXED_CASE', 'NO');
END;
/
```

L'attributo `BASE_LETTER YES` istruisce il Lexer a ridurre i caratteri accentati alla loro forma base (es. `è` → `e`, `ü` → `u`), rendendo le ricerche insensibili agli accenti — comportamento essenziale per l'italiano e molte altre lingue europee.

## Quando si usa

La scelta e la configurazione del Lexer impatta direttamente la qualità delle ricerche full-text. Occorre definire un Lexer personalizzato quando:

- il corpus contiene testi in lingue con accenti o caratteri non ASCII (italiano, francese, tedesco, spagnolo);
- si indicizzano URL, codici prodotto o identificatori tecnici che non devono essere spezzati come parole comuni;
- si vuole controllare la case-sensitivity dei token.

Il Lexer viene associato all'indice al momento della sua creazione tramite il parametro `LEXER` nella clausola `PARAMETERS` di `CREATE INDEX`. Una volta creato l'indice, modificare il Lexer richiede una reindicizzazione completa.
