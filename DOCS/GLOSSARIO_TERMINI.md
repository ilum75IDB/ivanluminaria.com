# Glossario Termini — Database Strategy Blog

Tabella centralizzata di tutti i termini tecnici e acronimi presenti nelle sezioni Glossario degli articoli del blog.

## Come usare questo file

- Ogni volta che si scrive un nuovo articolo con la sezione Glossario, aggiungere qui i termini nuovi
- Se un termine esiste gia, aggiornare solo la colonna **Contenuto in** aggiungendo il nuovo articolo
- I termini sono ordinati alfabeticamente
- La colonna **Contenuto in** elenca gli slug degli articoli (link relativi alla sezione)

## Tabella Termini

| Termine | Descrizione | Contenuto in |
|---------|-------------|--------------|
| ANALYZE | Comando PostgreSQL che raccoglie statistiche sulla distribuzione dei dati nelle tabelle, usate dall'optimizer per scegliere il piano di esecuzione | explain-analyze-postgresql |
| AWR | Automatic Workload Repository — strumento diagnostico integrato in Oracle Database per la raccolta e l'analisi delle statistiche di performance | oracle-awr-ash |
| default_statistics_target | Parametro PostgreSQL che definisce quanti campioni raccogliere per colonna durante l'ANALYZE. Il default è 100; su colonne con distribuzione asimmetrica conviene alzarlo a 500-1000 | explain-analyze-postgresql |
| ETL | Extract, Transform, Load — processo di estrazione, trasformazione e caricamento dati dai sistemi sorgente al data warehouse | scd-tipo-2, ragged-hierarchies |
| Execution Plan | Sequenza di operazioni (scan, join, sort) che il database sceglie per risolvere una query SQL. Si visualizza con EXPLAIN e EXPLAIN ANALYZE | explain-analyze-postgresql |
| Hash Join | Strategia di join che costruisce una hash table dalla tabella più piccola e poi scansiona la più grande cercando corrispondenze con lookup O(1). Efficiente su grandi volumi senza indici | explain-analyze-postgresql |
| Nested Loop | Strategia di join che per ogni riga della tabella esterna cerca le corrispondenze nella tabella interna. Ideale per poche righe, disastrosa su grandi volumi | explain-analyze-postgresql |
| SCD | Slowly Changing Dimension — tecnica di data warehouse per tracciare le variazioni nel tempo dei dati nelle tabelle dimensionali | scd-tipo-2 |

---

**Ultimo aggiornamento**: 2026-03-18
**Totale termini**: 8
**Totale articoli con glossario**: 1
