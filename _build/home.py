"""Homepage, enterprise-vendor style: hero band, services tiles, expertise explorer,
featured work, live demo band, journey, resource center, credentials, CTA, contact."""
from common import L, layout, EMAIL, LINKEDIN, SITE
from labs_data import LABS
from projects_data import PROJECTS
from chrome import ico, EXPERTISE


def home(lang):
    x = L(lang); t = x.t
    root = "../" if lang == "fr" else ""
    cv_en = root + "assets/CV_Tarek_MEDJOUB_EN.pdf"
    cv_fr = root + "assets/CV_Tarek_MEDJOUB.pdf"
    cv_main = cv_fr if lang == "fr" else cv_en
    P = {p["id"]: p for p in PROJECTS}
    LB = {l["id"]: l for l in LABS}

    def chips(items, hl=()):
        return '<div class="chips">' + "".join(f'<span class="chip{" hl" if c in hl else ""}">{c}</span>' for c in items) + "</div>"

    # ───────── illustrations (inline SVG, theme-aware) ─────────
    ILL = {
        "audit": '<svg viewBox="0 0 320 160" aria-hidden="true"><rect x="40" y="26" width="150" height="108" rx="10" class="il-card"/><path d="M60 54h90M60 74h110M60 94h70M60 114h96" class="il-line"/><circle cx="222" cy="88" r="36" class="il-ring"/><path d="M248 114l26 26" class="il-strong"/><path d="M206 88l11 11 22-24" class="il-ok"/></svg>',
        "firewall": '<svg viewBox="0 0 320 160" aria-hidden="true"><path d="M160 22l62 22v42c0 34-26 52-62 60-36-8-62-26-62-60V44z" class="il-card"/><path d="M160 46l38 14v26c0 22-16 34-38 40" class="il-strong"/><path d="M30 80h50M240 80h50" class="il-line"/><circle cx="30" cy="80" r="6" class="il-dot"/><circle cx="290" cy="80" r="6" class="il-dot"/><path d="M84 72l10 8-10 8" class="il-x"/></svg>',
        "sdwan": '<svg viewBox="0 0 320 160" aria-hidden="true"><circle cx="160" cy="80" r="22" class="il-ring"/><g class="il-line"><path d="M60 34L142 70M60 126L142 90M260 34L178 70M260 126L178 90"/></g><g class="il-dash"><path d="M66 46L144 78M66 114L144 82M254 46L176 78M254 114L176 82"/></g><g class="il-card"><rect x="30" y="20" width="44" height="28" rx="6"/><rect x="30" y="112" width="44" height="28" rx="6"/><rect x="246" y="20" width="44" height="28" rx="6"/><rect x="246" y="112" width="44" height="28" rx="6"/></g><circle cx="104" cy="52" r="5" class="il-dot"/><circle cx="214" cy="106" r="5" class="il-dot"/></svg>',
        "cloud": '<svg viewBox="0 0 320 160" aria-hidden="true"><path d="M206 76a30 30 0 0 0-58-8 24 24 0 0 0-4 47h60a20 20 0 0 0 2-39z" class="il-card"/><rect x="40" y="96" width="70" height="40" rx="8" class="il-card"/><path d="M110 112C140 112 140 100 150 100" class="il-dash"/><path d="M58 112h34M58 122h22" class="il-line"/><path d="M230 50l40-22M230 110l40 22" class="il-line"/><circle cx="274" cy="26" r="9" class="il-ring"/><circle cx="274" cy="134" r="9" class="il-ring"/></svg>',
    }

    # ───────── 1. hero ─────────
    hero = f"""
<section class="hero-band" id="top">
  <canvas class="mesh" id="mesh" aria-hidden="true"></canvas>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">Tarek Medjoub · {t('Network, Security &amp; Cloud Engineer', 'Ingénieur Réseaux, Sécurité &amp; Cloud')}</span>
      <h1>{t('Networks built to <em>stay up</em>. <br>Secured. Monitored. Documented.', 'Des réseaux conçus pour <em>tenir</em>. <br>Sécurisés. Supervisés. Documentés.')}</h1>
      <p class="hero-lede">{t('I design, secure and run multisite enterprise networks, from Fortinet SD-WAN and IPsec/BGP to hybrid connectivity with Azure and AWS.',
                              'Je conçois, sécurise et exploite des réseaux d’entreprise multisites : SD-WAN Fortinet, IPsec/BGP et connectivité hybride vers Azure et AWS.')}</p>
      <div class="cta">
        <a class="btn primary lg" href="#work">{t('Explore my work', 'Découvrir mes réalisations')} {ico('arrow', 16)}</a>
        <a class="btn ghost lg" href="#contact">{t('Contact me', 'Me contacter')}</a>
      </div>
    </div>
    <div class="hero-feature">
      <span class="hf-label">{t('Highlights', 'À la une')}</span>
      <a class="hf-card" href="projects/sdwan.html"><span class="hf-type">{t('Case study', 'Étude de cas')}</span><b>{t('SD-WAN migration: failover from 3–5 min to ≈1.5 s', 'Migration SD-WAN : bascule de 3–5 min à ≈1,5 s')}</b><span class="hf-go">{ico('arrow', 16)}</span></a>
      <a class="hf-card" href="projects/hybrid-cloud.html"><span class="hf-type">{t('Case study', 'Étude de cas')}</span><b>{t('One FortiGate, two clouds: Azure + AWS over BGP', 'Un FortiGate, deux clouds : Azure + AWS en BGP')}</b><span class="hf-go">{ico('arrow', 16)}</span></a>
      <a class="hf-card" href="tools.html"><span class="hf-type">{t('Free tool', 'Outil gratuit')}</span><b>{t('Network toolkit: subnet, IPv6, VLSM, IPsec MSS', 'Outils réseau : sous-réseau, IPv6, VLSM, MSS IPsec')}</b><span class="hf-go">{ico('arrow', 16)}</span></a>
    </div>
  </div>
  <div class="wrap">
    <div class="hero-stats">
      <div><b data-count="4">4</b><span>{t('sites migrated to SD-WAN', 'sites migrés en SD-WAN')}</span></div>
      <div><b data-count="1.5" data-pre="≈" data-suf=" s" data-dec="1">{t('≈1.5 s', '≈1,5 s')}</b><span>{t('failover in lab (was 3–5 min)', 'bascule en lab (contre 3–5 min)')}</span></div>
      <div><b data-count="6">6</b><span>{t('engineers &amp; technicians led', 'ingénieurs &amp; techniciens encadrés')}</span></div>
      <div><b data-count="2">2</b><span>{t('clouds connected: Azure + AWS', 'clouds connectés : Azure + AWS')}</span></div>
      <div><b data-count="10">10</b><span>{t('EVE-NG lab guides', 'guides de lab EVE-NG')}</span></div>
    </div>
  </div>
</section>"""


    # ───────── sticky section nav + technology strip ─────────
    subnav = f"""
<nav class="subnav" aria-label="{t('Page sections', 'Sections de la page')}">
  <div class="wrap">
    <div class="subnav-links">
      <a href="#services">{t('Services', 'Services')}</a><a href="#expertise">{t('Expertise', 'Expertise')}</a><a href="#work">{t('Work', 'Réalisations')}</a><a href="#demo">{t('Live demo', 'Démo')}</a><a href="#about">{t('About', 'À propos')}</a><a href="#resources">{t('Resources', 'Ressources')}</a><a href="#certs">{t('Credentials', 'Certifications')}</a>
    </div>
  </div>
  <span class="subnav-prog" aria-hidden="true"></span>
</nav>"""
    TECH = ["Fortinet FortiGate", "FortiManager", "FortiAnalyzer", "Fortinet SD-WAN", "Cisco IOS / IOS-XE", "Huawei", "Ubiquiti", "Microsoft Azure", "AWS", "Aviatrix",
            "Zabbix", "PRTG", "GLPI", "ManageEngine OpManager", "EVE-NG", "Ansible", "Windows Server", "Linux", "Wireshark"]
    row = "".join(f"<li>{x}</li>" for x in TECH)
    marquee = f"""
<section class="tech-strip" aria-label="{t('Technologies I work with', 'Technologies utilisées')}">
  <div class="wrap tech-inner">
    <span class="tech-h">{t('Technologies I work with', 'Technologies que j’utilise')}</span>
    <div class="marquee"><ul class="mq-track">{row}</ul><ul class="mq-track" aria-hidden="true">{row}</ul></div>
  </div>
</section>"""

    # ───────── 2. services tiles ─────────
    svc = [("audit", "routing", t('Network &amp; security audit', 'Audit réseau &amp; sécurité'),
            t('Switching, routing and firewall configurations reviewed against best practice, with prioritised findings.', 'Revue des configurations de commutation, routage et pare-feu face aux bonnes pratiques, avec constats priorisés.')),
           ("firewall", "security", t('Firewall policy review', 'Revue des politiques de pare-feu'),
            t('FortiGate rule bases, zones and DMZ, IPS profiles and hardening. Tighter policy, less exposure.', 'Règles FortiGate, zones et DMZ, profils IPS et durcissement. Moins de règles larges, moins d’exposition.')),
           ("sdwan", "sdwan", t('VPN &amp; SD-WAN assessment', 'Évaluation VPN &amp; SD-WAN'),
            t('IPsec and SSL VPN architecture, SD-WAN SLA rules, path steering and dual-ISP failover design.', 'Architecture VPN IPsec et SSL, règles SLA SD-WAN, orientation du trafic et bascule double opérateur.')),
           ("cloud", "cloud", t('Cloud connectivity review', 'Revue de la connectivité cloud'),
            t('Site-to-cloud VPN to Azure and AWS, BGP route propagation, filtering and monitoring.', 'VPN site-à-cloud vers Azure et AWS, propagation BGP, filtrage et supervision.'))]
    tiles = "".join(f"""
      <a class="tile reveal" href="#expertise-{exp}">
        <div class="tile-art">{ILL[il]}</div>
        <div class="tile-body"><h3>{ti}</h3><p>{de}</p><span class="link-arrow">{t('Learn more', 'En savoir plus')} {ico('arrow', 15)}</span></div>
      </a>""" for il, exp, ti, de in svc)
    services = f"""
<section class="band" id="services">
  <div class="wrap">
    <div class="band-head reveal">
      <div><span class="kicker">{t('Services', 'Services')}</span><h2>{t('How I can help your infrastructure', 'Comment je peux aider votre infrastructure')}</h2></div>
      <p>{t('As an independent Network &amp; Security Engineer, I audit and strengthen existing networks. Every engagement ends with clear, usable documentation.', 'Ingénieur réseaux &amp; sécurité indépendant, j’audite et je renforce les réseaux existants. Chaque mission se termine par une documentation claire et exploitable.')}</p>
    </div>
    <div class="tiles">{tiles}
    </div>
    <ol class="process reveal" aria-label="{t('Working method', 'Méthode de travail')}">
      <li><b>01</b><span>{t('Discover', 'Découvrir')}</span></li><li><b>02</b><span>{t('Audit', 'Auditer')}</span></li><li><b>03</b><span>{t('Design', 'Concevoir')}</span></li><li><b>04</b><span>{t('Validate in EVE-NG', 'Valider sous EVE-NG')}</span></li><li><b>05</b><span>{t('Document &amp; hand over', 'Documenter &amp; transmettre')}</span></li>
    </ol>
  </div>
</section>"""

    # ───────── 3. expertise explorer ─────────
    EXP = {
        "routing": (t('Campus and multisite designs that scale, with redundancy at every layer: VLAN segmentation, OSPF and BGP, gateway high availability and loop protection.',
                      'Des architectures campus et multisites qui passent à l’échelle, redondantes à chaque couche : segmentation VLAN, OSPF et BGP, haute disponibilité des passerelles et protection contre les boucles.'),
                    ["VLAN 802.1Q", "STP / RSTP / MSTP", "EtherChannel / LACP", "OSPF", "BGP", "EIGRP", "PBR", "IPv6", "HSRP / VRRP", "BFD"], ["OSPF", "BGP", "VLAN 802.1Q"],
                    [("case", "lan-optimization"), ("lab", "bgp"), ("lab", "ospf"), ("lab", "switching-resilience"), ("tool", "subnet")]),
        "security": (t('Perimeter and internal security on FortiGate: zone-based policies, DMZ design, IPS and application control, least-privilege segmentation and device hardening.',
                       'Sécurité périmétrique et interne sur FortiGate : politiques par zone, conception DMZ, IPS et contrôle applicatif, segmentation au moindre privilège et durcissement.'),
                     [t('FortiGate firewalls', 'Pare-feu FortiGate'), t('DMZ &amp; zone policies', 'DMZ &amp; politiques par zone'), "IDS / IPS", t('App control', 'Contrôle applicatif'), "ACL", "DHCP snooping", "DAI", t('Hardening', 'Durcissement'), "FortiGate HA"],
                     [t('FortiGate firewalls', 'Pare-feu FortiGate'), "FortiGate HA"],
                     [("case", "sdwan"), ("lab", "fortigate-ha"), ("lab", "vlan"), ("tool", "wildcard")]),
        "sdwan": (t('WAN that reacts in seconds, not minutes: Fortinet SD-WAN with SLA probes, dual-ISP designs, encrypted IPsec overlays and dynamic routing in every tunnel.',
                    'Un WAN qui réagit en secondes, pas en minutes : SD-WAN Fortinet avec sondes SLA, double opérateur, overlays IPsec chiffrés et routage dynamique dans chaque tunnel.'),
                  ["Fortinet SD-WAN", t('SLA probes', 'Sondes SLA'), t('Dual-ISP design', 'Double opérateur'), "IPsec IKEv1/v2", "SSL VPN", "GRE over IPsec", t('BGP over IPsec', 'BGP sur IPsec'), "FortiManager", "FortiAnalyzer", "QoS"],
                  ["Fortinet SD-WAN", "IPsec IKEv1/v2"],
                  [("case", "sdwan"), ("lab", "sdwan-failover"), ("lab", "ipsec"), ("tool", "mss")]),
        "cloud": (t('On-premises networks extended into the cloud the way enterprises need it: route-based IPsec, BGP everywhere, strict prefix filtering and one monitoring view.',
                    'Des réseaux locaux étendus vers le cloud comme l’exigent les entreprises : IPsec route-based, BGP partout, filtrage strict des préfixes et une seule vue de supervision.'),
                  ["Azure VPN Gateway", "AWS Transit Gateway", "Aviatrix", t('BGP route filtering', 'Filtrage BGP'), t('MSS clamping', 'Ajustement du MSS'), t('Hybrid architecture', 'Architecture hybride')],
                  ["Azure VPN Gateway", "AWS Transit Gateway"],
                  [("case", "hybrid-cloud"), ("lab", "ipsec"), ("lab", "bgp"), ("tool", "ipv6")]),
        "ops": (t('Visibility and repeatability: SNMPv3 monitoring, alerts that open tickets automatically, and Ansible for backups and standard changes.',
                  'Visibilité et reproductibilité : supervision SNMPv3, alertes qui ouvrent des tickets automatiquement, et Ansible pour les sauvegardes et changements standard.'),
                ["Zabbix", "PRTG", "ManageEngine OpManager", "GLPI", "SNMPv3", "Ansible", "Bash", "Windows Server", "Linux", "EVE-NG"],
                ["Zabbix", "PRTG", "GLPI"],
                [("case", "monitoring-stack"), ("lab", "snmp-zabbix"), ("lab", "ansible-network"), ("tool", "vlsm")]),
    }
    TOOLN = {"subnet": t('IPv4 subnet calculator', 'Calcul de sous-réseau IPv4'), "ipv6": t('IPv6 calculator', 'Calcul IPv6'), "vlsm": t('VLSM planner', 'Planificateur VLSM'),
             "wildcard": t('Wildcard &amp; ACL helper', 'Assistant wildcard &amp; ACL'), "mss": "IPsec MTU / MSS"}

    def rel_link(kind, key):
        if kind == "case": return f'<a href="projects/{key}.html"><span class="rl-type">{t("Case study", "Étude de cas")}</span>{t(*P[key]["title"])}{ico("arrow", 14)}</a>'
        if kind == "lab": return f'<a href="labs/{key}.html"><span class="rl-type">{t("Lab", "Lab")}</span>{t(*LB[key]["title"])}{ico("arrow", 14)}</a>'
        return f'<a href="tools.html#{key}"><span class="rl-type">{t("Tool", "Outil")}</span>{TOOLN[key]}{ico("arrow", 14)}</a>'

    tabs = "".join(f'<button type="button" role="tab" id="xt-{k}" aria-controls="expertise-{k}" class="xt{" on" if i == 0 else ""}" aria-selected="{"true" if i == 0 else "false"}"><span class="xt-ico">{ico(k)}</span><span><b>{t(*n)}</b><small>{t(*d)}</small></span></button>'
                   for i, (k, n, d) in enumerate(EXPERTISE))
    panels = "".join(f"""
        <div class="xp" role="tabpanel" id="expertise-{k}" aria-labelledby="xt-{k}"{'' if i == 0 else ' hidden'}>
          <span class="xp-ico">{ico(k, 26)}</span>
          <h3>{t(*n)}</h3>
          <p>{EXP[k][0]}</p>
          {chips(EXP[k][1], EXP[k][2])}
          <div class="xp-rel"><span class="xp-rel-h">{t('Explore related work', 'Explorer les contenus liés')}</span>{''.join(rel_link(a, b) for a, b in EXP[k][3])}</div>
        </div>""" for i, (k, n, d) in enumerate(EXPERTISE))
    expertise = f"""
<section class="band alt" id="expertise">
  <div class="wrap">
    <div class="band-head reveal">
      <div><span class="kicker">{t('Expertise', 'Expertise')}</span><h2>{t('Five domains, one end-to-end view of the network', 'Cinq domaines, une vision de bout en bout du réseau')}</h2></div>
      <p>{t('Pick a domain to see what I do there, the technologies I use and where to see it in practice.', 'Choisissez un domaine pour voir ce que j’y fais, les technologies utilisées et où les voir en pratique.')}</p>
    </div>
    <div class="explorer reveal">
      <div class="xt-list" role="tablist" aria-label="{t('Expertise domains', 'Domaines d’expertise')}">{tabs}</div>
      <div class="xp-wrap">{panels}
      </div>
    </div>
  </div>
</section>"""

    # ───────── 4. featured work ─────────
    arts = {
        "sdwan": ILL["sdwan"], "hybrid-cloud": ILL["cloud"],
        "lan-optimization": '<svg viewBox="0 0 320 160" aria-hidden="true"><g class="il-line"><path d="M160 34L96 80M160 34L224 80M96 80L60 126M96 80L132 126M224 80L188 126M224 80L260 126"/></g><g class="il-card"><rect x="134" y="20" width="52" height="26" rx="6"/><rect x="72" y="68" width="48" height="24" rx="6"/><rect x="200" y="68" width="48" height="24" rx="6"/><rect x="42" y="118" width="36" height="20" rx="5"/><rect x="114" y="118" width="36" height="20" rx="5"/><rect x="170" y="118" width="36" height="20" rx="5"/><rect x="242" y="118" width="36" height="20" rx="5"/></g><path d="M134 33h52" class="il-strong"/></svg>',
        "monitoring-stack": '<svg viewBox="0 0 320 160" aria-hidden="true"><rect x="30" y="24" width="260" height="112" rx="10" class="il-card"/><path d="M50 52h220" class="il-dash"/><polyline points="50,116 82,104 106,108 130,86 156,94 182,64 206,76 232,46 252,98 270,92" class="il-strong" fill="none"/><circle cx="232" cy="46" r="6" class="il-alert"/></svg>',
    }
    big = ""
    for i, pid in enumerate(["sdwan", "hybrid-cloud"]):
        p = P[pid]
        facts = "".join(f"<div><b>{a}</b><span>{t(*b)}</span></div>" for a, b in p["facts"])
        big += f"""
    <article class="split{' rev' if i else ''} reveal">
      <div class="split-art">{arts[pid]}</div>
      <div class="split-copy">
        <span class="kicker">{t('Case study', 'Étude de cas')} · {p['tagline']}</span>
        <h3>{t(*p['title'])}</h3>
        <p>{t(*p['card'])}</p>
        <div class="split-facts">{facts}</div>
        <a class="btn primary" href="projects/{pid}.html">{t('Read the case study', 'Lire l’étude de cas')} {ico('arrow', 15)}</a>
      </div>
    </article>"""
    small = "".join(f"""
      <a class="card-x reveal" href="projects/{pid}.html">
        <div class="cx-art">{arts[pid]}</div>
        <span class="kicker">{t('Case study', 'Étude de cas')}</span>
        <h3>{t(*P[pid]['title'])}</h3><p>{t(*P[pid]['card'])}</p>
        <span class="link-arrow">{t('Read more', 'Lire la suite')} {ico('arrow', 15)}</span>
      </a>""" for pid in ["lan-optimization", "monitoring-stack"])
    work = f"""
<section class="band" id="work">
  <div class="wrap">
    <div class="band-head reveal">
      <div><span class="kicker">{t('Featured work', 'Réalisations')}</span><h2>{t('Real migrations, validated designs', 'Des migrations réelles, des architectures validées')}</h2></div>
      <p>{t('Each project has a full case study: context, architecture, configuration, validation and lessons learned.', 'Chaque projet a son étude de cas complète : contexte, architecture, configuration, validation et retours d’expérience.')}</p>
    </div>
    {big}
    <div class="cx-grid">{small}
    </div>
  </div>
</section>"""

    # ───────── 5. live demo band ─────────
    demo = f"""
<section class="demo-band" id="demo">
  <div class="wrap demo-grid">
    <div class="demo-copy reveal">
      <span class="kicker">{t('Live demo', 'Démo interactive')}</span>
      <h2>{t('See SD-WAN failover in action', 'Voyez une bascule SD-WAN en direct')}</h2>
      <p>{t('Three branches with two ISPs each, an HQ hub and IPsec/BGP tunnels to Azure and AWS. Cut a link and watch traffic move to the backup path while the SLA graph reacts.',
            'Trois agences avec deux FAI chacune, un hub au siège et des tunnels IPsec/BGP vers Azure et AWS. Coupez un lien : le trafic bascule sur le chemin de secours et le graphe SLA réagit.')}</p>
      <ul class="ticks">
        <li>{t('Click any link to cut or restore it', 'Cliquez un lien pour le couper ou le rétablir')}</li>
        <li>{t('“Fail ISP-1” simulates an outage on every site', '« Couper ISP-1 » simule une panne sur toutes les agences')}</li>
        <li>{t('Based on the SD-WAN case study design', 'Basé sur l’architecture de l’étude de cas SD-WAN')}</li>
      </ul>
      <a class="link-arrow light" href="projects/sdwan.html">{t('How it was built', 'Comment c’est construit')} {ico('arrow', 15)}</a>
    </div>
    <figure class="topo reveal" aria-label="{t('Interactive SD-WAN and hybrid cloud topology simulation', 'Simulation interactive SD-WAN et cloud hybride')}">
      <div class="topo-head"><span class="t">{t('SD-WAN overlay · hub-and-spoke + hybrid cloud', 'Overlay SD-WAN · étoile + cloud hybride')}</span><span class="live"><span class="led"></span><span id="liveTxt">…</span></span></div>
      <svg id="topo" viewBox="0 0 530 400" role="img" aria-label="{t('Three branch sites with two ISP links each to an HQ hub, which connects to Azure and AWS over IPsec with BGP', 'Trois agences avec deux liens FAI chacune vers un hub HQ, relié à Azure et AWS en IPsec avec BGP')}"><g id="links"></g><g id="pkts"></g><g id="nodes"></g></svg>
      <div class="legend"><span><i style="--c:var(--green)"></i>{t('ISP-1 primary', 'ISP-1 principal')}</span><span><i class="d" style="--c:var(--green)"></i>{t('ISP-2 backup', 'ISP-2 secours')}</span><span><i class="d" style="--c:var(--violet)"></i>IPsec + BGP</span><span><i style="--c:var(--red)"></i>{t('down', 'coupé')}</span></div>
      <div class="sla"><div class="sla-head"><span>{t('SLA probe latency', 'Latence des sondes SLA')} · <select id="slaSite" aria-label="{t('Site', 'Agence')}"><option value="A">SITE-A</option><option value="B">SITE-B</option><option value="C">SITE-C</option></select></span><span class="vals"><span style="color:var(--green)">ISP-1 <b id="slaV1">—</b></span><span style="color:var(--violet)">ISP-2 <b id="slaV2">—</b></span><span style="color:var(--red)">{t('threshold 100 ms', 'seuil 100 ms')}</span></span></div><svg id="slaSvg" viewBox="0 0 400 58" preserveAspectRatio="none" aria-hidden="true"></svg></div>
      <div class="topo-ctl"><button class="warn" id="failIsp1">{t('Fail ISP-1 on all sites', 'Couper ISP-1 partout')}</button><button id="restore">{t('Restore', 'Rétablir')}</button></div>
      <div class="log" id="log" aria-live="polite"></div>
    </figure>
  </div>
</section>"""

    # ───────── 6. about + journey ─────────
    jobs = [
        ("2023", t('Network Engineer Intern', 'Stagiaire ingénieur réseau'), "3K Solutions · " + t('Algeria', 'Algérie'),
         t('Cisco configuration: IP addressing, VLANs, static routing, connectivity testing.', 'Configuration Cisco : adressage IP, VLAN, routage statique, tests de connectivité.'), False),
        ("2023–2025", t('Team Leader &amp; Network Security Project Lead', 'Chef d’équipe &amp; chef de projet sécurité réseau'), "Condor Electronics · " + t('Algeria', 'Algérie'),
         t('Led 4 technicians and 2 engineers on a multisite industrial network; migrated intersite links to Fortinet SD-WAN with Ubiquiti backup; audited VLAN, ACL and OSPF; handled Zabbix/PRTG alerts and GLPI tickets.',
           'Encadrement de 4 techniciens et 2 ingénieurs sur un réseau industriel multisite ; migration vers le SD-WAN Fortinet avec secours Ubiquiti ; audit VLAN, ACL et OSPF ; alertes Zabbix/PRTG et tickets GLPI.'), False),
        ("2026", t('Assistant Network &amp; Security Project Manager', 'Assistant chef de projet réseaux &amp; sécurité'), "SGHP · France",
         t('Supported a migration from on-premises infrastructure to the cloud.', 'Accompagnement d’une migration d’infrastructure locale vers le cloud.'), False),
        (t('2026 – now', '2026 – auj.'), t('Network &amp; Security Engineer', 'Ingénieur réseaux &amp; sécurité'), t('Independent · France', 'Indépendant · France'),
         t('Audits of network and security configurations, firewall and VPN reviews, SD-WAN and cloud connectivity assessments, with documentation.', 'Audits de configurations réseau et sécurité, revues pare-feu et VPN, évaluations SD-WAN et cloud, avec documentation.'), True),
    ]
    journey = "".join(f"""
      <li class="jr{' now' if now else ''} reveal"><span class="jr-year">{y}</span><div class="jr-card"><h3>{ti}</h3><span class="jr-org">{org}</span><p>{de}</p>{'<span class="pill-now">' + t('current', 'actuel') + '</span>' if now else ''}</div></li>""" for y, ti, org, de, now in jobs)
    about = f"""
<section class="band" id="about">
  <div class="wrap about-v">
    <div class="reveal">
      <span class="kicker">{t('About', 'À propos')}</span>
      <h2>{t('From network operations to project delivery', 'De l’exploitation réseau au pilotage de projets')}</h2>
      <p class="lead">{t('My core is Cisco routing &amp; switching and Fortinet security across multisite networks. At Condor Electronics I became a team leader and moved intersite connectivity to Fortinet SD-WAN. Today I extend on-prem networks into Azure and AWS, and an MBA in project management completes the picture.',
                         'Mon socle : routage &amp; commutation Cisco et sécurité Fortinet sur des réseaux multisites. Chez Condor Electronics, je suis devenu chef d’équipe et j’ai migré l’interconnexion vers le SD-WAN Fortinet. Aujourd’hui, j’étends les réseaux locaux vers Azure et AWS, et un MBA en management de projet complète le profil.')}</p>
      <blockquote>{t('I don’t just make it work. I make it resilient, documented and observable.', 'Faire fonctionner ne suffit pas : je rends les réseaux résilients, documentés et observables.')}</blockquote>
      <dl class="glance-row">
        <div><dt>{t('Based in', 'Basé à')}</dt><dd>Paris, France</dd></div>
        <div><dt>{t('Languages', 'Langues')}</dt><dd>{t('French · English', 'Français · Anglais')}</dd></div>
        <div><dt>{t('Looking for', 'Recherche')}</dt><dd>{t('Network, Security or Cloud role', 'Poste Réseaux, Sécurité ou Cloud')}</dd></div>
      </dl>
    </div>
    <div id="experience">
      <span class="kicker">{t('Experience', 'Expérience')}</span>
      <ol class="journey">{journey}
      </ol>
    </div>
  </div>
</section>"""

    # ───────── 7. resource center ─────────
    res = []
    for p in PROJECTS:
        res.append(("case", t('Case study', 'Étude de cas'), t(*p['title']), t(*p['card']), f"projects/{p['id']}.html", p['tagline']))
    for i, l in enumerate(LABS):
        res.append(("lab", t('Lab guide', 'Guide de lab') + f" {i + 1:02d}", t(*l['title']), t(*l['focus']), f"labs/{l['id']}.html", f"{t(*l['level'])} · {l['time']}"))
    for k, n in TOOLN.items():
        res.append(("tool", t('Tool', 'Outil'), n, t('Free, runs in your browser, no data sent.', 'Gratuit, dans votre navigateur, aucune donnée envoyée.'), f"tools.html#{k}", t('Network toolkit', 'Outils réseau')))
    cards = "".join(f"""
      <a class="res {k}" data-k="{k}" href="{h}"><span class="res-top"><span class="res-ico">{ico({'case': 'case', 'lab': 'lab', 'tool': 'tool'}[k])}</span><span class="res-type">{ty}</span></span><b>{ti}</b><span class="res-desc">{de}</span><span class="res-meta">{me}</span></a>"""
                    for k, ty, ti, de, h, me in res)
    resources = f"""
<section class="band alt" id="resources">
  <div class="wrap">
    <div class="band-head reveal">
      <div><span class="kicker">{t('Resource center', 'Centre de ressources')}</span><h2>{t('Guides, case studies and tools', 'Guides, études de cas et outils')}</h2></div>
      <p>{t('Everything I publish, in one place. Lab guides cover topology, configs, verification and break/fix exercises.', 'Tout ce que je publie, au même endroit. Les guides de lab couvrent topologie, configurations, vérifications et exercices de panne.')}</p>
    </div>
    <div class="res-filter reveal" role="group" aria-label="{t('Filter resources', 'Filtrer les ressources')}">
      <button type="button" class="on" data-f="all">{t('All', 'Tout')} <i>{len(res)}</i></button>
      <button type="button" data-f="case">{t('Case studies', 'Études de cas')} <i>{len(PROJECTS)}</i></button>
      <button type="button" data-f="lab">{t('Lab guides', 'Guides de lab')} <i>{len(LABS)}</i></button>
      <button type="button" data-f="tool">{t('Tools', 'Outils')} <i>{len(TOOLN)}</i></button>
    </div>
    <div class="res-grid" id="resGrid">{cards}
    </div>
    <div class="res-more"><button type="button" class="btn" id="resMore">{t('Show all resources', 'Afficher toutes les ressources')}</button></div>
  </div>
</section>"""

    # ───────── 8. credentials ─────────
    creds = f"""
<section class="band" id="certs">
  <div class="wrap">
    <div class="band-head reveal">
      <div><span class="kicker">{t('Credentials', 'Certifications &amp; formation')}</span><h2>{t('A technical foundation. A project mindset.', 'Un socle technique. Un esprit projet.')}</h2></div>
      <p>{t('Vendor certifications and academy training, a Master’s in networks and an MBA in project management.', 'Certifications constructeur et formations, un Master réseaux et un MBA en management de projet.')}</p>
    </div>
    <div class="cred-grid reveal">
      <div class="cred"><span class="cred-v" style="--c:#6d28d9">Aviatrix</span><b>Multicloud Network Associate</b><small>{t('Certification', 'Certification')}</small></div>
      <div class="cred"><span class="cred-v" style="--c:#c7000b">Huawei</span><b>HCIA Cloud Computing</b><small>{t('Certification', 'Certification')}</small></div>
      <div class="cred"><span class="cred-v" style="--c:#c7000b">Huawei</span><b>HCIA Routing &amp; Switching</b><small>{t('Certification', 'Certification')}</small></div>
      <div class="cred"><span class="cred-v" style="--c:#0a7ea4">Cisco NetAcad</span><b>CCNP: Core Networking</b><small>{t('Academy training', 'Formation académique')}</small></div>
      <div class="cred"><span class="cred-v" style="--c:#0a7ea4">Cisco NetAcad</span><b>CCNA: SRWE</b><small>{t('Academy training', 'Formation académique')}</small></div>
      <div class="cred"><span class="cred-v" style="--c:#0a7ea4">Cisco NetAcad</span><b>Network Defense · Network Security</b><small>{t('Academy training', 'Formation académique')}</small></div>
    </div>
    <div class="edu-row reveal">
      <div class="edu"><span>2024 – 2026</span><b>{t('MBA, Management &amp; Project Management', 'MBA Management &amp; Gestion de projet')}</b></div>
      <div class="edu"><span>2021 – 2023</span><b>{t('Master’s in Networks &amp; Telecommunications', 'Master Réseaux &amp; Télécommunications')}</b><small>{t('ENIC-NARIC France: comparable to level 7', 'ENIC-NARIC France : comparable au niveau 7')}</small></div>
      <div class="edu next"><span>{t('Next step', 'Prochaine étape')}</span><b>{t('Fortinet FCP · Cisco CCNA exams', 'Examens Fortinet FCP · Cisco CCNA')}</b></div>
    </div>
  </div>
</section>"""

    # ───────── 9. CTA band + contact ─────────
    cta = f"""
<section class="cta-band">
  <div class="wrap cta-inner reveal">
    <div><h2>{t('Let’s build a network that stays up.', 'Construisons un réseau qui tient.')}</h2><p>{t('Hiring, planning an audit or migrating to SD-WAN or the cloud? Let’s talk.', 'Un recrutement, un audit ou une migration SD-WAN ou cloud ? Parlons-en.')}</p></div>
    <div class="cta"><a class="btn white lg" href="#contact">{t('Contact me', 'Me contacter')}</a><a class="btn ghost lg" href="{cv_main}" download>{t('Download CV', 'Télécharger le CV')}</a><a class="btn ghost lg" href="cv.html">{t('Web CV', 'CV web')}</a></div>
  </div>
</section>"""
    contact = f"""
<section class="band" id="contact">
  <div class="wrap contact">
    <div class="reveal">
      <span class="kicker">Contact</span>
      <h2>{t('Let’s talk infrastructure', 'Parlons infrastructure')}</h2>
      <p class="lead">{t('A role, an audit or a network that needs fixing? I usually reply within one business day.', 'Un poste, un audit ou un réseau à remettre d’aplomb ? Je réponds généralement sous un jour ouvré.')}</p>
      <div class="clinks">
        <a class="clink" href="mailto:{EMAIL}"><span class="ico">{ico('mail')}</span><div><small>EMAIL</small><span>{EMAIL}</span></div><button class="copy" type="button" data-copy="{EMAIL}">{t('copy', 'copier')}</button></a>
        <a class="clink" href="{LINKEDIN}" target="_blank" rel="noopener"><span class="ico"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.78-1.7-2.78-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg></span><div><small>LINKEDIN</small><span>in/tarek-medjoub</span></div></a>
        <div class="clink" style="cursor:default"><span class="ico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span><div><small>{t('LOCATION', 'LOCALISATION')}</small><span>Paris, France</span></div></div>
      </div>
    </div>
    <div class="form-card reveal">
      <h3>{t('Send a message', 'Envoyer un message')}</h3>
      <form class="cf" id="cf">
        <div class="grid2">
          <div><label for="cfName">{t('Name', 'Nom')} <span class="req" aria-hidden="true">*</span></label><input id="cfName" required autocomplete="name"></div>
          <div><label for="cfEmail">Email <span class="req" aria-hidden="true">*</span></label><input id="cfEmail" type="email" required autocomplete="email" placeholder="{t('you@company.com', 'vous@entreprise.fr')}" aria-describedby="cfEmailErr"><span class="ferr" id="cfEmailErr" role="alert"></span></div>
        </div>
        <div class="grid2">
          <div><label for="cfOrg">{t('Company', 'Entreprise')}</label><input id="cfOrg" autocomplete="organization"></div>
          <div><label for="cfTopic">{t('Topic', 'Sujet')}</label><select id="cfTopic"><option>{t('Job opportunity', 'Opportunité de poste')}</option><option>{t('Network / security audit', 'Audit réseau / sécurité')}</option><option>{t('SD-WAN or VPN project', 'Projet SD-WAN ou VPN')}</option><option>{t('Cloud connectivity', 'Connectivité cloud')}</option><option>{t('Something else', 'Autre')}</option></select></div>
        </div>
        <div><label for="cfMsg">Message <span class="req" aria-hidden="true">*</span></label><textarea id="cfMsg" required></textarea></div>
        <button class="btn primary" type="submit" style="justify-self:start">{t('Send message', 'Envoyer le message')} {ico('arrow', 15)}</button>
        <span class="cf-hint">{t('* required. Opens your email client with the message pre-filled, including your address so I can reply.', '* obligatoire. Ouvre votre messagerie avec le message pré-rempli, votre adresse comprise pour que je puisse répondre.')}</span>
      </form>
    </div>
  </div>
</section>"""

    body = hero + subnav + marquee + services + expertise + work + demo + about + resources + creds + cta + contact
    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Tarek Medjoub","jobTitle":"%s",
