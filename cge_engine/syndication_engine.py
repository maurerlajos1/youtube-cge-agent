#!/usr/bin/env python3
"""
CGE 10x — 15-Minute Voice-Interview Ghostwriter & 95% AI Multi-Platform Syndication Engine
==========================================================================================
Reverse-engineered from Shane Hummus's full spoken masterclass transcript:
  1. The 15-Minute Voice-Interview VibeWriter Method (01:30:03 - 01:32:50, line 951):
     How Shane's 50-year-old brother Zach ("Zach of All Trades") scripted his 800,000-view
     first video in <15 minutes: VibeWriter interviews the creator with 5 targeted questions
     so they speak their real stories/opinions aloud, then weaves their answers into an
     anti-slop retention script.
  2. The 95% AI Multi-Platform Content Syndication System (01:19:06 - 01:19:50, lines 796-805
     & Slide 129 `Shane comment GPT for LI` / `Shane comment GPT for X`):
     Turns 1 long-form YouTube video into:
       - LinkedIn Authority Post + 3 High-Status Comment Replies (`Shane comment GPT for LI`)
       - X (Twitter) 7-Post Thread + 3 Viral Reply-Guy Hooks (`Shane comment GPT for X`)
       - 3 Vertical Shorts / Reels / TikTok Scripts with "Related Video" Bridge CTAs
       - YouTube Community Tab Pre-Warm Poll Post
       - "Cash Code" Story-Driven Email Newsletter + Show-Up Bribe Call CTA
"""

import argparse
import json
from typing import Dict, Any, List


def generate_voice_interview_prompts(
    title: str,
    niche_hypothesis: str,
    contrarian_belief: str,
) -> List[Dict[str, str]]:
    """
    Generates the 5-Question 15-Minute Voice Interview (Zach of All Trades Protocol)
    that extracts authentic human experience before scripting.
    """
    return [
        {
            "question_number": "Q1 (2 Mins - The Visceral Pain Story)",
            "prompt": f"Think about the exact person described in '{niche_hypothesis}'. What is the single most frustrating lie or bad piece of advice they've been told about '{title}'?",
            "why_shane_asks_this": "Creates the 'Mind-Reading' empathy hook in seconds 0:05-0:15 so viewers feel deeply understood."
        },
        {
            "question_number": "Q2 (3 Mins - The Personal / Client Proof Receipt)",
            "prompt": "Tell a quick 60-second real-life story (yours, a client's, or a mistake you witnessed in the trenches) that proves why the old way fails and your approach works.",
            "why_shane_asks_this": "Gives you an un-faked human 'Receipt' that 8 billion AI-slop channels cannot copy (02:20:03)."
        },
        {
            "question_number": "Q3 (4 Mins - The 3-Step Core Mechanism + Secret #2)",
            "prompt": f"If you had to explain your solution to a friend over coffee in 3 simple steps, what are they—and which one is your absolute favorite ('Secret #2') that surprises people the most?",
            "why_shane_asks_this": "Builds the open loop for seconds 0:15-0:30 ('Point #2 is my favorite because...') and structures the body."
        },
        {
            "question_number": "Q4 (3 Mins - The Contrarian Sacred Cow)",
            "prompt": f"Why do you believe '{contrarian_belief}' when 90% of beginners do the opposite? What happens if they ignore this warning?",
            "why_shane_asks_this": "Injects high-retention polarity and authority without sounding like corporate ChatGPT slop."
        },
        {
            "question_number": "Q5 (3 Mins - The Next Logical Problem / Cash Code Bridge)",
            "prompt": "Once the viewer learns these 3 steps from your free video, what is the 'implementation bottleneck' they will immediately hit next—and how does your free Lead Magnet / Strategy Call solve it?",
            "why_shane_asks_this": "Creates the seamless native mid-roll & outro bridge that turns 8,000 views into $48,000 (00:48:30)."
        }
    ]


