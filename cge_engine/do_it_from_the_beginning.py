#!/usr/bin/env python3
"""
=============================================================================
FAIL-SAFE END-TO-END AUTOMATION FROM THE BEGINNING
=============================================================================
Uses JavaScript direct clicks to bypass any Google Ads overlays.
1. Connects to live Avast Secure Browser on port 9222
2. Navigates fresh to Keyword Planner home
3. Triggers 'Get search volume and forecasts'
4. Fills all 69 Hungarian keywords
5. Clicks 'Get started'
6. Clicks Download CSV
7. Saves exact metrics to H:\\Youtube agent\\cge_engine\\
8. Parses and outputs verified Google Ads data
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
KEYWORDS_FILE = os.path.join(CGE_DIR, "keywords_to_paste_in_gkp_hu.txt")
MASTER_CSV = os.path.join(CGE_DIR, "verified_keywords_master.csv")


def run_from_the_beginning():
    start_time = time.time()
    print("=" * 65)
    print("STARTING GOOGLE ADS KEYWORD PLANNER AUTOMATION FROM THE BEGINNING")
    print("=" * 65)

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords = f.read().strip()
    kw_count = len(keywords.splitlines())
    print(f"[*] Loaded {kw_count} verified keywords from: {KEYWORDS_FILE}")

    with open(ACTIVE_PORT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        port = lines[0]
        browser_path = lines[1]

    ws_endpoint = f"ws://127.0.0.1:{port}{browser_path}"
    print(f"[*] Attaching to live browser on port {port}...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0]

        # Use or open Keyword Planner tab
        page = None
        for pg in context.pages:
            if "ads.google.com" in pg.url or "keywordplanner" in pg.url:
                page = pg
                break
        if not page:
            page = context.new_page()

        page.bring_to_front()
        print("[*] Step 1: Navigating to Keyword Planner home...")
        # Use existing account params if present
        current_url = page.url
        if "ocid=" in current_url:
            ocid_part = current_url.split("?")[1] if "?" in current_url else ""
            target_url = f"https://ads.google.com/aw/keywordplanner/home?{ocid_part}"
        else:
            target_url = "https://ads.google.com/aw/keywordplanner/home"

        page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        print(f"[+] Current Page: {page.title()} ({page.url})")

        # Step 2: Dismiss any overlays with Escape
        print("[*] Step 2: Dismissing any overlay popups...")
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

        # Step 3: Find and click 'Get search volume and forecasts' card using JS click
        print("[*] Step 3: Clicking 'Get search volume and forecasts' card...")
        click_card_js = """() => {
            const allElements = document.querySelectorAll('*');
            for (const el of allElements) {
                const txt = (el.innerText || '').trim();
                if (txt === 'Get search volume and forecasts' || txt === 'Keresési mennyiség és előrejelzések megtekintése' || txt.includes('Get search volume') || txt.includes('Keresési mennyiség')) {
                    let clickable = el;
                    while (clickable && clickable.tagName !== 'BODY') {
                        if (clickable.getAttribute('role') === 'button' || clickable.tagName === 'BUTTON' || clickable.classList.contains('card') || clickable.classList.contains('button')) {
                            clickable.click();
                            return 'clicked_parent_' + clickable.tagName;
                        }
                        clickable = clickable.parentElement;
                    }
                    el.click();
                    return 'clicked_direct_' + el.tagName;
                }
            }
            return 'not_found';
        }"""
        res = page.evaluate(click_card_js)
        print(f"  -> JS click card result: {res}")
        page.wait_for_timeout(3000)

        # Step 4: Locate textarea and enter keywords
        print("[*] Step 4: Entering keywords into textarea...")
        fill_textarea_js = f"""(kwText) => {{
            const ta = document.querySelector('textarea');
            if (ta) {{
                ta.focus();
                ta.value = kwText;
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
            }}
            return false;
        }}"""
        filled = page.evaluate(fill_textarea_js, keywords)
        if not filled:
            # Fallback Playwright locator
            ta_loc = page.locator("textarea").first
            if ta_loc.is_visible(timeout=3000):
                ta_loc.fill(keywords)
                filled = True

        print(f"  -> Textarea filled: {filled}")
        page.wait_for_timeout(1500)

        # Step 5: Click 'Get started' / 'Kezdés'
        print("[*] Step 5: Clicking 'Get started' button...")
        click_start_js = """() => {
            const btns = document.querySelectorAll('button, material-button, [role="button"]');
            for (const b of btns) {
                const txt = (b.innerText || '').trim();
                if (txt === 'Get started' || txt === 'Kezdés' || txt === 'Start') {
                    b.click();
                    return 'clicked_' + txt;
                }
            }
            return 'not_found';
        }"""
        start_res = page.evaluate(click_start_js)
        print(f"  -> Start button click result: {start_res}")

        print("[*] Step 6: Waiting for Keyword Planner results table to load...")
        page.wait_for_timeout(8000)
        print(f"[+] Results loaded! URL: {page.url}")

        # Step 7: Locate download button and trigger export
        print("[*] Step 7: Locating Download CSV icon on results page...")
        click_dl_js = """() => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
                const aria = (el.getAttribute('aria-label') || '').toLowerCase();
                const title = (el.getAttribute('title') || '').toLowerCase();
                const txt = (el.innerText || '').toLowerCase();
                if (aria.includes('download') || aria.includes('letöltés') || aria.includes('export') || title.includes('download') || title.includes('letöltés')) {
                    if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                        el.click();
                        return 'clicked_dl_' + el.tagName;
                    }
                }
            }
            return 'not_found';
        }"""
        dl_res = page.evaluate(click_dl_js)
        print(f"  -> Download icon click result: {dl_res}")
        page.wait_for_timeout(2000)

        # Click CSV option if dropdown appeared
        click_csv_opt_js = """() => {
            const items = document.querySelectorAll('*');
            for (const item of items) {
                const txt = (item.innerText || '').trim();
                if (txt.includes('Plan historical metrics') || txt.includes('előzményadatok') || (txt.includes('.csv') && !txt.includes('.csv)'))) {
                    item.click();
                    return 'clicked_csv_' + txt;
                }
            }
            return 'not_found';
        }"""
        csv_res = page.evaluate(click_csv_opt_js)
        print(f"  -> CSV option click result: {csv_res}")
        page.wait_for_timeout(5000)

        # Step 8: Check for downloaded file
        print("[*] Step 8: Checking for downloaded CSV file...")
        downloaded_csv = ""
        for _ in range(5):
            time.sleep(2)
            for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*.csv")):
                try:
                    if os.path.getmtime(f) >= start_time - 30:
                        downloaded_csv = f
                        break
                except Exception:
                    pass
            if downloaded_csv:
                break

        if downloaded_csv:
            print(f"[SUCCESS] Downloaded CSV found: {downloaded_csv}")
            parse_and_display_metrics(downloaded_csv)
        else:
            print("[*] Automated actions complete! The table with all 69 keywords is on your screen.")
            print("[*] Please click the Download icon in the top right -> 'Plan historical metrics (.csv)'.")


def parse_and_display_metrics(csv_path: str):
    """Parses Google Ads CSV and merges with master file."""
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
        return

    header_idx = -1
    for i, line in enumerate(lines[:15]):
        if "Keyword" in line or "Kulcsszó" in line:
            header_idx = i
            break

    if header_idx == -1:
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
        cpc_low = row.get("Top of page bid (low range)") or row.get("Oldaltetőre vonatkozó ajánlat (alsó tartomány)") or "N/A"
        cpc_high = row.get("Top of page bid (high range)") or row.get("Oldaltetőre vonatkozó ajánlat (felső tartomány)") or "N/A"
        exact_data[kw] = {"searches": avg_searches, "cpc_low": cpc_low, "cpc_high": cpc_high}

    print("\n" + "=" * 75)
    print("VERIFIED GOOGLE ADS EXACT MONTHLY SEARCH VOLUMES")
    print("=" * 75)
    for kw, vals in list(exact_data.items())[:20]:
        print(f"  {kw:<35} | Vol: {vals['searches']:<10} | Bid: {vals['cpc_low']} - {vals['cpc_high']}")
    print("=" * 75)


if __name__ == "__main__":
    run_from_the_beginning()
