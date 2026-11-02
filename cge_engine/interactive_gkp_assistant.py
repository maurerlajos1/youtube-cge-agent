#!/usr/bin/env python3
"""
=============================================================================
INTERACTIVE AVAST SECURE BROWSER ASSISTANT FOR GOOGLE KEYWORD PLANNER
=============================================================================
Launches a visible Avast window where you can sign in and allow access.
Once you log in, the assistant automatically:
  1. Detects you are in Google Ads Keyword Planner
  2. Pastes the verified keywords
  3. Gets search volume & forecasts
  4. Keeps the session persisted so you never have to log in again!
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

AVAST_EXE = r"C:\Program Files\Avast Software\Browser\Application\AvastBrowser.exe"
PROFILE_DIR = r"H:\Youtube agent\avast_automation_profile"
KEYWORDS_FILE = r"H:\Youtube agent\cge_engine\keywords_to_paste_in_gkp_hu.txt"
DOWNLOAD_DIR = r"H:\Youtube agent\cge_engine"

os.makedirs(PROFILE_DIR, exist_ok=True)


def run_interactive_assistant(target_lang: str = "hu"):
    kw_path = os.path.join(DOWNLOAD_DIR, f"keywords_to_paste_in_gkp_{target_lang}.txt")
    if not os.path.exists(kw_path):
        kw_path = KEYWORDS_FILE

    with open(kw_path, "r", encoding="utf-8") as f:
        keywords = f.read().strip()

    print("=" * 65)
    print("OPENING AVAST SECURE BROWSER FOR GOOGLE ADS AUTOMATION")
    print("=" * 65)
    print(f"[*] Target language: {target_lang.upper()}")
    print("[*] Launching visible Avast window...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            executable_path=AVAST_EXE,
            headless=False,
            accept_downloads=True,
            args=[
                "--start-maximized",
                "--remote-allow-origins=*"
            ],
            no_viewport=True
        )

        page = context.pages[0] if context.pages else context.new_page()
        
        print("[*] Navigating to Google Ads Keyword Planner...")
        page.goto("https://ads.google.com/aw/keywordplanner/home")

        print("\n" + "=" * 65)
        print(">>> ACTION REQUIRED IN THE OPEN AVAST BROWSER WINDOW <<<")
        print("1. Sign in with your Google account in the browser window.")
        print("2. Once signed in, you will be taken to Google Ads Keyword Planner.")
        print("3. The script is actively waiting to detect your login!")
        print("=" * 65 + "\n")

        # Wait loop for login
        logged_in = False
        for i in range(120):  # Wait up to 6 minutes
            current_url = page.url
            title = page.title()

            if "keywordplanner" in current_url and "accounts.google.com" not in current_url:
                logged_in = True
                print(f"\n[+] SUCCESS: Logged in! Current Page: '{title}'")
                break

            if i % 5 == 0:
                print(f"[*] Waiting for login... ({i*3}s elapsed). URL: {current_url[:60]}...")
            time.sleep(3)

        if not logged_in:
            print("[!] Timeout waiting for login. Leaving browser open so you can continue.")
            time.sleep(30)
            return

        print("[*] Waiting 5 seconds for Keyword Planner UI to stabilize...")
        page.wait_for_timeout(5000)

        # Look for "Get search volume and forecasts" card
        print("[*] Attempting to interact with Keyword Planner...")
        try:
            # Common selectors for the "Get search volume and forecasts" card
            # In Hungarian: "Keresési mennyiség és előrejelzések megtekintése"
            # In English: "Get search volume and forecasts"
            forecast_btn = page.locator("text=forecasts, text=előrejelzések, text=Keresési mennyiség").first
            if forecast_btn.is_visible(timeout=5000):
                print("[+] Clicking 'Get search volume and forecasts' card...")
                forecast_btn.click()
                page.wait_for_timeout(3000)
            
            # Look for textarea
            textarea = page.locator("textarea").first
            if textarea.is_visible(timeout=5000):
                print(f"[+] Pasting {len(keywords.splitlines())} keywords into search box...")
                textarea.fill(keywords)
                page.wait_for_timeout(1000)
                
                # Look for Start button ("Kezdés" / "Get started")
                start_btn = page.locator("button:has-text('Kezdés'), button:has-text('Get started'), button:has-text('Start')").first
                if start_btn.is_visible(timeout=3000):
                    print("[+] Clicking 'Get Started' button...")
                    start_btn.click()
                    page.wait_for_timeout(5000)
                    print("[+] Search volume and forecasts page loaded!")
            else:
                print("[*] Textbox not immediately found, please click 'Get search volume' and paste.")
        except Exception as e:
            print(f"[*] Note during UI interaction: {e}")

        print("\n[+] Browser session is ready and persisted!")
        print("[*] Leaving browser open so you can view/download exact metrics...")
        page.wait_for_timeout(30000)


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 else "hu"
    run_interactive_assistant(lang)
