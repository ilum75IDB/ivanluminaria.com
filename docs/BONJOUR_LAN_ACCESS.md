# Accesso LAN via Bonjour (mDNS) — ivanluminaria.com

Aprire la preview del sito Hugo **da un altro computer o dal telefono** sulla
stessa rete WiFi, con un nome parlante invece dell'IP del Mac:

```
http://ivanluminaria.local:1313/      # nome primario (lungo)
http://ilum.local:1313/               # alias breve (stesso servizio, 3 char come "www")
```

Pensato per revisione live del sito su smartphone/iPad **prima del publish su
GitHub Pages**. Quando attivo, il server espone su tutto il sito con
`--buildDrafts --buildFuture`: oltre ai post live vedi anche bozze e articoli
con data futura — perfetto per QA editoriale dal divano col cellulare.

## TL;DR — comandi

Con l'ambiente shell caricato (`workwww`), due manager parametrici stile
`wwwgo`:

**Annuncio LAN** — `wwwbonjour <cmd>`:

| Comando | Effetto |
|---|---|
| `wwwbonjour on` | Attiva l'annuncio LAN (load LaunchAgent) |
| `wwwbonjour off` | Disattiva l'annuncio (unload LaunchAgent) |
| `wwwbonjour status` | Stato annuncio + nomi pubblicati |
| `wwwbonjour test` | Risolve i due nomi via `dns-sd` (deve dare l'IP del Mac) |
| `wwwbonjour log [N]` / `logf` | Log dell'annuncio (ultime N righe / `tail -f`) |
| `wwwbonjour open` | Apre `http://ivanluminaria.local:1313/` |
| `wwwip` · `wwwopenlan` · `wwwopenshort` | IP del Mac · apri nome lungo · apri alias `ilum.local` |
| `wwwhelp -B` | Scheda help Bonjour nel menu |

**Server** — `wwwserver <cmd>` (il server dev'essere su per rispondere):

| Comando | Effetto |
|---|---|
| `wwwserver start` / `stop` / `restart` | Server LAN in **background** (bind `0.0.0.0:1313`, log su file) |
| `wwwserver status` | Stato (background / porta / LaunchAgent / URL) |
| `wwwserver fg` | Foreground LAN (stesso bind di `start`, blocca il terminale) |
| `wwwserver dev` | Foreground locale `127.0.0.1` = `hserve` (draft visibili, scheduled nascosti) |
| `wwwserver preview` | Foreground locale `127.0.0.1` = `hservepreview` (draft + scheduled visibili) |
| `wwwserver log [N]` / `logf` | Log del server (ultime N righe / `tail -f`) |
| `wwwserver enable` / `disable` | **LaunchAgent** persistente (parte al login) |
| `wwwhelp -S` | Scheda help Server nel menu |

Flusso tipico: `wwwserver start` → da un altro device apri
`http://ivanluminaria.local:1313/`. Il Bonjour è già attivo di suo
(LaunchAgent), non serve riattivarlo ogni volta.

## Come funziona

Due pezzi **indipendenti**:

1. **Bind di hugo server su `0.0.0.0`** (non più `127.0.0.1`) → Hugo ascolta su
   tutte le interfacce, quindi è raggiungibile dalla LAN. Gestito da `WWW_BIND`
   in [`scripts/shell/www_env.zsh`](../scripts/shell/www_env.zsh) (usato dal
   manager `wwwserver` — start/fg/enable).

2. **Annuncio mDNS dei nomi** → un LaunchAgent lancia lo script
   [`announce.sh`](../deploy/launchd/announce.sh) che pubblica, per ogni nome,
   un record `<nome>.local` → IP-LAN-del-Mac via `dns-sd -P`. Lo script gira in
   loop e **ri-annuncia da solo se l'IP cambia** (DHCP).

```
                 ┌──────────────────── Mac (IP-LAN, es. 192.168.1.x) ───────────────┐
 altro device    │  LaunchAgent ──► announce.sh 1313 ivanluminaria ilum             │
 (telefono/PC)   │     │              └─ dns-sd -P: ivanluminaria.local → IP         │
   │             │     │                 dns-sd -P: ilum.local          → IP         │
   │  http://ilum.local:1313                                                         │
   └────────────►│  hugo server  --bind 0.0.0.0 --port 1313  --baseURL ...           │
                 └──────────────────────────────────────────────────────────────────┘
```

> ⚠️ **La porta resta nell'URL**: il nome `.local` risolve a un **IP, non a una
> porta** (`ivanluminaria.local:1313`). Per nomi *senza* porta
> (`http://ivanluminaria.local`) servirebbe un reverse proxy (Caddy/nginx) su
> :80 che instrada per hostname — fuori scope per il workflow editoriale
> locale.

### Specificità Hugo — `--baseURL` è cruciale

A differenza degli altri progetti FastAPI (web-orchestrator, GMA, BCT, MFSC), il
manager passa al `hugo server` di LAN questi flag extra:

```
--baseURL "http://ivanluminaria.local:1313/" --appendPort=false --liveReloadPort=1313
```

- **`--baseURL`**: Hugo genera URL **assoluti** nei link interni del sito
  basandosi su `baseURL`. Senza override a runtime, un visitatore dal cellulare
  cliccando un link nel sito viene rimandato a `http://localhost:1313/...`
  invece di `http://ivanluminaria.local:1313/...` → 404.
- **`--appendPort=false`**: senza questo Hugo appende automaticamente la porta
  al baseURL, generando href con `:1313:1313/` duplicato.
- **`--liveReloadPort=1313`**: forza la live-reload del browser (WebSocket) sulla
  stessa porta 1313. Senza questo flag Hugo sceglie una porta random per il WS,
  che dal cellulare non si connette.

I flag `--buildDrafts --buildFuture` sono attivi anche in LAN: la modalità di
default è "vedi tutto" (drafts + scheduled), allineata al caso d'uso QA
editoriale pre-publish.

### E se l'IP del Mac cambia?

**Funziona lo stesso.** L'IP **non è scritto** da nessuna parte nella
configurazione: il plist passa solo porta + nomi, e `announce.sh` ricava l'IP
dal vivo con `ipconfig getifaddr`. Lo script gira in loop e **ogni 30 secondi**
controlla l'IP corrente: se è cambiato (es. nuovo lease DHCP), **ri-annuncia
automaticamente** entrambi i nomi sul nuovo IP. Con `KeepAlive` il LaunchAgent
riparte anche dopo riavvio/sospensione del Mac.

Tempi: finestra ≤30s tra il cambio IP e il ri-annuncio; il device che accede può
tenere in cache il vecchio IP per il TTL mDNS (~4 min), di norma basta
ricaricare. Per **zero churn**, opzionale: una *DHCP reservation* sul router
(IP fisso per il Mac via MAC address).

## Architettura "copia di riferimento" vs "attivo"

Stesso modello di `zshrc.txt`: i file nel repo sono **copie versionate di
riferimento**; i file **attivi** vivono fuori dal repo.

| Ruolo | Path attivo (fuori repo) | Riferimento (nel repo) |
|---|---|---|
| Script annuncio (condiviso da TUTTI i progetti) | `~/Library/Application Support/bonjour-lan/announce.sh` | [`deploy/launchd/announce.sh`](../deploy/launchd/announce.sh) |
| LaunchAgent Bonjour | `~/Library/LaunchAgents/com.ivanluminaria.bonjour.www.plist` | [`deploy/launchd/com.ivanluminaria.bonjour.www.plist`](../deploy/launchd/com.ivanluminaria.bonjour.www.plist) |
| LaunchAgent server Hugo (opzionale) | `~/Library/LaunchAgents/com.ivanluminaria.www.plist` | [`deploy/launchd/com.ivanluminaria.www.plist`](../deploy/launchd/com.ivanluminaria.www.plist) |
| Log Bonjour | `~/Library/Logs/bonjour-lan/ivanluminaria.com.log` | — |
| Log server Hugo | `~/Library/Logs/ivanluminaria.com/server.log` | — |

## Installazione (una tantum)

```sh
# 1. Script condiviso (una volta sola sul Mac, vale per tutti i progetti)
mkdir -p ~/Library/"Application Support"/bonjour-lan ~/Library/Logs/bonjour-lan
cp deploy/launchd/announce.sh ~/Library/"Application Support"/bonjour-lan/announce.sh
chmod +x ~/Library/"Application Support"/bonjour-lan/announce.sh

# 2. LaunchAgent Bonjour di questo progetto
cp deploy/launchd/com.ivanluminaria.bonjour.www.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/com.ivanluminaria.bonjour.www.plist

# 3. (Opzionale) LaunchAgent server Hugo persistente
wwwserver enable
```

Oppure, per il Bonjour: `wwwbonjour on` (presuppone che il plist sia già copiato
in `~/Library/LaunchAgents/`).

## Verifica

```sh
wwwbonjour test                          # risolve ivanluminaria.local + ilum.local
dns-sd -G v4 ivanluminaria.local         # deve stampare l'IP LAN del Mac
ping -c1 ilum.local                       # deve rispondere

# Server attivo + sito raggiungibile sui due nomi
wwwserver start
curl -o /dev/null -w "%{http_code}\n" http://ivanluminaria.local:1313/   # atteso: 200
curl -o /dev/null -w "%{http_code}\n" http://ilum.local:1313/            # atteso: 200

# Verifica che i link interni puntino ai nomi .local, non a localhost
curl -s http://ivanluminaria.local:1313/ | grep -o 'href="[^"]*"' | head -5

# Da un altro device sulla LAN: apri http://ivanluminaria.local:1313/
```

**Firewall**: se il Firewall applicativo di macOS è attivo, al primo avvio di
`hugo server` su `0.0.0.0` macOS chiede di autorizzare le connessioni in
entrata per `hugo` — confermare. (Impostazioni di Sistema → Rete → Firewall.)

## Sicurezza / scope

- **Hugo NON ha auth** → esposizione LAN espone **tutto** il sito (anche bozze
  `--buildDrafts` e post futuri `--buildFuture`). Per la WiFi domestica privata
  di Ivan è accettabile (single-user, rete trust).
- **Scenari "ospiti in casa"**: spegnere il LaunchAgent server
  (`wwwserver disable`) o il `wwwserver stop` del background, e tornare al
  workflow puramente locale `hserve` / `wwwserver dev`.
- I link `--baseURL` puntano a `ivanluminaria.local`: non sono navigabili
  dall'esterno della LAN comunque, anche se qualcuno li ottenesse.

## Replica su un altro progetto (pattern multi-progetto)

Ogni progetto di Ivan gira su una porta diversa (GMA :8001, web-orchestrator
:8002, BCT :8004, MFSC :8005, ivanluminaria.com :1313…) e può avere i suoi
nomi `.local`. Per aggiungerne uno:

1. Lo `announce.sh` condiviso è già installato → **non va ri-copiato**.
2. Duplica il plist Bonjour cambiando **3 cose**:
   - `Label` → `com.ivanluminaria.bonjour.<nuovo-progetto>`
   - i `ProgramArguments` → `<porta> <nome1> [nome2 ...]`
     (es. `8001 gma`, oppure `8004 bct business-tracker`)
   - i due path di log
3. `cp` in `~/Library/LaunchAgents/` + `launchctl load -w …`.

| Progetto | Porta | Nomi `.local` |
|---|---|---|
| GMA | 8001 | `gma.local` |
| web-orchestrator | 8002 | `web-orchestrator.local`, `webo.local` |
| **ivanluminaria.com** | **1313** | **`ivanluminaria.local`, `ilum.local`** |
| BCT | 8004 | `bct.local` |
| MFSC | 8005 | `mfsc.local` |

> Nota: il device che accede deve supportare mDNS. macOS/iOS/iPadOS: nativo.
> Android 12+: nativo. Windows: serve "Bonjour Print Services" o usare l'IP
> diretto.

## File coinvolti nel repo

- [`deploy/launchd/announce.sh`](../deploy/launchd/announce.sh) — script annuncio (riferimento)
- [`deploy/launchd/com.ivanluminaria.bonjour.www.plist`](../deploy/launchd/com.ivanluminaria.bonjour.www.plist) — LaunchAgent Bonjour (riferimento)
- [`deploy/launchd/com.ivanluminaria.www.plist`](../deploy/launchd/com.ivanluminaria.www.plist) — LaunchAgent server Hugo (riferimento)
- [`scripts/shell/www_env.zsh`](../scripts/shell/www_env.zsh) — `WWW_BIND`, `WWW_BONJOUR_*`, wrapper `wwwserver`/`wwwbonjour`, alias LAN
- [`scripts/shell/www_server_manager.zsh`](../scripts/shell/www_server_manager.zsh) — sub-comandi `wwwserver`
- [`scripts/shell/www_bonjour_manager.zsh`](../scripts/shell/www_bonjour_manager.zsh) — sub-comandi `wwwbonjour`
- [`scripts/shell/www_help.zsh`](../scripts/shell/www_help.zsh) — schede help `wwwhelp -S` e `wwwhelp -B`

## Caveat tema Congo

Il tema Congo è un **Git submodule** — dopo un fresh clone serve
`git submodule update --init --recursive` (alias `themeupdate`) altrimenti
`hugo server` fallisce con "theme not found". Vale anche per la modalità LAN:
il LaunchAgent del server non sa nulla del submodule, lo dà per scontato.
