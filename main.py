import subprocess
import sys

# Hardcoded settings
STREAM_URL = "http://47.181.86.62:8082/mjpg/video.mjpg"
AUDIO_FILE = "officeambience.mp3"
TWITCH_STREAM_KEY = "live_1546915000_CyHQRHDFlgVtzwra4qnA6OGbTndd2z"

TWITCH_RTMP_URL = f"rtmp://live.twitch.tv/app/{TWITCH_STREAM_KEY}"


def stream_to_twitch():
    ffmpeg_cmd = [
        "ffmpeg",
        # Input 0: Video Stream (MJPEG)
        "-use_wallclock_as_timestamps",
        "1",
        "-i",
        STREAM_URL,
        # Input 1: Background Audio (Loop infinitely)
        "-stream_loop",
        "-1",
        "-i",
        AUDIO_FILE,
        # Video encoding parameters
        "-r",
        "15",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-tune",
        "zerolatency",
        "-g",
        "30",  # Keyframe every 2 seconds (15 fps * 2s)
        "-b:v",
        "1500k",
        "-maxrate",
        "1500k",
        "-bufsize",
        "3000k",
        "-pix_fmt",
        "yuv420p",
        # Audio encoding parameters
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        # Stream Mapping
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        # Output format
        "-f",
        "flv",
        TWITCH_RTMP_URL,
    ]

    print("Starting continuous stream to Twitch...")

    try:
        process = subprocess.Popen(
            ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        for line in process.stdout:
            print(line, end="")

        process.wait()

    except KeyboardInterrupt:
        print("\nStopping stream...")
        process.terminate()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    stream_to_twitch()