import numpy as np
from pathlib import Path
import json

frame_width, frame_height = 1920, 1080
classnames = {"toprock": 0, "footwork": 1, "powermove": 2}


def get_box_from_keypoints(keypoints):
    box_x1, box_y1 = keypoints[:, :2].min(axis=0)
    box_x2, box_y2 = keypoints[:, :2].max(axis=0)
    box_x1 -= 100
    box_y1 -= 100
    box_x2 += 100
    box_y2 += 100
    w = box_x2 - box_x1
    h = box_y2 - box_y1
    box = ((box_x2 + box_x1) / 2, (box_y2 + box_y1) / 2, w, h)
    return box


# Make sure to run this script in the scripts folder, with manual_keypoints in the same level as scripts
if __name__ == "__main__":
    for path in Path("../manual_keypoints").rglob("*.npz"):
        keypoints = np.load(path)["coco_joints2d"][:, :2]
        _, _, year, video_id, img_id = str(path).rsplit(".", 1)[0].split("/")
        if video_id != "k1RTNQxNt6Q":
            continue
        frame_num = img_id.split("-")[1]
        for data_path in Path(f"../dataset/{year}/{video_id}").rglob("*.json"):
            _, frame_range, classname_and_ending = str(data_path).rsplit("_", 2)
            low, high = int(frame_range.split("-")[0]), int(frame_range.split("-")[1])
            if low <= int(frame_num) <= high:
                classname = classname_and_ending.split(".")[0]
                break
        x, y, w, h = get_box_from_keypoints(keypoints)
        normalized_x = str.format("{0:.6f}", x / frame_width)
        normalized_y = str.format("{0:.6f}", y / frame_height)
        normalized_w = str.format("{0:.6f}", w / frame_width)
        normalized_h = str.format("{0:.6f}", h / frame_height)
        normalized_keypoints = [
            (
                str.format("{0:.6f}", keypoints[i][0] / frame_width),
                str.format("{0:.6f}", keypoints[i][1] / frame_height),
            )
            for i in range(len(keypoints))
        ]
        filename = f"{video_id}-{frame_num.rjust(6, '0')}.txt"
        with open("../yolo_dataset/labels/" + filename, "w") as f:
            class_num = str(classnames[classname])
            f.write(
                class_num
                + " "
                + normalized_x
                + " "
                + normalized_y
                + " "
                + normalized_w
                + " "
                + normalized_h
                + " "
                + " ".join([f"{x} {y}" for x, y in normalized_keypoints])
            )
