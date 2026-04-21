#!/usr/bin/env bash
#
# serve-local.sh — avvia il server Hugo locale per ivanluminaria.com
#
# Fa partire Hugo in modalità sviluppo con:
#   -D / --buildDrafts       → render dei post draft
#   -F / --buildFuture       → render dei post con data futura (scheduled)
#   --bind 0.0.0.0           → server raggiungibile da altri device in rete locale
#   --navigateToChanged      → reload automatico del browser sul file modificato
#
# Uso:
#   ./scripts/serve-local.sh                  # default (porta 1313)
#   ./scripts/serve-local.sh --port 4000      # passa flag Hugo aggiuntivi
#
# Alias suggerito in ~/.zshrc (o ~/.bashrc):
#   alias hugoserve="$HOME/ivanluminaria.com/scripts/serve-local.sh"

set -euo pipefail

# Risolvi la root del repo indipendentemente dalla directory corrente di chiamata
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Verifica che Hugo sia installato
if ! command -v hugo >/dev/null 2>&1; then
    echo "Errore: 'hugo' non trovato nel PATH." >&2
    echo "Installa Hugo Extended con: brew install hugo" >&2
    exit 1
fi

# Avviso se non è la versione extended (il tema Congo la richiede)
if ! hugo version | grep -q "extended"; then
    echo "Attenzione: questa installazione di Hugo NON sembra extended." >&2
    echo "Il tema Congo richiede Hugo extended. Reinstalla con: brew reinstall hugo" >&2
    echo
fi

echo "→ Avvio Hugo server su http://localhost:1313"
echo "  Draft visibili: sì"
echo "  Post futuri (scheduled) visibili: sì"
echo "  Rete locale: bind 0.0.0.0 (accessibile da iPhone/iPad sulla stessa WiFi)"
echo "  Auto-reload browser: sì"
echo
echo "  CTRL-C per fermare"
echo

exec hugo server \
    --buildDrafts \
    --buildFuture \
    --bind 0.0.0.0 \
    --navigateToChanged \
    "$@"
