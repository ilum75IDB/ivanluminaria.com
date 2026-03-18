/* Glossary inline tooltips — vanilla JS, zero dependencies */
(function () {
  'use strict';

  var activeTooltip = null;
  var activeTerm = null;

  function createTooltip(term) {
    var desc = term.getAttribute('data-glossary-desc');
    var url = term.getAttribute('data-glossary-url');
    var more = term.getAttribute('data-glossary-more') || '→';
    if (!desc) return null;

    var tip = document.createElement('div');
    tip.className = 'glossary-tooltip';
    tip.setAttribute('role', 'tooltip');

    var text = document.createElement('span');
    text.className = 'glossary-tooltip-text';
    text.textContent = desc;
    tip.appendChild(text);

    if (url) {
      var link = document.createElement('a');
      link.className = 'glossary-tooltip-link';
      link.href = url;
      link.textContent = more;
      tip.appendChild(link);
    }

    return tip;
  }

  function positionTooltip(tip, term) {
    /* Reset to measure natural size */
    tip.style.left = '0';
    tip.style.top = '0';
    tip.classList.remove('glossary-tooltip--below');

    var rect = term.getBoundingClientRect();
    var tipRect = tip.getBoundingClientRect();
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    var vw = document.documentElement.clientWidth;

    /* Horizontal: center on term, clamp to viewport */
    var left = rect.left + scrollX + (rect.width - tipRect.width) / 2;
    var pad = 8;
    if (left < pad) left = pad;
    if (left + tipRect.width > vw - pad) left = vw - pad - tipRect.width;

    /* Vertical: prefer above, fallback below */
    var gap = 8;
    var top = rect.top + scrollY - tipRect.height - gap;
    if (rect.top - tipRect.height - gap < 0) {
      top = rect.bottom + scrollY + gap;
      tip.classList.add('glossary-tooltip--below');
    }

    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }

  function showTooltip(term) {
    if (activeTerm === term) return;
    hideTooltip();

    var tip = createTooltip(term);
    if (!tip) return;

    document.body.appendChild(tip);
    positionTooltip(tip, term);

    /* Trigger reflow then add visible class for animation */
    tip.offsetHeight; // force layout
    tip.classList.add('glossary-tooltip--visible');

    activeTooltip = tip;
    activeTerm = term;
    term.classList.add('glossary-tip--active');
  }

  function hideTooltip() {
    if (activeTooltip) {
      activeTooltip.remove();
      activeTooltip = null;
    }
    if (activeTerm) {
      activeTerm.classList.remove('glossary-tip--active');
      activeTerm = null;
    }
  }

  /* Detect touch device */
  var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  function init() {
    var terms = document.querySelectorAll('.glossary-tip');
    if (!terms.length) return;

    if (isTouch) {
      /* Mobile: tap to show, tap outside to hide */
      terms.forEach(function (term) {
        term.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          if (activeTerm === term) {
            hideTooltip();
          } else {
            showTooltip(term);
          }
        });
      });

      document.addEventListener('click', function (e) {
        if (activeTooltip && !activeTooltip.contains(e.target)) {
          hideTooltip();
        }
      });
    } else {
      /* Desktop: hover to show */
      terms.forEach(function (term) {
        term.addEventListener('mouseenter', function () {
          showTooltip(term);
        });
        term.addEventListener('mouseleave', function (e) {
          /* Don't hide if mouse moves to tooltip */
          setTimeout(function () {
            if (activeTooltip && !activeTooltip.matches(':hover') && !term.matches(':hover')) {
              hideTooltip();
            }
          }, 100);
        });
      });

      /* Also hide when mouse leaves tooltip */
      document.addEventListener('mouseover', function (e) {
        if (activeTooltip && !activeTooltip.contains(e.target) &&
            activeTerm && !activeTerm.contains(e.target)) {
          hideTooltip();
        }
      });
    }

    /* Hide on scroll (avoids mispositioned tooltips) */
    var scrollTimer;
    window.addEventListener('scroll', function () {
      if (activeTooltip) {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(hideTooltip, 100);
      }
    }, { passive: true });

    /* Hide on Escape */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') hideTooltip();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
