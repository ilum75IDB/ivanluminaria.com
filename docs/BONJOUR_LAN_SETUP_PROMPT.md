# PROMPT — Accesso LAN (Bonjour) + manager shell server/bonjour (ivanluminaria.com)

> **Come usarlo**: in una sessione di Claude Code aperta su QUESTO progetto
> (ivanluminaria.com), di' a Claude: *"leggi ed esegui
> `docs/BONJOUR_LAN_SETUP_PROMPT.md`"*. Replica l'architettura già implementata
> e collaudata su **web-orchestrator** (`webo.local`), **GMA** (`gma.local`),
> **BCT** (`bct.local`), **MFSC** (`mfsc.local`), adattandola al caso
> particolare **Hugo static site server** (non un app Python).

---

## Obiettivo

Portare su ivanluminaria.com la stessa struttura di web-orchestrator, ma
specifica per `hugo server`:

1. **Accesso LAN** da altri device/telefono per anteprima del sito locale
   prima del publish: `http://ivanluminaria.local:1313/` (e alias breve
   `ilum.local`).
2. **Manager parametrico server** `wwwserver <cmd>` (stile `wwwgo`):
   `start|stop|restart|status|dev|preview|fg|log [N]|logf|enable|disable|svc|help`.
3. **Manager parametrico Bonjour** `wwwbonjour <cmd>`:
   `on|off|status|test|log|logf|open|help`.

## Parametri di questo progetto

| Parametro | Valore |
|---|---|
| Progetto | ivanluminaria.com (sito Hugo blog tecnico multilingue) |
| Path | `/Users/ivanluminaria/Development/APPLICAZIONI/My-Web-Site/ivanluminaria.com` |
| Prefisso shell | `www` (env `scripts/shell/www_env.zsh`, help `www_help.zsh`, go `www_go_manager.zsh`) |
| Stack | **Hugo extended** (no Python/Node, no FastAPI/uvicorn) |
| Porta | **1313** (Hugo default) |
| Nomi `.local` | `ivanluminaria.local` (primario) + `ilum.local` (alias breve, 3 char come il prefisso `www`) |
| Label LaunchAgent Bonjour | `com.ivanluminaria.bonjour.www` |
| Label LaunchAgent server | `com.ivanluminaria.www` |
| Dove gira | **localmente su questo Mac** (Galadriel) |

## Riferimento collaudato (template da cui copiare e adattare)

Leggi questi file di **web-orchestrator** (fonte autorevole, già testati e2e):

- `/Users/ivanluminaria/Development/APPLICAZIONI/My-Web-Site/web-orchestrator/docs/BONJOUR_LAN_ACCESS.md`
- `…/web-orchestrator/scripts/shell/webo_server_manager.zsh`  ← manager server parametrico (uvicorn)
- `…/web-orchestrator/scripts/shell/webo_bonjour_manager.zsh` ← manager bonjour parametrico
- `…/web-orchestrator/scripts/shell/webo_env.zsh`             ← variabili + wrapper functions
- `…/web-orchestrator/scripts/shell/webo_help.zsh`            ← schede help -S e -B
- `…/web-orchestrator/deploy/launchd/announce.sh`             ← script mDNS condiviso (già installato in `~/Library/Application Support/bonjour-lan/`)
- `…/web-orchestrator/deploy/launchd/com.ivanluminaria.bonjour.web-orchestrator.plist` ← LaunchAgent bonjour
- `…/web-orchestrator/deploy/launchd/com.ivanluminaria.web-orchestrator.plist`         ← LaunchAgent server

E per riferimento sui peer Hugo: nessuno — questo è il primo progetto Hugo
della famiglia. I 4 precedenti (`web-orchestrator`, `GMA`, `BCT`, `MFSC`)
sono tutti Python/FastAPI con uvicorn. Le **differenze chiave Hugo** sono
documentate nella sezione "Note / caveat per ivanluminaria.com" sotto.

## Istruzioni per Claude (esegui in ordine)

1. **Leggi i riferimenti** sopra e gli attuali `www_env.zsh` / `www_help.zsh` /
   `www_go_manager.zsh` di ivanluminaria.com per capire pattern e stile.
   Identifica gli alias esistenti `hserve` / `hservepreview` / `workwww` per
   non duplicarli.

2. **Verifica la porta reale**: dovrebbe essere `1313` (default Hugo). Cerca
   `--port`/`port` in `www_env.zsh` o nei file di config Hugo (`hugo.toml`,
   `config.toml`). Se diversa, adatta i valori sotto.

3. **Bind `0.0.0.0`**: Hugo usa il flag `--bind` (non `--host`!). In
   `www_env.zsh` introduci `WWW_BIND="0.0.0.0"` (lascia `WWW_HOST=127.0.0.1`
   per gli URL locali). **Conferma con l'utente** prima di esporre sulla LAN.

