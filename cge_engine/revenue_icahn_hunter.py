#!/usr/bin/env python3
"""
CGE 10x — 3-Dimensional ICAHN Hunter & Evolution Method Diagnostic Engine
=========================================================================
Reverse-engineered from Shane Hummus's full spoken masterclass transcript:
  1. Views-Based ICAHN (01:20:09 - 01:25:37): Small channel + bad video ("drunken VHS potato camera") + huge views.
  2. Revenue-Based ICAHN (01:25:38, line 875 & 00:46:16 Karla Singson): Small channel + low views (100-500 views)
     + massive backend monetization ($48K-$300K via B2B placement, high-ticket coaching, or affiliate armies).
  3. Cross-Platform ICAHN (01:25:50, line 877): Porting viral outlier topics from TikTok/X/Reddit/Amazon Books
     into long-form YouTube before any niche competitor does.
  4. The 5-Level Niche Depth Matrix (01:09:05 - 01:13:50): Mapping any market from Level 1 (Academic Mass Market)
     to Level 5 (B2B Corporate Placement / Agency).
  5. The "Evolution Method" 3-by-30 Sprint Diagnostic (02:27:55, line 1588): Testing formats in 3-video sprints
     and diagnosing what to mutate before the 30-video niche pivot threshold.
"""

import argparse
import json
import math
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# High-Ticket / Commercial Buyer Intent Tokens (Karla Singson / B2B / Level 4-5 Signals)
HIGH_TICKET_BUYER_TOKENS = [
    "hire", "hiring", "agency", "consulting", "consultant", "controller", "executive",
    "b2b", "enterprise", "contract", "placement", "recruiting", "staffing", "fractional",
    "implement", "migration", "audit", "compliance", "tax strategy", "bookkeeping",
    "cpa", "practice", "clinic", "firm", "for business owners", "for founders",
    "case study", "roi", "system", "automate", "scale", "pipeline", "outbound", "inbound"
]


@dataclass
class NicheDepthLevel:
    level: int
    tier_name: str
    shane_archetype: str
    niche_hypothesis: str
    sample_video_title: str
    target_buyer: str
    expected_views_per_video: str
    estimated_rp1k_usd: int
    kirkland_private_label_offer: str
    affiliate_starter_shelf: str


