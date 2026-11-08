"""EVE-NG lab guides. Text is (en, fr); configs are language-neutral."""
from common import code, table, bullets, topo_svg

LABS = [
# ─────────────────────────── 1. BGP ───────────────────────────
dict(id="bgp", tags="Routing · eBGP", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("BGP fundamentals", "Fondamentaux BGP"),
 focus=("eBGP peering, advertisements, path selection", "Voisinage eBGP, annonces, sélection de chemin"),
 objective=("Build eBGP between three autonomous systems, advertise LAN prefixes, then change the path R1 uses to reach AS65003 with local preference, without touching the shortest AS path.",
            "Monter de l’eBGP entre trois systèmes autonomes, annoncer les préfixes LAN, puis modifier le chemin utilisé par R1 vers l’AS65003 avec la local preference, sans toucher au chemin AS le plus court."),
 nodes=[("R1", "R1", "AS65001 · 1.1.1.1", 120, 150, "rt"), ("R2", "R2", "AS65002 · 2.2.2.2", 340, 50, "rt"), ("R3", "R3", "AS65003 · 3.3.3.3", 560, 150, "rt"),
        ("L1", "LAN 172.16.1.0/24", "", 120, 250, "sw"), ("L3", "LAN 172.16.3.0/24", "", 560, 250, "sw")],
 links=[("R1", "R2", "10.0.12.0/30", "h"), ("R2", "R3", "10.0.23.0/30", "h"), ("R1", "R3", "10.0.13.0/30", ""), ("R1", "L1", "", ""), ("R3", "L3", "", "")],
 addressing=[["R1", "Gi0/0 → R2", "10.0.12.1/30"], ["R1", "Gi0/1 → R3", "10.0.13.1/30"], ["R2", "Gi0/0 → R1", "10.0.12.2/30"], ["R2", "Gi0/1 → R3", "10.0.23.1/30"],
             ["R3", "Gi0/0 → R2", "10.0.23.2/30"], ["R3", "Gi0/1 → R1", "10.0.13.2/30"], ["R1 / R3", "Gi0/2 (LAN)", "172.16.1.1/24 · 172.16.3.1/24"]],
 steps=[
  (("Bring up eBGP sessions", "Monter les sessions eBGP"), ("One neighbor per directly connected link. Activate them under the IPv4 address family.", "Un voisin par lien direct, activé dans l’address-family IPv4."), "R1", """
router bgp 65001
 bgp router-id 1.1.1.1
 bgp log-neighbor-changes
 neighbor 10.0.12.2 remote-as 65002
 neighbor 10.0.13.2 remote-as 65003
 address-family ipv4
  neighbor 10.0.12.2 activate
  neighbor 10.0.13.2 activate
  network 172.16.1.0 mask 255.255.255.0"""),
  (("Advertise the LANs", "Annoncer les LAN"), ("A <code>network</code> statement only works if the exact prefix is already in the routing table.", "Une commande <code>network</code> ne fonctionne que si le préfixe exact est déjà dans la table de routage."), "R3", """
router bgp 65003
 bgp router-id 3.3.3.3
 neighbor 10.0.23.1 remote-as 65002
 neighbor 10.0.13.1 remote-as 65001
 address-family ipv4
  neighbor 10.0.23.1 activate
  neighbor 10.0.13.1 activate
  network 172.16.3.0 mask 255.255.255.0"""),
  (("Change the best path", "Changer le meilleur chemin"), ("By default R1 reaches 172.16.3.0/24 directly (shortest AS path). Raise local preference on routes from R2 so R1 prefers the path through AS65002.", "Par défaut, R1 joint 172.16.3.0/24 en direct (chemin AS le plus court). On augmente la local preference des routes reçues de R2 pour que R1 préfère passer par l’AS65002."), "R1", """
route-map FROM-R2 permit 10
 set local-preference 200
!
router bgp 65001
 address-family ipv4
  neighbor 10.0.12.2 route-map FROM-R2 in
!
clear ip bgp 10.0.12.2 soft in"""),
 ],
 verify=[("show ip bgp summary", ("Both neighbors show a prefix count, not Idle/Active.", "Les deux voisins affichent un nombre de préfixes, pas Idle/Active.")),
         ("show ip bgp 172.16.3.0", ("Two paths; best path via 10.0.12.2 with localpref 200.", "Deux chemins ; le meilleur via 10.0.12.2 avec localpref 200.")),
         ("show ip route bgp", ("172.16.3.0/24 next hop 10.0.12.2 after the change.", "172.16.3.0/24 via 10.0.12.2 après la modification.")),
         ("traceroute 172.16.3.1 source 172.16.1.1", ("Goes through R2.", "Passe par R2."))],
 breakfix=[(("Wrong remote-as on one side", "remote-as erroné d’un côté"), ("Session flaps between Idle and Active; logs show a NOTIFICATION with \"bad peer AS\". Fix the ASN.", "La session oscille entre Idle et Active ; les logs montrent une NOTIFICATION \"bad peer AS\". Corriger l’ASN.")),
           (("Network statement with the wrong mask", "Commande network avec un mauvais masque"), ("The prefix never appears in <code>show ip bgp</code>, because no exact match exists in the RIB.", "Le préfixe n’apparaît jamais dans <code>show ip bgp</code> : aucune correspondance exacte dans la RIB.")),
           (("Route-map applied but nothing changes", "Route-map appliquée mais rien ne change"), ("Policy only applies to new updates. Run a soft inbound clear.", "La politique ne s’applique qu’aux nouvelles mises à jour : faire un clear soft en entrée."))],
 takeaways=[("eBGP is policy routing: you decide which path wins, not the metric.", "L’eBGP, c’est du routage par politique : c’est vous qui choisissez le chemin, pas la métrique."),
            ("Local preference is checked before AS-path length and stays inside your AS.", "La local preference est évaluée avant la longueur du chemin AS et reste interne à votre AS."),
            ("Always soft-clear after changing inbound policy.", "Toujours faire un clear soft après une modification de politique en entrée.")]),

# ─────────────────────────── 2. OSPF ───────────────────────────
dict(id="ospf", tags="Routing · OSPF", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("OSPF multi-area", "OSPF multi-zones"),
 focus=("Areas, LSA types, summarisation, stub areas", "Zones, types de LSA, agrégation, zones stub"),
 objective=("Build a backbone and two areas, summarise area 1 on its ABR, turn area 2 into a totally stubby area and secure adjacencies with MD5 authentication.",
            "Construire une zone backbone et deux zones, agréger la zone 1 sur son ABR, transformer la zone 2 en zone totally stubby et sécuriser les adjacences avec une authentification MD5."),
 nodes=[("R1", "R1", "area 1 · 10.1.x", 90, 150, "rt"), ("R2", "R2 (ABR)", "area 0 / 1", 260, 150, "rt"), ("R3", "R3 (ABR)", "area 0 / 2", 450, 150, "rt"), ("R4", "R4", "area 2 stub", 610, 150, "rt")],
 links=[("R1", "R2", "area 1", ""), ("R2", "R3", "area 0", "h"), ("R3", "R4", "area 2", "")],
 zones=[(30, 95, 150, 110, "AREA 1"), (200, 95, 310, 110, "AREA 0"), (540, 95, 130, 110, "AREA 2")],
 addressing=[["R1", "Lo1–Lo4", "10.1.0.1/24 … 10.1.3.1/24"], ["R1–R2", "Gi0/0", "10.0.12.0/30"], ["R2–R3", "Gi0/1", "10.0.23.0/30"], ["R3–R4", "Gi0/2", "10.0.34.0/30"], ["R4", "Lo0", "10.2.0.1/24"]],
 steps=[
  (("Areas and router IDs", "Zones et router-id"), ("Put each interface in its area. Loopbacks as point-to-point so the /24 is advertised as-is.", "Placer chaque interface dans sa zone. Loopbacks en point-to-point pour annoncer le /24 tel quel."), "R2", """
router ospf 1
 router-id 2.2.2.2
 network 10.0.12.0 0.0.0.3 area 1
 network 10.0.23.0 0.0.0.3 area 0"""),
  (("Summarise area 1 on the ABR", "Agréger la zone 1 sur l’ABR"), ("Four /24s leave area 1 as a single 10.1.0.0/16 type-3 LSA.", "Les quatre /24 sortent de la zone 1 sous forme d’un seul LSA de type 3 en 10.1.0.0/16."), "R2", """
router ospf 1
 area 1 range 10.1.0.0 255.255.0.0"""),
  (("Totally stubby area 2", "Zone 2 totally stubby"), ("Both routers in area 2 must agree on the stub flag. <code>no-summary</code> on the ABR only.", "Les deux routeurs de la zone 2 doivent avoir le même flag stub. <code>no-summary</code> sur l’ABR uniquement."), "R3 / R4", """
! R3 (ABR)
router ospf 1
 area 2 stub no-summary
! R4
router ospf 1
 area 2 stub"""),
  (("MD5 authentication on the backbone", "Authentification MD5 sur le backbone"), ("Same key ID and key on both ends.", "Même ID et même clé des deux côtés."), "R2 / R3", """
interface GigabitEthernet0/1
 ip ospf message-digest-key 1 md5 <redacted>
!
router ospf 1
 area 0 authentication message-digest"""),
 ],
 verify=[("show ip ospf neighbor", ("FULL adjacencies on every link.", "Adjacences FULL sur chaque lien.")),
         ("show ip route ospf  (on R3)", ("One O IA 10.1.0.0/16 instead of four /24s.", "Un seul O IA 10.1.0.0/16 au lieu de quatre /24.")),
         ("show ip route  (on R4)", ("Only a default route O*IA from the ABR.", "Seulement une route par défaut O*IA venant de l’ABR.")),
         ("show ip ospf database", ("Type-3 LSAs absent inside area 2.", "Aucun LSA de type 3 dans la zone 2."))],
 breakfix=[(("MTU mismatch on one link", "MTU différente sur un lien"), ("Neighbors stay stuck in EXSTART/EXCHANGE. Match the MTU (or ip ospf mtu-ignore as a last resort).", "Les voisins restent bloqués en EXSTART/EXCHANGE. Aligner la MTU (ou ip ospf mtu-ignore en dernier recours).")),
           (("Stub flag only on one side", "Flag stub d’un seul côté"), ("No adjacency: the hello options field differs. Configure stub on both routers.", "Pas d’adjacence : le champ options des hellos diffère. Configurer stub sur les deux routeurs.")),
           (("Different hello/dead timers", "Timers hello/dead différents"), ("Neighbor never appears. Align timers per link.", "Le voisin n’apparaît jamais. Aligner les timers sur le lien."))],
 takeaways=[("Areas limit the flooding scope; ABRs are where you summarise.", "Les zones limitent l’inondation ; c’est sur les ABR qu’on agrège."),
            ("Stub areas trade detail for stability: a default route is often enough.", "Les zones stub échangent du détail contre de la stabilité : une route par défaut suffit souvent."),
            ("Most adjacency problems are a parameter mismatch: area, MTU, timers, auth, stub flag.", "La plupart des problèmes d’adjacence viennent d’un paramètre différent : zone, MTU, timers, auth, flag stub.")]),

# ─────────────────────────── 3. VLAN ───────────────────────────
dict(id="vlan", tags="Switching · 802.1Q", level=("Beginner", "Débutant"), time="45 min",
 title=("VLANs & inter-VLAN routing", "VLAN & routage inter-VLAN"),
 focus=("Trunks, SVIs, router-on-a-stick", "Trunks, SVI, router-on-a-stick"),
 objective=("Segment users into VLANs, carry them over a secured trunk, and route between them twice: first with SVIs on a layer-3 switch, then with router-on-a-stick.",
            "Segmenter les utilisateurs en VLAN, les transporter sur un trunk sécurisé, puis les router de deux façons : SVI sur un commutateur de niveau 3, puis router-on-a-stick."),
 nodes=[("D", "DSW1 (L3)", "SVI 10 / 20", 340, 50, "rt"), ("A", "ASW1", "access", 340, 160, "sw"), ("P1", "PC-10", "10.10.10.11", 200, 260, "sv"), ("P2", "PC-20", "10.10.20.11", 480, 260, "sv"), ("R", "R1", "router-on-a-stick", 590, 50, "rt")],
 links=[("D", "A", "trunk 10,20 · native 99", "h"), ("A", "P1", "VLAN 10", ""), ("A", "P2", "VLAN 20", ""), ("A", "R", "trunk (variant)", "t")],
 addressing=[["VLAN 10", "Users", "10.10.10.0/24 · gw .1"], ["VLAN 20", "Voice / Lab", "10.10.20.0/24 · gw .1"], ["VLAN 99", "Native (unused)", "—"]],
 steps=[
  (("Create VLANs and access ports", "Créer les VLAN et les ports d’accès"), ("Same VLAN IDs on both switches.", "Mêmes ID de VLAN sur les deux commutateurs."), "ASW1", """
vlan 10
 name USERS
vlan 20
 name VOICE
vlan 99
 name NATIVE-UNUSED
!
interface Gi0/1
 switchport mode access
 switchport access vlan 10
interface Gi0/2
 switchport mode access
 switchport access vlan 20"""),
  (("Build a secure trunk", "Construire un trunk sécurisé"), ("Static trunk, explicit allowed list, unused native VLAN, no DTP.", "Trunk statique, liste autorisée explicite, VLAN natif inutilisé, pas de DTP."), "ASW1 / DSW1", """
interface Gi0/0
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 switchport nonegotiate"""),
  (("Route with SVIs", "Router avec des SVI"), ("Layer-3 switch: one SVI per VLAN, and enable routing.", "Commutateur L3 : une SVI par VLAN, et activer le routage."), "DSW1", """
ip routing
!
interface Vlan10
 ip address 10.10.10.1 255.255.255.0
 no shutdown
interface Vlan20
 ip address 10.10.20.1 255.255.255.0
 no shutdown"""),
  (("Variant: router-on-a-stick", "Variante : router-on-a-stick"), ("Remove the SVIs and route on R1 sub-interfaces instead.", "Supprimer les SVI et router sur des sous-interfaces de R1."), "R1", """
interface Gi0/0.10
 encapsulation dot1Q 10
 ip address 10.10.10.1 255.255.255.0
interface Gi0/0.20
 encapsulation dot1Q 20
 ip address 10.10.20.1 255.255.255.0
interface Gi0/0.99
 encapsulation dot1Q 99 native"""),
 ],
 verify=[("show vlan brief", ("Access ports in the right VLAN.", "Ports d’accès dans le bon VLAN.")),
         ("show interfaces trunk", ("Trunking, native 99, allowed 10,20,99.", "Trunk actif, natif 99, autorisés 10,20,99.")),
         ("show ip interface brief | include Vlan", ("SVIs up/up.", "SVI up/up.")),
         ("ping 10.10.20.11  (from PC-10)", ("Replies through the gateway.", "Réponses via la passerelle."))],
 breakfix=[(("VLAN missing from the allowed list", "VLAN absent de la liste autorisée"), ("Hosts in that VLAN can’t reach their gateway. Check <code>show interfaces trunk</code>.", "Les hôtes de ce VLAN ne joignent pas leur passerelle. Vérifier <code>show interfaces trunk</code>.")),
           (("Native VLAN mismatch", "VLAN natif différent"), ("CDP logs a native VLAN mismatch and untagged traffic leaks between VLANs.", "CDP signale un native VLAN mismatch et le trafic non tagué fuit entre VLAN.")),
           (("SVI stays down", "La SVI reste down"), ("An SVI is only up if one port in that VLAN is up (access or trunk).", "Une SVI n’est up que si un port de ce VLAN est actif (accès ou trunk)."))],
 takeaways=[("A VLAN is a broadcast domain; routing is what joins them.", "Un VLAN est un domaine de diffusion ; c’est le routage qui les relie."),
            ("Trunks should be explicit: allowed list, native VLAN, no DTP.", "Un trunk doit être explicite : liste autorisée, VLAN natif, pas de DTP."),
            ("SVIs scale better than router-on-a-stick, which shares one link for all VLANs.", "Les SVI passent mieux à l’échelle que le router-on-a-stick, qui partage un seul lien pour tous les VLAN.")]),

# ─────────────────────────── 4. IPsec ───────────────────────────
dict(id="ipsec", tags="VPN · IKEv2", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("IPsec site-to-site VPN", "VPN IPsec site à site"),
 focus=("IKEv2, route-based VTI, troubleshooting", "IKEv2, VTI route-based, dépannage"),
 objective=("Connect two sites over the internet with a route-based IKEv2 tunnel (VTI): AES-256, SHA-256, DH group 14 with PFS, then troubleshoot the classic negotiation failures.",
            "Relier deux sites via internet avec un tunnel IKEv2 route-based (VTI) : AES-256, SHA-256, groupe DH 14 avec PFS, puis dépanner les échecs de négociation classiques."),
 nodes=[("L1", "LAN-1", "192.168.1.0/24", 80, 140, "sw"), ("R1", "R1", "198.51.100.1", 230, 140, "rt"), ("I", "INTERNET", "ISP router", 400, 60, "cl"), ("R2", "R2", "198.51.100.2", 570, 140, "rt"), ("L2", "LAN-2", "192.168.2.0/24", 660, 230, "sw")],
 links=[("L1", "R1", "", ""), ("R1", "I", "", ""), ("I", "R2", "", ""), ("R1", "R2", "Tunnel0 10.255.0.0/30", "t"), ("R2", "L2", "", "")],
 addressing=[["R1", "Gi0/0 (WAN)", "198.51.100.1"], ["R2", "Gi0/0 (WAN)", "198.51.100.2"], ["R1 / R2", "Tunnel0", "10.255.0.1/30 · 10.255.0.2/30"], ["R1 / R2", "LAN", "192.168.1.1/24 · 192.168.2.1/24"]],
 steps=[
  (("IKEv2 proposal, policy and keyring", "Proposition, politique et keyring IKEv2"), ("Phase 1 parameters must match on both peers.", "Les paramètres de phase 1 doivent être identiques des deux côtés."), "R1", """
crypto ikev2 proposal PROP-AES256
 encryption aes-cbc-256
 integrity sha256
 group 14
crypto ikev2 policy POL-1
 proposal PROP-AES256
crypto ikev2 keyring KR-R2
 peer R2
  address 198.51.100.2
  pre-shared-key <redacted>
crypto ikev2 profile PROF-R2
 match identity remote address 198.51.100.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR-R2"""),
  (("IPsec profile (phase 2)", "Profil IPsec (phase 2)"), ("ESP AES-256 / SHA-256 with PFS group 14.", "ESP AES-256 / SHA-256 avec PFS groupe 14."), "R1", """
crypto ipsec transform-set TS-AES256 esp-aes 256 esp-sha256-hmac
 mode tunnel
crypto ipsec profile IPSEC-R2
 set transform-set TS-AES256
 set ikev2-profile PROF-R2
 set pfs group14"""),
  (("Tunnel interface and routing", "Interface tunnel et routage"), ("The VTI is a normal interface: route the remote LAN into it. MSS is clamped for the IPsec overhead.", "La VTI est une interface classique : on y route le LAN distant. Le MSS est ajusté pour l’en-tête IPsec."), "R1", """
interface Tunnel0
 ip address 10.255.0.1 255.255.255.252
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0
 tunnel destination 198.51.100.2
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile IPSEC-R2
!
ip route 192.168.2.0 255.255.255.0 Tunnel0"""),
 ],
 verify=[("show crypto ikev2 sa", ("Status READY.", "Statut READY.")),
         ("show crypto ipsec sa", ("encaps and decaps counters both increase.", "Les compteurs encaps et decaps augmentent tous les deux.")),
         ("show interface Tunnel0", ("up/up, tunnel protocol IPSEC/IP.", "up/up, protocole IPSEC/IP.")),
         ("ping 192.168.2.1 source 192.168.1.1", ("Success; the first packet may be lost while the SA builds.", "Succès ; le premier paquet peut être perdu pendant la création de la SA."))],
 breakfix=[(("Pre-shared key mismatch", "Clé pré-partagée différente"), ("IKE_AUTH fails; debug shows an authentication failure. Re-enter the key on both sides.", "IKE_AUTH échoue ; le debug indique un échec d’authentification. Ressaisir la clé des deux côtés.")),
           (("Different proposals", "Propositions différentes"), ("NO_PROPOSAL_CHOSEN in the logs. Compare encryption, integrity and DH group.", "NO_PROPOSAL_CHOSEN dans les logs. Comparer chiffrement, intégrité et groupe DH.")),
           (("Tunnel up, no traffic", "Tunnel actif, pas de trafic"), ("Encaps stays at 0: the route to the remote LAN is missing, or a firewall blocks UDP 500/4500.", "Encaps reste à 0 : la route vers le LAN distant manque, ou un pare-feu bloque l’UDP 500/4500."))],
 takeaways=[("Route-based VPNs scale: add a route (or BGP) instead of editing crypto ACLs.", "Les VPN route-based passent à l’échelle : on ajoute une route (ou BGP) au lieu de modifier des ACL crypto."),
            ("Read the error: NO_PROPOSAL_CHOSEN, AUTH_FAILED and TS_UNACCEPTABLE each point to a different fix.", "Lire l’erreur : NO_PROPOSAL_CHOSEN, AUTH_FAILED et TS_UNACCEPTABLE pointent chacun vers une correction différente."),
            ("Clamp MSS on tunnels to avoid fragmentation problems.", "Ajuster le MSS sur les tunnels pour éviter les problèmes de fragmentation.")]),

# ─────────────────────────── 5. MPLS ───────────────────────────
dict(id="mpls-vrf", tags="MPLS · L3VPN", level=("Advanced", "Avancé"), time="90 min",
 title=("MPLS L3VPN & VRF", "MPLS L3VPN & VRF"),
 focus=("LDP, VRF, MP-BGP VPNv4, route targets", "LDP, VRF, MP-BGP VPNv4, route targets"),
 objective=("Build a small provider core (OSPF + LDP), then a customer L3VPN: VRFs on the PEs, MP-BGP VPNv4 between PE loopbacks and eBGP to the customer edges.",
            "Construire un petit cœur opérateur (OSPF + LDP), puis un L3VPN client : VRF sur les PE, MP-BGP VPNv4 entre les loopbacks des PE et eBGP vers les CE."),
 nodes=[("C1", "CE-A1", "AS65101", 70, 150, "sw"), ("P1", "PE1", "lo 10.0.0.1", 220, 150, "rt"), ("P", "P", "lo 10.0.0.2", 380, 150, "rt"), ("P2", "PE2", "lo 10.0.0.3", 540, 150, "rt"), ("C2", "CE-A2", "AS65102", 660, 150, "sw")],
 links=[("C1", "P1", "eBGP · VRF CUST-A", ""), ("P1", "P", "OSPF + LDP", "h"), ("P", "P2", "OSPF + LDP", "h"), ("P2", "C2", "eBGP · VRF CUST-A", "")],
 zones=[(150, 95, 460, 110, "PROVIDER AS65000")],
 addressing=[["PE1 / P / PE2", "Loopback0", "10.0.0.1 · 10.0.0.2 · 10.0.0.3 /32"], ["Core links", "Gi0/0–Gi0/1", "10.1.12.0/30 · 10.1.23.0/30"], ["CE-A1 ↔ PE1", "VRF CUST-A", "10.10.1.0/30"], ["CE-A2 ↔ PE2", "VRF CUST-A", "10.10.2.0/30"]],
 steps=[
  (("Core: OSPF + LDP", "Cœur : OSPF + LDP"), ("Every core interface runs OSPF and LDP. Loopbacks are the LDP router IDs and BGP sources.", "Chaque interface du cœur fait tourner OSPF et LDP. Les loopbacks servent de router-id LDP et de source BGP."), "PE1 / P / PE2", """
mpls label protocol ldp
mpls ldp router-id Loopback0 force
!
interface GigabitEthernet0/0
 mpls ip
!
router ospf 1
 network 10.0.0.0 0.0.0.255 area 0
 network 10.1.0.0 0.0.255.255 area 0"""),
  (("Customer VRF on the PE", "VRF client sur le PE"), ("The RD makes routes unique; route targets decide who imports them.", "Le RD rend les routes uniques ; les route targets décident qui les importe."), "PE1", """
vrf definition CUST-A
 rd 65000:1
 address-family ipv4
  route-target export 65000:1
  route-target import 65000:1
!
interface GigabitEthernet0/2
 vrf forwarding CUST-A
 ip address 10.10.1.1 255.255.255.252"""),
  (("MP-BGP VPNv4 + PE–CE eBGP", "MP-BGP VPNv4 + eBGP PE–CE"), ("iBGP between PE loopbacks carries VPNv4 routes with extended communities.", "L’iBGP entre loopbacks des PE transporte les routes VPNv4 avec les communautés étendues."), "PE1", """
router bgp 65000
 neighbor 10.0.0.3 remote-as 65000
 neighbor 10.0.0.3 update-source Loopback0
 address-family vpnv4
  neighbor 10.0.0.3 activate
  neighbor 10.0.0.3 send-community extended
 address-family ipv4 vrf CUST-A
  neighbor 10.10.1.2 remote-as 65101
  neighbor 10.10.1.2 activate"""),
 ],
 verify=[("show mpls ldp neighbor", ("LDP sessions Oper on every core link.", "Sessions LDP en Oper sur chaque lien du cœur.")),
         ("show mpls forwarding-table", ("Labels for the remote PE loopbacks.", "Des labels pour les loopbacks des PE distants.")),
         ("show bgp vpnv4 unicast all", ("Customer prefixes with RD 65000:1.", "Préfixes client avec le RD 65000:1.")),
         ("ping vrf CUST-A 10.10.2.2", ("CE-to-CE reachability across the core.", "Joignabilité CE à CE à travers le cœur."))],
 breakfix=[(("No send-community extended", "Pas de send-community extended"), ("VPNv4 routes arrive without route targets and are not imported into the VRF.", "Les routes VPNv4 arrivent sans route target et ne sont pas importées dans la VRF.")),
           (("Route-target mismatch", "Route targets différentes"), ("Routes are in the VPNv4 table but not in the VRF table on the other PE.", "Les routes sont dans la table VPNv4 mais pas dans la table VRF de l’autre PE.")),
           (("LDP disabled on one core link", "LDP désactivé sur un lien du cœur"), ("BGP is fine, but the label path breaks and VPN traffic is dropped at the P router.", "BGP fonctionne, mais le chemin labellisé est rompu et le trafic VPN est perdu sur le P."))],
 takeaways=[("RD = uniqueness, RT = membership. They are not the same thing.", "RD = unicité, RT = appartenance. Ce n’est pas la même chose."),
            ("The P router knows nothing about customers: that’s what makes MPLS scale.", "Le P ne connaît rien des clients : c’est ce qui fait passer MPLS à l’échelle."),
            ("Check control plane (BGP) and data plane (labels) separately.", "Vérifier séparément le plan de contrôle (BGP) et le plan de données (labels).")]),

# ─────────────────────────── 6. STP & LACP ───────────────────────────
dict(id="switching-resilience", tags="Switching · STP · LACP", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("STP & LACP resilience", "Résilience STP & LACP"),
 focus=("Root placement, guards, EtherChannel", "Placement de la racine, protections, EtherChannel"),
 objective=("Make a looped switch triangle predictable: Rapid PVST+ with a planned root per VLAN, an LACP bundle between the distribution switches, and guards that protect the topology at the edge.",
            "Rendre prévisible un triangle de commutateurs bouclé : Rapid PVST+ avec une racine prévue par VLAN, un agrégat LACP entre les distributions et des protections en bordure."),
 nodes=[("D1", "DSW1", "root VLAN 10", 200, 60, "rt"), ("D2", "DSW2", "root VLAN 20", 480, 60, "rt"), ("A", "ASW1", "access", 340, 230, "sw")],
 links=[("D1", "D2", "Po1 · LACP 2×1G", "h"), ("D1", "A", "trunk", ""), ("D2", "A", "trunk", "")],
 addressing=[["DSW1 ↔ DSW2", "Gi0/1–2 → Po1", "trunk 10,20"], ["DSW1 / DSW2 → ASW1", "Gi0/3", "trunk 10,20"], ["ASW1", "Gi1/0–3", "access VLAN 10 / 20"]],
 steps=[
  (("Rapid PVST+ and root placement", "Rapid PVST+ et placement de la racine"), ("Split roots per VLAN to use both uplinks.", "Répartir les racines par VLAN pour utiliser les deux liaisons montantes."), "DSW1", """
spanning-tree mode rapid-pvst
spanning-tree vlan 10 root primary
spanning-tree vlan 20 root secondary"""),
  (("LACP bundle", "Agrégat LACP"), ("Members must share speed, duplex and trunk settings.", "Les membres doivent partager vitesse, duplex et paramètres de trunk."), "DSW1 / DSW2", """
interface range GigabitEthernet0/1 - 2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 1 mode active
!
interface Port-channel1
 switchport trunk allowed vlan 10,20"""),
  (("Edge protection", "Protection en bordure"), ("PortFast + BPDU Guard on access ports, Root Guard on distribution ports facing access.", "PortFast + BPDU Guard sur les ports d’accès, Root Guard sur les ports de distribution vers l’accès."), "ASW1 / DSW1", """
! ASW1 access ports
interface range GigabitEthernet1/0 - 3
 spanning-tree portfast
 spanning-tree bpduguard enable
! DSW1 downlink to ASW1
interface GigabitEthernet0/3
 spanning-tree guard root
!
errdisable recovery cause bpduguard
errdisable recovery interval 300"""),
 ],
 verify=[("show spanning-tree vlan 10", ("DSW1 is root; one ASW1 uplink is Alternate/Blocking.", "DSW1 est racine ; une liaison de ASW1 est Alternate/Blocking.")),
         ("show etherchannel summary", ("Po1(SU) with members (P).", "Po1(SU) avec membres (P).")),
         ("show lacp neighbor", ("Partner seen on both members.", "Partenaire visible sur les deux membres.")),
         ("show spanning-tree inconsistentports", ("Empty in normal operation.", "Vide en fonctionnement normal."))],
 breakfix=[(("mode on vs mode active", "mode on contre mode active"), ("No bundle; members suspended. Use LACP active (or passive) on both sides.", "Pas d’agrégat ; membres suspendus. Utiliser LACP active (ou passive) des deux côtés.")),
           (("Rogue switch on an access port", "Commutateur pirate sur un port d’accès"), ("BPDU Guard puts the port err-disabled. Check <code>show interfaces status err-disabled</code>.", "BPDU Guard passe le port en err-disabled. Vérifier <code>show interfaces status err-disabled</code>.")),
           (("Better priority announced from access", "Meilleure priorité annoncée depuis l’accès"), ("Root Guard blocks it: the port goes root-inconsistent instead of moving the root.", "Root Guard la bloque : le port passe en root-inconsistent au lieu de déplacer la racine."))],
 takeaways=[("Never let STP elect the root by accident: place it.", "Ne jamais laisser STP élire la racine par hasard : la placer."),
            ("LACP negotiates; mode on hides mistakes.", "LACP négocie ; le mode on masque les erreurs."),
            ("Guards turn edge mistakes into a single err-disabled port instead of an outage.", "Les protections transforment une erreur en bordure en un seul port err-disabled, pas en panne.")]),

# ─────────────────────────── 7. SD-WAN ───────────────────────────
dict(id="sdwan-failover", tags="Fortinet · SD-WAN", level=("Intermediate", "Intermédiaire"), time="75 min",
 title=("SD-WAN path selection & failover", "SD-WAN : sélection de chemin & bascule"),
 focus=("SLA probes, steering rules, failover timing", "Sondes SLA, règles d’orientation, temps de bascule"),
 objective=("Give a FortiGate branch two internet links, measure them with SLA probes, steer traffic per application, then degrade a link with latency and loss to watch the decision change.",
            "Donner deux liens internet à une agence FortiGate, les mesurer avec des sondes SLA, orienter le trafic par application, puis dégrader un lien (latence, perte) pour observer le changement de décision."),
 nodes=[("BR", "FG-BRANCH", "FortiGate 7.4", 110, 150, "fw"), ("I1", "ISP-1", "Linux + netem", 340, 60, "cl"), ("I2", "ISP-2", "Linux + netem", 340, 240, "cl"), ("HQ", "FG-HQ", "probe target 10.1.0.10", 580, 150, "fw")],
 links=[("BR", "I1", "wan1", "h"), ("BR", "I2", "wan2", ""), ("I1", "HQ", "", "h"), ("I2", "HQ", "", "")],
 addressing=[["FG-BRANCH", "wan1 / wan2", "100.64.1.2/30 · 100.64.2.2/30"], ["ISP-1 / ISP-2", "eth1 → branch", "100.64.1.1 · 100.64.2.1"], ["FG-HQ", "LAN probe server", "10.1.0.10"]],
 steps=[
  (("Members and zone", "Membres et zone"), ("Both WAN interfaces in one SD-WAN zone, each with its gateway.", "Les deux interfaces WAN dans une zone SD-WAN, chacune avec sa passerelle."), "FG-BRANCH", """
config system sdwan
    set status enable
    config members
        edit 1
            set interface "wan1"
            set gateway 100.64.1.1
        next
        edit 2
            set interface "wan2"
            set gateway 100.64.2.1
        next
    end
end"""),
  (("SLA probe", "Sonde SLA"), ("500 ms probes; a member is dead after 3 failures and back after 5 successes.", "Sondes toutes les 500 ms ; un membre est mort après 3 échecs et rétabli après 5 succès."), "FG-BRANCH", """
config system sdwan
    config health-check
        edit "SLA-HQ"
            set server "10.1.0.10"
            set protocol ping
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
end"""),
  (("Steering rules", "Règles d’orientation"), ("VoIP stays on wan1 while it meets the SLA; bulk traffic prefers wan2.", "La VoIP reste sur wan1 tant que le SLA est respecté ; le trafic de masse préfère wan2."), "FG-BRANCH", """
config system sdwan
    config service
        edit 1
            set name "VOIP"
            set mode sla
            set dst "VOIP-SERVERS"
            config sla
                edit "SLA-HQ"
                    set id 1
                next
            end
            set priority-members 1 2
        next
        edit 2
            set name "BULK"
            set mode manual
            set dst "BACKUP-SERVERS"
            set priority-members 2 1
        next
    end
end"""),
  (("Degrade a link", "Dégrader un lien"), ("On the ISP-1 Linux node, add delay and loss, then remove it.", "Sur le nœud Linux ISP-1, ajouter latence et perte, puis les retirer."), "ISP-1 (Linux)", """
# add 150 ms delay and 5 % loss towards the branch
tc qdisc add dev eth1 root netem delay 150ms loss 5%
# restore
tc qdisc del dev eth1 root"""),
 ],
 verify=[("diagnose sys sdwan health-check", ("Per-member latency, jitter, loss and SLA state.", "Latence, gigue, perte et état SLA par membre.")),
         ("diagnose sys sdwan service", ("Which member the VOIP rule selects now.", "Le membre choisi par la règle VOIP à l’instant.")),
         ("diagnose sniffer packet any 'icmp' 4", ("Probes leaving on both members.", "Les sondes sortent sur les deux membres.")),
         ("execute ping-options source … + ping", ("Continuous test traffic while you degrade the link.", "Trafic de test continu pendant la dégradation."))],
 breakfix=[(("Probe server unreachable on one member", "Serveur de sonde injoignable sur un membre"), ("That member is always dead. Check routing and firewall policy for the probe path.", "Ce membre est toujours mort. Vérifier le routage et la politique de pare-feu sur le chemin de la sonde.")),
           (("Thresholds too tight", "Seuils trop serrés"), ("Traffic flaps between links. Raise thresholds or recovery time.", "Le trafic oscille entre les liens. Relever les seuils ou le temps de rétablissement.")),
           (("Rule never matches", "La règle ne correspond jamais"), ("Traffic falls to the implicit rule. Check rule order and the destination object.", "Le trafic tombe dans la règle implicite. Vérifier l’ordre des règles et l’objet destination."))],
 takeaways=[("Detection time ≈ interval × failtime. Tune it per application.", "Temps de détection ≈ interval × failtime. À ajuster par application."),
            ("A link can be up and still unusable: SLA probes catch that.", "Un lien peut être actif et pourtant inutilisable : les sondes SLA le détectent."),
            ("Always test failover with real degradation, not only a cable pull.", "Toujours tester la bascule avec une vraie dégradation, pas seulement un câble débranché.")]),

# ─────────────────────────── 8. FortiGate HA ───────────────────────────
dict(id="fortigate-ha", tags="Fortinet · HA", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("FortiGate HA cluster", "Cluster FortiGate HA"),
 focus=("Active-passive FGCP, session pickup, failover tests", "FGCP actif-passif, reprise de session, tests de bascule"),
 objective=("Build an active-passive FGCP cluster with two heartbeat links, monitored interfaces and session pickup, then fail the primary and check that sessions survive.",
            "Monter un cluster FGCP actif-passif avec deux liens de heartbeat, des interfaces surveillées et la reprise de session, puis faire tomber le primaire et vérifier que les sessions survivent."),
 nodes=[("W", "WAN switch", "", 340, 40, "sw"), ("F1", "FG-A (primary)", "priority 200", 200, 150, "fw"), ("F2", "FG-B (secondary)", "priority 100", 480, 150, "fw"), ("L", "LAN switch", "", 340, 260, "sw")],
 links=[("W", "F1", "port1", ""), ("W", "F2", "port1", ""), ("F1", "F2", "port3 + port4 heartbeat", "h"), ("F1", "L", "port2", ""), ("F2", "L", "port2", "")],
 addressing=[["Cluster", "port1 (WAN)", "203.0.113.2/29"], ["Cluster", "port2 (LAN)", "10.1.0.1/24"], ["FG-A / FG-B", "port5 (mgmt)", "10.99.0.11 · 10.99.0.12"], ["Heartbeat", "port3 / port4", "169.254.0.x (FGCP, automatic)"]],
 steps=[
  (("Same firmware, same model", "Même firmware, même modèle"), ("FGCP only forms between identical models and versions. Check with <code>get system status</code>.", "FGCP ne se forme qu’entre modèles et versions identiques. Vérifier avec <code>get system status</code>."), "FG-A / FG-B", """
get system status"""),
  (("HA settings (primary)", "Paramètres HA (primaire)"), ("Two heartbeat links, monitored data ports, session pickup.", "Deux liens de heartbeat, ports de données surveillés, reprise de session."), "FG-A", """
config system ha
    set group-name "FG-CLUSTER"
    set group-id 10
    set mode a-p
    set password ENC ********
    set hbdev "port3" 50 "port4" 50
    set session-pickup enable
    set override disable
    set priority 200
    set monitor "port1" "port2"
    set ha-mgmt-status enable
    config ha-mgmt-interfaces
        edit 1
            set interface "port5"
            set gateway 10.99.0.254
        next
    end
end"""),
  (("Secondary", "Secondaire"), ("Same settings, lower priority. The config syncs from the primary once the cluster forms.", "Mêmes paramètres, priorité plus basse. La configuration se synchronise depuis le primaire une fois le cluster formé."), "FG-B", """
config system ha
    set group-name "FG-CLUSTER"
    set group-id 10
    set mode a-p
    set password ENC ********
    set hbdev "port3" 50 "port4" 50
    set session-pickup enable
    set override disable
    set priority 100
    set monitor "port1" "port2"
end"""),
 ],
 verify=[("get system ha status", ("Both units listed, primary and secondary identified.", "Les deux unités listées, primaire et secondaire identifiés.")),
         ("diagnose sys ha checksum cluster", ("Identical checksums on both units.", "Checksums identiques sur les deux unités.")),
         ("execute ha manage 1 admin", ("CLI on the secondary from the primary.", "CLI du secondaire depuis le primaire.")),
         ("diagnose sys session list (on secondary)", ("Sessions present when session-pickup is on.", "Sessions présentes quand session-pickup est actif."))],
 breakfix=[(("Different firmware", "Firmwares différents"), ("No cluster forms. Upgrade one unit before joining.", "Aucun cluster ne se forme. Mettre à niveau une unité avant de la joindre.")),
           (("Single heartbeat link cut", "Coupure de l’unique lien de heartbeat"), ("Both units become primary (split brain). Always use two heartbeat links.", "Les deux unités deviennent primaires (split brain). Toujours utiliser deux liens de heartbeat.")),
           (("Monitored port down on the primary", "Port surveillé tombé sur le primaire"), ("Failover to the secondary, as expected. With override disabled, it stays there after recovery.", "Bascule vers le secondaire, comme prévu. Avec override désactivé, il le reste après le retour."))],
 takeaways=[("Two heartbeats, monitored ports and session pickup are the minimum.", "Deux heartbeats, des ports surveillés et la reprise de session sont le minimum."),
            ("Override disabled avoids a second failover when the old primary comes back.", "Override désactivé évite une seconde bascule quand l’ancien primaire revient."),
            ("Test failover with live sessions, not just pings.", "Tester la bascule avec des sessions actives, pas seulement des pings.")]),

# ─────────────────────────── 9. Ansible ───────────────────────────
dict(id="ansible-network", tags="Automation · Ansible", level=("Intermediate", "Intermédiaire"), time="60 min",
 title=("Ansible network automation", "Automatisation réseau Ansible"),
 focus=("Inventory, config backups, idempotent changes", "Inventaire, sauvegardes, changements idempotents"),
 objective=("Use Ansible to back up every router configuration, push a standard NTP and logging baseline, and prove the change is idempotent with check mode.",
            "Utiliser Ansible pour sauvegarder la configuration de chaque routeur, déployer une base NTP et journalisation standard, et prouver l’idempotence avec le mode check."),
 nodes=[("A", "Ansible host", "Linux · 10.99.0.5", 340, 50, "sv"), ("R1", "R1", "10.99.0.11", 160, 220, "rt"), ("R2", "R2", "10.99.0.12", 340, 220, "rt"), ("R3", "R3", "10.99.0.13", 520, 220, "rt")],
 links=[("A", "R1", "SSH", "t"), ("A", "R2", "SSH", "t"), ("A", "R3", "SSH", "t")],
 addressing=[["Ansible host", "eth0", "10.99.0.5/24"], ["R1–R3", "Gi0/3 (mgmt)", "10.99.0.11–13/24"]],
 steps=[
  (("Inventory", "Inventaire"), ("Group the routers and set the network connection. The password comes from Ansible Vault.", "Grouper les routeurs et définir la connexion réseau. Le mot de passe vient d’Ansible Vault."), "inventory.yml", """
all:
  children:
    ios:
      hosts:
        r1: { ansible_host: 10.99.0.11 }
        r2: { ansible_host: 10.99.0.12 }
        r3: { ansible_host: 10.99.0.13 }
      vars:
        ansible_network_os: cisco.ios.ios
        ansible_connection: ansible.netcommon.network_cli
        ansible_user: netadmin
        ansible_password: "{{ vault_ios_password }}"
        ansible_become: true
        ansible_become_method: enable"""),
  (("Back up configurations", "Sauvegarder les configurations"), ("One file per device in ./backups.", "Un fichier par équipement dans ./backups."), "backup.yml", """
- name: Backup running configs
  hosts: ios
  gather_facts: false
  tasks:
    - name: Save running-config
      cisco.ios.ios_config:
        backup: true
        backup_options:
          dir_path: ./backups
          filename: "{{ inventory_hostname }}.cfg\""""),
  (("Push a baseline", "Déployer une base commune"), ("Only missing lines are sent. Save the config only if something changed.", "Seules les lignes manquantes sont envoyées. La config n’est sauvegardée que si quelque chose a changé."), "baseline.yml", """
- name: NTP and logging baseline
  hosts: ios
  gather_facts: false
  tasks:
    - name: Ensure NTP and syslog
      cisco.ios.ios_config:
        lines:
          - ntp server 10.99.0.1
          - logging host 10.99.0.20
          - service timestamps log datetime msec
        save_when: changed"""),
 ],
 verify=[("ansible-playbook -i inventory.yml backup.yml", ("One .cfg per router in ./backups.", "Un .cfg par routeur dans ./backups.")),
         ("ansible-playbook -i inventory.yml baseline.yml --check --diff", ("Shows the lines that would be added, changes nothing.", "Affiche les lignes qui seraient ajoutées, sans rien modifier.")),
         ("ansible-playbook -i inventory.yml baseline.yml  (run twice)", ("Second run: changed=0 (idempotent).", "Second passage : changed=0 (idempotent).")),
         ("ansible ios -i inventory.yml -m cisco.ios.ios_command -a \"commands='show run | i ntp'\"", ("NTP line present on every router.", "Ligne NTP présente sur chaque routeur."))],
 breakfix=[(("Unknown SSH host key", "Clé d’hôte SSH inconnue"), ("Connection refused on first run. Add the keys to known_hosts (do not disable checking in production).", "Connexion refusée au premier passage. Ajouter les clés à known_hosts (ne pas désactiver la vérification en production).")),
           (("Privilege level too low", "Niveau de privilège insuffisant"), ("Config commands fail. Set become with method enable.", "Les commandes de config échouent. Définir become avec la méthode enable.")),
           (("Line written differently on the device", "Ligne écrite différemment sur l’équipement"), ("Task reports changed every run. Match the exact running-config syntax.", "La tâche indique changed à chaque passage. Reprendre exactement la syntaxe de la running-config."))],
 takeaways=[("Back up before you automate changes.", "Sauvegarder avant d’automatiser des changements."),
            ("Check mode with diff is your change review.", "Le mode check avec diff, c’est votre revue de changement."),
            ("Idempotence (changed=0 on rerun) proves the playbook describes a state, not a script.", "L’idempotence (changed=0 au second passage) prouve que le playbook décrit un état, pas un script.")]),

# ─────────────────────────── 10. SNMP / Zabbix ───────────────────────────
dict(id="snmp-zabbix", tags="Monitoring · SNMPv3", level=("Beginner", "Débutant"), time="45 min",
 title=("SNMPv3 monitoring with Zabbix", "Supervision SNMPv3 avec Zabbix"),
 focus=("SNMPv3 authPriv, templates, triggers", "SNMPv3 authPriv, modèles, déclencheurs"),
 objective=("Secure SNMP with v3 authPriv on a switch, test it from the Zabbix server with snmpwalk, add the device with a vendor template and fire a trigger by shutting an interface.",
            "Sécuriser SNMP en v3 authPriv sur un commutateur, le tester depuis le serveur Zabbix avec snmpwalk, ajouter l’équipement avec un modèle constructeur et déclencher une alerte en coupant une interface."),
 nodes=[("Z", "Zabbix server", "10.10.50.20", 160, 140, "sv"), ("S", "SW1", "10.10.50.2", 420, 140, "sw"), ("H", "Host", "Gi0/5", 600, 140, "sv")],
 links=[("Z", "S", "UDP 161 (poll) · 162 (traps)", "h"), ("S", "H", "", "")],
 addressing=[["Zabbix server", "eth0", "10.10.50.20/24"], ["SW1", "Vlan50 (mgmt)", "10.10.50.2/24"]],
 steps=[
  (("SNMPv3 on the switch", "SNMPv3 sur le commutateur"), ("authPriv (SHA + AES), read-only view, and an ACL so only Zabbix can poll.", "authPriv (SHA + AES), vue en lecture seule, et une ACL pour que seul Zabbix puisse interroger."), "SW1", """
ip access-list standard ACL-NMS
 permit 10.10.50.20
!
snmp-server view NMS-VIEW iso included
snmp-server group NMS v3 priv read NMS-VIEW access ACL-NMS
snmp-server user zabbix NMS v3 auth sha <redacted> priv aes 128 <redacted>
snmp-server host 10.10.50.20 version 3 priv zabbix
snmp-server enable traps snmp linkdown linkup"""),
  (("Test from the server", "Tester depuis le serveur"), ("If snmpwalk fails, Zabbix will too. Fix it here first.", "Si snmpwalk échoue, Zabbix échouera aussi. Corriger d’abord ici."), "Zabbix server", """
snmpwalk -v3 -l authPriv -u zabbix \\
  -a SHA -A '<auth-pass>' -x AES -X '<priv-pass>' \\
  10.10.50.2 1.3.6.1.2.1.1"""),
  (("Add the host in Zabbix", "Ajouter l’hôte dans Zabbix"), ("Data collection → Hosts → Create host: SNMP interface 10.10.50.2, SNMPv3 authPriv credentials, template for the vendor (for example <em>Cisco IOS by SNMP</em>).", "Collecte de données → Hôtes → Créer un hôte : interface SNMP 10.10.50.2, identifiants SNMPv3 authPriv, modèle du constructeur (par exemple <em>Cisco IOS by SNMP</em>)."), "Zabbix UI", """
Host name      : SW1
Interface      : SNMP 10.10.50.2:161
SNMP version   : SNMPv3
Security level : authPriv
Auth / Priv    : SHA / AES
Template       : Cisco IOS by SNMP"""),
 ],
 verify=[("snmpwalk … 1.3.6.1.2.1.1", ("sysDescr, sysName and sysUpTime returned.", "sysDescr, sysName et sysUpTime retournés.")),
         ("Zabbix → Monitoring → Latest data", ("Interface and CPU items updating.", "Items interfaces et CPU mis à jour.")),
         ("shutdown Gi0/5 on SW1", ("Link down problem appears in Zabbix within the polling interval.", "Le problème link down apparaît dans Zabbix dans l’intervalle de collecte.")),
         ("no shutdown", ("Problem resolves automatically.", "Le problème se résout automatiquement."))],
 breakfix=[(("Wrong auth or priv password", "Mot de passe auth ou priv erroné"), ("snmpwalk returns an authentication failure or decryption error. Re-create the user.", "snmpwalk renvoie un échec d’authentification ou une erreur de déchiffrement. Recréer l’utilisateur.")),
           (("ACL doesn’t include the server", "L’ACL n’inclut pas le serveur"), ("Timeouts only. Check the ACL hit counters.", "Uniquement des timeouts. Vérifier les compteurs de l’ACL.")),
           (("Security level mismatch", "Niveau de sécurité différent"), ("Zabbix set to authNoPriv against a priv user: no data. Align on authPriv.", "Zabbix en authNoPriv face à un utilisateur priv : aucune donnée. Aligner sur authPriv."))],
 takeaways=[("SNMPv1/v2c send the community in clear text; use v3 authPriv.", "SNMPv1/v2c envoient la communauté en clair ; utiliser v3 authPriv."),
            ("Always prove SNMP with snmpwalk before blaming the monitoring tool.", "Toujours valider SNMP avec snmpwalk avant d’accuser l’outil de supervision."),
            ("Start from vendor templates, then tune triggers to cut noise.", "Partir des modèles constructeur, puis ajuster les déclencheurs pour réduire le bruit.")]),
]


