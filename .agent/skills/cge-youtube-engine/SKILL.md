---
name: cge-youtube-engine
description: Autonomous YouTube Growth & Monetization Engine combining Shane Hummus's reverse-engineered Content Growth Engine (CGE) 9 Claude Skills, 12 Custom GPTs, Niche 2.0, the Carl Icahn Outlier Method, the Holy Trifecta Packaging System, VibeWriter Anti-Slop Scripting, and 2026 Industry SOTA (Paddy Galloway, Derral Eves, Ed Lawrence RevTrack, Aprilynne Alter). Activate this skill whenever planning a YouTube channel, validating a niche, hunting outlier video ideas, grading or designing thumbnails, writing titles and 30-second intros, drafting YouTube scripts, or building high-ticket/affiliate YouTube funnels.
---

# Content Growth Engine (CGE) 10x — Autonomous YouTube Skill Suite

This skill integrates **all 9 of Shane Hummus's internal Claude Personal Skills**, **12 Custom GPT workflows**, and **3 local Python execution tools** located in `H:\Youtube agent\cge_engine\`.

---

## 1. Local Executable Tools (`H:\Youtube agent\cge_engine\`)

Always run these local Python tools to gather live data or objective metrics before generating recommendations:

### A. Automated ICAHN Outlier & Wildcard Keyword Radar (`icahn_radar.py`)
Executes Shane's 3-Step ICAHN Method live against YouTube's autocomplete and search engine (no API keys required):
```powershell
python "H:\Youtube agent\cge_engine\icahn_radar.py" --keyword "<root_keyword>" --max-results 15 --output "H:\Youtube agent\cge_engine\latest_icahn_report.json"
```
- **Step 1 (Outlier Discovery)**: Scrapes live YouTube search results, view counts, channel names, upload dates, and calculates the **Cohort Outlier Multiplier** and **Psychological Hook Archetype**.
- **Step 2 (`*keyword` Wildcard Expansion)**: Queries YouTube's autocomplete API across `* <keyword>`, `worst <keyword>`, `best <keyword>`, `<keyword> for ...`, `how to <keyword>`, and `truth about <keyword>`.
- **Step 3 (Slight Twist Generator)**: Generates 5 Reach Outlier titles + 5 High-Ticket Buyer titles with synchronized thumbnail text and 0–5s Click Confirmation hooks.

### B. Computer-Vision Thumbnail Analyzer (`thumbnail_analyzer.py`)
Executes Shane's leaked *High-converting Thumbnail Toolkit™* (`slide_133`–`134`) + 2026 SOTA vision grading:
```powershell
python "H:\Youtube agent\cge_engine\thumbnail_analyzer.py" --image "<path_to_thumbnail.png>" --title "<proposed_video_title>" --thumb-text "<text_on_thumbnail>"
```
- Scores **Luminance Contrast (20 pts)**, **Saturation Pop (15 pts)**, **Rule-of-Thirds & Clutter Index (25 pts)**, **Mobile `168x94px` Squint Survival (20 pts)**, and **Title-to-Thumbnail Complementarity (20 pts)**.
- Generates an annotated `*_cge_audit.png` showing the red 3x3 Rule-of-Thirds grid lines, the 4 yellow intersection power points, and an embedded `168x94px` mobile feed preview.

### C. Niche 2.0, Value Ladder & Cash Code RPM Calculator (`niche_20_calculator.py`)
Computes the Niche Hypothesis Statement (`I HELP "X" OVERCOME "Y" BY DOING "Z"`), Level 1/3/5 Value Ladder, Water-Body Expansion Roadmap (*Puddle → Ocean*), and exact views required to hit any monthly income target:
```powershell
python "H:\Youtube agent\cge_engine\niche_20_calculator.py" --market "<Avatar X>" --problem "<Problem Y>" --solution "<Mechanism Z>" --offer-price 3500 --target-income 25000
```

---

## 2. The 9 Internal CGE Sub-Skills (Operating Protocols)

When the user invokes this skill or asks for any step of the YouTube workflow, execute the matching sub-skill below:

