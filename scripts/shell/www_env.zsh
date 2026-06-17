#!/bin/zsh
# ===================================================================
# IVANLUMINARIA.COM - ENVIRONMENT CONFIGURATION FOR ZSH
# File: www_env.zsh
# Versione: 1.0 (Allineamento allo standard RCCS2025: env separato + help parametrico)
# Data Creazione: Domenica 31 Maggio 2026
# Autore: Ivan Luminaria
# Progetto: ivanluminaria.com (sito personale Hugo multilingua)
# Repository: ilum75IDB/ivanluminaria.com
# ===================================================================

# ===================================================================
# DIRECTORY BASE E PROGETTO
# ===================================================================
export WWW_PROJECT_DIR="${HOME}/Development/APPLICAZIONI/My-Web-Site/ivanluminaria.com"
export WWW_CONTENT_DIR="$WWW_PROJECT_DIR/content"
export WWW_CONFIG_DIR="$WWW_PROJECT_DIR/config/_default"
export WWW_DOCS_DIR="$WWW_PROJECT_DIR/docs"
export WWW_SHELL_DIR="$WWW_PROJECT_DIR/scripts/shell"

# ===================================================================
# URL E REPOSITORY
# ===================================================================
export HUGO_BASE_URL="https://ivanluminaria.com/"
export WWW_PROD_URL="https://ivanluminaria.com/"
export WWW_REPO="ilum75IDB/ivanluminaria.com"

# ===================================================================
# SERVER HUGO LOCALE + ACCESSO LAN (BONJOUR mDNS)
# ===================================================================
# Porta e bind del server `hugo server` locale.
#   WWW_HOST: host usato per costruire URL/alias locali (browser sul Mac).
#   WWW_BIND: interfaccia su cui hugo ascolta. 0.0.0.0 = raggiungibile da
#             altri device sulla stessa LAN (telefono/tablet). Vedi:
#             docs/BONJOUR_LAN_ACCESS.md
export WWW_PORT="1313"
export WWW_HOST="127.0.0.1"
export WWW_BIND="0.0.0.0"

# Nomi annunciati via mDNS sulla LAN (vedi LaunchAgent + announce.sh).
#   Primario : http://ivanluminaria.local:1313/
#   Alias    : http://ilum.local:1313/  (3 char, come il prefisso shell `www`)
export WWW_BONJOUR_HOSTNAME="ivanluminaria.local"
export WWW_BONJOUR_HOSTNAME_ALIAS="ilum.local"
export WWW_BONJOUR_LABEL="com.ivanluminaria.bonjour.www"
export WWW_BONJOUR_LOG="${HOME}/Library/Logs/bonjour-lan/ivanluminaria.com.log"

# Server background + log + LaunchAgent (gestiti da wwwserver <cmd>)
export WWW_LOG_DIR="${HOME}/Library/Logs/ivanluminaria.com"
export WWW_SERVER_LOG="$WWW_LOG_DIR/server.log"
export WWW_SERVER_PID="$WWW_LOG_DIR/server.pid"
export WWW_SERVER_LABEL="com.ivanluminaria.www"

# ===================================================================
# ALIAS - HUGO (build, server, clean)
# ===================================================================
# hserve: simula esattamente cosa sara' online su GitHub Pages
#   (draft visibili, post con data futura NASCOSTI)
alias hserve='hugo server -D --navigateToChanged'

# hservepreview: include anche post scheduled (data futura), per revisione pre-pubblicazione
alias hservepreview='hugo server -D -F --navigateToChanged'

# hbuild: build di produzione minificata (come fa il workflow GitHub Actions)
alias hbuild='hugo --minify'

# hclean: pulisce public/ + cache (utile dopo cambi al tema o ai layout)
alias hclean='rm -rf "$WWW_PROJECT_DIR/public" "$WWW_PROJECT_DIR/resources/_gen" "$WWW_PROJECT_DIR/.hugo_build.lock"'

# hnew: wrapper per "hugo new" (crea contenuto da archetype)
alias hnew='hugo new'

# themeupdate: aggiorna il submodule del tema Congo
alias themeupdate='cd "$WWW_PROJECT_DIR" && git submodule update --init --recursive'

# ===================================================================
# SERVER MANAGER PARAMETRICO (stile wwwgo) — hugo server + LAN
# ===================================================================
# wwwserver <cmd> — gestione completa di `hugo server`:
#   start | stop | restart | status | dev | preview | fg | log [N] | logf |
#   enable | disable | svc | help
# Senza argomenti mostra status. Logica in www_server_manager.zsh.
#   • start/fg/enable usano bind $WWW_BIND (LAN, --baseURL ivanluminaria.local)
#   • dev/preview restano locali (127.0.0.1) per il workflow editoriale di Ivan
wwwserver() {
    "$WWW_SHELL_DIR/www_server_manager.zsh" "$@"
}

# ===================================================================
# BONJOUR MANAGER PARAMETRICO (stile wwwgo) — accesso LAN da altri device
# ===================================================================
# wwwbonjour <cmd> — gestione dell'annuncio mDNS sulla LAN:
#   on | off | status | test | log [N] | logf | open | help
# Senza argomenti mostra status. Logica in www_bonjour_manager.zsh.
# Setup + replica multi-progetto: vedi docs/BONJOUR_LAN_ACCESS.md
wwwbonjour() {
    "$WWW_SHELL_DIR/www_bonjour_manager.zsh" "$@"
}

# Browser quick-open
alias wwwopen='open http://$WWW_HOST:$WWW_PORT/'
alias wwwopenlan='open http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/'
alias wwwopenshort='open http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/'
# IP LAN corrente del Mac (utile per debug Bonjour)
alias wwwip='ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null'

