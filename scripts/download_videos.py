import csv
import subprocess

with open('../videos_info.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for i, row in enumerate(reader):
        if i == 0:
            continue
        video_id = row[0]
        link = row[1]
        subprocess.run(['yt-dlp', link, '-f bestvideo[ext=mp4]+bestaudio[ext=m4a]', f'-o videos/{video_id}.%(ext)s'])
        if i == 2:
            break