### Skill 1: `cge-niche-finder-niche-20-skill` (*Niche Validator Pro / YouTube Niche Growth AI*)
1. Run `niche_20_calculator.py` with the user's candidate avatar (`X`), problem (`Y`), and mechanism (`Z`).
2. Enforce the **4-Circle Niche 2.0 Rule**: (1) Passion/Sustainability, (2) Unfair Skill/Experience, (3) Small-Channel Outlier Demand (`<10K` sub channels hitting `>50K` views), and (4) High Monetization Ceiling.
3. Always push the user up the **Value Ladder** from **Level 1** (broke students/spectators) to **Level 3** (career switchers/prosumers at \$150–\$400 True RPM) or **Level 5** (B2B decision-makers at \$1,000–\$3,000+ True RPM).
4. Map out their **Water-Body Expansion**:
   - **Puddle (Videos 1–15)**: Minimum Viable Specificity (e.g., *"Personal Finance for Single Moms"* or *"AI Voice Agents for Plumbers"*).
   - **Pond (Videos 16–30)**: Adjacent pain points for the same avatar.
   - **Lake → Ocean (Videos 31+)**: Hybrid Personal Brand (*"You Are The Niche"*).

### Skill 2: `cge-video-idea-finder-icahn-method-skill` (*30-Second Video Idea Generator*)
1. Run `icahn_radar.py --keyword "<niche_keyword>"`.
2. Filter for **Golden Icahn Targets**: Small channels where a video achieved `>5x–100x` its channel baseline *despite* mediocre packaging (ugly Canva thumbnail, slow intro).
3. Apply the **Slight Twist Rule (`slide_098`)**: Never copy the exact competitor title/keywords verbatim. Twist the angle slightly and split the output 50/50 between:
   - **Reach Outlier Videos** (for Browse/Suggested discovery & AdSense/Affiliates)
   - **Karla Singson Buyer Videos** (hyper-specific Level-5 problem videos designed to close \$3K–\$100K clients on `<500 views`).

### Skill 3: `cge-holy-trifecta-title-thumbnail-intro` (*Holy Trifecta Packaging Architect*)
Never write a script before locking in the **Holy Trifecta** (**Thumbnail 👉 Title 👉 First 30s Intro**):
1. **Thumbnail Blueprint (The Eye-Tracking Hierarchy, `slide_133`)**:
   - **Right 1/3 Intersection**: Close-up high-res face shot blown up so **THE WHITES OF THE EYES** are clearly visible, with minimal gap above the head or below the chin.
   - **Left 2/3 Zone**: Maximum 1 high-contrast visual prop + **2–4 words of bold text** that **complements (never repeats)** the video title.
   - **3-Variant Test & Compare**: Output 3 distinct thumbnail angles: (A) *Close-up Face + Prop*, (B) *Red ❌ vs. Green ✅ Split Comparison*, and (C) *Pure Data/Object Close-up (No Face)*.
2. **Title Engineering**: Pair with 3 curiosity-gap or negativity-bias titles.
3. **The 4-Part 30-Second Intro (65–85 words max)**:
   - `0:00–0:05` **Click Confirmation**: Validate the exact promise of the title/thumbnail in sentence #1.
   - `0:05–0:15` **Curiosity Loop & Stakes**: Tease a counterintuitive point later in the video (`#3` or `#1`) and state the cost of getting this wrong.
   - `0:15–0:22` **1-Sentence Proof**: Why the viewer can trust your breakdown.
   - `0:22–0:30` **Fast Dive into Point #1**: Zero channel bumper, zero *"Hey guys, welcome back!"*

