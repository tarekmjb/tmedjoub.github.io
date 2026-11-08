"""Site-wide header (utility bar + mega menu) and footer, vendor-site style."""
from common import EMAIL, LINKEDIN

ICON = {
    "routing": "M4 6h16M4 12h16M4 18h10",
    "security": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z",
    "sdwan": "M3 12h4l3-8 4 16 3-8h4",
    "cloud": "M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9a4.5 4.5 0 0 0 1 9z",
    "ops": "M3 3v18h18M7 15l4-4 3 3 5-6",
    "case": "M4 7h16v12H4zM9 7V5h6v2",
    "lab": "M9 3v6l-5 9a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-5-9V3M8 3h8",
    "tool": "M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z",
    "user": "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0",
    "mail": "M3 5h18v14H3zM3 7l9 6 9-6",
    "arrow": "M5 12h14M13 6l6 6-6 6",
}


def ico(name, size=18):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICON[name]}"/></svg>')


EXPERTISE = [
    ("routing", ("Routing &amp; Switching", "Routage &amp; Commutation"), ("Campus &amp; multisite, OSPF/BGP, HA", "Campus &amp; multisite, OSPF/BGP, HA")),
    ("security", ("Network Security", "Sécurité réseau"), ("FortiGate, segmentation, IPS", "FortiGate, segmentation, IPS")),
    ("sdwan", ("SD-WAN &amp; VPN", "SD-WAN &amp; VPN"), ("SLA steering, IPsec, dual ISP", "Orientation SLA, IPsec, double FAI")),
    ("cloud", ("Hybrid Cloud", "Cloud hybride"), ("Azure, AWS, BGP over IPsec", "Azure, AWS, BGP sur IPsec")),
    ("ops", ("Monitoring &amp; Automation", "Supervision &amp; Automatisation"), ("Zabbix, PRTG, GLPI, Ansible", "Zabbix, PRTG, GLPI, Ansible")),
]


def header(x, root, lp, home):
    from projects_data import PROJECTS
    from labs_data import LABS
    t = x.t
    H = "" if home else root + lp + "index.html"

    def panel(pid, label, cols, feature):
        return f"""
      <li class="mm">
        <button class="mm-btn" type="button" aria-expanded="false" aria-controls="mm-{pid}">{label}<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
        <div class="mm-panel" id="mm-{pid}">
          <div class="wrap mm-grid">
            {cols}
            {feature}
          </div>
        </div>
      </li>"""

    exp_items = "".join(
        f'<a class="mm-item" href="{H}#expertise-{k}"><span class="mm-ico">{ico(k)}</span><span><b>{t(*n)}</b><small>{t(*d)}</small></span></a>'
        for k, n, d in EXPERTISE)
    exp = panel("expertise", t("Expertise", "Expertise"),
                f'<div class="mm-col mm-col-2"><span class="mm-h">{t("Domains", "Domaines")}</span><div class="mm-items">{exp_items}</div></div>',
                f'<a class="mm-feature" href="{H}#services"><span class="mm-h">{t("Services", "Services")}</span><b>{t("Audit, firewall review, SD-WAN &amp; cloud assessments", "Audit, revue pare-feu, évaluation SD-WAN &amp; cloud")}</b><span class="mm-cta">{t("See how I can help", "Voir comment je peux aider")} {ico("arrow", 14)}</span></a>')

    work_items = "".join(
        f'<a class="mm-item" href="{root + lp}projects/{p["id"]}.html"><span class="mm-ico">{ico("case")}</span><span><b>{t(*p["title"])}</b><small>{p["tagline"]}</small></span></a>'
        for p in PROJECTS)
    work = panel("work", t("Case studies", "Études de cas"),
                 f'<div class="mm-col mm-col-2"><span class="mm-h">{t("Featured work", "Réalisations")}</span><div class="mm-items">{work_items}</div></div>',
                 f'<a class="mm-feature dark" href="{root + lp}projects/sdwan.html"><span class="mm-h">{t("Spotlight", "À la une")}</span><b>{t("From 3–5 minutes to ≈1.5 s failover", "De 3–5 minutes à ≈1,5 s de bascule")}</b><small>{t("Four-site Fortinet SD-WAN migration", "Migration SD-WAN Fortinet sur quatre sites")}</small><span class="mm-cta">{t("Read the case study", "Lire l’étude de cas")} {ico("arrow", 14)}</span></a>')

    lab_items = "".join(
        f'<a class="mm-link" href="{root + lp}labs/{l["id"]}.html"><span>{i + 1:02d}</span>{t(*l["title"])}</a>' for i, l in enumerate(LABS))
    labs = panel("labs", "Labs",
                 f'<div class="mm-col mm-col-2"><span class="mm-h">{t("EVE-NG lab guides", "Guides de lab EVE-NG")}</span><div class="mm-links">{lab_items}</div></div>',
                 f'<a class="mm-feature" href="{H}#resources"><span class="mm-h">{t("Resource center", "Centre de ressources")}</span><b>{t("Browse every guide, case study and tool in one place", "Tous les guides, études de cas et outils au même endroit")}</b><span class="mm-cta">{t("Open the resource center", "Ouvrir le centre de ressources")} {ico("arrow", 14)}</span></a>')

    tools = [("subnet", t("IPv4 subnet calculator", "Calcul de sous-réseau IPv4")), ("ipv6", t("IPv6 calculator", "Calcul IPv6")),
             ("vlsm", t("VLSM planner", "Planificateur VLSM")), ("wildcard", t("Wildcard &amp; ACL helper", "Assistant wildcard &amp; ACL")), ("mss", "IPsec MTU / MSS")]
    tool_items = "".join(f'<a class="mm-link" href="{root + lp}tools.html#{k}"><span>{ico("tool", 14)}</span>{n}</a>' for k, n in tools)
    toolkit = panel("toolkit", t("Toolkit", "Outils"),
                    f'<div class="mm-col"><span class="mm-h">{t("Free network tools", "Outils réseau gratuits")}</span><div class="mm-links one">{tool_items}</div></div>',
                    f'<a class="mm-feature" href="{root + lp}tools.html"><span class="mm-h">{t("Runs in your browser", "Dans votre navigateur")}</span><b>{t("Subnetting, VLSM and IPsec maths, done in seconds", "Sous-réseaux, VLSM et calculs IPsec en quelques secondes")}</b><span class="mm-cta">{t("Open the toolkit", "Ouvrir les outils")} {ico("arrow", 14)}</span></a>')

    about_items = "".join(f'<a class="mm-link" href="{h}"><span>{ico(i, 14)}</span>{n}</a>' for h, i, n in [
        (f"{H}#about", "user", t("About me", "À propos")), (f"{H}#experience", "case", t("Experience", "Expérience")),
        (f"{H}#certs", "lab", t("Certifications &amp; education", "Certifications &amp; formation")), (f"{root + lp}cv.html", "case", t("Web CV", "CV web")),
        (f"{H}#contact", "mail", "Contact")])
    about = panel("about", t("About", "À propos"),
                  f'<div class="mm-col"><span class="mm-h">Tarek Medjoub</span><div class="mm-links one">{about_items}</div></div>',
                  f'<div class="mm-feature plain"><span class="mm-h">{t("In short", "En bref")}</span><b>{t("Former team leader of six, MBA in project management, based in Paris.", "Ancien chef d’une équipe de six, MBA en management de projet, basé à Paris.")}</b><span class="mm-cta"><a href="{root}{"assets/CV_Tarek_MEDJOUB.pdf" if lp else "assets/CV_Tarek_MEDJOUB_EN.pdf"}" download>{t("Download CV (PDF)", "Télécharger le CV (PDF)")} {ico("arrow", 14)}</a></span></div>')

    return exp + work + labs + toolkit + about


