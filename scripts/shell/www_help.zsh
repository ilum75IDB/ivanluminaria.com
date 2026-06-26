#!/usr/bin/env zsh

###############################################################################
# IVANLUMINARIA.COM - HELP SYSTEM
# Sistema help parametrico per accesso rapido a tutti i comandi WWW
# Versione: 1.0 (Allineamento allo standard RCCS2025)
# Data Creazione: Domenica 31 Maggio 2026
# Autore: Ivan Luminaria
# Progetto: ivanluminaria.com (sito personale Hugo multilingua)
# Repository: ilum75IDB/ivanluminaria.com
###############################################################################

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Header e Footer comuni
show_header() {
    echo "================================================================"
    echo "🌐 IVANLUMINARIA.COM - HELP"
    echo "================================================================"
}

show_footer() {
    echo "================================================================"
}

# Menu principale
show_main_menu() {
    show_header
    echo ""
    echo -e "${YELLOW}SEZIONI HELP DISPONIBILI:${NC}"
    echo ""
    echo -e "  ${WHITE}1${NC}  wwwhelp -U    Hugo (server, build, clean, theme)"
    echo -e "  ${WHITE}2${NC}  wwwhelp -S    Server manager (wwwserver: start/stop/dev/preview/enable...)"
    echo -e "  ${WHITE}3${NC}  wwwhelp -B    Bonjour / accesso LAN (altri device sulla stessa WiFi)"
    echo -e "  ${WHITE}4${NC}  wwwhelp -N    Navigazione directory"
    echo -e "  ${WHITE}5${NC}  wwwhelp -C    Contenuti multilingua (4 lingue)"
    echo -e "  ${WHITE}6${NC}  wwwhelp -G    Git & Deploy"
    echo -e "  ${WHITE}7${NC}  wwwhelp -L    Links esterni"
    echo -e "  ${WHITE}8${NC}  wwwhelp -V    Variabili ambiente"
    echo -e "  ${WHITE}9${NC}  wwwhelp -H    Help e Setup"
    echo ""
    echo -e "${CYAN}Esempio:${NC} wwwhelp -S  ${CYAN}(mostra help Server LAN)${NC}"
    echo ""
    show_footer
}

# Sezione: HUGO
show_hugo() {
    show_header
    echo ""
    echo -e "${YELLOW}🚀 HUGO (server, build, clean, theme):${NC}"
    echo ""
    echo -e "  ${WHITE}hserve${NC}          # Server locale come apparirà su GitHub Pages"
    echo -e "                  #   (drafts visibili, post futuri NASCOSTI)"
    echo -e "  ${WHITE}hservepreview${NC}   # Server locale con anche i post programmati"
    echo -e "                  #   (date future) visibili - per revisione pre-pubblicazione"
    echo -e "  ${WHITE}hbuild${NC}          # Build produzione (--minify)"
    echo -e "  ${WHITE}hclean${NC}          # Pulisci public/ + resources/_gen/ + .hugo_build.lock"
    echo -e "  ${WHITE}hnew${NC}            # Wrapper per 'hugo new' (crea contenuto da archetype)"
    echo -e "  ${WHITE}themeupdate${NC}     # Aggiorna submodule tema Congo"
    echo ""
    echo -e "${CYAN}Esempi:${NC}"
    echo -e "  hserve                              # avvia server locale standard"
    echo -e "  hservepreview                       # include articoli con date future"
    echo -e "  hnew posts/oracle/<slug>/index.it.md  # nuovo post Oracle in italiano"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Hugo deve essere installato in versione ${WHITE}extended${NC} (per SCSS Congo)"
    echo -e "  • Il tema Congo è un Git submodule: dopo clone usa ${WHITE}themeupdate${NC}"
    echo -e "  • Deploy live: solo via ${WHITE}git push origin main${NC} (workflow GitHub Actions)"
    echo ""
    show_footer
}

