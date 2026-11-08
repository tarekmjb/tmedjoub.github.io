/* Tarek Medjoub portfolio: site-wide behaviour (theme, nav, console, code blocks, TOC) */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const LANG = root.lang === 'fr' ? 'fr' : 'en';
  const BASE = root.dataset.root || '';            // relative path to site root
  const LP = LANG === 'fr' ? 'fr/' : '';            // language prefix
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const t = (en, fr) => (LANG === 'fr' ? fr : en);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ── theme ── */
  const setTheme = th => { root.dataset.theme = th; try { localStorage.setItem('tm-theme', th); } catch (e) {} };
  $('#themeBtn') && ($('#themeBtn').onclick = () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));

  /* ── language memory ── */
  $$('[data-lang]').forEach(a => a.addEventListener('click', () => { try { localStorage.setItem('tm-lang', a.dataset.lang); } catch (e) {} }));

  /* ── mobile menu ── */
  const nav = $('#nav'), mb = $('#menuBtn');
  if (nav && mb) {
    mb.onclick = () => { const o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); };
    nav.addEventListener('click', e => { if (e.target.tagName === 'A') { nav.classList.remove('open'); mb.setAttribute('aria-expanded', false); } });
  }


  /* ── mega menu: click / hover on desktop, accordion on mobile ── */
  const mmBtns = $$('.mm-btn');
  const desk = () => matchMedia('(min-width: 1061px)').matches;
  const closeAll = except => mmBtns.forEach(b => { if (b !== except) { b.setAttribute('aria-expanded', 'false'); b.parentElement.classList.remove('open'); } });
  const openMM = (b, on) => { b.setAttribute('aria-expanded', on); b.parentElement.classList.toggle('open', on); };
  mmBtns.forEach(b => {
    const li = b.parentElement; let tmr;
    b.addEventListener('click', e => { e.stopPropagation(); const on = b.getAttribute('aria-expanded') !== 'true'; closeAll(b); openMM(b, on); });
    li.addEventListener('mouseenter', () => { if (!desk()) return; clearTimeout(tmr); tmr = setTimeout(() => { closeAll(b); openMM(b, true); }, 90); });
    li.addEventListener('mouseleave', () => { if (!desk()) return; clearTimeout(tmr); tmr = setTimeout(() => openMM(b, false), 160); });
    li.querySelector('.mm-panel').addEventListener('click', e => { if (e.target.closest('a')) { closeAll(); nav && nav.classList.remove('open'); mb && mb.setAttribute('aria-expanded', false); } });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.mm')) closeAll(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && mmBtns.some(b => b.getAttribute('aria-expanded') === 'true')) { const b = mmBtns.find(b => b.getAttribute('aria-expanded') === 'true'); closeAll(); b.focus(); } });
  /* header shadow once scrolled */
  const bar = $('.bar');
  if (bar) { const sc = () => bar.classList.toggle('scrolled', scrollY > 8); addEventListener('scroll', sc, { passive: true }); sc(); }

  /* ── toast + copy ── */
  const toast = msg => {
    const el = $('#toast'); if (!el) return;
    el.textContent = msg; el.classList.add('show');
    clearTimeout(el._h); el._h = setTimeout(() => el.classList.remove('show'), 1800);
  };
  const copy = (txt, label) => (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject())
    .then(() => toast(label || t('copied', 'copié'))).catch(() => toast(t('copy failed', 'échec de la copie')));
  $$('[data-copy]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); copy(b.dataset.copy, t('copied: ', 'copié : ') + b.dataset.copy); }));

  /* ── code blocks: light syntax colouring + copy ── */
  $$('div.code').forEach(block => {
    const pre = $('pre', block), btn = $('button', block);
    const raw = pre.textContent;
    const lines = raw.split('\n').map(line => {
      let h = esc(line);
      if (/^\s*(!|#|\/\/)/.test(line)) return `<span class="c">${h}</span>`;
      h = h.replace(/(&quot;[^&]*?&quot;)/g, '<span class="s">$1</span>');
      h = h.replace(/^(\s*)(config|edit|set|unset|next|end|interface|router|ip|ipv6|vlan|standby|network|neighbor|address-family|access-list|route-map|crypto|spanning-tree|switchport|channel-group|show|get|diagnose|execute|hostname|no|mpls|vrf|rd|route-target|snmp-server|logging|ntp|service|line|description|bfd|key|tunnel|- name|tasks|hosts|vars)\b/,
        '$1<span class="kw">$2</span>');
      h = h.replace(/\b(\d{1,3}(?:\.\d{1,3}){3}(?:\/\d{1,2})?)\b/g, '<span class="n">$1</span>');
      return h;
    });
    pre.innerHTML = lines.join('\n');
    btn && btn.addEventListener('click', () => copy(raw, t('config copied', 'configuration copiée')));
  });


  /* ── staggered reveals for card grids ── */
  $$('.tiles,.res-grid,.cx-grid,.cred-grid,.rel-grid,.skills-grid,.edu-row').forEach(g => {
    [...g.children].forEach((c, i) => { c.classList.add('reveal'); c.style.transitionDelay = Math.min(i, 8) * 60 + 'ms'; });
  });
  /* ── cursor spotlight on cards ── */
  if (matchMedia('(hover: hover)').matches && !reduce) {
    document.addEventListener('pointermove', e => {
      const c = e.target.closest('.tile,.res,.card-x,.rel-card,.hf-card,.cred,.jr-card,.mm-feature,.split-art');
      if (!c) return;
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }

  /* ── reveal on scroll ── */
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
    $$('.reveal').forEach(el => io.observe(el));
  } else $$('.reveal').forEach(el => el.classList.add('in'));

  /* ── active link in nav (home) and TOC (doc pages) ── */
  const spy = (links, targets) => {
    if (!('IntersectionObserver' in window) || !links.length) return;
    const so = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id));
    }), { rootMargin: '-40% 0px -55% 0px' });
    targets.forEach(s => so.observe(s));
  };
  if (nav) spy($$('a[href^="#"]', nav), $$('section.sec[id]'));
  const toc = $('.toc');
  if (toc) spy($$('a', toc), $$('.doc-body section[id]'));

  /* ── reading progress (doc pages) ── */
  const prog = $('.progress');
  if (prog) {
    const upd = () => { const h = document.documentElement; const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight); prog.style.width = (p * 100).toFixed(1) + '%'; };
    addEventListener('scroll', upd, { passive: true }); upd();
  }


  /* ── back to top: appears after one screen, highlighted at the end of the page ── */
  const top = $('#toTop');
  if (top) {
    const upd = () => {
      const h = document.documentElement, y = h.scrollTop || document.body.scrollTop;
      top.classList.toggle('show', y > innerHeight * .8);
      top.classList.toggle('end', y + innerHeight >= h.scrollHeight - 120);
    };
    addEventListener('scroll', upd, { passive: true }); upd();
    const goTop = e => { e && e.preventDefault(); scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); history.replaceState(null, '', location.pathname); };
    top.addEventListener('click', goTop);
    $$('[data-top]').forEach(a => a.addEventListener('click', goTop));
  }


  /* ── lab filter (homepage) ── */
  const lf = $('.lab-filter');
  if (lf) lf.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    $$('button', lf).forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
    const f = b.dataset.f;
    $$('.ifs tbody tr').forEach(r => r.classList.toggle('hide', f !== 'all' && r.dataset.cat !== f));
  });

  /* ── heading anchors on case studies / labs: click to copy a direct link ── */
  $$('.doc-body section[id] > h2').forEach(h => {
    const id = h.parentElement.id, a = document.createElement('a');
    a.className = 'anc'; a.href = '#' + id; a.textContent = '#';
    a.setAttribute('aria-label', t('Copy link to this section', 'Copier le lien vers cette section'));
    a.addEventListener('click', e => {
      e.preventDefault(); history.replaceState(null, '', '#' + id);
      copy(location.href, t('link copied', 'lien copié'));
    });
    h.appendChild(a);
  });

  /* ── year ── */
  $$('.yr').forEach(el => (el.textContent = new Date().getFullYear()));

  /* ── contact form → mailto ── */
  const cf = $('#cf');
  cf && cf.addEventListener('submit', e => {
    e.preventDefault();
    const em = $('#cfEmail'), err = $('#cfEmailErr');
    const n = $('#cfName').value.trim(), mail = em.value.trim(), o = $('#cfOrg').value.trim(), tp = $('#cfTopic').value, m = $('#cfMsg').value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail)) {
      err.textContent = t('Please enter a valid email address so I can reply.', 'Indiquez une adresse e-mail valide pour que je puisse vous répondre.');
      em.setAttribute('aria-invalid', 'true'); em.focus(); return;
    }
    err.textContent = ''; em.removeAttribute('aria-invalid');
    const subj = `[Portfolio] ${tp}${o ? ' — ' + o : ''}`;
    const body = `${m}\n\n— ${n}${o ? ', ' + o : ''}\n${t('Reply to', 'Répondre à')}: ${mail}`;
    location.href = `mailto:tarek.medjoub@outlook.fr?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
  });
  const cfe = $('#cfEmail');
  cfe && cfe.addEventListener('input', () => { if (cfe.getAttribute('aria-invalid')) { $('#cfEmailErr').textContent = ''; cfe.removeAttribute('aria-invalid'); } });


  /* ═════════ SITE SEARCH (Ctrl+K or /) ═════════ */
  (() => {
    const sb = $('#sdBack'), si = $('#sdIn'), sr = $('#sdRes'), btn = $('#searchBtn');
    if (!sb) return;
    const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    let items = [], sel = 0, lastFocus = null;
    const data = () => (window.SEARCH_INDEX && window.SEARCH_INDEX[LANG]) || [];
    const ICO = { case: 'M4 7h16v12H4zM9 7V5h6v2', lab: 'M9 3v6l-5 9a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-5-9V3M8 3h8', tool: 'M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z', sec: 'M4 6h16M4 12h10M4 18h14', act: 'M5 12h14M13 6l6 6-6 6' };
    const kindOf = y => /lab/i.test(y) ? 'lab' : /tool|outil/i.test(y) ? 'tool' : /case|étude/i.test(y) ? 'case' : 'sec';
    const actions = () => [
      { y: t('Action', 'Action'), t: t('Contact Tarek', 'Contacter Tarek'), d: 'tarek.medjoub@outlook.fr', u: LP + 'index.html#contact', a: 'go' },
      { y: t('Action', 'Action'), t: t('Download CV (PDF)', 'Télécharger le CV (PDF)'), d: t('One page', 'Une page'), u: LANG === 'fr' ? 'assets/CV_Tarek_MEDJOUB.pdf' : 'assets/CV_Tarek_MEDJOUB_EN.pdf', a: 'go' },
      { y: t('Action', 'Action'), t: t('Switch light / dark theme', 'Basculer thème clair / sombre'), d: '', a: 'theme' },
      { y: t('Action', 'Action'), t: t('Open the network console', 'Ouvrir la console réseau'), d: t('Type commands like “show version”', 'Tapez des commandes comme « show version »'), a: 'console' }
    ];
    const featured = () => {
      const d = data(), pick = u => d.find(i => i.u === LP + u);
      return [pick('projects/sdwan.html'), pick('projects/hybrid-cloud.html'), pick('tools.html#subnet'), pick('labs/bgp.html'), pick('index.html#expertise-security')].filter(Boolean).concat(actions().slice(0, 2));
    };
    const hl = (txt, terms) => {
      let h = esc(txt);
      terms.forEach(q => { if (q.length < 2) return; const i = norm(h).indexOf(q); if (i >= 0) h = h.slice(0, i) + '<mark>' + h.slice(i, i + q.length) + '</mark>' + h.slice(i + q.length); });
      return h;
    };
    const run = q => {
      const terms = norm(q).split(/\s+/).filter(Boolean);
      if (!terms.length) { items = featured(); render(items, [], t('Suggested', 'Suggestions')); return; }
      const scored = [];
      data().concat(actions()).forEach(it => {
        const T = norm(it.t), D = norm(it.d || ''), K = norm(it.k || ''), Y = norm(it.y);
        let sc = 0;
        for (const w of terms) {
          if (T.includes(w)) sc += T.startsWith(w) ? 12 : 8; else if (K.includes(w) || Y.includes(w)) sc += 4; else if (D.includes(w)) sc += 2; else { sc = 0; break; }
        }
        if (sc) scored.push([sc - (it.t.includes('›') ? 3 : 0), it]);
      });
      scored.sort((a, b) => b[0] - a[0]);
      items = scored.slice(0, 12).map(x => x[1]);
      render(items, terms, items.length ? `${items.length} ${t('results', 'résultats')}` : '');
    };
    const render = (list, terms, head) => {
      sel = 0;
      if (!list.length) { sr.innerHTML = `<div class="sd-empty">${t('No results. Try “BGP”, “subnet”, “Azure” or “failover”.', 'Aucun résultat. Essayez « BGP », « sous-réseau », « Azure » ou « bascule ».')}</div>`; return; }
      sr.innerHTML = (head ? `<div class="sd-head">${head}</div>` : '') + list.map((it, i) => {
        const k = it.a ? 'act' : kindOf(it.y);
        return `<a class="sd-item k-${k}" role="option" id="sdo${i}" aria-selected="${i === 0}" href="${it.u ? BASE + it.u : '#'}" data-i="${i}">
          <span class="sd-ico"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="${ICO[k]}"/></svg></span>
          <span class="sd-txt"><b>${hl(it.t, terms)}</b>${it.d ? `<small>${hl(it.d, terms)}</small>` : ''}</span><span class="sd-type">${esc(it.y)}</span></a>`;
      }).join('');
      mark();
    };
    const mark = () => { $$('.sd-item', sr).forEach((a, i) => a.setAttribute('aria-selected', i === sel)); const c = $('#sdo' + sel); if (c) { c.scrollIntoView({ block: 'nearest' }); si.setAttribute('aria-activedescendant', c.id); } };
    const act = (i, ev) => {
      const it = items[i]; if (!it) return;
      if (it.a === 'theme') { ev && ev.preventDefault(); setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'); closeS(); return; }
      if (it.a === 'console') { ev && ev.preventDefault(); closeS(); setTimeout(() => $('#fab') && $('#fab').click(), 50); return; }
      if (!ev) location.href = BASE + it.u;
      closeS(true);
    };
    const openS = () => { lastFocus = document.activeElement; sb.hidden = false; requestAnimationFrame(() => sb.classList.add('open')); si.value = ''; run(''); si.focus(); document.body.style.overflow = 'hidden'; };
    const closeS = (keep) => { sb.classList.remove('open'); sb.hidden = true; document.body.style.overflow = ''; if (!keep && lastFocus) lastFocus.focus(); };
    btn && btn.addEventListener('click', openS);
    $('#sdClose').addEventListener('click', () => closeS());
    sb.addEventListener('click', e => { if (e.target === sb) closeS(); });
    si.addEventListener('input', () => run(si.value));
    si.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); sel = Math.min(items.length - 1, sel + 1); mark(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); sel = Math.max(0, sel - 1); mark(); }
      else if (e.key === 'Enter') { e.preventDefault(); act(sel); }
      else if (e.key === 'Escape') { e.preventDefault(); closeS(); }
    });
    sr.addEventListener('click', e => { const a = e.target.closest('.sd-item'); if (a) act(+a.dataset.i, e); });
    sr.addEventListener('mousemove', e => { const a = e.target.closest('.sd-item'); if (a && +a.dataset.i !== sel) { sel = +a.dataset.i; mark(); } });
    document.addEventListener('keydown', e => {
      const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
      if ((e.key.toLowerCase() === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !typing)) { e.preventDefault(); sb.hidden ? openS() : closeS(); }
    });
  })();

  /* ═════════ CONSOLE ═════════ */
  const SITE = {
    projects: [
      ['sdwan', 'SD-WAN Enterprise Migration', 'Migration SD-WAN d’entreprise'],
      ['hybrid-cloud', 'Hybrid Cloud Architecture', 'Architecture cloud hybride'],
      ['lan-optimization', 'LAN Architecture Optimisation', 'Optimisation de l’architecture LAN'],
      ['monitoring-stack', 'Monitoring & Alerting Stack', 'Supervision & alerting']
    ],
    labs: [
      ['bgp', 'BGP fundamentals', 'Fondamentaux BGP'],
      ['ospf', 'OSPF multi-area', 'OSPF multi-zones'],
      ['vlan', 'VLANs & inter-VLAN routing', 'VLAN & routage inter-VLAN'],
      ['ipsec', 'IPsec site-to-site VPN', 'VPN IPsec site à site'],
      ['mpls-vrf', 'MPLS L3VPN & VRF', 'MPLS L3VPN & VRF'],
      ['switching-resilience', 'STP & LACP resilience', 'Résilience STP & LACP'],
      ['sdwan-failover', 'SD-WAN path selection & failover', 'SD-WAN : sélection de chemin & bascule'],
      ['fortigate-ha', 'FortiGate HA cluster', 'Cluster FortiGate HA'],
      ['ansible-network', 'Ansible network automation', 'Automatisation réseau Ansible'],
      ['snmp-zabbix', 'SNMPv3 monitoring with Zabbix', 'Supervision SNMPv3 avec Zabbix']
    ]
  };
  const back = $('#conBack'), out = $('#conOut'), inp = $('#conIn');
  if (!back) return;
  const url = p => BASE + LP + p;
  const hist = []; let hi = 0;
  const print = (html, cls) => { const d = document.createElement('div'); if (cls) d.className = cls; d.innerHTML = html; out.appendChild(d); out.scrollTop = out.scrollHeight; };
  const nav2 = (href) => { print(`→ ${esc(href)}`, 'k'); setTimeout(() => (location.href = href), 250); };
  const onHome = !!$('#top');
  const section = id => {
    if (onHome && document.getElementById(id)) { close(); setTimeout(() => document.getElementById(id).scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }), 60); }
    else nav2(url('index.html#' + id));
  };
  const name = r => (LANG === 'fr' ? r[2] : r[1]);
  const C = {
    help: () => print(t(
`<span class="k">available commands</span>
  <span class="p">whoami</span>             who is Tarek
  <span class="p">skills</span>             show ip route skills
  <span class="p">experience</span>         traceroute career
  <span class="p">projects</span>           list case studies
  <span class="p">open</span> &lt;project&gt;     open a case study  (e.g. open sdwan)
  <span class="p">labs</span>               list lab guides
  <span class="p">lab</span> &lt;name&gt;         open a lab guide   (e.g. lab bgp)
  <span class="p">cv</span> [en|fr|web]     download / view CV
  <span class="p">contact</span>            how to reach me
  <span class="p">ping tarek</span>         check availability
  <span class="p">tools</span>              network toolkit (subnet, VLSM, MSS…)
  <span class="p">goto</span> &lt;section&gt;     jump to a homepage section
  <span class="p">theme</span> · <span class="p">fr</span> · <span class="p">en</span> · <span class="p">home</span> · <span class="p">clear</span> · <span class="p">exit</span>`,
`<span class="k">commandes disponibles</span>
  <span class="p">whoami</span>             qui est Tarek
  <span class="p">skills</span>             show ip route skills
  <span class="p">experience</span>         traceroute du parcours
  <span class="p">projects</span>           liste des études de cas
  <span class="p">open</span> &lt;projet&gt;      ouvrir un projet   (ex. open sdwan)
  <span class="p">labs</span>               liste des labs
  <span class="p">lab</span> &lt;nom&gt;          ouvrir un lab      (ex. lab bgp)
  <span class="p">cv</span> [fr|en|web]     télécharger / voir le CV
  <span class="p">contact</span>            me contacter
  <span class="p">ping tarek</span>         vérifier la disponibilité
  <span class="p">tools</span>              outils réseau (sous-réseau, VLSM, MSS…)
  <span class="p">goto</span> &lt;section&gt;     aller à une section
  <span class="p">theme</span> · <span class="p">fr</span> · <span class="p">en</span> · <span class="p">home</span> · <span class="p">clear</span> · <span class="p">exit</span>`)),
    whoami: () => print(t(
`<span class="g">Tarek MEDJOUB</span>, Network, Security & Cloud Engineer, Paris.
Multisite networks · Fortinet security · Hybrid cloud (Azure / AWS).
Former team leader (4 technicians + 2 engineers). MBA in project management.
Now: independent Network & Security Engineer, <span class="g">open to roles</span>.`,
`<span class="g">Tarek MEDJOUB</span>, Ingénieur Réseaux, Sécurité & Cloud, Paris.
Réseaux multisites · Sécurité Fortinet · Cloud hybride (Azure / AWS).
Ancien chef d’équipe (4 techniciens + 2 ingénieurs). MBA en management de projet.
Aujourd’hui : ingénieur réseaux & sécurité indépendant, <span class="g">ouvert aux opportunités</span>.`)),
    skills: () => print(
`<span class="k">Codes: C core, W WAN, V VPN, S security, K cloud, M monitoring</span>
<span class="p">C</span>  Routing      OSPF, BGP, EIGRP, PBR, IPv6
<span class="p">C</span>  Switching    VLAN, STP/RSTP/MSTP, LACP, DHCP snooping, DAI
<span class="p">W</span>  SD-WAN       Fortinet SD-WAN, dual-ISP, FortiManager, FortiAnalyzer
<span class="p">V</span>  VPN          IPsec IKEv1/v2, SSL VPN, GRE, BGP over IPsec
<span class="p">S</span>  Security     FortiGate, DMZ/zones, ACL, IDS/IPS, hardening
<span class="p">K</span>  Cloud        Azure VPN GW, AWS Transit GW, Aviatrix
<span class="p">M</span>  Monitoring   Zabbix, PRTG, OpManager, GLPI`),
    experience: () => print(
`traceroute ${t('to', 'vers')} <span class="g">${t('your-team', 'votre-equipe')}</span>, 30 hops max
 1  <span class="p">3K Solutions</span>           2023        ${t('Network Engineer Intern', 'Stagiaire ingénieur réseau')}
 2  <span class="p">Condor Electronics</span>     2023–2025   ${t('Team Leader & Network Security Project Lead', 'Chef d’équipe & chef de projet sécurité réseau')}
 3  <span class="p">SGHP</span>                   2026        ${t('Assistant Network & Security PM', 'Assistant chef de projet réseaux & sécurité')}
 4  <span class="p">${t('Independent', 'Indépendant')}</span>            2026–${t('now', 'auj.')}    ${t('Network & Security Engineer', 'Ingénieur réseaux & sécurité')}
 5  * * *  <span class="k">${t('(that could be you, try "contact")', '(ce pourrait être vous, tapez "contact")')}</span>`),
    projects: () => print(SITE.projects.map(p => `<span class="p">${p[0].padEnd(18)}</span>${esc(name(p))}`).join('\n') + `\n<span class="k">${t('→ open <id>', '→ open <id>')}</span>`),
    open: a => {
      const q = (a[0] || '').toLowerCase(); const p = SITE.projects.find(x => x[0].startsWith(q) && q);
      p ? nav2(url('projects/' + p[0] + '.html')) : print(t('open: unknown project. Try "projects".', 'open : projet inconnu. Tapez "projects".'), 'r');
    },
    labs: () => print(SITE.labs.map((l, i) => `Gi0/${String(i + 1).padEnd(3)} <span class="p">${l[0].padEnd(21)}</span>${esc(name(l))}`).join('\n') + `\n<span class="k">→ lab &lt;id&gt;</span>`),
    lab: a => {
      const q = (a[0] || '').toLowerCase(); const l = SITE.labs.find(x => x[0].startsWith(q) && q);
      l ? nav2(url('labs/' + l[0] + '.html')) : print(t('lab: unknown lab. Try "labs".', 'lab : lab inconnu. Tapez "labs".'), 'r');
    },
    cv: a => {
      const x = (a[0] || LANG).toLowerCase();
      if (x === 'web') return nav2(url('cv.html'));
      const f = BASE + (x === 'fr' ? 'assets/CV_Tarek_MEDJOUB.pdf' : 'assets/CV_Tarek_MEDJOUB_EN.pdf');
      print(`${t('downloading', 'téléchargement')} <a href="${f}" download>${f.split('/').pop()}</a> …`, 'g');
      const dl = document.createElement('a'); dl.href = f; dl.download = ''; document.body.appendChild(dl); dl.click(); dl.remove();
    },
    contact: () => print(
`email     <a href="mailto:tarek.medjoub@outlook.fr">tarek.medjoub@outlook.fr</a>
linkedin  <a href="https://linkedin.com/in/tarek-medjoub" target="_blank" rel="noopener">linkedin.com/in/tarek-medjoub</a>
${t('location', 'lieu    ')}  Paris, France`),
    ping: a => {
      const host = esc(a[0] || 'tarek');
      print(`PING ${host} (paris.fr): 56 data bytes`);
      let i = 0; const iv = setInterval(() => {
        print(`64 bytes from ${host}: icmp_seq=${i} ttl=64 time=${(8 + Math.random() * 4).toFixed(1)} ms`);
        if (++i === 3) { clearInterval(iv); print(`--- ${host} ping statistics ---\n3 packets transmitted, 3 received, <span class="g">0% packet loss</span>\nstatus: <span class="g">${t('available for new opportunities', 'disponible pour de nouvelles opportunités')}</span>`); }
      }, 350);
    },
    goto: a => {
      const m = { about: 'about', services: 'services', skills: 'stack', stack: 'stack', experience: 'experience', projects: 'projects', labs: 'labs', certs: 'certs', cv: 'resume', resume: 'resume', contact: 'contact', top: 'top' };
      const id = m[(a[0] || '').toLowerCase()];
      id ? section(id) : print(`goto: ${Object.keys(m).join(', ')}`, 'r');
    },
    theme: () => { setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'); print('theme → ' + root.dataset.theme, 'g'); },
    fr: () => { const a = $('[data-lang="fr"]'); a && nav2(a.getAttribute('href')); },
    en: () => { const a = $('[data-lang="en"]'); a && nav2(a.getAttribute('href')); },
    home: () => nav2(url('index.html')),
    tools: () => nav2(url('tools.html')),
    subnet: () => nav2(url('tools.html#subnet')),
    clear: () => { out.innerHTML = ''; },
    exit: () => close(),
    sudo: () => print(t('Permission denied 😉. Hire me and we can talk about privileges.', 'Permission refusée 😉. Recrutez-moi et on parlera de privilèges.'), 'r'),
    show: a => {
      const m = { version: 'whoami', ip: 'skills', interfaces: 'labs', running: 'whoami' };
      const c = m[(a[0] || '').toLowerCase()];
      c ? C[c]([]) : print(t('% Incomplete command. Try "show version", "show ip route", "show interfaces".', '% Commande incomplète. Essayez "show version", "show ip route", "show interfaces".'), 'r');
    }
  };
  C.ls = C.help; C.quit = C.exit; C['?'] = C.help;
  const sugg = ['help', 'whoami', 'projects', 'labs', 'open sdwan', 'ping tarek', 'cv web', 'contact'];
  const sg = $('#conSug');
  sg.innerHTML = sugg.map(s => `<button type="button">${s}</button>`).join('');
  sg.addEventListener('click', e => { if (e.target.tagName === 'BUTTON') run(e.target.textContent); });
  function run(raw) {
    const line = raw.trim(); if (!line) return;
    hist.push(line); hi = hist.length;
    print(`<span class="p">guest@portfolio:~$</span> ${esc(line)}`);
    const [cmd, ...args] = line.split(/\s+/);
    const fn = C[cmd.toLowerCase()];
    fn ? fn(args) : print(`${esc(cmd)}: ${t('command not found. Type', 'commande introuvable. Tapez')} <span class="p">help</span>`, 'r');
  }
  let opened = false;
  const open = () => {
    back.classList.add('open');
    if (!opened) { opened = true; print(`<span class="g">${t('Connected to', 'Connecté à')} tarek-medjoub</span> <span class="k">(SSH-2.0, AES-256)</span>\n${t('Type', 'Tapez')} <span class="p">help</span> ${t('to list commands.', 'pour la liste des commandes.')}`); }
    setTimeout(() => inp.focus(), 30);
  };
  function close() { back.classList.remove('open'); }
  $$('#fab, #conBtn').forEach(b => (b.onclick = open));
  $('#conClose') && ($('#conClose').onclick = close);
  back.addEventListener('click', e => { if (e.target === back) close(); });
  inp.addEventListener('keydown', e => {
    if (e.key === 'Enter') { run(inp.value); inp.value = ''; }
    else if (e.key === 'ArrowUp') { if (hi > 0) inp.value = hist[--hi]; e.preventDefault(); }
    else if (e.key === 'ArrowDown') { if (hi < hist.length - 1) inp.value = hist[++hi]; else { hi = hist.length; inp.value = ''; } e.preventDefault(); }
    else if (e.key === 'Tab') { e.preventDefault(); const m = Object.keys(C).filter(k => k.startsWith(inp.value.toLowerCase())); if (m.length === 1) inp.value = m[0] + ' '; }
  });
  document.addEventListener('keydown', e => {
    const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
    if (e.key === '`' && !typing) { e.preventDefault(); back.classList.contains('open') ? close() : open(); }
    if (e.key === 'Escape') close();
  });
})();
