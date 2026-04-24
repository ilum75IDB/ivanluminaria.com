/*
 * assets/js/search.js — override del search.js del tema Congo.
 *
 * Hugo Pipes prende l'asset dal progetto prima del tema (resources.Get),
 * quindi questo file sostituisce completamente il JS della search.
 *
 * Differenze dal tema:
 *  - Markup split column (sinistra: lista raggruppata per kind / destra: preview)
 *  - Raggruppamento per kind: article / glossary / tag
 *  - Highlight dei match con <mark>
 *  - Tastiera: ↑ ↓ per navigare, Enter per aprire, Esc per chiudere, / per aprire
 *  - Sync automatica della preview in base al risultato focalizzato
 *
 * Dipende da: Fuse.js (caricato dallo stesso bundle del tema).
 */

(function () {
  "use strict";

  var fuse = null;
  var indexed = false;
  var searchVisible = false;
  var lastResults = [];
  var selectedIndex = -1;
  var currentQuery = "";

  var wrapper = document.getElementById("search-wrapper");
  var modal = document.getElementById("search-modal");
  var input = document.getElementById("search-query");
  var closeBtn = document.getElementById("close-search-button");
  var listEl = document.getElementById("search-list");
  var previewEl = document.getElementById("search-preview");
  var countEl = document.getElementById("search-count");

  if (!wrapper || !input || !listEl || !previewEl) return;

  var showButtons = document.querySelectorAll("[id^='search-button']");
  var lang = wrapper.getAttribute("data-lang") || "it";

  var LABELS = {
    it: { articles: "Articoli", glossary: "Glossario", tags: "Tag", result: "risultato", results: "risultati", readTheArticle: "Leggi l'articolo", readDefinition: "Leggi la definizione", viewTag: "Vedi tutti gli articoli", emptyQuery: "Inizia a digitare per cercare…", noResults: "Nessun risultato per", previewHint: "Seleziona un risultato per vedere l'anteprima" },
    en: { articles: "Articles", glossary: "Glossary", tags: "Tags", result: "result", results: "results", readTheArticle: "Read the article", readDefinition: "Read definition", viewTag: "See all articles", emptyQuery: "Start typing to search…", noResults: "No results for", previewHint: "Select a result to see the preview" },
    es: { articles: "Artículos", glossary: "Glosario", tags: "Etiquetas", result: "resultado", results: "resultados", readTheArticle: "Leer el artículo", readDefinition: "Leer la definición", viewTag: "Ver todos los artículos", emptyQuery: "Empieza a escribir para buscar…", noResults: "Sin resultados para", previewHint: "Selecciona un resultado para ver la vista previa" },
    ro: { articles: "Articole", glossary: "Glosar", tags: "Etichete", result: "rezultat", results: "rezultate", readTheArticle: "Citește articolul", readDefinition: "Citește definiția", viewTag: "Vezi toate articolele", emptyQuery: "Începe să scrii pentru a căuta…", noResults: "Niciun rezultat pentru", previewHint: "Selectează un rezultat pentru previzualizare" }
  };
  var L = LABELS[lang] || LABELS.it;

  // ----- Event wiring -----
  showButtons.forEach(function (b) { b.addEventListener("click", displaySearch); });
  if (closeBtn) closeBtn.addEventListener("click", hideSearch);
  wrapper.addEventListener("click", hideSearch);
  if (modal) {
    modal.addEventListener("click", function (ev) { ev.stopPropagation(); });
  }
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "/" && !searchVisible && !isTextInputFocused(ev.target)) {
      ev.preventDefault();
      displaySearch();
      return;
    }
    if (!searchVisible) return;
    if (ev.key === "Escape") { hideSearch(); return; }
    if (ev.key === "ArrowDown") { ev.preventDefault(); moveSelection(1); return; }
    if (ev.key === "ArrowUp") { ev.preventDefault(); moveSelection(-1); return; }
    if (ev.key === "Enter") {
      ev.preventDefault();
      var cur = lastResults[selectedIndex];
      if (cur) window.location.href = cur.item.permalink;
    }
  });
  input.addEventListener("input", onInputChange);

  function isTextInputFocused(el) {
    if (!el) return false;
    var tag = (el.tagName || "").toLowerCase();
    return tag === "input" || tag === "textarea" || el.isContentEditable;
  }

  // ----- Show/hide -----
  function displaySearch() {
    if (!indexed) buildIndex();
    if (searchVisible) return;
    document.body.style.overflow = "hidden";
    wrapper.style.visibility = "visible";
    input.focus();
    searchVisible = true;
  }
  function hideSearch() {
    if (!searchVisible) return;
    document.body.style.overflow = "visible";
    wrapper.style.visibility = "hidden";
    input.value = "";
    currentQuery = "";
    lastResults = [];
    selectedIndex = -1;
    renderEmpty();
    if (countEl) countEl.textContent = "";
    searchVisible = false;
  }

  // ----- Index -----
  function buildIndex() {
    var baseURL = wrapper.getAttribute("data-url") || "/";
    if (baseURL.charAt(baseURL.length - 1) !== "/") baseURL += "/";
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
      if (req.readyState !== 4) return;
      if (req.status !== 200) return;
      try {
        var data = JSON.parse(req.responseText);
        var options = {
          shouldSort: true,
          ignoreLocation: true,
          threshold: 0.0,
          includeMatches: true,
          keys: [
            { name: "title", weight: 0.6 },
            { name: "aka", weight: 0.25 },
            { name: "summary", weight: 0.1 },
            { name: "section", weight: 0.05 }
          ]
        };
        fuse = new Fuse(data, options);
        indexed = true;
        if (currentQuery) executeQuery(currentQuery);
      } catch (e) { /* silent */ }
    };
    req.open("GET", baseURL + "index.json");
    req.send();
  }

  // ----- Query handling -----
  function onInputChange() {
    currentQuery = input.value.trim();
    if (!currentQuery) {
      lastResults = [];
      selectedIndex = -1;
      renderEmpty();
      if (countEl) countEl.textContent = "";
      return;
    }
    if (!indexed) return;
    executeQuery(currentQuery);
  }

  function executeQuery(q) {
    if (!fuse) return;
    var results = fuse.search(q);
    lastResults = results;
    selectedIndex = results.length > 0 ? 0 : -1;
    renderResults(q, results);
    updateCount(results.length);
  }

  function updateCount(n) {
    if (!countEl) return;
    if (n === 0) { countEl.textContent = ""; return; }
    countEl.textContent = n + " " + (n === 1 ? L.result : L.results);
  }

  // ----- Render -----
  function renderEmpty() {
    listEl.innerHTML = '<div class="search-empty-v2" data-empty-state>' +
      '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>' +
      '<p>' + escapeHTML(L.emptyQuery) + '</p>' +
      '</div>';
    previewEl.innerHTML = '<div class="search-preview-empty-v2" data-preview-empty><p>' + escapeHTML(L.previewHint) + '</p></div>';
  }

  function renderNoResults(q) {
    listEl.innerHTML = '<div class="search-noresults-v2">' +
      '<p>' + escapeHTML(L.noResults) + ' <strong>"' + escapeHTML(q) + '"</strong></p>' +
      '</div>';
    previewEl.innerHTML = '<div class="search-preview-empty-v2" data-preview-empty><p>' + escapeHTML(L.previewHint) + '</p></div>';
  }

  function renderResults(q, results) {
    if (!results || results.length === 0) { renderNoResults(q); return; }

    var groups = { article: [], glossary: [], tag: [] };
    results.forEach(function (r, i) {
      var k = r.item.kind || "article";
      if (!groups[k]) groups[k] = [];
      r._idx = i;
      groups[k].push(r);
    });

    var html = "";
    if (groups.article.length) html += renderGroup(L.articles, groups.article, q);
    if (groups.glossary.length) html += renderGroup(L.glossary, groups.glossary, q);
    if (groups.tag.length) html += renderGroup(L.tags, groups.tag, q);

    listEl.innerHTML = html;

    // Click → seleziona la riga e mostra la preview (NON naviga).
    // Double-click → apre la pagina (shortcut per utenti che lo preferiscono).
    // La navigazione avviene tramite Enter sulla tastiera o click sul CTA
    // nella card di preview a destra.
    var rows = listEl.querySelectorAll("[data-result-idx]");
    rows.forEach(function (row) {
      row.addEventListener("click", function (ev) {
        ev.preventDefault();
        selectedIndex = parseInt(row.getAttribute("data-result-idx"), 10);
        applySelectionStyles();
        renderPreview(lastResults[selectedIndex]);
      });
      row.addEventListener("dblclick", function (ev) {
        ev.preventDefault();
        var idx = parseInt(row.getAttribute("data-result-idx"), 10);
        window.location.href = lastResults[idx].item.permalink;
      });
    });

    applySelectionStyles();
    if (selectedIndex >= 0) renderPreview(lastResults[selectedIndex]);
  }

  function renderGroup(label, items, q) {
    var rows = items.map(function (r) { return renderRow(r, q); }).join("");
    return '<div class="search-group-v2">' +
      '<div class="search-group-label-v2">' + escapeHTML(label) + '</div>' +
      rows +
    '</div>';
  }

  function renderRow(result, q) {
    var item = result.item;
    var kind = item.kind || "article";
    var iconHTML = kindIcon(kind);
    var subtitle = "";
    if (kind === "article") {
      subtitle = (item.date ? escapeHTML(item.date) : "");
    } else if (kind === "glossary") {
      subtitle = escapeHTML(item.section || L.glossary);
    } else if (kind === "tag") {
      subtitle = escapeHTML(item.summary || "");
    }
    return '<a class="search-row-v2" data-result-idx="' + result._idx + '" href="' + item.permalink + '">' +
      '<span class="search-row-icon-v2 search-row-icon-' + kind + '" aria-hidden="true">' + iconHTML + '</span>' +
      '<span class="search-row-content-v2">' +
        '<span class="search-row-title-v2">' + highlight(item.title, q) + '</span>' +
        '<span class="search-row-subtitle-v2">' + subtitle + '</span>' +
      '</span>' +
    '</a>';
  }

  function applySelectionStyles() {
    var rows = listEl.querySelectorAll("[data-result-idx]");
    rows.forEach(function (row) {
      var idx = parseInt(row.getAttribute("data-result-idx"), 10);
      if (idx === selectedIndex) {
        row.classList.add("is-selected");
        // scroll into view se fuori
        var r = row.getBoundingClientRect();
        var p = listEl.getBoundingClientRect();
        if (r.top < p.top) row.scrollIntoView({ block: "nearest" });
        else if (r.bottom > p.bottom) row.scrollIntoView({ block: "nearest" });
      } else {
        row.classList.remove("is-selected");
      }
    });
  }

  function moveSelection(delta) {
    if (!lastResults.length) return;
    selectedIndex = (selectedIndex + delta + lastResults.length) % lastResults.length;
    applySelectionStyles();
    renderPreview(lastResults[selectedIndex]);
  }

  // ----- Preview (right side) -----
  function renderPreview(result) {
    if (!result) { previewEl.innerHTML = '<div class="search-preview-empty-v2"><p>' + escapeHTML(L.previewHint) + '</p></div>'; return; }
    var item = result.item;
    var kind = item.kind || "article";
    var html = '';

    if (kind === "article") {
      var coverHTML = item.thumbnail
        ? '<div class="search-preview-cover-v2" style="background-image:url(' + JSON.stringify(item.thumbnail) + ');"></div>'
        : '<div class="search-preview-cover-v2 search-preview-cover-placeholder-v2"></div>';
      html += '<span class="search-preview-badge-v2 search-preview-badge-article">' + escapeHTML(L.articles) + '</span>';
      html += coverHTML;
      html += '<h2 class="search-preview-title-v2">' + escapeHTML(item.title) + '</h2>';
      var metaParts = [];
      if (item.section) metaParts.push('<span>' + escapeHTML(item.section) + '</span>');
      if (item.date) metaParts.push('<span>' + escapeHTML(item.date) + '</span>');
      if (item.readingTime) metaParts.push('<span>' + item.readingTime + ' min</span>');
      if (metaParts.length) {
        html += '<div class="search-preview-meta-v2">' + metaParts.join('<span class="search-preview-meta-sep-v2">·</span>') + '</div>';
      }
      if (item.excerpt) {
        html += '<p class="search-preview-excerpt-v2">' + escapeHTML(item.excerpt) + '</p>';
      }
      html += '<a class="search-preview-cta-v2" href="' + item.permalink + '">' +
        escapeHTML(L.readTheArticle) +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>' +
      '</a>';
    } else if (kind === "glossary") {
      html += '<span class="search-preview-badge-v2 search-preview-badge-glossary">' + escapeHTML(L.glossary) + '</span>';
      html += '<h2 class="search-preview-title-v2">' + escapeHTML(item.title) + '</h2>';
      if (item.aka) {
        html += '<p class="search-preview-aka-v2">' + escapeHTML(item.aka) + '</p>';
      }
      if (item.excerpt) {
        html += '<p class="search-preview-excerpt-v2">' + escapeHTML(item.excerpt) + '</p>';
      }
      html += '<a class="search-preview-cta-v2" href="' + item.permalink + '">' +
        escapeHTML(L.readDefinition) +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>' +
      '</a>';
    } else if (kind === "tag") {
      html += '<span class="search-preview-badge-v2 search-preview-badge-tag">' + escapeHTML(L.tags) + '</span>';
      html += '<h2 class="search-preview-title-v2">#' + escapeHTML(item.title) + '</h2>';
      if (item.summary) {
        html += '<p class="search-preview-meta-v2"><span>' + escapeHTML(item.summary) + '</span></p>';
      }
      if (item.excerpt) {
        html += '<p class="search-preview-excerpt-v2">' + escapeHTML(item.excerpt) + '</p>';
      }
      html += '<a class="search-preview-cta-v2" href="' + item.permalink + '">' +
        escapeHTML(L.viewTag) +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>' +
      '</a>';
    }

    previewEl.innerHTML = html;
  }

  // ----- Helpers -----
  function escapeHTML(s) {
    if (s == null) return "";
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[c];
    });
  }

  function highlight(text, query) {
    var esc = escapeHTML(text);
    if (!query) return esc;
    var terms = query.split(/\s+/).filter(Boolean).map(function (t) { return regexEscape(t); });
    if (!terms.length) return esc;
    var re = new RegExp("(" + terms.join("|") + ")", "ig");
    return esc.replace(re, "<mark>$1</mark>");
  }

  function regexEscape(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  function kindIcon(kind) {
    if (kind === "glossary") return "📖";
    if (kind === "tag") return "🏷";
    return "📄";
  }

  // Initial empty render
  renderEmpty();
})();
