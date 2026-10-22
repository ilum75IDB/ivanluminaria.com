---
categories:
- postgresql
date: '2026-11-17'
description: 12 microservizi, 600 connessioni simultanee, PostgreSQL in ginocchio.
  Come PgBouncer ha ridotto le connessioni reali a 80 migliorando throughput e stabilità.
  Transaction pooling, prepared statements, parametri critici.
draft: false
image: pgbouncer-su-postgresql-transaction-pooling-parametri-critici-e-il-salto-da-600.cover.jpg
seoTitle: 'PgBouncer: da 600 a 80 connessioni PostgreSQL senza perdere throughput'
tags:
- pgbouncer
- connection-pooling
- postgresql
- performance
- scalability
title: 'PgBouncer su PostgreSQL: transaction pooling, parametri critici e il salto
  da 600 a 80 connessioni'
translationKey: pgbouncer_su_postgresql_transaction_pooling_parametri_critici_e_il_salto_da_600
webo_generated_at: 2026-10-22
webo_status: scheduled
---

## Seicento connessioni e un lunedì mattina

Il monitor di sistema mostrava numeri che non tornavano. Un'applicazione distribuita su dodici microservizi, ognuno configurato con il proprio pool interno da cinquanta connessioni verso PostgreSQL. Sulla carta: cinquanta per dodici fa seicento, ma in produzione le istanze scalavano orizzontalmente e i picchi portavano il totale ancora più in alto.

PostgreSQL non stava reggendo. Le query che normalmente completavano in pochi millisecondi aspettavano slot liberi per decine di secondi. Il load average del server era costantemente sopra dieci. La memoria era quasi esaurita — non per i dati, ma per i processi backend di PostgreSQL stessi.

Il team aveva già provato a ridurre i pool lato applicazione, ma ogni microservizio era sviluppato da un team diverso, con dipendenze e vincoli propri. Coordinare una riduzione uniforme avrebbe richiesto settimane. Serviva una soluzione a livello infrastrutturale.

Quella soluzione era PgBouncer.

## Perché PostgreSQL fatica con centinaia di connessioni

Prima di capire perché PgBouncer aiuta, vale la pena capire perché PostgreSQL soffre con molte connessioni simultanee — non è un difetto di configurazione, è architettura.

PostgreSQL usa un modello **process-per-connection**: ogni connessione client viene servita da un processo OS separato, con il proprio stack, la propria memoria privata e il proprio overhead di context switch. Su Linux, ogni backend PostgreSQL occupa tipicamente tra 5 e 10 MB di memoria privata (più la shared memory condivisa). Con seicento connessioni attive, stiamo parlando di 3-6 GB di RAM dedicati solo ai processi backend — prima ancora di eseguire una query.

Il problema si aggrava con il **context switching**. Lo scheduler del kernel deve gestire centinaia di processi che competono per i core CPU. Quando la maggior parte di questi processi è in attesa di I/O o di lock, il kernel passa tempo a fare scheduling invece che a eseguire lavoro utile. Il risultato è visibile nel load average: un server con otto core che mostra load average di dodici o quindici non sta facendo dodici volte il lavoro — sta sprecando cicli CPU in overhead di scheduling.

C'è anche il problema dei **lock e delle statistiche**. Ogni connessione, anche quando idle, mantiene strutture dati in memoria condivisa. Con seicento connessioni, operazioni come `VACUUM`, `ANALYZE` e la gestione dei lock diventano più costose perché devono attraversare strutture più grandi.

Il parametro `max_connections` di PostgreSQL esiste proprio per questo: non è un limite arbitrario, è una protezione contro il collasso del sistema [1].

## Cosa fa PgBouncer e come si posiziona nell'architettura

PgBouncer è un connection pooler leggero che si posiziona tra i client (i microservizi) e PostgreSQL. I client si connettono a PgBouncer come se fosse PostgreSQL — stessa porta, stesso protocollo. PgBouncer mantiene un pool ridotto di connessioni reali verso il database e le riutilizza tra i client.