# Sezione: SERVER MANAGER (wwwserver)
show_server() {
    show_header
    echo ""
    echo -e "${YELLOW}🚀 SERVER hugo server — manager parametrico ${WHITE}wwwserver <cmd>${NC}:"
    echo ""
    echo -e "${CYAN}LAN (background, raggiungibile da telefono/iPad/PC):${NC}"
    echo -e "  ${WHITE}wwwserver start${NC}    # Avvia in background (bind 0.0.0.0:$WWW_PORT)"
    echo -e "                     # flags: --buildDrafts --buildFuture --baseURL=http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/ --appendPort=false"
    echo -e "  ${WHITE}wwwserver stop${NC}     # Ferma il server background"
    echo -e "  ${WHITE}wwwserver restart${NC}  # Stop + start"
    echo -e "  ${WHITE}wwwserver status${NC}   # Stato (background / porta / LaunchAgent / URL)"
    echo -e "  ${WHITE}wwwserver fg${NC}       # Foreground LAN (stesso bind di start, blocca il terminale)"
    echo ""
    echo -e "${CYAN}Locale (foreground, 127.0.0.1 — workflow editoriale):${NC}"
    echo -e "  ${WHITE}wwwserver dev${NC}      # hugo server -D --navigateToChanged   (= ${WHITE}hserve${NC})"
    echo -e "                     # draft visibili, scheduled nascosti (anteprima GitHub Pages)"
    echo -e "  ${WHITE}wwwserver preview${NC}  # hugo server -D -F --navigateToChanged   (= ${WHITE}hservepreview${NC})"
    echo -e "                     # draft + scheduled visibili (revisione pre-pubblicazione)"
    echo ""
    echo -e "${CYAN}Log:${NC}"
    echo -e "  ${WHITE}wwwserver log [N]${NC}  # Ultime N righe (default 50). Es: wwwserver log 100"
    echo -e "  ${WHITE}wwwserver logf${NC}     # tail -f (segui live)  ·  anche: wwwserver log -f"
    echo ""
    echo -e "${CYAN}Servizio persistente (LaunchAgent, parte al login):${NC}"
    echo -e "  ${WHITE}wwwserver enable${NC}   # Installa + carica il LaunchAgent (sempre attivo)"
    echo -e "  ${WHITE}wwwserver disable${NC}  # Scarica il LaunchAgent"
    echo -e "  ${WHITE}wwwserver svc${NC}      # Stato del LaunchAgent"
    echo ""
    echo -e "${CYAN}Browser quick-open:${NC}"
    echo -e "  ${WHITE}wwwopen${NC}        # http://$WWW_HOST:$WWW_PORT/ (locale)"
    echo -e "  ${WHITE}wwwopenlan${NC}     # http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/ (nome lungo)"
    echo -e "  ${WHITE}wwwopenshort${NC}   # http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/ (alias breve)"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Bind 0.0.0.0 (\$WWW_BIND) → raggiungibile dalla LAN — vedi wwwhelp -B"
    echo -e "  • Background e LaunchAgent usano la stessa porta :$WWW_PORT → usa l'uno O l'altro"
    echo -e "  • Log: \$WWW_SERVER_LOG (~/Library/Logs/ivanluminaria.com/server.log)"
    echo -e "  • Hugo NON ha auth: \`start\` espone TUTTO il sito (drafts + scheduled inclusi)"
    echo ""
    show_footer
}

