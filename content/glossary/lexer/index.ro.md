---
title: "Lexer"
description: "Componentă Oracle Text care împarte textul în tokeni în timpul indexării, aplicând reguli de normalizare specifice limbii și formatului."
translationKey: "glossary_lexer"
aka: "Lexer (Oracle Text)"
articles:
  - "/posts/oracle/oracle-text-indicizzare-e-ricercare-testo-in-modo-efficiente"
---

Lexer-ul este componenta Oracle Text responsabilă de analiza textuală în faza de indexare. Primește textul brut dintr-un document sau dintr-o coloană și îl împarte în tokeni — unitățile atomice pe care se construiește indexul inversat — aplicând reguli de normalizare care variază în funcție de limbă și tipul conținutului.

## Cum funcționează

Lexer-ul acționează înainte ca tokenii să fie scrisi în indexul inversat. Responsabilitățile sale principale sunt tokenizarea (unde să se dividă textul), normalizarea (cum să fie transformat fiecare token) și gestionarea caracterelor speciale.

Oracle Text pune la dispoziție mai multe tipuri de Lexer. Cel mai utilizat pentru text în limbaj natural este `BASIC_LEXER`, configurabil prin `CTX_DDL.SET_ATTRIBUTE`:

```sql
BEGIN
  CTX_DDL.CREATE_PREFERENCE('my_lexer', 'BASIC_LEXER');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'BASE_LETTER', 'YES');
  CTX_DDL.SET_ATTRIBUTE('my_lexer', 'MIXED_CASE', 'NO');
END;
/
```

Atributul `BASE_LETTER YES` instruiește Lexer-ul să reducă caracterele accentuate la forma lor de bază (ex. `è` → `e`, `ü` → `u`), făcând căutările insensibile la accente — comportament esențial pentru română, italiană și alte limbi europene.

## Când se folosește

Alegerea și configurarea Lexer-ului influențează direct calitatea căutărilor full-text. Un Lexer personalizat este necesar atunci când:

- corpusul conține texte în limbi cu accente sau caractere non-ASCII (română, italiană, franceză, germană);
- se indexează URL-uri, coduri de produs sau identificatori tehnici care nu trebuie fragmentați ca și cuvinte obișnuite;
- este necesară controlul explicit al sensibilității la majuscule și minuscule a tokenilor.

Lexer-ul este asociat indexului la momentul creării acestuia prin parametrul `LEXER` din clauza `PARAMETERS` a instrucțiunii `CREATE INDEX`. Odată creat indexul, modificarea Lexer-ului necesită o reindexare completă.