4. **`--baseURL` obbligatorio per LAN**: Hugo genera URL **assoluti** nei
   link interni del sito basandosi su `baseURL`. Se non lo riscrivi a runtime,
   un visitatore dal cellulare cliccando un link nel sito viene rimandato a
   `http://localhost:1313/...` invece di `http://ivanluminaria.local:1313/...`
   → 404. Soluzione: il manager passa sempre
   `--baseURL "http://ivanluminaria.local:1313/" --appendPort=false` quando
   bind è `0.0.0.0`. Per il dev fg locale puro lascia `--baseURL` di default.

5. **Variabili nuove** in `www_env.zsh`:
   ```zsh
   WWW_LOG_DIR="$HOME/Library/Logs/ivanluminaria.com"
   WWW_SERVER_LOG="$WWW_LOG_DIR/server.log"
   WWW_SERVER_PID="/tmp/www-server.pid"
   WWW_SERVER_LABEL="com.ivanluminaria.www"
   WWW_PORT=1313
   WWW_BIND="0.0.0.0"
   WWW_HOST="127.0.0.1"
   WWW_BONJOUR_HOSTNAME="ivanluminaria.local"
   WWW_BONJOUR_HOSTNAME_ALIAS="ilum.local"
   WWW_BONJOUR_LABEL="com.ivanluminaria.bonjour.www"
   WWW_BONJOUR_LOG="$WWW_LOG_DIR/bonjour.log"
   ```

6. **Manager server** `scripts/shell/www_server_manager.zsh` (adatta
   `webo_server_manager.zsh`): sub-comandi
   `start|stop|restart|status|dev|preview|fg|log [N]|logf|enable|disable|svc|help`.

   Particolarità Hugo (no uvicorn):
   - **start**: `nohup hugo server --bind "$WWW_BIND" --port "$WWW_PORT" --baseURL "http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/" --appendPort=false --buildDrafts --buildFuture >> $WWW_SERVER_LOG 2>&1 &` + PID file in `$WWW_SERVER_PID`
   - **stop**: `kill $(cat $WWW_SERVER_PID)` + rm PID
   - **dev**: foreground hugo server con `hserve` esistente (draft visibili,
     scheduled nascosti) → solo `127.0.0.1`
   - **preview**: foreground come `hservepreview` esistente (`--buildFuture`
     per articoli scheduled), bind 127.0.0.1
   - **fg**: foreground LAN (stesse opzioni di `start` ma in foreground per
     debug live-reload visibile)
   - **status**: PID + lsof porta + URL local + URL LAN + check baseURL
   - **enable/disable/svc**: install/uninstall LaunchAgent `WWW_SERVER_LABEL`

7. **Manager bonjour** `scripts/shell/www_bonjour_manager.zsh` (adatta
   `webo_bonjour_manager.zsh`): `on|off|status|test|log|logf|open|help`.
   Usa lo **stesso `announce.sh`** condiviso (`~/Library/Application Support/
   bonjour-lan/announce.sh`) — è multi-progetto, non duplicarlo.

   Sintassi: `announce.sh 1313 ivanluminaria` (nome Bonjour = "ivanluminaria"
   + alias "ilum"). Lo script gestisce la registrazione mDNS con
   `dns-sd -R`, e si auto-aggiorna se cambia l'IP DHCP.

   Il LaunchAgent (`com.ivanluminaria.bonjour.www.plist`) chiamerà
   `announce.sh` con 2 nomi (pattern già usato da webo per `web-orchestrator` +
   `webo`): registra entrambi `ivanluminaria.local` e `ilum.local` puntando
   allo stesso IP.

8. **Wrapper functions** in `www_env.zsh`:
   ```zsh
   wwwserver() { "$WWW_SHELL_DIR/www_server_manager.zsh" "$@"; }
   wwwbonjour() { "$WWW_SHELL_DIR/www_bonjour_manager.zsh" "$@"; }
   alias wwwopenlan="open http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/"
   alias wwwip='ipconfig getifaddr en0 || ipconfig getifaddr en1'
   ```
   **Lascia intatti** gli alias storici `hserve`/`hservepreview` (sono
   il workflow editoriale di Ivan), magari rifatti come scorciatoie a
   `wwwserver dev` / `wwwserver preview`.

9. **LaunchAgent di riferimento** in `deploy/launchd/`:
   - `com.ivanluminaria.bonjour.www.plist` → `ProgramArguments: ["~/Library/Application Support/bonjour-lan/announce.sh", "1313", "ivanluminaria", "ilum"]`
   - `com.ivanluminaria.www.plist` → server Hugo (vedi command in step 6) +
     `KeepAlive`, `RunAtLoad`, log path
   Copie attive in `~/Library/LaunchAgents/` via i comandi `enable`/`on` del
   manager (non installare manualmente).

