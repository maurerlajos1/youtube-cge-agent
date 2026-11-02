#!/usr/bin/env python3
"""
Holy Trifecta & VibeWriter 10x — Anti-Slop Script Architect & Linter
====================================================================
Reverse-engineered & 10x upgraded implementation of Shane Hummus's:
- `cge-holy-trifecta-title-thumbnail-intro` (Module #4: The Holy Trifecta System)
- `youtube-script-writer-skill` (Module #5: Scriptwriting Alchemy & VibeWriter AI Deluxe)
- Anti-AI-Slop Linter (bans robotic AI vocabulary & enforces 6th-8th grade spoken cadence)
- 0-30s WPM Pacing Timer & Dual-Column Editor Production Sheet Generator

Usage:
  python cge_engine/holy_trifecta_vibe_writer.py --title "7 Boring Businesses That Print $20K/Month" --thumb-text "BORING = RICH" --avatar "burned-out corporate employees" --offer "Free Boring Business Acquisition Checklist (first link in description)"
"""

import argparse
import json
import re
from typing import Dict, List, Any


BANNED_AI_SLOP_WORDS = [
    "delve",
    "tapestry",
    "testament",
    "moreover",
    "furthermore",
    "in conclusion",
    "in today's fast-paced world",
    "in today's digital age",
    "ever-evolving",
    "beacon",
    "symphony",
    "unlock the power",
    "unleash",
    "dive deep into the intricacies",
    "without further ado",
    "hey guys welcome back",
    "smash that like button",
]


def lint_script_for_ai_slop(script_text: str) -> Dict[str, Any]:
    low = script_text.lower()
    flagged = [w for w in BANNED_AI_SLOP_WORDS if w in low]
    sentences = [s.strip() for s in re.split(r"[.!?]+", script_text) if s.strip()]
    words = re.findall(r"\b\w+\b", script_text)
    avg_words_per_sentence = round(len(words) / max(len(sentences), 1), 1)
    est_speaking_seconds = round((len(words) / 160.0) * 60.0, 1)

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_words_per_sentence": avg_words_per_sentence,
        "estimated_speaking_time_seconds_at_160wpm": est_speaking_seconds,
        "banned_ai_slop_detected": flagged,
        "cadence_verdict": (
            "PASS (Conversational 6th-8th Grade Spoken Cadence)"
            if avg_words_per_sentence <= 18 and not flagged
            else "WARN (Shorten sentences to <=18 words and remove flagged AI phrases)"
        ),
    }


