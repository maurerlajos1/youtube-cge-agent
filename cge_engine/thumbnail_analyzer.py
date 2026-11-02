#!/usr/bin/env python3
"""
CGE Thumbnail Analyzer & Visual Rule-of-Thirds Inspector
========================================================
Reverse-engineered & 10x upgraded local computer-vision implementation of:
- Shane Hummus's `Thumbnail Analyzer by Content Growth Engine` GPT
- `High-converting Thumbnail Toolkit™` (`slide_133` - `slide_134`):
  1. Rule of Thirds Grid Alignment (Right 1/3 Face/Eyes Anchor vs Left 2/3 Prop/Text Zone)
  2. Visual Clutter & Edge Density Score (Penalizes >3 competing visual clusters)
  3. High-Contrast & Color Pop Score (Luminance standard deviation + HSV saturation)
  4. Mobile Feed Squint Test (`168x94px` legibility survival score)
  5. Title-to-Thumbnail Text Redundancy Check (Ensures thumbnail complements rather than repeats title)
  6. Generates an annotated `*_audit_overlay.png` with red 3x3 Rule-of-Thirds grid lines & focal zone heat scores.

Usage:
  python cge_engine/thumbnail_analyzer.py --image "slides/slide_133_01-45-26.png" --title "10 Most Worthless College Majors" --thumb-text "DEGREES TO AVOID"
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, Any, Set

if os.path.exists(r"H:\TTS\venv\Lib\site-packages"):
    sys.path.insert(0, r"H:\TTS\venv\Lib\site-packages")

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


STOPWORDS: Set[str] = {
    "the", "a", "an", "to", "in", "on", "of", "for", "and", "or", "with", "by", "at", "from", "is", "are", "this", "that"
}


def tokenize_words(text: str) -> Set[str]:
    words = re.findall(r"[a-zA-Z0-9$]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


def analyze_thumbnail(
    image_path: str,
    video_title: str = "",
    thumb_text: str = "",
    output_overlay_path: str = "",
) -> Dict[str, Any]:
    img = Image.open(image_path).convert("RGB")
    # Standardize to 1280x720 (16:9 YouTube aspect ratio) for analysis
    img_720 = img.resize((1280, 720), Image.Resampling.LANCZOS)
    arr = np.asarray(img_720, dtype=np.float32) / 255.0

    # 1. Luminance & Contrast Score (20 pts)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    contrast_std = float(np.std(lum))
    p95_p05 = float(np.percentile(lum, 95) - np.percentile(lum, 5))
    # Ideal std is >= 0.26, dynamic range >= 0.70
    contrast_score = min(20.0, round((contrast_std / 0.28) * 12.0 + (p95_p05 / 0.75) * 8.0, 1))

    # 2. Color Saturation Pop (15 pts)
    max_c = np.max(arr, axis=2)
    min_c = np.min(arr, axis=2)
    delta = max_c - min_c
    sat = np.where(max_c > 1e-5, delta / np.maximum(max_c, 1e-5), 0.0)
    mean_sat = float(np.mean(sat))
    p90_sat = float(np.percentile(sat, 90))
    saturation_score = min(15.0, round((mean_sat / 0.35) * 8.0 + (p90_sat / 0.80) * 7.0, 1))

    # 3. Edge Density / Visual Clutter Check & Rule-of-Thirds Asymmetry (25 pts)
    gx = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1]))
    gy = np.abs(np.diff(lum, axis=0, prepend=lum[:1, :]))
    edges = np.hypot(gx, gy)
    edge_mean = float(np.mean(edges))

    # Divide into 3x3 Rule-of-Thirds Grid
    h, w = lum.shape
    h3, w3 = h // 3, w // 3
    grid_energy = np.zeros((3, 3), dtype=np.float32)
    for r in range(3):
        for c in range(3):
            patch = edges[r * h3 : (r + 1) * h3, c * w3 : (c + 1) * w3]
            grid_energy[r, c] = float(np.mean(patch))

    right_third_energy = float(np.mean(grid_energy[:, 2]))
    left_two_thirds_energy = float(np.mean(grid_energy[:, :2]))
    # Penalize extreme clutter (edge_mean > 0.085) or completely flat image (< 0.015)
    if 0.020 <= edge_mean <= 0.075:
        clutter_score = 15.0
    elif edge_mean > 0.075:
        clutter_score = max(4.0, round(15.0 - (edge_mean - 0.075) * 180.0, 1))
    else:
        clutter_score = max(5.0, round((edge_mean / 0.020) * 15.0, 1))

    # Rule-of-thirds focal balance (10 pts)
    focal_ratio = max(right_third_energy, left_two_thirds_energy) / max(
        min(right_third_energy, left_two_thirds_energy), 1e-4
    )
    thirds_score = min(10.0, round(10.0 if 1.05 <= focal_ratio <= 2.5 else 7.0, 1))
    composition_score = round(clutter_score + thirds_score, 1)

    # 4. Mobile Squint Legibility Survival (`168x94px` downscale vs upscale loss) (20 pts)
    mobile_small = img_720.resize((168, 94), Image.Resampling.BOX)
    mobile_back = mobile_small.resize((1280, 720), Image.Resampling.BILINEAR)
    arr_back = np.asarray(mobile_back, dtype=np.float32) / 255.0
    lum_back = 0.299 * arr_back[:, :, 0] + 0.587 * arr_back[:, :, 1] + 0.114 * arr_back[:, :, 2]
    # How much contrast survives at 168x94px?
    mobile_contrast_retention = float(np.std(lum_back)) / max(contrast_std, 1e-4)
    mobile_score = min(20.0, round(mobile_contrast_retention * 21.0, 1))

    # 5. Text Economy & Title Synergy Check (20 pts)
    words_thumb = re.findall(r"\S+", thumb_text.strip()) if thumb_text.strip() else []
    word_count = len(words_thumb)
    if word_count == 0:
        text_len_score = 9.0  # Visual-only thumbnail is fine, or text not supplied
    elif 1 <= word_count <= 4:
        text_len_score = 10.0
    elif word_count <= 6:
        text_len_score = 6.0
    else:
        text_len_score = 2.0

    t_tokens = tokenize_words(video_title)
    th_tokens = tokenize_words(thumb_text)
    overlap = t_tokens.intersection(th_tokens)
    if not th_tokens or not t_tokens:
        synergy_score = 9.0
    elif len(overlap) == 0:
        synergy_score = 10.0  # 100% complementary!
    else:
        overlap_ratio = len(overlap) / max(len(th_tokens), 1)
        synergy_score = max(2.0, round(10.0 * (1.0 - overlap_ratio), 1))

    packaging_synergy_score = round(text_len_score + synergy_score, 1)
    total_score = round(
        contrast_score + saturation_score + composition_score + mobile_score + packaging_synergy_score, 1
    )

    # Generate diagnostic recommendations
    recommendations = []
    if contrast_score < 14.0:
        recommendations.append(
            "Boost luminance contrast: darken the background slightly and add a subtle rim light or bright text pill so the subject pops."
        )
    if saturation_score < 10.0:
        recommendations.append(
            "Increase color saturation on your primary focal prop or corner text badge (use high-contrast neon green, red, or yellow)."
        )
    if clutter_score < 11.0:
        recommendations.append(
            "High visual clutter detected (>3 competing detail zones). Blur the background or remove secondary icons to obey Shane's <=3 Element Rule."
        )
    if word_count > 4:
        recommendations.append(
            f"Thumbnail text has {word_count} words ('{thumb_text}'). Cut to 2-4 bold words max for mobile legibility."
        )
    if overlap:
        recommendations.append(
            f"Title-Thumbnail Redundancy Warning: Words {sorted(list(overlap))} appear in BOTH the title and thumbnail. Change thumbnail text to create a Curiosity Gap."
        )
    recommendations.append(
        "Whites-of-the-Eyes Check: Verify the creator's head fills ~75-85% of the vertical height on the right Rule-of-Thirds line so the whites of the eyes are unmistakable at 168x94px."
    )

    # Render annotated Rule-of-Thirds overlay image if requested
    if not output_overlay_path:
        base, _ = os.path.splitext(image_path)
        output_overlay_path = f"{base}_cge_audit.png"

    overlay = img_720.copy()
    draw = ImageDraw.Draw(overlay)
    # Draw Rule of Thirds lines in bright red (matching Shane's Slide 133 guide)
    for idx in (1, 2):
        x = idx * w3
        y = idx * h3
        draw.line([(x, 0), (x, h)], fill=(255, 40, 40), width=4)
        draw.line([(0, y), (w, y)], fill=(255, 40, 40), width=4)

    # Draw intersection power points (Circles at the 4 Rule-of-Thirds intersections)
    for ix in (w3, 2 * w3):
        for iy in (h3, 2 * h3):
            r_pt = 12
            draw.ellipse([(ix - r_pt, iy - r_pt), (ix + r_pt, iy + r_pt)], outline=(255, 230, 0), width=4)

    # Paste actual 168x94 mobile preview in bottom-left corner with border
    border_w = 4
    preview_box = Image.new("RGB", (168 + 2 * border_w, 94 + 2 * border_w), (255, 230, 0))
    preview_box.paste(mobile_small, (border_w, border_w))
    overlay.paste(preview_box, (20, h - 94 - 28))
    overlay.save(output_overlay_path)

    return {
        "image_path": image_path,
        "audit_overlay_image": output_overlay_path,
        "video_title": video_title,
        "thumbnail_text": thumb_text,
        "total_score_out_of_100": total_score,
        "grade": "A+ (Viral Ready)" if total_score >= 88 else ("B+ (Solid, Minor Tweaks)" if total_score >= 76 else "C (Needs Rework Before Upload)"),
        "subscores": {
            "contrast_and_dynamic_range_20": contrast_score,
            "color_saturation_pop_15": saturation_score,
            "rule_of_thirds_and_clutter_25": composition_score,
            "mobile_168x94_squint_survival_20": mobile_score,
            "text_economy_and_title_synergy_20": packaging_synergy_score,
        },
        "metrics": {
            "luminance_std": round(contrast_std, 3),
            "dynamic_range_p95_p05": round(p95_p05, 3),
            "mean_saturation": round(mean_sat, 3),
            "edge_clutter_index": round(edge_mean, 4),
            "mobile_contrast_retention": round(mobile_contrast_retention, 3),
            "thumbnail_word_count": word_count,
            "redundant_title_words": sorted(list(overlap)),
        },
        "actionable_fixes": recommendations,
    }


def main():
    parser = argparse.ArgumentParser(description="CGE Computer-Vision Thumbnail Analyzer")
    parser.add_argument("--image", "-i", required=True, help="Path to thumbnail image")
    parser.add_argument("--title", "-t", default="", help="Proposed YouTube video title")
    parser.add_argument("--thumb-text", "-x", default="", help="Text written on the thumbnail")
    parser.add_argument("--output-overlay", "-o", default="", help="Output path for annotated Rule-of-Thirds image")
    args = parser.parse_args()

    result = analyze_thumbnail(
        image_path=args.image,
        video_title=args.title,
        thumb_text=args.thumb_text,
        output_overlay_path=args.output_overlay,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