# ===================================================================
# FUNZIONI GO MANAGER (UNIFIED v1.0 — pattern RCCS2025 rccgo)
# ===================================================================
# Funzione wrapper per go manager
# - Senza argomenti       → mostra lista directory (delega allo script)
# - 'help'/-h/--help      → mostra help completo (delega allo script)
# - <target>              → cambia directory in shell corrente (case locale)
wwwgo() {
    local target="${1:-}"

    if [[ -z "$target" ]]; then
        # Mostra lista
        "$WWW_SHELL_DIR/www_go_manager.zsh"
        return 0
    fi

    if [[ "$target" == "help" ]] || [[ "$target" == "-h" ]] || [[ "$target" == "--help" ]]; then
        # Mostra help
        "$WWW_SHELL_DIR/www_go_manager.zsh" help
        return 0
    fi

    # Determina la directory target
    local target_dir=""

    case "$target" in
        project|root)
            target_dir="$WWW_PROJECT_DIR"
            ;;
        content)
            target_dir="$WWW_CONTENT_DIR"
            ;;
        posts|blog)
            target_dir="$WWW_CONTENT_DIR/posts"
            ;;
        resumes)
            target_dir="$WWW_CONTENT_DIR/resumes"
            ;;
        config)
            target_dir="$WWW_CONFIG_DIR"
            ;;
        docs)
            target_dir="$WWW_DOCS_DIR"
            ;;
        css)
            target_dir="$WWW_PROJECT_DIR/assets/css"
            ;;
        layouts)
            target_dir="$WWW_PROJECT_DIR/layouts"
            ;;
        shell)
            target_dir="$WWW_SHELL_DIR"
            ;;
        scripts)
            target_dir="$WWW_PROJECT_DIR/scripts"
            ;;
        *)
            echo "❌ Directory non riconosciuta: $target"
            echo ""
            echo "Directory disponibili:"
            echo "  project, content, posts, resumes, config, docs, css, layouts, shell, scripts"
            echo ""
            echo "Usa 'wwwgo help' per maggiori informazioni"
            return 1
            ;;
    esac

    # Verifica esistenza directory
    if [[ ! -d "$target_dir" ]]; then
        echo "❌ Directory non trovata: $target_dir"
        return 1
    fi

    # Cambia directory
    cd "$target_dir"

    # Feedback visivo
    echo "✅ 📁 $(pwd)"
}

# ===================================================================
# ALIAS - GIT (shortcut comuni)
# ===================================================================
alias gstatus='git status'
alias gdiff='git diff'
alias glog='git log --oneline -20'
alias gpush='git push origin main'
alias gpull='git pull origin main'

# ===================================================================
# ALIAS - DEPLOY & PREVIEW
# ===================================================================
# deploy: shortcut "add + commit + push" - USARE CON CAUTELA (no validazione)
alias deploy='git add -A && git commit -m "update site" && git push origin main'

# preview: apre il sito di produzione nel browser
alias preview='open "$WWW_PROD_URL"'

# ghactions: apre il pannello GitHub Actions del repo
alias ghactions='open "https://github.com/$WWW_REPO/actions"'

# ===================================================================
# FUNZIONI - CONTENUTI MULTILINGUA
# ===================================================================
# www_new_page: crea un set di 4 file (it/en/es/ro) per una nuova pagina
www_new_page() {
    local name="$1"
    local dir="${2:-content}"
    if [[ -z "$name" ]]; then
        echo "❌ Uso: www_new_page <nome> [directory]"
        echo "   Esempio: www_new_page about content"
        return 1
    fi
    for lang in it en es ro; do
        local filepath="$WWW_PROJECT_DIR/$dir/${name}.${lang}.md"
        if [[ ! -f "$filepath" ]]; then
            {
                echo "---"
                echo "title: \"\""
                echo "date: $(date +%Y-%m-%dT%H:%M:%S%z)"
                echo "draft: true"
                echo "---"
            } > "$filepath"
            echo "✅ Creato: $filepath"
        else
            echo "⚠️  Esiste già: $filepath"
        fi
    done
}

# www_new_post: scorciatoia per creare un nuovo post (4 lingue) in content/posts/
www_new_post() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "❌ Uso: www_new_post <slug-del-post>"
        echo "   Esempio: www_new_post oracle-vs-postgres"
        return 1
    fi
    www_new_page "$name" "content/posts"
}

# ===================================================================
# HELP FUNCTION CON SISTEMA PARAMETRICO
# ===================================================================
wwwhelp() {
    # Delega SEMPRE a www_help.zsh per help parametrico
    "$WWW_SHELL_DIR/www_help.zsh" "$@"
}

# ===================================================================
# MESSAGGI DI BENVENUTO
# ===================================================================
echo "🌐 ivanluminaria.com - Environment Loaded"
echo "   Versione: 1.0 (env separato + help parametrico, standard RCCS2025)"
echo "   Repository: $WWW_REPO"
echo "   URL prod:   $WWW_PROD_URL"
echo ""
echo "   💡 Comandi rapidi:"
echo "      wwwhelp        - Help completo (menu sezioni: -U -S -B -N -C -G -L -V -H)"
echo "      wwwgo          - Navigazione directory (lista target)"
echo "      wwwgo posts    - Vai a content/posts/"
echo "      hserve         - Server locale (anteprima GitHub Pages)"
echo "      hservepreview  - Server locale con post futuri visibili"
echo "      wwwserver      - Manager server (start/stop/restart/status/dev/preview/log/enable...)"
echo "      wwwbonjour     - Manager accesso LAN (on/off/status/test/log/open)"
echo ""
