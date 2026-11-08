# Tarek MEDJOUB · Network, Security & Cloud Engineer

Personal portfolio: **https://tarekmjb.github.io/tmedjoub.github.io/**

Fortinet SD-WAN · multisite enterprise networks · IPsec/BGP · hybrid connectivity to Azure and AWS · Zabbix / PRTG / GLPI.

---

## What's inside

| Path | Content |
|---|---|
| `index.html` · `fr/index.html` | Homepage (EN / FR), with the interactive SD-WAN topology and live SLA graph |
| `projects/*.html` · `fr/projects/*.html` | 4 full case studies: SD-WAN, hybrid cloud, LAN, monitoring |
| `labs/*.html` · `fr/labs/*.html` | 10 EVE-NG lab guides: topology, configs, verification, break/fix |
| `cv.html` · `fr/cv.html` | Web CV, printable to PDF |
| `tools.html` · `fr/tools.html` | Network toolkit: subnet calculator, VLSM planner, wildcard & ACL helper, IPsec MTU/MSS |
| `assets/CV_Tarek_MEDJOUB*.pdf` | Designed PDF CVs (FR / EN) |
| `assets/css/main.css` | All styles (dark / light theme) |
| `assets/js/main.js` | Theme, navigation, interactive console, code copy, table of contents |
| `assets/js/topology.js` | Homepage SD-WAN simulation |
| `assets/js/tools.js` | Toolkit calculators (run in the browser) |
| `assets/img/` | Favicon and social preview image (`og-image.png`, 1200×630) |
| `404.html` | "Destination host unreachable" page |
| `sitemap.xml` · `robots.txt` | SEO |
| `_build/` | Python generator for every HTML page (ignored by GitHub Pages) |

## Editing content

All HTML pages are generated from the Python files in `_build/`, so the header, footer, navigation and both languages stay consistent.

```bash
cd _build
# edit the text in one of these files:
#   home.py           homepage (EN + FR side by side)
#   projects_data.py  case studies
#   labs_data.py      lab guides
#   tools.py          network toolkit page
#   build.py          web CV, 404, sitemap
python3 build.py      # rewrites the HTML pages in the repository root
```

Each text appears as a pair: `t('English text', 'Texte français')`.
Styles and scripts in `assets/` are edited directly; the build doesn't touch them.

**When you finish a lab** (screenshots, real outputs, `.unl` export): add them to the lab in `labs_data.py`, then change its "Publication status" items from `todo` to `ok` in `lab_sections()`.

## Publishing

GitHub Pages serves the `main` branch root. After a change:

```bash
git add -A
git commit -m "Update portfolio"
git push
```

The site updates within a minute or two.

## Interactive extras

- Press `/` or `Ctrl + K` anywhere to open the console. Try `help`, `whoami`, `open sdwan`, `lab bgp`, `ping tarek`, `cv web`.
- On the homepage, click any link in the topology (or "Fail ISP-1") to watch SD-WAN failover.

---

📧 tarek.medjoub@outlook.fr · 💼 [linkedin.com/in/tarek-medjoub](https://linkedin.com/in/tarek-medjoub) · 📍 Paris, France