"email":"mailto:%s","url":"%s","address":{"@type":"PostalAddress","addressLocality":"Paris","addressCountry":"FR"},
"sameAs":["%s"],"knowsLanguage":["fr","en"],
"knowsAbout":["Fortinet SD-WAN","FortiGate","BGP","OSPF","IPsec VPN","Azure VPN Gateway","AWS Transit Gateway","Zabbix","PRTG","Network security"]}
</script>""" % (t("Network, Security & Cloud Engineer", "Ingénieur Réseaux, Sécurité & Cloud"), EMAIL, SITE, LINKEDIN)
    return layout(
        lang, "index.html",
        t("Tarek MEDJOUB · Network, Security & Cloud Engineer", "Tarek MEDJOUB · Ingénieur Réseaux, Sécurité & Cloud"),
        t("Network, Security & Cloud Engineer in Paris. Fortinet SD-WAN, multisite networks, IPsec/BGP and hybrid connectivity to Azure and AWS.",
          "Ingénieur Réseaux, Sécurité & Cloud à Paris. SD-WAN Fortinet, réseaux multisites, IPsec/BGP et connectivité hybride vers Azure et AWS."),
        body, home=True, jsonld=jsonld,
        extra_js=f'<script src="{root}assets/js/topology.js" defer></script><script src="{root}assets/js/home.js" defer></script>')