# Sezione: BONJOUR / ACCESSO LAN (wwwbonjour)
show_bonjour() {
    show_header
    echo ""
    echo -e "${YELLOW}📡 BONJOUR / ACCESSO LAN — manager parametrico ${WHITE}wwwbonjour <cmd>${NC}:"
    echo ""
    echo -e "  ${WHITE}wwwbonjour on${NC}      # Attiva l'annuncio mDNS (load LaunchAgent)"
    echo -e "  ${WHITE}wwwbonjour off${NC}     # Disattiva l'annuncio (unload LaunchAgent)"
    echo -e "  ${WHITE}wwwbonjour status${NC}  # Stato annuncio + nomi pubblicati"
    echo -e "  ${WHITE}wwwbonjour test${NC}    # Risolve i nomi via dns-sd (deve dare l'IP del Mac)"
    echo -e "  ${WHITE}wwwbonjour log [N]${NC} # Ultime N righe del log annuncio (default 50)"
    echo -e "  ${WHITE}wwwbonjour logf${NC}    # tail -f del log  ·  anche: wwwbonjour log -f"
    echo -e "  ${WHITE}wwwbonjour open${NC}    # Apri http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/"
    echo ""
    echo -e "${CYAN}Scorciatoie:${NC} ${WHITE}wwwopenlan${NC} (nome lungo) · ${WHITE}wwwopenshort${NC} (alias breve) · ${WHITE}wwwip${NC} (IP del Mac)"
    echo ""
    echo -e "${CYAN}Nomi annunciati sulla LAN:${NC}"
    echo -e "  • http://$WWW_BONJOUR_HOSTNAME:$WWW_PORT/   (primario)"
    echo -e "  • http://$WWW_BONJOUR_HOSTNAME_ALIAS:$WWW_PORT/                 (alias breve)"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Il nome .local risolve a un IP, la porta resta nell'URL (:$WWW_PORT)"
    echo -e "  • Auto-healing: se l'IP DHCP cambia, l'annuncio si aggiorna da solo"
    echo -e "  • Il server deve girare (wwwserver start / enable) per rispondere"
    echo -e "  • Particolarità Hugo: --baseURL crucial per link interni (gestito dal manager)"
    echo -e "  • Client: macOS/iOS/Android 12+ nativi; Windows richiede Bonjour Service"
    echo -e "  • Doc completa + replica multi-progetto: docs/BONJOUR_LAN_ACCESS.md"
    echo ""
    show_footer
}

# Sezione: NAVIGAZIONE (Unified Manager v1.0 — pattern RCCS2025 rccgo)
show_navigation() {
    show_header
    echo ""
    echo -e "${YELLOW}🧭 NAVIGAZIONE (Unified Manager v1.0):${NC}"
    echo ""
    echo -e "  ${WHITE}wwwgo project${NC}       # Va a project root directory"
    echo -e "  ${WHITE}wwwgo content${NC}       # Va a content/ (radice contenuti)"
    echo -e "  ${WHITE}wwwgo posts${NC}         # Va a content/posts/ (articoli del blog)"
    echo -e "  ${WHITE}wwwgo resumes${NC}       # Va a content/resumes/ (CV multilingua)"
    echo -e "  ${WHITE}wwwgo config${NC}        # Va a config/_default/ (languages, menus, params)"
    echo -e "  ${WHITE}wwwgo docs${NC}          # Va a docs/ (guidelines, glossario, issues)"
    echo -e "  ${WHITE}wwwgo css${NC}           # Va a assets/css/ (custom.css)"
    echo -e "  ${WHITE}wwwgo layouts${NC}       # Va a layouts/ (override partials e template)"
    echo -e "  ${WHITE}wwwgo shell${NC}         # Va a scripts/shell/ (env, help, go manager)"
    echo -e "  ${WHITE}wwwgo scripts${NC}       # Va a scripts/ (script Python applicativi)"
    echo ""
    echo -e "  ${WHITE}wwwgo${NC}               # Mostra lista directory disponibili"
    echo -e "  ${WHITE}wwwgo help${NC}          # Help completo navigation manager"
    echo ""
    echo -e "${CYAN}Alias:${NC}"
    echo -e "  wwwgo root = project, wwwgo blog = posts"
    echo ""
    echo -e "${CYAN}Esempi:${NC}"
    echo -e "  wwwgo project"
    echo -e "  wwwgo posts"
    echo -e "  wwwgo css"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Le path target sono ricavate dalle variabili \$WWW_* (vedi ${WHITE}wwwhelp -V${NC})"
    echo -e "  • Funzione wrapper in: ${WHITE}\$WWW_SHELL_DIR/www_env.zsh${NC}"
    echo -e "  • Script list/help in:  ${WHITE}\$WWW_SHELL_DIR/www_go_manager.zsh${NC}"
    echo ""
    show_footer
}

