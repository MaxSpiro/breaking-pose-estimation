import csv
import subprocess
from pathlib import Path

Path("../videos").mkdir(exist_ok=True)

# Uses yt-dlp and ffmpeg
if __name__ == "__main__":
    with open("../videos_info.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for i, row in enumerate(reader):
            if i == 1:
                continue
            video_id = row[0]
            link = row[1]
            ytdl_command = [
                "yt-dlp",
                "-f",
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
                "-o",
                "../videos/%(id)s.%(ext)s",
                "--ffmpeg-location",
                "./ffmpeg",
                link,
            ]
            subprocess.run(ytdl_command)
