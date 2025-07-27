from pathlib import Path
import subprocess


if __name__ == '__main__':
    for path in Path('../yolo_dataset/labels').iterdir():
        video_id, frame_num = path.stem.rsplit('-', 1)
        if not Path(f'../yolo_dataset/images/{path.stem}.png').exists():
            subprocess.run([
                './ffmpeg',
                '-i', f'../videos/{video_id}.mp4',
                '-vf', f'select=eq(n\\,{int(frame_num)}),scale=640:360', '-sws_flags', 'lanczos',
                '-frames:v', '1',
                f'../yolo_dataset/images/{path.stem}.png'
            ])
            print(f'Saved to ../yolo_dataset/images/{path.stem}.png')