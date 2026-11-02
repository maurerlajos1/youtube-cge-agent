#!/usr/bin/env python3
"""
CGE 10x — Live YouTube Search, Deep Analytics & Verbatim Transcript Extractor
=============================================================================
Supports Multi-Market / Multi-Language Intelligence (English `en-US` + Hungarian `hu-HU`):
  1. Mines YouTube Autocomplete Wildcards (`* keyword`) per language/country (`hl` & `gl`).
  2. Searches YouTube & uses `yt_dlp` to pull REAL video/channel analytics:
       - Exact View Count (`view_count`)
       - Exact Channel Subscriber Count (`channel_follower_count`)
       - True Carl Icahn View-to-Subscriber Ratio (`view_count / channel_follower_count`)
       - Views-Per-Day Velocity (from `upload_date`)
       - Exact Likes (`like_count`), Comments (`comment_count`), Engagement Rate
       - Full Description + Extracted External Funnel/Lead-Magnet URLs
  3. Extracts Full Verbatim Transcripts (manual subtitles or auto-captions in `en` / `hu`)
     and audits the First 30 Seconds (0:00 - 0:30 Holy Trifecta Intro) + Mid-Roll CTAs!
"""

import argparse
import datetime
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from typing import List, Dict, Any, Optional
import yt_dlp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SSL_CTX = ssl._create_unverified_context()

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def fetch_autocomplete_wildcards(keyword: str, hl: str = "en", gl: str = "US") -> List[str]:
    """
    Runs Shane's `* keyword` autocomplete wildcard trick (Slide 97, 01:21:55)
    localized for language `hl` (e.g., 'en' or 'hu') and country `gl` ('US' or 'HU').
    """
    queries = [f"* {keyword}", f"{keyword} *", f"how to {keyword}" if hl == "en" else f"{keyword} tippek"]
    suggestions = []
    for q in queries:
        encoded = urllib.parse.quote_plus(q)
        url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl={hl}&gl={gl}&q={encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=8, context=SSL_CTX) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            match = re.search(r"window\.google\.ac\.h\((.*)\)", raw)
            if match:
                payload = json.loads(match.group(1))
                for item in payload[1]:
                    s = item[0]
                    if s not in suggestions:
                        suggestions.append(s)
        except Exception:
            pass
    return suggestions[:15]


def search_youtube_video_ids(query: str, hl: str = "en", gl: str = "US", limit: int = 6) -> List[str]:
    """
    Searches YouTube with localized `hl` and `gl` parameters and returns top video IDs.
    """
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded}&hl={hl}&gl={gl}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": f"{hl}-{gl},{hl};q=0.9"},
    )
    video_ids = []
    try:
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        for m in re.finditer(r'"videoRenderer":\{"videoId":"([a-zA-Z0-9_-]{11})"', html):
            vid = m.group(1)
            if vid not in video_ids:
                video_ids.append(vid)
            if len(video_ids) >= limit:
                break
    except Exception:
        pass
    return video_ids


