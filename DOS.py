from scapy.all import IP, TCP, send
import time

def send_packets(destination_ip, destination_port, duration, rate):
    packet = IP(dst=destination_ip) / TCP(dport=destination_port)
    end_time = time.time() + duration
    while time.time() < end_time:
        send(packet)
        time.sleep(1 / rate)

# Example usage:
if __name__ == "__main__":
    target_ip = "192.168.88.123"
    target_port = 8080
    duration = 60*5  # duration in seconds
    rate = 100  # packets per second
    send_packets(target_ip, target_port, duration, rate)
