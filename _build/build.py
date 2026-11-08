"""Static site generator for tarekmjb.github.io/tmedjoub.github.io.
Usage:  python3 build.py [output_dir]      (default: ../out)
Edit content in home.py, projects_data.py, labs_data.py, then rebuild."""
import os, sys, datetime
from common import L, layout, doc_page, SITE, EMAIL, LINKEDIN, esc
from home import home
from projects_data import PROJECTS, BUILDERS, META
from labs_data import LABS, lab_sections
from tools import tools_page

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
written = []


def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    written.append(rel)


LAB_FOR = {"sdwan": ["sdwan-failover", "ipsec", "fortigate-ha"], "hybrid-cloud": ["ipsec", "bgp", "sdwan-failover"],
           "lan-optimization": ["vlan", "switching-resilience", "ospf"], "monitoring-stack": ["snmp-zabbix", "ansible-network", "fortigate-ha"]}
TOOL_FOR = {"sdwan": "mss", "hybrid-cloud": "mss", "lan-optimization": "vlsm", "monitoring-stack": "subnet"}
TOOL_NAME = {"mss": ("IPsec MTU / MSS calculator", "Calcul MTU / MSS IPsec"), "vlsm": ("VLSM planner", "Planificateur VLSM"),
             "subnet": ("IPv4 subnet calculator", "Calcul de sous-réseau IPv4")}
PROJ_FOR_LAB = {"bgp": "hybrid-cloud", "ospf": "lan-optimization", "vlan": "lan-optimization", "ipsec": "sdwan", "mpls-vrf": "sdwan",
                "switching-resilience": "lan-optimization", "sdwan-failover": "sdwan", "fortigate-ha": "sdwan",
                "ansible-network": "monitoring-stack", "snmp-zabbix": "monitoring-stack"}


def related_for_project(x, pid):
    t = x.t; out = []
    for p in [p for p in PROJECTS if p["id"] != pid][:2]:
        out.append((t("Case study", "Étude de cas"), t(*p["title"]), p["tagline"], p["id"] + ".html"))
    labs = {l["id"]: l for l in LABS}
    for lid in LAB_FOR[pid][:1]:
        l = labs[lid]; out.append((t("Lab guide", "Guide de lab"), t(*l["title"]), t(*l["focus"]), f"../labs/{lid}.html"))
    tk = TOOL_FOR[pid]
    out.append((t("Tool", "Outil"), t(*TOOL_NAME[tk]), t("Free, runs in your browser", "Gratuit, dans votre navigateur"), f"../tools.html#{tk}"))
    return out


def related_for_lab(x, idx):
    t = x.t; out = []
    for k in (1, 2):
        l = LABS[(idx + k) % len(LABS)]
        out.append((t("Lab guide", "Guide de lab"), t(*l["title"]), t(*l["focus"]), l["id"] + ".html"))
    p = next(p for p in PROJECTS if p["id"] == PROJ_FOR_LAB[LABS[idx]["id"]])
    out.append((t("In production", "En production"), t(*p["title"]), p["tagline"], f"../projects/{p['id']}.html"))
    out.append((t("Tool", "Outil"), t("Network toolkit", "Outils réseau"), t("Subnet, VLSM, wildcard, MSS", "Sous-réseau, VLSM, wildcard, MSS"), "../tools.html"))
    return out


def project_page(lang, idx):
    x = L(lang); t = x.t
    p = PROJECTS[idx]; m = META[p["id"]]
    prv, nxt = PROJECTS[idx - 1], PROJECTS[(idx + 1) % len(PROJECTS)]
    home_href = "../index.html"
    body = doc_page(
        x,
        crumbs=[f'<a href="{home_href}">{t("Home", "Accueil")}</a>', f'<a href="{home_href}#projects">{t("Projects", "Projets")}</a>', t(*p["title"])],
        kicker=f'{t("case study", "étude de cas")} · {p["tagline"]}',
        title=t(*p["title"]), summary=t(*p["card"]),
        metas=[(t(*k) + ":", t(*v)) for k, v in m["metas"]],
        kpis=[(a, t(*b)) for a, b in m["kpis"]],
        sections=BUILDERS[p["id"]](x),
        pn=((t(*prv["title"]), prv["id"] + ".html"), (t(*nxt["title"]), nxt["id"] + ".html")),
        back=(home_href + "#projects", t("Back to projects", "Retour aux projets")),
        related=related_for_project(x, p["id"]))
    write(("fr/" if lang == "fr" else "") + f"projects/{p['id']}.html",
          layout(lang, f"projects/{p['id']}.html", f"{t(*p['title'])} · Tarek MEDJOUB", t(*p["card"])[:158], body, doc=True))


