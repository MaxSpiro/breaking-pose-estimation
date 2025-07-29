from pathlib import Path
import subprocess

IMAGES_DIR = Path("../dataset/images")
IMAGES_DIR.mkdir(exist_ok=True)
LABELS_DIR = Path("../dataset/labels")
VIDEOS_DIR = Path("../videos")


def extract_frames(video_path: Path):
    video_id = video_path.stem
    with open("highest_frames.txt", "r") as highest_frames:
        for line in highest_frames.readlines():
            video_id, max_frame = line.strip().rsplit(":", 1)
            max_frame = int(max_frame.strip()) + 10
    print(f"Extracting {max_frame} frames from {video_id}")
    subprocess.run(
        [
            "./ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            "scale=640:360",
            "-vframes",
            str(max_frame or 12000),
            str(IMAGES_DIR / f"{video_id}-%06d.png"),
        ]
    )
    # remove unnecessary frames
    for image_path in Path(IMAGES_DIR).glob(f"{video_id}*.png"):
        if not Path(f"{LABELS_DIR}/{image_path.stem}.txt").exists():
            image_path.unlink()
    print("Extracted frames for " + video_id)
    video_path.unlink()


if __name__ == "__main__":
    for video in VIDEOS_DIR.iterdir():
        extract_frames(video)