10. **Help** `www_help.zsh`: aggiungi schede `-S` (server manager) e `-B`
    (bonjour manager) come in `webo_help.zsh`. Mantieni le sezioni esistenti
    (`-U`/`-N`/`-C`/`-G`/`-L`/`-V`/`-H`) e fai shift dei numeri solo se serve.

11. **Doc** `docs/BONJOUR_LAN_ACCESS.md` di ivanluminaria.com (adatta da
    web-orchestrator: porta `1313`, nomi `ivanluminaria.local`+`ilum.local`,
    prefisso `www`, specificità Hugo `--baseURL`).

12. **Verifica e2e**:
    ```bash
    # 1. Server start + bind LAN
    wwwserver start
    wwwserver status            # atteso: porta 1313 in ascolto + URL LAN
    curl -o /dev/null -w "%{http_code}\n" http://ivanluminaria.local:1313/   # atteso: 200
    curl -o /dev/null -w "%{http_code}\n" http://ilum.local:1313/            # atteso: 200

    # 2. Verifica baseURL nei link interni (deve puntare a ivanluminaria.local, non localhost)
    curl -s http://ivanluminaria.local:1313/ | grep -o 'href="[^"]*"' | head -5
    # atteso: nessun localhost/127.0.0.1; href devono iniziare con / o http://ivanluminaria.local

    # 3. Bonjour test
    wwwbonjour test             # risolve all'IP del Mac
    dns-sd -B _http._tcp local. | grep -i ivan   # vede l'annuncio

    # 4. Smartphone (sulla stessa WiFi): apri Safari → http://ivanluminaria.local:1313/
    # Naviga il sito, verifica che il selettore lingua + i link articoli funzionino

    # 5. Stop & cleanup
    wwwserver stop
    wwwbonjour off
    ```

13. **Commit + push** sul branch operativo (`claude/work-in-progress`)
    seguendo le convenzioni git di ivanluminaria.com (Conventional Commits
    in italiano + co-authored con Claude se la convenzione del repo lo
    richiede). Aggiorna il `CLAUDE.md` di ivanluminaria.com con la sezione
    "Accesso LAN via Bonjour" + comando rapido + caveat.

## Note / caveat per ivanluminaria.com

- **Hugo NON ha auth** → esposizione LAN espone **tutto** il sito (anche
  bozze `--buildDrafts` e post futuri `--buildFuture` se attivi). Per la LAN
  domestica privata di Ivan è accettabile (single-user, rete trust). Se mai
  servisse uno scenario "ospiti", spegnere il LaunchAgent server (`wwwserver
  disable`) e usare solo il `dev` foreground locale.

- **`--baseURL` è CRUCIALE**: senza, i link interni del sito generato da
  Hugo puntano sempre a `localhost`, e dal cellulare il browser fallisce.
  Verifica il comportamento empiricamente al primo run.

- **Tema Congo è submodule git**: assicurati che dopo un fresh clone il
  submodule sia inizializzato (`git submodule update --init --recursive`)
  altrimenti `hugo server` fallisce con "theme not found".

- **IP mai hardcodato**: lo script `announce.sh` (condiviso) lo ricava da
  `ipconfig getifaddr` e si auto-aggiorna su cambio DHCP. Non scrivere
  l'IP nei plist.

- **`hugo server` ha startup veloce** (~1-2 secondi su questo sito ~70
  articoli × 4 lingue). Non serve poll attivo per il bind, basta `sleep 2`
  dopo lo start prima del curl di verifica.

- **Background manuale e LaunchAgent server condividono la porta** → usa
  l'uno **o** l'altro (il manager fa il guard di porta in `start`).

- **Live-reload Hugo via WebSocket**: dal cellulare la live-reload del
  browser si connette via WS a `ws://ivanluminaria.local:1313/livereload`.
  Funziona se il manager passa `--liveReloadPort=1313` (porta esplicita,
  altrimenti Hugo picca una random). Includi questo flag nei comandi
  `start` e `fg` del manager.

- **Cron Hugo build esistenti**: il GitHub Actions deploy non è impattato
  da questa configurazione locale — il manager controlla solo
  `hugo server` (dev preview), non il build di produzione.

## Output atteso

Quando il prompt finisce:
- `wwwserver start` funziona, espone il sito LAN su `:1313`
- Da Safari iPhone su WiFi locale: `http://ivanluminaria.local:1313/` mostra
  il sito + link interni navigabili
- 2 nuovi script in `scripts/shell/` + 2 plist in `deploy/launchd/` + doc
  in `docs/BONJOUR_LAN_ACCESS.md`
- `CLAUDE.md` aggiornato con sezione "Accesso LAN via Bonjour"
- Commit + push su `claude/work-in-progress`
