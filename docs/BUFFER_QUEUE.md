# Buffer queue — articoli schedulati su LinkedIn via MCP

File di tracking idempotenza per i post LinkedIn schedulati tramite il server MCP ufficiale di Buffer (`https://mcp.buffer.com/mcp`).

**Aggiornato automaticamente da Claude** dopo ogni operazione di schedule riuscita. Letto **prima** di ogni nuovo scheduling per evitare duplicati. Se uno slug compare già in "Coda corrente" o "Storico", lo scheduling viene saltato con messaggio esplicito all'utente.

## Slot Buffer di riferimento

| Tipo post | Slot standard | Slot festività italiane |
|---|---|---|
| **Main** (annuncio articolo)   | Martedì 10:15 CET | Mercoledì 16:20 CET |
| **Teaser** (anticipa il martedì successivo) | Venerdì 15:20 CET | Giovedì 17:10 CET |

Per il calcolo dello slot a partire dalla data di pubblicazione `D` dell'articolo:

- **Main post** → `D` 10:15 CET (con shift mercoledì 16:20 se `D` è festività italiana)
- **Teaser post** → venerdì precedente a `D` (`D − 4 giorni`) alle 15:20 CET (con shift giovedì 17:10 se quel venerdì è festività)

Le festività italiane sono in `docs/HOLIDAYS_CALENDAR.md`.

## Capacità Buffer Free Plan

- 3 canali simultanei connessi (lifetime max 8 unique connections)
- **10 post in coda per canale**

Con cadenza 2 post/settimana (1 main + 1 teaser), la coda LinkedIn satura dopo 5 settimane. Mantenendo il ritmo settimanale (1 articolo nuovo → 2 nuovi post, ma nel frattempo 2 post sono andati live), il bilancio resta stabile a ~10.

## Coda corrente

_Nessun articolo schedulato. La tabella verrà popolata al primo scheduling via MCP Buffer._

| Slug articolo | Data pubblicazione | Teaser post_id | Teaser scheduled_at | Main post_id | Main scheduled_at | Schedulato il |
|---|---|---|---|---|---|---|

## Storico (post pubblicati)

_Gli entry vengono spostati qui dopo che il post Buffer è andato live (status `published`). Manutenzione manuale o via comando "aggiorna stato coda Buffer"._

| Slug articolo | Teaser publicato il | Main pubblicato il | URL articolo |
|---|---|---|---|

## Note operative

- I `post_id` sono gli ID interni di Buffer (non gli URL LinkedIn). Servono per query/update/delete via MCP.
- Se uno slot calcolato è già occupato in coda Buffer (verifica preliminare via MCP `get_scheduled_posts`), Claude segnala il conflitto e chiede istruzioni — non sovrascrive mai automaticamente.
- Per cancellare un post schedulato: comando esplicito "cancella post Buffer di articolo X" → Claude usa MCP `delete_post` e rimuove l'entry da questo file.
