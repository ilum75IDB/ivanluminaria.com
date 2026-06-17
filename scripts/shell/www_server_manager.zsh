#!/bin/zsh
# ===================================================================
# IVANLUMINARIA.COM - SERVER MANAGER PARAMETRICO (hugo server)
# File: www_server_manager.zsh
# Gestione di `hugo server`: background LAN, foreground locale (dev/preview),
# log, LaunchAgent persistente. Invocato dal wrapper wwwserver() in www_env.zsh.
# Pattern: stile www_go_manager.zsh (sub-comando come 1° argomento).
# Doc: docs/BONJOUR_LAN_ACCESS.md
# ===================================================================

# --- Colori ---
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
CYAN='\033[0;36m'; WHITE='\033[1;37m'; NC='\033[0m'

# --- Default (se invocato senza env caricato) ---
: ${WWW_PROJECT_DIR:="${HOME}/Development/APPLICAZIONI/My-Web-Site/ivanluminaria.com"}
: ${WWW_SHELL_DIR:="$WWW_PROJECT_DIR/scripts/shell"}
: ${WWW_PORT:="1313"}
: ${WWW_HOST:="127.0.0.1"}
: ${WWW_BIND:="0.0.0.0"}
: ${WWW_BONJOUR_HOSTNAME:="ivanluminaria.local"}
: ${WWW_BONJOUR_HOSTNAME_ALIAS:="ilum.local"}
: ${WWW_LOG_DIR:="${HOME}/Library/Logs/ivanluminaria.com"}
: ${WWW_SERVER_LOG:="$WWW_LOG_DIR/server.log"}
: ${WWW_SERVER_PID:="$WWW_LOG_DIR/server.pid"}
: ${WWW_SERVER_LABEL:="com.ivanluminaria.www"}
PLIST_REF="$WWW_PROJECT_DIR/deploy/launchd/$WWW_SERVER_LABEL.plist"
PLIST_ACTIVE="$HOME/Library/LaunchAgents/$WWW_SERVER_LABEL.plist"

# baseURL usato sui comandi LAN (start/fg/enable). I link interni del sito
# generato da Hugo devono puntare al nome .local: senza --baseURL il browser
# del telefono cliccando su un link interno verrebbe rimandato a localhost.
# --appendPort=false evita la duplicazione :1313:1313/ negli href generati.
WWW_LAN_BASEURL="http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/"

_www_urls() {
    echo -e "   • locale : ${CYAN}http://$WWW_HOST:$WWW_PORT/${NC}"
    echo -e "   • LAN    : ${CYAN}http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/${NC}  (alias http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/)"
}

_www_check_hugo() {
    if ! command -v hugo >/dev/null 2>&1; then
        echo -e "${RED}⚠️  hugo non trovato nel PATH.${NC}"
        echo "    Installa con: brew install hugo"
        return 1
    fi
    return 0
}

# PID del processo manuale, se vivo (altrimenti vuoto + pulizia pidfile stale)
_www_running_pid() {
    [[ -f "$WWW_SERVER_PID" ]] || return 1
    local pid=$(cat "$WWW_SERVER_PID" 2>/dev/null)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        echo "$pid"; return 0
    fi
    rm -f "$WWW_SERVER_PID"
    return 1
}

# Chi ascolta sulla porta (qualsiasi processo: manuale o LaunchAgent)
_www_port_pid() {
    lsof -nP -iTCP:"$WWW_PORT" -sTCP:LISTEN -t 2>/dev/null | head -1
}

_www_service_loaded() {
    launchctl list 2>/dev/null | grep -q "$WWW_SERVER_LABEL"
}