def generate_holy_trifecta_and_script(
    title: str,
    thumb_text: str,
    avatar: str,
    offer_cta: str,
    points: List[str] = None,
) -> Dict[str, Any]:
    if not points:
        points = [
            "The Counterintuitive Selection Filter (Why 90% of beginners pick the wrong lane)",
            "The ICAHN Validation Shortcut (How to copy proven demand in 15 minutes)",
            "The #1 Highest-Leverage Execution Step (Where 80% of the profit actually lives)",
        ]

    # 4-Part 30-Second Intro (strictly 65-78 words, <=15 words/sentence for ~26-29s at 160 WPM)
    click_confirmation_0_5s = (
        f"Here is the truth about {title}. What looks '{thumb_text.lower()}' is actually the fastest path for {avatar}."
    )
    curiosity_loop_5_15s = (
        f"Make sure you stay for #{len(points)}. It breaks every rule gurus teach, yet it drives 80% of our results."
    )
    credibility_15_22s = (
        "We tested all of these over 12 months so you don't waste a single dollar."
    )
    fast_transition_22_30s = "No fluff. Let's jump straight into #1."

    full_intro = f"{click_confirmation_0_5s} {curiosity_loop_5_15s} {credibility_15_22s} {fast_transition_22_30s}"
    intro_lint = lint_script_for_ai_slop(full_intro)

    # Dual-Column Script Architecture
    script_blocks = [
        {
            "timecode": "0:00 - 0:05",
            "section": "INTRO PART 1: Click Confirmation",
            "editor_visual_cue": f"[A-ROLL CLOSE-UP] Creator head on right Rule-of-Thirds line (whites of eyes clear). Pop up '{thumb_text}' graphic on left 2/3 in first 1.5s.",
            "spoken_script": click_confirmation_0_5s,
        },
        {
            "timecode": "0:05 - 0:15",
            "section": "INTRO PART 2: Curiosity Loop & Stakes",
            "editor_visual_cue": f"[B-ROLL SPLIT / BLURRED LIST] Show numbered list 1 to {len(points)} with #{len(points)} blurred out in gold + subtle tension whoosh.",
            "spoken_script": curiosity_loop_5_15s,
        },
        {
            "timecode": "0:15 - 0:22",
            "section": "INTRO PART 3: 1-Sentence Proof",
            "editor_visual_cue": "[PROOF OVERLAY] Flash real analytics / case study screenshot on screen for 3 seconds.",
            "spoken_script": credibility_15_22s,
        },
        {
            "timecode": "0:22 - 0:30",
            "section": "INTRO PART 4: Fast Transition",
            "editor_visual_cue": "[HARD CUT + TEXT CARD] Punch in 15% on camera -> Full-screen chapter card: '#1'.",
            "spoken_script": fast_transition_22_30s,
        },
    ]

    for idx, pt in enumerate(points, 1):
        script_blocks.append(
            {
                "timecode": f"Point #{idx} (90-120s)",
                "section": f"VALUE BOMB #{idx}: {pt}",
                "editor_visual_cue": (
                    f"[DIAGRAM / SCREENSHARE] Draw X -> Y -> Z visual on screen. At +60s insert PATTERN INTERRUPT (camera crop change + on-screen stat)."
                ),
                "spoken_script": (
                    f"Number {idx} is {pt}. Most {avatar} get stuck here because they overcomplicate the setup. "
                    f"Instead, focus on the 80/20 lever first. [INSERT 45-SECOND REAL CLIENT STORY / EXAMPLE HERE]. "
                    + (
                        f"Now, #{idx} gets the ball rolling, but it completely falls apart if you miss #{idx + 1}..."
                        if idx < len(points)
                        else "And that brings us to how you actually put this on autopilot today."
                    )
                ),
            }
        )
        if idx == 2:
            script_blocks.append(
                {
                    "timecode": "Mid-Roll Native Seed (15s)",
                    "section": "CASH CODE NATIVE LEAD MAGNET BRIDGE",
                    "editor_visual_cue": "[SCREEN OVERLAY] Show arrow pointing down to the 1st line of the YouTube description.",
                    "spoken_script": (
                        f"By the way, if you don't want to build this from scratch, I put our complete {offer_cta} "
                        f"at the very first link in the description. It's 100% free—grab it after this point."
                    ),
                }
            )

    script_blocks.append(
        {
            "timecode": "Final 20 Seconds",
            "section": "ABRUPT END-SCREEN BINGE BRIDGE (No 'In Conclusion' Drop-off!)",
            "editor_visual_cue": "[END SCREEN ELEMENT] Point directly to left/right end-screen video box. Zero outro music fade.",
            "spoken_script": (
                f"Now that you have all {len(points)} steps for {title}, the next bottleneck you'll hit is turning those views "
                f"into high-paying clients in under 3 hours a week. I broke down that exact system in this video right here on screen—click it now and I'll see you there."
            ),
        }
    )

    return {
        "holy_trifecta_package": {
            "video_title": title,
            "thumbnail_text": thumb_text,
            "target_avatar": avatar,
            "intro_30s_full_text": full_intro,
            "intro_30s_telemetry": intro_lint,
        },
        "dual_column_production_script": script_blocks,
    }


def main():
    parser = argparse.ArgumentParser(description="CGE Holy Trifecta & VibeWriter Script Architect")
    parser.add_argument("--title", "-t", required=True, help="Video Title")
    parser.add_argument("--thumb-text", "-x", required=True, help="2-4 Word Thumbnail Text")
    parser.add_argument("--avatar", "-a", default="busy entrepreneurs", help="Target Avatar X")
    parser.add_argument("--offer", "-o", default="Niche 2.0 & Cash Code Blueprint", help="Free Lead Magnet / Offer CTA")
    args = parser.parse_args()

    out = generate_holy_trifecta_and_script(
        title=args.title,
        thumb_text=args.thumb_text,
        avatar=args.avatar,
        offer_cta=args.offer,
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
