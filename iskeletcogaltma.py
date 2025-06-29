import cv2
import os
import albumentations as A
import numpy as np

# 📁 Klasör Yolları
input_dir = "iskelet/aparkat"  # Elindeki  görselleri buraya
output_dir = "cogaltAparkat"
os.makedirs(output_dir, exist_ok=True)

# 🔁 Augmentasyon (blur yok)
augment = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=15, p=0.7),
    A.RandomBrightnessContrast(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=10, p=0.7),
    A.Resize(256, 256)
])

# 🔄 Çoğaltma işlemi
image_paths = [f for f in os.listdir(input_dir) if f.endswith((".jpg", ".png"))]
multiplier = 5  # Her görselden 5 yeni örnek üret

for img_name in image_paths:
    img_path = os.path.join(input_dir, img_name)
    image = cv2.imread(img_path)

    for i in range(multiplier):
        augmented = augment(image=image)['image']
        out_name = f"{img_name.split('.')[0]}_aug_{i}.jpg"
        cv2.imwrite(os.path.join(output_dir, out_name), augmented)