def generate_95_percent_syndication_suite(
    video_title: str,
    thumbnail_text: str,
    niche_hypothesis: str,
    key_points: List[str],
    personal_story: str,
    lead_magnet_name: str,
    booking_url: str,
) -> Dict[str, Any]:
    """
    Generates the complete 95% AI Multi-Platform Syndication Suite from 1 YouTube video.
    Includes clones of `Shane comment GPT for LI` and `Shane comment GPT for X` visible on Slide 129.
    """
    p1 = key_points[0] if len(key_points) > 0 else "Own the distribution shelves before building products"
    p2 = key_points[1] if len(key_points) > 1 else "Target high-intent Level 4 & Level 5 buyer problems"
    p3 = key_points[2] if len(key_points) > 2 else "Bridge every viewer to an email list + Show-Up Bribe strategy call"

    linkedin_post = f"""Most people in our industry have the math completely backwards.

They think you need 1,000,000 views to build a 7-figure business.

Last week I broke down why an 8,000-view video generated $48,000—while a 4,000,000-view viral video made only $31,000 over 6 years.

{personal_story}

Here is the 3-part framework from my latest YouTube breakdown ("{video_title}"):

1. {p1}
Stop trying to sell products on someone else's counter when you don't own the store shelves.

2. {p2} (This one is my favorite)
When you solve a painful, expensive problem for a specific market, 200 views from decision-makers beats 200,000 views from bored teenagers.

3. {p3}
Every video you publish is a 6-year compounding piece of digital real estate.

I put together the complete {lead_magnet_name} that maps this out step-by-step.

Watch the full breakdown + grab the {lead_magnet_name} here: {booking_url}"""

    shane_comment_gpt_linkedin = [
        {
            "scenario": "Commenting on an Industry Peer's Viral Post (Authority Piggybacking)",
            "comment": f"Spot on. What we've seen in the trenches is that {p2.lower()} is the actual lever that moves revenue. Views without buyer intent are just vanity metrics—great breakdown."
        },
        {
            "scenario": "Replying to a Skeptical Prospect in Your Own Comments",
            "comment": f"Great question. The reason this works even with a tiny audience is that {p1.lower()}. Once you solve the exact bottleneck before the call, conversion takes care of itself. Sent you the {lead_magnet_name} link above!"
        },
        {
            "scenario": "Pinned Self-Comment Under Your LinkedIn Post (Algorithm Safe Link Drop)",
            "comment": f"P.S. If you want the exact {lead_magnet_name} we use inside our business (plus the full YouTube video on '{video_title}'), you can grab it free right here: {booking_url}"
        }
    ]

    x_thread = [
        f"1/ Most creators are playing a rigged game.\n\nThey chase millions of entertainment views making $2 per 1,000 views.\n\nMeanwhile, tiny niche authority channels are making $1,736 to $6,000 per 1,000 views.\n\nHere is the exact blueprint from '{video_title}': 🧵👇",
        f"2/ The Proof:\n\n{personal_story}\n\nYou do NOT need a massive following when you solve an expensive problem for people who already have budget.",
        f"3/ Step 1: {p1}\n\nThink like Costco. First, own the shelves (distribution). You can monetize Day 1 with other people's offers, then roll out your own 'Kirkland Signature' high-ticket offer once you see what flies off the shelf.",
        f"4/ Step 2: {p2}\n\nThis is the secret weapon.\n\nInstead of guessing what to post, use the Carl Icahn Outlier Method: find small channels with bad packaging ('drunken VHS camera') that still got massive traction—and make your version 10x better.",
        f"5/ Step 3: {p3}\n\nNever end a video with 'like and subscribe.'\n\nOpen a loop into the NEXT logical problem they'll face, and offer your {lead_magnet_name} to solve it.",
        f"6/ The 6-Year Digital Real Estate Rule:\n\nA TikTok dies in 48 hours.\n\nA search + browse YouTube video compounds for 6+ years—bringing in leads while you sleep or travel on 4 hours of work a week.",
        f"7/ Want the full deep dive + our free {lead_magnet_name}?\n\nWatch '{video_title}' and lock in your strategy session here:\n{booking_url}"
    ]

    shane_comment_gpt_x = [
        {
            "scenario": "High-Velocity Reply to a Large Creator in Your Niche (<15 mins after they tweet)",
            "reply": f"100%. And the crazy part is when you pair this with '{p2}', you only need ~200-500 targeted views per video to out-earn channels getting 1M+ views."
        },
        {
            "scenario": "Contrarian Quote-Tweet Hook",
            "reply": f"Unpopular truth: {thumbnail_text}.\n\nIf you're still chasing viral vanity views instead of '{p1}', you're working 10x harder for 1/10th the income."
        },
        {
            "scenario": "Auto-Plug Tweet When Thread Hits 25+ Likes",
            "reply": f"If you found this thread helpful, I just dropped the full video breakdown ('{video_title}') + our free {lead_magnet_name} right here: {booking_url}"
        }
    ]

    shorts_scripts = [
        {
            "short_number": 1,
            "angle": "The Contrarian Math Hook (0-60s)",
            "visual_hook_0_to_3s": f"Hold up a sheet of paper reading '{thumbnail_text}' and rip it in half at 0:01.",
            "spoken_script": (
                f"Why did an 8,000-view YouTube video make $48,000 while a 4-million-view video made only $31,000? "
                f"Because {p1.lower()}. When you target {niche_hypothesis}, you don't need millions of teenagers watching—you only need "
                f"a few hundred buyers with a painful problem. Tap the 'Related Video' link at the bottom of this Short to watch the full breakdown."
            ),
            "related_video_bridge": f"Points directly to long-form video: '{video_title}'"
        },
        {
            "short_number": 2,
            "angle": "Secret #2 Extraction (0-60s)",
            "visual_hook_0_to_3s": "Point at screen split-comparison of 'Potato Camera Outlier' vs 'Pro Studio Flop'.",
            "spoken_script": (
                f"Here is the #1 shortcut to never posting a flop again: {p2}. "
                f"Find a tiny channel where the lighting is terrible and the thumbnail is a random screenshot—yet the video still blew up. "
                f"That proves 100/100 idea demand. Make that exact topic 10% better and you win. Full tutorial linked in the Related Video below!"
            ),
            "related_video_bridge": f"Points directly to long-form video: '{video_title}'"
        },
        {
            "short_number": 3,
            "angle": "The Real-Life Receipt Story (0-60s)",
            "visual_hook_0_to_3s": "Show revenue/analytics receipt on phone or monitor in first 1.5 seconds.",
            "spoken_script": (
                f"{personal_story} And the best part? It only takes 4 hours a week once you install {p3.lower()}. "
                f"Click the Related Video right above my title to get the full step-by-step playbook and our free {lead_magnet_name}."
            ),
            "related_video_bridge": f"Points directly to long-form video: '{video_title}'"
        }
    ]

    community_tab_poll = {
        "post_timing": "Publish 24 hours BEFORE long-form video upload to pre-warm core viewer session history",
        "poll_question": f"Be honest: What is your #1 bottleneck right now when it comes to {video_title}?",
        "options": [
            f"1. Figuring out {p1[:45]}...",
            f"2. Executing {p2[:45]}...",
            f"3. Turning views into actual revenue ({p3[:35]}...)",
            "4. I haven't started yet — show me the step-by-step blueprint!"
        ],
        "pinned_comment_followup": f"Dropping a full deep-dive video tomorrow that solves whichever option wins—plus giving away our {lead_magnet_name} free: {booking_url}"
    }

    cash_code_email = {
        "subject_line_a": f"8,000 views = $48,000? ({video_title})",
        "subject_line_b": f"The '{thumbnail_text}' mistake costing you 6 figures",
        "preview_text": f"Plus how to grab the {lead_magnet_name} before tomorrow's deadline...",
        "body": f"""Hey there,

{personal_story}

Most people think you have to grind 60 hours a week and pray for the algorithm lottery to win on YouTube.

That's completely backwards.

I just published a brand-new breakdown: "{video_title}"

Inside this video, you'll discover:
- {p1}
- {p2} (Pay close attention at the 3-minute mark—this is my favorite part)
- {p3}

==> Watch "{video_title}" & Grab the Free {lead_magnet_name} Here:
{booking_url}

IMPORTANT: When you book your free strategy call on that page and show up live, we'll also unlock our internal monetization roadmap tool for your exact niche on the spot.

Talk soon,
[Your Name]"""
    }

    return {
        "video_title": video_title,
        "linkedin_authority_post": linkedin_post,
        "shane_comment_gpt_for_li": shane_comment_gpt_linkedin,
        "x_twitter_7_post_thread": x_thread,
        "shane_comment_gpt_for_x": shane_comment_gpt_x,
        "vertical_shorts_3_pack": shorts_scripts,
        "youtube_community_prewarm_poll": community_tab_poll,
        "cash_code_newsletter_email": cash_code_email,
    }


