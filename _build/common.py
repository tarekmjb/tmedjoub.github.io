"""Shared layout + helpers for the static site generator."""
import html as _html

SITE = "https://tarekmjb.github.io/tmedjoub.github.io/"
EMAIL = "tarek.medjoub@outlook.fr"
LINKEDIN = "https://linkedin.com/in/tarek-medjoub"


def esc(s):
    return _html.escape(s, quote=True)


class L:
    """Language context. t(en, fr) picks the right string."""

    def __init__(self, lang):
        self.lang = lang

    def t(self, en, fr):
        return en if self.lang == "en" else fr


def out_path(lang, path):
    return ("fr/" if lang == "fr" else "") + path


def root_of(lang, path):
    return "../" * out_path(lang, path).count("/")


HEAD_THEME = (
    "<script>(function(){try{var t=localStorage.getItem('tm-theme');"
    "if(t!=='dark')t='light';"
    "document.documentElement.dataset.theme=t;}catch(e){}})();</script>"
)

FAVICON = "assets/img/favicon.svg"


def layout(lang, path, title, desc, body, *, home=False, doc=False, extra_js="", jsonld="", noindex=False, alt_path=None):
    x = L(lang)
    t = x.t
    root = root_of(lang, path)
    lp = "fr/" if lang == "fr" else ""
    alt_path = alt_path or path
    en_href = root + alt_path if lang == "en" else root + alt_path
    fr_href = root + "fr/" + alt_path
    if lang == "en":
        en_href, fr_href = root + path, root + "fr/" + alt_path
    else:
        en_href, fr_href = root + alt_path, root + "fr/" + path
    canon = SITE + out_path(lang, path)
    home_href = "" if home else root + lp + "index.html"

    def a(anchor):
        return f"{home_href}#{anchor}"

    nav_items = [
        ("about", t("About", "À propos")),
        ("services", "Services"),
        ("stack", t("Skills", "Compétences")),
        ("experience", t("Experience", "Expérience")),
        ("projects", t("Projects", "Projets")),
        ("labs", "Labs"),
        ("certs", t("Certs", "Certifs")),
        ("resume", "CV"),
        ("contact", "Contact"),
    ]
    nav = "\n".join(f'      <a href="{a(i)}">{lbl}</a>' for i, lbl in nav_items)
    nav += f'\n      <a href="{root + lp}tools.html" class="nav-tools">{t("Toolkit", "Outils")}</a>'
    og_img = SITE + "assets/img/og-image.png"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light" data-root="{root}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Tarek Medjoub">
{robots}
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{SITE}{alt_path if lang == 'fr' else path}">
<link rel="alternate" hreflang="fr" href="{SITE}fr/{path if lang == 'fr' else alt_path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{alt_path if lang == 'fr' else path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_GB'}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" type="image/svg+xml" href="{root}{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/main.css">
{HEAD_THEME}
{jsonld}
</head>
<body>
<a class="skip" href="#main">{t('Skip to content', 'Aller au contenu')}</a>
{'<div class="progress" aria-hidden="true"></div>' if doc else ''}
<header class="bar">
  <div class="wrap">
    <a href="{root + lp + 'index.html' if not home else '#top'}" class="brand" aria-label="Tarek Medjoub · {t('home', 'accueil')}"><span class="brand-mark" aria-hidden="true">TM</span><span class="brand-txt">Tarek Medjoub<small>{t('Network · Security · Cloud', 'Réseaux · Sécurité · Cloud')}</small></span></a>
    <nav class="links" id="nav" aria-label="{t('Main', 'Principale')}">
{nav}
    </nav>
    <div class="tools">
      <button class="btn-ico menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false">☰</button>
      <button class="btn-ico" id="themeBtn" title="{t('Toggle theme', 'Changer de thème')}" aria-label="{t('Toggle light/dark theme', 'Basculer thème clair/sombre')}"><svg class="i-moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="i-sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
      <div class="lang" role="group" aria-label="{t('Language', 'Langue')}">
        <a href="{en_href}" data-lang="en" hreflang="en"{' class="on" aria-current="true"' if lang == 'en' else ''}>EN</a>
        <a href="{fr_href}" data-lang="fr" hreflang="fr"{' class="on" aria-current="true"' if lang == 'fr' else ''}>FR</a>
      </div>
    </div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer>
  <div class="wrap">
    <span>© <span class="yr">2026</span> Tarek Medjoub · Paris · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <span class="foot-links"><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{root + lp}cv.html">CV</a><a href="{root + lp}tools.html">{t('Toolkit', 'Outils')}</a></span>
  </div>
</footer>

<button class="totop" id="toTop" type="button" aria-label="{t('Back to top', 'Retour en haut')}" title="{t('Back to top', 'Retour en haut')}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg><span>{t('top', 'haut')}</span></button>
<button class="fab" id="fab" aria-label="{t('Open interactive console', 'Ouvrir la console interactive')}" title="{t('Console (/ or Ctrl+K)', 'Console (/ ou Ctrl+K)')}"><b>&gt;_</b></button>
<div class="con-back" id="conBack" role="dialog" aria-modal="true" aria-label="{t('Interactive console', 'Console interactive')}">
  <div class="con">
    <div class="term-head"><div class="dots"><i></i><i></i><i></i></div><span>tarek@medjoub · {t('interactive console', 'console interactive')}</span><span class="con-hint">{t('esc to close', 'échap pour fermer')}</span><button class="con-x" id="conClose" type="button" aria-label="{t('Close console', 'Fermer la console')}" title="{t('Close', 'Fermer')}">✕</button></div>
    <div class="con-out" id="conOut"></div>
    <div class="con-sug" id="conSug"></div>
    <div class="con-in"><span class="p">guest@portfolio:~$</span><input id="conIn" autocomplete="off" spellcheck="false" aria-label="{t('Command', 'Commande')}"></div>
  </div>
