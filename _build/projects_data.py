"""Case-study content. Each page builder receives an L() language context."""
from common import code, table, bullets, steps, dcards, note, topo_svg

PROJECTS = [
    dict(id="sdwan", tagline="Fortinet · SD-WAN · BGP", kind=("production + lab", "production + lab"),
         title=("SD-WAN Enterprise Migration", "Migration SD-WAN d’entreprise"),
         card=("Moved a four-site enterprise from MPLS and static routes to a hub-and-spoke Fortinet SD-WAN: two ISPs per site, IPsec IKEv2 / AES-256 and BGP/OSPF. Validated in EVE-NG before cutover.",
               "Passage d’une entreprise de quatre sites du MPLS et des routes statiques à un SD-WAN Fortinet en étoile : deux FAI par site, IPsec IKEv2 / AES-256 et BGP/OSPF. Validé sous EVE-NG avant la bascule."),
         facts=[("4", ("sites", "sites")), ("2×", ("ISP / site", "FAI / site")), ("≈1.5s", ("lab failover", "bascule en lab"))],
         chips=["FortiGate", "IPsec", "BGP", "OSPF"]),
    dict(id="hybrid-cloud", tagline="FortiGate · Azure · AWS", kind=("lab", "lab"),
         title=("Hybrid Cloud Architecture", "Architecture cloud hybride"),
         card=("An on-premises FortiGate connected to Azure VPN Gateway and AWS Transit Gateway with route-based IPsec, BGP route exchange, strict prefix filtering and centralised PRTG monitoring.",
               "Un FortiGate local relié à Azure VPN Gateway et AWS Transit Gateway en IPsec route-based, avec échange BGP, filtrage strict des préfixes et supervision PRTG centralisée."),
         facts=[("2", ("clouds", "clouds")), ("3", ("BGP peers", "pairs BGP")), ("0", ("static routes to cloud", "route statique vers le cloud"))],
         chips=["Azure", "AWS", "IPsec", "BGP", "PRTG"]),
    dict(id="lan-optimization", tagline="VLAN · OSPF · HSRP · ACL", kind=("design + lab", "conception + lab"),
         title=("LAN Architecture Optimisation", "Optimisation de l’architecture LAN"),
         card=("Replaced a flat /16 network (800+ hosts in one broadcast domain) with a 3-tier core/distribution/access design: VLAN segmentation, OSPF, HSRP gateways, ACLs and SNMPv3.",
               "Remplacement d’un réseau à plat en /16 (plus de 800 hôtes dans un seul domaine de diffusion) par une architecture 3 couches : VLAN, OSPF, passerelles HSRP, ACL et SNMPv3."),
         facts=[("3", ("tiers", "couches")), ("/16 → /24", ("broadcast domains", "domaines de diffusion")), ("HSRP", ("gateway HA", "passerelle HA"))],
         chips=["VLAN", "OSPF", "HSRP", "ACL", "SNMPv3"]),
    dict(id="monitoring-stack", tagline="Zabbix · PRTG · GLPI", kind=("operations", "exploitation"),
         title=("Monitoring & Alerting Stack", "Supervision & alerting"),
         card=("Zabbix SNMPv3 polling, severity-based triggers and automatic GLPI tickets, with NOC dashboards. Every alert becomes a tracked incident instead of an email nobody reads.",
               "Collecte SNMPv3 Zabbix, déclencheurs par niveau de sévérité et tickets GLPI automatiques, avec tableaux de bord NOC. Chaque alerte devient un incident suivi, pas un e-mail ignoré."),
         facts=[],
         chips=["Zabbix", "PRTG", "SNMPv3", "GLPI"]),
]


