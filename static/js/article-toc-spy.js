// Article TOC scroll-spy (sidebar option C)
// Evidenzia il link del TOC corrispondente al paragrafo H2 corrente
// in viewport. Si autodisattiva se la pagina non ha la card TOC.
// Vanilla, scroll listener + rAF, niente dipendenze.
(function () {
  const toc = document.querySelector('.article-toc-card');
  if (!toc) return;

  const links = Array.from(toc.querySelectorAll('.article-toc-list a'));
  if (links.length === 0) return;

  // Mappa: id -> link
  const linkById = {};
  links.forEach((a) => {
    const href = a.getAttribute('href') || '';
    if (href.startsWith('#')) linkById[href.slice(1)] = a;
  });

  // Trova gli H2 referenziati dal TOC, in ordine di apparizione nel DOM
  const targets = Object.keys(linkById)
    .map((id) => document.getElementById(id))
    .filter(Boolean)
    .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  if (targets.length === 0) return;

  let activeId = null;
  function setActive(id) {
    if (id === activeId) return;
    activeId = id;
    links.forEach((a) => a.classList.remove('active'));
    const link = linkById[id];
    if (link) link.classList.add('active');
  }

  // L'H2 attivo e' l'ULTIMO che ha il suo top sopra la "linea di lettura"
  // (25% dall'alto del viewport). E' equivalente a: la sezione in cui sto
  // leggendo e' quella iniziata piu' di recente, prima del punto attuale.
  function pickActive() {
    const lineY = window.innerHeight * 0.25;
    let candidate = null;
    for (const h2 of targets) {
      const top = h2.getBoundingClientRect().top;
      if (top <= lineY) {
        candidate = h2.id;
      } else {
        // Gli H2 successivi sono sotto la linea, stop
        break;
      }
    }
    // Se siamo sopra il primo H2 (preambolo), attiva comunque il primo
    if (!candidate && targets.length > 0) {
      const firstTop = targets[0].getBoundingClientRect().top;
      if (firstTop < window.innerHeight) {
        candidate = targets[0].id;
      }
    }
    if (candidate) setActive(candidate);
  }

  let scheduled = false;
  function onScroll() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      pickActive();
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });

  // Inizializzazione: se siamo gia' su un #anchor, evidenzia quello
  // Altrimenti calcola lo stato in base allo scroll attuale
  const fromHash = window.location.hash.slice(1);
  if (fromHash && linkById[fromHash]) {
    setActive(fromHash);
  } else {
    pickActive();
  }
})();