Il punto chiave è che PgBouncer è scritto in C, è single-threaded con I/O asincrono (basato su `libevent`), e gestisce migliaia di connessioni client con un overhead minimo. Una singola istanza PgBouncer può reggere tranquillamente mille connessioni client usando poche decine di MB di RAM.

L'architettura risultante è questa:

```text
[Microservizio A] ──┐
[Microservizio B] ──┤                    ┌──────────────────┐
[Microservizio C] ──┼──► [PgBouncer] ───►│  PostgreSQL      │
[Microservizio D] ──┤    (porta 5432)    │  (80 connessioni)│
[Microservizio E] ──┘                    └──────────────────┘
  (600 connessioni client)
```

PgBouncer riceve le seicento connessioni client, ma verso PostgreSQL mantiene solo ottanta connessioni reali. Quando un client invia una query, PgBouncer assegna una connessione backend disponibile, esegue la query, e — a seconda della modalità di pooling — rilascia quella connessione per altri client.

## Transaction pooling vs session pooling: la scelta che cambia tutto

PgBouncer supporta tre modalità di pooling. Le due rilevanti in produzione sono **session pooling** e **transaction pooling**.

**Session pooling**: una connessione backend viene assegnata a un client per tutta la durata della sua sessione. Il backend viene rilasciato solo quando il client si disconnette. È la modalità più compatibile — funziona con tutto — ma offre il minor risparmio: se un client tiene aperta la sessione senza fare query, il backend è comunque occupato.

**Transaction pooling**: una connessione backend viene assegnata al client solo per la durata di una transazione. Appena la transazione termina (COMMIT o ROLLBACK), il backend torna nel pool e può essere assegnato a un altro client. Questa è la modalità che permette di servire seicento client con ottanta backend reali, perché nella pratica la maggior parte dei client è idle tra una transazione e l'altra.

La scelta tra le due non è banale. Transaction pooling ha vincoli importanti:

- Le **variabili di sessione** (`SET search_path`, `SET timezone`, ecc.) non persistono tra transazioni diverse
- I **prepared statements** nominati non funzionano in modo trasparente (ne parliamo nella sezione dedicata)
- Le **advisory lock** a livello di sessione non funzionano
- `LISTEN/NOTIFY` non è supportato in transaction pooling

Session pooling è più sicuro, ma richiede che i client si disconnettano quando non servono — cosa che i connection pool applicativi fanno già. In quel caso, il risparmio è reale ma meno drastico.

Nel nostro caso, i microservizi usavano un ORM standard senza prepared statements nominati, senza advisory lock, senza `LISTEN/NOTIFY`. Transaction pooling era la scelta giusta.

## Installazione e configurazione di base

Su una distribuzione Debian/Ubuntu recente, l'installazione è diretta [2]:

```bash
apt install pgbouncer
```

La configurazione vive in due file: `pgbouncer.ini` e `userlist.txt`.

### `pgbouncer.ini`

```ini
[databases]
; "appdb" è il nome del database virtuale esposto da PgBouncer
; i client si connettono a questo nome
appdb = host=127.0.0.1 port=5432 dbname=appdb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; modalità di pooling
pool_mode = transaction

; connessioni reali verso PostgreSQL per pool
default_pool_size = 80

; massimo connessioni client accettate da PgBouncer
max_client_conn = 1000

; pool di riserva per picchi
reserve_pool_size = 10
reserve_pool_timeout = 5

; timeout connessioni idle lato server
server_idle_timeout = 600

; log
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

; statistiche
stats_period = 60
```

### `userlist.txt`

Il file contiene le credenziali nel formato `"username" "password_hash"`. PgBouncer supporta hash MD5 nel formato PostgreSQL (`md5` + md5(password + username)):