### Skill 4: `youtube-script-writer-skill` (*VibeWriter Content Creation AI Deluxe*)
1. **Anti-AI-Slop Cadence**: Never use words like *delve, tapestry, testament, moreover, in today's fast-paced world*. Write at a conversational 6th–8th grade spoken level with short punchy sentences.
2. **Voice Interview First**: Ask 3 rapid questions (or ingest the user's voice memo/transcript) to extract real stories, contrarian takes, and specific numbers before drafting.
3. **Scriptwriting Alchemy Structure**:
   - **0:00–0:30**: Synchronized Holy Trifecta Intro.
   - **Every 90–120 Seconds**: Insert a **Pattern Interrupt / Re-Hook** (*"Now Step 1 gets you started, but it completely backfires if you miss Step 2..."*) + visual B-roll state change cue.
   - **Mid-Roll Native Cash Code Bridge**: Embed a frictionless 15-second handoff to the lead magnet or booking link inside the middle teaching point (*"I put this entire calculator at the first link in the description so you can copy mine"*).
   - **Abrupt End-Screen Bridge**: Never say *"In conclusion"* or *"Thanks for watching."* End on the final insight and bridge directly to a specific **Buyer Video** on the end screen to maximize YouTube Session Time.

### Skill 5: `cge-monetization-skill-for-clients` & `cge-niche-monetization-skill` (*The Cash Code System*)
- Design the **6-Stream Hybrid Monetization Stack** (`AdSense`, `Affiliates`, `Sponsorships` even at `<500 subs` like Guy's \$1,500 deal, `Job/Network Opportunities`, `Membership/SaaS`, and `High-Ticket Offer`).
- Generate the **Lead Magnet + Thank-You VSL Funnel** (including the Gmail *"I know the sender"* calendar confirmation step from `slide_146` and the 5-step pre-call indoctrination page from `slide_148`).

### Skill 6: `youtube-launch-loop-post-upload-analytics` (*Post-Upload Diagnostic & Evolution Method*)
- Enforce the **3-Video Triad & 30-Video Evolution Rule**.
- Diagnose 24-hour post-upload metrics:
  - **CTR `< 4.5%` + APV `> 45%`** $\rightarrow$ Keep video, immediately swap Thumbnail/Title using `thumbnail_analyzer.py`.
  - **CTR `> 6.5%` + 30-Second Retention `< 65%`** $\rightarrow$ Intro failed Click Confirmation; trim fluff in YouTube Studio Editor.
  - **High Views + `\$0` Revenue** $\rightarrow$ Topic is Level 1 spectator bait; pivot next triad to Level 3/5 buyer problems.

### Skill 7: `prospect-interaction-analyzer-audience-language`
- Mine YouTube comment sections, sales call transcripts, and Reddit/forum threads to extract verbatim buyer pain phrases, objections, and false beliefs to feed back into `icahn_radar.py`.

### Skill 8: `cge-revenue-icahn-and-5-level-depth` (`H:\Youtube agent\cge_engine\revenue_icahn_hunter.py`)
- Run `python "H:\Youtube agent\cge_engine\revenue_icahn_hunter.py" --market "<Market>" --skill "<Skill>" --keyword "<Keyword>"` to:
  1. Generate Shane's **5-Level Niche Depth Matrix** (Level 1 Academic Mass Market $\rightarrow$ Level 2 Exam/Cert Prep $\rightarrow$ Level 3 Entry-Level Job $\rightarrow$ Level 4 Executive \$200K–\$300K Ascension $\rightarrow$ Level 5 B2B Placement/Agency) + **Costco/Kirkland Private-Label Shelf Progression**.
  2. Hunt **Revenue-Based ICAHN B2B Candidates** (the Karla Singson \$106K–\$300K from 158 views model).
  3. Run the **3-by-30 Evolution Method Sprint Diagnostic**.

### Skill 9: `cge-15min-voice-interview-and-95pct-syndication` (`H:\Youtube agent\cge_engine\syndication_engine.py`)
- Run `python "H:\Youtube agent\cge_engine\syndication_engine.py" --title "<Video Title>" --thumb-text "<3 Words>"` to:
  1. Generate the **5-Question 15-Minute Voice-Interview Extraction Prompts** (how Zach of All Trades scripted an 800K-view video in `<15 minutes`).
  2. Generate the **95% AI Multi-Platform Syndication Suite**: LinkedIn Authority Post + `Shane comment GPT for LI` 3-pack, X 7-post thread + `Shane comment GPT for X` 3-pack, 3 Vertical Shorts scripts with Related-Video bridges, YouTube Community Tab Poll, and Cash Code Story Email.
- Reference `H:\Youtube agent\COMPLETE_TRANSCRIPT_SYSTEMS_DEEP_DIVE.md` for all 14 hidden spoken transcript systems and the full Live Q&A vault.
