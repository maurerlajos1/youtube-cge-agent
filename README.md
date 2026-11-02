# 🚀 YouTube CGE Agent & 10x Automation Suite

> **An Autonomous AI-Powered Content Growth Engine, Outlier Radar, Computer Vision Grader & Dual-Market Search Intelligence System.**
> Deconstructed and engineered from Shane Hummus's 2.5-hour YouTube Masterclass, upgraded with 2026 State-of-the-Art Agentic Workflows.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Automation: Playwright & OpenCV](https://img.shields.io/badge/Tech-OpenCV%20%7C%20Playwright-orange.svg)](#)

---

## 📌 Overview

Most creators and businesses fail on YouTube because they get trapped in **"The Maze"**—treating equipment, complex editing, and algorithm chasing as equally important. 

This repository implements the **80/20 Pareto Principle twice ($80\% \times 80\% = 64\%$)**, showing that **two-thirds of all YouTube revenue and growth comes from just three levers**:
1. **Niche 2.0 & High-RPM Offer Alignment**: Targeting high-intent buyers rather than low-RPM entertainment viewers.
2. **The Carl Icahn Method**: Identifying pre-validated outlier topics from small channels and applying a high-converting slight twist.
3. **The Holy Trifecta**: 168x94px mobile-first thumbnails + high-CTR title hooks + non-linear first 30-second script hooks.

This suite provides both **interactive visual applications** and **Python automation scripts** to automate this entire workflow end-to-end.

---

## 🏗️ Architecture & Core Tooling

```
Youtube agent/
├── cge_engine/                        # Autonomous Python Toolkit
│   ├── icahn_radar.py                 # Live YouTube wildcard scraper & outlier view multiplier
│   ├── revenue_icahn_hunter.py        # High-ticket / B2B revenue outlier hunter ($10K+ on <1K views)
│   ├── thumbnail_analyzer.py          # CV Rule-of-Thirds, 168x94px mobile squint & title overlap audit
│   ├── niche_20_calculator.py         # 5-Level Niche Hypothesis & True Business RPM ladder
│   ├── holy_trifecta_vibe_writer.py   # 30s hook writer, anti-AI-slop linter & editor script generator
│   ├── syndication_engine.py          # Long-form to Short-form repurposing & multi-platform syndicator
│   ├── keyword_researcher.py          # Dual-market (EN/HU) autocomplete miner (2,000+ keywords)
│   ├── google_keyword_planner_sync.py # Google Ads Keyword Planner CSV parser & database merger
│   └── autonomous_goal_executor.py    # Headless/CDP browser automator for Google Ads data extraction
│
├── CGE_10X_MASTER_WORKBENCH.html      # Standalone interactive browser workbench & prompt studio
├── SLIDES_AND_TRANSCRIPT_VIEWER.html  # Synchronized 204-slide + full timestamped transcript viewer
│
├── Playbooks & Documentation/
│   ├── SHANE_HUMMUS_YOUTUBE_PLAYBOOK.md        # Master deconstruction & unit economics playbook
│   ├── CGE_10X_COMPLETE_CURRICULUM_TEXTBOOK.md # 7-Module masterclass curriculum textbook
│   ├── DEEP_RESEARCH_CGE_VS_2026_SOTA.md       # Comparative study: CGE vs. 2026 Agentic SOTA
│   ├── SLIDES_001_TO_204_VISUAL_TRANSCRIPT.md  # Verbatim slide-by-slide transcription
│   └── GOOGLE_ADS_CRO_DUAL_MARKET_PLAYBOOK.md  # Dual-market search & conversion optimization guide
│
├── slides/                            # 204 high-resolution cropped slide assets
└── transcript.json                    # Full Whisper large-v3-turbo transcribed segments
```

---

## ⚡ The Python CGE 10x Suite (`cge_engine/`)

### 1. The Carl Icahn Outlier Radar (`icahn_radar.py`)
Scrapes YouTube autocomplete using wildcard queries (`* keyword`, `keyword vs *`, `how to * keyword`) and detects videos where **views exceed subscriber count by 3x to 50x+** on small channels. Automatically outputs optimized "slight-twist" titles.
```bash
python cge_engine/icahn_radar.py --keyword "google ads" --min-multiplier 3.0
```

### 2. Revenue-First Icahn Hunter (`revenue_icahn_hunter.py`)
Identifies high-ticket authority niches (B2B, consulting, medical, SaaS) where videos with fewer than 500 views generate \$10,000 to \$100,000+ contracts. Calculates expected True Business RPM.
```bash
python cge_engine/revenue_icahn_hunter.py --niche "b2b consulting"
```

