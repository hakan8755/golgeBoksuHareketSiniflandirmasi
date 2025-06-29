from pathlib import Path
import os

folder = Path("frame2/dosya11")  # Orijinal frame klasörü
new_prefix = "frame"

# Dosyaları sırala ve yeniden adlandır
for i, file in enumerate(sorted(folder.glob("*.jpg")), start=1):
    new_name = folder / f"{new_prefix}_{i:05}.jpg"
    file.rename(new_name)

print("✅ Orijinal frameler sırayla yeniden adlandırıldı.")