def utility_bar(x, en_href, fr_href, lang):
    t = x.t
    return f"""<div class="util">
  <div class="wrap">
    <span class="util-status"><span class="dot-ok"></span>{t('Open to Network, Security &amp; Cloud roles · Paris', 'Ouvert aux postes Réseaux, Sécurité &amp; Cloud · Paris')}</span>
    <span class="util-links">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      <span class="lang" role="group" aria-label="{t('Language', 'Langue')}">
        <a href="{en_href}" data-lang="en" hreflang="en"{' class="on" aria-current="true"' if lang == 'en' else ''}>EN</a>
        <a href="{fr_href}" data-lang="fr" hreflang="fr"{' class="on" aria-current="true"' if lang == 'fr' else ''}>FR</a>
      </span>
    </span>
  </div>
</div>"""


def footer(x, root, lp, home):
    from projects_data import PROJECTS
    from labs_data import LABS
    t = x.t
    H = "" if home else root + lp + "index.html"
    col = lambda title, links: f'<div class="fcol"><h4>{title}</h4>' + "".join(f'<a href="{h}">{n}</a>' for h, n in links) + "</div>"
    return f"""<footer class="fat">
  <div class="wrap">
    <div class="f-top">
      <div class="f-brand">
        <a href="{root + lp}index.html" class="brand"><span class="brand-mark" aria-hidden="true">TM</span><span class="brand-txt">Tarek Medjoub<small>{t('Network · Security · Cloud', 'Réseaux · Sécurité · Cloud')}</small></span></a>
        <p>{t('I design, secure and monitor multisite enterprise networks, from campus to cloud.', 'Je conçois, sécurise et supervise des réseaux d’entreprise multisites, du campus au cloud.')}</p>
        <a class="btn primary" href="{H}#contact">{t('Contact me', 'Me contacter')}</a>
      </div>
      {col(t('Expertise', 'Expertise'), [(f'{H}#expertise-{k}', t(*n)) for k, n, _ in EXPERTISE])}
      {col(t('Case studies', 'Études de cas'), [(f'{root + lp}projects/{p["id"]}.html', t(*p["title"])) for p in PROJECTS])}
      {col(t('Resources', 'Ressources'), [(f'{H}#resources', t('Resource center', 'Centre de ressources')), (f'{root + lp}labs/{LABS[0]["id"]}.html', t('Lab guides', 'Guides de lab')), (f'{root + lp}tools.html', t('Network toolkit', 'Outils réseau')), (f'{root + lp}cv.html', t('Web CV', 'CV web'))])}
      {col('Contact', [(f'mailto:{EMAIL}', EMAIL), (LINKEDIN, 'LinkedIn'), (f'{H}#contact', t('Send a message', 'Envoyer un message'))])}
    </div>
    <div class="f-bottom">
      <span>© <span class="yr">2026</span> Tarek Medjoub · Paris, France</span>
      <span>{t('Built and maintained by me · hosted on GitHub Pages', 'Conçu et maintenu par moi · hébergé sur GitHub Pages')}</span>
    </div>
  </div>
</footer>"""