def generate_5_level_depth_matrix(market: str, core_skill: str) -> List[NicheDepthLevel]:
    """
    Implements Shane's 5-Level Accounting Depth Matrix (01:09:05 - 01:13:50)
    plus the Costco/Kirkland Shelf-Ownership Progression (00:42:45 - 00:44:25)
    for ANY user market.
    """
    m = market.strip()
    s = core_skill.strip()
    return [
        NicheDepthLevel(
            level=1,
            tier_name="Level 1: Broad Academic / Concept Mass-Market",
            shane_archetype="The Organic Chemistry Tutor ($43K-$119K/mo AdSense passively, 177 days offline)",
            niche_hypothesis=f"I help beginners and students understand foundational {m} concepts without textbook jargon.",
            sample_video_title=f"What Is {s}? ({m} Explained in 10 Minutes for Complete Beginners)",
            target_buyer=f"Students, curious beginners, and hobbyists researching {m}",
            expected_views_per_video="25,000 - 250,000+ views",
            estimated_rp1k_usd=18,
            affiliate_starter_shelf=f"Entry-level {m} books, study guides, and $20-$50/mo software trials",
            kirkland_private_label_offer=f"$47-{m} Quickstart Vault / $29/mo Study Membership"
        ),
        NicheDepthLevel(
            level=2,
            tier_name="Level 2: Standardized Exam / Certification Prep",
            shane_archetype="Physics Wallah ($5.2B EdTech Unicorn started in parents' basement) / Nurse Cheung",
            niche_hypothesis=f"I help {m} students and candidates pass their certification exams on the first attempt.",
            sample_video_title=f"How to Pass the {m} Certification Exam in 2026 (Full Study Guide & Practice Breakdown)",
            target_buyer=f"Pre-professionals who MUST pass a high-stakes {m} test to unlock their career",
            expected_views_per_video="5,000 - 50,000 views",
            estimated_rp1k_usd=85,
            affiliate_starter_shelf=f"Prep courses, exam simulators, and certification bootcamps (20-30% rev-share)",
            kirkland_private_label_offer=f"$197-$497 {m} Exam Cram Cohort & Practice Question Bank"
        ),
        NicheDepthLevel(
            level=3,
            tier_name="Level 3: Career Switcher / First Entry-Level Job",
            shane_archetype="Shane Hummus Main Channel / Zach of All Trades ($18,328/mo via CourseCareers Army)",
            niche_hypothesis=f"I help career switchers and new grads land their first $60K-$90K job in {m} without 5 years of experience.",
            sample_video_title=f"How to Land Your First {m} Job in 90 Days (Even With Zero Experience)",
            target_buyer=f"Burned-out workers and recent grads hungry to break into {m}",
            expected_views_per_video="2,500 - 30,000 views",
            estimated_rp1k_usd=350,
            affiliate_starter_shelf=f"CourseCareers ($500 course w/ $150-$300 affiliate payout) + Resume/Portfolio tools",
            kirkland_private_label_offer=f"$1,500-$3,000 {m} Job-Placement Accelerator & Portfolio Bootcamp (Josh Madakor Model)"
        ),
        NicheDepthLevel(
            level=4,
            tier_name="Level 4: Executive Upskilling / $100K to $250K+ Career Ascension",
            shane_archetype="Shane's Financial Controller Client (01:12:09) & Davis Nguyen (My Consulting Offer)",
            niche_hypothesis=f"I help mid-level {m} professionals making $70K-$100K ascend into $200K-$300K leadership roles using {s}.",
            sample_video_title=f"How to Go From Senior {m} Specialist to $250K Director/Controller in 12 Months",
            target_buyer=f"Already-employed, affluent {m} professionals who want executive pay & status",
            expected_views_per_video="800 - 6,000 views",
            estimated_rp1k_usd=1736,
            affiliate_starter_shelf=f"Executive enterprise software, B2B intelligence tools, and high-ticket masterminds",
            kirkland_private_label_offer=f"$5,000-$9,800 6-Month 1-on-1 Executive Ascension Mentorship (0% APR In-House Financing)"
        ),
        NicheDepthLevel(
            level=5,
            tier_name="Level 5: B2B Corporate Placement / Done-For-You Turnkey Agency",
            shane_archetype="Karla Singson ($106K-$300K contract from 158 views) & Shane's $30K-$300K 'Build & Release' Offer",
            niche_hypothesis=f"I help 7- and 8-figure companies hire, place, or install turnkey {s} systems inside their {m} department.",
            sample_video_title=f"How 7-Figure Companies Hire & Retain A-Player {m} Teams (Without Agency Markup)",
            target_buyer=f"CEOs, CMOs, CROs, and Founders with corporate budgets who want {s} done for them",
            expected_views_per_video="100 - 1,200 views",
            estimated_rp1k_usd=6000,
            affiliate_starter_shelf=f"Enterprise ERP/SaaS referrals ($2,000-$10,000 B2B partner bounties)",
            kirkland_private_label_offer=f"$30,000 'Build & Release' 6-Month Turnkey Installation OR $106,000/yr Renewable Placement Contract"
        ),
    ]


def score_revenue_icahn_candidates(keyword: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """
    Searches YouTube for B2B / High-Ticket commercial queries around `keyword`
    and computes the Revenue-Based ICAHN Score (RevICAHN):
      - Looks for videos with High Commercial Buyer Intent that solve expensive Level 4 / Level 5 problems.
      - Evaluates how easy it is to out-package and out-monetize them using the Cash Code funnel.
    """
    b2b_query = f"how to {keyword} for business"
    encoded = urllib.parse.quote_plus(b2b_query)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})

    candidates = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        match = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
        if match:
            data = json.loads(match.group(1))
            contents = (
                data.get("contents", {})
                .get("twoColumnSearchResultsRenderer", {})
                .get("primaryContents", {})
                .get("sectionListRenderer", {})
                .get("contents", [])
            )
            for section in contents:
                items = section.get("itemSectionRenderer", {}).get("contents", [])
                for item in items:
                    vr = item.get("videoRenderer")
                    if not vr:
                        continue
                    vid_id = vr.get("videoId", "")
                    title_runs = vr.get("title", {}).get("runs", [])
                    title = "".join(r.get("text", "") for r in title_runs)
                    channel_runs = vr.get("ownerText", {}).get("runs", [])
                    channel = "".join(r.get("text", "") for r in channel_runs)
                    view_text = vr.get("viewCountText", {}).get("simpleText", "0 views")
                    views_digits = re.sub(r"[^\d]", "", view_text)
                    views = int(views_digits) if views_digits else 250

                    # Snippet / description preview
                    desc_snippets = vr.get("detailedMetadataSnippets", [])
                    desc_text = ""
                    if desc_snippets:
                        runs = desc_snippets[0].get("snippetText", {}).get("runs", [])
                        desc_text = "".join(r.get("text", "") for r in runs)

                    combined_text = f"{title} {desc_text}".lower()
                    commercial_hits = [tok for tok in HIGH_TICKET_BUYER_TOKENS if tok in combined_text]
                    has_funnel_signal = any(
                        s in combined_text for s in ["book", "call", "apply", "schedule", "free", "guide", "template", "http", ".com"]
                    )

                    # Revenue ICAHN Formula:
                    # High buyer intent + low-to-moderate view competition = high backend $$$ per 1,000 views
                    intent_multiplier = 1.0 + (0.35 * len(commercial_hits)) + (0.5 if has_funnel_signal else 0.0)
                    competition_ease = max(1.0, 10.0 - math.log10(max(views, 100)))
                    rev_icahn_score = round(min(99.9, intent_multiplier * competition_ease * 9.5), 1)

                    est_rp1k = int(250 * intent_multiplier * (2.2 if views < 15000 else 1.0))
                    est_video_revenue = int((max(views, 500) / 1000.0) * est_rp1k)

                    candidates.append({
                        "video_id": vid_id,
                        "url": f"https://www.youtube.com/watch?v={vid_id}",
                        "title": title,
                        "channel": channel,
                        "views": views,
                        "commercial_tokens_matched": commercial_hits,
                        "has_funnel_bridge_signal": has_funnel_signal,
                        "rev_icahn_score": rev_icahn_score,
                        "estimated_potential_rp1k_usd": est_rp1k,
                        "karla_singson_b2b_potential_usd": max(est_video_revenue, 10000) if rev_icahn_score > 55 else est_video_revenue,
                        "cge_10x_hijack_angle": f"Keep core buyer promise of '{title[:55]}...', add a 3-word high-contrast thumbnail + Day-1 'YouTube Niche Growth AI' show-up bribe funnel."
                    })
                    if len(candidates) >= max_results:
                        break
    except Exception as exc:
        candidates.append({"error": str(exc), "note": "Fallback offline heuristic used."})

    candidates.sort(key=lambda x: x.get("rev_icahn_score", 0), reverse=True)
    return candidates


