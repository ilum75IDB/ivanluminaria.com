---
title: "Session pooling"
description: "Mod de pooling în care o conexiune backend rămâne alocată clientului pe toată durata sesiunii: mai compatibil, dar mai puțin eficient decât transaction pooling."
translationKey: "glossary_session_pooling"
aka: "Session-level pooling"
articles:
  - "/posts/postgresql/pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600"
---

În session pooling, o conexiune backend este rezervată unui client din momentul conectării până la deconectare. Este modul cel mai apropiat de comportamentul unei conexiuni directe și oferă cea mai mare compatibilitate cu funcționalitățile care depind de starea sesiunii: variabile `SET`, cursoare, tabele temporare și prepared statements cu nume.

## Cum funcționează

Managerul de pool (de exemplu PgBouncer) alocă o conexiune backend clientului la autentificare și o menține rezervată exclusiv pe toată durata sesiunii. Niciun alt client nu o poate folosi între timp, chiar dacă clientul este idle.

Configurare în PgBouncer:

```ini
[pgbouncer]
pool_mode = session
```

Numărul maxim de conexiuni simultane la baza de date este egal cu numărul de clienți activi, ceea ce limitează câștigul de eficiență față de conexiunile directe.

## Când se folosește

Session pooling este alegerea potrivită când aplicația folosește funcționalități care necesită stare persistentă de sesiune: ORM-uri care emit `SET search_path`, drivere care folosesc prepared statements cu nume sau cod legacy care se așteaptă ca variabilele de sesiune să supraviețuiască între interogări.

Este mai puțin eficient decât transaction pooling deoarece backend-ul rămâne ocupat chiar și în perioadele de inactivitate ale clientului. În scenarii cu concurență ridicată, avantajul principal față de conexiunile directe este reducerea overhead-ului de autentificare și a numărului de procese backend — nu o multiplexare reală a conexiunilor.