def lab_page(lang, idx):
    x = L(lang); t = x.t
    lab = LABS[idx]
    prv, nxt = LABS[idx - 1], LABS[(idx + 1) % len(LABS)]
    home_href = "../index.html"
    status = f'<span class="status-pill" style="--c:var(--green)">{t("guide ready · lab captures coming", "guide prêt · captures du lab à venir")}</span>'
    body = doc_page(
        x,
        crumbs=[f'<a href="{home_href}">{t("Home", "Accueil")}</a>', f'<a href="{home_href}#resources">Labs</a>', t(*lab["title"])],
        kicker=f'EVE-NG lab {idx + 1:02d} · {lab["tags"]}',
        title=t(*lab["title"]), summary=t(*lab["objective"]),
        metas=[(t("Level:", "Niveau :"), t(*lab["level"])), (t("Time:", "Durée :"), lab["time"]), (t("Focus:", "Objet :"), t(*lab["focus"]))],
        kpis=None, sections=lab_sections(x, lab), status=status,
        pn=((t(*prv["title"]), prv["id"] + ".html"), (t(*nxt["title"]), nxt["id"] + ".html")),
        back=(home_href + "#resources", t("Back to resources", "Retour aux ressources")),
        related=related_for_lab(x, idx))
    write(("fr/" if lang == "fr" else "") + f"labs/{lab['id']}.html",
          layout(lang, f"labs/{lab['id']}.html", f"{t(*lab['title'])} · EVE-NG lab · Tarek MEDJOUB", t(*lab["objective"])[:158], body, doc=True))


