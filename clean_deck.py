import os
import json
from PIL import Image

slides_dir = r"H:\Youtube agent\slides"
manifest_path = os.path.join(slides_dir, "slides_manifest.json")

with open(manifest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

slides = data["slides"]

# Remove slide 1 (00:12:50 black screen share initiation) and slide 95 (01:22:16 black transition frame)
filtered = [s for s in slides if s["slide_number"] not in [1, 95]]

for num in [1, 95]:
    target = [s for s in slides if s["slide_number"] == num]
    if target:
        p = os.path.join(slides_dir, target[0]["filename"])
        if os.path.exists(p):
            os.remove(p)
            print(f"Removed transition frame: {target[0]['filename']}")

clean_slides = []
pil_images = []

for idx, s in enumerate(filtered, start=1):
    old_path = os.path.join(slides_dir, s["filename"])
    time_tag = s["timestamp_formatted"].replace(":", "-")
    new_filename = f"slide_{idx:03d}_{time_tag}.png"
    new_path = os.path.join(slides_dir, new_filename)

    if os.path.exists(old_path) and old_path != new_path:
        # Avoid collision if already named
        temp_path = old_path + ".tmp"
        os.rename(old_path, temp_path)
        os.rename(temp_path, new_path)

    clean_slides.append({
        "slide_number": idx,
        "timestamp_seconds": s["timestamp_seconds"],
        "timestamp_formatted": s["timestamp_formatted"],
        "filename": new_filename,
        "resolution": s["resolution"]
    })

    pil_images.append(Image.open(new_path).convert("RGB"))

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump({
        "total_slides": len(clean_slides),
        "video_file": data["video_file"],
        "scan_range": data["scan_range"],
        "slides": clean_slides
    }, f, indent=2)

pdf_path = r"H:\Youtube agent\extracted_slides.pdf"
pil_images[0].save(pdf_path, save_all=True, append_images=pil_images[1:], resolution=150.0)
print(f"Successfully re-compiled {len(clean_slides)} pure content slides into {pdf_path} ({os.path.getsize(pdf_path)/(1024*1024):.2f} MB)!")
