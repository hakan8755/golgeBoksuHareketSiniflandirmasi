import os
import shutil
import random
from pathlib import Path

# === KAYNAK VE HEDEF KLASÖRLER ===
SOURCE_DIR = Path("sonData")
TARGET_DIR = Path("ayrikData")
TRAIN_RATIO = 0.8 

# === Her şeyden önce hedef klasörleri oluştur ===
for split in ["train", "val"]:
    (TARGET_DIR / split).mkdir(parents=True, exist_ok=True)

# === Her sınıfı işle ===
for class_folder in SOURCE_DIR.iterdir():
    if not class_folder.is_dir():
        continue

    class_name = class_folder.name
    all_files = list(class_folder.glob("*.jpg"))
    random.shuffle(all_files)

    split_index = int(len(all_files) * TRAIN_RATIO)
    train_files = all_files[:split_index]
    val_files = all_files[split_index:]

    (TARGET_DIR / "train" / class_name).mkdir(parents=True, exist_ok=True)
    (TARGET_DIR / "val" / class_name).mkdir(parents=True, exist_ok=True)

    
    for f in train_files:
        shutil.copy(f, TARGET_DIR / "train" / class_name / f.name)

    for f in val_files:
        shutil.copy(f, TARGET_DIR / "val" / class_name / f.name)

    print(f"✔ {class_name} → {len(train_files)} train / {len(val_files)} val")

print("✅ Veri başarıyla bölündü → pose_dataset_split/train ve val klasörlerine bakabilirsin.")