def cv_page(lang):
    x = L(lang); t = x.t
    root = "../" if lang == "fr" else ""
    pdf = root + ("assets/CV_Tarek_MEDJOUB.pdf" if lang == "fr" else "assets/CV_Tarek_MEDJOUB_EN.pdf")

    def job(title, org, dates, items):
        return (f'<div class="cvj"><div class="h"><b>{title}</b><span class="d">{dates}</span></div><div class="o">{org}</div>'
                + "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>")

    body = f"""
<div class="wrap" id="top">
  <div class="crumbs"><a class="back-btn" href="index.html#resume">← {t('Back to home', 'Retour à l’accueil')}</a><a href="index.html">{t('Home', 'Accueil')}</a><span class="sep">/</span>CV</div>
  <article class="cvpage">
    <header class="cv-top">
      <div><h1>Tarek MEDJOUB</h1><div class="role">{t('Network, Security &amp; Cloud Engineer', 'Ingénieur Réseaux, Sécurité &amp; Cloud')}</div></div>
      <div class="ct">Paris, France<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{LINKEDIN}">linkedin.com/in/tarek-medjoub</a><br><a href="{SITE}">tarekmjb.github.io/tmedjoub.github.io</a></div>
    </header>
    <section class="cvs"><h2>{t('Profile', 'Profil')}</h2><p>{t('Network and security engineer focused on multisite enterprise networks, Fortinet security and hybrid cloud connectivity (Azure, AWS). Former team leader of six on a multisite industrial network, with an MBA in project management. Open to network, security and cloud roles.',
        'Ingénieur réseaux et sécurité spécialisé dans les réseaux d’entreprise multisites, la sécurité Fortinet et la connectivité cloud hybride (Azure, AWS). Ancien chef d’une équipe de six personnes sur un réseau industriel multisite, titulaire d’un MBA en management de projet. Ouvert aux postes réseaux, sécurité et cloud.')}</p></section>
    <section class="cvs"><h2>{t('Experience', 'Expérience')}</h2><div>
      {job(t('Network &amp; Security Engineer', 'Ingénieur réseaux &amp; sécurité'), t('Independent · France', 'Indépendant · France'), t('Aug 2026 – present', 'août 2026 – aujourd’hui'),
           [t('Audit of network and security configurations.', 'Audit des configurations réseau et sécurité.'), t('Review of firewall policies and VPN architectures.', 'Revue des politiques de pare-feu et des architectures VPN.'), t('Assessment of SD-WAN and cloud connectivity, with documentation.', 'Évaluation du SD-WAN et de la connectivité cloud, avec documentation.')])}
      {job(t('Assistant Network &amp; Security Project Manager', 'Assistant chef de projet réseaux &amp; sécurité'), t('SGHP · France · internship', 'SGHP · France · stage'), t('Mar – Sep 2026', 'mars – sept. 2026'),
           [t('Supported a migration from on-premises infrastructure to the cloud.', 'Accompagnement d’une migration d’infrastructure locale vers le cloud.')])}
      {job(t('Team Leader &amp; Network Security Project Lead', 'Chef d’équipe &amp; chef de projet sécurité réseau'), t('Condor Electronics · Algeria', 'Condor Electronics · Algérie'), t('Oct 2023 – Sep 2025', 'oct. 2023 – sept. 2025'),
           [t('Led four technicians and two engineers on a multisite industrial network.', 'Encadrement de quatre techniciens et deux ingénieurs sur un réseau industriel multisite.'),
            t('Migrated intersite connectivity to Fortinet SD-WAN with Ubiquiti backup links.', 'Migration de l’interconnexion des sites vers le SD-WAN Fortinet avec liens de secours Ubiquiti.'),
            t('Audited VLAN, ACL and OSPF configurations; handled Zabbix/PRTG alerts and GLPI tickets.', 'Audit des configurations VLAN, ACL et OSPF ; traitement des alertes Zabbix/PRTG et des tickets GLPI.')])}
      {job(t('Network Engineer Intern', 'Stagiaire ingénieur réseau'), t('3K Solutions · Algeria', '3K Solutions · Algérie'), t('Feb – Jun 2023', 'févr. – juin 2023'),
           [t('Configured Cisco equipment (IP addressing, VLANs, static routing) and tested connectivity.', 'Configuration d’équipements Cisco (adressage IP, VLAN, routage statique) et tests de connectivité.')])}
    </div></section>
    <section class="cvs"><h2>{t('Skills', 'Compétences')}</h2>
      <dl class="cv-skills">
        <dt>{t('Routing &amp; switching', 'Routage &amp; commutation')}</dt><dd>OSPF, BGP, EIGRP, PBR, IPv6 · VLAN, STP/RSTP/MSTP, LACP, DHCP snooping, DAI</dd>
        <dt>WAN / VPN</dt><dd>Fortinet SD-WAN, {t('dual-ISP', 'double FAI')}, FortiManager, FortiAnalyzer · IPsec IKEv1/v2, SSL VPN, GRE, {t('BGP over IPsec', 'BGP sur IPsec')}</dd>
        <dt>{t('Security', 'Sécurité')}</dt><dd>{t('FortiGate firewalls, DMZ &amp; zone policies, ACL, IDS/IPS, segmentation, hardening', 'Pare-feu FortiGate, DMZ &amp; politiques par zone, ACL, IDS/IPS, segmentation, durcissement')}</dd>
        <dt>{t('High availability', 'Haute disponibilité')}</dt><dd>HSRP/VRRP, FortiGate HA, BFD</dd>
        <dt>Cloud</dt><dd>Azure VPN Gateway, AWS Transit Gateway, Aviatrix</dd>
        <dt>{t('Monitoring', 'Supervision')}</dt><dd>Zabbix, PRTG, ManageEngine OpManager, GLPI, SNMPv3</dd>
        <dt>{t('Systems', 'Systèmes')}</dt><dd>Windows Server (AD, DNS, DHCP, GPO), Linux, Bash, Ansible, EVE-NG</dd>
      </dl></section>
    <section class="cvs"><h2>{t('Education', 'Formation')}</h2><div>
      <div class="cvj"><div class="h"><b>{t('MBA, Management &amp; Project Management', 'MBA Management &amp; Gestion de projet')}</b><span class="d">2024 – 2026</span></div></div>
      <div class="cvj"><div class="h"><b>{t('Master’s in Networks &amp; Telecommunications', 'Master Réseaux &amp; Télécommunications')}</b><span class="d">2021 – 2023</span></div><div class="o">{t('ENIC-NARIC France: comparable to level 7', 'ENIC-NARIC France : comparable au niveau 7')}</div></div>
    </div></section>
    <section class="cvs"><h2>{t('Certifications', 'Certifications')}</h2><p>Aviatrix Multicloud Network Associate · Huawei HCIA Cloud Computing · Huawei HCIA Routing &amp; Switching<br>{t('Cisco Networking Academy training', 'Formations Cisco Networking Academy')}: CCNP Core Networking, CCNA SRWE, Network Defense, Network Security</p></section>
    <section class="cvs"><h2>{t('Languages', 'Langues')}</h2><p>{t('French · English', 'Français · Anglais')}</p></section>
  </article>
  <div class="cv-actions">
    <button class="btn primary" type="button" onclick="window.print()">⎙ {t('Print / save as PDF', 'Imprimer / enregistrer en PDF')}</button>
    <a class="btn" href="{pdf}" download>↓ {t('Designed PDF', 'PDF mis en page')}</a>
    <a class="btn" href="index.html#resume">← {t('Back to home', 'Retour à l’accueil')}</a>
    <a class="btn" href="index.html#contact">{t('Contact me', 'Me contacter')} →</a>
  </div>
</div>"""
    write(("fr/" if lang == "fr" else "") + "cv.html",
          layout(lang, "cv.html", t("CV · Tarek MEDJOUB · Network, Security & Cloud Engineer", "CV · Tarek MEDJOUB · Ingénieur Réseaux, Sécurité & Cloud"),
                 t("Web CV of Tarek Medjoub, Network, Security & Cloud Engineer in Paris.", "CV web de Tarek Medjoub, ingénieur réseaux, sécurité & cloud à Paris."), body))