```text
"app_user" "md5a1b2c3d4e5f6..."
"pgbouncer_admin" "md5..."
```

Per generare l'hash corretto:

```bash
echo -n "passwordusername" | md5sum
# prefissa "md5" al risultato
```

Dopo la configurazione, avviare PgBouncer e verificare che si connetta correttamente:

```bash
systemctl start pgbouncer
systemctl enable pgbouncer

# verifica connessione admin
psql -h 127.0.0.1 -p 5432 -U pgbouncer pgbouncer
```

## Da seicento a ottanta: i numeri prima e dopo

Dopo il deploy di PgBouncer in transaction pooling, i numeri sono cambiati in modo sostanziale. Alcune misurazioni rappresentative, raccolte nelle prime settimane:

| Metrica | Prima | Dopo |
|---|---|---|
| Connessioni reali a PostgreSQL | 580-620 | 65-80 |
| RAM occupata dai backend PG | ~4.2 GB | ~600 MB |
| Load average (8 core) | 12-18 | 3-5 |
| Latenza media query (p50) | 180 ms | 22 ms |
| Latenza p99 | 4.2 s | 310 ms |
| Timeout di connessione | frequenti | assenti |

La riduzione di latenza non è solo dovuta a meno contention sulle connessioni. Con meno processi backend attivi, il kernel fa meno context switching, PostgreSQL gestisce strutture dati più piccole, e `VACUUM` riesce a completare i suoi cicli senza essere continuamente interrotto. È un effetto a cascata.

Il throughput complessivo — query al secondo — è aumentato del 40% circa, nonostante il numero di connessioni reali fosse ridotto di quasi un ordine di grandezza. Questo è il punto che spesso sorprende: meno connessioni non significa meno lavoro fatto, significa meno overhead per unità di lavoro.

## Prepared statements e transaction pooling: il nodo da sciogliere

Il problema più comune quando si migra a PgBouncer in transaction pooling riguarda i **prepared statements**.

In PostgreSQL, i prepared statements nominati (`PREPARE nome AS ...`) sono legati alla sessione. In transaction pooling, ogni transazione può finire su un backend diverso — quindi un prepared statement creato in una transazione precedente non esiste sul nuovo backend.

Il risultato è un errore del tipo:

```text
ERROR: prepared statement "s1" does not exist
```

Ci sono tre approcci per gestirlo:

**1. Usare prepared statements anonimi (protocol-level)**

I driver moderni come `libpq`, `asyncpg`, `psycopg3` e JDBC supportano i prepared statements a livello di protocollo senza nome esplicito. PgBouncer gestisce questi in modo trasparente in transaction pooling. Se il framework usa questo meccanismo (la maggior parte degli ORM moderni lo fa), non c'è problema.

**2. Disabilitare i prepared statements lato applicazione**

Se il driver o l'ORM usa prepared statements nominati, la soluzione più semplice è disabilitarli. In SQLAlchemy, per esempio:

```python
engine = create_engine(
    "postgresql+psycopg2://user:pass@pgbouncer-host/appdb",
    execution_options={"no_parameters": True},
    # oppure con psycopg2:
    connect_args={"options": "-c statement_timeout=30000"}
)
```

Con JDBC e driver PostgreSQL:

```text
jdbc:postgresql://pgbouncer-host/appdb?prepareThreshold=0
```

`prepareThreshold=0` dice al driver di non usare mai prepared statements server-side.

**3. Usare `DEALLOCATE ALL` tra transazioni**

Meno elegante, ma funziona: configurare PgBouncer con `server_reset_query = DEALLOCATE ALL` per pulire i prepared statements quando un backend torna nel pool. Attenzione: questo aggiunge latenza ad ogni rilascio di connessione.

Nel nostro caso, i microservizi usavano SQLAlchemy con psycopg2 e prepared statements nominati. La soluzione è stata aggiungere `prepareThreshold=0` equivalente nella configurazione del driver — una modifica di due righe per servizio, deployata in un pomeriggio.

