# 2IC80-Deep-CS-Final-Project

This toolkit provides utilities for ARP spoofing and network stream recording, designed for network security testing and educational purposes. The toolkit includes three main components: `main.py`, `arp_spoof.py`, and `record_stream.py`, which are managed through a simple text-based menu.

### Features

- **ARP Spoofing**: Manipulate ARP tables to intercept or alter network traffic between devices.
- **Network Stream Recording**: Capture video streams using RTSP, storing the data securely for analysis.

### Prerequisites

Before you install and run this toolkit, ensure you have the following installed:

- Python 3.6 or higher
- FFmpeg for handling video streams

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/deniz0zn/2IC80-Deep-CS-Final-Project.git
cd 2IC80-Deep-CS-Final-Project
```

#### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install FFmpeg

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download the builds from [FFmpeg Official Site](https://ffmpeg.org/download.html).
- Add FFmpeg to your system path.

### Configuration

Edit the `targets.txt` file to set up the target configurations:

```plaintext
victim = <VICTIM IP>
router = <ROUTER IP>
username = <USERNAME>
password = <PASSWORD>
```

Ensure that the `targets.txt` file is in the same directory as the scripts or update the file path in `main.py` accordingly.

### Usage

Run the main script to start the menu-driven interface:

```bash
python main.py
```

Follow the on-screen prompts to select either ARP spoofing or network recording. Use the menu to safely stop all activities and exit the program:

1. Run ARP Spoofing
2. Run Network Recording
3. Stop all tasks and Exit

### Contributing

Contributions to this project are welcome. Please ensure to follow best practices for code changes and updates.

### License

This project is licensed under MIT License. For more details, see the LICENSE file.

### Disclaimer

This toolkit is for educational and ethical testing purposes only. Usage of this software for attacking targets without prior mutual consent is illegal. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---
