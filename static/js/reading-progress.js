// Reading Progress Bar
// Gestisce: barra principale sotto navbar, badge floating bottom-right,
// mini-card nella sidebar autore. Tutti e tre si aggiornano in sincrono
// in funzione dello scroll dentro l'<article>.
//
// Si autodisattiva se nella pagina non c'e' la barra (.reading-progress-bar)
// o se non c'e' un <article>. Persistente da pct > 5 a pct 100; scompare
// solo se l'utente torna proprio all'inizio della pagina.
//
// Tutto vanilla, niente librerie, scroll listener passivo + rAF.
(function () {
  const bar = document.querySelector('.reading-progress-bar');
  const article = document.querySelector('article');
  if (!bar || !article) return;

  const barFill = bar.querySelector('.reading-progress-bar-fill');
  const floatBadge = document.querySelector('.reading-percent');
  const floatBadgeVal = floatBadge ? floatBadge.querySelector('.reading-percent-val') : null;
  const sideBadge = document.querySelector('.reading-percent-sidebar');
  const sideBadgeVal = sideBadge ? sideBadge.querySelector('.reading-percent-val') : null;
  const sideMini = sideBadge ? sideBadge.querySelector('.reading-percent-mini-fill') : null;

  let scheduled = false;

  function update() {
    scheduled = false;
    const articleTop = article.offsetTop;
    const articleHeight = article.offsetHeight;
    const viewportHeight = window.innerHeight;
    const scrollY = window.scrollY;
    const totalScrollable = articleHeight - viewportHeight;
    if (totalScrollable <= 0) {
      bar.style.setProperty('--reading-progress', '0%');
      return;
    }
    const progress = Math.max(0, Math.min(1, (scrollY - articleTop) / totalScrollable));
    const pct = Math.round(progress * 100);
    const pctStr = pct + '%';

    if (barFill) barFill.style.width = pctStr;
    else bar.style.setProperty('--reading-progress', pctStr);

    const shouldShow = pct > 5;

    if (floatBadge) {
      if (floatBadgeVal) floatBadgeVal.textContent = pctStr;
      floatBadge.classList.toggle('visible', shouldShow);
    }
    if (sideBadge) {
      if (sideBadgeVal) sideBadgeVal.textContent = pctStr;
      if (sideMini) sideMini.style.width = pctStr;
      sideBadge.classList.toggle('visible', shouldShow);
    }
  }

  function onScroll() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();

  // Rileva quando il footer entra in viewport e nasconde gli elementi
  // floating (badge percentuale + scroll-to-top del theme Congo) per
  // evitare la sovrapposizione con i link di navigazione e le icone social.
  const footer = document.querySelector('footer');
  const toTop = document.getElementById('to-top');
  if (footer && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const nearFooter = entries[0].isIntersecting;
      if (floatBadge) floatBadge.classList.toggle('near-footer', nearFooter);
      if (toTop) toTop.classList.toggle('near-footer', nearFooter);
    }, { rootMargin: '0px 0px -80px 0px' });
    observer.observe(footer);
  }
})();