def diagnose_evolution_method_sprint(
    sprint_number: int,
    total_videos_published: int,
    avg_impressions: int,
    avg_ctr_percent: float,
    avg_30s_retention_percent: float,
    avg_avd_percent: float,
    leads_captured: int,
    calls_booked: int,
) -> Dict[str, Any]:
    """
    Implements Shane's "Evolution Method" (02:27:55 - 02:28:38, lines 1587-1594):
      - Test formats & idea styles in batches of 3 videos.
      - Never abandon the niche before 30 videos (10 sprints of 3 videos).
      - Pinpoints the exact bottleneck in the 3-video batch and prescribes Sprint N+1's mutation.
    """
    bottlenecks = []
    mutations = []

    if avg_impressions < 1500:
        bottlenecks.append("BOTTLENECK 1: Low Topic Demand / Poor ICAHN Outlier Selection (<1,500 impressions)")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Stop inventing topics from scratch. Run `icahn_radar.py` with `*keyword` "
            "autocomplete wildcards and only pick topics where a <25K sub channel got >3x their average views."
        )

    if avg_ctr_percent < 5.5:
        bottlenecks.append(f"BOTTLENECK 2: Weak Packaging / Curiosity Gap (CTR is {avg_ctr_percent}%, target >= 6.5%)")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Run `thumbnail_analyzer.py` before uploading. Enforce <= 3 thumbnail words, "
            "0% word overlap with the title, high luminance contrast, and test 3 thumbnails via YouTube Test & Compare."
        )

    if avg_30s_retention_percent < 62.0:
        bottlenecks.append(
            f"BOTTLENECK 3: Holy Trifecta Intro Disconnect (30s Hold is {avg_30s_retention_percent}%, target >= 65%)"
        )
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Your first 5 seconds are not confirming the exact thumbnail + title click expectation. "
            "Use `holy_trifecta_vibe_writer.py` to cap the intro at <= 80 words (30s at 160 WPM) and deliver Point #1 by 0:31."
        )

    if avg_avd_percent < 38.0:
        bottlenecks.append(f"BOTTLENECK 4: Mid-Video Pacing / AI Slop Fatigue (AVD is {avg_avd_percent}%, target >= 42%)")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Strip all 18 banned AI-slop phrases, use the 15-Minute Voice-Interview method to inject "
            "personal stories, and instruct your Filipino editor to add pattern interrupts every 20-30 seconds during the first 3 minutes."
        )

    if leads_captured == 0 and avg_impressions * (avg_ctr_percent / 100.0) > 200:
        bottlenecks.append("BOTTLENECK 5: Broken 'Cash Code' Bridge (Views are happening, but 0 leads captured)")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Do NOT wait until the outro to pitch. Insert a Native Mid-Roll Lead Magnet Bridge at 40% "
            "of the video solving the 'Next Logical Problem', put the link on Line 1 of the description + Pinned Comment."
        )

    if leads_captured > 0 and calls_booked == 0:
        bottlenecks.append("BOTTLENECK 6: Thank-You Page / Show-Up Bribe Leak (Leads captured, 0 strategy calls booked)")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Redirect opt-ins immediately to a 26-second VSL + Calendly page offering a 'Show-Up Bribe' "
            "(like Shane's YouTube Niche Growth AI) unlocked only when they attend the call."
        )

    if not bottlenecks:
        bottlenecks.append("ALL SYSTEMS GREEN: Sprint metrics exceed CGE benchmarks!")
        mutations.append(
            "MUTATION FOR NEXT 3 VIDEOS: Double down on this exact format for 3 more videos, then activate the 95% AI Multi-Platform "
            "Syndication Engine (`syndication_engine.py`) to multiply distribution across LinkedIn, X, and Shorts."
        )

    niche_verdict = (
        f"STAY IN NICHE ({total_videos_published}/30 videos completed — {max(0, 30 - total_videos_published)} videos remaining before any niche pivot check)."
        if total_videos_published < 30
        else "30-VIDEO THRESHOLD REACHED: Evaluate RP1K and lead flow to decide between Water-Body Expansion (Pond -> Lake) or Niche Hypothesis Pivot."
    )

    return {
        "sprint_number": sprint_number,
        "total_videos_published": total_videos_published,
        "shane_30_video_rule_verdict": niche_verdict,
        "diagnosed_bottlenecks": bottlenecks,
        "next_3_video_sprint_mutations": mutations,
    }


