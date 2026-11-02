#!/usr/bin/env python3
"""
=============================================================================
ALL-IN-ONE AUTONOMOUS GOOGLE ADS KEYWORD PLANNER BROWSER AGENT
=============================================================================
Runs end-to-end without asking for step-by-step approvals:
  1. Hooks into live Avast Secure Browser session on port 9222
  2. Detects current Keyword Planner state
  3. Triggers Historical Metrics CSV download
  4. Scans user Downloads folder and intercepts downloads
  5. Ingests exact Google Ads monthly search volumes, CPCs, and competition
  6. Merges exact metrics directly into master database
=============================================================================
"""

import sys
import os
import time
import glob
import csv
from playwright.sync_api import sync_playwright

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CGE_DIR = r"H:\Youtube agent\cge_engine"
ACTIVE_PORT_FILE = os.path.expandvars(r"%LOCALAPPDATA%\AVAST Software\Browser\User Data\DevToolsActivePort")
DOWNLOADS_DIR = os.path.expandvars(r"%USERPROFILE%\Downloads")
MASTER_CSV = os.path.join(CGE_DIR, "verified_keywords_master.csv")


def find_latest_downloaded_csv(since_timestamp: float) -> str:
    """Finds any CSV downloaded to Downloads folder since script started."""
    candidates = []
    # Check Downloads folder
    for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*.csv")):
        try:
            mtime = os.path.getmtime(f)
            if mtime >= since_timestamp:
                candidates.append((mtime, f))
        except Exception:
            pass
    # Check CGE dir
    for f in glob.glob(os.path.join(CGE_DIR, "*.csv")):
        try:
            mtime = os.path.getmtime(f)
            if mtime >= since_timestamp and "verified_keywords" not in f:
                candidates.append((mtime, f))
        except Exception:
            pass
            
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    return ""


def parse_and_merge_gkp_csv(csv_path: str):
    """Parses Google Keyword Planner CSV and merges into verified_keywords_master.csv."""
    print(f"\n[*] Parsing Google Keyword Planner export: {csv_path}...")
    
    encodings = ["utf-16", "utf-8", "utf-8-sig", "latin-1"]
    lines = []
    for enc in encodings:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                lines = f.readlines()
            if lines and any("Keyword" in l or "Kulcsszó" in l for l in lines[:10]):
                break
        except Exception:
            continue

    if not lines:
        print("[!] Could not decode GKP CSV.")
        return

    header_idx = -1
    for i, line in enumerate(lines[:15]):
        if "Keyword" in line or "Kulcsszó" in line:
            header_idx = i
            break

    if header_idx == -1:
        print("[!] Could not locate header in CSV.")
        return

    import io
    csv_data = "".join(lines[header_idx:])
    delimiter = "\t" if "\t" in lines[header_idx] else ","
    reader = csv.DictReader(io.StringIO(csv_data), delimiter=delimiter)

    exact_data = {}
    for row in reader:
        kw = row.get("Keyword") or row.get("Kulcsszó")
        if not kw:
            continue
        kw = kw.strip().lower()
        
        avg_searches = row.get("Avg. monthly searches") or row.get("Átlagos havi keresések") or row.get("Avg. Monthly Searches") or "N/A"
        competition = row.get("Competition") or row.get("Verseny") or "N/A"
        cpc_low = row.get("Top of page bid (low range)") or row.get("Oldaltetőre vonatkozó ajánlat (alsó tartomány)") or "N/A"
        cpc_high = row.get("Top of page bid (high range)") or row.get("Oldaltetőre vonatkozó ajánlat (felső tartomány)") or "N/A"

        exact_data[kw] = {
            "exact_searches": avg_searches,
            "competition": competition,
            "cpc_low": cpc_low,
            "cpc_high": cpc_high
        }

    print(f"[+] Loaded {len(exact_data)} exact keyword records from Google Ads!")

    # Merge into Master CSV
    if os.path.exists(MASTER_CSV):
        merged_rows = []
        with open(MASTER_CSV, "r", encoding="utf-8") as f:
            m_reader = csv.DictReader(f)
            fieldnames = list(m_reader.fieldnames)
            for col in ["Exact_Monthly_Searches", "GKP_Competition", "CPC_Low_HUF", "CPC_High_HUF"]:
                if col not in fieldnames:
                    fieldnames.append(col)

            for row in m_reader:
                kw = row["Keyword"].strip().lower()
                m = exact_data.get(kw, {})
                row["Exact_Monthly_Searches"] = m.get("exact_searches", row.get("Exact_Monthly_Searches", "N/A"))
                row["GKP_Competition"] = m.get("competition", row.get("GKP_Competition", "N/A"))
                row["CPC_Low_HUF"] = m.get("cpc_low", row.get("CPC_Low_HUF", "N/A"))
                row["CPC_High_HUF"] = m.get("cpc_high", row.get("CPC_High_HUF", "N/A"))
                merged_rows.append(row)

        with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged_rows)
        print(f"[SUCCESS] Updated master database at: {MASTER_CSV}")

    # Display Top 10 Exact Matches
    print("\n" + "=" * 75)
    print("GOOGLE ADS VERIFIED EXACT SEARCH VOLUMES & CPC BIDS")
    print("=" * 75)
    print(f"{'Keyword':<35} | {'Exact Monthly':<15} | {'CPC Range':<20}")
    print("-" * 75)
    for kw, vals in list(exact_data.items())[:15]:
        cpc_str = f"{vals['cpc_low']} - {vals['cpc_high']}"
        print(f"{kw:<35} | {vals['exact_searches']:<15} | {cpc_str:<20}")
    print("=" * 75)


