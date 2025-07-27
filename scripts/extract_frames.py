from pathlib import Path
import subprocess
from collections import defaultdict

labels_dir = Path("../yolo_dataset/labels")
images_dir = Path("../yolo_dataset/images")
videos_dir = Path("../videos")

video_to_frames = defaultdict(set)

for label_path in labels_dir.iterdir():
    video_id, frame_num = label_path.stem.rsplit("-", 1)
    output_path = images_dir / f"{video_id}-{frame_num}.png"
    if not output_path.exists():
        video_to_frames[video_id].add(frame_num)

for video_id, frame_nums in video_to_frames.items():
    input_video = videos_dir / f"{video_id}.mp4"
    if not input_video.exists():
        print(f"Video {video_id} not found.")
        continue
    subprocess.run(
        [
            "./ffmpeg",
            "-i",
            str(input_video),
            str(images_dir / f"{video_id}-%d.png"),
        ]
    )