# ═════════════════════════ SD-WAN ═════════════════════════
def sdwan(x):
    t = x.t
    topo = topo_svg(
        [("A", "FG-SITE-A", "FG-100F · AS65002", 110, 50, "fw"),
         ("B", "FG-SITE-B", "FG-100F · AS65003", 110, 150, "fw"),
         ("C", "FG-SITE-C", "FG-60F · AS65004", 110, 250, "fw"),
         ("I1", "ISP-1", t("primary", "principal"), 300, 90, "cl"),
         ("I2", "ISP-2", t("backup", "secours"), 300, 210, "cl"),
         ("HQ", "FG-HQ (hub)", "FG-200E · AS65001", 490, 150, "rt"),
         ("FM", "FortiManager", t("mgmt VLAN", "VLAN mgmt"), 600, 60, "sv"),
         ("FA", "FortiAnalyzer", t("90-day logs", "logs 90 j"), 600, 240, "sv")],
        [("A", "I1", "", "h"), ("B", "I1", "", "h"), ("C", "I1", "", "h"),
         ("A", "I2", "", ""), ("B", "I2", "", ""), ("C", "I2", "", ""),
         ("I1", "HQ", "100M", "h"), ("I2", "HQ", "50M", ""), ("HQ", "FM", "", "t"), ("HQ", "FA", "", "t")],
        w=680, h=300,
        caption=t("Hub-and-spoke overlay: two IPsec tunnels per spoke (one per ISP), BGP over each tunnel, OSPF towards the LANs.",
                  "Overlay en étoile : deux tunnels IPsec par agence (un par FAI), BGP sur chaque tunnel, OSPF vers les LAN."))
    ftl = f"""<div class="ftl">
  <div class="mono" style="font-size:12px;color:var(--muted)">{t('Failover timeline: ISP-1 failure at Site A (EVE-NG lab)', 'Chronologie de bascule : panne ISP-1 sur le site A (lab EVE-NG)')}</div>
  <div class="ftl-track"><div class="ftl-line"></div>
    <div class="ftl-pt" style="left:0%;--c:var(--red)"><i></i><b>t = 0 s</b></div>
    <div class="ftl-pt" style="left:33.3%;--c:var(--red)"><i></i><b>0.5 s</b></div>
    <div class="ftl-pt" style="left:66.6%;--c:var(--amber)"><i></i><b>1.0 s</b></div>
    <div class="ftl-pt" style="left:100%;--c:var(--green)"><i></i><b>1.5 s</b></div>
  </div>
  <div class="ftl-legend">
    <div style="--c:var(--red)"><b>0 s</b>{t('ISP-1 link fails', 'Le lien ISP-1 tombe')}</div>
    <div style="--c:var(--red)"><b>0.5 s</b>{t('First probe lost', 'Première sonde perdue')}</div>
    <div style="--c:var(--amber)"><b>1.0 s</b>{t('Packet loss over the SLA threshold', 'Perte au-dessus du seuil SLA')}</div>
    <div style="--c:var(--green)"><b>1.5 s</b>{t('3rd failed probe: member marked dead, traffic on ISP-2', '3ᵉ sonde perdue : membre déclaré mort, trafic sur ISP-2')}</div>
  </div>
  <div class="ftl-cmp">
    <div style="--c:var(--red)"><span>{t('Before: static routes', 'Avant : routes statiques')}</span><b>3–5 min</b><div class="ftl-bar"><i style="width:100%"></i></div></div>
    <div style="--c:var(--green)"><span>{t('After: SD-WAN SLA steering', 'Après : orientation SLA SD-WAN')}</span><b>≈1.5 s</b><div class="ftl-bar"><i style="width:1.5%"></i></div></div>
  </div>
</div>"""

    sections = [
        ("overview", t("Context", "Contexte"), f"""
<h2>{t('Context &amp; objectives', 'Contexte &amp; objectifs')}</h2>
{note(t('Configurations are sanitised and simplified for publication. Failover times are <strong>lab measurements</strong> taken in EVE-NG with FortiGate 7.4 VMs.',
        'Les configurations sont anonymisées et simplifiées pour publication. Les temps de bascule sont des <strong>mesures de lab</strong> réalisées sous EVE-NG avec des VM FortiGate 7.4.'))}
<p>{t('The company connected its sites with a legacy WAN: MPLS plus static routes. When a link failed, traffic stayed black-holed until the static route was changed, typically <strong>3 to 5 minutes</strong>. There was no visibility per application and part of the MPLS traffic was unencrypted.',
      'L’entreprise reliait ses sites par un WAN historique : MPLS et routes statiques. En cas de panne, le trafic restait bloqué jusqu’à la modification de la route statique, soit <strong>3 à 5 minutes</strong>. Aucune visibilité par application, et une partie du trafic MPLS circulait en clair.')}</p>
<h3>{t('Objectives', 'Objectifs')}</h3>
{bullets([t('Faster, automatic failover between links.', 'Une bascule rapide et automatique entre les liens.'),
          t('Application-aware steering (VoIP, bulk data, business apps).', 'Une orientation du trafic par application (VoIP, gros volumes, applications métier).'),
          t('Encrypt all intersite traffic, replacing clear-text MPLS segments.', 'Chiffrer tout le trafic inter-sites, à la place des segments MPLS en clair.'),
          t('Reduce bandwidth cost by sending bulk traffic over a cheaper second ISP.', 'Réduire les coûts en envoyant les gros volumes sur un second FAI moins cher.'),
          t('Central management and logs (FortiManager, FortiAnalyzer).', 'Gestion et journaux centralisés (FortiManager, FortiAnalyzer).')])}"""),
        ("architecture", "Architecture", f"""
<h2>Architecture</h2>
<p>{t('A <strong>hub-and-spoke</strong> overlay: the HQ FortiGate is the hub, each branch is a spoke with <strong>two IPsec tunnels</strong> to HQ, one per ISP. BGP runs over each tunnel, so routing follows tunnel health; OSPF carries the routes into each LAN.',
      'Un overlay <strong>en étoile</strong> : le FortiGate du siège est le hub, chaque agence est un spoke avec <strong>deux tunnels IPsec</strong> vers le siège, un par FAI. BGP tourne dans chaque tunnel, le routage suit donc l’état des tunnels ; OSPF propage les routes dans chaque LAN.')}</p>
{topo}
{table([t('Site', 'Site'), t('Device', 'Équipement'), t('Role', 'Rôle'), 'ISP-1 / ISP-2', 'AS', 'LAN'],
       [['HQ', 'FG-200E', t('SD-WAN hub', 'Hub SD-WAN'), '100 / 50 Mb/s', '65001', '10.1.0.0/16'],
        ['Site A', 'FG-100F', 'Spoke', '50 / 30 Mb/s', '65002', '10.2.0.0/16'],
        ['Site B', 'FG-100F', 'Spoke', '50 / 30 Mb/s', '65003', '10.3.0.0/16'],
        ['Site C', 'FG-60F', 'Spoke', '20 / 20 Mb/s', '65004', '10.4.0.0/16']])}
<h3>{t('Overlay addressing (Site A example)', 'Adressage overlay (exemple site A)')}</h3>
{table([t('Tunnel', 'Tunnel'), t('Subnet', 'Sous-réseau'), 'HQ', 'Spoke', t('BGP preference', 'Préférence BGP')],
       [['HQ-ISP1', '10.255.1.0/30', '.1', '.2', 'local-pref 200 (' + t('preferred', 'préféré') + ')'],
        ['HQ-ISP2', '10.255.2.0/30', '.1', '.2', 'local-pref 100 (' + t('backup', 'secours') + ')']])}"""),
        ("design", t("Design choices", "Choix de conception"), f"""
<h2>{t('Design choices', 'Choix de conception')}</h2>
{dcards([(t('why hub-and-spoke', 'pourquoi en étoile'), t('Central inspection', 'Inspection centralisée'), t('All spoke internet traffic is backhauled through HQ for IPS and application control. One policy point, one log source.', 'Tout le trafic internet des agences repasse par le siège pour l’IPS et le contrôle applicatif : un seul point de politique, une seule source de logs.')),
          (t('why BGP over IPsec', 'pourquoi BGP sur IPsec'), t('Dynamic routing per tunnel', 'Routage dynamique par tunnel'), t('A failed tunnel withdraws its routes on its own. No static routes to update, and new sites only need a new neighbor.', 'Un tunnel tombé retire ses routes tout seul. Aucune route statique à modifier, et un nouveau site ne demande qu’un voisin de plus.')),
          (t('why SLA probes', 'pourquoi des sondes SLA'), t('Performance, not just link state', 'La performance, pas seulement l’état du lien'), t('A link can be up but unusable. Probes measure latency, jitter and loss, and steer each application to the link that meets its SLA.', 'Un lien peut être actif mais inutilisable. Les sondes mesurent latence, gigue et perte, et orientent chaque application vers le lien qui respecte son SLA.')),
          (t('why BFD', 'pourquoi BFD'), t('Stable BGP on small links', 'BGP stable sur les petits liens'), t('Short BGP timers caused flaps on 20 Mb/s links. BFD detects failures fast while BGP keeps conservative 10 s / 30 s timers.', 'Des timers BGP courts provoquaient des flaps sur les liens 20 Mb/s. BFD détecte vite les pannes, BGP garde des timers prudents de 10 s / 30 s.'))])}"""),
        ("implementation", t("Implementation", "Mise en œuvre"), f"""
<h2>{t('Implementation', 'Mise en œuvre')}</h2>
{steps([(t('Audit &amp; baseline', 'Audit &amp; état des lieux'), t('Documented peering, routing policies and latency per site. Root causes: static-route failover and no application-aware steering.', 'Documentation des peerings, politiques de routage et latences par site. Causes identifiées : bascule par routes statiques et aucune orientation applicative.')),
        (t('Full replica in EVE-NG', 'Maquette complète sous EVE-NG'), t('Four FortiGate 7.4 VMs (2 vCPU / 2 GB each) on a 32 GB host. Every rule and failure case was tested here first.', 'Quatre VM FortiGate 7.4 (2 vCPU / 2 Go chacune) sur un hôte de 32 Go. Chaque règle et chaque scénario de panne y a d’abord été testé.')),
        (t('IPsec provisioning', 'Déploiement IPsec'), t('IKEv2, AES-256 / SHA-256, DH group 14 with PFS, DPD. Two route-based tunnels per spoke, BGP on each.', 'IKEv2, AES-256 / SHA-256, groupe DH 14 avec PFS, DPD. Deux tunnels route-based par agence, BGP sur chacun.')),
        (t('SD-WAN rules &amp; SLA probes', 'Règles SD-WAN &amp; sondes SLA'), t('VoIP prefers ISP-1, bulk data goes to ISP-2, business apps take the lowest-latency member.', 'La VoIP préfère ISP-1, les gros volumes passent par ISP-2, les applications métier prennent le membre à plus faible latence.')),
        (t('FortiManager push &amp; cutover', 'Déploiement FortiManager &amp; bascule'), t('HQ first, in a Saturday 02:00–06:00 window with a rollback snapshot. Spokes on following nights, about 45 minutes each, watched in PRTG.', 'Le siège d’abord, un samedi entre 02h00 et 06h00 avec un snapshot de retour arrière. Les agences les nuits suivantes, environ 45 minutes chacune, sous surveillance PRTG.')),
        (t('Stabilisation &amp; handover', 'Stabilisation &amp; passation'), t('One week of parallel PRTG / FortiAnalyzer monitoring, SLA threshold tuning, then runbooks handed to operations.', 'Une semaine de supervision PRTG / FortiAnalyzer en parallèle, ajustement des seuils SLA, puis remise des procédures à l’exploitation.'))])}"""),
        ("config", "Configuration", f"""
<h2>{t('Key configuration', 'Configuration clé')}</h2>
<h3>{t('SD-WAN members, SLA probe and VoIP rule (spoke)', 'Membres SD-WAN, sonde SLA et règle VoIP (agence)')}</h3>
{code('FortiOS 7.4 · FG-SITE-A', '''
config system sdwan
    set status enable
    config zone
        edit "SDWAN-ZONE"
        next
    end
    config members
        edit 1
            set interface "HQ-ISP1"
            set zone "SDWAN-ZONE"
        next
        edit 2
            set interface "HQ-ISP2"
            set zone "SDWAN-ZONE"
        next
    end
    config health-check
        edit "SLA-VOIP"
            set server "10.1.0.10"
            set interval 500
            set failtime 3
            set recoverytime 5
            set members 1 2
            config sla
                edit 1
                    set latency-threshold 100
                    set jitter-threshold 20
                    set packetloss-threshold 2
                next
            end
        next
    end
    config service
        edit 1
            set name "VoIP-Preferred-ISP1"
            set mode sla
            set dst "VOIP-SERVERS"
            config sla
                edit "SLA-VOIP"
                    set id 1
                next
            end
            set priority-members 1 2
        next
    end
end''')}
<h3>{t('IPsec tunnel to HQ over ISP-1', 'Tunnel IPsec vers le siège via ISP-1')}</h3>
{code('FortiOS 7.4 · FG-SITE-A', '''
config vpn ipsec phase1-interface
    edit "HQ-ISP1"
        set interface "wan1"
        set ike-version 2
        set proposal aes256-sha256
        set dhgrp 14
        set remote-gw 203.0.113.1
        set dpd on-idle
        set dpd-retrycount 3
        set dpd-retryinterval 5
        set psksecret ENC ********
    next
end
config vpn ipsec phase2-interface
    edit "HQ-ISP1-P2"
        set phase1name "HQ-ISP1"
        set proposal aes256-sha256
        set pfs enable
        set dhgrp 14
        set keylifeseconds 3600
    next
end
config system interface
    edit "HQ-ISP1"
        set ip 10.255.1.2 255.255.255.255
        set remote-ip 10.255.1.1 255.255.255.252
    next
end''')}
<h3>{t('BGP: prefer ISP-1, BFD for fast detection, redistribute into OSPF', 'BGP : préférer ISP-1, BFD pour la détection rapide, redistribution dans OSPF')}</h3>
{code('FortiOS 7.4 · FG-SITE-A', '''
config router route-map
    edit "RM-ISP1-IN"
        config rule
            edit 1
                set set-local-preference 200
            next
        end
    next
    edit "RM-ISP2-IN"
        config rule
            edit 1
                set set-local-preference 100
            next
        end
    next
end
config router bgp
    set as 65002
    set router-id 10.2.255.1
    set keepalive-timer 10
    set holdtime-timer 30
    config neighbor
        edit "10.255.1.1"
            set remote-as 65001
            set route-map-in "RM-ISP1-IN"
            set soft-reconfiguration enable
            set bfd enable
        next
        edit "10.255.2.1"
            set remote-as 65001
            set route-map-in "RM-ISP2-IN"
            set soft-reconfiguration enable
            set bfd enable
        next
    end
    config network
        edit 1
            set prefix 10.2.0.0 255.255.0.0
        next
    end
end
config router ospf
    config redistribute "bgp"
        set status enable
        set metric 20
        set metric-type 2
        set routemap "RM-TAG-BGP"
    end
end''')}
<p>{t('<code>local-preference</code> is applied <strong>inbound</strong> on the spoke, so it only influences the spoke’s own choice of path, which is exactly what we want. The route-map <code>RM-TAG-BGP</code> tags redistributed routes so they are never re-imported (see lessons learned).',
      'La <code>local-preference</code> est appliquée <strong>en entrée</strong> sur l’agence : elle n’influence que le choix de chemin de l’agence, ce qui est exactement l’objectif. La route-map <code>RM-TAG-BGP</code> marque les routes redistribuées pour qu’elles ne soient jamais réimportées (voir retours d’expérience).')}</p>"""),
        ("security", t("Security policy", "Politique de sécurité"), f"""
<h2>{t('Security policy', 'Politique de sécurité')}</h2>
<p>{t('Policies apply to the SD-WAN zone, not to individual tunnels, so a failover never needs a policy change. Anything not listed is denied by the implicit deny.',
      'Les politiques s’appliquent à la zone SD-WAN et non aux tunnels : une bascule ne nécessite donc aucun changement de politique. Tout ce qui n’est pas listé est bloqué par le refus implicite.')}</p>
{table([t('Flow', 'Flux'), t('Services', 'Services'), t('Inspection', 'Inspection'), t('Action', 'Action')],
       [[t('Site ↔ site (corporate)', 'Site ↔ site (métier)'), 'HTTPS, SMB, RDP', 'IPS', '<span style="color:var(--green)">allow</span>'],
        ['VoIP', 'SIP, RTP', t('none (latency)', 'aucune (latence)'), '<span style="color:var(--green)">allow</span>'],
        [t('HQ → Internet', 'Siège → Internet'), 'any', t('IPS + application control', 'IPS + contrôle applicatif'), '<span style="color:var(--green)">allow</span>'],
        [t('Spoke → Internet (via HQ)', 'Agence → Internet (via siège)'), 'HTTP, HTTPS', 'IPS', '<span style="color:var(--green)">allow</span>'],
        [t('Spoke → ISP directly', 'Agence → FAI en direct'), 'any', '—', '<span style="color:var(--red)">deny</span>'],
        [t('Unknown intersite', 'Inter-sites inconnu'), 'any', '—', '<span style="color:var(--red)">deny</span>']])}
<p>{t('FortiAnalyzer keeps session logs for <strong>90 days</strong>.', 'FortiAnalyzer conserve les journaux de session <strong>90 jours</strong>.')}</p>"""),
        ("validation", t("Validation", "Validation"), f"""
<h2>{t('Validation &amp; results', 'Validation &amp; résultats')}</h2>
<p>{t('Detection time is driven by the probe settings: <code>interval 500 ms × failtime 3 = 1.5 s</code>. The lab measurement matched that figure.',
      'Le temps de détection découle des réglages de sonde : <code>interval 500 ms × failtime 3 = 1,5 s</code>. La mesure en lab correspond à ce calcul.')}</p>
{ftl}
{bullets([t('<strong>Failover:</strong> from 3–5 minutes with static routes to about 1.5 s with SLA steering (lab).', '<strong>Bascule :</strong> de 3–5 minutes avec les routes statiques à environ 1,5 s avec l’orientation SLA (lab).'),
          t('<strong>Visibility:</strong> per-application traffic dashboards in FortiManager / FortiAnalyzer, where there were none before.', '<strong>Visibilité :</strong> tableaux de bord par application dans FortiManager / FortiAnalyzer, inexistants auparavant.'),
          t('<strong>Encryption:</strong> all intersite traffic now runs in IPsec tunnels.', '<strong>Chiffrement :</strong> tout le trafic inter-sites passe désormais dans des tunnels IPsec.'),
          t('<strong>Cutover:</strong> HQ plus three spokes migrated in maintenance windows with no reported production impact.', '<strong>Bascule en production :</strong> siège et trois agences migrés en fenêtres de maintenance, sans impact signalé sur la production.')])}"""),
        ("lessons", t("Lessons learned", "Retours d’expérience"), f"""
<h2>{t('Lessons learned', 'Retours d’expérience')}</h2>
{table([t('Problem', 'Problème'), t('Fix', 'Correction')],
       [[t('BGP flapping on the 20 Mb/s ISP-2 links', 'Flaps BGP sur les liens ISP-2 à 20 Mb/s'), t('Conservative timers (10 s / 30 s) plus BFD at 300 ms for fast detection.', 'Timers prudents (10 s / 30 s) et BFD à 300 ms pour la détection rapide.')],
        [t('OSPF ↔ BGP redistribution loop', 'Boucle de redistribution OSPF ↔ BGP'), t('Tag routes on redistribution and deny that tag on re-import.', 'Marquage des routes à la redistribution et refus de ce tag à la réimportation.')],
        [t('FortiManager push failures from config drift', 'Échecs de push FortiManager dus à la dérive de config'), t('Retrieve the device config before every push; resolve conflicts in a staging ADOM.', 'Récupérer la config de l’équipement avant chaque push ; résoudre les conflits dans un ADOM de préproduction.')],
        [t('Active VoIP calls dropped on failover', 'Appels VoIP coupés lors de la bascule'), t('SIP session helper on both tunnels and a 500 ms probe interval.', 'SIP session helper sur les deux tunnels et sondes toutes les 500 ms.')],
        [t('Asymmetric routing after cutover', 'Routage asymétrique après la bascule'), t('Zone-based policy routing keeps each session on one path.', 'Le routage par zone garde chaque session sur un seul chemin.')],
        [t('Lab ≠ production (PPPoE on ISP-1)', 'Lab ≠ production (PPPoE sur ISP-1)'), t('Production-specific FortiManager layer on top of the validated base template.', 'Une couche FortiManager propre à la production, au-dessus du modèle validé.')]])}"""),
        ("operations", t("Operations", "Exploitation"), f"""
<h2>{t('Day-2 operations', 'Exploitation au quotidien')}</h2>
{table([t('Command', 'Commande'), t('What it tells you', 'Ce qu’elle montre')],
       [['<code>diagnose sys sdwan health-check</code>', t('SLA probe status per member', 'État des sondes SLA par membre')],
        ['<code>diagnose sys sdwan service</code>', t('Which member each rule is using right now', 'Le membre utilisé par chaque règle à l’instant')],
        ['<code>diagnose sys sdwan member</code>', t('Member state after a failover', 'État des membres après une bascule')],
        ['<code>get router info bgp summary</code>', t('BGP neighbor state and prefixes received', 'État des voisins BGP et préfixes reçus')],
        ['<code>diagnose vpn tunnel list</code>', t('IPsec SAs, counters and DPD state', 'SA IPsec, compteurs et état DPD')]])}"""),
    ]
    return sections