cmd_start() {
    _www_check_hugo || return 1
    local pid=$(_www_running_pid)
    if [[ -n "$pid" ]]; then
        echo -e "${YELLOW}⚠️  Server già in esecuzione (background, pid $pid).${NC} Usa 'wwwserver restart' o 'wwwserver stop'."
        return 1
    fi
    if [[ -n "$(_www_port_pid)" ]]; then
        echo -e "${YELLOW}⚠️  La porta $WWW_PORT è già occupata (pid $(_www_port_pid)).${NC}"
        echo "    Forse è attivo il LaunchAgent (wwwserver svc) o un altro processo. Niente avvio."
        return 1
    fi
    mkdir -p "$WWW_LOG_DIR"
    cd "$WWW_PROJECT_DIR" || return 1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === wwwserver start (bind $WWW_BIND:$WWW_PORT, baseURL $WWW_LAN_BASEURL) ===" >> "$WWW_SERVER_LOG"
    nohup hugo server \
        --bind "$WWW_BIND" \
        --port "$WWW_PORT" \
        --baseURL "$WWW_LAN_BASEURL" \
        --appendPort=false \
        --buildDrafts \
        --buildFuture \
        --liveReloadPort="$WWW_PORT" \
        >> "$WWW_SERVER_LOG" 2>&1 &
    local newpid=$!
    echo "$newpid" > "$WWW_SERVER_PID"
    disown 2>/dev/null
    sleep 2
    if kill -0 "$newpid" 2>/dev/null; then
        echo -e "${GREEN}🚀 Server avviato in background${NC} (pid $newpid)"
        _www_urls
        echo -e "   • log    : ${WHITE}wwwserver log${NC} / ${WHITE}wwwserver logf${NC}  ($WWW_SERVER_LOG)"
        echo -e "   • flags  : --buildDrafts --buildFuture --baseURL=$WWW_LAN_BASEURL --appendPort=false"
    else
        echo -e "${RED}❌ Avvio fallito.${NC} Ultime righe di log:"
        tail -n 20 "$WWW_SERVER_LOG"
        rm -f "$WWW_SERVER_PID"
        return 1
    fi
}

cmd_stop() {
    local pid=$(_www_running_pid)
    if [[ -z "$pid" ]]; then
        local lpid=$(_www_port_pid)
        if [[ -n "$lpid" ]] && ! _www_service_loaded; then
            echo -e "${YELLOW}Nessun pidfile, ma la porta $WWW_PORT è occupata (pid $lpid). La fermo.${NC}"
            kill "$lpid" 2>/dev/null
            return 0
        fi
        echo -e "${YELLOW}Nessun server in background da fermare.${NC}"
        _www_service_loaded && echo "    (Il LaunchAgent risulta caricato: usa 'wwwserver disable'.)"
        return 0
    fi
    kill "$pid" 2>/dev/null
    local i=0
    while kill -0 "$pid" 2>/dev/null && (( i < 10 )); do sleep 0.3; (( i++ )); done
    if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid" 2>/dev/null
    fi
    rm -f "$WWW_SERVER_PID"
    echo -e "${GREEN}🛑 Server fermato${NC} (pid $pid)"
}

cmd_restart() {
    cmd_stop
    sleep 1
    cmd_start
}

cmd_status() {
    echo -e "${YELLOW}📊 Stato server ivanluminaria.com (hugo server)${NC}"
    local pid=$(_www_running_pid)
    if [[ -n "$pid" ]]; then
        echo -e "   background : ${GREEN}● attivo${NC} (pid $pid)"
    else
        echo -e "   background : ${RED}○ spento${NC}"
    fi
    local lpid=$(_www_port_pid)
    if [[ -n "$lpid" ]]; then
        echo -e "   porta $WWW_PORT : ${GREEN}● in ascolto${NC} (pid $lpid)"
    else
        echo -e "   porta $WWW_PORT : ${RED}○ libera${NC}"
    fi
    if _www_service_loaded; then
        echo -e "   LaunchAgent: ${GREEN}● caricato${NC} ($WWW_SERVER_LABEL)"
    else
        echo -e "   LaunchAgent: ${RED}○ non caricato${NC}"
    fi
    echo -e "   bind       : $WWW_BIND:$WWW_PORT  (baseURL LAN: $WWW_LAN_BASEURL)"
    [[ -n "$lpid" ]] && _www_urls
    echo -e "   log        : $WWW_SERVER_LOG"
}

