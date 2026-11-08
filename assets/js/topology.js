/* Interactive SD-WAN + hybrid-cloud topology with a live SLA graph (homepage hero) */
(() => {
  'use strict';
  const svg = document.getElementById('topo'); if (!svg) return;
  const $ = s => document.querySelector(s);
  const FR = document.documentElement.lang === 'fr';
  const t = (en, fr) => (FR ? fr : en);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs, parent) => { const el = document.createElementNS(NS, tag); for (const k in attrs) el.setAttribute(k, attrs[k]); parent && parent.appendChild(el); return el; };

  const N = {
    A: { x: 80, y: 70, label: 'SITE-A', sub: 'FG-100F · spoke' },
    B: { x: 80, y: 200, label: 'SITE-B', sub: 'FG-100F · spoke' },
    C: { x: 80, y: 330, label: 'SITE-C', sub: 'FG-60F · spoke' },
    HUB: { x: 268, y: 200, label: 'HQ-HUB', sub: 'FG-200E · AS65001', cls: 'hub' },
    AZ: { x: 452, y: 110, label: 'AZURE', sub: 'VPN Gateway', cls: 'cloud' },
    AWS: { x: 452, y: 290, label: 'AWS', sub: 'Transit Gateway', cls: 'cloud' }
  };
  const spokes = ['A', 'B', 'C'], clouds = ['AZ', 'AWS'];
  const L = [];
  spokes.forEach(s => {
    L.push({ id: s + '1', a: s, b: 'HUB', kind: 'isp1', off: -7, up: true, site: s, name: 'ISP-1' });
    L.push({ id: s + '2', a: s, b: 'HUB', kind: 'isp2', off: 7, up: true, site: s, name: 'ISP-2' });
  });
  clouds.forEach(c => L.push({ id: c, a: 'HUB', b: c, kind: 'tun', off: 0, up: true, site: c, name: 'IPsec/BGP' }));

  const gL = $('#links'), gP = $('#pkts'), gN = $('#nodes');
  const geo = l => {
    const A = N[l.a], B = N[l.b], dx = B.x - A.x, dy = B.y - A.y, len = Math.hypot(dx, dy);
    const nx = -dy / len, ny = dx / len;
    return { x1: A.x + nx * l.off, y1: A.y + ny * l.off, x2: B.x + nx * l.off, y2: B.y + ny * l.off };
  };
  L.forEach(l => {
    const g = geo(l); l.g = g;
    const hit = mk('line', { ...g, class: 'hit', tabindex: 0, role: 'button' }, gL);
    l.el = mk('line', { ...g, class: 'lnk ' + l.kind }, gL);
    const act = () => toggle(l);
    hit.addEventListener('click', act);
    hit.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); act(); } });
    hit.addEventListener('mouseenter', () => l.el.classList.add('hover'));
    hit.addEventListener('mouseleave', () => l.el.classList.remove('hover'));
    mk('title', {}, hit).textContent = `${N[l.a].label} ↔ ${N[l.b].label} (${l.name}): ${t('click to cut / restore', 'cliquer pour couper / rétablir')}`;
  });
  spokes.forEach(s => {
    L.filter(l => l.site === s).forEach(l => {
      mk('text', { x: l.g.x1 + (l.g.x2 - l.g.x1) * .34, y: l.g.y1 + (l.g.y2 - l.g.y1) * .34 + (l.off < 0 ? -6 : 13), class: 'isp-tag' }, gL).textContent = l.kind;
    });
  });
  Object.entries(N).forEach(([k, n]) => {
    const w = k === 'HUB' ? 128 : 112, h = 38;
    const g = mk('g', { class: 'node ' + (n.cls || ''), transform: `translate(${n.x - w / 2},${n.y - h / 2})` }, gN);
    mk('rect', { width: w, height: h, rx: n.cls === 'cloud' ? 19 : 7 }, g);
    n.st = mk('circle', { cx: 12, cy: 13, r: 3.5, class: 'st', fill: n.cls === 'cloud' ? 'var(--violet)' : 'var(--green)' }, g);
    mk('text', { x: 21, y: 17, class: 'lbl' }, g).textContent = n.label;
    mk('text', { x: 12, y: 30, class: 'sub' }, g).textContent = n.sub;
    n.el = g;
  });

  const flows = [];
  [...spokes, ...clouds].forEach((s, i) => {
    for (let j = 0; j < 2; j++) flows.push({
      site: s, t: (i * .23 + j * .5) % 1, dir: j ? -1 : 1, speed: .28 + (i % 3) * .04,
      el: mk('circle', { r: 3.2, class: 'pkt', fill: clouds.includes(s) ? 'var(--violet)' : 'var(--amber)' }, gP)
    });
  });
  const activeLink = site => { const ls = L.filter(l => l.site === site && l.up); return ls.find(l => l.kind === 'isp1') || ls[0] || null; };

  /* log */
  const logEl = $('#log');
  const log = (msg, cls = 'in') => {
    const row = document.createElement('div');
    row.innerHTML = `<span class="ts">${new Date().toTimeString().slice(0, 8)}</span> <span class="${cls}">${msg}</span>`;
    logEl.appendChild(row); logEl.scrollTop = logEl.scrollHeight;
    while (logEl.children.length > 40) logEl.firstChild.remove();
  };

  const refresh = () => {
    let issues = 0;
    L.forEach(l => {
      l.el.classList.toggle('down', !l.up);
      l.el.classList.toggle('standby', l.up && l.kind !== 'tun' && activeLink(l.site) !== l);
    });
    spokes.forEach(s => {
      const up = L.filter(l => l.site === s && l.up), n = N[s];
      n.el.classList.toggle('isolated', up.length === 0);
      n.el.classList.toggle('degraded', up.length === 1);
      n.st.setAttribute('fill', up.length === 2 ? 'var(--green)' : up.length ? 'var(--amber)' : 'var(--red)');
      if (up.length < 2) issues++;
    });
    clouds.forEach(c => {
      const up = L.find(l => l.site === c).up;
      N[c].st.setAttribute('fill', up ? 'var(--violet)' : 'var(--red)');
      N[c].el.classList.toggle('isolated', !up);
      if (!up) issues++;
    });
    const lt = $('#liveTxt');
    lt.textContent = issues ? `${issues} ${t('degraded', 'dégradé(s)')}` : t('all paths up', 'tous les chemins actifs');
    lt.parentElement.style.color = issues ? 'var(--amber)' : 'var(--green)';
  };

  const toggle = (l, quiet) => {
    l.up = !l.up;
    if (!quiet) {
      const site = N[l.site].label;
      if (l.kind === 'tun') {
        log(l.up ? `${site}: ${t('IPsec SA up, BGP Established', 'SA IPsec active, BGP Established')}` : `${site}: ${t('IPsec tunnel down, BGP routes withdrawn', 'tunnel IPsec tombé, routes BGP retirées')}`, l.up ? 'ok' : 'er');
      } else {
        const other = L.find(x => x.site === l.site && x !== l);
        if (!l.up && other.up) log(`${site}: ${t('SLA failed on', 'SLA en échec sur')} ${l.name} → ${t('steered to', 'bascule vers')} ${other.name}`, 'wn');
        else if (!l.up) log(`${site}: ${t('all SD-WAN members down, site isolated', 'tous les membres SD-WAN tombés, site isolé')}`, 'er');
        else if (l.kind === 'isp1') log(`${site}: ${l.name} ${t('SLA recovered → preferred path restored', 'SLA rétabli → chemin préféré restauré')}`, 'ok');
        else log(`${site}: ${l.name} ${t('back up (standby)', 'rétabli (secours)')}`, 'ok');
      }
    }
    refresh();
  };

  $('#failIsp1').onclick = () => {
    L.filter(l => l.kind === 'isp1' && l.up).forEach(l => toggle(l, true));
    log(t('ISP-1 outage injected on all spokes', 'panne ISP-1 injectée sur toutes les agences'), 'er');
    spokes.forEach(s => { if (L.find(l => l.site === s && l.kind === 'isp2').up) log(`${N[s].label}: ${t('SLA probe failed on ISP-1 → steered to ISP-2', 'sonde SLA en échec sur ISP-1 → bascule vers ISP-2')}`, 'wn'); });
    log(t('Lab result: traffic on ISP-2 ≈1.5 s after the failure (static routes: 3–5 min)', 'Résultat lab : trafic sur ISP-2 ≈1,5 s après la panne (routes statiques : 3–5 min)'), 'ok');
  };
  $('#restore').onclick = () => { L.forEach(l => (l.up = true)); refresh(); log(t('All links restored, back on preferred paths', 'Tous les liens rétablis, retour sur les chemins préférés'), 'ok'); };

  log(t('SD-WAN overlay up: 3 spokes × 2 ISPs → HQ hub', 'Overlay SD-WAN actif : 3 agences × 2 FAI → hub HQ'), 'ok');
  log(t('BGP over IPsec established with Azure VPN GW and AWS TGW', 'BGP sur IPsec établi avec Azure VPN GW et AWS TGW'), 'in');
  refresh();

  /* SLA graph: latency of ISP-1 and ISP-2 for the selected site */
  const slaSvg = $('#slaSvg'), sel = $('#slaSite');
  const W = 400, H = 56, MAXMS = 160, PTS = 60, THR = 100;
  const p1 = mk('polyline', { class: 'l1' }, slaSvg), p2 = mk('polyline', { class: 'l2' }, slaSvg);
  mk('line', { x1: 0, x2: W, y1: H - THR / MAXMS * H, y2: H - THR / MAXMS * H, class: 'thr' }, slaSvg);
  const series = {}; spokes.forEach(s => (series[s] = { a: Array(PTS).fill(null), b: Array(PTS).fill(null) }));
  const base = { A: [28, 41], B: [33, 47], C: [46, 58] };
  const sample = (s, k) => {
    const l = L.find(x => x.site === s && x.kind === (k ? 'isp2' : 'isp1'));
    if (!l.up) return MAXMS; // probe timeout drawn at the top
    return base[s][k] + Math.random() * 9 - 3 + (Math.random() < .04 ? 25 : 0);
  };
  const pts = arr => arr.map((v, i) => v == null ? null : `${(i / (PTS - 1) * W).toFixed(1)},${(H - Math.min(v, MAXMS) / MAXMS * H + 1).toFixed(1)}`).filter(Boolean).join(' ');
  const draw = () => {
    const s = sel.value, sr = series[s];
    p1.setAttribute('points', pts(sr.a)); p2.setAttribute('points', pts(sr.b));
    const la = sr.a[PTS - 1], lb = sr.b[PTS - 1];
    $('#slaV1').textContent = la == null ? '—' : la >= MAXMS ? t('timeout', 'perte') : la.toFixed(0) + ' ms';
    $('#slaV2').textContent = lb == null ? '—' : lb >= MAXMS ? t('timeout', 'perte') : lb.toFixed(0) + ' ms';
  };
  const tickSla = () => { spokes.forEach(s => { const sr = series[s]; sr.a.push(sample(s, 0)); sr.a.shift(); sr.b.push(sample(s, 1)); sr.b.shift(); }); draw(); };
  for (let i = 0; i < PTS; i++) tickSla();
  sel.addEventListener('change', draw);
  if (!reduce) setInterval(() => { if (!document.hidden && onScreen) tickSla(); }, 500);

  /* packets */
  const place = f => {
    const l = activeLink(f.site);
    if (!l) { f.el.style.opacity = 0; return; }
    f.el.style.opacity = 1;
    const p = f.dir > 0 ? f.t : 1 - f.t, g = l.g;
    f.el.setAttribute('cx', g.x1 + (g.x2 - g.x1) * p);
    f.el.setAttribute('cy', g.y1 + (g.y2 - g.y1) * p);
  };
  let onScreen = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { onScreen = es[0].isIntersecting; }).observe(svg);
  if (reduce) flows.forEach(place);
  else {
    let last = performance.now();
    const tick = now => {
      const dt = Math.min(.05, (now - last) / 1000); last = now;
      if (!document.hidden && onScreen) flows.forEach(f => { f.t = (f.t + dt * f.speed) % 1; place(f); });
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
})();

