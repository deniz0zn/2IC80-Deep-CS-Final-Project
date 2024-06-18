import subprocess
import os
# Define the command as a list of elements
# command = [
#     'ffmpeg',
#     '-fflags', '+genpts+igndts',
#     '-rtbufsize', '500M',
#     '-i', 'rtsp://admin:123456@192.168.88.123/channel1',
#     '-c', 'copy',
#     '-t', '180',  # Duration in seconds
#     'output14.mkv'
# ]

def record_stream(url, format='mkv', directory_path = 'Videos'):
    """
    Record a video stream using FFmpeg and save it to a specified file.

    Args:
    url (str): URL of the stream, including credentials.
    output_path (str): Path where the recorded video will be saved.
    format (str): Format of the output file ('mkv' or 'avi').

    Returns:
    None
    """
    # Construct the FFmpeg command

    i = 1
    while True:
        new_filename = f"{'output'}{i}.{'mkv'}"
        output_path = os.path.join(directory_path, new_filename)
        if not os.path.exists(output_path):
            break
        i += 1


    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',   # Use TCP for RTSP transport
        '-i', url,                  # Input URL of the stream
        '-c', 'copy',               # Use stream copy mode to avoid re-encoding
        '-t', '60',               # Duration to record in seconds, e.g., 3600 seconds for 1 hour
        output_path                 # Output file path
    ]

    # Adjust the format if specified
    if format == 'avi':
        command.append('-f')
        command.append('avi')
    elif format == 'mkv':
        command.append('-f')
        command.append('mkv')

    # Execute the FFmpeg command and handle the output
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


record_stream('rtsp://admin:123456@192.168.88.123/channel1',format='mkv')