# Foreground locale (= hserve): drafts visibili, scheduled NASCOSTI, bind 127.0.0.1
cmd_dev() {
    _www_check_hugo || return 1
    cd "$WWW_PROJECT_DIR" || return 1
    echo -e "${GREEN}🚀 hugo server foreground (dev = hserve)${NC} su $WWW_HOST:$WWW_PORT (Ctrl-C per fermare)"
    echo -e "   draft: ${WHITE}visibili${NC} · scheduled: ${WHITE}nascosti${NC} (anteprima GitHub Pages)"
    exec hugo server -D --navigateToChanged
}

# Foreground locale (= hservepreview): drafts + scheduled visibili, bind 127.0.0.1
cmd_preview() {
    _www_check_hugo || return 1
    cd "$WWW_PROJECT_DIR" || return 1
    echo -e "${GREEN}🚀 hugo server foreground (preview = hservepreview)${NC} su $WWW_HOST:$WWW_PORT (Ctrl-C per fermare)"
    echo -e "   draft: ${WHITE}visibili${NC} · scheduled: ${WHITE}visibili${NC} (revisione pre-pubblicazione)"
    exec hugo server -D -F --navigateToChanged
}

# Foreground LAN: stesso comando di `start` ma in foreground (debug live-reload visibile)
cmd_fg() {
    _www_check_hugo || return 1
    cd "$WWW_PROJECT_DIR" || return 1
    echo -e "${GREEN}🚀 hugo server foreground LAN${NC} su $WWW_BIND:$WWW_PORT (Ctrl-C per fermare)"
    _www_urls
    echo -e "   flags: --buildDrafts --buildFuture --baseURL=$WWW_LAN_BASEURL --appendPort=false"
    exec hugo server \
        --bind "$WWW_BIND" \
        --port "$WWW_PORT" \
        --baseURL "$WWW_LAN_BASEURL" \
        --appendPort=false \
        --buildDrafts \
        --buildFuture \
        --liveReloadPort="$WWW_PORT"
}

cmd_log() {
    if [[ ! -f "$WWW_SERVER_LOG" ]]; then
        echo -e "${YELLOW}Nessun log ancora: $WWW_SERVER_LOG${NC}"
        return 0
    fi
    local arg="${1:-50}"
    if [[ "$arg" == "-f" || "$arg" == "f" ]]; then
        cmd_logf; return
    fi
    local n="${arg#-}"
    [[ "$n" =~ ^[0-9]+$ ]] || n=50
    echo -e "${CYAN}── ultime $n righe di $WWW_SERVER_LOG ──${NC}"
    tail -n "$n" "$WWW_SERVER_LOG"
}

cmd_logf() {
    mkdir -p "$WWW_LOG_DIR"; touch "$WWW_SERVER_LOG"
    echo -e "${CYAN}── tail -f $WWW_SERVER_LOG (Ctrl-C per uscire) ──${NC}"
    tail -f "$WWW_SERVER_LOG"
}

cmd_enable() {
    if [[ ! -f "$PLIST_REF" ]]; then
        echo -e "${RED}❌ plist di riferimento mancante: $PLIST_REF${NC}"
        return 1
    fi
    local pid=$(_www_running_pid)
    if [[ -n "$pid" ]]; then
        echo -e "${YELLOW}⚠️  C'è un server background attivo (pid $pid). Lo fermo prima di abilitare il servizio.${NC}"
        cmd_stop
    fi
    mkdir -p "$HOME/Library/LaunchAgents" "$WWW_LOG_DIR"
    cp "$PLIST_REF" "$PLIST_ACTIVE"
    launchctl unload "$PLIST_ACTIVE" 2>/dev/null
    if launchctl load -w "$PLIST_ACTIVE"; then
        echo -e "${GREEN}✅ Servizio abilitato${NC}: hugo server parte al login e si riavvia da solo (KeepAlive)."
        _www_urls
        echo -e "   • log    : wwwserver log / logf"
    else
        echo -e "${RED}❌ launchctl load fallito.${NC}"
        return 1
    fi
}

cmd_disable() {
    if [[ -f "$PLIST_ACTIVE" ]]; then
        launchctl unload -w "$PLIST_ACTIVE" 2>/dev/null
        echo -e "${GREEN}🛑 Servizio disabilitato${NC} (LaunchAgent scaricato). Il plist resta in ~/Library/LaunchAgents/."
    else
        echo -e "${YELLOW}Nessun LaunchAgent installato in $PLIST_ACTIVE${NC}"
    fi
}