def extract_transcript_from_info(info: Dict[str, Any], preferred_langs: List[str]) -> Dict[str, Any]:
    """
    Downloads and parses the `json3` caption track from `yt_dlp` info dict.
    Returns both the first 30 seconds (Holy Trifecta Intro) and the full transcript text.
    """
    subtitles = info.get("subtitles") or {}
    auto_captions = info.get("automatic_captions") or {}

    track_url = None
    selected_lang = None
    is_auto = False

    # Try manual subtitles first, then automatic captions
    for lang in preferred_langs + ["en", "en-US", "hu"]:
        if lang in subtitles:
            for fmt in subtitles[lang]:
                if fmt.get("ext") == "json3":
                    track_url = fmt.get("url")
                    selected_lang = lang
                    is_auto = False
                    break
        if track_url:
            break

    if not track_url:
        for lang in preferred_langs + ["en", "en-US", "hu"]:
            if lang in auto_captions:
                for fmt in auto_captions[lang]:
                    if fmt.get("ext") == "json3":
                        track_url = fmt.get("url")
                        selected_lang = lang
                        is_auto = True
                        break
            if track_url:
                break

    if not track_url:
        return {"available": False, "reason": "No caption track found"}

    try:
        req = urllib.request.Request(track_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            sub_data = json.loads(resp.read().decode("utf-8", errors="ignore"))

        events = sub_data.get("events", [])
        segments = []
        intro_30s_words = []
        full_words = []

        for ev in events:
            segs = ev.get("segs")
            if not segs:
                continue
            start_ms = ev.get("tStartMs", 0)
            start_sec = round(start_ms / 1000.0, 1)
            text = "".join(s.get("utf8", "") for s in segs).replace("\n", " ").strip()
            if not text:
                continue
            segments.append({"t": start_sec, "text": text})
            full_words.append(text)
            if start_sec <= 32.0:
                intro_30s_words.append(text)

        full_text = re.sub(r"\s+", " ", " ".join(full_words)).strip()
        intro_30s_text = re.sub(r"\s+", " ", " ".join(intro_30s_words)).strip()

        return {
            "available": True,
            "language": selected_lang,
            "is_auto_generated": is_auto,
            "total_word_count": len(full_text.split()),
            "first_30_seconds_hook": intro_30s_text,
            "first_30s_word_count": len(intro_30s_text.split()),
            "full_transcript_preview_1500_chars": full_text[:1500],
            "full_transcript": full_text,
            "timestamped_segments_sample": segments[:25],
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}


def analyze_video_deep(video_id: str, preferred_langs: List[str], pull_transcript: bool = True) -> Optional[Dict[str, Any]]:
    """
    Uses `yt_dlp` to pull exact analytics + optional full transcript for a single video ID.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
        "nocheckcertificate": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:
        return {"video_id": video_id, "error": str(exc)}

    views = info.get("view_count") or 0
    subs = info.get("channel_follower_count") or 0
    likes = info.get("like_count") or 0
    comments = info.get("comment_count") or 0
    duration_sec = info.get("duration") or 0
    upload_date_str = info.get("upload_date") or ""
    description = info.get("description") or ""
    title = info.get("title") or ""
    channel = info.get("uploader") or info.get("channel") or ""

    # Compute age in days and views/day velocity
    days_old = 365
    if len(upload_date_str) == 8:
        try:
            dt = datetime.datetime.strptime(upload_date_str, "%Y%m%d").date()
            days_old = max(1, (datetime.date.today() - dt).days)
        except Exception:
            pass
    views_per_day = round(views / float(days_old), 1)

    # True Carl Icahn Outlier Ratio = Views / Subscribers
    true_icahn_ratio = round(views / float(max(subs, 100)), 2) if subs else round(views / 1000.0, 2)
    like_rate_pct = round((likes / float(max(views, 1))) * 100.0, 2)

    # Extract external funnel / lead-magnet URLs from description
    urls_in_desc = re.findall(r"https?://[^\s)\]>\"']+", description)
    external_funnel_links = [
        u for u in urls_in_desc
        if not any(plat in u.lower() for plat in ["youtube.com", "youtu.be", "facebook.com", "instagram.com", "twitter.com", "tiktok.com"])
    ]

    result = {
        "video_id": video_id,
        "url": url,
        "title": title,
        "channel": channel,
        "subscribers": subs,
        "views": views,
        "true_icahn_views_to_subs_ratio": true_icahn_ratio,
        "is_icahn_outlier": bool(true_icahn_ratio >= 1.5 or (subs < 25000 and views > 15000)),
        "is_karla_singson_b2b_candidate": bool(len(external_funnel_links) > 0 and subs < 30000),
        "likes": likes,
        "like_to_view_rate_pct": like_rate_pct,
        "comments": comments,
        "duration_minutes": round(duration_sec / 60.0, 1),
        "upload_date": upload_date_str,
        "days_since_upload": days_old,
        "views_per_day_velocity": views_per_day,
        "external_funnel_links": external_funnel_links[:6],
        "description_first_300_chars": description[:300].replace("\n", " "),
        "tags": (info.get("tags") or [])[:12],
    }

    if pull_transcript:
        result["transcript_data"] = extract_transcript_from_info(info, preferred_langs)

    return result


def run_market_scan(
    market_label: str,
    queries: List[str],
    hl: str,
    gl: str,
    preferred_langs: List[str],
    videos_per_query: int = 3,
    transcripts_to_pull: int = 3,
) -> Dict[str, Any]:
    """
    Runs a complete market scan (Wildcard Autocomplete + Video Analytics + Verbatim Transcripts).
    """
    wildcards = {}
    all_video_ids = []
    for q in queries:
        wildcards[q] = fetch_autocomplete_wildcards(q, hl=hl, gl=gl)
        vids = search_youtube_video_ids(q, hl=hl, gl=gl, limit=videos_per_query)
        for v in vids:
            if v not in all_video_ids:
                all_video_ids.append(v)

    analyzed_videos = []
    transcripts_pulled = 0
    for vid in all_video_ids:
        want_tx = transcripts_pulled < transcripts_to_pull
        data = analyze_video_deep(vid, preferred_langs=preferred_langs, pull_transcript=want_tx)
        if data:
            if want_tx and data.get("transcript_data", {}).get("available"):
                transcripts_pulled += 1
            analyzed_videos.append(data)

    # Sort by True ICAHN Views-to-Subscribers ratio descending
    analyzed_videos.sort(key=lambda x: x.get("true_icahn_views_to_subs_ratio", 0), reverse=True)

    return {
        "market_label": market_label,
        "hl": hl,
        "gl": gl,
        "autocomplete_wildcard_ideas": wildcards,
        "analyzed_videos": analyzed_videos,
    }


def main():
    parser = argparse.ArgumentParser(description="CGE 10x Live YouTube Search, Analytics & Transcript Extractor")
    parser.add_argument(
        "--output",
        default=r"H:\Youtube agent\cge_engine\google_ads_cro_en_hu_intel.json",
        help="Output JSON file path",
    )
    args = parser.parse_args()

    print("Scanning Market 1: ENGLISH (en-US) — Google Ads & CRO...")
    en_report = run_market_scan(
        market_label="English Market (US/UK/Global) — Google Ads & CRO",
        queries=["google ads tutorial", "conversion rate optimization landing page"],
        hl="en",
        gl="US",
        preferred_langs=["en", "en-US"],
        videos_per_query=3,
        transcripts_to_pull=3,
    )

    print("Scanning Market 2: HUNGARIAN (hu-HU) — Google Ads & CRO (Konverzió Optimalizálás)...")
    hu_report = run_market_scan(
        market_label="Hungarian Market (Magyarország) — Google Ads & Konverzió Optimalizálás (CRO)",
        queries=["google ads hirdetés", "konverzió optimalizálás landing oldal"],
        hl="hu",
        gl="HU",
        preferred_langs=["hu", "en"],
        videos_per_query=3,
        transcripts_to_pull=3,
    )

    master_intel = {
        "generated_at": datetime.datetime.now().isoformat(),
        "niche": "Google Ads & Conversion Rate Optimization (CRO)",
        "english_market": en_report,
        "hungarian_market": hu_report,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(master_intel, f, indent=2, ensure_ascii=False)

    for mkt in [en_report, hu_report]:
        print("\n" + "=" * 90)
        print(f"MARKET REPORT: {mkt['market_label']}")
        print("=" * 90)
        for q, suggestions in mkt["autocomplete_wildcard_ideas"].items():
            print(f"  [* Wildcard Autocomplete for '{q}']: {', '.join(suggestions[:8])}")
        print("\n  [LIVE YOUTUBE ANALYTICS & ICAHN OUTLIER RANKING]:")
        for idx, v in enumerate(mkt["analyzed_videos"], 1):
            if "error" in v:
                continue
            tx = v.get("transcript_data", {})
            tx_status = (
                f"YES ({tx.get('language')}, {tx.get('total_word_count')} words | 30s Hook: {tx.get('first_30s_word_count')} words)"
                if tx.get("available")
                else "Not pulled / unavailable"
            )
            print(
                f"  {idx}. {v['title']}\n"
                f"     Channel: {v['channel']} ({v['subscribers']:,} subs) | Views: {v['views']:,} "
                f"| True ICAHN Ratio: {v['true_icahn_views_to_subs_ratio']}x subs\n"
                f"     Likes: {v['likes']:,} ({v['like_to_view_rate_pct']}%) | Comments: {v['comments']:,} "
                f"| Velocity: {v['views_per_day_velocity']}/day | Duration: {v['duration_minutes']}m\n"
                f"     Funnel Links in Desc: {v['external_funnel_links'][:3]}\n"
                f"     Transcript Extracted: {tx_status}"
            )
            if tx.get("available"):
                print(f"     -> First 30s Spoken Intro: \"{tx.get('first_30_seconds_hook', '')[:220]}...\"")


if __name__ == "__main__":
    main()
