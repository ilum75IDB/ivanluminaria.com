---
title: "VALIDATE / NOVALIDATE"
description: "Moduri Oracle de aplicare a unei constrângeri la crearea sau modificarea ei: VALIDATE verifică toate rândurile existente, NOVALIDATE sare peste verificare."
translationKey: "glossary_oracle_validate_novalidate"
aka: "Constraint validation modes (Oracle)"
articles:
  - "/posts/oracle/enum-oracle-19c-26ai-domini"
---

**`VALIDATE`** și **`NOVALIDATE`** sunt cele două moduri în care Oracle Database aplică o constrângere (CHECK, FK, UNIQUE, NOT NULL, și din 23ai și `SQL DOMAIN`) la momentul **creării sau modificării constrângerii**. Diferența privește doar **rândurile deja prezente** în tabel: tot ceea ce este inserat sau actualizat după este întotdeauna verificat de motor.

## Cum funcționează

Se specifică ca opțiune de clauză la `CREATE TABLE`, `ALTER TABLE ADD CONSTRAINT`, `ALTER TABLE MODIFY` sau `ALTER DOMAIN`. `VALIDATE` (default) face o **scanare completă** a tabelului pentru a verifica dacă fiecare rând respectă constrângerea; dacă chiar și un singur rând o încalcă, operația eșuează cu `ORA-02293`. `NOVALIDATE` sare peste scanare și acceptă starea curentă "așa cum este": constrângerea este marcată ca aplicată în avans, dar dicționarul de date o semnalează ca **nevalidată** (`STATUS = ENABLED NOVALIDATE` în `DBA_CONSTRAINTS`).

## Când se folosește NOVALIDATE

Tipic pe **tabele foarte mari** în ferestre de mentenanță strânse, unde scanarea de validare ar costa ore de blocare. Se aplică `NOVALIDATE`, se garantează integritatea înainte, și se face un cleanup ulterior prin script batch în background. Comun în:

- Migrare schemă pe tabele istorice de sute de milioane de rânduri
- Adăugare CHECK pe o coloană `status` a unui fact table DWH
- Conversie a vechilor `CHECK` inline la `SQL DOMAIN` pe multe tabele (Oracle 23ai+)

## Ce de verificat după

Odată ce constrângerea este `ENABLED NOVALIDATE`, optimizatorul **nu o folosește pentru a optimiza interogări** (ex. pentru a elimina condiții imposibile), pentru că nu are garanție că rândurile istorice o respectă. Pentru a recupera planul optim, după ce au fost curățate datele istorice, merită executat un `ALTER TABLE ... ENABLE VALIDATE CONSTRAINT` care readuce constrângerea la stare pe deplin validă.