cmd_svc() {
    echo -e "${YELLOW}🔧 LaunchAgent $WWW_SERVER_LABEL${NC}"
    if _www_service_loaded; then
        launchctl list | grep "$WWW_SERVER_LABEL" | sed 's/^/   /'
        echo -e "   stato: ${GREEN}caricato${NC}"
    else
        echo -e "   stato: ${RED}non caricato${NC} (usa 'wwwserver enable')"
    fi
    [[ -f "$PLIST_ACTIVE" ]] && echo "   plist attivo: $PLIST_ACTIVE" || echo "   plist attivo: assente"
}

cmd_help() {
    echo "================================================================"
    echo "🎛  IVANLUMINARIA.COM - SERVER MANAGER (hugo server)"
    echo "================================================================"
    echo ""
    echo -e "${YELLOW}Uso:${NC} wwwserver <comando>"
    echo ""
    echo -e "${CYAN}LAN (background, raggiungibile da telefono/iPad/PC):${NC}"
    echo -e "  ${WHITE}start${NC}      Avvia in background (bind $WWW_BIND:$WWW_PORT, baseURL $WWW_LAN_BASEURL)"
    echo -e "             flags: --buildDrafts --buildFuture --appendPort=false --liveReloadPort=$WWW_PORT"
    echo -e "  ${WHITE}stop${NC}       Ferma il server background"
    echo -e "  ${WHITE}restart${NC}    Stop + start"
    echo -e "  ${WHITE}status${NC}     Stato (background / porta / LaunchAgent / URL)"
    echo -e "  ${WHITE}fg${NC}         Foreground LAN (stesso bind di start, blocca il terminale)"
    echo ""
    echo -e "${CYAN}Locale (foreground, 127.0.0.1 — workflow editoriale):${NC}"
    echo -e "  ${WHITE}dev${NC}        hugo server -D --navigateToChanged   (= ${WHITE}hserve${NC})"
    echo -e "             draft visibili, scheduled nascosti (anteprima GitHub Pages)"
    echo -e "  ${WHITE}preview${NC}    hugo server -D -F --navigateToChanged   (= ${WHITE}hservepreview${NC})"
    echo -e "             draft + scheduled visibili (revisione pre-pubblicazione)"
    echo ""
    echo -e "${CYAN}Log:${NC}"
    echo -e "  ${WHITE}log [N]${NC}    Ultime N righe (default 50). Es: wwwserver log 100"
    echo -e "  ${WHITE}logf${NC}       tail -f (segui il log live)  ·  anche: wwwserver log -f"
    echo ""
    echo -e "${CYAN}Servizio persistente (LaunchAgent, parte al login):${NC}"
    echo -e "  ${WHITE}enable${NC}     Installa + carica il LaunchAgent (sempre attivo)"
    echo -e "  ${WHITE}disable${NC}    Scarica il LaunchAgent"
    echo -e "  ${WHITE}svc${NC}        Stato del LaunchAgent"
    echo ""
    echo -e "${CYAN}Browser:${NC} wwwopen (locale) · wwwopenlan (LAN) · wwwopenshort (alias ilum.local)"
    echo -e "${CYAN}Accesso LAN:${NC} wwwbonjour (vedi wwwhelp -B)"
    echo "================================================================"
}

# --- Dispatch ---
case "${1:-status}" in
    start)               cmd_start ;;
    stop)                cmd_stop ;;
    restart)             cmd_restart ;;
    status|"")           cmd_status ;;
    dev)                 cmd_dev ;;
    preview)             cmd_preview ;;
    fg|foreground)       cmd_fg ;;
    log)                 cmd_log "$2" ;;
    logf|tailf)          cmd_logf ;;
    enable)              cmd_enable ;;
    disable)             cmd_disable ;;
    svc|service)         cmd_svc ;;
    help|-h|--help)      cmd_help ;;
    *)
        echo -e "${RED}Comando non riconosciuto: $1${NC}"
        echo ""
        cmd_help
        return 1 2>/dev/null || exit 1
        ;;
esac