# ═════════════════════════ HYBRID CLOUD ═════════════════════════
def hybrid(x):
    t = x.t
    topo = topo_svg(
        [("LAN", "LAN 10.1.0.0/16", t("on-premises", "sur site"), 90, 140, "sw"),
         ("FG", "FG-HQ", "AS65001 · lo 10.1.255.1", 250, 140, "fw"),
         ("PR", "PRTG", t("monitoring", "supervision"), 250, 250, "sv"),
         ("AZ", "Azure VPN GW", "AS65515 · VpnGw1", 470, 60, "cl"),
         ("VN", "VNet hub", "10.100.0.0/16", 600, 60, "sw"),
         ("TG", "AWS TGW", "AS64512", 470, 220, "cl"),
         ("VP", "VPC", "10.200.0.0/16", 600, 220, "sw")],
        [("LAN", "FG", "", "h"), ("FG", "PR", "SNMP", ""), ("FG", "AZ", "IKEv2 + eBGP multihop", "t"),
         ("FG", "TG", t("2 tunnels + eBGP", "2 tunnels + eBGP"), "t"), ("AZ", "VN", "", ""), ("TG", "VP", "attach", "")],
        w=680, h=290,
        zones=[(400, 20, 270, 90, "Azure · France Central"), (400, 180, 270, 90, "AWS · eu-west-3")],
        caption=t("Route-based IPsec from one FortiGate to both clouds. BGP learns cloud prefixes dynamically; prefix lists stop any route leak.",
                  "IPsec route-based d’un seul FortiGate vers les deux clouds. BGP apprend dynamiquement les préfixes cloud ; des prefix-lists empêchent toute fuite de routes."))
    sections = [
        ("overview", t("Context", "Contexte"), f"""
<h2>{t('Context &amp; objectives', 'Contexte &amp; objectifs')}</h2>
{note(t('Lab project. Addressing, ASNs and IPs are lab values (documentation ranges for public IPs). Pre-shared keys are redacted.',
        'Projet de lab. Adressage, ASN et IP sont des valeurs de lab (plages de documentation pour les IP publiques). Les clés pré-partagées sont masquées.'))}
<p>{t('Most companies end up with workloads in more than one cloud. The goal of this lab was to connect one on-premises site to <strong>Azure and AWS at the same time</strong>, the way an enterprise would: encrypted, dynamically routed, filtered and monitored from one place.',
      'La plupart des entreprises finissent avec des charges dans plusieurs clouds. L’objectif de ce lab : relier un site local à <strong>Azure et AWS en même temps</strong>, comme le ferait une entreprise : chiffré, routé dynamiquement, filtré et supervisé depuis un seul endroit.')}</p>
{bullets([t('Route-based IPsec (IKEv2) from a FortiGate to Azure VPN Gateway and AWS Transit Gateway.', 'IPsec route-based (IKEv2) d’un FortiGate vers Azure VPN Gateway et AWS Transit Gateway.'),
          t('BGP everywhere: no static routes towards the cloud, new VNets / VPCs appear automatically.', 'BGP partout : aucune route statique vers le cloud, les nouveaux VNet / VPC apparaissent automatiquement.'),
          t('Strict filtering: on-prem advertises only its LAN, accepts only the expected cloud prefixes.', 'Filtrage strict : le site n’annonce que son LAN et n’accepte que les préfixes cloud attendus.'),
          t('One monitoring view (PRTG) for tunnels, BGP sessions and end-to-end latency.', 'Une seule vue de supervision (PRTG) pour les tunnels, les sessions BGP et la latence de bout en bout.')])}"""),
        ("architecture", "Architecture", f"""
<h2>Architecture</h2>
{topo}
{table([t('Element', 'Élément'), 'ASN', t('Prefix / address', 'Préfixe / adresse'), t('Notes', 'Remarques')],
       [['FG-HQ', '65001', '10.1.0.0/16 · BGP lo 10.1.255.1', t('Public IP 203.0.113.10', 'IP publique 203.0.113.10')],
        ['Azure VPN Gateway', '65515', 'VNet 10.100.0.0/16 · GatewaySubnet 10.100.255.0/27', t('Route-based, BGP enabled', 'Route-based, BGP activé')],
        ['AWS Transit Gateway', '64512', 'VPC 10.200.0.0/16', t('Inside CIDRs 169.254.10.0/30 and 169.254.11.0/30', 'Inside CIDR 169.254.10.0/30 et 169.254.11.0/30')]])}"""),
        ("design", t("Design choices", "Choix de conception"), f"""
<h2>{t('Design choices', 'Choix de conception')}</h2>
{dcards([(t('route-based, not policy-based', 'route-based plutôt que policy-based'), t('Tunnels as interfaces', 'Tunnels vus comme des interfaces'), t('Routing decides what goes into a tunnel, so BGP, SD-WAN and firewall policies all work on top of it.', 'C’est le routage qui décide de ce qui entre dans un tunnel : BGP, SD-WAN et politiques de pare-feu fonctionnent par-dessus.')),
          (t('Transit Gateway, not a VGW', 'Transit Gateway plutôt qu’un VGW'), t('Scales to many VPCs', 'Passe à l’échelle sur plusieurs VPC'), t('One VPN attachment serves every VPC attached to the TGW. Propagation fills the TGW route table automatically.', 'Une seule attache VPN sert tous les VPC rattachés au TGW. La propagation remplit automatiquement sa table de routage.')),
          (t('prefix lists in &amp; out', 'prefix-lists en entrée et en sortie'), t('No route leaks', 'Aucune fuite de routes'), t('Without filters, the FortiGate could re-advertise AWS routes to Azure and become an unplanned transit between clouds.', 'Sans filtre, le FortiGate pourrait réannoncer les routes AWS vers Azure et devenir un transit imprévu entre clouds.')),
          (t('MSS clamping', 'Ajustement du MSS'), t('No silent drops', 'Pas de pertes silencieuses'), t('IPsec overhead lowers the usable MTU. TCP MSS is clamped to 1350 on cloud-bound policies to avoid fragmentation issues.', 'L’en-tête IPsec réduit la MTU utile. Le MSS TCP est fixé à 1350 sur les politiques vers le cloud pour éviter les problèmes de fragmentation.'))])}"""),
        ("implementation", t("Implementation", "Mise en œuvre"), f"""
<h2>{t('Implementation', 'Mise en œuvre')}</h2>
{steps([(t('Plan addressing &amp; ASNs', 'Plan d’adressage &amp; ASN'), t('Non-overlapping prefixes for on-prem, Azure and AWS; private ASNs per domain (65001, 65515, 64512).', 'Préfixes sans chevauchement entre site, Azure et AWS ; ASN privés par domaine (65001, 65515, 64512).')),
        (t('Azure side', 'Côté Azure'), t('VNet with GatewaySubnet, route-based VPN Gateway with BGP, a Local Network Gateway describing the FortiGate, then the connection.', 'VNet avec GatewaySubnet, VPN Gateway route-based avec BGP, Local Network Gateway décrivant le FortiGate, puis la connexion.')),
        (t('AWS side', 'Côté AWS'), t('Transit Gateway, VPC attachment, Customer Gateway (FortiGate public IP + ASN) and a Site-to-Site VPN attached to the TGW: two tunnels.', 'Transit Gateway, attache VPC, Customer Gateway (IP publique + ASN du FortiGate) et VPN Site-to-Site attaché au TGW : deux tunnels.')),
        (t('FortiGate side', 'Côté FortiGate'), t('Three IPsec interfaces, three BGP neighbors, prefix lists, firewall policies with MSS clamping.', 'Trois interfaces IPsec, trois voisins BGP, prefix-lists, politiques de pare-feu avec ajustement du MSS.')),
        (t('Monitoring', 'Supervision'), t('PRTG sensors for tunnel status, BGP state and ping latency to a test VM in each cloud.', 'Capteurs PRTG pour l’état des tunnels, des sessions BGP et la latence vers une VM de test dans chaque cloud.'))])}"""),
        ("config", "Configuration", f"""
<h2>{t('Key configuration', 'Configuration clé')}</h2>
<h3>Azure (CLI)</h3>
{code('az cli', '''
# Route-based VPN gateway with BGP (ASN 65515)
az network vnet-gateway create -g rg-hybrid -n vgw-hub \\
  --vnet vnet-hub --public-ip-addresses pip-vgw \\
  --gateway-type Vpn --vpn-type RouteBased --sku VpnGw1 --asn 65515

# The FortiGate, seen from Azure
az network local-gateway create -g rg-hybrid -n lng-onprem \\
  --gateway-ip-address 203.0.113.10 --asn 65001 \\
  --bgp-peering-address 10.1.255.1 --local-address-prefixes 10.1.255.1/32

az network vpn-connection create -g rg-hybrid -n cn-onprem \\
  --vnet-gateway1 vgw-hub --local-gateway2 lng-onprem \\
  --shared-key "<redacted>" --enable-bgp''')}
<h3>AWS (CLI)</h3>
{code('aws cli', '''
aws ec2 create-transit-gateway --options \\
  AmazonSideAsn=64512,VpnEcmpSupport=enable,DefaultRouteTablePropagation=enable

aws ec2 create-customer-gateway --type ipsec.1 \\
  --public-ip 203.0.113.10 --bgp-asn 65001

aws ec2 create-vpn-connection --type ipsec.1 \\
  --customer-gateway-id cgw-0abc --transit-gateway-id tgw-0def \\
  --options "TunnelOptions=[{{TunnelInsideCidr=169.254.10.0/30}},{{TunnelInsideCidr=169.254.11.0/30}}]"''').replace('{{', '{').replace('}}', '}')}
<h3>{t('FortiGate: BGP with filtering', 'FortiGate : BGP avec filtrage')}</h3>
{code('FortiOS 7.4 · FG-HQ', '''
config router prefix-list
    edit "PL-ONPREM-OUT"
        config rule
            edit 1
                set prefix 10.1.0.0 255.255.0.0
            next
        end
    next
    edit "PL-AZURE-IN"
        config rule
            edit 1
                set prefix 10.100.0.0 255.255.0.0
                set le 24
            next
        end
    next
    edit "PL-AWS-IN"
        config rule
            edit 1
                set prefix 10.200.0.0 255.255.0.0
                set le 24
            next
        end
    next
end
config router bgp
    set as 65001
    set router-id 10.1.255.1
    set ebgp-multipath enable
    config neighbor
        edit "10.100.255.30"
            set remote-as 65515
            set ebgp-enforce-multihop enable
            set update-source "lo-bgp"
            set prefix-list-in "PL-AZURE-IN"
            set prefix-list-out "PL-ONPREM-OUT"
        next
        edit "169.254.10.1"
            set remote-as 64512
            set prefix-list-in "PL-AWS-IN"
            set prefix-list-out "PL-ONPREM-OUT"
        next
        edit "169.254.11.1"
            set remote-as 64512
            set prefix-list-in "PL-AWS-IN"
            set prefix-list-out "PL-ONPREM-OUT"
        next
    end
    config network
        edit 1
            set prefix 10.1.0.0 255.255.0.0
        next
    end
end''')}
<p>{t('Azure’s BGP peer address sits inside the GatewaySubnet (here <code>10.100.255.30</code>), so the FortiGate reaches it through the tunnel with eBGP multihop from a loopback. On AWS, the peers are the <code>.1</code> addresses of each inside /30, and <code>ebgp-multipath</code> lets both tunnels carry traffic.',
      'L’adresse BGP d’Azure se trouve dans le GatewaySubnet (ici <code>10.100.255.30</code>) : le FortiGate la joint à travers le tunnel en eBGP multihop depuis une loopback. Côté AWS, les pairs sont les adresses <code>.1</code> de chaque /30 interne, et <code>ebgp-multipath</code> permet aux deux tunnels de porter du trafic.')}</p>"""),
        ("validation", t("Validation", "Validation"), f"""
<h2>{t('Validation test plan', 'Plan de tests de validation')}</h2>
{table([t('Test', 'Test'), t('How', 'Comment'), t('Expected result', 'Résultat attendu')],
       [[t('BGP sessions', 'Sessions BGP'), '<code>get router info bgp summary</code>', t('3 neighbors Established', '3 voisins en Established')],
        [t('Routes learned on-prem', 'Routes apprises sur site'), '<code>get router info routing-table bgp</code>', '10.100.0.0/16, 10.200.0.0/16'],
        [t('Routes learned by Azure', 'Routes apprises par Azure'), '<code>az network vnet-gateway list-learned-routes</code>', '10.1.0.0/16 ' + t('only', 'uniquement')],
        [t('Routes in AWS', 'Routes dans AWS'), t('TGW route table', 'Table de routage du TGW'), '10.1.0.0/16 ' + t('via VPN attachment (propagated)', 'via l’attache VPN (propagée)')],
        [t('No transit between clouds', 'Pas de transit entre clouds'), t('Azure VM → AWS VM ping', 'Ping VM Azure → VM AWS'), t('Fails, by design', 'Échoue, par conception')],
        [t('AWS tunnel redundancy', 'Redondance des tunnels AWS'), t('Shut tunnel 1', 'Couper le tunnel 1'), t('Traffic continues on tunnel 2', 'Le trafic continue sur le tunnel 2')],
        [t('End-to-end apps', 'Applications de bout en bout'), 'ICMP + TCP 443 ' + t('to each test VM', 'vers chaque VM de test'), t('Reachable, latency in PRTG', 'Joignable, latence dans PRTG')]])}"""),
        ("considerations", t("Pitfalls", "Points d’attention"), f"""
<h2>{t('Things to watch', 'Points d’attention')}</h2>
{bullets([t('Azure VPN Gateway creation can take <strong>30+ minutes</strong>: start it first.', 'La création d’une Azure VPN Gateway peut prendre <strong>plus de 30 minutes</strong> : la lancer en premier.'),
          t('AWS tunnel inside CIDRs must be /30s from 169.254.0.0/16, avoiding the ranges AWS reserves.', 'Les inside CIDR des tunnels AWS doivent être des /30 de 169.254.0.0/16, hors des plages réservées par AWS.'),
          t('Overlapping prefixes between sites and clouds break everything. Plan the addressing before the first tunnel.', 'Des préfixes qui se chevauchent entre sites et clouds cassent tout. Planifier l’adressage avant le premier tunnel.'),
          t('Without inbound prefix lists, a mistake in a cloud route table can reach your LAN.', 'Sans prefix-list en entrée, une erreur dans une table de routage cloud peut atteindre votre LAN.')])}"""),
    ]
    return sections


