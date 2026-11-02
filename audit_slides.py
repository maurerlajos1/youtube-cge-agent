import os
import json
import cv2
import numpy as np

MANIFEST_PATH = r"H:\Youtube agent\slides\slides_manifest.json"
SLIDES_DIR = r"H:\Youtube agent\slides"

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)["slides"]

print(f"Auditing {len(manifest)} slides...")

blank_or_black = []
camera_frames = []
valid_slides = []

for s in manifest:
    fpath = os.path.join(SLIDES_DIR, s["filename"])
    img = cv2.imread(fpath)
    if img is None:
        continue
    
    mean_val = np.mean(img)
    std_val = np.std(img)
    
    # Check if mostly uniform black or blank
    if mean_val < 5:
        blank_or_black.append((s["slide_number"], s["timestamp_formatted"], "Black", mean_val))
    elif std_val < 5:
        blank_or_black.append((s["slide_number"], s["timestamp_formatted"], "Uniform", std_val))
    else:
        valid_slides.append((s["slide_number"], s["timestamp_formatted"], mean_val, std_val))

print(f"Valid slides: {len(valid_slides)}")
print(f"Blank/Black frames: {len(blank_or_black)} -> {blank_or_black}")

# Let's inspect slide 1, 2, 3
for s_num in [1, 2, 3, 4, 5, 205, 206]:
    s = manifest[s_num - 1]
    fpath = os.path.join(SLIDES_DIR, s["filename"])
    img = cv2.imread(fpath)
    print(f"Slide {s_num:03d} ({s['timestamp_formatted']}): mean={img.mean():.1f}, std={img.std():.1f}")
