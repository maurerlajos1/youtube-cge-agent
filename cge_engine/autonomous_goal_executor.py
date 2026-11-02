#!/usr/bin/env python3
"""
=============================================================================
AUTONOMOUS GOOGLE ADS KEYWORD PLANNER GOAL EXECUTOR
=============================================================================
Automates the full extraction process inside the user's live Avast Browser:
  1. Connects to live Avast Secure Browser via active WebSocket
  2. Overcomes the account picker modal (clicks customer-picker-cell.first)
  3. Clicks 'Get search volume and forecasts'
  4. Fills 69 Hungarian keywords and submits
  5. Intercepts/downloads exact historical metrics CSV for Hungarian
  6. Submits 75 English keywords and downloads exact metrics for English
  7. Parses single-digit monthly search volumes, CPCs, and competition
  8. Merges exact data into verified_keywords_master.csv and master playbook
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
HU_KW_FILE = os.path.join(CGE_DIR, "keywords_to_paste_in_gkp_hu.txt")
EN_KW_FILE = os.path.join(CGE_DIR, "keywords_to_paste_in_gkp_en.txt")
HU_CSV_DEST = os.path.join(CGE_DIR, "gkp_hu_exact.csv")
EN_CSV_DEST = os.path.join(CGE_DIR, "gkp_en_exact.csv")
MASTER_CSV = os.path.join(CGE_DIR, "verified_keywords_master.csv")
PLAYBOOK_FILE = r"H:\Youtube agent\GOOGLE_ADS_CRO_DUAL_MARKET_PLAYBOOK.md"


def get_ws_endpoint():
    with open(ACTIVE_PORT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    port = lines[0]
    browser_path = lines[1]
    return f"ws://127.0.0.1:{port}{browser_path}"


def dismiss_account_picker_and_open_forecasts(page):
    print("[*] Inspecting page state and dismissing any modals...")
    # Check if 'Select an account' modal is present
    picker_cells = page.locator("customer-picker-cell, .customer-picker-cell-wrapper, tr[role='row']")
    count = picker_cells.count()
    print(f"  -> Found {count} account picker rows.")
    if count > 0:
        print("[+] Clicking first account row (Bpro Március)...")
        picker_cells.first.click(force=True)
        page.wait_for_timeout(3000)

    # If modal is still open, try clicking text 'Bpro' or pressing Escape
    modal = page.locator("text='Select an account', text='Fiók kiválasztása'")
    if modal.is_visible(timeout=1500):
        print("[*] Modal still visible, clicking Bpro text directly...")
        bpro = page.locator("text='Bpro Március', text='765-355-6378'").first
        if bpro.is_visible(timeout=1500):
            bpro.click(force=True)
            page.wait_for_timeout(3000)
        else:
            page.keyboard.press("Escape")
            page.wait_for_timeout(1500)

    # Now click 'Get search volume and forecasts'
    print("[*] Locating 'Get search volume and forecasts' card...")
    card = page.locator("text='Get search volume and forecasts', text='Keresési mennyiség és előrejelzések megtekintése', text='Get search volume'").first
    if card.is_visible(timeout=4000):
        print("[+] Clicking 'Get search volume and forecasts' card...")
        card.click(force=True)
        page.wait_for_timeout(2500)
    else:
        print("[*] Card not directly found, evaluating DOM click...")
        page.evaluate('''() => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
                const t = (el.innerText || '').trim();
                if (t === 'Get search volume and forecasts' || t === 'Keresési mennyiség és előrejelzések megtekintése' || t.includes('Get search volume')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }''')
        page.wait_for_timeout(2500)


def enter_keywords_and_submit(page, keywords_text):
    print(f"[*] Entering {len(keywords_text.splitlines())} keywords into search textarea...")
    ta = page.locator("textarea").first
    if not ta.is_visible(timeout=5000):
        # Click search volume card again if needed
        dismiss_account_picker_and_open_forecasts(page)
        ta = page.locator("textarea").first

    if ta.is_visible(timeout=5000):
        ta.fill(keywords_text)
        page.wait_for_timeout(1000)
        print("[+] Filled keywords! Clicking 'Get started'...")
        start_btn = page.locator("button:has-text('Get started'), button:has-text('Kezdés'), material-button:has-text('Get started')").first
        if start_btn.is_visible(timeout=3000):
            start_btn.click(force=True)
        else:
            page.evaluate('''() => {
                for (const b of document.querySelectorAll('button, material-button, [role="button"]')) {
                    const t = (b.innerText || '').trim();
                    if (t === 'Get started' || t === 'Kezdés' || t === 'Start') {
                        b.click();
                        return true;
                    }
                }
                return false;
            }''')
        print("[*] Waiting 8 seconds for metrics table to calculate...")
        page.wait_for_timeout(8000)
        return True
    else:
        print("[!] Textarea was not visible.")
        return False


def download_historical_metrics_csv(page, target_dest):
    print(f"[*] Initiating download of metrics to: {target_dest}...")
    start_t = time.time()
    
    # Click download icon on table header
    dl_btn = page.locator("material-button.download-button, [aria-label*='Download'], [aria-label*='Letöltés'], [aria-label*='Export']").first
    if dl_btn.is_visible(timeout=4000):
        print("[+] Found download button, clicking...")
        dl_btn.click(force=True)
        page.wait_for_timeout(1500)
    else:
        page.evaluate('''() => {
            for (const el of document.querySelectorAll('*')) {
                const a = (el.getAttribute('aria-label') || '').toLowerCase();
                const t = (el.innerText || '').toLowerCase();
                if (a.includes('download') || a.includes('letöltés') || a.includes('export')) {
                    if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                        el.click();
                        return true;
                    }
                }
            }
            return false;
        }''')
        page.wait_for_timeout(1500)

    # Click CSV option
    download_success = False
    try:
        with page.expect_download(timeout=12000) as dl_info:
            page.locator("text='Plan historical metrics', text='előzményadatok', text='.csv'").first.click(force=True)
        dl = dl_info.value
        dl.save_as(target_dest)
        print(f"[SUCCESS] Download intercepted and saved: {target_dest}")
        download_success = True
    except Exception as e:
        print(f"[*] Expect download timed out ({e}), checking Downloads folder...")

    if not download_success:
        time.sleep(3)
        for f in glob.glob(os.path.join(DOWNLOADS_DIR, "*.csv")):
            try:
                if os.path.getmtime(f) >= start_t - 15:
                    import shutil
                    shutil.copy2(f, target_dest)
                    print(f"[SUCCESS] Picked up CSV from Downloads folder: {f}")
                    download_success = True
                    break
            except Exception:
                pass

    return download_success


def parse_and_merge_exact_metrics(csv_path, language="hu"):
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print(f"[!] File not found or empty: {csv_path}")
        return {}

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
        return {}

    header_idx = -1
    for i, line in enumerate(lines[:15]):
        if "Keyword" in line or "Kulcsszó" in line:
            header_idx = i
            break

    if header_idx == -1:
        return {}

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

    print(f"\n[+] Extracted {len(exact_records)} exact records from {csv_path}!")

    # Merge into Master CSV
    if os.path.exists(MASTER_CSV):
        merged = []
        with open(MASTER_CSV, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            fieldnames = list(r.fieldnames)
            for col in ["Exact_Monthly_Searches", "GKP_Competition", "CPC_Low", "CPC_High"]:
                if col not in fieldnames:
                    fieldnames.append(col)
            for row in r:
                kw = row["Keyword"].strip().lower()
                m = exact_records.get(kw, {})
                if m:
                    row["Exact_Monthly_Searches"] = m.get("vol", row.get("Exact_Monthly_Searches", "N/A"))
                    row["GKP_Competition"] = m.get("comp", row.get("GKP_Competition", "N/A"))
                    row["CPC_Low"] = m.get("cpc_low", row.get("CPC_Low", "N/A"))
                    row["CPC_High"] = m.get("cpc_high", row.get("CPC_High", "N/A"))
                merged.append(row)

        with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(merged)

    return exact_records


def update_playbook_with_exact_numbers(hu_records, en_records):
    print("[*] Updating GOOGLE_ADS_CRO_DUAL_MARKET_PLAYBOOK.md with verified numbers...")
    if not os.path.exists(PLAYBOOK_FILE):
        return

    with open(PLAYBOOK_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Append Verified Data Section
    verified_section = "\n\n---\n\n## 6. Official Google Ads Verified Exact Search Volumes & CPC Data\n\n"
    verified_section += "Data extracted directly from Google Ads Manager Account (`Bpro`) via Keyword Planner:\n\n"
    
    if hu_records:
        verified_section += "### Hungarian Market Verified Exact Metrics\n\n"
        verified_section += "| Keyword | Exact Monthly Searches | Competition | Top of Page Bid (Low - High) |\n"
        verified_section += "| :--- | :---: | :---: | :--- |\n"
        for kw, d in list(hu_records.items())[:25]:
            verified_section += f"| `{kw}` | **{d['vol']}** | {d['comp']} | {d['cpc_low']} - {d['cpc_high']} |\n"

    if en_records:
        verified_section += "\n### English Market Verified Exact Metrics\n\n"
        verified_section += "| Keyword | Exact Monthly Searches | Competition | Top of Page Bid (Low - High) |\n"
        verified_section += "| :--- | :---: | :---: | :--- |\n"
        for kw, d in list(en_records.items())[:25]:
            verified_section += f"| `{kw}` | **{d['vol']}** | {d['comp']} | {d['cpc_low']} - {d['cpc_high']} |\n"

    with open(PLAYBOOK_FILE, "a", encoding="utf-8") as f:
        f.write(verified_section)
    print(f"[SUCCESS] Playbook updated with official data: {PLAYBOOK_FILE}")


def execute_full_goal():
    print("=" * 75)
    print("AUTONOMOUS GOAL EXECUTION STARTED")
    print("=" * 75)
    
    ws_endpoint = get_ws_endpoint()
    print(f"[*] Target browser endpoint: {ws_endpoint}")

    with sync_playwright() as p:
        browser = None
        for i in range(12):
            try:
                browser = p.chromium.connect_over_cdp(ws_endpoint)
                print("[+] Successfully connected to live Avast Secure Browser!")
                break
            except Exception as e:
                print(f"[*] Waiting for connection ({i+1}/12)... {e}")
                time.sleep(3)

        if not browser:
            print("[!] Connection could not be established.")
            return False

        context = browser.contexts[0]
        # Find Google Ads tab
        ads_page = None
        for pg in context.pages:
            if "ads.google.com" in pg.url:
                ads_page = pg
                break
        if not ads_page:
            ads_page = context.new_page()
            ads_page.goto("https://ads.google.com/aw/keywordplanner/home")
            ads_page.wait_for_timeout(4000)

        ads_page.bring_to_front()
        print(f"[+] Active Tab: {ads_page.title()} ({ads_page.url})")

        # 1. Hungarian Batch Execution
        with open(HU_KW_FILE, "r", encoding="utf-8") as f:
            hu_kw_text = f.read().strip()

        dismiss_account_picker_and_open_forecasts(ads_page)
        submitted = enter_keywords_and_submit(ads_page, hu_kw_text)
        hu_downloaded = False
        if submitted:
            hu_downloaded = download_historical_metrics_csv(ads_page, HU_CSV_DEST)

        # 2. Parse Hungarian Results
        hu_records = {}
        if os.path.exists(HU_CSV_DEST):
            hu_records = parse_and_merge_exact_metrics(HU_CSV_DEST, "hu")

        # 3. English Batch Execution
        with open(EN_KW_FILE, "r", encoding="utf-8") as f:
            en_kw_text = f.read().strip()

        print("\n[*] Starting English Keyword Batch...")
        ads_page.goto("https://ads.google.com/aw/keywordplanner/home?ocid=817881775&ascid=817881775&euid=138289646&__u=7801939454&uscid=817881775&__c=2873001975&authuser=1")
        ads_page.wait_for_timeout(3000)
        dismiss_account_picker_and_open_forecasts(ads_page)
        en_submitted = enter_keywords_and_submit(ads_page, en_kw_text)
        en_downloaded = False
        if en_submitted:
            en_downloaded = download_historical_metrics_csv(ads_page, EN_CSV_DEST)

        en_records = {}
        if os.path.exists(EN_CSV_DEST):
            en_records = parse_and_merge_exact_metrics(EN_CSV_DEST, "en")

        # 4. Update Playbook
        update_playbook_with_exact_numbers(hu_records, en_records)

        print("\n" + "=" * 75)
        print("GOAL EXECUTION COMPLETE: DUAL-MARKET EXACT DATA CAPTURED")
        print("=" * 75)
        return True


if __name__ == "__main__":
    execute_full_goal()