def page_404():
    # GitHub Pages serves this for any missing URL, at any depth: use absolute paths.
    base = "/tmedjoub.github.io/"
    html = layout("en", "404.html", "404 · Destination host unreachable", "Page not found.", f"""
<div class="wrap nf"><div>
  <h1>404</h1>
  <pre><span class="p">guest@portfolio:~$</span> traceroute <span id="nfPath">this-page</span>
 1  tarek-medjoub (gateway)      1.2 ms
 2  * * *
 3  <span style="color:var(--red)">!H  Destination host unreachable</span></pre>
  <p style="color:var(--muted);margin-bottom:22px">This page doesn’t exist (or moved). Cette page n’existe pas (ou a été déplacée).</p>
  <div class="cta" style="justify-content:center">
    <a class="btn primary" href="{base}index.html">← Home</a>
    <a class="btn" href="{base}fr/index.html">← Accueil</a>
    <a class="btn" href="{base}index.html#projects">Projects</a>
  </div>
</div></div>
<script>document.getElementById('nfPath').textContent=location.pathname.replace('{base}','/');</script>""", noindex=True)
    html = html.replace('data-root=""', f'data-root="{base}"')
    html = html.replace('href="assets/', f'href="{base}assets/').replace('src="assets/', f'src="{base}assets/')
    html = html.replace('href="index.html"', f'href="{base}index.html"').replace('href="fr/404.html"', f'href="{base}fr/index.html"')
    html = html.replace('href="404.html"', f'href="{base}index.html"')
    write("404.html", html)


def seo_files():
    today = datetime.date.today().isoformat()
    urls = []
    for lang in ("en", "fr"):
        pre = "fr/" if lang == "fr" else ""
        urls += [pre + "index.html", pre + "cv.html", pre + "tools.html"]
        urls += [pre + f"projects/{p['id']}.html" for p in PROJECTS]
        urls += [pre + f"labs/{l['id']}.html" for l in LABS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u.endswith("index.html") else "0.7"
        sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    write("assets/img/favicon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#1d4ed8"/><text x="16" y="21" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="13" fill="#fff">TM</text></svg>
""")


if __name__ == "__main__":
    for lang in ("en", "fr"):
        write(("fr/" if lang == "fr" else "") + "index.html", home(lang))
        cv_page(lang)
        write(("fr/" if lang == "fr" else "") + "tools.html", tools_page(lang))
        for i in range(len(PROJECTS)):
            project_page(lang, i)
        for i in range(len(LABS)):
            lab_page(lang, i)
    page_404()
    seo_files()
    print(f"built {len(written)} files into {OUT}")
