#!/usr/bin/env python3
"""
=============================================================================
SINGLE-SHOT ALL-IN-ONE BROWSER AGENT
=============================================================================
Requires only ONE approval from you.
Connects once and executes the complete sequence without disconnecting:
  1. Selects 'Bpro Március'
  2. Clicks 'Get search volume and forecasts'
  3. Pastes 69 Hungarian keywords
  4. Clicks 'Get started'
  5. Clicks 'Download CSV' -> 'Plan historical metrics (.csv)'
  6. Saves exact metrics to H:\\Youtube agent\\cge_engine\\gkp_hu_exact.csv
  7. Parses and displays all exact monthly search volumes and CPC bids!
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
CSV_DEST = os.path.join(CGE_DIR, "gkp_hu_exact.csv")
MASTER_CSV = os.path.join(CGE_DIR, "verified_keywords_master.csv")


def parse_and_report_results(csv_path: str):
    print("\n" + "=" * 75)
    print("PARSING EXACT GOOGLE ADS HISTORICAL SEARCH METRICS")
    print("=" * 75)
    
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
        print("[!] Could not decode CSV file.")
        return

    header_idx = -1
    for i, line in enumerate(lines[:15]):
        if "Keyword" in line or "Kulcsszó" in line:
            header_idx = i
            break

    if header_idx == -1:
        print("[!] Could not locate table header in CSV.")
        return

    import io
    csv_data = "".join(lines[header_idx:])
    delimiter = "\t" if "\t" in lines[header_idx] else ","
    reader = csv.DictReader(io.StringIO(csv_data), delimiter=delimiter)

    exact_records = {}
    for row in reader:
        kw = row.get("Keyword") or row.get("Kulcsszó")
        if not kw:
            continue
        kw = kw.strip().lower()
        vol = row.get("Avg. monthly searches") or row.get("Átlagos havi keresések") or row.get("Avg. Monthly Searches") or "N/A"
        comp = row.get("Competition") or row.get("Verseny") or "N/A"
        cpc_low = row.get("Top of page bid (low range)") or row.get("Oldaltetőre vonatkozó ajánlat (alsó tartomány)") or "N/A"
        cpc_high = row.get("Top of page bid (high range)") or row.get("Oldaltetőre vonatkozó ajánlat (felső tartomány)") or "N/A"
        exact_records[kw] = {"vol": vol, "comp": comp, "cpc_low": cpc_low, "cpc_high": cpc_high}

    print(f"\n[SUCCESS] Successfully parsed {len(exact_records)} verified keywords from Google Ads!")
    print("-" * 75)
    print(f"{'Keyword':<35} | {'Exact Monthly':<15} | {'Top of Page Bid':<20}")
    print("-" * 75)
    for kw, data in list(exact_records.items())[:25]:
        bids = f"{data['cpc_low']} - {data['cpc_high']}"
        print(f"{kw:<35} | {data['vol']:<15} | {bids:<20}")
    print("=" * 75)

    # Merge into Master CSV
    if os.path.exists(MASTER_CSV):
        merged = []
        with open(MASTER_CSV, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            fieldnames = list(r.fieldnames)
            for col in ["Exact_Monthly_Searches", "GKP_Competition", "CPC_Low_HUF", "CPC_High_HUF"]:
                if col not in fieldnames:
                    fieldnames.append(col)
            for row in r:
                kw = row["Keyword"].strip().lower()
                m = exact_records.get(kw, {})
                row["Exact_Monthly_Searches"] = m.get("vol", row.get("Exact_Monthly_Searches", "N/A"))
                row["GKP_Competition"] = m.get("comp", row.get("GKP_Competition", "N/A"))
                row["CPC_Low_HUF"] = m.get("cpc_low", row.get("CPC_Low_HUF", "N/A"))
                row["CPC_High_HUF"] = m.get("cpc_high", row.get("CPC_High_HUF", "N/A"))
                merged.append(row)

        with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(merged)
        print(f"[+] Master intelligence database updated at: {MASTER_CSV}")


def run():
    start_time = time.time()
    print("=" * 75)
    print("EXECUTING SINGLE-SHOT BROWSER AGENT")
    print("=" * 75)

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords = f.read().strip()
    print(f"[*] Loaded {len(keywords.splitlines())} verified keywords.")

    with open(ACTIVE_PORT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        port = lines[0]
        browser_path = lines[1]

    ws_endpoint = f"ws://127.0.0.1:{port}{browser_path}"
    print(f"[*] Connecting to live Avast Secure Browser...")
    print("[*] (If Avast prompts 'Engedélyezi a távoli hibaelhárítást?', please click 'Engedélyezés' once!)")

    # Retry connection for up to 30s to allow user to click Engedélyezés if prompted
    browser = None
    with sync_playwright() as p:
        for attempt in range(10):
            try:
                browser = p.chromium.connect_over_cdp(ws_endpoint)
                print("[+] Connected to live Avast browser!")
                break
            except Exception as e:
                print(f"[*] Waiting for connection ({attempt+1}/10)... If Avast shows prompt, click 'Engedélyezés'")
                time.sleep(3)

        if not browser:
            print("[!] Could not connect to browser.")
            return

        context = browser.contexts[0]
        page = None
        for pg in context.pages:
            if "ads.google.com" in pg.url:
                page = pg
                break
        if not page:
            page = context.new_page()
            page.goto("https://ads.google.com/aw/keywordplanner/home")
            page.wait_for_timeout(4000)

        page.bring_to_front()
        print(f"[+] Active Page: {page.title()}")

        # Step 1: Select Bpro Március if modal is open
        print("[*] Step 1: Selecting 'Bpro Március' from account list...")
        selected = page.evaluate('''() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                const txt = (el.innerText || '').trim();
                if (txt.includes('Bpro Március') || txt.includes('765-355-6378')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }''')
        print(f"  -> Account selected: {selected}")
        page.wait_for_timeout(3000)

        # Step 2: Click 'Get search volume and forecasts'
        print("[*] Step 2: Clicking 'Get search volume and forecasts' card...")
        card_clicked = page.evaluate('''() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                const txt = (el.innerText || '').trim();
                if (txt === 'Get search volume and forecasts' || txt === 'Keresési mennyiség és előrejelzések megtekintése' || txt.includes('Get search volume') || txt.includes('Keresési mennyiség')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }''')
        print(f"  -> Card clicked: {card_clicked}")
        page.wait_for_timeout(2500)

        # Step 3: Fill textarea
        print("[*] Step 3: Pasting keywords into textarea...")
        filled = page.evaluate('''(kw) => {
            const ta = document.querySelector('textarea');
            if (ta) {
                ta.focus();
                ta.value = kw;
                ta.dispatchEvent(new Event('input', { bubbles: true }));
                ta.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }
            return false;
        }''', keywords)
        if not filled:
            ta = page.locator("textarea").first
            if ta.is_visible(timeout=3000):
                ta.fill(keywords)
                filled = True
        print(f"  -> Keywords pasted: {filled}")
        page.wait_for_timeout(1500)

        # Step 4: Click 'Get started'
        print("[*] Step 4: Clicking 'Get started' / 'Kezdés' button...")
        start_clicked = page.evaluate('''() => {
            const btns = document.querySelectorAll('button, material-button, [role="button"]');
            for (const b of btns) {
                const txt = (b.innerText || '').trim();
                if (txt === 'Get started' || txt === 'Kezdés' || txt === 'Start') {
                    b.click();
                    return true;
                }
            }
            return false;
        }''')
        print(f"  -> Start button clicked: {start_clicked}")
        print("[*] Step 5: Waiting 8 seconds for Google Ads metrics table to compute...")
        page.wait_for_timeout(8000)
        print(f"[+] Results loaded! URL: {page.url}")

        # Step 6: Click Download icon
        print("[*] Step 6: Triggering CSV export...")
        dl_clicked = page.evaluate('''() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                const aria = (el.getAttribute('aria-label') || '').toLowerCase();
                const title = (el.getAttribute('title') || '').toLowerCase();
                if (aria.includes('download') || aria.includes('letöltés') || aria.includes('export') || title.includes('download')) {
                    if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                        el.click();
                        return true;
                    }
                }
            }
            return false;
        }''')
        print(f"  -> Download icon clicked: {dl_clicked}")
        page.wait_for_timeout(2000)

        # Click CSV option and catch download
        csv_opt_clicked = False
        try:
            with page.expect_download(timeout=10000) as dl_info:
                page.evaluate('''() => {
                    for (const el of document.querySelectorAll('*')) {
                        const txt = (el.innerText || '').trim();
                        if (txt.includes('Plan historical metrics') || txt.includes('előzményadatok') || (txt.includes('.csv') && !txt.includes('.csv)'))) {
                            el.click();
                            return true;
                        }
                    }
                    return false;
                }''')
            dl = dl_info.value
            dl.save_as(CSV_DEST)
            print(f"[+] Download intercepted and saved to: {CSV_DEST}")
            csv_opt_clicked = True
        except Exception as e:
            print(f"[*] Note on direct download catch: {e}")

        # Fallback: scan Downloads folder
        if not os.path.exists(CSV_DEST) or os.path.getsize(CSV_DEST) == 0:
            print("[*] Scanning Downloads folder for downloaded CSV...")
            time.sleep(3)
            latest = ""
            for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*.csv")):
                try:
                    if os.path.getmtime(f) >= start_time - 30:
                        latest = f
                        break
                except Exception:
                    pass
            if latest:
                print(f"[+] Found CSV in Downloads: {latest}")
                import shutil
                shutil.copy2(latest, CSV_DEST)
                csv_opt_clicked = True

        # Step 7: Parse and display
        if os.path.exists(CSV_DEST) and os.path.getsize(CSV_DEST) > 0:
            parse_and_report_results(CSV_DEST)
        else:
            print("[*] The results table is fully loaded on your screen!")
            print("[*] Please click the Download icon in the top right of the table -> 'Plan historical metrics (.csv)'.")

        page.screenshot(path=os.path.join(CGE_DIR, "final_run_screen.png"))
        print("[+] Finished end-to-end execution!")


if __name__ == "__main__":
    run()
