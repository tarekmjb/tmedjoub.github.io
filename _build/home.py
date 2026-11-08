from common import L, layout, EMAIL, LINKEDIN, SITE
from labs_data import LABS
from projects_data import PROJECTS


def home(lang):
    x = L(lang); t = x.t
    lp = "fr/" if lang == "fr" else ""
    root = "../" if lang == "fr" else ""
    cv_en = root + "assets/CV_Tarek_MEDJOUB_EN.pdf"
    cv_fr = root + "assets/CV_Tarek_MEDJOUB.pdf"
    cv_main = cv_fr if lang == "fr" else cv_en

    def chips(s, hl=()):
        return '<div class="chips">' + "".join(
            f'<span class="chip{" hl" if c in hl else ""}">{c}</span>' for c in s) + "</div>"

    # skills routing table
    skills = [
        ("C", t("Switching", "Commutation"), t("L2 · campus", "L2 · campus"),
         ["VLAN 802.1Q", "STP / RSTP / MSTP", "EtherChannel / LACP", t("Port security", "Sécurité des ports"), "DHCP snooping", "DAI", "CDP / LLDP"], ["VLAN 802.1Q"]),
        ("C", t("Routing", "Routage"), "L3 · IGP / EGP",
         ["OSPF", "BGP", "EIGRP", t("Redistribution", "Redistribution"), "PBR", "IPv6 / OSPFv3"], ["OSPF", "BGP"]),
        ("W", "WAN / SD-WAN", t("multisite", "multisite"),
         ["Fortinet SD-WAN", t("Dual-ISP design", "Double opérateur"), t("SLA probes", "Sondes SLA"), "QoS", t("MPLS concepts", "Principes MPLS"), "FortiManager", "FortiAnalyzer"], ["Fortinet SD-WAN", t("Dual-ISP design", "Double opérateur")]),
        ("V", "VPN", t("site-to-site · remote", "site à site · nomade"),
         ["IPsec IKEv1/v2", "Hub-and-spoke", "SSL VPN", "GRE over IPsec", t("BGP over IPsec", "BGP sur IPsec"), t("Site-to-cloud VPN", "VPN site-à-cloud")], ["IPsec IKEv1/v2", t("BGP over IPsec", "BGP sur IPsec")]),
        ("S", t("Security", "Sécurité"), t("perimeter · segmentation", "périmètre · segmentation"),
         [t("FortiGate firewalls", "Pare-feu FortiGate"), t("DMZ & zone policies", "DMZ & politiques par zone"), "ACL", "IDS / IPS", t("App control", "Contrôle applicatif"), t("Segmentation", "Segmentation"), t("Hardening", "Durcissement")], [t("FortiGate firewalls", "Pare-feu FortiGate")]),
        ("H", t("High availability", "Haute disponibilité"), t("resilience", "résilience"),
         ["HSRP / VRRP", "FortiGate HA", t("Dual-ISP failover", "Bascule double FAI"), "BFD"], ["FortiGate HA"]),
        ("K", "Cloud", t("hybrid", "hybride"),
         ["Azure VPN Gateway", "AWS Transit Gateway", "Aviatrix", t("Hybrid architecture", "Architecture hybride"), t("PRTG cloud monitoring", "Supervision cloud PRTG")], ["Azure VPN Gateway", "AWS Transit Gateway"]),
        ("M", t("Monitoring & ITSM", "Supervision & ITSM"), t("visibility", "visibilité"),
         ["Zabbix", "PRTG", "ManageEngine OpManager", "GLPI", "SNMPv3", t("Alerting design", "Conception des alertes")], ["Zabbix", "PRTG"]),
        ("N", t("Network services", "Services réseau"), t("design · docs", "conception · docs"),
         ["DHCP", "DNS", "NTP", t("3-tier design", "Architecture 3 couches"), t("IP addressing plans", "Plans d’adressage"), "Documentation"], []),
        ("O", t("Systems", "Systèmes"), t("& delivery", "& pilotage"),
         ["Windows Server (AD, DNS, DHCP, GPO)", "Linux", "Bash", "Ansible", "EVE-NG", t("IT project management", "Gestion de projet IT")], []),
    ]
    rrows = "".join(
        f'<div class="rrow"><span class="code">{c}</span><span class="dom">{d}<small>{s}</small></span>{chips(items, hl)}</div>'
        for c, d, s, items, hl in skills)

    # projects cards
    arts = {
        "sdwan": """<svg viewBox="0 0 400 150" preserveAspectRatio="xMidYMid slice"><path class="a-ok flow" d="M80 35 L200 75"/><path class="a-line" d="M80 45 L200 82" stroke-dasharray="4 4"/><path class="a-ok flow" d="M80 115 L200 75"/><path class="a-line" d="M80 105 L200 68" stroke-dasharray="4 4"/><path class="a-ok flow" d="M320 35 L200 75"/><path class="a-line" d="M320 45 L200 82" stroke-dasharray="4 4"/><rect class="a-box" x="40" y="25" width="56" height="24" rx="5"/><text class="a-txt" x="52" y="40">SITE-A</text><rect class="a-box" x="40" y="101" width="56" height="24" rx="5"/><text class="a-txt" x="52" y="116">SITE-B</text><rect class="a-box" x="304" y="25" width="56" height="24" rx="5"/><text class="a-txt" x="316" y="40">SITE-C</text><rect class="a-box" x="168" y="62" width="64" height="26" rx="5" style="stroke:var(--amber)"/><text class="a-txt" x="183" y="79" style="fill:var(--amber)">HUB</text><text class="a-txt" x="290" y="125">IKEv2 · AES-256</text></svg>""",
        "hybrid-cloud": """<svg viewBox="0 0 400 150" preserveAspectRatio="xMidYMid slice"><path class="a-vi" d="M110 75 L270 40"/><path class="a-vi" d="M110 75 L270 110"/><rect class="a-box" x="50" y="60" width="74" height="30" rx="5" style="stroke:var(--amber)"/><text class="a-txt" x="58" y="79" style="fill:var(--amber)">FORTIGATE</text><rect class="a-box" x="262" y="25" width="90" height="30" rx="15" style="stroke:var(--violet)"/><text class="a-txt" x="276" y="44">AZURE VPN GW</text><rect class="a-box" x="262" y="95" width="90" height="30" rx="15" style="stroke:var(--violet)"/><text class="a-txt" x="280" y="114">AWS TGW</text><text class="a-txt" x="160" y="70">BGP / IPsec</text></svg>""",
        "lan-optimization": """<svg viewBox="0 0 400 150" preserveAspectRatio="xMidYMid slice"><path class="a-hot" d="M200 30 L120 75 M200 30 L280 75"/><path class="a-line" d="M120 75 L70 120 M120 75 L170 120 M280 75 L230 120 M280 75 L330 120"/><rect class="a-box" x="172" y="18" width="56" height="22" rx="5" style="stroke:var(--amber)"/><text class="a-txt" x="187" y="32">CORE</text><rect class="a-box" x="96" y="64" width="48" height="22" rx="5"/><text class="a-txt" x="106" y="78">DIST</text><rect class="a-box" x="256" y="64" width="48" height="22" rx="5"/><text class="a-txt" x="266" y="78">DIST</text><rect class="a-box" x="52" y="112" width="36" height="18" rx="4"/><rect class="a-box" x="152" y="112" width="36" height="18" rx="4"/><rect class="a-box" x="212" y="112" width="36" height="18" rx="4"/><rect class="a-box" x="312" y="112" width="36" height="18" rx="4"/><text class="a-txt" x="56" y="124">V10</text><text class="a-txt" x="156" y="124">V20</text><text class="a-txt" x="216" y="124">V30</text><text class="a-txt" x="316" y="124">V40</text></svg>""",
        "monitoring-stack": """<svg viewBox="0 0 400 150" preserveAspectRatio="xMidYMid slice"><polyline class="a-ok" points="30,110 70,100 100,104 130,80 160,90 190,60 220,72 250,40 280,96 300,104 330,88 370,92"/><path class="a-line" d="M30 50 L370 50" stroke-dasharray="3 5"/><circle cx="250" cy="40" r="5" style="fill:var(--red)"/><text class="a-txt" x="260" y="34" style="fill:var(--red)">trigger → GLPI</text><text class="a-txt" x="30" y="44">threshold</text></svg>""",
    }
    pcards = ""
    for p in PROJECTS:
        facts = "".join(f"<div><b>{a}</b><span>{t(*b)}</span></div>" for a, b in p["facts"])
        pcards += f"""
      <article class="proj reveal">
        <a class="art" href="projects/{p['id']}.html" aria-hidden="true" tabindex="-1">{arts[p['id']]}</a>
        <div class="body">
          <span class="tagline">{p['tagline']} · {t(*p['kind'])}</span>
          <h3>{t(*p['title'])}</h3>
          <p>{t(*p['card'])}</p>
          {'<div class="facts">' + facts + '</div>' if facts else ''}
          <div class="foot">{chips(p['chips'])}<a class="more" href="projects/{p['id']}.html">{t('Case study', 'Étude de cas')} →</a></div>
        </div>
      </article>"""

    CAT = {"bgp": "routing", "ospf": "routing", "mpls-vrf": "routing", "vlan": "switching", "switching-resilience": "switching",
           "ipsec": "vpn", "sdwan-failover": "fortinet", "fortigate-ha": "fortinet", "ansible-network": "ops", "snmp-zabbix": "ops"}
    labrows = "".join(
        f"""<tr data-cat="{CAT[l['id']]}"><td>Gi0/{i + 1}</td><td><a href="labs/{l['id']}.html">{t(*l['title'])}</a></td><td class="desc">{t(*l['focus'])}</td>
<td><span class="state" style="--c:var(--green)">{t('guide ready', 'guide prêt')}</span> <span class="lvl">{t(*l['level'])}</span></td></tr>"""
        for i, l in enumerate(LABS))

    body = f"""
<section class="hero" id="top">
  <div class="wrap">
    <div>
      <span class="status"><span class="led"></span>{t('Open to Network, Security &amp; Cloud roles · Paris', 'Ouvert aux postes Réseaux, Sécurité &amp; Cloud · Paris')}</span>
      <h1><span class="name">TAREK MEDJOUB</span>{t('Network, Security &amp; <em>Cloud</em> Engineer.', 'Ingénieur Réseaux, Sécurité &amp; <em>Cloud</em>.')}</h1>
      <p class="lede">{t('I design, secure and monitor <strong>multisite enterprise networks</strong>: Fortinet SD-WAN, IPsec/BGP and <strong>hybrid connectivity to Azure and AWS</strong>. I’ve run production networks, led a team and managed projects.',
                         'Je conçois, sécurise et supervise des <strong>réseaux d’entreprise multisites</strong> : SD-WAN Fortinet, IPsec/BGP et <strong>connectivité hybride vers Azure et AWS</strong>. J’ai exploité des réseaux en production, encadré une équipe et piloté des projets.')}</p>
      <div class="motto">
        <span style="--c:var(--green)">{t('Connected.', 'Connecter.')}</span>
        <span style="--c:var(--red)">{t('Secured.', 'Sécuriser.')}</span>
        <span style="--c:var(--violet)">{t('Monitored.', 'Superviser.')}</span>
      </div>
      <div class="cta">
        <a class="btn primary" href="#contact">{t('Let’s talk', 'Me contacter')} →</a>
        <a class="btn" href="{cv_main}" download>↓ {t('Download CV', 'Télécharger le CV')}</a>
        <a class="btn" href="#projects">{t('See my work', 'Voir mes projets')}</a>
      </div>
    </div>

    <figure class="topo" aria-label="{t('Interactive SD-WAN and hybrid cloud topology simulation', 'Simulation interactive SD-WAN et cloud hybride')}">
      <div class="topo-head">
        <div class="dots"><i></i><i></i><i></i></div>
        <span class="t">sdwan-lab · hub-and-spoke + {t('hybrid cloud', 'cloud hybride')}</span>
        <span class="live"><span class="led"></span><span id="liveTxt">…</span></span>
      </div>
      <svg id="topo" viewBox="0 0 530 400" role="img" aria-label="{t('Three branch sites with two ISP links each to an HQ hub, which connects to Azure and AWS over IPsec with BGP', 'Trois agences avec deux liens FAI chacune vers un hub HQ, relié à Azure et AWS en IPsec avec BGP')}">
        <g id="links"></g><g id="pkts"></g><g id="nodes"></g>
      </svg>
      <div class="legend">
        <span><i style="--c:var(--green)"></i>{t('ISP-1 primary', 'ISP-1 principal')}</span>
        <span><i class="d" style="--c:var(--green)"></i>{t('ISP-2 backup', 'ISP-2 secours')}</span>
        <span><i class="d" style="--c:var(--violet)"></i>{t('IPsec + BGP to cloud', 'IPsec + BGP vers le cloud')}</span>
        <span><i style="--c:var(--red)"></i>{t('down', 'coupé')}</span>
      </div>
      <div class="sla">
        <div class="sla-head">
          <span>{t('SLA probe latency', 'Latence des sondes SLA')} ·
            <select id="slaSite" aria-label="{t('Site', 'Agence')}"><option value="A">SITE-A</option><option value="B">SITE-B</option><option value="C">SITE-C</option></select></span>
          <span class="vals"><span style="color:var(--green)">ISP-1 <b id="slaV1">—</b></span><span style="color:var(--violet)">ISP-2 <b id="slaV2">—</b></span><span style="color:var(--red)">{t('threshold 100 ms', 'seuil 100 ms')}</span></span>
        </div>
        <svg id="slaSvg" viewBox="0 0 400 58" preserveAspectRatio="none" aria-hidden="true"></svg>
      </div>
      <div class="topo-ctl">
        <button class="warn" id="failIsp1">⚡ {t('Fail ISP-1 on all sites', 'Couper ISP-1 sur toutes les agences')}</button>
        <button id="restore">↺ {t('Restore', 'Rétablir')}</button>
        <span class="hint">{t('tip: click any link to cut it', 'astuce : cliquez un lien pour le couper')}</span>
      </div>
      <div class="log" id="log" aria-live="polite"></div>
    </figure>
  </div>
</section>

<div class="stats">
  <div class="wrap">
    <div class="stat"><b>4</b><span>{t('sites on SD-WAN', 'sites en SD-WAN')}</span></div>
    <div class="stat"><b>≈1.5<small>s</small></b><span>{t('failover in lab (was 3–5 min)', 'bascule en lab (contre 3–5 min)')}</span></div>
    <div class="stat"><b>6</b><span>{t('engineers &amp; techs led', 'ingénieurs &amp; techniciens encadrés')}</span></div>
    <div class="stat"><b>2</b><span>{t('clouds: Azure + AWS', 'clouds : Azure + AWS')}</span></div>
    <div class="stat"><b>10</b><span>{t('EVE-NG lab guides', 'guides de lab EVE-NG')}</span></div>
  </div>
</div>


<section class="quick" aria-labelledby="quickT">
  <div class="wrap">
    <div class="quick-card reveal">
      <div class="quick-head"><span class="kicker" id="quickT" style="margin:0">{t('for recruiters · in 30 seconds', 'pour les recruteurs · en 30 secondes')}</span></div>
      <dl class="quick-grid">
        <div><dt>{t('Looking for', 'Recherche')}</dt><dd>{t('Network, Security or Cloud Engineer role', 'Poste d’ingénieur Réseaux, Sécurité ou Cloud')}</dd></div>
        <div><dt>{t('Based in', 'Basé à')}</dt><dd>Paris, France</dd></div>
        <div><dt>{t('Core strengths', 'Points forts')}</dt><dd>{t('Fortinet SD-WAN &amp; firewalls · OSPF/BGP · IPsec · Azure/AWS connectivity', 'SD-WAN &amp; pare-feu Fortinet · OSPF/BGP · IPsec · connectivité Azure/AWS')}</dd></div>
        <div><dt>{t('Beyond tech', 'Au-delà de la technique')}</dt><dd>{t('Led a team of 6 · MBA in project management', 'Chef d’une équipe de 6 · MBA management de projet')}</dd></div>
      </dl>
      <div class="quick-act">
        <a class="btn primary" href="{cv_main}" download>↓ CV (PDF)</a>
        <a class="btn" href="mailto:{EMAIL}">✉ {t('Email me', 'M’écrire')}</a>
        <a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">in LinkedIn</a>
        <a class="btn" href="projects/sdwan.html">{t('Best case study', 'Étude de cas phare')} →</a>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="about">
  <div class="wrap about-grid">
    <div class="about-text reveal">
      <div class="kicker">01 / {t('about', 'à propos')}</div>
      <h2>{t('From network operations to project delivery.', 'De l’exploitation réseau au pilotage de projets.')}</h2>
      <p>{t('My core is <strong>Cisco routing &amp; switching and Fortinet security</strong>: VLANs, OSPF/BGP, firewall policies, NAT and IPsec VPNs across multisite networks.',
            'Mon socle : <strong>routage &amp; commutation Cisco et sécurité Fortinet</strong>. VLAN, OSPF/BGP, politiques de pare-feu, NAT et VPN IPsec sur des réseaux multisites.')}</p>
      <p>{t('At Condor Electronics I became a <strong>team leader</strong>, running a multisite industrial network with four technicians and two engineers. I also moved its intersite connectivity to Fortinet SD-WAN.',
            'Chez Condor Electronics, je suis devenu <strong>chef d’équipe</strong> : j’ai piloté un réseau industriel multisite avec quatre techniciens et deux ingénieurs, et migré son interconnexion vers le SD-WAN Fortinet.')}</p>
      <p>{t('Today I extend on-prem networks into the cloud: <strong>FortiGate to Azure VPN Gateway and AWS Transit Gateway</strong> over IPsec with BGP, monitored centrally with PRTG. An MBA in project management completes the picture.',
            'Aujourd’hui, j’étends les réseaux locaux vers le cloud : <strong>FortiGate vers Azure VPN Gateway et AWS Transit Gateway</strong> en IPsec avec BGP, supervisés depuis PRTG. Un MBA en management de projet complète le profil.')}</p>
      <p class="quote">{t('I don’t just make it work. I make it resilient, documented and observable.', 'Faire fonctionner ne suffit pas : je rends les réseaux résilients, documentés et observables.')}</p>
    </div>
    <div class="term reveal">
      <div class="term-head"><div class="dots"><i></i><i></i><i></i></div><span>tarek-medjoub · ssh</span></div>
<pre class="term-body"><span class="p">tarek#</span> show version
<span class="k">{t('Engineer', 'Ingénieur')} </span>  Tarek MEDJOUB
<span class="k">{t('Role    ', 'Poste   ')} </span>  {t('Network, Security &amp; Cloud Engineer', 'Ingénieur Réseaux, Sécurité &amp; Cloud')}
<span class="k">{t('Location', 'Lieu    ')} </span>  Paris, France
<span class="k">Status   </span>  <span class="g">● {t('open to opportunities', 'ouvert aux opportunités')}</span>
<span class="k">{t('Since   ', 'Depuis  ')} </span>  {t('2023 (production networks)', '2023 (réseaux en production)')}

<span class="p">tarek#</span> show modules
<span class="k">slot 1</span>   {t('Routing &amp; Switching', 'Routage &amp; Commutation')}   <span class="g">ok</span>
<span class="k">slot 2</span>   {t('Fortinet Security    ', 'Sécurité Fortinet    ')}   <span class="g">ok</span>
<span class="k">slot 3</span>   SD-WAN / VPN            <span class="g">ok</span>
<span class="k">slot 4</span>   {t('Hybrid Cloud         ', 'Cloud hybride        ')}   <span class="g">ok</span>
<span class="k">slot 5</span>   {t('Monitoring &amp; ITSM    ', 'Supervision &amp; ITSM   ')}   <span class="g">ok</span>
<span class="k">slot 6</span>   {t('Project Management   ', 'Gestion de projet    ')}   <span class="v">MBA</span>

<span class="p">tarek#</span> show interfaces languages
<span class="k">FR, EN</span>     <span class="g">up/up</span></pre>
    </div>
  </div>
</section>

<section class="sec" id="services">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">02 / {t('what i do', 'ce que je fais')}</div>
      <h2>{t('How I can help your infrastructure.', 'Comment je peux aider votre infrastructure.')}</h2>
      <p class="intro">{t('As an independent Network &amp; Security Engineer, I audit and strengthen existing infrastructure. Every engagement ends with clear, usable documentation.',
                           'En tant qu’ingénieur réseaux &amp; sécurité indépendant, j’audite et je renforce les infrastructures existantes. Chaque mission se termine par une documentation claire et exploitable.')}</p>
    </div>
    <div class="cards4">
      <article class="card reveal"><div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg></div>
        <span class="num">svc-01</span><h3>{t('Network &amp; security audit', 'Audit réseau &amp; sécurité')}</h3>
        <p>{t('Review of switching, routing and firewall configurations (VLAN, ACL, OSPF/BGP), with prioritised findings.', 'Revue des configurations de commutation, routage et pare-feu (VLAN, ACL, OSPF/BGP), avec constats priorisés.')}</p></article>
      <article class="card reveal"><div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg></div>
        <span class="num">svc-02</span><h3>{t('Firewall policy review', 'Revue des politiques de pare-feu')}</h3>
        <p>{t('FortiGate rule bases, zones &amp; DMZ, segmentation, IPS profiles and hardening. Tighter policy, less exposure.', 'Règles FortiGate, zones &amp; DMZ, segmentation, profils IPS et durcissement. Moins de règles larges, moins d’exposition.')}</p></article>
      <article class="card reveal"><div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M7.3 11l9.4-4M7.3 13l9.4 4"/></svg></div>
        <span class="num">svc-03</span><h3>{t('VPN &amp; SD-WAN assessment', 'Évaluation VPN &amp; SD-WAN')}</h3>
        <p>{t('IPsec / SSL VPN architecture, SD-WAN SLA rules, path steering and dual-ISP failover design.', 'Architecture VPN IPsec / SSL, règles SLA SD-WAN, orientation du trafic et bascule double opérateur.')}</p></article>
      <article class="card reveal"><div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9a4.5 4.5 0 0 0 1 9z"/></svg></div>
        <span class="num">svc-04</span><h3>{t('Cloud connectivity review', 'Revue de la connectivité cloud')}</h3>
        <p>{t('Site-to-cloud VPN to Azure VPN Gateway and AWS Transit Gateway, BGP route propagation and monitoring.', 'VPN site-à-cloud vers Azure VPN Gateway et AWS Transit Gateway, propagation BGP et supervision.')}</p></article>
    </div>
    <div class="method reveal" aria-label="{t('Working method', 'Méthode de travail')}">
      <div><b>01</b><h4>{t('Discover', 'Découvrir')}</h4><p>{t('Inventory, diagrams, current flows.', 'Inventaire, schémas, flux existants.')}</p></div>
      <div><b>02</b><h4>{t('Audit', 'Auditer')}</h4><p>{t('Configs against best practice.', 'Configurations vs bonnes pratiques.')}</p></div>
      <div><b>03</b><h4>{t('Design', 'Concevoir')}</h4><p>{t('Target architecture &amp; plan.', 'Architecture cible &amp; plan.')}</p></div>
      <div><b>04</b><h4>{t('Validate', 'Valider')}</h4><p>{t('Test in EVE-NG before production.', 'Tester sous EVE-NG avant la production.')}</p></div>
      <div><b>05</b><h4>{t('Document', 'Documenter')}</h4><p>{t('Runbooks, diagrams, handover.', 'Procédures, schémas, passation.')}</p></div>
    </div>
  </div>
</section>

<section class="sec" id="stack">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">03 / {t('technical stack', 'environnement technique')}</div>
      <h2>{t('Skills &amp; expertise.', 'Compétences &amp; expertise.')}</h2>
      <p class="intro">{t('My skills, laid out as a routing table. Highlighted entries are the ones I use most in production.', 'Mes compétences, présentées comme une table de routage. Les entrées en surbrillance sont celles que j’utilise le plus en production.')}</p>
    </div>
    <div class="rtable reveal">
      <div class="rcodes"><span class="p">tarek#</span>show ip route skills<br>Codes: C - core, S - {t('security', 'sécurité')}, W - WAN, V - VPN, H - {t('high availability', 'haute dispo')}, N - services, K - cloud, M - {t('monitoring', 'supervision')}, O - {t('systems', 'systèmes')}</div>
      {rrows}
    </div>
  </div>
</section>

<section class="sec" id="experience">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">04 / {t('experience', 'expérience')}</div>
      <h2>{t('Experience &amp; responsibilities.', 'Expérience &amp; responsabilités.')}</h2>
      <p class="intro">{t('My career as a traceroute: one hop per role, from my first Cisco configs to independent consulting.', 'Mon parcours en traceroute : un saut par poste, de mes premières configurations Cisco au conseil indépendant.')}</p>
    </div>
    <div class="trace">
      <div class="trace-cmd reveal"><span class="p">tarek#</span> traceroute career --from 2023 --to now</div>
      <div class="hop reveal"><div class="hopn">1</div><div class="hopbody">
        <div class="hophead"><h3>{t('Network Engineer Intern', 'Stagiaire ingénieur réseau')}</h3><span class="when">{t('Feb 2023 → Jun 2023', 'févr. 2023 → juin 2023')}</span></div>
        <div class="hopmeta">3K Solutions · {t('Algeria · internship', 'Algérie · stage')}</div>
        <ul><li>{t('Configured Cisco equipment: IP addressing, VLANs and static routing.', 'Configuration d’équipements Cisco : adressage IP, VLAN et routage statique.')}</li>
            <li>{t('Ran connectivity tests and validated the configurations.', 'Tests de connectivité et validation des configurations.')}</li></ul>
        {chips(['Cisco IOS', 'VLAN', t('Static routing', 'Routage statique')])}
      </div></div>
      <div class="hop reveal"><div class="hopn">2</div><div class="hopbody">
        <div class="hophead"><h3>{t('Team Leader &amp; Network Security Project Lead', 'Chef d’équipe &amp; chef de projet sécurité réseau')}</h3><span class="when">{t('Oct 2023 → Sep 2025', 'oct. 2023 → sept. 2025')}</span></div>
        <div class="hopmeta">Condor Electronics · {t('Algeria · multisite industrial network', 'Algérie · réseau industriel multisite')}</div>
        <ul><li>{t('Led a team of <strong>four technicians and two engineers</strong> running a multisite industrial network.', 'Encadrement d’une équipe de <strong>quatre techniciens et deux ingénieurs</strong> sur un réseau industriel multisite.')}</li>
            <li>{t('Migrated intersite connectivity to <strong>Fortinet SD-WAN</strong>, with Ubiquiti links as backup paths.', 'Migration de l’interconnexion des sites vers le <strong>SD-WAN Fortinet</strong>, avec des liens Ubiquiti en secours.')}</li>
            <li>{t('Audited VLAN, ACL and OSPF configurations across sites.', 'Audit des configurations VLAN, ACL et OSPF sur l’ensemble des sites.')}</li>
            <li>{t('Handled Zabbix / PRTG alerts and GLPI incident tickets.', 'Traitement des alertes Zabbix / PRTG et des tickets d’incident GLPI.')}</li></ul>
        {chips(['Fortinet SD-WAN', 'Ubiquiti', 'OSPF', 'ACL', 'Zabbix', 'PRTG', 'GLPI', t('Team leadership', 'Management d’équipe')], ['Fortinet SD-WAN'])}
      </div></div>
      <div class="hop reveal"><div class="hopn">3</div><div class="hopbody">
        <div class="hophead"><h3>{t('Assistant Network &amp; Security Project Manager', 'Assistant chef de projet réseaux &amp; sécurité')}</h3><span class="when">{t('Mar 2026 → Sep 2026', 'mars 2026 → sept. 2026')}</span></div>
        <div class="hopmeta">SGHP · France · {t('internship', 'stage')}</div>
        <ul><li>{t('Supported a migration from on-premises infrastructure to the cloud.', 'Accompagnement d’une migration d’infrastructure locale vers le cloud.')}</li></ul>
        {chips([t('Cloud migration', 'Migration cloud'), t('Project management', 'Gestion de projet')])}
      </div></div>
      <div class="hop now reveal"><div class="hopn">4</div><div class="hopbody">
        <div class="hophead"><h3>{t('Network &amp; Security Engineer', 'Ingénieur réseaux &amp; sécurité')} <span class="pill-now">{t('current', 'actuel')}</span></h3><span class="when">{t('Aug 2026 → now', 'août 2026 → aujourd’hui')}</span></div>
        <div class="hopmeta">{t('Independent', 'Indépendant')} · France</div>
        <ul><li>{t('Audit network and security configurations.', 'Audit des configurations réseau et sécurité.')}</li>
            <li>{t('Review firewall policies and VPN architectures.', 'Revue des politiques de pare-feu et des architectures VPN.')}</li>
            <li>{t('Assess SD-WAN and cloud connectivity, and deliver documentation.', 'Évaluation du SD-WAN et de la connectivité cloud, avec documentation livrée.')}</li></ul>
        {chips(['Audit', t('Firewall policy', 'Politiques pare-feu'), 'VPN', 'SD-WAN', 'Cloud'], ['Audit'])}
      </div></div>
      <div class="hop reveal"><div class="hopn" style="border-style:dashed;color:var(--amber)">5</div><div class="hopbody" style="border-style:dashed;background:transparent">
        <div class="hophead"><h3 style="color:var(--amber)">{t('Your team?', 'Votre équipe ?')}</h3><span class="when">* * * request timed out</span></div>
        <p style="color:var(--muted);margin-top:6px">{t('The next hop isn’t reachable yet.', 'Le prochain saut n’est pas encore joignable.')} <a href="#contact" class="more">{t('Add a route', 'Ajouter une route')} →</a></p>
      </div></div>
    </div>
  </div>
</section>

<section class="sec" id="projects">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">05 / {t('featured work', 'réalisations')}</div>
      <h2>{t('Projects.', 'Projets.')}</h2>
      <p class="intro">{t('Architectures I’ve designed and validated, from production migrations to multi-cloud lab builds. Each one has a full case study: architecture, configs, validation and lessons learned.',
                           'Des architectures conçues et validées, des migrations en production aux maquettes multi-cloud. Chacune a son étude de cas complète : architecture, configurations, validation et retours d’expérience.')}</p>
    </div>
    <div class="proj-grid">{pcards}
    </div>
  </div>
</section>

<section class="sec" id="labs">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">06 / {t('eve-ng learning labs', 'labs eve-ng')}</div>
      <h2>{t('Protocols, explained in the lab.', 'Les protocoles, expliqués en lab.')}</h2>
      <p class="intro">{t('Ten hands-on EVE-NG lab guides. Each covers topology, addressing, configs, verification commands and break/fix exercises.',
                           'Dix guides de lab EVE-NG. Chacun couvre topologie, adressage, configurations, commandes de vérification et exercices de panne.')}</p>
    </div>
    <div class="labs-wrap reveal">
      <div class="labs-top">
        <span class="cmd"><span class="p">tarek#</span> show interfaces status labs</span>
        <div class="prog"><span>{t('10 / 10 guides · captures &amp; .unl files coming', '10 / 10 guides · captures &amp; fichiers .unl à venir')}</span><div class="bar-p"><i style="width:100%"></i></div></div>
      </div>
      <div class="lab-filter" role="group" aria-label="{t('Filter labs', 'Filtrer les labs')}">
        <button type="button" class="on" data-f="all">{t('All', 'Tous')} <i>10</i></button>
        <button type="button" data-f="routing">{t('Routing', 'Routage')} <i>3</i></button>
        <button type="button" data-f="switching">{t('Switching', 'Commutation')} <i>2</i></button>
        <button type="button" data-f="vpn">VPN <i>1</i></button>
        <button type="button" data-f="fortinet">Fortinet <i>2</i></button>
        <button type="button" data-f="ops">{t('Automation &amp; monitoring', 'Automatisation &amp; supervision')} <i>2</i></button>
      </div>
      <table class="ifs">
        <thead><tr><th>Port</th><th>Lab</th><th>{t('Focus', 'Objet')}</th><th>Status</th></tr></thead>
        <tbody>{labrows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec" id="certs">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">07 / {t('credentials', 'certifications &amp; formation')}</div>
      <h2>{t('A technical foundation. A project mindset.', 'Un socle technique. Un esprit projet.')}</h2>
      <p class="intro">{t('Certifications and academy training on the technical side, plus a Master’s and an MBA.', 'Certifications et formations côté technique, complétées par un Master et un MBA.')}</p>
    </div>
    <div class="two">
      <div class="list reveal">
        <h3>// {t('CERTIFICATIONS &amp; TRAINING', 'CERTIFICATIONS &amp; FORMATIONS')}</h3>
        <div class="li"><span class="badge" style="--c:var(--violet)">AVIATRIX</span><div><b>Multicloud Network Associate</b><span>{t('Multicloud networking certification', 'Certification réseau multicloud')}</span></div></div>
        <div class="li"><span class="badge" style="--c:var(--red)">HUAWEI</span><div><b>HCIA Cloud Computing</b><span>{t('Huawei certification', 'Certification Huawei')}</span></div></div>
        <div class="li"><span class="badge" style="--c:var(--red)">HUAWEI</span><div><b>HCIA Routing &amp; Switching</b><span>{t('Huawei certification', 'Certification Huawei')}</span></div></div>
        <div class="li"><span class="badge" style="--c:var(--green)">CISCO NA</span><div><b>CCNP: Core Networking</b><span>{t('Cisco Networking Academy training', 'Formation Cisco Networking Academy')}</span></div></div>
        <div class="li"><span class="badge" style="--c:var(--green)">CISCO NA</span><div><b>CCNA: Switching, Routing &amp; Wireless Essentials</b><span>{t('Cisco Networking Academy training', 'Formation Cisco Networking Academy')}</span></div></div>
        <div class="li"><span class="badge" style="--c:var(--green)">CISCO NA</span><div><b>Network Defense · Network Security</b><span>{t('Cisco Networking Academy training', 'Formation Cisco Networking Academy')}</span></div></div>
      </div>
      <div>
        <div class="list reveal">
          <h3>// {t('EDUCATION', 'FORMATION')}</h3>
          <div class="li"><span class="badge" style="--c:var(--amber)">2024–26</span><div><b>{t('MBA, Management &amp; Project Management', 'MBA Management &amp; Gestion de projet')}</b><span>{t('Leadership, planning and delivery of IT projects', 'Leadership, planification et conduite de projets IT')}</span></div></div>
          <div class="li"><span class="badge" style="--c:var(--amber)">2021–23</span><div><b>{t('Master’s in Networks &amp; Telecommunications', 'Master Réseaux &amp; Télécommunications')}</b><span>{t('Assessed by ENIC-NARIC France as comparable to level 7 (Master’s)', 'Attestation de comparabilité ENIC-NARIC France : niveau 7 (Master)')}</span></div></div>
        </div>
        <div class="next reveal"><b>$ next-hop</b> → {t('official vendor exams (Fortinet FCP, Cisco CCNA) to formalise my hands-on experience.', 'examens officiels (Fortinet FCP, Cisco CCNA) pour valider mon expérience terrain.')}</div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="resume">
  <div class="wrap">
    <div class="reveal">
      <div class="kicker">08 / {t('resume', 'cv')}</div>
      <h2>{t('Choose your CV.', 'Choisissez votre CV.')}</h2>
      <p class="intro">{t('One-page PDFs in English and French, plus a web version you can read here and print.', 'PDF d’une page en français et en anglais, plus une version web lisible ici et imprimable.')}</p>
    </div>
    <div class="cv cv3">
      <div class="cvcard reveal"><div class="paper"><i></i><i></i><i style="width:80%"></i><i></i><i style="width:60%"></i><i></i><span>EN</span></div>
        <div><h3>English CV</h3><p>1 page · PDF</p><div class="row"><a class="btn primary" href="{cv_en}" download>↓ {t('Download', 'Télécharger')}</a><a class="btn" href="{cv_en}" target="_blank" rel="noopener">{t('Preview', 'Aperçu')}</a></div></div></div>
      <div class="cvcard reveal"><div class="paper"><i></i><i></i><i style="width:75%"></i><i></i><i style="width:55%"></i><i></i><span>FR</span></div>
        <div><h3>CV en français</h3><p>1 page · PDF</p><div class="row"><a class="btn primary" href="{cv_fr}" download>↓ {t('Download', 'Télécharger')}</a><a class="btn" href="{cv_fr}" target="_blank" rel="noopener">{t('Preview', 'Aperçu')}</a></div></div></div>
      <div class="cvcard reveal"><div class="paper"><i></i><i></i><i style="width:70%"></i><i></i><i style="width:65%"></i><i></i><span>WEB</span></div>
        <div><h3>{t('Web CV', 'CV web')}</h3><p>{t('Readable · printable', 'Lisible · imprimable')}</p><div class="row"><a class="btn primary" href="cv.html">{t('Open', 'Ouvrir')} →</a></div></div></div>
    </div>
  </div>
</section>

<section class="sec" id="contact">
  <div class="wrap contact">
    <div class="reveal">
      <div class="kicker">09 / contact</div>
      <h2>{t('Let’s talk infrastructure.', 'Parlons infrastructure.')}</h2>
      <p class="big">{t('A role, an audit or a network that needs fixing?', 'Un poste, un audit ou un réseau à remettre d’aplomb ?')} <span style="color:var(--amber)">{t('Send me a packet.', 'Envoyez-moi un paquet.')}</span></p>
      <div class="clinks">
        <a class="clink" href="mailto:{EMAIL}"><span class="ico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span>
          <div><small>EMAIL</small><span>{EMAIL}</span></div><button class="copy" type="button" data-copy="{EMAIL}">{t('copy', 'copier')}</button></a>
        <a class="clink" href="{LINKEDIN}" target="_blank" rel="noopener"><span class="ico"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.78-1.7-2.78-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg></span>
          <div><small>LINKEDIN</small><span>in/tarek-medjoub</span></div></a>
        <div class="clink" style="cursor:default"><span class="ico"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span>
          <div><small>{t('LOCATION', 'LOCALISATION')}</small><span>Paris, France</span></div></div>
      </div>
    </div>
    <div class="term reveal">
      <div class="term-head"><div class="dots"><i></i><i></i><i></i></div><span>compose-message.sh</span></div>
      <form class="cf term-body" id="cf">
        <div class="grid2">
          <div><label for="cfName"><span class="p">$</span>{t('name', 'nom')}</label><input id="cfName" required autocomplete="name"></div>
          <div><label for="cfOrg"><span class="p">$</span>{t('company', 'entreprise')}</label><input id="cfOrg" autocomplete="organization"></div>
        </div>
        <div><label for="cfTopic"><span class="p">$</span>{t('topic', 'sujet')}</label>
          <select id="cfTopic"><option>{t('Job opportunity', 'Opportunité de poste')}</option><option>{t('Network / security audit', 'Audit réseau / sécurité')}</option><option>{t('SD-WAN or VPN project', 'Projet SD-WAN ou VPN')}</option><option>{t('Cloud connectivity', 'Connectivité cloud')}</option><option>{t('Something else', 'Autre')}</option></select></div>
        <div><label for="cfMsg"><span class="p">$</span>message</label><textarea id="cfMsg" required></textarea></div>
        <button class="btn primary" type="submit" style="justify-self:start">./send --via mail →</button>
        <span class="note" style="all:unset;font-family:var(--mono);font-size:11px;color:var(--dim)">{t('Opens your email client with the message pre-filled.', 'Ouvre votre messagerie avec le message pré-rempli.')}</span>
      </form>
    </div>
  </div>
</section>
"""
    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Tarek Medjoub","jobTitle":"%s",