# ═════════════════════════ LAN ═════════════════════════
def lan(x):
    t = x.t
    topo = topo_svg(
        [("C1", "CORE-SW-01", "Catalyst 9500", 220, 40, "rt"), ("C2", "CORE-SW-02", "Catalyst 9500", 460, 40, "rt"),
         ("DA", "DIST-A", "Catalyst 3850", 120, 140, "sw"), ("DB", "DIST-B", "Catalyst 3850", 340, 140, "sw"), ("DC", "DIST-C", "Catalyst 3850", 560, 140, "sw"),
         ("A1", "ACC-A1", "2960X", 70, 245, "sv"), ("A2", "ACC-A2", "2960X", 175, 245, "sv"),
         ("B1", "ACC-B1", "2960X", 290, 245, "sv"), ("B2", "ACC-B2", "2960X", 395, 245, "sv"),
         ("X1", "ACC-C1", "2960X", 510, 245, "sv"), ("X2", "ACC-C2", "2960X", 615, 245, "sv")],
        [("C1", "C2", "", "h")] + [(c, d, "", "h") for c in ("C1", "C2") for d in ("DA", "DB", "DC")] +
        [("DA", "A1", "", ""), ("DA", "A2", "", ""), ("DB", "B1", "", ""), ("DB", "B2", "", ""), ("DC", "X1", "", ""), ("DC", "X2", "", "")],
        w=680, h=280,
        caption=t("Three tiers: dual core, one distribution switch per building (OSPF + HSRP), access switches per floor.",
                  "Trois couches : cœur doublé, un commutateur de distribution par bâtiment (OSPF + HSRP), des commutateurs d’accès par étage."))
    sections = [
        ("overview", t("Context", "Contexte"), f"""
<h2>{t('Context &amp; objectives', 'Contexte &amp; objectifs')}</h2>
{note(t('Design and lab validation in EVE-NG. The topology and configurations describe the architecture; figures are not presented as independently audited production results.',
        'Conception et validation en lab sous EVE-NG. La topologie et les configurations décrivent l’architecture ; les chiffres ne sont pas présentés comme des résultats de production audités.'))}
<p>{t('The starting point was a <strong>flat network</strong>: one /16 subnet with more than 800 hosts in a single broadcast domain, no segmentation, and uplinks that saturated. Any broadcast storm or compromised device could reach everything.',
      'Le point de départ : un <strong>réseau à plat</strong>, un seul /16 avec plus de 800 hôtes dans un même domaine de diffusion, aucune segmentation et des liaisons montantes saturées. Une tempête de broadcast ou un poste compromis pouvait tout atteindre.')}</p>
{bullets([t('Structure the campus into core, distribution and access tiers.', 'Structurer le campus en couches cœur, distribution et accès.'),
          t('Segment by role with VLANs and filter between segments with ACLs.', 'Segmenter par usage avec des VLAN et filtrer entre segments avec des ACL.'),
          t('Remove single points of failure for user gateways (HSRP).', 'Supprimer les points uniques de défaillance des passerelles (HSRP).'),
          t('Make the network observable with SNMPv3 and PRTG.', 'Rendre le réseau observable avec SNMPv3 et PRTG.')])}"""),
        ("architecture", "Architecture", f"""
<h2>Architecture</h2>
{topo}
<h3>{t('VLAN plan', 'Plan VLAN')}</h3>
{table(['VLAN', t('Name', 'Nom'), t('Subnet', 'Sous-réseau'), t('Purpose', 'Usage')],
       [['10', 'Corporate', '10.10.10.0/24', t('User workstations', 'Postes utilisateurs')],
        ['20', 'Voice', '10.10.20.0/24', t('IP phones (QoS marked)', 'Téléphones IP (marquage QoS)')],
        ['30', 'Guest', '192.168.30.0/24', t('Internet only, isolated', 'Internet uniquement, isolé')],
        ['40', 'IoT', '10.10.40.0/24', t('Industrial sensors &amp; cameras', 'Capteurs industriels &amp; caméras')],
        ['50', 'Management', '10.10.50.0/24', t('Network device management', 'Administration des équipements')],
        ['60', 'Servers', '10.10.60.0/24', t('Application &amp; file servers', 'Serveurs applicatifs &amp; fichiers')],
        ['99', 'Native / blackhole', '—', t('Unused ports, trunk native VLAN', 'Ports inutilisés, VLAN natif des trunks')]])}"""),
        ("implementation", t("Implementation", "Mise en œuvre"), f"""
<h2>{t('Implementation', 'Mise en œuvre')}</h2>
{steps([(t('Audit &amp; traffic baseline', 'Audit &amp; mesure du trafic'), t('Mapped the flat topology with CDP/LLDP, measured broadcast levels and uplink utilisation.', 'Cartographie de la topologie à plat via CDP/LLDP, mesure du broadcast et de l’utilisation des liaisons montantes.')),
        (t('3-tier design', 'Conception 3 couches'), t('Dual Catalyst 9500 core, one distribution switch per building, access per floor with port-channel uplinks.', 'Cœur Catalyst 9500 doublé, une distribution par bâtiment, accès par étage avec uplinks en port-channel.')),
        (t('VLANs &amp; trunks', 'VLAN &amp; trunks'), t('802.1Q trunks with explicit allowed-VLAN lists and an unused native VLAN (99). Unused VLANs pruned.', 'Trunks 802.1Q avec listes de VLAN autorisés explicites et VLAN natif inutilisé (99). VLAN inutiles élagués.')),
        (t('OSPF &amp; HSRP', 'OSPF &amp; HSRP'), t('SVIs on distribution switches, OSPF area 0 towards the core, HSRPv2 per VLAN with interface tracking and sub-second timers.', 'SVI sur la distribution, OSPF zone 0 vers le cœur, HSRPv2 par VLAN avec suivi d’interface et timers sous la seconde.')),
        (t('ACL enforcement', 'Application des ACL'), t('Guest blocked from internal VLANs, IoT allowed only to its servers, management reachable only from the network team.', 'Invités bloqués vers les VLAN internes, IoT limité à ses serveurs, administration réservée à l’équipe réseau.')),
        (t('Monitoring &amp; validation', 'Supervision &amp; validation'), t('SNMPv3 to PRTG (utilisation, CPU/memory, STP changes). Validated with a ping matrix across VLANs, captures and STP root checks.', 'SNMPv3 vers PRTG (utilisation, CPU/mémoire, changements STP). Validation par matrice de ping inter-VLAN, captures et contrôle de la racine STP.'))])}"""),
        ("config", "Configuration", f"""
<h2>{t('Key configuration', 'Configuration clé')}</h2>
<h3>{t('SVI with HSRP (sub-second timers + tracking)', 'SVI avec HSRP (timers sous la seconde + suivi)')}</h3>
{code('Cisco IOS-XE · DIST-A', '''
interface Vlan10
 description Corporate
 ip address 10.10.10.2 255.255.255.0
 ip helper-address 10.10.60.10
 standby version 2
 standby 10 ip 10.10.10.1
 standby 10 timers msec 250 msec 750
 standby 10 priority 110
 standby 10 preempt
 standby 10 track 1 decrement 20
!
track 1 interface GigabitEthernet1/0/49 line-protocol''')}
<h3>OSPF</h3>
{code('Cisco IOS-XE · DIST-A', '''
router ospf 1
 router-id 10.10.50.2
 passive-interface default
 no passive-interface GigabitEthernet1/0/49
 network 10.10.10.0 0.0.0.255 area 0
 network 10.10.20.0 0.0.0.255 area 0
 network 10.10.40.0 0.0.0.255 area 0
 network 10.10.50.0 0.0.0.255 area 0
 network 10.10.60.0 0.0.0.255 area 0''')}
<h3>{t('Guest isolation ACL', 'ACL d’isolement invités')}</h3>
{code('Cisco IOS-XE · DIST-A', '''
ip access-list extended GUEST-IN
 remark Guest: internet only
 deny   ip 192.168.30.0 0.0.0.255 10.0.0.0 0.255.255.255
 deny   ip 192.168.30.0 0.0.0.255 172.16.0.0 0.15.255.255
 permit udp 192.168.30.0 0.0.0.255 any eq 53
 permit ip 192.168.30.0 0.0.0.255 any
!
interface Vlan30
 ip access-group GUEST-IN in''')}
<h3>{t('Access port hardening', 'Durcissement des ports d’accès')}</h3>
{code('Cisco IOS · ACC-A1', '''
interface range GigabitEthernet0/1 - 46
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 switchport port-security maximum 3
 switchport port-security violation restrict
 spanning-tree portfast
 spanning-tree bpduguard enable
!
ip dhcp snooping
ip dhcp snooping vlan 10,20,30,40
ip arp inspection vlan 10,20,30,40''')}"""),
        ("results", t("Results", "Résultats"), f"""
<h2>{t('Results', 'Résultats')}</h2>
{dcards([('', t('Smaller blast radius', 'Rayon d’impact réduit'), t('From one /16 broadcast domain with 800+ hosts to /24 segments per role.', 'D’un domaine de diffusion /16 de plus de 800 hôtes à des segments /24 par usage.')),
          ('', t('Isolation', 'Isolement'), t('Guest and IoT traffic filtered at distribution; no direct path to corporate or server VLANs.', 'Trafic invités et IoT filtré en distribution : aucun chemin direct vers les VLAN métier ou serveurs.')),
          ('', t('Gateway redundancy', 'Redondance des passerelles'), t('HSRP switchover under one second in the lab with 250 / 750 ms timers, checked with continuous ping.', 'Bascule HSRP en moins d’une seconde en lab avec des timers 250 / 750 ms, vérifiée par ping continu.')),
          ('', t('Observability', 'Observabilité'), t('SNMPv3 on every switch, PRTG dashboards and STP topology-change alerts.', 'SNMPv3 sur chaque commutateur, tableaux de bord PRTG et alertes sur changement de topologie STP.'))])}"""),
        ("operations", t("Operations", "Exploitation"), f"""
<h2>{t('Verification commands', 'Commandes de vérification')}</h2>
{table([t('Command', 'Commande'), t('Checks', 'Vérifie')],
       [['<code>show standby brief</code>', t('HSRP active/standby per VLAN', 'HSRP actif/secours par VLAN')],
        ['<code>show ip ospf neighbor</code>', t('Adjacencies to the core', 'Adjacences vers le cœur')],
        ['<code>show spanning-tree root</code>', t('Root bridge placement per VLAN', 'Placement du pont racine par VLAN')],
        ['<code>show interfaces trunk</code>', t('Allowed and pruned VLANs', 'VLAN autorisés et élagués')],
        ['<code>show ip access-lists GUEST-IN</code>', t('ACL hit counters', 'Compteurs de l’ACL')]])}"""),
    ]
    return sections


