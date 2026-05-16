---
title: "ALTER DOMAIN"
description: "Comandă Oracle 23ai care modifică un SQL Domain (constrângere CHECK, DEFAULT, annotations) propagând schimbarea la toate coloanele care folosesc domeniul."
translationKey: "glossary_oracle_alter_domain"
aka: "ALTER DOMAIN (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

`ALTER DOMAIN` este comanda Oracle Database 23ai care **modifică un SQL Domain existent** — constrângerea `CHECK`, valoarea `DEFAULT`, `ANNOTATIONS` — propagând schimbarea la toate coloanele care au declarat acel domeniu ca tip. Este ceea ce face din SQL Domain o alternativă reală la lookup table, nu un simplu `CHECK` reutilizabil.

## Cum funcționează

`ALTER DOMAIN nume_domeniu CONSTRAINT chk_X CHECK (VALUE IN (...))` actualizează constrângerea domeniului. Oracle caută automat toate coloanele declarate cu `nume_domeniu` (în orice tabel și schemă, conform grant-urilor) și aplică noua constrângere. Rândurile existente pot fi validate (`VALIDATE`) sau lăsate cum sunt (`NOVALIDATE`), la discreția celui care gestionează migrarea.

## La ce servește

Înlocuirea a zeci de `ALTER TABLE` cu o singură operație. Când domeniul unei coloane este folosit pe 20 de tabele și trebuie adăugată o nouă valoare admisă, înainte de 23ai trebuiau modificate 20 de `CHECK`-uri distincte — cu `ALTER DOMAIN` este o singură instrucțiune. Se aplică și modificărilor la `DEFAULT` sau la `ANNOTATIONS`.

## Ce se schimbă față de ALTER TABLE

`ALTER TABLE ... MODIFY CONSTRAINT` acționează asupra unei singure constrângeri a unui singur tabel. `ALTER DOMAIN` acționează asupra tuturor coloanelor, în toate tabelele, care moștenesc domeniul. Este diferența între o operație locală și o operație de schema-wide governance.
