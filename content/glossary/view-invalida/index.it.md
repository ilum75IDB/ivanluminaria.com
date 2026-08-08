---
title: "View invalida"
description: "Vista MySQL il cui corpo SQL referenzia oggetti non più esistenti o accessibili: tabelle rinominate, colonne eliminate, permessi revocati."
translationKey: "glossary_view_invalida"
aka: "Vista corrotta, Broken view"
articles:
  - "/posts/mysql/articolo-mysql-patching-mysql-8-0-dal-backup-alla-verifica-passo-per-passo"
---

Una **view invalida** è una vista il cui corpo SQL fa riferimento a oggetti non più esistenti o non accessibili: tabelle rinominate, colonne eliminate, permessi revocati. MySQL non invalida automaticamente le view quando la tabella sottostante viene modificata, quindi l'errore rimane silente fino alla prima esecuzione della vista o durante un `mysqldump`.

## Come funziona

MySQL memorizza il testo SQL della view in `information_schema.VIEWS` al momento della creazione, ma non mantiene dipendenze tracciate a runtime. Se una tabella referenziata viene rinominata o una colonna viene eliminata con `ALTER TABLE ... DROP COLUMN`, la view continua a esistere nel catalogo senza alcun segnale di errore.

```sql
-- Verifica rapida dello stato delle view nel database corrente
SELECT table_name, is_updatable
FROM information_schema.VIEWS
WHERE table_schema = DATABASE();

-- Tentativo di accesso che espone l'invalidità
SELECT * FROM nome_view;
-- ERROR 1356 (HY000): View 'db.nome_view' references invalid table(s) or column(s)
```

## Contesto operativo

Il problema emerge tipicamente in tre scenari: durante un **patching** o una migrazione di schema, dopo un `RENAME TABLE` eseguito senza aggiornare le view dipendenti, oppure durante un dump con `mysqldump --routines` che tenta di esportare la definizione. In quest'ultimo caso il dump può completarsi ma il restore fallisce o produce warning difficili da tracciare. Prima di qualsiasi operazione di manutenzione è buona pratica eseguire una verifica sistematica delle view con `CHECK TABLE nome_view` o interrogando `information_schema`.