"email":"mailto:%s","url":"%s","address":{"@type":"PostalAddress","addressLocality":"Paris","addressCountry":"FR"},
"sameAs":["%s"],"knowsLanguage":["fr","en"],
"knowsAbout":["Fortinet SD-WAN","FortiGate","BGP","OSPF","IPsec VPN","Azure VPN Gateway","AWS Transit Gateway","Zabbix","PRTG","Network security"],
"alumniOf":[{"@type":"EducationalOrganization","name":"Master's in Networks & Telecommunications"}]}
</script>""" % (t("Network, Security & Cloud Engineer", "Ingénieur Réseaux, Sécurité & Cloud"), EMAIL, SITE, LINKEDIN)
    root_js = "../" if lang == "fr" else ""
    return layout(
        lang, "index.html",
        t("Tarek MEDJOUB · Network, Security & Cloud Engineer", "Tarek MEDJOUB · Ingénieur Réseaux, Sécurité & Cloud"),
        t("Network, Security & Cloud Engineer in Paris. Fortinet SD-WAN, multisite networks, IPsec/BGP and hybrid connectivity to Azure and AWS.",
          "Ingénieur Réseaux, Sécurité & Cloud à Paris. SD-WAN Fortinet, réseaux multisites, IPsec/BGP et connectivité hybride vers Azure et AWS."),
        body, home=True, jsonld=jsonld,
        extra_js=f'<script src="{root_js}assets/js/topology.js" defer></script>')
