import cv2
import os
from pathlib import Path
import shutil


INPUT_DIR = Path("iskelet")                 
OUTPUT_DIR = Path("a")         


label_map = {
    ord('q'): "direkt",
    ord('w'): "krose",
    ord('e'): "aparkat",
    ord('r'): "gard", 
    ord('t'): "egilme",
    ord(' '): "belirsiz"

}


for label in label_map.values():
    (OUTPUT_DIR / label).mkdir(parents=True, exist_ok=True)


images = sorted(INPUT_DIR.glob("*.jpg"))
for img_path in images:
    img = cv2.imread(str(img_path))
    if img is None:
        continue

    cv2.imshow("Etiketleme Aracı - Bas: U/K/D/I/X | ESC ile çık", img)
    key = cv2.waitKey(0)

    if key == 27:  # ESC
        print("🚪 Etiketleme iptal edildi.")
        break

    if key in label_map:
        label_name = label_map[key]
        target_path = OUTPUT_DIR / label_name / img_path.name
        shutil.move(str(img_path), str(target_path))
        print(f"✔ {img_path.name} → {label_name}")
    else:
        print("❌ Geçersiz tuş, görsel atlandı.")


print("✅ Etiketleme tamamlandı.")
