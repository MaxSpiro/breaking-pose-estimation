import csv
import subprocess

# Uses yt-dlp and ffmpeg
if __name__ == '__main__':
    with open('../videos_info.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                continue
            video_id = row[0]
            link = row[1]
            ytdl_command = ['yt-dlp', link, '-f bestvideo[ext=mp4]', f'-o videos/{video_id}.%(ext)s']
            subprocess.run(ytdl_command)