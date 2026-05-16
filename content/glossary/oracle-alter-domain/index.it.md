---
title: "ALTER DOMAIN"
description: "Comando Oracle 23ai che modifica un SQL Domain (vincolo CHECK, DEFAULT, annotations) propagando il cambiamento a tutte le colonne che usano il dominio."
translationKey: "glossary_oracle_alter_domain"
aka: "ALTER DOMAIN (Oracle 23ai)"
articles:
  - "/posts/oracle/enum-oracle-workaround-fino-a-23ai"
---

`ALTER DOMAIN` è il comando Oracle Database 23ai che **modifica un SQL Domain esistente** — il vincolo `CHECK`, il valore di `DEFAULT`, le `ANNOTATIONS` — propagando il cambiamento a tutte le colonne che hanno dichiarato quel dominio come tipo. È quello che rende il SQL Domain una vera alternativa alla lookup table, non un semplice `CHECK` riusabile.

## Come funziona

`ALTER DOMAIN nome_dominio CONSTRAINT chk_X CHECK (VALUE IN (...))` aggiorna il vincolo del dominio. Oracle ricerca automaticamente tutte le colonne dichiarate con `nome_dominio` (in qualunque tabella e schema, secondo le grant) e applica il nuovo vincolo. Le righe esistenti possono essere validate (`VALIDATE`) o lasciate come sono (`NOVALIDATE`), a discrezione di chi gestisce la migrazione.

## A cosa serve

Sostituire decine di `ALTER TABLE` con una sola operazione. Quando il dominio di una colonna è usato su 20 tabelle e va aggiunto un nuovo valore ammesso, prima della 23ai bisognava modificare 20 `CHECK` distinti — con `ALTER DOMAIN` è una sola istruzione. Vale anche per modifiche al `DEFAULT` o alle `ANNOTATIONS`.

## Cosa cambia rispetto ad ALTER TABLE

`ALTER TABLE ... MODIFY CONSTRAINT` agisce su un singolo vincolo di una singola tabella. `ALTER DOMAIN` agisce su tutte le colonne, in tutte le tabelle, che ereditano il dominio. È la differenza tra un'operazione locale e un'operazione di schema-wide governance.
