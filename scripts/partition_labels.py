from pathlib import Path
import shutil

for label in Path("../all_labels").iterdir():
    if Path(f"../dataset/images/{label.stem}.png").exists():
        shutil.copy(label, Path(f"../dataset/labels/{label.name}"))