## I parametri critici da capire prima di andare in produzione

Tre parametri di `pgbouncer.ini` meritano attenzione specifica [3]:

**`default_pool_size`**: il numero di connessioni reali verso PostgreSQL per ogni coppia (database, utente). È il parametro più importante. Come sceglierlo? Una regola empirica: `num_cores * 2` come punto di partenza, poi misurare. Con otto core, si parte da sedici e si sale fino a trovare il punto di saturazione. Nel nostro caso, ottanta connessioni su un server con sedici core e SSD NVMe era il punto di equilibrio.

**`max_client_conn`**: il numero massimo di connessioni client che PgBouncer accetta in totale. Deve essere maggiore del numero di connessioni che i client possono aprire. Se i seicento client aprono una connessione ciascuno, `max_client_conn` deve essere almeno seicento, meglio mille per avere margine. Quando si supera questo limite, PgBouncer rifiuta nuove connessioni — meglio un errore esplicito che un timeout silenzioso.

**`reserve_pool_size`** e **`reserve_pool_timeout`**: il pool di riserva è un insieme di connessioni aggiuntive che PgBouncer può aprire quando il pool principale è esaurito. Se un client aspetta più di `reserve_pool_timeout` secondi per una connessione, PgBouncer attinge al reserve pool. È una rete di sicurezza per i picchi, non una soluzione strutturale: se il reserve pool si esaurisce regolarmente, `default_pool_size` va aumentato.

Un parametro spesso trascurato è **`server_idle_timeout`**: dopo quanti secondi di inattività PgBouncer chiude una connessione backend. Il default è seicento secondi (dieci minuti). In ambienti con traffico molto variabile — alto di giorno, quasi nullo di notte — abbassarlo a centocinquanta o duecento secondi riduce il numero di connessioni idle che PostgreSQL mantiene aperte nelle ore di bassa attività.

## Leggere i numeri: SHOW STATS e SHOW POOLS

PgBouncer espone una console di amministrazione accessibile connettendosi al database virtuale `pgbouncer`:

```bash
psql -h 127.0.0.1 -p 5432 -U pgbouncer_admin pgbouncer
```

Il comando più utile per il monitoraggio quotidiano è `SHOW STATS` [4]:

```sql
SHOW STATS;
```

```text
 database | total_xact_count | total_query_count | total_received | total_sent | total_xact_time | total_query_time | total_wait_time | avg_xact_count | avg_query_count | avg_recv | avg_sent | avg_xact_time | avg_query_time | avg_wait_time
----------+------------------+-------------------+----------------+------------+-----------------+------------------+-----------------+----------------+-----------------+----------+----------+---------------+----------------+---------------
 appdb    |        284721043 |         284721043 |   182043219872 | 9823041928 |    492831029183 |     492831029183 |      1823041928 |            312 |             312 |   199823 |    10782 |          1732 |           1732 |             6
```

Le colonne chiave: `avg_wait_time` (tempo medio di attesa per una connessione backend — se supera qualche millisecondo, il pool è troppo piccolo) e `avg_xact_time` (durata media delle transazioni).

`SHOW POOLS` mostra lo stato in tempo reale dei pool:

```sql
SHOW POOLS;
```

```text
 database | user     | cl_active | cl_waiting | sv_active | sv_idle | sv_used | sv_tested | sv_login | maxwait | maxwait_us | pool_mode
----------+----------+-----------+------------+-----------+---------+---------+-----------+----------+---------+------------+-----------
 appdb    | app_user |       412 |          0 |        78 |       2 |       0 |         0 |        0 |       0 |          0 | transaction
```

- `cl_active`: client con una connessione backend assegnata
- `cl_waiting`: client in attesa di una connessione backend — se questo numero è costantemente > 0, il pool è saturo
- `sv_active`: backend occupati
- `sv_idle`: backend liberi nel pool
- `maxwait`: tempo massimo di attesa di un client (in secondi) — l'indicatore di allarme principale

