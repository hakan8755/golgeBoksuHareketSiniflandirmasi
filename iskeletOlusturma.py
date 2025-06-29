import cv2
import mediapipe as mp
import os
from pathlib import Path
import numpy as np


INPUT_DIR = Path("etiketler/egilme")         
OUTPUT_DIR = Path("iskelet/egilme")          
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


IMPORTANT_LANDMARKS = [
    0,          # Burun (kafa pozisyonu)
    11, 12,     # Omuzlar
    13, 14,     # Dirsekler
    15, 16,     # Bilekler
    23, 24      # Kalçalar
]


CUSTOM_CONNECTIONS = [
    (11, 13), (13, 15),    # Sol kol
    (12, 14), (14, 16),    # Sağ kol
    (11, 23), (12, 24),    # Omuz-kalça
    (23, 24),              # Kalçalar arası
    (11, 12),              # Omuzlar arası
    (0, 11), (0, 12),      # Kafa - omuz bağlantısı 
]


with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
    for file_name in sorted(os.listdir(INPUT_DIR)):
        if not file_name.endswith(('.jpg', '.png')):
            continue

        input_path = INPUT_DIR / file_name
        image = cv2.imread(str(input_path))
        if image is None:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            blank = 255 * np.ones_like(image)
            h, w, _ = image.shape

            # Noktaları çiz
            for idx in IMPORTANT_LANDMARKS:
                lm = results.pose_landmarks.landmark[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(blank, (cx, cy), 5, (0, 0, 255), -1)

            # Bağlantıları çiz
            for start_idx, end_idx in CUSTOM_CONNECTIONS:
                start = results.pose_landmarks.landmark[start_idx]
                end = results.pose_landmarks.landmark[end_idx]
                x1, y1 = int(start.x * w), int(start.y * h)
                x2, y2 = int(end.x * w), int(end.y * h)
                cv2.line(blank, (x1, y1), (x2, y2), (0, 255, 0), 2)

          
            output_path = OUTPUT_DIR / file_name
            cv2.imwrite(str(output_path), blank)

        else:
            # Pose bulunamadıysa frame'i sil
            print(f"⛔ Pose yok, silindi: {file_name}")
            os.remove(input_path)

print("✅ Gölge boksu için iskelet çizimi tamamlandı.")