### 3. Computer Vision Thumbnail Grader (`thumbnail_analyzer.py`)
Uses OpenCV and PIL to evaluate thumbnails before uploading:
- **Mobile Squint Test**: Downsamples image to `168x94px` (how it appears on mobile feeds) and calculates luminance contrast.
- **Rule of Thirds Grid**: Overlays focal lines to verify eye-tracking placement.
- **Timestamp / Duration Overlay Safety**: Flags whether the bottom-right corner contains critical text obscured by YouTube's duration pill.
```bash
python cge_engine/thumbnail_analyzer.py --input path/to/thumbnail.jpg
```

### 4. Niche 2.0 Hypothesis Calculator (`niche_20_calculator.py`)
Formulates the exact **Avatar $\rightarrow$ Problem $\rightarrow$ Mechanism** hypothesis:
$$\text{Hypothesis: } \text{I help } [X] \text{ overcome } [Y] \text{ by doing } [Z]$$
Evaluates Level 1 (Broke students, \$1–\$3 RPM) vs. Level 3 (Professionals, \$15–\$30 RPM) vs. Level 5 (Enterprise/B2B, \$1,000+ True RPM).
```bash
python cge_engine/niche_20_calculator.py
```

### 5. Holy Trifecta Vibe Writer (`holy_trifecta_vibe_writer.py`)
- Generates 30-second non-linear intro hooks (The "Cold Open" formula).
- **Anti-AI-Slop Linter**: Automatically scrubs overused AI phrases (*"In today's fast-paced digital world"*, *"Delve"*, *"Tapestry"*, *"Game-changer"*).
- Produces a dual-column production script formatted directly for \$5–\$8/hr Filipino video editors.
```bash
python cge_engine/holy_trifecta_vibe_writer.py --topic "How to scale Google Ads"
```

### 6. Dual-Market Search Volume Intelligence (`keyword_researcher.py`)
Automated multi-threaded autocomplete miner extracting high-intent keywords across Hungarian (`HU`) and English (`EN`) markets. Integrates directly with Google Ads Keyword Planner data pipelines.
```bash
python cge_engine/keyword_researcher.py
```

---

## 🖥️ Interactive Web Applications

### 🛠️ CGE 10x Master Workbench (`CGE_10X_MASTER_WORKBENCH.html`)
Open in any modern browser to access:
- **Interactive True RPM Calculator**: Real-time revenue projection modeling AdSense vs. Affiliates vs. Backend High-Ticket Offers.
- **Niche Statement Builder**: Real-time validator with built-in buying power scoring.
- **Prompt Generator Matrix**: One-click prompts for Claude, GPT-4, and Gemini for all 7 workshop modules.

### 📽️ Slides & Transcript Synchronizer (`SLIDES_AND_TRANSCRIPT_VIEWER.html`)
- Displays all **204 high-resolution cropped slides** extracted directly from the workshop video.
- Real-time search across the entire **30,873-word verbatim transcript**.
- Bidirectional sync: Clicking any timestamp instantly jumps to the corresponding slide; clicking any slide highlights the spoken audio segments.

---

## 📊 The Unit Economics: RPM Comparison

| Channel Model | Views Needed | Revenue Per 1,000 Views (True RPM) | Revenue on 24,200 Views | Primary Monetization Stack |
| :--- | :---: | :---: | :---: | :--- |
| **1. Entertainment** | Millions | **\$1 – \$3** | **\$24 – \$73** | AdSense + Low-CPM Sponsors |
| **2. Pure Education** | Tens of Thousands | **\$10 – \$20+** | **~\$484** | High-CPM AdSense + Basic Affiliates |
| **3. High-Intent Affiliate + Edu** | Thousands | **\$400** | **\$9,680** | High-CPA Affiliates + Courses |
| **4. Niche Authority / B2B** | **Hundreds** | **\$1,736+** | **\$42,000+** | Retainers, High-Ticket Deals (\$3K–\$106K) |

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- Chrome / Chromium (optional, for browser automation)

### Installation
```bash
# Clone the repository
git clone https://github.com/maurerlajos1/youtube-cge-agent.git
cd youtube-cge-agent

# Install dependencies
pip install opencv-python pillow playwright requests numpy tabulate
playwright install chromium
```

### Testing the Suite
```bash
# Run the Outlier Radar
python cge_engine/icahn_radar.py

# Test the Thumbnail Grader
python cge_engine/thumbnail_analyzer.py --sample

# Launch the Master Workbench
# Simply double click CGE_10X_MASTER_WORKBENCH.html or run:
start CGE_10X_MASTER_WORKBENCH.html
```

---

## 📜 License

MIT License — feel free to use, modify, and build upon this engine for personal and commercial projects.
