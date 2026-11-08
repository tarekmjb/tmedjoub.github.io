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

  /* ── 1. IPv4 subnet calculator (calculator.net style) ── */
  const snIn = $('#snIn'), snOut = $('#snOut'), snMask = $('#snMask'), snNets = $('#snNets');
  const classMin = { any: 1, A: 8, B: 16, C: 24 };
  const fillMasks = (keep) => {
    const cls = document.querySelector('input[name="snClass"]:checked').value, min = classMin[cls];
    let cur = keep != null ? keep : +snMask.value || 24;
    if (cur < min) cur = min;
    let h = '';
    for (let p = 32; p >= min; p--) h += `<option value="${p}"${p === cur ? ' selected' : ''}>${n2ip(pfx2mask(p))} /${p}</option>`;
    snMask.innerHTML = h;
  };
  const ipClass = ip => { const a = ip >>> 24; return a < 128 ? 'A' : a < 192 ? 'B' : a < 224 ? 'C' : a < 240 ? 'D (multicast)' : 'E (' + t('reserved', 'réservée') + ')'; };
  const hex4 = n => n.toString(16).padStart(4, '0');
  const sn = () => {
    let raw = snIn.value.trim();
    const m = raw.match(/^([\d.]+)\s*(?:\/\s*(\d{1,2})|\s+([\d.]+))$/);
    if (m) {   // pasted "ip/p" or "ip mask": move the prefix into the dropdown
      const p = m[2] != null ? +m[2] : mask2pfx(ip2n(m[3]) ?? -1);
      if (p != null && p >= 1 && p <= 32) {
        if (p < classMin[document.querySelector('input[name="snClass"]:checked').value]) document.querySelector('input[name="snClass"][value="any"]').checked = true;
        fillMasks(p); snIn.value = m[1]; raw = m[1];
      }
    }
    const ip = ip2n(raw), p = +snMask.value;
    if (ip == null) { snOut.innerHTML = err(t('Enter a valid IPv4 address, e.g. 10.0.0.1', 'Saisissez une adresse IPv4 valide, ex. 10.0.0.1')); snNets.innerHTML = ''; return; }
    const b = block(ip, p);
    const o = [ip >>> 24, (ip >>> 16) & 255, (ip >>> 8) & 255, ip & 255];
    snOut.innerHTML = `<div class="big mono">${n2ip(b.net)}<span>/${p}</span></div>` + rows([
      [t('IP address', 'Adresse IP'), n2ip(ip), 1],
      [t('Network address', 'Adresse réseau'), n2ip(b.net), 1],
      [t('Usable host IP range', 'Plage d’hôtes utilisables'), `${n2ip(b.first)} – ${n2ip(b.last)}`, 1],
      [t('Broadcast address', 'Adresse de diffusion'), p >= 31 ? '—' : n2ip(b.bc), 1],
      [t('Total number of hosts', 'Nombre total d’adresses'), fmt(b.size), 0],
      [t('Number of usable hosts', 'Hôtes utilisables'), fmt(b.usable) + (p === 31 ? ' (RFC 3021)' : ''), 0],
      [t('Subnet mask', 'Masque de sous-réseau'), n2ip(b.mask), 1],
      [t('Wildcard mask', 'Masque générique (wildcard)'), n2ip(b.wc), 1],
      [t('Binary subnet mask', 'Masque en binaire'), `<span class="binm">${bin(b.mask)}</span>`, 1],
      [t('IP class', 'Classe IP'), ipClass(ip), 0],
      [t('CIDR notation', 'Notation CIDR'), '/' + p, 1],
      [t('IP type', 'Type d’adresse'), kind(ip), 0],
      [t('Short', 'Forme courte'), `${n2ip(ip)} /${p}`, 1],
      [t('Binary ID', 'ID binaire'), `<span class="binm">${(ip >>> 0).toString(2).padStart(32, '0')}</span>`, 1],
      [t('Integer ID', 'ID entier'), String(ip >>> 0), 1],
      [t('Hex ID', 'ID hexadécimal'), '0x' + (ip >>> 0).toString(16).padStart(8, '0'), 1],
      ['in-addr.arpa', `${o[3]}.${o[2]}.${o[1]}.${o[0]}.in-addr.arpa`, 1],
      [t('IPv4-mapped address', 'Adresse IPv4 mappée'), `::ffff:${hex4((ip >>> 16) & 0xffff)}:${hex4(ip & 0xffff)}`, 1],
      [t('6to4 prefix', 'Préfixe 6to4'), `2002:${hex4((ip >>> 16) & 0xffff)}:${hex4(ip & 0xffff)}::/48`, 1]
    ]);
    // all possible networks inside the classful-style parent (/24, /16 or /8)
    const parentP = p >= 24 ? 24 : p >= 16 ? 16 : p >= 8 ? 8 : 0;
    const count = 2 ** (p - parentP), pnet = (ip & pfx2mask(parentP)) >>> 0, size = 2 ** (32 - p);
    const label = parentP === 24 ? `${o[0]}.${o[1]}.${o[2]}.*` : parentP === 16 ? `${o[0]}.${o[1]}.*.*` : parentP === 8 ? `${o[0]}.*.*.*` : '*.*.*.*';
    const MAX = 256, shown = Math.min(count, MAX);
    let trs = '';
    const start = count > MAX ? Math.max(0, Math.min(count - MAX, Math.floor((b.net - pnet) / size) - MAX / 2)) : 0;
    for (let i = start; i < start + shown; i++) {
      const net = pnet + i * size, bb = block(net, p), cur = net === b.net;
      trs += `<tr${cur ? ' class="cur"' : ''}><td class="mono">${n2ip(net)}</td><td class="mono">${n2ip(bb.first)} – ${n2ip(bb.last)}</td><td class="mono">${p >= 31 ? '—' : n2ip(bb.bc)}</td></tr>`;
    }
    snNets.innerHTML = `<h3>${t(`All ${fmt(count)} possible /${p} networks for ${label}`, `Les ${fmt(count)} réseaux /${p} possibles pour ${label}`)}</h3>` +
      (count > MAX ? `<p class="tnote">${t(`Showing ${MAX} networks around yours.`, `Affichage de ${MAX} réseaux autour du vôtre.`)}</p>` : '') +
      `<div class="tbl-wrap nets"><table class="t"><thead><tr><th>${t('Network address', 'Adresse réseau')}</th><th>${t('Usable host range', 'Plage d’hôtes utilisables')}</th><th>${t('Broadcast address', 'Adresse de diffusion')}</th></tr></thead><tbody>${trs}</tbody></table></div>`;
    const cur = snNets.querySelector('tr.cur'), wrap = snNets.querySelector('.nets');
    if (cur && wrap) wrap.scrollTop = cur.offsetTop - wrap.clientHeight / 2;
  };
  document.querySelectorAll('input[name="snClass"]').forEach(r => r.addEventListener('change', () => { fillMasks(); sn(); }));
  fillMasks(26);

  /* ── 1b. IPv6 subnet calculator (BigInt) ── */
  const v6In = $('#v6In'), v6Pfx = $('#v6Pfx'), v6Out = $('#v6Out');
  v6Pfx.innerHTML = Array.from({ length: 128 }, (_, i) => 128 - i).map(p => `<option value="${p}"${p === 64 ? ' selected' : ''}>/${p}${p === 64 ? ' *' : ''}</option>`).join('');
  const v6parse = str => {
    let s = str.trim().toLowerCase();
    if (!s || /[^0-9a-f:.]/.test(s) || (s.match(/::/g) || []).length > 1) return null;
    let tail = [];
    const v4 = s.match(/(\d+\.\d+\.\d+\.\d+)$/);
    if (v4) { const n = ip2n(v4[1]); if (n == null) return null; tail = [(n >>> 16).toString(16), (n & 0xffff).toString(16)]; s = s.slice(0, -v4[1].length) + 'x'; }
    let [l, r] = s.includes('::') ? s.split('::') : [s, null];
    const L = l ? l.split(':') : [], R = r != null ? (r ? r.split(':') : []) : [];
    const fix = arr => arr.flatMap(x => (x === 'x' ? tail : [x]));
    const Lf = fix(L), Rf = fix(R);
    let groups;
    if (r == null) groups = Lf; else { const fill = 8 - Lf.length - Rf.length; if (fill < 1) return null; groups = [...Lf, ...Array(fill).fill('0'), ...Rf]; }
    if (groups.length !== 8 || groups.some(g => !/^[0-9a-f]{1,4}$/.test(g))) return null;
    return groups.reduce((acc, g) => (acc << 16n) + BigInt(parseInt(g, 16)), 0n);
  };
  const v6groups = n => Array.from({ length: 8 }, (_, i) => Number((n >> BigInt(112 - 16 * i)) & 0xffffn));
  const v6full = n => v6groups(n).map(g => g.toString(16).padStart(4, '0')).join(':');
  const v6short = n => {
    const g = v6groups(n).map(x => x.toString(16));
    let best = [-1, 0], cur = [-1, 0];
    g.forEach((x, i) => { if (x === '0') { if (cur[0] < 0) cur = [i, 0]; cur[1]++; if (cur[1] > best[1]) best = [...cur]; } else cur = [-1, 0]; });
    if (best[1] < 2) return g.join(':');
    return (g.slice(0, best[0]).join(':') + '::' + g.slice(best[0] + best[1]).join(':'));
  };
  const v6type = n => {
    const top = Number(n >> 112n);
    if (n === 0n) return t('unspecified', 'non spécifiée');
    if (n === 1n) return 'loopback';
    if ((n >> 32n) === 0xffffn) return t('IPv4-mapped', 'IPv4 mappée') + ' (' + n2ip(Number(n & 0xffffffffn)) + ')';
    if ((top & 0xffc0) === 0xfe80) return t('link-local', 'lien local');
    if ((top & 0xfe00) === 0xfc00) return t('unique local (ULA)', 'locale unique (ULA)');
    if ((top & 0xff00) === 0xff00) return 'multicast';
    if (top === 0x2001 && Number((n >> 96n) & 0xffffn) === 0x0db8) return t('documentation (2001:db8::/32)', 'documentation (2001:db8::/32)');
    if (top === 0x2002) return '6to4';
    if ((top & 0xe000) === 0x2000) return t('global unicast', 'unicast globale');
    return t('reserved / other', 'réservée / autre');
  };
  const v6 = () => {
    let raw = v6In.value.trim();
    const m = raw.match(/^(.+)\/(\d{1,3})$/);
    if (m && +m[2] >= 1 && +m[2] <= 128) { v6Pfx.value = m[2]; v6In.value = raw = m[1].trim(); }
    const n = v6parse(raw), p = BigInt(+v6Pfx.value);
    if (n == null) { v6Out.innerHTML = err(t('Enter a valid IPv6 address, e.g. 2001:db8::1', 'Saisissez une adresse IPv6 valide, ex. 2001:db8::1')); return; }
    const all = (1n << 128n) - 1n, host = (1n << (128n - p)) - 1n, mask = all ^ host;
    const net = n & mask, last = net | host, total = 1n << (128n - p);
    const totalTxt = total.toLocaleString(FR ? 'fr-FR' : 'en-GB') + (p <= 64n ? ` (2<sup>${128n - p}</sup>)` : '');
    v6Out.innerHTML = `<div class="big mono">${v6short(net)}<span>/${p}</span></div>` + rows([
      [t('IP address', 'Adresse IP'), v6short(n), 1],
      [t('Full IP address', 'Adresse complète'), v6full(n), 1],
      [t('Network', 'Réseau'), `${v6short(net)}/${p}`, 1],
      [t('Prefix length', 'Longueur de préfixe'), '/' + p, 1],
      [t('Network range', 'Plage du réseau'), `${v6full(net)}<br>${v6full(last)}`, 1],
      [t('Total IP addresses', 'Nombre total d’adresses'), totalTxt, 0],
      [t('Address type', 'Type d’adresse'), v6type(n), 0],
      [t('Subnets of /64 inside', 'Sous-réseaux /64 contenus'), p <= 64n ? (1n << (64n - p)).toLocaleString(FR ? 'fr-FR' : 'en-GB') : '—', 0],
      ['ip6.arpa', `<span class="binm">${v6full(n).replace(/:/g, '').split('').reverse().join('.')}.ip6.arpa</span>`, 1]
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
  on([snIn, snMask], sn); on([v6In, v6Pfx], v6); on([vlBase, vlReq], vl); on([wcIn, wcAct], wc);
  on(['#msMtu', '#msEnc', '#msNat', '#msGre', '#msPpp'].map(s => $(s)), ms);
  document.querySelectorAll('[data-ex]').forEach(b => b.addEventListener('click', () => { const i = document.getElementById(b.dataset.ex); i.value = b.textContent; i.dispatchEvent(new Event('input')); }));
  document.addEventListener('click', e => {
    const b = e.target.closest('button[data-c]'); if (!b) return;
    navigator.clipboard && navigator.clipboard.writeText(b.dataset.c).then(() => { b.textContent = '✓'; setTimeout(() => (b.textContent = 'copy'), 1200); });
  });
  /* tabs: one tool visible at a time, linkable with #subnet, #vlsm, #wildcard, #mss */
  const tabs = [...document.querySelectorAll('.tool-tabs a')];
  const panels = [...document.querySelectorAll('section.tool')];
  document.body.classList.add('tools-tabbed');
  const show = (id, focus) => {
    if (!panels.some(p => p.id === id)) id = panels[0].id;
    panels.forEach(p => { p.hidden = p.id !== id; });
    tabs.forEach(a => {
      const on = a.getAttribute('href') === '#' + id;
      a.classList.toggle('on', on); a.setAttribute('aria-selected', on); a.tabIndex = on ? 0 : -1;
      if (on && focus) a.focus();
    });
    const inp = document.querySelector('#' + id + ' .tin');
    if (focus === 'input' && inp) inp.focus();
  };
  tabs.forEach((a, i) => {
    a.addEventListener('click', e => { e.preventDefault(); const id = a.getAttribute('href').slice(1); history.replaceState(null, '', '#' + id); show(id); });
    a.addEventListener('keydown', e => {
      const k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!k) return;
      e.preventDefault(); const n = tabs[(i + k + tabs.length) % tabs.length]; n.click(); n.focus();
    });
  });
  addEventListener('hashchange', () => show(location.hash.slice(1)));
  show(location.hash.slice(1));
})();