Per il monitoraggio automatico, questi valori si estraggono facilmente con qualsiasi sistema di metriche. Prometheus ha un exporter dedicato (`pgbouncer_exporter`) che espone tutte le metriche di `SHOW STATS` e `SHOW POOLS` in formato scrape [5].

## Quello che resta dopo il deploy

PgBouncer non è una soluzione magica e non elimina la necessità di progettare bene il layer di accesso ai dati. Se le query sono lente, PgBouncer non le accelera. Se il database ha problemi di lock, PgBouncer non li risolve. Quello che fa è rimuovere un collo di bottiglia specifico — l'overhead di gestione delle connessioni — che in architetture a microservizi diventa rapidamente il problema dominante.

La cosa che colpisce, guardando i numeri a posteriori, è quanto fosse semplice la diagnosi: il server aveva memoria sufficiente per i dati, CPU sufficiente per le query, I/O sufficiente per i write. Stava soffrendo per il puro overhead di gestire seicento processi OS contemporaneamente. PgBouncer ha spostato quel problema fuori da PostgreSQL, dove può essere gestito in modo molto più efficiente.

Un punto che vale la pena tenere a mente per architetture future: in un sistema con molti microservizi, il connection pooling non dovrebbe essere un'aggiunta a posteriori. Dovrebbe essere parte del design iniziale, al pari del load balancer o del service mesh. Il costo di aggiungerlo dopo — coordinare i team, gestire la migrazione, testare la compatibilità dei prepared statements — è reale, anche se alla fine gestibile.

Il team ha poi aggiunto PgBouncer come componente standard nel template di deploy per tutti i nuovi servizi. Non è più una decisione da prendere caso per caso.

## Fonti ufficiali

1. PostgreSQL Documentation — [Connections and Authentication: max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html)
2. PgBouncer Documentation — [Installation](https://www.pgbouncer.org/install.html)
3. PgBouncer Documentation — [Configuration file pgbouncer.ini](https://www.pgbouncer.org/config.html)
4. PgBouncer Documentation — [Usage: SHOW commands](https://www.pgbouncer.org/usage.html)
5. prometheus-community — [pgbouncer_exporter](https://github.com/prometheus-community/pgbouncer_exporter)

## Glossario
- **[PgBouncer](/it/glossary/pgbouncer/)** — Connection pooler leggero per PostgreSQL, scritto in C con I/O asincrono. Si posiziona tra i client e il database, mantenendo un pool ridotto di connessioni reali verso PostgreSQL e riutilizzandole tra molti client.

- **[Transaction pooling](/it/glossary/pgbouncer/)** — Modalità di pooling in cui una connessione backend viene assegnata al client solo per la durata di una transazione. Appena la transazione termina, il backend torna nel pool disponibile per altri client. Permette di servire molti client con poche connessioni reali.

- **[Session pooling](/it/glossary/transaction-pooling/)** — Modalità di pooling in cui una connessione backend rimane assegnata a un client per tutta la durata della sua sessione. Più compatibile del transaction pooling, ma meno efficiente perché il backend è occupato anche quando il client è idle.

- **[`max_connections`](/it/glossary/pgbouncer/)** (PostgreSQL) — Parametro di configurazione che limita il numero massimo di connessioni simultanee accettate da PostgreSQL. Non è un limite arbitrario: riflette il costo reale in memoria e overhead di scheduling di ogni processo backend.

- **[`default_pool_size`](/it/glossary/transaction-pooling/)** (PgBouncer) — Numero di connessioni reali verso PostgreSQL mantenute da PgBouncer per ogni coppia (database, utente). È il parametro principale per dimensionare il pool: troppo basso causa attese, troppo alto riporta il problema delle connessioni eccessive su PostgreSQL.
