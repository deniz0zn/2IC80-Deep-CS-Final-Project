import subprocess
import os

class StreamRecorder:
    def __init__(self, url, directory_path='Videos'):
        self.url = url
        self.directory_path = directory_path
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)  # Ensure the directory exists

    def generate_unique_filename(self):
        """Generates a unique filename for the recording."""
        i = 1
        while True:
            new_filename = f"output{i}.mkv"  # Always use .mkv format
            output_path = os.path.join(self.directory_path, new_filename)
            if not os.path.exists(output_path):
                return output_path
            i += 1

    def record(self):
        """Records a video stream using FFmpeg."""
        output_path = self.generate_unique_filename()

        command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', self.url,
            '-c', 'copy',
            '-t', '60',  # Duration in seconds
            output_path  # Directly specify the output path with the .mkv extension
        ]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stderr.readline()
                if process.poll() is not None and output == '':
                    break
                if output:
                    print(output.strip())
            process.poll()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during recording: {e}")
        finally:
            if process.returncode and process.returncode != 0:
                print("FFmpeg terminated with an error:", process.returncode)
            else:
                print(f"Recording completed successfully, output saved to {output_path}")
