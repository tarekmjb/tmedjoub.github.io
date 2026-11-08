/* Homepage: animated network mesh, expertise explorer, resource center */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. hero mesh: drifting nodes linked when close ── */
  const cv = $('#mesh');
  if (cv && cv.getContext) {
    const ctx = cv.getContext('2d');
    let W = 0, H = 0, dpr = 1, nodes = [], run = true, raf;
    const N = () => Math.round(Math.min(70, Math.max(28, W * H / 22000)));
    const size = () => {
      const r = cv.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1);
      W = r.width; H = r.height; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      nodes = Array.from({ length: N() }, () => ({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25, r: Math.random() * 1.6 + 1 }));
    };
    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      const D = 150;
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
          if (d < D) { ctx.strokeStyle = `rgba(96,190,255,${(1 - d / D) * .28})`; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
      }
      for (const n of nodes) { ctx.fillStyle = 'rgba(140,210,255,.75)'; ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, 7); ctx.fill(); }
    };
    const step = () => {
      for (const n of nodes) { n.x += n.vx; n.y += n.vy; if (n.x < 0 || n.x > W) n.vx *= -1; if (n.y < 0 || n.y > H) n.vy *= -1; }
      draw(); if (run) raf = requestAnimationFrame(step);
    };
    size(); draw();
    addEventListener('resize', () => { size(); draw(); });
    if (!reduce) {
      new IntersectionObserver(es => { const v = es[0].isIntersecting; if (v && !run) { run = true; step(); } else if (!v) { run = false; cancelAnimationFrame(raf); } }).observe(cv);
      step();
    }
  }

  /* ── 2. expertise explorer (tabs, deep-linkable: #expertise-security) ── */
  const tabs = $$('.xt'), panels = $$('.xp');
  const showX = (id, scroll) => {
    if (!panels.some(p => p.id === id)) return false;
    panels.forEach(p => (p.hidden = p.id !== id));
    tabs.forEach(b => { const on = b.getAttribute('aria-controls') === id; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1; });
    if (scroll) $('#expertise').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    return true;
  };
  tabs.forEach((b, i) => {
    b.addEventListener('click', () => { showX(b.getAttribute('aria-controls')); history.replaceState(null, '', '#' + b.getAttribute('aria-controls')); });
    b.addEventListener('keydown', e => {
      const k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key]; if (!k) return;
      e.preventDefault(); const n = tabs[(i + k + tabs.length) % tabs.length]; n.click(); n.focus();
    });
  });
  const fromHash = () => { const h = location.hash.slice(1); if (h.startsWith('expertise-')) showX(h, true); };
  addEventListener('hashchange', fromHash); fromHash();
  document.addEventListener('click', e => {   // links to #expertise-x from tiles / menu on the same page
    const a = e.target.closest('a[href*="#expertise-"]'); if (!a) return;
    const id = a.getAttribute('href').split('#')[1];
    if (showX(id, true)) { e.preventDefault(); history.replaceState(null, '', '#' + id); }
  });

  /* ── 3. resource center: filter + "show all" ── */
  const grid = $('#resGrid'), more = $('#resMore'), LIMIT = 8;
  if (grid) {
    let f = 'all', expanded = false;
    const apply = () => {
      let shown = 0, total = 0;
      $$('.res', grid).forEach(c => {
        const match = f === 'all' || c.dataset.k === f;
        if (match) total++;
        const vis = match && (expanded || f !== 'all' || shown < LIMIT);
        if (vis) shown++;
        c.hidden = !vis;
      });
      more.parentElement.hidden = expanded || f !== 'all' || total <= LIMIT;
    };
    $('.res-filter').addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      $$('.res-filter button').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
      f = b.dataset.f; apply();
    });
    more.addEventListener('click', () => { expanded = true; apply(); });
    apply();
  }
})();