# Sezione: CONTENUTI MULTILINGUA
show_content() {
    show_header
    echo ""
    echo -e "${YELLOW}📝 CONTENUTI MULTILINGUA (4 lingue):${NC}"
    echo ""
    echo -e "  ${WHITE}www_new_page <nome> [dir]${NC}    # Crea pagina in 4 lingue (it/en/es/ro)"
    echo -e "  ${WHITE}www_new_post <slug>${NC}          # Crea post in 4 lingue (content/posts/)"
    echo ""
    echo -e "${CYAN}Esempi:${NC}"
    echo -e "  www_new_page about content"
    echo -e "  www_new_post oracle-vs-postgres"
    echo ""
    echo -e "${CYAN}Cosa fa:${NC}"
    echo -e "  • Crea 4 file: <nome>.{it,en,es,ro}.md con frontmatter base"
    echo -e "  • Frontmatter: title vuoto, date oggi, draft true"
    echo -e "  • Skip se il file esiste già (warning)"
    echo ""
    echo -e "${CYAN}Lingue gestite (ordine peso in Hugo):${NC}"
    echo -e "  ${WHITE}it${NC} (default, peso 1)   ${WHITE}en${NC} (peso 2)   ${WHITE}es${NC} (peso 3)   ${WHITE}ro${NC} (peso 4)"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Per workflow completo articoli vedi ${WHITE}CLAUDE.md → \"Writing articles\"${NC}"
    echo -e "  • Procedura a step + commit intermedi anti-timeout (step 0→7)"
    echo ""
    show_footer
}

# Sezione: GIT & DEPLOY
show_git() {
    show_header
    echo ""
    echo -e "${YELLOW}🔀 GIT & DEPLOY:${NC}"
    echo ""
    echo -e "${CYAN}Shortcut Git:${NC}"
    echo -e "  ${WHITE}gstatus${NC}         # git status"
    echo -e "  ${WHITE}gdiff${NC}           # git diff"
    echo -e "  ${WHITE}glog${NC}            # git log --oneline -20"
    echo -e "  ${WHITE}gpush${NC}           # git push origin main"
    echo -e "  ${WHITE}gpull${NC}           # git pull origin main"
    echo ""
    echo -e "${CYAN}Deploy (USARE CON CAUTELA):${NC}"
    echo -e "  ${WHITE}deploy${NC}          # add -A + commit \"update site\" + push origin main"
    echo ""
    echo -e "${RED}⚠️  Avvertenze:${NC}"
    echo -e "  • ${WHITE}deploy${NC} è uno shortcut senza validazione: NO review, NO message custom"
    echo -e "  • Per cambi importanti preferire workflow normale: git add + commit + push"
    echo -e "  • Push su main triggera il deploy GitHub Actions → live su ivanluminaria.com"
    echo -e "  • Branch di lavoro Claude: mai push diretto su main (regola CLAUDE.md globale)"
    echo ""
    show_footer
}

# Sezione: LINKS
show_links() {
    show_header
    echo ""
    echo -e "${YELLOW}🔗 LINKS ESTERNI:${NC}"
    echo ""
    echo -e "  ${WHITE}preview${NC}         # Apri il sito di produzione nel browser"
    echo -e "                  #   → \$WWW_PROD_URL"
    echo -e "  ${WHITE}ghactions${NC}       # Apri il pannello GitHub Actions del repo"
    echo -e "                  #   → https://github.com/\$WWW_REPO/actions"
    echo ""
    echo -e "${CYAN}URL utili (apri manualmente):${NC}"
    echo -e "  • Repo:     ${WHITE}https://github.com/$WWW_REPO${NC}"
    echo -e "  • Issues:   ${WHITE}https://github.com/$WWW_REPO/issues${NC}"
    echo -e "  • Pages:    ${WHITE}https://github.com/$WWW_REPO/settings/pages${NC}"
    echo ""
    show_footer
}