# ═════════════════════════ MONITORING ═════════════════════════
def monitoring(x):
    t = x.t
    topo = topo_svg(
        [("SW", t("Switches / routers", "Commutateurs / routeurs"), "SNMPv3", 90, 60, "sw"),
         ("FW", "FortiGate", "SNMPv3 + traps", 90, 150, "fw"),
         ("SV", t("Servers", "Serveurs"), "Zabbix agent", 90, 240, "sv"),
         ("ZB", "Zabbix server", t("triggers · actions", "déclencheurs · actions"), 330, 150, "rt"),
         ("PR", "PRTG", t("WAN / cloud sensors", "capteurs WAN / cloud"), 330, 260, "rt"),
         ("GL", "GLPI", t("tickets · SLA", "tickets · SLA"), 560, 90, "cl"),
         ("DB", t("NOC dashboards", "Tableaux NOC"), "Grafana / Zabbix", 560, 210, "cl")],
        [("SW", "ZB", "", ""), ("FW", "ZB", "", ""), ("SV", "ZB", "", ""), ("FW", "PR", "", ""),
         ("ZB", "GL", "webhook → API", "h"), ("ZB", "DB", "", "t"), ("PR", "DB", "", "t")],
        w=680, h=300,
        caption=t("Collection → detection → ticket: every high-severity problem opens (and later closes) a GLPI incident.",
                  "Collecte → détection → ticket : chaque problème de sévérité haute ouvre (puis referme) un incident GLPI."))
    sections = [
        ("overview", t("Context", "Contexte"), f"""
<h2>{t('Context &amp; objectives', 'Contexte &amp; objectifs')}</h2>
{note(t('Thresholds and configuration below are representative values from this design, shown for illustration.', 'Les seuils et la configuration ci-dessous sont des valeurs représentatives de cette conception, données à titre d’illustration.'))}
<p>{t('In a multisite network, the problem is rarely a lack of alerts. It is too many emails, no owner and no history. The goal was to turn monitoring into an <strong>incident workflow</strong>: detect, open a ticket, assign, resolve, and close automatically when the problem clears.',
      'Dans un réseau multisite, le problème n’est pas le manque d’alertes, mais trop d’e-mails, sans responsable ni historique. L’objectif : transformer la supervision en <strong>processus d’incident</strong>. Détecter, ouvrir un ticket, affecter, résoudre, et clôturer automatiquement quand le problème disparaît.')}</p>"""),
        ("architecture", "Architecture", f"""
<h2>Architecture</h2>
{topo}
{dcards([(t('collection', 'collecte'), 'Zabbix + SNMPv3', t('authPriv (SHA / AES) on every network device; agents on servers. Templates per device family.', 'authPriv (SHA / AES) sur chaque équipement réseau ; agents sur les serveurs. Modèles par famille d’équipements.')),
          (t('WAN &amp; cloud', 'WAN &amp; cloud'), 'PRTG', t('Ping, SNMP and HTTP sensors on ISP links, IPsec tunnels and cloud endpoints.', 'Capteurs ping, SNMP et HTTP sur les liens FAI, tunnels IPsec et points d’accès cloud.')),
          (t('incident', 'incident'), 'GLPI', t('A webhook creates the ticket via the GLPI REST API, with host, severity and graph link. Recovery adds a follow-up and closes it.', 'Un webhook crée le ticket via l’API REST de GLPI, avec hôte, sévérité et lien vers le graphe. Le retour à la normale ajoute un suivi et le clôture.')),
          (t('noise control', 'anti-bruit'), t('Dependencies &amp; hysteresis', 'Dépendances &amp; hystérésis'), t('If a site router is down, alerts for everything behind it are suppressed. Recovery thresholds sit below problem thresholds to avoid flapping.', 'Si le routeur d’un site tombe, les alertes des équipements derrière lui sont supprimées. Les seuils de retour sont plus bas que les seuils de déclenchement pour éviter les oscillations.'))])}"""),
        ("thresholds", t("Alert design", "Conception des alertes"), f"""
<h2>{t('Alert design', 'Conception des alertes')}</h2>
{table([t('Signal', 'Signal'), t('Problem', 'Déclenchement'), t('Recovery', 'Retour'), t('Severity', 'Sévérité'), 'GLPI'],
       [[t('Device unreachable (ICMP)', 'Équipement injoignable (ICMP)'), t('3 failed checks', '3 échecs consécutifs'), t('1 success', '1 succès'), 'Disaster', t('P1 ticket', 'Ticket P1')],
        [t('BGP / IPsec peer down', 'Pair BGP / IPsec tombé'), t('state ≠ Established', 'état ≠ Established'), 'Established', 'High', t('P1 ticket', 'Ticket P1')],
        [t('SD-WAN SLA failed', 'SLA SD-WAN en échec'), t('member out of SLA', 'membre hors SLA'), t('back in SLA', 'retour dans le SLA'), 'Average', t('P2 ticket', 'Ticket P2')],
        [t('Interface utilisation', 'Utilisation d’interface'), '&gt; 90 % / 10 min', '&lt; 75 %', 'Average', t('P3 ticket', 'Ticket P3')],
        ['CPU', '&gt; 85 % / 5 min', '&lt; 70 %', 'Warning', t('dashboard only', 'tableau de bord')],
        [t('STP topology change', 'Changement de topologie STP'), t('trap received', 'trap reçu'), '—', 'Warning', t('dashboard only', 'tableau de bord')]])}
{code(t('Zabbix trigger expressions (6.x syntax)', 'Expressions de déclencheurs Zabbix (syntaxe 6.x)'), '''
# Interface saturation, with hysteresis via recovery expression
avg(/FG-SITE-A/net.if.in[ifHCInOctets.5],10m) > 0.9 * last(/FG-SITE-A/net.if.speed[ifHighSpeed.5])
# recovery:
avg(/FG-SITE-A/net.if.in[ifHCInOctets.5],10m) < 0.75 * last(/FG-SITE-A/net.if.speed[ifHighSpeed.5])

# Device unreachable: 3 consecutive ICMP failures
max(/FG-SITE-A/icmpping,#3) = 0''')}
<p>{t('Item keys are simplified for readability; in practice they come from the vendor templates.', 'Les clés d’items sont simplifiées pour la lecture ; en pratique elles proviennent des modèles constructeur.')}</p>"""),
        ("workflow", t("Incident workflow", "Processus d’incident"), f"""
<h2>{t('Incident workflow', 'Processus d’incident')}</h2>
{steps([(t('Detect', 'Détecter'), t('Trigger fires in Zabbix (or sensor goes down in PRTG).', 'Un déclencheur s’active dans Zabbix (ou un capteur passe en erreur dans PRTG).')),
        (t('Open', 'Ouvrir'), t('Webhook creates a GLPI ticket: category, priority from severity, host, last values and a link to the graph.', 'Le webhook crée un ticket GLPI : catégorie, priorité selon la sévérité, hôte, dernières valeurs et lien vers le graphe.')),
        (t('Assign &amp; acknowledge', 'Affecter &amp; acquitter'), t('Ticket goes to the network group; acknowledging in Zabbix stops escalation.', 'Le ticket part au groupe réseau ; l’acquittement dans Zabbix stoppe l’escalade.')),
        (t('Resolve', 'Résoudre'), t('When the trigger recovers, a follow-up is added and the ticket is solved automatically.', 'Quand le déclencheur revient à la normale, un suivi est ajouté et le ticket est résolu automatiquement.')),
        (t('Review', 'Analyser'), t('Weekly review of top recurring tickets to fix root causes, not symptoms.', 'Revue hebdomadaire des tickets récurrents pour traiter les causes, pas les symptômes.'))])}"""),
        ("config", "Configuration", f"""
<h2>{t('Device-side configuration', 'Configuration côté équipements')}</h2>
{code('Cisco IOS · SNMPv3 authPriv', '''
snmp-server group NMS v3 priv read NMS-VIEW access ACL-NMS
snmp-server view NMS-VIEW iso included
snmp-server user zabbix NMS v3 auth sha <redacted> priv aes 128 <redacted>
snmp-server host 10.10.50.20 version 3 priv zabbix
snmp-server enable traps snmp linkdown linkup
!
ip access-list standard ACL-NMS
 permit 10.10.50.20''')}
{code('FortiOS · SNMPv3', '''
config system snmp user
    edit "zabbix"
        set notify-hosts 10.10.50.20
        set security-level auth-priv
        set auth-proto sha256
        set auth-pwd ENC ********
        set priv-proto aes256
        set priv-pwd ENC ********
    next
end''')}"""),
    ]
    return sections


