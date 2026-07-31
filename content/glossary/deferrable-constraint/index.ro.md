---
title: "DEFERRABLE constraint"
description: "Constrângere de integritate a cărei verificare poate fi amânată până la COMMIT, în loc să fie executată după fiecare instrucțiune DML. Utilă în tranzacții multi-pas."
translationKey: "glossary_deferrable_constraint"
aka: "constrângere amânabilă"
articles:
  - "/posts/oracle/articolo-oracle-assertions-in-oracle-26ai"
---

Un DEFERRABLE constraint este o constrângere de integritate referențială sau de domeniu a cărei verificare poate fi amânată până la momentul COMMIT, în loc să fie declanșată imediat după fiecare instrucțiune DML. Aceasta permite tranzacției să traverseze stări intermediare temporar inconsistente, cu condiția că integritatea să fie restabilită înainte de închiderea tranzacției.

## Cum funcționează

O constrângere declarată `DEFERRABLE` poate opera în două moduri:

- `INITIALLY IMMEDIATE` — verificată după fiecare DML în mod implicit; poate fi amânată explicit prin `SET CONSTRAINT`.
- `INITIALLY DEFERRED` — amânată până la COMMIT în mod implicit.

```sql
ALTER TABLE comenzi
  ADD CONSTRAINT fk_client
  FOREIGN KEY (client_id) REFERENCES clienti(id)
  DEFERRABLE INITIALLY DEFERRED;

-- În interiorul tranzacției:
SET CONSTRAINT fk_client DEFERRED;
INSERT INTO comenzi (id, client_id) VALUES (1, 999); -- clientul 999 nu există încă
INSERT INTO clienti (id) VALUES (999);               -- acum există
COMMIT;                                              -- verificarea este trecută
```

## Când se folosește

Cazul de utilizare clasic este încărcarea datelor cu dependențe circulare sau inserarea rândurilor legate prin chei externe într-o ordine nedeterministă. Este frecvent întâlnit și în pipeline-uri de replicare și procese ETL unde ordinea de sosire a înregistrărilor nu este garantată.

**Limitare fundamentală**: un DEFERRABLE constraint nu este o Assertion. Acționează asupra rândurilor individuale sau a relațiilor predefinite între tabele, dar nu poate exprima predicate arbitrare între tabele, precum `CHECK (SELECT COUNT(*) FROM ...)`. Pentru acest nivel de expresivitate, Oracle 23ai introduce SQL Assertions native.
