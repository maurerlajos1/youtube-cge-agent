import json
import os

JSON_PATH = r"H:\Youtube agent\transcript.json"
MD_PATH = r"H:\Youtube agent\FULL_TRANSCRIPT.md"

def fmt_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data["segments"]

    # Group segments into ~1-minute or natural pause blocks
    blocks = []
    current_block = []
    current_start = 0

    for seg in segments:
        if not current_block:
            current_start = seg["start"]
        current_block.append(seg["text"])
        
        # Break block if block duration >= 60s
        if seg["end"] - current_start >= 60:
            blocks.append((current_start, seg["end"], " ".join(current_block)))
            current_block = []

    if current_block:
        blocks.append((current_start, segments[-1]["end"], " ".join(current_block)))

    md_lines = [
        "# Full Video Transcript: LIVE - How To Start On YouTube Step-By-Step For Beginners",
        "",
        "| Metric | Value |",
        "| :--- | :--- |",
        f"| **Source Video** | `_GMT20261025-224816_Recording_1920x1080.mp4` |",
        f"| **Total Duration** | {data['duration_formatted']} (2 Hours 32 Minutes 10 Seconds) |",
        f"| **Total Word Count** | {data['total_words']:,} words |",
        f"| **Total Segments** | {data['total_segments']:,} |",
        "| **Language** | English |",
        "| **Transcription Engine** | Whisper `large-v3-turbo` (FP16 on NVIDIA GeForce RTX 3090) |",
        "",
        "---",
        "",
        "## Table of Contents & Timeline Overview",
        "",
        "- [00:00:00 - 00:10:56] Phase 1: Pre-roll Showcase, Creator Economy Overview & Case Studies",
        "- [00:10:56 - 00:12:49] Phase 2: Live Welcome, Setup & Speaker Introduction",
        "- [00:12:50 - 01:05:00] Phase 3: Core Training - The Hybrid Model & The Icahn Method",
        "- [01:05:00 - 01:50:00] Phase 4: Systems, Workflows, Scripting & Monetization Architecture",
        "- [01:50:00 - 02:32:10] Phase 5: Program Walkthrough, Resources & Extended Live Q&A",
        "",
        "---",
        "",
        "## Full Chronological Transcript",
        ""
    ]

    for start_s, end_s, text in blocks:
        md_lines.append(f"### `[{fmt_time(start_s)} - {fmt_time(end_s)}]`")
        md_lines.append("")
        md_lines.append(text)
        md_lines.append("")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Successfully generated {MD_PATH} ({len(blocks)} sections, {len(md_lines)} lines)!")

if __name__ == "__main__":
    main()
