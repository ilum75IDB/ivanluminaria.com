#!/usr/bin/env zsh

###############################################################################
# IVANLUMINARIA.COM - GO MANAGER
# Gestione unificata navigazione directory progetto
# Versione: 1.0 (Allineamento allo standard RCCS2025 rcc_go_manager.zsh)
# Data Creazione: Domenica 31 Maggio 2026
# Autore: Ivan Luminaria
# Progetto: ivanluminaria.com (sito personale Hugo multilingua)
# Repository: ilum75IDB/ivanluminaria.com
###############################################################################

# Exit on error
set -e

# Verifica che l'environment WWW sia caricato
if [[ -z "$WWW_SHELL_DIR" ]]; then
    echo "❌ ERROR: Environment WWW non caricato!"
    echo "   Assicurati di aver caricato www_env.zsh nella tua shell"
    exit 1
fi

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

###############################################################################
# FUNZIONI UTILITÀ
###############################################################################

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

###############################################################################
# COMANDO: HELP
###############################################################################

show_help() {
    cat << EOF
================================================================
🧭 IVANLUMINARIA.COM - GO MANAGER
================================================================

Gestione unificata navigazione directory progetto

COMANDI DISPONIBILI:

  project             Va a project root directory
  content             Va a content/ (radice contenuti)
  posts               Va a content/posts/ (articoli del blog)
  resumes             Va a content/resumes/ (CV multilingua)
  config              Va a config/_default/ (languages, menus, params)
  docs                Va a docs/ (guidelines, glossario, issues)
  css                 Va a assets/css/ (custom.css)
  layouts             Va a layouts/ (override partials e template)
  shell               Va a scripts/shell/ (env, help, go manager)
  scripts             Va a scripts/ (script Python applicativi)

  help                Mostra questo messaggio

ALIAS:

  root                Alias per 'project'
  blog                Alias per 'posts'

ESEMPI:

  wwwgo project
  wwwgo posts
  wwwgo css
  wwwgo                # Mostra lista directory

DIRECTORY MAPPATE:

  project    → $WWW_PROJECT_DIR
  content    → $WWW_CONTENT_DIR
  posts      → $WWW_CONTENT_DIR/posts
  resumes    → $WWW_CONTENT_DIR/resumes
  config     → $WWW_CONFIG_DIR
  docs       → $WWW_DOCS_DIR
  css        → $WWW_PROJECT_DIR/assets/css
  layouts    → $WWW_PROJECT_DIR/layouts
  shell      → $WWW_SHELL_DIR
  scripts    → $WWW_PROJECT_DIR/scripts

NOTE:

  • Repository: ilum75IDB/ivanluminaria.com
  • Le path sono ricavate dalle variabili \$WWW_* (vedi 'wwwhelp -V')

================================================================
EOF
}

###############################################################################
# COMANDO: LIST (senza parametri)
###############################################################################

show_list() {
    cat << EOF
================================================================
🧭 WWW - DIRECTORY DISPONIBILI
================================================================

$(echo -e "${YELLOW}Directory Progetto:${NC}")
  project    → $WWW_PROJECT_DIR
  content    → $WWW_CONTENT_DIR
  posts      → $WWW_CONTENT_DIR/posts
  resumes    → $WWW_CONTENT_DIR/resumes

$(echo -e "${YELLOW}Directory Configurazione & Stile:${NC}")
  config     → $WWW_CONFIG_DIR
  css        → $WWW_PROJECT_DIR/assets/css
  layouts    → $WWW_PROJECT_DIR/layouts

$(echo -e "${YELLOW}Directory Docs & Scripts:${NC}")
  docs       → $WWW_DOCS_DIR
  shell      → $WWW_SHELL_DIR
  scripts    → $WWW_PROJECT_DIR/scripts

$(echo -e "${CYAN}Alias:${NC}")
  root = project, blog = posts

$(echo -e "${CYAN}Uso:${NC}")
  wwwgo <directory>
  wwwgo help

================================================================
EOF
}

###############################################################################
# MAIN EXECUTION
###############################################################################

main() {
    # Se nessun argomento, mostra lista
    if [[ $# -eq 0 ]]; then
        show_list
        return 0
    fi

    local command="$1"

    case "$command" in
        help|-h|--help)
            show_help
            ;;
        list|ls)
            show_list
            ;;
        *)
            # Per directory target, la funzione wrapper wwwgo() in www_env.zsh
            # gestisce il cd effettivo nella shell chiamante.
            # Qui produciamo solo un messaggio d'errore se invocati direttamente
            # con un target sconosciuto (uso atipico).
            log_error "Comando non riconosciuto in esecuzione standalone: $command"
            echo ""
            echo "Usa 'wwwgo' (senza script) per navigare. Vedi 'wwwgo help'."
            return 1
            ;;
    esac
}

# NOTA IMPORTANTE: Per cambiare directory nella shell chiamante,
# questo script viene chiamato solo per i comandi list/help.
# Il cambio di directory effettivo è gestito dalla funzione wrapper
# wwwgo() definita in www_env.zsh (case + cd diretto in shell corrente).

# Gestione interruzioni
trap 'echo -e "\n${RED}[INTERROTTO]${NC} Go manager interrotto"; exit 130' INT TERM

# Esegui main con tutti gli argomenti
main "$@"
