// Article TOC scroll-spy (sidebar option C)
// Evidenzia il link del TOC corrispondente al paragrafo H2 corrente
// in viewport. Si autodisattiva se la pagina non ha la card TOC.
// Vanilla, IntersectionObserver, niente dipendenze.
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

  // Trova gli H2 referenziati dal TOC
  const targets = Object.keys(linkById)
    .map((id) => document.getElementById(id))
    .filter(Boolean);
  if (targets.length === 0) return;

  if (!('IntersectionObserver' in window)) return;

  // Stato: tracciamo l'ultimo id attivato per evitare flicker
  let activeId = null;

  function setActive(id) {
    if (id === activeId) return;
    activeId = id;
    links.forEach((a) => a.classList.remove('active'));
    const link = linkById[id];
    if (link) link.classList.add('active');
  }

  // Tracciamo quali H2 sono visibili. Quando ce ne sono piu' di uno
  // attivo (es. fra una sezione e l'altra), prendiamo quello piu' in alto
  // (top piu' piccolo positivo).
  const visible = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) visible.add(e.target.id);
        else visible.delete(e.target.id);
      });
      // Prendi l'H2 piu' vicino al top tra quelli visibili
      if (visible.size > 0) {
        let best = null;
        let bestTop = Infinity;
        targets.forEach((t) => {
          if (visible.has(t.id)) {
            const top = t.getBoundingClientRect().top;
            if (top >= 0 && top < bestTop) { bestTop = top; best = t.id; }
          }
        });
        if (best) setActive(best);
      } else {
        // Nessun H2 in viewport: trova quello piu' vicino sopra il viewport
        let last = null;
        targets.forEach((t) => {
          if (t.getBoundingClientRect().top < 0) last = t.id;
        });
        if (last) setActive(last);
      }
    },
    {
      // 20% dall'alto, 70% dal basso: l'H2 e' "attivo" quando entra
      // nella fascia centrale dello schermo
      rootMargin: '-20% 0% -70% 0%',
      threshold: 0,
    }
  );
  targets.forEach((t) => observer.observe(t));

  // Inizializzazione: se siamo gia' scrollati al carico (es. con un #anchor),
  // forziamo un check iniziale dopo un tick
  setTimeout(() => {
    const fromHash = window.location.hash.slice(1);
    if (fromHash && linkById[fromHash]) {
      setActive(fromHash);
    } else {
      // Trova il primo H2 sopra il viewport (o il primissimo)
      let last = targets[0].id;
      targets.forEach((t) => {
        if (t.getBoundingClientRect().top < window.innerHeight * 0.3) last = t.id;
      });
      setActive(last);
    }
  }, 50);
})();
