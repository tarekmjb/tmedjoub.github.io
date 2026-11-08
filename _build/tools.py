"""Network toolkit page: subnet calculator, VLSM planner, wildcard/ACL helper, IPsec MTU/MSS."""
from common import VER, L, layout


IC = {k: f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>' for k, d in {
    "subnet": "M3 6h18M3 12h18M3 18h18M9 3v18",
    "ipv6": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18",
    "vlsm": "M4 4h16v16H4zM4 12h16M12 12v8M16 12v8",
    "wildcard": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM9 12h6",
    "mss": "M3 12h4l3-8 4 16 3-8h4"}.items()}


def tools_page(lang):
    x = L(lang); t = x.t
    body = f"""
<section class="doc-band" id="top">
  <div class="wrap">
  <div class="crumbs"><a class="back-btn" href="index.html">← {t('Back to home', 'Retour à l’accueil')}</a><a href="index.html">{t('Home', 'Accueil')}</a><span class="sep">/</span>{t('Toolkit', 'Outils')}</div>
  <div class="doc-hero">
    <div class="kicker">{t('network toolkit', 'boîte à outils réseau')}</div>
    <h1>{t('Everyday network tools.', 'Outils réseau du quotidien.')}</h1>
    <p class="sum">{t('The calculators I reach for when designing and troubleshooting networks. Everything runs in your browser: nothing is sent anywhere.',
                     'Les calculateurs que j’utilise pour concevoir et dépanner des réseaux. Tout s’exécute dans votre navigateur : rien n’est envoyé.')}</p>
  </div>
  </div>
</section>
<div class="wrap">
  <div class="tk">
  <aside class="tk-side">
    <span class="tk-h">{t('Tools', 'Outils')}</span>
    <nav class="tool-tabs" role="tablist" aria-orientation="vertical" aria-label="{t('Tools', 'Outils')}">
      <a href="#subnet" role="tab" id="tab-subnet" aria-controls="subnet" class="on"><span class="tk-ico">{IC['subnet']}</span><span><b>{t('IPv4 subnet calculator', 'Calcul de sous-réseau IPv4')}</b><small>{t('Masks, ranges, all networks', 'Masques, plages, tous les réseaux')}</small></span></a>
      <a href="#ipv6" role="tab" id="tab-ipv6" aria-controls="ipv6"><span class="tk-ico">{IC['ipv6']}</span><span><b>{t('IPv6 calculator', 'Calcul IPv6')}</b><small>{t('Prefix, range, address type', 'Préfixe, plage, type d’adresse')}</small></span></a>
      <a href="#vlsm" role="tab" id="tab-vlsm" aria-controls="vlsm"><span class="tk-ico">{IC['vlsm']}</span><span><b>{t('VLSM planner', 'Planificateur VLSM')}</b><small>{t('Split a block by host needs', 'Découper un bloc selon les besoins')}</small></span></a>
      <a href="#wildcard" role="tab" id="tab-wildcard" aria-controls="wildcard"><span class="tk-ico">{IC['wildcard']}</span><span><b>{t('Wildcard &amp; ACL', 'Wildcard &amp; ACL')}</b><small>{t('Cisco &amp; FortiOS syntax', 'Syntaxe Cisco &amp; FortiOS')}</small></span></a>
      <a href="#mss" role="tab" id="tab-mss" aria-controls="mss"><span class="tk-ico">{IC['mss']}</span><span><b>IPsec MTU / MSS</b><small>{t('Tunnel overhead &amp; MSS', 'Surcoût tunnel &amp; MSS')}</small></span></a>
    </nav>
    <div class="tk-note"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>{t('Runs in your browser. Nothing is sent.', 'Exécuté dans votre navigateur. Rien n’est envoyé.')}</div>
  </aside>
  <div class="tk-main">
  <section class="tool tool-wide" id="subnet" role="tabpanel" aria-labelledby="tab-subnet">
    <div class="tool-in">
      <h2>{t('IPv4 subnet calculator', 'Calculateur de sous-réseau IPv4')}</h2>
      <p>{t('Pick a class to filter the masks, choose a subnet, enter an IP address. You can also paste <code>10.0.0.1/24</code> straight into the address field.',
            'Choisissez une classe pour filtrer les masques, sélectionnez un sous-réseau, saisissez une adresse IP. Vous pouvez aussi coller <code>10.0.0.1/24</code> directement dans le champ adresse.')}</p>
      <form class="calc-form" id="snForm" novalidate>
        <div class="fld fld-wide"><span class="fl">{t('Network class', 'Classe de réseau')}</span>
        <div class="radios" role="radiogroup" aria-label="{t('Network class', 'Classe de réseau')}">
          <label><input type="radio" name="snClass" value="any" checked> {t('Any', 'Toutes')}</label>
          <label><input type="radio" name="snClass" value="A"> A</label>
          <label><input type="radio" name="snClass" value="B"> B</label>
          <label><input type="radio" name="snClass" value="C"> C</label>
        </div></div>
        <div class="fld"><label class="fl" for="snMask">{t('Subnet', 'Sous-réseau')}</label>
        <select id="snMask" class="tin"></select></div>
        <div class="fld"><label class="fl" for="snIn">{t('IP address', 'Adresse IP')}</label>
        <input id="snIn" class="tin" value="10.10.20.37" spellcheck="false" autocomplete="off" inputmode="decimal"></div>
        <div class="ex">{t('Try', 'Essayez')}: <button type="button" data-ex="snIn">192.168.1.130/25</button><button type="button" data-ex="snIn">172.16.5.4/22</button><button type="button" data-ex="snIn">10.255.1.2/30</button><button type="button" data-ex="snIn">82.65.236.174/30</button></div>
        <div class="calc-btns"><button type="submit" class="btn primary">{t('Calculate', 'Calculer')}</button><button type="button" class="btn" data-clear="snForm">{t('Clear', 'Effacer')}</button></div>
      </form>
    </div>
    <div class="tool-out" id="snOut" aria-live="polite"></div>
    <div class="tool-full" id="snNets"></div>
  </section>

  <section class="tool tool-wide" id="ipv6" role="tabpanel" aria-labelledby="tab-ipv6">
    <div class="tool-in">
      <h2>{t('IPv6 subnet calculator', 'Calculateur de sous-réseau IPv6')}</h2>
      <p>{t('Enter an IPv6 address (compressed or full) and a prefix length.', 'Saisissez une adresse IPv6 (compressée ou complète) et une longueur de préfixe.')}</p>
      <form id="v6Form" novalidate>
      <div class="fld"><label class="fl" for="v6Pfx">{t('Prefix length', 'Longueur de préfixe')}</label>
      <select id="v6Pfx" class="tin"></select></div>
      <div class="fld fld-2">
<label class="fl" for="v6In">{t('IP address', 'Adresse IP')}</label>
      <input id="v6In" class="tin" value="2001:db8:85a3::8a2e:370:7334" spellcheck="false" autocomplete="off"></div>
      <div class="ex">{t('Try', 'Essayez')}: <button type="button" data-ex="v6In">fe80::1ff:fe23:4567:890a</button><button type="button" data-ex="v6In">fd12:3456:789a:1::1</button><button type="button" data-ex="v6In">2a01:cb00:1234::/48</button></div>
      <div class="calc-btns"><button type="submit" class="btn primary">{t('Calculate', 'Calculer')}</button><button type="button" class="btn" data-clear="v6Form">{t('Clear', 'Effacer')}</button></div>
      </form>
    </div>
    <div class="tool-out" id="v6Out" aria-live="polite"></div>
  </section>

  <section class="tool" id="vlsm" role="tabpanel" aria-labelledby="tab-vlsm">
    <div class="tool-in">
      <h2>{t('VLSM planner', 'Planificateur VLSM')}</h2>
      <p>{t('One segment per line: <code>name hosts</code>. Largest segments are placed first to avoid gaps.', 'Un segment par ligne : <code>nom hôtes</code>. Les plus grands segments sont placés en premier pour éviter les trous.')}</p>
      <form id="vlForm" novalidate>
      <div class="fld"><label class="fl" for="vlBase">{t('Address block', 'Bloc d’adresses')}</label>
      <input id="vlBase" class="tin" value="10.10.0.0/22" spellcheck="false" autocomplete="off"></div>
      <div class="fld fld-wide"><label class="fl" for="vlReq">{t('Segments', 'Segments')}</label>
      <textarea id="vlReq" class="tin" rows="7" spellcheck="false">Users 200
Voice 120
Servers 50
IoT 30
Management 14
WAN-link 2
WAN-link-2 2</textarea></div>
      <div class="calc-btns"><button type="submit" class="btn primary">{t('Calculate', 'Calculer')}</button><button type="button" class="btn" data-clear="vlForm">{t('Clear', 'Effacer')}</button></div>
      </form>
    </div>
    <div class="tool-out" id="vlOut" aria-live="polite"></div>
  </section>

  <section class="tool" id="wildcard" role="tabpanel" aria-labelledby="tab-wildcard">
    <div class="tool-in">
      <h2>{t('Wildcard &amp; ACL helper', 'Assistant wildcard &amp; ACL')}</h2>
      <p>{t('Convert between prefix, mask and wildcard, and get ready-to-paste ACL and object syntax.', 'Conversion entre préfixe, masque et wildcard, avec la syntaxe ACL et objet prête à coller.')}</p>
      <form id="wcForm" novalidate>
      <div class="fld"><label class="fl" for="wcIn">{t('Network', 'Réseau')}</label>
      <input id="wcIn" class="tin" value="192.168.30.0/24" spellcheck="false" autocomplete="off"></div>
      <div class="fld"><label class="fl" for="wcAct">{t('Action', 'Action')}</label>
      <select id="wcAct" class="tin"><option>permit</option><option>deny</option></select></div>
      <div class="calc-btns"><button type="submit" class="btn primary">{t('Calculate', 'Calculer')}</button><button type="button" class="btn" data-clear="wcForm">{t('Clear', 'Effacer')}</button></div>
      </form>
    </div>
    <div class="tool-out" id="wcOut" aria-live="polite"></div>
  </section>

  <section class="tool" id="mss" role="tabpanel" aria-labelledby="tab-mss">
    <div class="tool-in">
      <h2>IPsec MTU / MSS</h2>
      <p>{t('Estimate tunnel overhead and the <code>ip mtu</code> / <code>adjust-mss</code> values to configure. Worst-case padding is assumed.', 'Estimation de l’en-tête du tunnel et des valeurs <code>ip mtu</code> / <code>adjust-mss</code> à configurer. Le pire cas de bourrage est pris en compte.')}</p>
      <form id="msForm" novalidate>
      <div class="fld"><label class="fl" for="msMtu">{t('Physical MTU', 'MTU physique')}</label>
      <input id="msMtu" class="tin" type="number" value="1500" min="576" max="9216"></div>
      <div class="fld"><label class="fl" for="msEnc">{t('Encryption / integrity', 'Chiffrement / intégrité')}</label>
      <select id="msEnc" class="tin">
        <option value="cbc256">AES-256-CBC + SHA-256</option>
        <option value="cbc1">AES-256-CBC + SHA-1</option>
        <option value="gcm">AES-256-GCM</option>
      </select></div>
      <div class="checks">
        <label><input type="checkbox" id="msNat"> NAT-T (UDP 4500)</label>
        <label><input type="checkbox" id="msGre"> GRE over IPsec</label>
        <label><input type="checkbox" id="msPpp"> PPPoE</label>
      </div>
      <div class="calc-btns"><button type="submit" class="btn primary">{t('Calculate', 'Calculer')}</button><button type="button" class="btn" data-clear="msForm">{t('Clear', 'Effacer')}</button></div>
      </form>
    </div>
    <div class="tool-out" id="msOut" aria-live="polite"></div>
  </section>
  </div>
  </div>
</div>
"""
    root = "../" if lang == "fr" else ""
    return layout(lang, "tools.html",
                  t("Network toolkit · Tarek MEDJOUB", "Outils réseau · Tarek MEDJOUB"),
                  t("Free network tools: IPv4 and IPv6 subnet calculators, VLSM planner, wildcard & ACL helper, IPsec MTU/MSS calculator.",
                    "Outils réseau gratuits : calculateurs de sous-réseau IPv4 et IPv6, planificateur VLSM, assistant wildcard & ACL, calcul MTU/MSS IPsec."),
                  body, extra_js=f'<script src="{root}assets/js/tools.js?v={VER}" defer></script>')