def lab_sections(x, lab):
    t = x.t
    s = []
    s.append(("objective", t("Objective", "Objectif"),
              f"<h2>{t('Objective', 'Objectif')}</h2><p>{t(*lab['objective'])}</p>"
              + f"<h3>{t('Prerequisites', 'Prérequis')}</h3>"
              + bullets([t('EVE-NG (Community or Pro) with the images listed in the topology.', 'EVE-NG (Community ou Pro) avec les images indiquées dans la topologie.'),
                         t('Console access to every node; basic CLI knowledge.', 'Accès console à chaque nœud ; bases de la CLI.')])))
    s.append(("topology", t("Topology", "Topologie"),
              f"<h2>{t('Topology &amp; addressing', 'Topologie &amp; adressage')}</h2>"
              + topo_svg(lab["nodes"], lab["links"], w=680, h=300, zones=lab.get("zones", ()), caption=t(*lab["title"]))
              + table([t('Device', 'Équipement'), 'Interface', t('Address / role', 'Adresse / rôle')], lab["addressing"])))
    body = ""
    for i, (title, text, dev, cfg) in enumerate(lab["steps"], 1):
        body += f"<h3>{i}. {t(*title)}</h3><p>{t(*text)}</p>" + code(dev, cfg)
    s.append(("build", t("Build", "Construction"), f"<h2>{t('Build it step by step', 'Construction pas à pas')}</h2>{body}"))
    s.append(("verify", t("Verify", "Vérifier"),
              f"<h2>{t('Verify', 'Vérifier')}</h2>"
              + table([t('Command', 'Commande'), t('What you should see', 'Ce que vous devez voir')],
                      [[f"<code>{c}</code>", t(*e)] for c, e in lab["verify"]])))
    bf = "".join(f'<details><summary><span class="tag">{t("break", "panne")}</span>{t(*ti)}</summary><p>{t(*hint)}</p></details>' for ti, hint in lab["breakfix"])
    s.append(("breakfix", t("Break / fix", "Pannes à corriger"),
              f"<h2>{t('Break it, then fix it', 'Casser, puis réparer')}</h2><p>{t('Introduce each fault, observe the symptom, then open the hint.', 'Introduisez chaque panne, observez le symptôme, puis ouvrez l’indice.')}</p><div class=\"bf\">{bf}</div>"))
    s.append(("takeaways", t("Takeaways", "À retenir"), f"<h2>{t('Key takeaways', 'À retenir')}</h2>" + bullets([t(*k) for k in lab["takeaways"]])))
    s.append(("status", t("Publication", "Publication"),
              f"<h2>{t('Publication status', 'État de publication')}</h2>"
              + '<ul class="check">'
              + f'<li class="ok">{t("Objective, topology &amp; addressing", "Objectif, topologie &amp; adressage")}</li>'
              + f'<li class="ok">{t("Step-by-step configuration", "Configuration pas à pas")}</li>'
              + f'<li class="ok">{t("Verification commands &amp; expected results", "Commandes de vérification &amp; résultats attendus")}</li>'
              + f'<li class="ok">{t("Break / fix scenarios", "Scénarios de panne")}</li>'
              + f'<li class="todo">{t("Screenshots &amp; real command outputs from my lab", "Captures &amp; sorties réelles de mon lab")}</li>'
              + f'<li class="todo">{t("EVE-NG .unl export", "Export EVE-NG .unl")}</li></ul>'))
    return s
