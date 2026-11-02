#!/usr/bin/env python3
"""
Single-shot automation inside selected Google Ads account (817881775)
"""
import os
import time
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

print(f"Connecting to live browser...")
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(ws_endpoint)
    context = browser.contexts[0]
    
    # Get active Google Ads page
    ads_page = None
    for page in context.pages:
        if 'ads.google.com' in page.url:
            ads_page = page
            break
            
    if not ads_page:
        ads_page = context.new_page()

    print(f"Navigating to Keyword Planner for active account...")
    ads_page.goto("https://ads.google.com/aw/keywordplanner/home?ocid=817881775&euid=138289646&__u=7801939454&uscid=817881775&__c=2873001975&authuser=1", timeout=60000)
    ads_page.wait_for_timeout(4000)

    print(f"Current Title: {ads_page.title()}")

    # Click 'Get search volume and forecasts'
    print("Clicking 'Get search volume and forecasts'...")
    clicked = False
    for sel in ["text='Get search volume and forecasts'", "text='Keresési mennyiség és előrejelzések'", "div[role='button']:has-text('volume')", "div[role='button']:has-text('mennyiség')"]:
        loc = ads_page.locator(sel).first
        if loc.is_visible(timeout=3000):
            loc.click()
            clicked = True
            break
            
    ads_page.wait_for_timeout(2000)

    # Locate textarea
    print("Filling keywords...")
    textarea = ads_page.locator("textarea").first
    if textarea.is_visible(timeout=5000):
        textarea.fill(keywords)
        ads_page.wait_for_timeout(1000)

        # Click Start / Kezdés
        print("Clicking Start...")
        start_btn = ads_page.locator("button:has-text('Get started'), button:has-text('Kezdés'), material-button:has-text('Get started')").first
        if start_btn.is_visible(timeout=3000):
            start_btn.click()
            ads_page.wait_for_timeout(6000)

        print(f"Results page loaded! URL: {ads_page.url}")

        # Find and click download
        print("Finding download button...")
        dl_btn = ads_page.locator("material-button.download-button, [aria-label*='Download'], [aria-label*='Letöltés'], [aria-label*='Export']").first
        if dl_btn.is_visible(timeout=5000):
            print("Clicking download icon...")
            dl_btn.click()
            ads_page.wait_for_timeout(1500)

            # Click CSV option and intercept download
            csv_opt = ads_page.locator("text='Plan historical metrics', text='előzményadatok', text='.csv'").first
            if csv_opt.is_visible(timeout=3000):
                print("Clicking CSV export...")
                save_dest = r"H:\Youtube agent\cge_engine\gkp_hu_exact.csv"
                with ads_page.expect_download(timeout=15000) as dl_info:
                    csv_opt.click()
                dl = dl_info.value
                dl.save_as(save_dest)
                print(f"[SUCCESS] Downloaded exact CSV to: {save_dest}")
    else:
        print("Textarea not visible.")

    # Save final screenshot
    final_shot = r"H:\Youtube agent\cge_engine\final_gkp_screen.png"
    ads_page.screenshot(path=final_shot)
    print(f"Final screenshot saved to: {final_shot}")
