/**
 * Scroll Reveal — lightweight IntersectionObserver for yuyang.nl
 * Adds `.in-view` class to `.scroll-reveal` elements when they enter viewport.
 * No dependencies, ~300 bytes gzipped.
 * Respects static-mode and prefers-reduced-motion.
 */
(function() {
  'use strict';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (document.documentElement.classList.contains('static-mode')) return;
  var els = document.querySelectorAll('.scroll-reveal');
  if (!els.length) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function(el) { obs.observe(el); });
})();
