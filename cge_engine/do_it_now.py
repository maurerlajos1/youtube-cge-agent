#!/usr/bin/env python3
"""
Targeted script to complete the Keyword Planner workflow right now.
"""
import os
import time
import glob
import csv
from playwright.sync_api import sync_playwright

active_port_file = os.path.expandvars(r'%LOCALAPPDATA%\AVAST Software\Browser\User Data\DevToolsActivePort')
with open(active_port_file, 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f.readlines()]
    port = lines[0]
    browser_path = lines[1]

ws_endpoint = f'ws://127.0.0.1:{port}{browser_path}'
kw_file = r'H:\Youtube agent\cge_engine\keywords_to_paste_in_gkp_hu.txt'
with open(kw_file, 'r', encoding='utf-8') as f:
    keywords = f.read().strip()

print("Attaching to live Keyword Planner tab...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(ws_endpoint)
    context = browser.contexts[0]
    page = [pg for pg in context.pages if 'ads.google.com' in pg.url][0]
    page.bring_to_front()
    print(f"Attached to page: {page.title()}")

    # Step 1: If account picker dialog is open, click 'Bpro Március'
    print("Checking for account picker...")
    account_row = page.locator("text='Bpro Március', text='765-355-6378', customer-picker-cell").first
    if account_row.is_visible(timeout=2000):
        print("Clicking 'Bpro Március' account row...")
        account_row.click()
        page.wait_for_timeout(3000)

    # Step 2: Click 'Get search volume and forecasts'
    print("Looking for 'Get search volume and forecasts' card...")
    card = page.locator("text='Get search volume and forecasts', text='Keresési mennyiség és előrejelzések'").first
    if card.is_visible(timeout=3000):
        print("Clicking 'Get search volume and forecasts' card...")
        card.click(force=True)
        page.wait_for_timeout(2000)
    else:
        # Try JS click
        page.evaluate('''() => {
            for (const el of document.querySelectorAll('*')) {
                const t = (el.innerText || '').trim();
                if (t === 'Get search volume and forecasts' || t === 'Keresési mennyiség és előrejelzések megtekintése' || t.includes('Get search volume')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }''')
        page.wait_for_timeout(2000)

    # Step 3: Fill textarea
    print("Looking for textarea...")
    textarea = page.locator("textarea").first
    if textarea.is_visible(timeout=5000):
        print(f"Filling {len(keywords.splitlines())} keywords into textarea...")
        textarea.fill(keywords)
        page.wait_for_timeout(1000)

        # Step 4: Click Get started / Kezdés
        print("Clicking Get started...")
        start_btn = page.locator("button:has-text('Get started'), button:has-text('Kezdés'), material-button:has-text('Get started')").first
        if start_btn.is_visible(timeout=3000):
            start_btn.click(force=True)
            print("Get started clicked! Waiting for results...")
            page.wait_for_timeout(7000)

        print(f"Results page loaded! URL: {page.url}")

        # Step 5: Click Download CSV
        print("Looking for download button...")
        dl_btn = page.locator("material-button.download-button, [aria-label*='Download'], [aria-label*='Letöltés'], [aria-label*='Export']").first
        if dl_btn.is_visible(timeout=5000):
            print("Clicking download icon...")
            dl_btn.click()
            page.wait_for_timeout(1500)

            # Click CSV export option
            csv_opt = page.locator("text='Plan historical metrics', text='előzményadatok', text='.csv'").first
            if csv_opt.is_visible(timeout=3000):
                print("Clicking 'Plan historical metrics (.csv)'...")
                save_path = r"H:\Youtube agent\cge_engine\gkp_hu_exact.csv"
                with page.expect_download(timeout=15000) as dl_info:
                    csv_opt.click()
                dl = dl_info.value
                dl.save_as(save_path)
                print(f"[SUCCESS] Downloaded exact CSV to: {save_path}")

    # Final screenshot
    shot_path = r"H:\Youtube agent\cge_engine\latest_gkp_action.png"
    page.screenshot(path=shot_path)
    print(f"Screenshot captured to: {shot_path}")
