#!/bin/zsh
# ===================================================================
# IVANLUMINARIA.COM - BONJOUR MANAGER PARAMETRICO
# File: www_bonjour_manager.zsh
# Gestione dell'annuncio mDNS (accesso LAN da altri device).
# Invocato dal wrapper wwwbonjour() in www_env.zsh.
# Pattern: stile www_go_manager.zsh (sub-comando come 1° argomento).
# Doc completa: docs/BONJOUR_LAN_ACCESS.md
# ===================================================================

# --- Colori ---
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
CYAN='\033[0;36m'; WHITE='\033[1;37m'; NC='\033[0m'

# --- Default (se invocato senza env caricato) ---
: ${WWW_PORT:="1313"}
: ${WWW_BONJOUR_HOSTNAME:="ivanluminaria.local"}
: ${WWW_BONJOUR_HOSTNAME_ALIAS:="ilum.local"}
: ${WWW_BONJOUR_LABEL:="com.ivanluminaria.bonjour.www"}
: ${WWW_BONJOUR_LOG:="${HOME}/Library/Logs/bonjour-lan/ivanluminaria.com.log"}
PLIST_ACTIVE="$HOME/Library/LaunchAgents/$WWW_BONJOUR_LABEL.plist"

_wwwb_loaded() {
    launchctl list 2>/dev/null | grep -q "bonjour.www"
}

_wwwb_resolve() {
    local name="$1"
    echo -e "${CYAN}→ $name${NC}"
    ( dns-sd -G v4 "$name" & local p=$!; sleep 3; kill $p 2>/dev/null ) 2>&1 \
        | grep -i "$name" | head -1 || echo "   (nessuna risposta)"
}

cmd_on() {
    if [[ ! -f "$PLIST_ACTIVE" ]]; then
        echo -e "${RED}❌ LaunchAgent non installato: $PLIST_ACTIVE${NC}"
        echo "    Vedi setup in docs/BONJOUR_LAN_ACCESS.md"
        return 1
    fi
    launchctl load -w "$PLIST_ACTIVE" 2>/dev/null
    echo -e "${GREEN}✅ Bonjour ON${NC}: http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/ (alias http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/)"
}

cmd_off() {
    launchctl unload -w "$PLIST_ACTIVE" 2>/dev/null
    echo -e "${GREEN}🔕 Bonjour OFF${NC}: $WWW_BONJOUR_HOSTNAME / $WWW_BONJOUR_HOSTNAME_ALIAS non più annunciati"
}

cmd_status() {
    echo -e "${YELLOW}📡 Stato Bonjour / accesso LAN${NC}"
    if _wwwb_loaded; then
        launchctl list | grep "bonjour.www" | sed 's/^/   /'
        echo -e "   stato: ${GREEN}● annuncio attivo${NC}"
        echo -e "   nomi : http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/  ·  http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/"
    else
        echo -e "   stato: ${RED}○ non caricato${NC} (usa 'wwwbonjour on')"
    fi
    [[ -f "$PLIST_ACTIVE" ]] && echo "   plist: $PLIST_ACTIVE" || echo "   plist: assente"
}

cmd_test() {
    echo -e "${YELLOW}🔎 Risoluzione mDNS (deve dare l'IP del Mac)${NC}"
    _wwwb_resolve "$WWW_BONJOUR_HOSTNAME"
    _wwwb_resolve "$WWW_BONJOUR_HOSTNAME_ALIAS"
    echo -e "${CYAN}IP LAN del Mac:${NC} $(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo '?')"
}

cmd_log() {
    if [[ ! -f "$WWW_BONJOUR_LOG" ]]; then
        echo -e "${YELLOW}Nessun log ancora: $WWW_BONJOUR_LOG${NC}"
        return 0
    fi
    local arg="${1:-50}"
    if [[ "$arg" == "-f" || "$arg" == "f" ]]; then cmd_logf; return; fi
    local n="${arg#-}"
    [[ "$n" =~ ^[0-9]+$ ]] || n=50
    echo -e "${CYAN}── ultime $n righe di $WWW_BONJOUR_LOG ──${NC}"
    tail -n "$n" "$WWW_BONJOUR_LOG"
}

cmd_logf() {
    [[ -f "$WWW_BONJOUR_LOG" ]] || { echo -e "${YELLOW}Nessun log: $WWW_BONJOUR_LOG${NC}"; return 0; }
    echo -e "${CYAN}── tail -f $WWW_BONJOUR_LOG (Ctrl-C per uscire) ──${NC}"
    tail -f "$WWW_BONJOUR_LOG"
}

cmd_open() {
    open "http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/"
}

cmd_help() {
    echo "================================================================"
    echo "📡  IVANLUMINARIA.COM - BONJOUR / ACCESSO LAN MANAGER"
    echo "================================================================"
    echo ""
    echo -e "${YELLOW}Uso:${NC} wwwbonjour <comando>"
    echo ""
    echo -e "  ${WHITE}on${NC}         Attiva l'annuncio mDNS (load LaunchAgent)"
    echo -e "  ${WHITE}off${NC}        Disattiva l'annuncio (unload LaunchAgent)"
    echo -e "  ${WHITE}status${NC}     Stato dell'annuncio + nomi pubblicati"
    echo -e "  ${WHITE}test${NC}       Risolve $WWW_BONJOUR_HOSTNAME e $WWW_BONJOUR_HOSTNAME_ALIAS via dns-sd"
    echo -e "  ${WHITE}log [N]${NC}    Ultime N righe del log annuncio (default 50)"
    echo -e "  ${WHITE}logf${NC}       tail -f del log  ·  anche: wwwbonjour log -f"
    echo -e "  ${WHITE}open${NC}       Apre http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/ nel browser"
    echo ""
    echo -e "${CYAN}Nomi LAN:${NC} http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/  ·  http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/"
    echo -e "${CYAN}Nota:${NC} il server dev'essere avviato (wwwserver start / enable) per rispondere."
    echo -e "${CYAN}Doc:${NC} docs/BONJOUR_LAN_ACCESS.md  ·  scheda help: wwwhelp -B"
    echo "================================================================"
}

# --- Dispatch ---
case "${1:-status}" in
    on|start)         cmd_on ;;
    off|stop)         cmd_off ;;
    status|"")        cmd_status ;;
    test)             cmd_test ;;
    log)              cmd_log "$2" ;;
    logf|tailf)       cmd_logf ;;
    open)             cmd_open ;;
    help|-h|--help)   cmd_help ;;
    *)
        echo -e "${RED}Comando non riconosciuto: $1${NC}"
        echo ""
        cmd_help
        return 1 2>/dev/null || exit 1
        ;;
esac
