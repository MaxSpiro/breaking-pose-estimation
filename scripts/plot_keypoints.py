import cv2
from pathlib import Path
from PIL import Image
import numpy as np
import random

# Constants
INPUT_IMAGES = Path("../dataset/images")
INPUT_LABELS = Path("../dataset/labels")
OUTPUT_DIR = Path("../visualize")
# subprocess.run(["rm", "-rf", OUTPUT_DIR])
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_SAMPLES = 1000

CLASS_NAMES = ["toprock", "footwork", "powermove"]

# Ultralytics-style color palettes
CLASS_COLORS = [(255, 56, 56), (72, 249, 10), (146, 204, 23)]
KEYPOINT_COLORS = [
    (255, 0, 0),
    (255, 85, 0),
    (255, 170, 0),
    (255, 255, 0),
    (170, 255, 0),
    (85, 255, 0),
    (0, 255, 0),
    (0, 255, 85),
    (0, 255, 170),
    (0, 255, 255),
    (0, 170, 255),
    (0, 85, 255),
    (0, 0, 255),
    (85, 0, 255),
    (170, 0, 255),
    (255, 0, 255),
    (255, 0, 170),
]

# Random image selection
all_images = list(INPUT_IMAGES.glob("*.png"))
random.shuffle(all_images)
selected_images = all_images[:NUM_SAMPLES]

for image_path in selected_images:
    label_path = INPUT_LABELS / f"{image_path.stem}.txt"
    if not label_path.exists():
        print(f"Label not found for {image_path.stem}")
        continue

    img_pil = Image.open(image_path).convert("RGB")
    img = np.array(img_pil)
    height, width, _ = img.shape

    draw_img = img.copy()

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        bbox = list(map(float, parts[1:5]))
        keypoints = list(map(float, parts[5:]))

        # Convert bbox to pixel coordinates
        x_center, y_center, w, h = bbox
        x_center *= width
        y_center *= height
        w *= width
        h *= height
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        x2 = int(x_center + w / 2)
        y2 = int(y_center + h / 2)

        # Draw bounding box
        box_color = CLASS_COLORS[class_id]
        cv2.rectangle(draw_img, (x1, y1), (x2, y2), box_color, 2)

        # Draw class name
        label = (
            CLASS_NAMES[class_id]
            if class_id < len(CLASS_NAMES)
            else f"class {class_id}"
        )
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(label, font, 0.5, 1)[0]
        text_origin = (x1, max(y1 - 4, text_size[1] + 4))
        cv2.rectangle(
            draw_img,
            (x1, y1 - text_size[1] - 8),
            (x1 + text_size[0], y1),
            box_color,
            -1,
        )
        cv2.putText(
            draw_img, label, (x1, y1 - 4), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA
        )

        # Draw keypoints (assuming format: x1 y1 x2 y2 ...)
        points = []
        for i in range(0, len(keypoints), 2):
            x = int(keypoints[i] * width)
            y = int(keypoints[i + 1] * height)
            cv2.circle(
                draw_img,
                (x, y),
                9,
                KEYPOINT_COLORS[(i // 2) % len(KEYPOINT_COLORS)],
                -1,
            )
            points.append((x, y))

    # Save visualization
    output_path = OUTPUT_DIR / image_path.name
    cv2.imwrite(str(output_path), cv2.cvtColor(draw_img, cv2.COLOR_RGB2BGR))
