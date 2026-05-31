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
    echo -e "  ${WHITE}2${NC}  wwwhelp -N    Navigazione directory"
    echo -e "  ${WHITE}3${NC}  wwwhelp -C    Contenuti multilingua (4 lingue)"
    echo -e "  ${WHITE}4${NC}  wwwhelp -G    Git & Deploy"
    echo -e "  ${WHITE}5${NC}  wwwhelp -L    Links esterni"
    echo -e "  ${WHITE}6${NC}  wwwhelp -V    Variabili ambiente"
    echo -e "  ${WHITE}7${NC}  wwwhelp -H    Help e Setup"
    echo ""
    echo -e "${CYAN}Esempio:${NC} wwwhelp -U  ${CYAN}(mostra help Hugo)${NC}"
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