def main():
    parser = argparse.ArgumentParser(description="CGE 10x 15-Minute Voice-Interview & 95% AI Syndication Engine")
    parser.add_argument("--title", default="How to Build a $100K/Month B2B YouTube Channel With Under 1,000 Views", help="YouTube Video Title")
    parser.add_argument("--thumb-text", default="158 VIEWS = $106K", help="3-Word Thumbnail Text")
    parser.add_argument("--hypothesis", default="I help B2B consultants & agency owners land 6-figure retainers from low-view YouTube videos", help="Niche 2.0 Hypothesis")
    parser.add_argument("--story", default="One of our clients, Karla, posted once a month getting 158 views per video—and closed a $106,000/year renewable corporate placement contract.", help="Personal/Client Proof Story")
    parser.add_argument("--lead-magnet", default="Niche 2.0 Cash Code Blueprint", help="Lead Magnet Name")
    parser.add_argument("--url", default="https://yourdomain.com/coaching", help="Funnel / Booking URL")
    parser.add_argument("--output", default="", help="Optional JSON output path")
    args = parser.parse_args()

    interview_prompts = generate_voice_interview_prompts(
        title=args.title,
        niche_hypothesis=args.hypothesis,
        contrarian_belief="You DO NOT need viral views when you target Level 4 and Level 5 B2B decision-makers"
    )

    syndication = generate_95_percent_syndication_suite(
        video_title=args.title,
        thumbnail_text=args.thumb_text,
        niche_hypothesis=args.hypothesis,
        key_points=[
            "Use the Niche 2.0 Hypothesis Statement to target Level 4/5 buyers with budget",
            "Run the Revenue-Based ICAHN Method to replicate small channels printing backend cash",
            "Install the Cash Code Show-Up Bribe & Gmail Whitelist Funnel on every upload"
        ],
        personal_story=args.story,
        lead_magnet_name=args.lead_magnet,
        booking_url=args.url,
    )

    full_output = {
        "tool": "CGE 10x Voice-Interview Ghostwriter & 95% AI Syndication Engine",
        "fifteen_minute_voice_interview_protocol": interview_prompts,
        "ninety_five_percent_syndication_suite": syndication,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(full_output, f, indent=2)

    print("=" * 80)
    print("PART 1: 15-MINUTE VOICE-INTERVIEW PROTOCOL (ZACH OF ALL TRADES 800K-VIEW METHOD)")
    print("=" * 80)
    for q in interview_prompts:
        print(f"\n[{q['question_number']}]")
        print(f"  Ask Creator: {q['prompt']}")
        print(f"  Mechanism  : {q['why_shane_asks_this']}")

    print("\n" + "=" * 80)
    print("PART 2: 95% AI MULTI-PLATFORM SYNDICATION SUITE GENERATED")
    print("=" * 80)
    print(f" - LinkedIn Authority Post ({len(syndication['linkedin_authority_post'].split())} words) + 3 `Shane comment GPT for LI` replies")
    print(f" - X (Twitter) {len(syndication['x_twitter_7_post_thread'])}-Post Thread + 3 `Shane comment GPT for X` hooks")
    print(f" - {len(syndication['vertical_shorts_3_pack'])} Vertical Shorts Scripts (with Related-Video Long-Form Bridges)")
    print(" - 1 YouTube Community Pre-Warm Poll + 1 Cash Code Story Email")


if __name__ == "__main__":
    main()
