## Vulnerability Exploitations of a Wi-Fi Cloud Camera
**Deniz Ozen, Kuzey Hamidoglu, Arda Dinsoy**\
_2IC80 - Lab on Offensive Computer Security, \
Eindhoven University of Technology
2023-2024_

### About
This toolkit is designed to provide tools for network security testing and stream recording and processing, utilizing Python for various tasks including ARP spoofing, DOS attacks, and video stream recording and conversion.

### Features

- **ARP Spoofing**: Manipulate ARP tables to intercept or alter network traffic between devices.
- **DOS Attacks**: Perform denial of service tests to evaluate network robustness.
- **Stream Recording**: Capture RTSP video streams, storing them locally.
- **Stream Processing**: Convert video files to different formats and manage video storage. This includes processing video files to optimize them for various playback scenarios.

### Prerequisites
We recommend the installation of these packages to ensure an end-to-end process with no errors.
- Python 3.6 or higher
- FFmpeg (for stream recording and processing)
```plaintext
scapy==2.5.0
matplotlib==3.9.0
```

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/deniz0zn/2IC80-Deep-CS-Final-Project
    cd 2IC80-Deep-CS-Final-Project
    ```

2. **Install Python Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **FFmpeg Installation**

    - **Ubuntu/Linux**:

      ```bash
      sudo apt update
      sudo apt install ffmpeg
      ```

    - **macOS** (using Homebrew):

      ```bash
      brew install ffmpeg
      ```

    - **Windows**:
      - Download the builds from [FFmpeg Official Site](https://ffmpeg.org/download.html).
      - Add FFmpeg to your system path.
      - [Video Guide for setting up FFmpeg](https://www.youtube.com/watch?v=r1AtmY-RMyQ)

### Usage

1. **Running the Main Menu**
    - Navigate to the project directory and run:
      
      ```bash
      python main.py
      ```

    - Follow the on-screen prompts to select and execute tasks such as ARP spoofing, DOS attacks, stream recording, or stream processing.

2. **Using Stream Processing**
    - The `process_stream.py` script can be used independently to convert and manage video files:
      
      ```bash
      python process_stream.py --dir=<directory_with_videos> --cleanup
      ```

    - This script provides functionality to convert videos to MP4, remove unnecessary files, and reorganize video storage.

3. **Configuration**
    - Adjust settings like target IP addresses and credentials in the `targets.txt` file:
      
      ```plaintext
      victim = <VICTIM IP>
      router = <ROUTER IP>
      username = <USERNAME>
      password = <PASSWORD>
      ```

### License

This project is licensed under MIT Licence. For more details, see the LICENSE file.

### Disclaimer

This toolkit is for educational and ethical testing purposes only. Usage of this software for attacking targets without prior mutual consent is illegal. The developers assume no liability and are not responsible for any misuse or damage caused by this program.


