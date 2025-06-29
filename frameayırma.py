import cv2
import os
from pathlib import Path


VIDEO_DIR = Path("video")             
OUTPUT_DIR = Path("framevideo")    
FRAME_INTERVAL = 10                   # Her 10. frame kaydedilecek
SUPPORTED_FORMATS = [".mp4", ".mkv", ".avi", ".mov"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_frames(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"⚠ {video_path.name} açılamadı.")
        return

    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % FRAME_INTERVAL == 0:
            frame_file = OUTPUT_DIR / f"{video_path.stem}_frame{count}.jpg"
            cv2.imwrite(str(frame_file), frame)
            saved += 1

        count += 1

    cap.release()
    print(f"✔ {video_path.name} → {saved} kare kaydedildi.")


for video_file in VIDEO_DIR.iterdir():
    if video_file.suffix.lower() in SUPPORTED_FORMATS:
        extract_frames(video_file)