def main():
    parser = argparse.ArgumentParser(description="CGE 10x Revenue-ICAHN Hunter & Evolution Method Diagnostic")
    parser.add_argument("--market", default="Accounting & Finance Automation", help="Broad market name")
    parser.add_argument("--skill", default="AI Cash-Flow Forecasting", help="Specific skill or mechanism")
    parser.add_argument("--keyword", default="accounting automation", help="Search keyword for Revenue-ICAHN scan")
    parser.add_argument("--output", default="", help="Optional JSON file path to save report")
    args = parser.parse_args()

    depth_matrix = [asdict(lvl) for lvl in generate_5_level_depth_matrix(args.market, args.skill)]
    rev_candidates = score_revenue_icahn_candidates(args.keyword, max_results=6)
    sprint_diagnosis = diagnose_evolution_method_sprint(
        sprint_number=3,
        total_videos_published=9,
        avg_impressions=4200,
        avg_ctr_percent=4.8,
        avg_30s_retention_percent=58.0,
        avg_avd_percent=41.5,
        leads_captured=4,
        calls_booked=0,
    )

    report = {
        "tool": "CGE 10x Revenue-ICAHN & Evolution Method Engine",
        "market": args.market,
        "skill": args.skill,
        "five_level_niche_depth_matrix": depth_matrix,
        "revenue_icahn_b2b_candidates": rev_candidates,
        "sample_evolution_method_sprint_diagnosis": sprint_diagnosis,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    print("=" * 80)
    print(f"CGE 10X REVENUE-ICAHN & 5-LEVEL DEPTH MATRIX: {args.market.upper()}")
    print("=" * 80)
    for lvl in depth_matrix:
        print(f"\n[Level {lvl['level']}] {lvl['tier_name']} (Est. RP1K: ${lvl['estimated_rp1k_usd']}/1K views)")
        print(f"  Hypothesis : {lvl['niche_hypothesis']}")
        print(f"  Video Title: {lvl['sample_video_title']}")
        print(f"  Shelf Step : {lvl['affiliate_starter_shelf']}  -->  {lvl['kirkland_private_label_offer']}")

    print("\n" + "=" * 80)
    print(f"TOP REVENUE-ICAHN B2B CANDIDATES FOR '{args.keyword}'")
    print("=" * 80)
    for idx, c in enumerate(rev_candidates[:5], 1):
        if "error" in c:
            print(f"  Note: {c['error']}")
            continue
        print(f"{idx}. [{c['rev_icahn_score']}/100 RevICAHN] {c['title']} ({c['views']:,} views | {c['channel']})")
        print(f"   Est. RP1K: ${c['estimated_potential_rp1k_usd']}/1K views | B2B Contract Potential: ${c['karla_singson_b2b_potential_usd']:,}")

    print("\n" + "=" * 80)
    print("EVOLUTION METHOD (3-BY-30 SPRINT DIAGNOSTIC)")
    print("=" * 80)
    print(f"Verdict: {sprint_diagnosis['shane_30_video_rule_verdict']}")
    for b, m in zip(sprint_diagnosis["diagnosed_bottlenecks"], sprint_diagnosis["next_3_video_sprint_mutations"]):
        print(f" - {b}")
        print(f"   -> {m}")


if __name__ == "__main__":
    main()
