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
    sorted_frames = sorted(frame_nums)
    select_expr = "+".join(f"eq(n\\,{int(fn)})" for fn in sorted_frames)
    tmp_output_pattern = f'{video_id}-%d.png'
    subprocess.run(
        [
            "./ffmpeg",
            "-i",
            str(input_video),
            "-vf",
            f"select={select_expr},scale=640:360",
            "-vsync",
            "0",
            "-sws_flags",
            "lanczos",
            "-frames:v",
            str(len(sorted_frames)),
            str(images_dir / tmp_output_pattern),
        ]
    )
    for i, frame_num in enumerate(sorted_frames):
        tmp_path = images_dir / f'{video_id}-{i}.png'
        final_path = images_dir / f'{video_id}-{frame_num}.png'
        if tmp_path.exists():
            tmp_path.rename(final_path)
            print(f'Saved to {final_path}')
