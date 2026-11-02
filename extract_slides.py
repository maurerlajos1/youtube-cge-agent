import os
import sys
import time
import json
import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

VIDEO_PATH = r"H:\Youtube agent\_GMT20261025-224816_Recording_1920x1080.mp4"
OUTPUT_DIR = r"H:\Youtube agent\slides"
PDF_PATH = r"H:\Youtube agent\extracted_slides.pdf"

# Slide boundaries identified from video layout
# 1920x1080 -> Slide canvas: y in [112, 1006], x in [155, 1746] (1591x894 px)
Y_START = 112
Y_END = 1006
X_START = 155
X_END = 1746

# Webcam exclusion region (top right of the crop)
# webcam overlay is at y < 70, x > 1400 in relative crop coordinates
WEBCAM_Y_MAX = 70
WEBCAM_X_MIN = 1400

# Presentation timeline
START_SEC = 770
END_SEC = 9060
SAMPLE_STEP_SEC = 2 # Check every 2 seconds

def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def compute_thumb(crop):
    """Downsample and mask webcam for fast difference calculation."""
    masked = crop.copy()
    masked[:WEBCAM_Y_MAX, WEBCAM_X_MIN:] = 0
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, (160, 90))

def main():
    print("=" * 60)
    print("STARTING SLIDE EXTRACTION")
    print(f"Video: {VIDEO_PATH}")
    print(f"Output folder: {OUTPUT_DIR}")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Unable to open video {VIDEO_PATH}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_dur = total_frames / fps

    print(f"FPS: {fps:.2f} | Total Frames: {total_frames:,} | Duration: {format_time(video_dur)}")
    print(f"Scanning range: {format_time(START_SEC)} to {format_time(END_SEC)} (step = {SAMPLE_STEP_SEC}s)...")

    # Set start position
    cap.set(cv2.CAP_PROP_POS_MSEC, START_SEC * 1000)

    extracted_slides = [] # list of dicts: {id, timestamp, time_str, crop, filename}
    prev_thumb = None
    last_slide_thumb = None
    current_sec = START_SEC

    # Frame skipping calculation
    frames_per_step = int(round(fps * SAMPLE_STEP_SEC))

    t0 = time.time()
    last_status_time = time.time()

    while current_sec <= END_SEC:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop slide region
        slide_crop = frame[Y_START:Y_END, X_START:X_END].copy()
        thumb = compute_thumb(slide_crop)

        if last_slide_thumb is None:
            # First slide
            slide_id = 1
            time_tag = format_time(current_sec).replace(":", "-")
            fname = f"slide_{slide_id:03d}_{time_tag}.png"
            extracted_slides.append({
                "id": slide_id,
                "timestamp": current_sec,
                "time_str": format_time(current_sec),
                "crop": slide_crop,
                "filename": fname,
                "thumb": thumb
            })
            last_slide_thumb = thumb
        else:
            diff_from_last = np.mean(np.abs(thumb.astype(float) - last_slide_thumb.astype(float)))

            # If difference is significant (> 12.0 for new slide, or > 5.0 for major build)
            if diff_from_last > 14.0:
                # Definite new slide
                slide_id = len(extracted_slides) + 1
                time_tag = format_time(current_sec).replace(":", "-")
                fname = f"slide_{slide_id:03d}_{time_tag}.png"
                extracted_slides.append({
                    "id": slide_id,
                    "timestamp": current_sec,
                    "time_str": format_time(current_sec),
                    "crop": slide_crop,
                    "filename": fname,
                    "thumb": thumb
                })
                last_slide_thumb = thumb
            elif diff_from_last > 4.5:
                # Moderate change (e.g. bullet point added or build completed on same slide)
                # If this build has persisted or replaces previous build, update the previous slide image
                # to get the final complete version of the slide!
                extracted_slides[-1]["crop"] = slide_crop
                extracted_slides[-1]["timestamp"] = current_sec
                extracted_slides[-1]["time_str"] = format_time(current_sec)
                last_slide_thumb = thumb

        # Skip frames to next sample step
        for _ in range(frames_per_step - 1):
            if not cap.grab():
                break

        current_sec += SAMPLE_STEP_SEC

        now = time.time()
        if now - last_status_time >= 15:
            pct = ((current_sec - START_SEC) / (END_SEC - START_SEC)) * 100
            elapsed = now - t0
            speed = (current_sec - START_SEC) / max(elapsed, 0.001)
            eta = (END_SEC - current_sec) / max(speed, 0.001)
            print(f"[{format_time(current_sec)} / {format_time(END_SEC)}] {pct:5.1f}% | "
                  f"Slides found: {len(extracted_slides)} | Speed: {speed:.1f}x real-time | ETA: {eta/60:.1f}m")
            last_status_time = now

    cap.release()
    scan_time = time.time() - t0
    print(f"\nScan finished in {scan_time:.1f}s ({scan_time/60:.1f}m)!")
    print(f"Total raw slides found: {len(extracted_slides)}")

    # Deduplicate / filter any transient frames
    final_slides = []
    print("Saving slides and generating metadata...")

    manifest = []
    pil_images = []

    for idx, s in enumerate(extracted_slides, start=1):
        clean_fname = f"slide_{idx:03d}_{s['time_str'].replace(':', '-')}.png"
        save_path = os.path.join(OUTPUT_DIR, clean_fname)

        # Save high quality PNG
        cv2.imwrite(save_path, s["crop"])

        # Also prepare RGB PIL image for PDF
        rgb_crop = cv2.cvtColor(s["crop"], cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_crop)
        pil_images.append(pil_img)

        manifest.append({
            "slide_number": idx,
            "timestamp_seconds": s["timestamp"],
            "timestamp_formatted": s["time_str"],
            "filename": clean_fname,
            "resolution": f"{s['crop'].shape[1]}x{s['crop'].shape[0]}"
        })

    # Save manifest JSON
    manifest_path = os.path.join(OUTPUT_DIR, "slides_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_slides": len(manifest),
            "video_file": os.path.basename(VIDEO_PATH),
            "scan_range": f"{format_time(START_SEC)} - {format_time(END_SEC)}",
            "slides": manifest
        }, f, indent=2)
    print(f"Saved manifest: {manifest_path}")

    # Compile all slides into single PDF
    if pil_images:
        print(f"Compiling {len(pil_images)} slides into PDF...")
        pil_images[0].save(
            PDF_PATH,
            save_all=True,
            append_images=pil_images[1:],
            resolution=150.0
        )
        print(f"Saved PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH) / (1024*1024):.2f} MB)")

    print("=" * 60)
    print(f"[SUCCESS] SLIDE EXTRACTION COMPLETE: {len(manifest)} slides generated!")
    print("=" * 60)

if __name__ == "__main__":
    main()
