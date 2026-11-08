/* Network toolkit: all calculations run locally in the browser */
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const FR = document.documentElement.lang === 'fr';
  const t = (en, fr) => (FR ? fr : en);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ── IPv4 helpers (unsigned 32-bit) ── */
  const ip2n = s => {
    const p = s.trim().split('.');
    if (p.length !== 4) return null;
    let n = 0;
    for (const o of p) { if (!/^\d{1,3}$/.test(o) || +o > 255) return null; n = n * 256 + +o; }
    return n >>> 0;
  };
  const n2ip = n => [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.');
  const pfx2mask = p => (p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0);
  const mask2pfx = m => { const b = (m >>> 0).toString(2).padStart(32, '0'); return /^1*0*$/.test(b) ? b.indexOf('0') < 0 ? 32 : b.indexOf('0') : null; };
  const bin = n => (n >>> 0).toString(2).padStart(32, '0').replace(/(.{8})(?!$)/g, '$1.');
  const parse = str => {
    const s = str.trim().replace(/\s+/g, ' ');
    let ip, p;
    let m = s.match(/^([\d.]+)\s*\/\s*(\d{1,2})$/);
    if (m) { ip = ip2n(m[1]); p = +m[2]; }
    else if ((m = s.match(/^([\d.]+) ([\d.]+)$/))) { ip = ip2n(m[1]); const mk = ip2n(m[2]); p = mk == null ? null : mask2pfx(mk); }
    else if ((m = s.match(/^([\d.]+)$/))) { ip = ip2n(m[1]); p = 32; }
    if (ip == null || p == null || p > 32) return null;
    return { ip, p };
  };
  const block = (ip, p) => {
    const mask = pfx2mask(p), net = (ip & mask) >>> 0, bc = (net | (~mask >>> 0)) >>> 0;
    const size = 2 ** (32 - p);
    const usable = p >= 31 ? size : size - 2;
    return { mask, net, bc, size, usable, wc: (~mask) >>> 0,
      first: p >= 31 ? net : net + 1, last: p >= 31 ? bc : bc - 1 };
  };
  const kind = ip => {
    const a = ip >>> 24, b = (ip >>> 16) & 255;
    if (a === 10 || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168)) return t('private (RFC 1918)', 'privée (RFC 1918)');
    if (a === 100 && b >= 64 && b <= 127) return t('shared / CGNAT (RFC 6598)', 'partagée / CGNAT (RFC 6598)');
    if (a === 169 && b === 254) return t('link-local (APIPA)', 'lien local (APIPA)');
    if (a === 127) return 'loopback';
    if (a >= 224 && a <= 239) return 'multicast';
    if ((a === 192 && b === 0) || (a === 198 && (b === 51 || b === 18 || b === 19)) || (a === 203 && b === 0)) return t('documentation / test', 'documentation / test');
    return t('public', 'publique');
  };
  const rows = arr => '<table class="kv">' + arr.map(([k, v, c]) => `<tr><th>${k}</th><td${c ? ' class="mono"' : ''}>${v}</td></tr>`).join('') + '</table>';
  const err = msg => `<div class="terr">⚠ ${msg}</div>`;
  const fmt = n => n.toLocaleString(FR ? 'fr-FR' : 'en-GB');

  /* ── 1. subnet calculator ── */
  const snIn = $('#snIn'), snOut = $('#snOut');
  const sn = () => {
    const r = parse(snIn.value);
    if (!r) { snOut.innerHTML = err(t('Use a format like 10.0.0.1/24 or 10.0.0.1 255.255.255.0', 'Format attendu : 10.0.0.1/24 ou 10.0.0.1 255.255.255.0')); return; }
    const b = block(r.ip, r.p);
    snOut.innerHTML = `<div class="big mono">${n2ip(b.net)}<span>/${r.p}</span></div>` + rows([
      [t('Network', 'Réseau'), n2ip(b.net), 1],
      [t('Broadcast', 'Diffusion'), r.p >= 31 ? '—' : n2ip(b.bc), 1],
      [t('Host range', 'Plage d’hôtes'), `${n2ip(b.first)} – ${n2ip(b.last)}`, 1],
      [t('Usable hosts', 'Hôtes utilisables'), fmt(b.usable) + (r.p === 31 ? ' (RFC 3021 p2p)' : ''), 0],
      [t('Mask', 'Masque'), n2ip(b.mask), 1],
      ['Wildcard', n2ip(b.wc), 1],
      [t('Address type', 'Type d’adresse'), kind(r.ip), 0],
      [t('Mask in binary', 'Masque en binaire'), `<span class="binm">${bin(b.mask)}</span>`, 1]
    ]);
  };

  /* ── 2. VLSM planner ── */
  const vlBase = $('#vlBase'), vlReq = $('#vlReq'), vlOut = $('#vlOut');
  const vl = () => {
    const base = parse(vlBase.value);
    if (!base) { vlOut.innerHTML = err(t('Invalid address block.', 'Bloc d’adresses invalide.')); return; }
    const B = block(base.ip, base.p);
    const reqs = vlReq.value.split('\n').map(l => l.trim()).filter(Boolean).map(l => {
      const m = l.match(/^(.*?)[\s,;:]+(\d+)$/); return m ? { name: m[1].trim() || '?', hosts: +m[2] } : { bad: l };
    });
    const bad = reqs.find(r => r.bad);
    if (bad) { vlOut.innerHTML = err(t('Cannot read line: ', 'Ligne illisible : ') + esc(bad.bad)); return; }
    const need = r => { if (r.hosts <= 2) return 30; let p = 32 - Math.ceil(Math.log2(r.hosts + 2)); return Math.max(p, 0); };
    const sorted = reqs.map((r, i) => ({ ...r, i, p: need(r) })).sort((a, b) => a.p - b.p || a.i - b.i);
    let cur = B.net; const out = []; let overflow = false;
    for (const r of sorted) {
      const size = 2 ** (32 - r.p);
      cur = Math.ceil(cur / size) * size;
      if (cur + size - 1 > B.bc) { overflow = true; out.push({ ...r, fail: true }); continue; }
      out.push({ ...r, b: block(cur, r.p) }); cur += size;
    }
    const used = out.filter(o => !o.fail).reduce((s, o) => s + o.b.size, 0);
    const pct = Math.round(used / B.size * 100);
    vlOut.innerHTML =
      `<div class="vl-bar" title="${pct}%"><i style="width:${Math.min(pct, 100)}%"></i></div>
       <div class="vl-sum mono">${fmt(used)} / ${fmt(B.size)} ${t('addresses used', 'adresses utilisées')} (${pct}%)${overflow ? ` · <span style="color:var(--red)">${t('block too small', 'bloc trop petit')}</span>` : ''}</div>
       <div class="tbl-wrap"><table class="t"><thead><tr><th>${t('Segment', 'Segment')}</th><th>${t('Need', 'Besoin')}</th><th>${t('Subnet', 'Sous-réseau')}</th><th>${t('Range', 'Plage')}</th><th>${t('Free', 'Libres')}</th></tr></thead><tbody>` +
      out.map(o => o.fail
        ? `<tr><td>${esc(o.name)}</td><td>${o.hosts}</td><td colspan="3" style="color:var(--red)">${t('does not fit', 'ne rentre pas')}</td></tr>`
        : `<tr><td>${esc(o.name)}</td><td>${o.hosts}</td><td class="mono">${n2ip(o.b.net)}/${o.p}</td><td class="mono">${n2ip(o.b.first)} – ${n2ip(o.b.last)}</td><td>${fmt(o.b.usable - o.hosts)}</td></tr>`).join('') +
      `</tbody></table></div>`;
  };

  /* ── 3. wildcard & ACL ── */
  const wcIn = $('#wcIn'), wcAct = $('#wcAct'), wcOut = $('#wcOut');
  const wc = () => {
    const r = parse(wcIn.value);
    if (!r) { wcOut.innerHTML = err(t('Invalid network.', 'Réseau invalide.')); return; }
    const b = block(r.ip, r.p), a = wcAct.value, net = n2ip(b.net), w = n2ip(b.wc), m = n2ip(b.mask);
    const host = r.p === 32;
    const cisco = host ? `${a} ip host ${net} any` : `${a} ip ${net} ${w} any`;
    const fgt = `config firewall address\n    edit "NET_${net.replace(/\./g, '-')}_${r.p}"\n        set subnet ${net} ${m}\n    next\nend`;
    const ospf = `network ${net} ${w} area 0`;
    const changed = b.net !== r.ip && !host ? `<div class="tnote">${t('Host bits were set: using network', 'Des bits d’hôte étaient positionnés : réseau utilisé')} ${net}/${r.p}</div>` : '';
    wcOut.innerHTML = changed + rows([['Prefix', '/' + r.p, 1], [t('Mask', 'Masque'), m, 1], ['Wildcard', w, 1]]) +
      snippet('Cisco IOS · extended ACL', cisco) + snippet('Cisco IOS · OSPF', ospf) + snippet('FortiOS · address object', fgt);
  };
  const snippet = (title, txt) => `<div class="code"><div class="ch"><span>${title}</span><button type="button" data-c="${esc(txt)}">copy</button></div><pre>${esc(txt)}</pre></div>`;

  /* ── 4. IPsec MTU / MSS ── */
  const ms = () => {
    const mtu = +$('#msMtu').value || 1500, enc = $('#msEnc').value;
    const nat = $('#msNat').checked, gre = $('#msGre').checked, ppp = $('#msPpp').checked;
    // tunnel-mode ESP worst case: outer IP 20 + SPI/seq 8 + IV + max padding + pad-len/next-header 2 + ICV
    const iv = enc === 'gcm' ? 8 : 16, pad = enc === 'gcm' ? 3 : 15, icv = enc === 'cbc1' ? 12 : 16;
    const parts = [];
    if (ppp) parts.push(['PPPoE', 8]);
    parts.push([t('Outer IP header', 'En-tête IP externe'), 20]);
    if (nat) parts.push(['NAT-T UDP', 8]);
    parts.push(['ESP SPI + seq', 8], ['IV', iv], [t('Padding (max)', 'Bourrage (max)'), pad], ['Pad len + next header', 2], ['ICV', icv]);
    if (gre) parts.push(['GRE + inner IP', 24]);
    const over = parts.reduce((s, p) => s + p[1], 0);
    let tmtu = mtu - over;
    tmtu = Math.floor(tmtu / 8) * 8;          // keep it on an 8-byte boundary
    const mss = tmtu - 40;
    $('#msOut').innerHTML =
      `<div class="big mono">${tmtu}<span> MTU</span> · ${mss}<span> MSS</span></div>` +
      '<table class="kv">' + parts.map(([k, v]) => `<tr><th>${k}</th><td class="mono">${v} B</td></tr>`).join('') +
      `<tr><th><b>${t('Total overhead', 'Surcoût total')}</b></th><td class="mono"><b>${over} B</b></td></tr></table>` +
      snippet('Cisco IOS · tunnel interface', `interface Tunnel0\n ip mtu ${tmtu}\n ip tcp adjust-mss ${mss}`) +
      snippet('FortiOS · firewall policy', `config firewall policy\n    edit <id>\n        set tcp-mss-sender ${mss}\n        set tcp-mss-receiver ${mss}\n    next\nend`) +
      `<div class="tnote">${t('Estimate with worst-case padding. Validate with ping -f -l (Windows) or ping -M do -s (Linux) across the tunnel.', 'Estimation avec le pire cas de bourrage. À valider avec ping -f -l (Windows) ou ping -M do -s (Linux) à travers le tunnel.')}</div>`;
  };

  /* ── wiring ── */
  const on = (els, fn) => { els.forEach(e => e && ['input', 'change'].forEach(ev => e.addEventListener(ev, fn))); fn(); };
  on([snIn], sn); on([vlBase, vlReq], vl); on([wcIn, wcAct], wc);
  on(['#msMtu', '#msEnc', '#msNat', '#msGre', '#msPpp'].map(s => $(s)), ms);
  document.querySelectorAll('[data-ex]').forEach(b => b.addEventListener('click', () => { const i = document.getElementById(b.dataset.ex); i.value = b.textContent; i.dispatchEvent(new Event('input')); }));
  document.addEventListener('click', e => {
    const b = e.target.closest('button[data-c]'); if (!b) return;
    navigator.clipboard && navigator.clipboard.writeText(b.dataset.c).then(() => { b.textContent = '✓'; setTimeout(() => (b.textContent = 'copy'), 1200); });
  });
  /* tabs highlight */
  const tabs = [...document.querySelectorAll('.tool-tabs a')];
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) tabs.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('section.tool').forEach(s => io.observe(s));
  }
})();
