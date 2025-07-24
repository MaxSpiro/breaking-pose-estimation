import numpy as np
from pathlib import Path
import json

frame_width, frame_height = 1920, 1080

if __name__ == "__main__":
    for path in Path('../manual_keypoints').rglob('*.npz'):
        keypoints = np.load(path)['coco_joints2d'][:, :2]
        path_str = str(path)
        _, _, year, video_id, img_id = path_str.rsplit('.', 1)[0].split('/')
        frame_num = int(img_id.split('.')[0].split('-')[1])
        sequence_path = None
        for data_path in Path(f'../dataset/{year}/{video_id}').rglob('*.json'):
            _, frame_range, _ = str(data_path).split('_')
            low, high = int(frame_range.split('-')[0]), int(frame_range.split('-')[1])
            if low <= frame_num <= high:
                sequence_path = data_path
                break
        if sequence_path is None:
            continue
        with open(sequence_path, 'r') as f:
            sequence = json.load(f)
            frame_key = f'{video_id}/{img_id}.png'
            if frame_key in sequence:
                x, y, w, h, _ = sequence[frame_key]['box']
                print(x, y, w, h)
                normalized_x = x / frame_width
                normalized_y = y / frame_height
                normalized_w = w / frame_width
                normalized_h = h / frame_height
                print(normalized_x, normalized_y, normalized_w, normalized_h)
                normalized_keypoints = [(keypoints[i][0] / frame_width, keypoints[i][1] / frame_height) for i in range(len(keypoints))]
                print(keypoints)
                print(normalized_keypoints)
            else:
                print(f'{frame_key} not found')
        break