</div>
<div class="toast" id="toast" role="status"></div>
<script src="{root}assets/js/main.js" defer></script>
{extra_js}
</body>
</html>
"""


# ───────── content helpers ─────────

def code(title, text, lang_label=""):
    return f"""<div class="code"><div class="ch"><span>{esc(title)}</span><button type="button">copy</button></div><pre>{esc(text.strip(chr(10)))}</pre></div>"""


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="t"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def bullets(items):
    return '<ul class="bul">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def steps(items):
    return '<div class="steps">' + "".join(f'<div class="step"><div><h4>{h}</h4><p>{p}</p></div></div>' for h, p in items) + "</div>"


def dcards(items):
    return '<div class="dgrid">' + "".join(
        f'<div class="dcard">{f"<span class=why>{w}</span>" if w else ""}<b>{h}</b><span>{p}</span></div>' for w, h, p in items) + "</div>"


def note(txt):
    return f'<div class="note"><div>{txt}</div></div>'


def topo_svg(nodes, links, w=640, h=300, zones=(), caption=""):
    """nodes: (id, label, sub, x, y, kind) ; links: (a, b, label, cls) ; zones: (x,y,w,h,label)"""
    pos = {n[0]: n for n in nodes}
    out = [f'<figure class="figure topo-fig"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(caption)}">']
    for zx, zy, zw, zh, zl in zones:
        out.append(f'<rect class="zone" x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="10"/><text class="zt" x="{zx + 10}" y="{zy + 16}">{esc(zl)}</text>')
    for a, b, lbl, cls in links:
        A, B = pos[a], pos[b]
        out.append(f'<line class="lk {cls}" x1="{A[3]}" y1="{A[4]}" x2="{B[3]}" y2="{B[4]}"/>')
        if lbl:
            mx, my = (A[3] + B[3]) / 2, (A[4] + B[4]) / 2
            out.append(f'<text class="lt" x="{mx + 6:.0f}" y="{my - 5:.0f}">{esc(lbl)}</text>')
    for nid, lbl, sub, x, y, kind in nodes:
        bw = max(78, 8 * max(len(lbl), int(len(sub) * .75)) + 18)
        out.append(f'<g class="nd {kind}" transform="translate({x - bw / 2:.0f},{y - 17})"><rect width="{bw}" height="34" rx="6"/>'
                   f'<text x="9" y="15">{esc(lbl)}</text><text class="s" x="9" y="27">{esc(sub)}</text></g>')
    out.append("</svg>")
    if caption:
        out.append(f"<figcaption>{esc(caption)}</figcaption>")
    out.append("</figure>")
    return "".join(out)


def doc_page(x, *, crumbs, kicker, title, summary, metas, kpis, sections, pn, status=None, back=None):
    """Generic case-study / lab page body. sections: list of (id, toc_label, html)."""
    t = x.t
    crumb = '<span class="sep">/</span>'.join(crumbs)
    meta = "".join(f'<span class="meta">{k}<b>{v}</b></span>' for k, v in metas)
    kp = ""
    if kpis:
        kp = '<div class="kpis">' + "".join(f'<div class="kpi"><b>{a}</b><span>{b}</span></div>' for a, b in kpis) + "</div>"
    toc = "".join(f'<a href="#{i}">{lbl}</a>' for i, lbl, _ in sections)
    secs = "".join(f'<section id="{i}">{h}</section>' for i, _, h in sections)
    st = f'<div style="margin-top:14px">{status}</div>' if status else ""
    pnh = ""
    if pn:
        (pl, ph), (nl, nh) = pn
        pnh = (f'<div class="pn"><a href="{ph}"><small>← {t("previous", "précédent")}</small><span>{pl}</span></a>'
               f'<a class="r" href="{nh}"><small>{t("next", "suivant")} →</small><span>{nl}</span></a></div>')
    back_top = back_end = ""
    if back:
        bh, bl = back
        back_top = f'<a class="back-btn" href="{bh}">← {bl}</a>'
        back_end = (f'<div class="end-nav"><a class="back-btn" href="{bh}">← {bl}</a>'
                    f'<a class="back-btn" href="#top" data-top>↑ {t("Back to top", "Retour en haut")}</a></div>')
    return f"""
<div class="wrap" id="top">
  <div class="crumbs">{back_top}{crumb}</div>
  <div class="doc-hero">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="sum">{summary}</p>
    {st}
    <div class="meta-row">{meta}</div>
    {kp}
  </div>
  <div class="doc">
    <nav class="toc" aria-label="{t('On this page', 'Sur cette page')}"><b>{t('ON THIS PAGE', 'SUR CETTE PAGE')}</b>{toc}</nav>
    <div class="doc-body">{secs}{pnh}{back_end}</div>
  </div>
</div>
"""
