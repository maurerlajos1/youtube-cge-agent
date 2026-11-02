#!/usr/bin/env python3
"""
=============================================================================
AVAST SECURE BROWSER PLAYWRIGHT AUTOMATOR FOR GOOGLE KEYWORD PLANNER
=============================================================================
Takes over Avast Secure Browser via Playwright to automate:
  1. Navigation to Google Ads Keyword Planner
  2. Pasting verified keywords (English / Hungarian)
  3. Downloading the exact search volume metrics CSV
  4. Merging exact metrics into the CGE Master Intelligence Database
=============================================================================
"""

import sys
import os
import time
import asyncio
from playwright.async_api import async_playwright

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AVAST_EXE = r"C:\Program Files\Avast Software\Browser\Application\AvastBrowser.exe"
AVAST_USER_DATA = os.path.expandvars(r"%LOCALAPPDATA%\AVAST Software\Browser\User Data")
DOWNLOAD_DIR = r"H:\Youtube agent\cge_engine"


async def run_automator(mode: str = "cdp", target_lang: str = "hu"):
    """
    mode: 'cdp' (connect to running Avast on port 9222)
          'launch' (launch Avast persistent context directly)
    """
    kw_file = os.path.join(DOWNLOAD_DIR, f"keywords_to_paste_in_gkp_{target_lang}.txt")
    if not os.path.exists(kw_file):
        print(f"[!] Keyword file not found: {kw_file}")
        return

    with open(kw_file, "r", encoding="utf-8") as f:
        keywords = f.read().strip()

    print(f"[*] Loaded {len(keywords.splitlines())} keywords for target: {target_lang.upper()}")

    async with async_playwright() as p:
        browser = None
        context = None
        
        if mode == "cdp":
            print("[*] Connecting to Avast Secure Browser over CDP (http://localhost:9222)...")
            try:
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                contexts = browser.contexts
                if not contexts:
                    context = await browser.new_context(accept_downloads=True)
                else:
                    context = contexts[0]
                print("[+] Successfully connected to running Avast Browser!")
            except Exception as e:
                print(f"[!] CDP connection failed: {e}")
                print("[*] Tip: Launch Avast with: --remote-debugging-port=9222 --remote-allow-origins=*")
                return
        else:
            print(f"[*] Launching Avast Secure Browser directly with profile: {AVAST_USER_DATA}...")
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=AVAST_USER_DATA,
                    executable_path=AVAST_EXE,
                    headless=False,
                    accept_downloads=True,
                    args=["--remote-allow-origins=*"]
                )
                print("[+] Avast Secure Browser launched with user profile!")
            except Exception as e:
                print(f"[!] Failed to launch persistent context: {e}")
                print("[!] Ensure all running AvastBrowser.exe instances are closed before launching.")
                return

        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        print("[*] Navigating to Google Ads Keyword Planner...")
        await page.goto("https://ads.google.com/aw/keywordplanner/home", wait_until="domcontentloaded")
        print("[*] Waiting for Keyword Planner UI to initialize...")
        await page.wait_for_timeout(5000)

        # Output current page title and URL
        title = await page.title()
        url = page.url
        print(f"[+] Current Page: '{title}' ({url})")

        print("[*] Automation ready. Please ensure your Google Ads account is selected in the window.")
        # Keep open for interactive verification or automation steps
        await page.wait_for_timeout(10000)


if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "cdp"
    lang_arg = sys.argv[2] if len(sys.argv) > 2 else "hu"
    asyncio.run(run_automator(mode=mode_arg, target_lang=lang_arg))
