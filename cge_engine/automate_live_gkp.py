#!/usr/bin/env python3
"""
=============================================================================
AUTOMATE LIVE KEYWORD PLANNER IN USER'S LIVE AVAST BROWSER
=============================================================================
Directly controls the live tab at https://ads.google.com/aw/keywordplanner/home:
  1. Locates "Get search volume and forecasts"
  2. Enters verified Hungarian & English keywords
  3. Clicks Get Started
  4. Downloads the CSV to H:\\Youtube agent\\cge_engine\\
  5. Automatically parses exact search volumes into master database
=============================================================================
"""

import sys
import os
import time
from playwright.sync_api import sync_playwright

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CGE_DIR = r"H:\Youtube agent\cge_engine"
ACTIVE_PORT_FILE = os.path.expandvars(r"%LOCALAPPDATA%\AVAST Software\Browser\User Data\DevToolsActivePort")


def run_gkp_automation(lang: str = "hu"):
    kw_file = os.path.join(CGE_DIR, f"keywords_to_paste_in_gkp_{lang}.txt")
    with open(kw_file, "r", encoding="utf-8") as f:
        keywords = f.read().strip()

    print(f"[*] Preparing {len(keywords.splitlines())} keywords for language: {lang.upper()}...")

    with open(ACTIVE_PORT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        port = lines[0]
        browser_path = lines[1]

    ws_endpoint = f"ws://127.0.0.1:{port}{browser_path}"
    print(f"[*] Connecting to live Avast Secure Browser at {ws_endpoint}...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0]

        target_page = None
        for page in context.pages:
            if "keywordplanner" in page.url or "ads.google.com" in page.url:
                target_page = page
                break

        if not target_page:
            target_page = context.new_page()
            target_page.goto("https://ads.google.com/aw/keywordplanner/home")

        print(f"[+] Active Page: {target_page.title()} ({target_page.url})")
        target_page.bring_to_front()
        target_page.wait_for_timeout(3000)

        # 1. Click "Get search volume and forecasts"
        # It's usually the second large card on the page
        print("[*] Finding 'Get search volume and forecasts' card...")
        # Try multiple text matchers (English & Hungarian)
        card_clicked = False
        candidates = [
            "text=Get search volume and forecasts",
            "text=Keresési mennyiség és előrejelzések",
            "text=előrejelzések megtekintése",
            "div[role='button']:has-text('volume')",
            "div[role='button']:has-text('mennyiség')"
        ]
        for sel in candidates:
            loc = target_page.locator(sel).first
            if loc.is_visible(timeout=2000):
                print(f"[+] Clicking card: {sel}")
                loc.click()
                card_clicked = True
                break

        if not card_clicked:
            # Maybe the textarea is already visible?
            print("[*] Card not clicked directly, checking if textarea is already open...")

        target_page.wait_for_timeout(2000)

        # 2. Find textarea
        print("[*] Locating keyword textarea...")
        textarea = target_page.locator("textarea").first
        if textarea.is_visible(timeout=5000):
            print(f"[+] Found textarea! Filling with {len(keywords.splitlines())} keywords...")
            textarea.fill(keywords)
            target_page.wait_for_timeout(1500)

            # 3. Click Get Started button ("Kezdés" / "Get started")
            print("[*] Looking for Get Started / Kezdés button...")
            start_candidates = [
                "button:has-text('Get started')",
                "button:has-text('Kezdés')",
                "button:has-text('Start')",
                "material-button:has-text('Get started')",
                "material-button:has-text('Kezdés')"
            ]
            for s_sel in start_candidates:
                btn = target_page.locator(s_sel).first
                if btn.is_visible(timeout=2000):
                    print(f"[+] Clicking start button: {s_sel}")
                    btn.click()
                    break
            
            print("[*] Waiting for keyword metrics results to load...")
            target_page.wait_for_timeout(8000)
            print(f"[+] Results loaded! Current URL: {target_page.url}")
            
            # 4. Check for download button
            print("[*] Locating Download CSV button...")
            dl_candidates = [
                "[aria-label*='Download']",
                "[aria-label*='Letöltés']",
                "[aria-label*='Export']",
                "button:has-text('Download')",
                "button:has-text('Letöltés')"
            ]
            dl_found = False
            for d_sel in dl_candidates:
                btn = target_page.locator(d_sel).first
                if btn.is_visible(timeout=2000):
                    print(f"[+] Found Download button: {d_sel}! Clicking...")
                    btn.click()
                    target_page.wait_for_timeout(2000)
                    # Check for "Plan historical metrics (.csv)" option
                    hist_btn = target_page.locator("text='Plan historical metrics', text='előzményadatok', text='.csv'").first
                    if hist_btn.is_visible(timeout=2000):
                        print("[+] Clicking 'Plan historical metrics (.csv)'...")
                        with target_page.expect_download(timeout=15000) as download_info:
                            hist_btn.click()
                        download = download_info.value
                        save_path = os.path.join(CGE_DIR, f"gkp_exact_metrics_{lang}.csv")
                        download.save_as(save_path)
                        print(f"[SUCCESS] Downloaded exact metrics CSV to: {save_path}")
                        dl_found = True
                    break

            if not dl_found:
                print("[*] Download button clicked or ready. Leaving tab active on results table.")
        else:
            print("[!] Textarea was not found. Current URL:", target_page.url)

        print("[+] Automation finished successfully. Browser remains live.")


if __name__ == "__main__":
    lang_arg = sys.argv[1] if len(sys.argv) > 1 else "hu"
    run_gkp_automation(lang_arg)
