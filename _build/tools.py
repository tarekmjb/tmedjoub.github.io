"""Network toolkit page: subnet calculator, VLSM planner, wildcard/ACL helper, IPsec MTU/MSS."""
from common import L, layout


def tools_page(lang):
    x = L(lang); t = x.t
    body = f"""
<div class="wrap" id="top">
  <div class="crumbs"><a class="back-btn" href="index.html">← {t('Back to home', 'Retour à l’accueil')}</a><a href="index.html">tarek@medjoub</a><span class="sep">/</span>{t('toolkit', 'outils')}</div>
  <div class="doc-hero">
    <div class="kicker">{t('network toolkit', 'boîte à outils réseau')}</div>
    <h1>{t('Everyday network tools.', 'Outils réseau du quotidien.')}</h1>
    <p class="sum">{t('The calculators I reach for when designing and troubleshooting networks. Everything runs in your browser: nothing is sent anywhere.',
                     'Les calculateurs que j’utilise pour concevoir et dépanner des réseaux. Tout s’exécute dans votre navigateur : rien n’est envoyé.')}</p>
    <div class="tool-tabs" role="tablist">
      <a href="#subnet" class="on">{t('Subnet calculator', 'Calcul de sous-réseau')}</a>
      <a href="#vlsm">{t('VLSM planner', 'Planificateur VLSM')}</a>
      <a href="#wildcard">{t('Wildcard &amp; ACL', 'Wildcard &amp; ACL')}</a>
      <a href="#mss">IPsec MTU / MSS</a>
    </div>
  </div>

  <section class="tool" id="subnet">
    <div class="tool-in">
      <h2>{t('Subnet calculator', 'Calcul de sous-réseau')}</h2>
      <p>{t('Enter an address with a prefix or a mask.', 'Saisissez une adresse avec un préfixe ou un masque.')}</p>
      <label class="fl" for="snIn">{t('Address', 'Adresse')}</label>
      <input id="snIn" class="tin" value="10.10.20.37/26" spellcheck="false" autocomplete="off">
      <div class="ex">{t('Try', 'Essayez')}: <button type="button" data-ex="snIn">192.168.1.130/25</button><button type="button" data-ex="snIn">172.16.5.4 255.255.252.0</button><button type="button" data-ex="snIn">10.255.1.2/30</button></div>
    </div>
    <div class="tool-out" id="snOut" aria-live="polite"></div>
  </section>

  <section class="tool" id="vlsm">
    <div class="tool-in">
      <h2>{t('VLSM planner', 'Planificateur VLSM')}</h2>
      <p>{t('One segment per line: <code>name hosts</code>. Largest segments are placed first to avoid gaps.', 'Un segment par ligne : <code>nom hôtes</code>. Les plus grands segments sont placés en premier pour éviter les trous.')}</p>
      <label class="fl" for="vlBase">{t('Address block', 'Bloc d’adresses')}</label>
      <input id="vlBase" class="tin" value="10.10.0.0/22" spellcheck="false" autocomplete="off">
      <label class="fl" for="vlReq">{t('Segments', 'Segments')}</label>
      <textarea id="vlReq" class="tin" rows="7" spellcheck="false">Users 200
Voice 120
Servers 50
IoT 30
Management 14
WAN-link 2
WAN-link-2 2</textarea>
    </div>
    <div class="tool-out" id="vlOut" aria-live="polite"></div>
  </section>

  <section class="tool" id="wildcard">
    <div class="tool-in">
      <h2>{t('Wildcard &amp; ACL helper', 'Assistant wildcard &amp; ACL')}</h2>
      <p>{t('Convert between prefix, mask and wildcard, and get ready-to-paste ACL and object syntax.', 'Conversion entre préfixe, masque et wildcard, avec la syntaxe ACL et objet prête à coller.')}</p>
      <label class="fl" for="wcIn">{t('Network', 'Réseau')}</label>
      <input id="wcIn" class="tin" value="192.168.30.0/24" spellcheck="false" autocomplete="off">
      <label class="fl" for="wcAct">{t('Action', 'Action')}</label>
      <select id="wcAct" class="tin"><option>permit</option><option>deny</option></select>
    </div>
    <div class="tool-out" id="wcOut" aria-live="polite"></div>
  </section>

  <section class="tool" id="mss">
    <div class="tool-in">
      <h2>IPsec MTU / MSS</h2>
      <p>{t('Estimate tunnel overhead and the <code>ip mtu</code> / <code>adjust-mss</code> values to configure. Worst-case padding is assumed.', 'Estimation de l’en-tête du tunnel et des valeurs <code>ip mtu</code> / <code>adjust-mss</code> à configurer. Le pire cas de bourrage est pris en compte.')}</p>
      <label class="fl" for="msMtu">{t('Physical MTU', 'MTU physique')}</label>
      <input id="msMtu" class="tin" type="number" value="1500" min="576" max="9216">
      <label class="fl" for="msEnc">{t('Encryption / integrity', 'Chiffrement / intégrité')}</label>
      <select id="msEnc" class="tin">
        <option value="cbc256">AES-256-CBC + SHA-256</option>
        <option value="cbc1">AES-256-CBC + SHA-1</option>
        <option value="gcm">AES-256-GCM</option>
      </select>
      <div class="checks">
        <label><input type="checkbox" id="msNat"> NAT-T (UDP 4500)</label>
        <label><input type="checkbox" id="msGre"> GRE over IPsec</label>
        <label><input type="checkbox" id="msPpp"> PPPoE</label>
      </div>
    </div>
    <div class="tool-out" id="msOut" aria-live="polite"></div>
  </section>
</div>
"""
    root = "../" if lang == "fr" else ""
    return layout(lang, "tools.html",
                  t("Network toolkit · Tarek MEDJOUB", "Outils réseau · Tarek MEDJOUB"),
                  t("Free network tools: subnet calculator, VLSM planner, wildcard & ACL helper, IPsec MTU/MSS calculator.",
                    "Outils réseau gratuits : calcul de sous-réseau, planificateur VLSM, assistant wildcard & ACL, calcul MTU/MSS IPsec."),
                  body, extra_js=f'<script src="{root}assets/js/tools.js" defer></script>')
