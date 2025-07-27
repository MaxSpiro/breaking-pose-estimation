import cv2
import matplotlib.pyplot as plt
import random
from pathlib import Path
from PIL import Image
import numpy as np

all_files = [f for f in Path('../yolo_dataset/images').iterdir()]
image_path = random.choice(all_files)
label_path = Path(f'../yolo_dataset/labels/{image_path.stem}.txt')
print(image_path)
print(label_path)

img_pil = Image.open(image_path).convert('RGB')
img = np.array(img_pil)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, _ = img.shape

# Read the label file
with open(label_path, 'r') as f:
    lines = f.readlines()

for line in lines:
    parts = line.strip().split()
    class_id = int(parts[0])
    bbox = list(map(float, parts[1:5]))
    keypoints = list(map(float, parts[5:]))

    # Convert bbox to pixel coords
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
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw keypoints
    for i in range(0, len(keypoints), 2):
        kp_x = int(keypoints[i] * width)
        kp_y = int(keypoints[i+1] * height)
        cv2.circle(img, (kp_x, kp_y), radius=3, color=(255, 0, 0), thickness=-1)

plt.imshow(img)
plt.axis('off')
plt.show()