/* Full-screen mode for the demo (Fullscreen API, with a CSS fallback for iPhone) */
(() => {
  const fig = document.getElementById('topoFig'), btn = document.getElementById('fsBtn');
  if (!fig || !btn) return;
  const FR = document.documentElement.lang === 'fr';
  const label = btn.querySelector('span');
  const native = !!(fig.requestFullscreen || fig.webkitRequestFullscreen);
  const isFull = () => !!(document.fullscreenElement || document.webkitFullscreenElement) || fig.classList.contains('is-full');
  const sync = () => {
    const on = isFull();
    fig.classList.toggle('full-on', on);
    btn.setAttribute('aria-pressed', on);
    label.textContent = on ? (FR ? 'Quitter' : 'Exit') : (FR ? 'Plein écran' : 'Full screen');
    btn.title = btn.getAttribute('aria-label') ;
    document.body.style.overflow = fig.classList.contains('is-full') ? 'hidden' : '';
  };
  const enter = () => {
    if (native) (fig.requestFullscreen || fig.webkitRequestFullscreen).call(fig).catch?.(() => { fig.classList.add('is-full'); sync(); });
    else { fig.classList.add('is-full'); sync(); }
  };
  const exit = () => {
    if (document.fullscreenElement || document.webkitFullscreenElement) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    fig.classList.remove('is-full'); sync();
  };
  btn.addEventListener('click', () => (isFull() ? exit() : enter()));
  document.addEventListener('fullscreenchange', sync);
  document.addEventListener('webkitfullscreenchange', sync);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && fig.classList.contains('is-full')) exit(); });
})();