BUILDERS = {"sdwan": sdwan, "hybrid-cloud": hybrid, "lan-optimization": lan, "monitoring-stack": monitoring}

META = {
    "sdwan": dict(kpis=[("4", ("sites", "sites")), ("≈1.5 s", ("lab failover", "bascule en lab")), ("3–5 min", ("before (static routes)", "avant (routes statiques)")), ("90 d", ("log retention", "rétention des logs"))],
                  metas=[(("Role", "Rôle"), ("Network security project lead", "Chef de projet sécurité réseau")), (("Stack", "Stack"), ("FortiGate 7.4 · FortiManager · FortiAnalyzer", "FortiGate 7.4 · FortiManager · FortiAnalyzer")), (("Validation", "Validation"), ("EVE-NG", "EVE-NG"))]),
    "hybrid-cloud": dict(kpis=[("2", ("clouds", "clouds")), ("3", ("BGP peers", "pairs BGP")), ("IKEv2", ("route-based IPsec", "IPsec route-based")), ("1", ("monitoring view", "vue de supervision"))],
                         metas=[(("Type", "Type"), ("Lab project", "Projet de lab")), (("Stack", "Stack"), ("FortiGate · Azure VPN GW · AWS TGW · PRTG", "FortiGate · Azure VPN GW · AWS TGW · PRTG"))]),
    "lan-optimization": dict(kpis=[("3", ("tiers", "couches")), ("12", ("VLANs deployed", "VLAN déployés")), ("800+", ("hosts in the old /16", "hôtes dans l’ancien /16")), ("&lt;1 s", ("HSRP switchover (lab)", "bascule HSRP (lab)"))],
                             metas=[(("Type", "Type"), ("Design + EVE-NG lab", "Conception + lab EVE-NG")), (("Stack", "Stack"), ("Cisco Catalyst · OSPF · HSRP · PRTG", "Cisco Catalyst · OSPF · HSRP · PRTG"))]),
    "monitoring-stack": dict(kpis=[("SNMPv3", ("authPriv everywhere", "authPriv partout")), ("5", ("severity levels", "niveaux de sévérité")), ("auto", ("ticket open &amp; close", "ouverture &amp; clôture des tickets")), ("1", ("NOC view", "vue NOC"))],
                             metas=[(("Type", "Type"), ("Operations", "Exploitation")), (("Stack", "Stack"), ("Zabbix · PRTG · GLPI", "Zabbix · PRTG · GLPI"))]),
}
