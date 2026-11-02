#!/usr/bin/env python3
"""
Niche 2.0 & Cash Code True Business RPM Calculator
==================================================
Reverse-engineered & 10x upgraded implementation of Shane Hummus's:
- `cge-niche-finder-niche-20-skill` (Niche Validator Pro / YouTube Niche Growth AI)
- `cge-niche-monetization-skill` & `cge-monetization-skill-for-clients` (Module #1 & Module #7)
- Niche Hypothesis Statement (`I HELP "X" OVERCOME "Y" BY DOING "Z"`, Slide 077)
- Level 1 -> Level 3 -> Level 5 Monetization Ladder (Slides 078 - 081)
- 6-Stage Water-Body Expansion Roadmap (Puddle -> Pond -> Lake -> River -> Sea -> Ocean)
- True Business RPM ($20 Edu AdSense vs $400 Affiliate RPM vs $1,736+ B2B Authority RPM, Slides 070 - 071)

Usage:
  python cge_engine/niche_20_calculator.py --market "Plumbing & HVAC Business Owners" --problem "losing leads to missed calls" --solution "24/7 AI voice & SMS booking agents" --offer-price 3500 --target-income 30000
"""

import argparse
import json
import math
from typing import Dict, Any


def build_niche_20_blueprint(
    market_x: str,
    problem_y: str,
    solution_z: str,
    offer_price: float = 3000.0,
    affiliate_cpa: float = 150.0,
    adsense_rpm: float = 22.0,
    target_monthly_income: float = 20000.0,
) -> Dict[str, Any]:
    # 1. Verbatim Niche Hypothesis Statements (Slide 077)
    short_hypothesis = f'I HELP "{market_x.upper()}" OVERCOME "{problem_y.upper()}"'
    full_hypothesis = f'I HELP "{market_x.upper()}" OVERCOME "{problem_y.upper()}" BY DOING "{solution_z.upper()}"'

    # 2. Level 1 -> Level 3 -> Level 5 Value Ladder (Slides 078 - 081)
    value_ladder = {
        "Level_1_Beginner_Spectator_Trap": {
            "avatar": f"Students / Hobbyists curious about {solution_z}",
            "hypothesis": f"I help students learn basic {solution_z} concepts.",
            "verdict": "AVOID FOR MONETIZATION — High views needed, low purchasing power ($2-$6 RPM).",
        },
        "Level_3_Career_Prosumer_Sweet_Spot": {
            "avatar": f"Solo practitioners / Professionals in {market_x}",
            "hypothesis": f"I help {market_x} overcome {problem_y} using {solution_z} templates & self-paced systems.",
            "verdict": "GREAT FOR AFFILIATES + COURSES ($49-$997) — Target $150-$400 True RPM (like Zach of All Trades & Josh Madakor).",
        },
        "Level_5_High_Ticket_B2B_Goldmine": {
            "avatar": f"Established {market_x} / Decision Makers with budget",
            "hypothesis": full_hypothesis,
            "verdict": "ULTIMATE CASH CODE — Converts on 50 to 500 views/video at $1,000-$3,000+ True RPM (like Karla Singson's $106,200 contract & Sean's $500K/mo).",
        },
    }

    # 3. Water-Body Expansion Roadmap (Puddle -> Ocean)
    water_body_roadmap = [
        {
            "stage": "1. The Puddle (Videos 1 - 15 | Months 1 - 3)",
            "focus": f"Hyper-specific pain solving '{problem_y}' exclusively for '{market_x}' using '{solution_z}'.",
            "goal": "Zero competition, rapid buyer trust, first $10K in 18-60 days with <1,000 subscribers.",
        },
        {
            "stage": "2. The Pond (Videos 16 - 30 | Months 4 - 6)",
            "focus": f"Expand to all top 3 bottlenecks facing '{market_x}' (Hiring, Operations, Lead Gen, Retention).",
            "goal": "Hit 30-Video Evolution Rule milestone; identify top 3 outlier formats and double down.",
        },
        {
            "stage": "3. The Lake (Months 6 - 12)",
            "focus": f"Expand from '{market_x}' to adjacent industries needing '{solution_z}'.",
            "goal": "Scale from $10K-$30K/mo to $50K-$100K/mo using a 50/50 mix of ICAHN Reach Outliers and Level-5 Buyer Videos.",
        },
        {
            "stage": "4. The Ocean — Hybrid Personal Brand (Months 12+)",
            "focus": "'You Are The Niche' (Alex Hormozi / Doug DeMuro model). Broad entrepreneurship, wealth, and case studies.",
            "goal": "Unlock all 6 Hybrid Personal Brand streams: AdSense + Affiliates + Sponsors + Talent/Job Opportunities + SaaS/Membership + High-Ticket.",
        },
    ]

    # 4. Cash Code Monetization Math & Views Needed
    # Conversion assumptions based on CGE benchmarks:
    # - Video Views -> Description Link Click-Through Rate (CTR): 2.5% on Buyer/Edu videos
    # - Link Clicks -> Booked Strategy Call / Application Rate: 12%
    # - Booked Call -> Show-up & Close Rate: 25%
    # Net View-to-High-Ticket-Client Conversion Rate = 0.025 * 0.12 * 0.25 = 0.00075 (0.075%, or 1 client per ~1,333 targeted views)
    view_to_client_rate = 0.00075
    clients_needed = math.ceil(target_monthly_income / max(offer_price, 1.0))
    views_needed_high_ticket = int(math.ceil(clients_needed / view_to_client_rate))
    high_ticket_true_rpm = round((offer_price * view_to_client_rate) * 1000.0, 2)

    # Affiliate math (assuming 2.5% link click rate * 4% affiliate conversion = 0.1% view-to-sale, or 1 sale per 1,000 views)
    affiliate_sales_needed = math.ceil(target_monthly_income / max(affiliate_cpa, 1.0))
    views_needed_affiliate = affiliate_sales_needed * 1000
    affiliate_true_rpm = round(affiliate_cpa * 1.0, 2)

    # Pure AdSense math
    views_needed_adsense = int(math.ceil((target_monthly_income / max(adsense_rpm, 1.0)) * 1000))
    entertainment_views_needed = int(math.ceil((target_monthly_income / 2.0) * 1000))

    return {
        "niche_hypothesis_short": short_hypothesis,
        "niche_hypothesis_full": full_hypothesis,
        "value_ladder_levels_1_3_5": value_ladder,
        "water_body_expansion_roadmap": water_body_roadmap,
        "cash_code_monetization_math": {
            "target_monthly_income_usd": target_monthly_income,
            "model_A_entertainment_adsense_2_rpm": {
                "rpm_usd": 2.0,
                "monthly_views_required": entertainment_views_needed,
            },
            "model_B_education_adsense": {
                "rpm_usd": adsense_rpm,
                "monthly_views_required": views_needed_adsense,
            },
            "model_C_affiliate_plus_adsense_shane_main_channel": {
                "affiliate_cpa_usd": affiliate_cpa,
                "combined_true_rpm_usd": round(affiliate_true_rpm + adsense_rpm, 2),
                "sales_needed_per_month": affiliate_sales_needed,
                "monthly_views_required": views_needed_affiliate,
            },
            "model_D_high_ticket_cash_code_shane_2nd_channel": {
                "offer_price_usd": offer_price,
                "clients_needed_per_month": clients_needed,
                "estimated_booked_calls_needed": clients_needed * 4,
                "true_business_rpm_usd": high_ticket_true_rpm,
                "monthly_views_required": views_needed_high_ticket,
                "views_per_video_at_4_videos_per_month": math.ceil(views_needed_high_ticket / 4),
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Niche 2.0 & Cash Code True Business RPM Calculator")
    parser.add_argument("--market", "-x", required=True, help="Market X (e.g. 'Roofing & HVAC Business Owners')")
    parser.add_argument("--problem", "-y", required=True, help="Problem Y (e.g. 'losing $20k/mo in missed calls')")
    parser.add_argument("--solution", "-z", required=True, help="Solution Z (e.g. '24/7 AI voice booking agents')")
    parser.add_argument("--offer-price", type=float, default=3500.0, help="High-ticket offer price in USD")
    parser.add_argument("--affiliate-cpa", type=float, default=150.0, help="Affiliate commission per sale in USD")
    parser.add_argument("--adsense-rpm", type=float, default=25.0, help="Educational AdSense RPM in USD")
    parser.add_argument("--target-income", type=float, default=20000.0, help="Target monthly income in USD")
    args = parser.parse_args()

    blueprint = build_niche_20_blueprint(
        market_x=args.market,
        problem_y=args.problem,
        solution_z=args.solution,
        offer_price=args.offer_price,
        affiliate_cpa=args.affiliate_cpa,
        adsense_rpm=args.adsense_rpm,
        target_monthly_income=args.target_income,
    )
    print(json.dumps(blueprint, indent=2))


if __name__ == "__main__":
    main()