# Sezione: VARIABILI AMBIENTE
show_vars() {
    show_header
    echo ""
    echo -e "${YELLOW}📋 VARIABILI AMBIENTE:${NC}"
    echo ""
    echo -e "${CYAN}Path progetto:${NC}"
    echo -e "  ${WHITE}\$WWW_PROJECT_DIR${NC}  # $WWW_PROJECT_DIR"
    echo -e "  ${WHITE}\$WWW_CONTENT_DIR${NC}  # $WWW_CONTENT_DIR"
    echo -e "  ${WHITE}\$WWW_CONFIG_DIR${NC}   # $WWW_CONFIG_DIR"
    echo -e "  ${WHITE}\$WWW_DOCS_DIR${NC}     # $WWW_DOCS_DIR"
    echo -e "  ${WHITE}\$WWW_SHELL_DIR${NC}    # $WWW_SHELL_DIR"
    echo ""
    echo -e "${CYAN}URL & repo:${NC}"
    echo -e "  ${WHITE}\$HUGO_BASE_URL${NC}    # $HUGO_BASE_URL"
    echo -e "  ${WHITE}\$WWW_PROD_URL${NC}     # $WWW_PROD_URL"
    echo -e "  ${WHITE}\$WWW_REPO${NC}         # $WWW_REPO"
    echo ""
    echo -e "${CYAN}Note:${NC}"
    echo -e "  • Caricate da: ${WHITE}\$WWW_SHELL_DIR/www_env.zsh${NC}"
    echo -e "  • Sostituibili per ambienti alternativi modificando il file env"
    echo ""
    show_footer
}

# Sezione: HELP E SETUP
show_help_section() {
    show_header
    echo ""
    echo -e "${YELLOW}❓ HELP E SETUP:${NC}"
    echo ""
    echo -e "  ${WHITE}wwwhelp${NC}         # Mostra elenco sezioni"
    echo -e "  ${WHITE}wwwhelp -X${NC}      # Mostra sezione specifica (X = parametro)"
    echo ""
    echo -e "${CYAN}Sezioni disponibili:${NC}"
    echo -e "  -U  Hugo            |  -S  Server (wwwserver)  |  -B  Bonjour/LAN"
    echo -e "  -N  Navigazione     |  -C  Contenuti           |  -G  Git & Deploy"
    echo -e "  -L  Links           |  -V  Variabili           |  -H  Help & Setup (questa)"
    echo ""
    echo -e "${CYAN}Setup ambiente:${NC}"
    echo -e "  ${WHITE}workwww${NC}         # Carica ambiente WWW (alias da ~/.zshrc)"
    echo -e "  ${WHITE}prjmenu${NC}         # Ricarica ~/.zshrc (menu progetti)"
    echo ""
    echo -e "${CYAN}File di configurazione:${NC}"
    echo -e "  • Env progetto:  ${WHITE}\$WWW_SHELL_DIR/www_env.zsh${NC}"
    echo -e "  • Help progetto: ${WHITE}\$WWW_SHELL_DIR/www_help.zsh${NC}"
    echo -e "  • Menu globale:  ${WHITE}~/.zshrc${NC} (case 3|www → carica env)"
    echo ""
    echo -e "${CYAN}Documentazione progetto:${NC}"
    echo -e "  • ${WHITE}CLAUDE.md${NC}                          → istruzioni AI + workflow articoli"
    echo -e "  • ${WHITE}docs/AI_CONTENT_GUIDELINES.md${NC}      → linee guida contenuti (EN)"
    echo -e "  • ${WHITE}docs/AI_CONTENT_GUIDELINES_IT.md${NC}   → linee guida contenuti (IT)"
    echo -e "  • ${WHITE}docs/HUGO_PUBLICATIONS_TABLE.md${NC}    → calendario editoriale"
    echo -e "  • ${WHITE}docs/GLOSSARIO_TERMINI.md${NC}          → glossario cross-articoli"
    echo ""
    show_footer
}

# MAIN - Gestione parametri (CASE-INSENSITIVE)
main() {
    # Converte il parametro in minuscolo per gestione case-insensitive
    local param="${1}"
    local param_lower="${param:l}"  # ZSH parameter expansion per lowercase

    case "${param_lower}" in
        -u|--hugo)
            show_hugo
            ;;
        -s|--server)
            show_server
            ;;
        -b|--bonjour)
            show_bonjour
            ;;
        -n|--navigation)
            show_navigation
            ;;
        -c|--content)
            show_content
            ;;
        -g|--git)
            show_git
            ;;
        -l|--links)
            show_links
            ;;
        -v|--vars)
            show_vars
            ;;
        -h|--help)
            show_help_section
            ;;
        "")
            show_main_menu
            ;;
        *)
            echo -e "${RED}Errore: Parametro non riconosciuto: $1${NC}"
            echo ""
            show_main_menu
            ;;
    esac
}

# Esegui main
main "$@"