def run_autonomous_agent():
    start_time = time.time()
    print("=" * 65)
    print("AUTONOMOUS BROWSER AGENT: GOOGLE ADS KEYWORD PLANNER")
    print("=" * 65)

    if not os.path.exists(ACTIVE_PORT_FILE):
        print(f"[!] Active port file not found at: {ACTIVE_PORT_FILE}")
        return

    with open(ACTIVE_PORT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        port = lines[0]
        browser_path = lines[1]

    ws_endpoint = f"ws://127.0.0.1:{port}{browser_path}"
    print(f"[*] Attaching to live browser on port {port}...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0]

        # Find Keyword Planner Page
        kp_page = None
        for page in context.pages:
            if "keywordplanner" in page.url:
                kp_page = page
                break

        if not kp_page:
            print("[*] Opening Keyword Planner tab...")
            kp_page = context.new_page()
            kp_page.goto("https://ads.google.com/aw/keywordplanner/home")
            kp_page.wait_for_timeout(5000)

        kp_page.bring_to_front()
        print(f"[+] Attached to tab: {kp_page.title()}")

        # Look for the download button on the table toolbar
        print("[*] Looking for download action...")
        
        # Click download icon (in Google Ads table header)
        download_clicked = False
        selectors = [
            "material-button.download-button",
            "material-button[aria-label*='Download']",
            "material-button[aria-label*='Letöltés']",
            "material-button[aria-label*='Export']",
            "material-icon:has-text('get_app')",
            "material-icon:has-text('file_download')",
            "[aria-label*='Download']",
            "[aria-label*='Letöltés']"
        ]

        for s in selectors:
            loc = kp_page.locator(s).first
            if loc.is_visible(timeout=1500):
                print(f"[+] Found download button: {s}! Clicking...")
                loc.click()
                download_clicked = True
                kp_page.wait_for_timeout(1500)
                break

        if download_clicked:
            # Click "Plan historical metrics (.csv)"
            csv_opt = kp_page.locator("text='Plan historical metrics', text='előzményadatok', text='.csv'").first
            if csv_opt.is_visible(timeout=3000):
                print("[+] Clicking 'Plan historical metrics (.csv)'...")
                csv_opt.click()
                print("[*] Waiting for file to download...")
                kp_page.wait_for_timeout(5000)
        else:
            print("[*] Note: Download menu might already be open or manual click available.")

        # Check if file arrived in Downloads
        time.sleep(3)
        latest_csv = find_latest_downloaded_csv(start_time - 120)
        if latest_csv:
            print(f"[+] Successfully detected downloaded CSV: {latest_csv}")
            parse_and_merge_gkp_csv(latest_csv)
        else:
            print("[*] Polling for CSV in Downloads folder for 15 seconds...")
            for _ in range(5):
                time.sleep(3)
                latest_csv = find_latest_downloaded_csv(start_time - 120)
                if latest_csv:
                    print(f"[+] Detected downloaded CSV: {latest_csv}")
                    parse_and_merge_gkp_csv(latest_csv)
                    break

        if not latest_csv:
            print("\n[!] Please click the Download icon in the top right of the table -> 'Plan historical metrics (.csv)'.")
            print("[*] The script will immediately ingest it as soon as it appears in Downloads!")
            for _ in range(10):
                time.sleep(3)
                latest_csv = find_latest_downloaded_csv(start_time - 120)
                if latest_csv:
                    print(f"[+] Detected downloaded CSV: {latest_csv}")
                    parse_and_merge_gkp_csv(latest_csv)
                    break


if __name__ == "__main__":
    run_autonomous_agent()
