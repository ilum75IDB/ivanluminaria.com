#!/bin/zsh
# =====================================================================
# generate-cv-pdfs.sh
# ---------------------------------------------------------------------
# Genera tutti i CV PDF EN a partire dai file Markdown in docs/,
# usando pandoc + WeasyPrint con il CSS in scripts/resumes/template/.
#
# Output: static/downloads/CV_*_202609_EN.pdf
#
# Prerequisiti:
#   - pandoc    (brew install pandoc)
#   - weasyprint (brew install weasyprint  oppure  pip install weasyprint)
#
# Uso:
#   ./scripts/resumes/generate-cv-pdfs.sh          # tutti i CV
#   ./scripts/resumes/generate-cv-pdfs.sh -h       # help
#
# Convenzioni di naming:
#   docs/CV_<Role>_Ivan_Luminaria_<YYYYMM>_EN.md   → sorgente
#   static/downloads/<same-name>.pdf                → output
# =====================================================================
set -euo pipefail

# ---------- Percorsi (assoluti, robusti a cwd) ----------
SCRIPT_DIR="${0:A:h}"                          # dir di questo script
ROOT="${SCRIPT_DIR:h:h}"                       # …/ivanluminaria.com
DOCS="$ROOT/docs"
OUT="$ROOT/static/downloads"
CSS="$SCRIPT_DIR/template/cv-style.css"

# ---------- PATH augmentation ----------
# Se WeasyPrint è installato via pip3 --user, il binario sta in
# ~/Library/Python/3.x/bin/ che NON è nel PATH di default su macOS.
# Aggiungiamo tutti i possibili path Python user-site al PATH interno.
for pyver in 3.14 3.13 3.12 3.11 3.10 3.9; do
  candidate="$HOME/Library/Python/${pyver}/bin"
  [[ -d "$candidate" ]] && PATH="${candidate}:${PATH}"
done
export PATH

# ---------- Help ----------
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Uso: generate-cv-pdfs.sh [-h|--help]

Genera i 5 CV PDF EN in static/downloads/ a partire dai file MD
in docs/. Usa pandoc + WeasyPrint con il CSS di scripts/resumes/template/.

Prerequisiti:
  - pandoc       (brew install pandoc)
  - weasyprint   (brew install weasyprint  OPPURE  pip install weasyprint)

CV attesi (già presenti in docs/):
  - CV_Technical_Leader_Ivan_Luminaria_202609_EN.md
  - CV_DWH_Architect_Ivan_Luminaria_202609_EN.md
  - CV_Oracle_DBA_Ivan_Luminaria_202609_EN.md
  - CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN.md
  - CV_Project_Manager_Ivan_Luminaria_202609_EN.md
EOF
  exit 0
fi

# ---------- Sanity check ----------
command -v pandoc >/dev/null 2>&1 || {
  echo "❌ pandoc non installato. Installa con: brew install pandoc"
  exit 1
}
command -v weasyprint >/dev/null 2>&1 || {
  echo "❌ weasyprint non installato."
  echo "   Installa con: brew install weasyprint  OPPURE  pip install weasyprint"
  exit 1
}
[[ -f "$CSS" ]] || {
  echo "❌ CSS non trovato: $CSS"
  exit 1
}

# ---------- Lista dei CV attesi ----------
CVS=(
  "CV_Technical_Leader_Ivan_Luminaria_202609_EN"
  "CV_DWH_Architect_Ivan_Luminaria_202609_EN"
  "CV_Oracle_DBA_Ivan_Luminaria_202609_EN"
  "CV_Oracle_PLSQL_Ivan_Luminaria_202609_EN"
  "CV_Project_Manager_Ivan_Luminaria_202609_EN"
)

mkdir -p "$OUT"

# ---------- Loop di generazione ----------
GENERATED=0
SKIPPED=0
FAILED=0

for cv in "${CVS[@]}"; do
  MD="$DOCS/${cv}.md"
  PDF="$OUT/${cv}.pdf"

  if [[ ! -f "$MD" ]]; then
    echo "⚠️  Skip: $MD non trovato"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  echo "▶️  Generating $(basename "$PDF")"
  if pandoc "$MD" \
       --from markdown+raw_html \
       --to html5 \
       --standalone \
       --metadata title="Ivan Luminaria — CV" \
       --css "$CSS" \
       --pdf-engine=weasyprint \
       --output "$PDF" 2>&1 | grep -v "^$" || true; then
    if [[ -f "$PDF" ]]; then
      SIZE=$(du -h "$PDF" | cut -f1)
      echo "   ✅ $SIZE — $PDF"
      GENERATED=$((GENERATED + 1))
    else
      echo "   ❌ Output non prodotto"
      FAILED=$((FAILED + 1))
    fi
  else
    echo "   ❌ pandoc failure"
    FAILED=$((FAILED + 1))
  fi
done

# ---------- Riepilogo ----------
echo ""
echo "══════════════════════════════════════════════════════"
echo "🎯 Generazione completata"
echo "   ✅ generati:  $GENERATED"
echo "   ⚠️  saltati:   $SKIPPED"
echo "   ❌ falliti:   $FAILED"
echo "   📂 output in: $OUT"
echo "══════════════════════════════════════════════════════"

# Exit code = numero di errori (0 = tutto ok)
exit $FAILED
