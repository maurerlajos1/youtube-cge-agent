#!/usr/bin/env python3
"""
=============================================================================
GOOGLE KEYWORD PLANNER SYNC & EXACT VOLUME INTEGRATION MODULE
=============================================================================
Supports two workflows:
  Workflow A (Instant, 0 setup):
    1. Generates clean keyword lists for Google Keyword Planner copy-paste.
    2. Automatically parses Google Keyword Planner CSV exports and merges
       exact monthly search volumes, CPCs, and competition metrics.
  Workflow B (Programmatic API):
    Uses official `google-ads` Python SDK with `google-ads.yaml` credentials.
=============================================================================
"""

import sys
import os
import csv
import json
from typing import List, Dict, Any, Optional

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def export_keywords_for_keyword_planner(master_csv_path: str, output_dir: str):
    """
    Reads verified_keywords_master.csv and exports plain text files
    ready for 1-click copy-pasting into Google Ads Keyword Planner.
    """
    if not os.path.exists(master_csv_path):
        print(f"Error: {master_csv_path} not found.")
        return

    en_keywords = []
    hu_keywords = []

    with open(master_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kw = row["Keyword"].strip()
            lang = row["Language"].strip().lower()
            if lang == "en" and kw not in en_keywords:
                en_keywords.append(kw)
            elif lang == "hu" and kw not in hu_keywords:
                hu_keywords.append(kw)

    en_out = os.path.join(output_dir, "keywords_to_paste_in_gkp_en.txt")
    hu_out = os.path.join(output_dir, "keywords_to_paste_in_gkp_hu.txt")

    with open(en_out, "w", encoding="utf-8") as f:
        f.write("\n".join(en_keywords))

    with open(hu_out, "w", encoding="utf-8") as f:
        f.write("\n".join(hu_keywords))

    print(f"[+] Exported {len(en_keywords)} English keywords to: {en_out}")
    print(f"[+] Exported {len(hu_keywords)} Hungarian keywords to: {hu_out}")
    return en_out, hu_out


def import_google_keyword_planner_csv(gkp_export_path: str, master_csv_path: str, output_merged_path: str):
    """
    Merges an exported CSV from Google Keyword Planner (containing exact search volumes,
    competition, and top of page CPCs) with our master keyword intelligence database.
    """
    if not os.path.exists(gkp_export_path):
        print(f"Error: Export file {gkp_export_path} does not exist.")
        return

    # Parse Google Keyword Planner CSV (often has utf-16 or utf-8, with header metadata)
    gkp_metrics = {}
    
    # Try different encodings Google uses
    encodings = ["utf-16", "utf-8", "utf-8-sig", "latin-1"]
    lines = []
    for enc in encodings:
        try:
            with open(gkp_export_path, "r", encoding=enc) as f:
                lines = f.readlines()
            if lines and ("Keyword" in lines[0] or "Kulcsszó" in lines[0] or any("Keyword" in l or "Kulcsszó" in l for l in lines[:10])):
                break
        except Exception:
            continue

    if not lines:
        print("[!] Could not decode Google Keyword Planner CSV file.")
        return

    # Find the actual header line
    header_idx = -1
    for i, line in enumerate(lines[:15]):
        if "Keyword" in line or "Kulcsszó" in line:
            header_idx = i
            break

    if header_idx == -1:
        print("[!] Could not locate header in Keyword Planner CSV.")
        return

    import io
    csv_data = "".join(lines[header_idx:])
    reader = csv.DictReader(io.StringIO(csv_data), delimiter="\t" if "\t" in lines[header_idx] else ",")

    for row in reader:
        # Match English or Hungarian Google Ads headers
        kw = row.get("Keyword") or row.get("Kulcsszó")
        if not kw:
            continue
        kw = kw.strip().lower()
        
        avg_vol = row.get("Avg. monthly searches") or row.get("Átlagos havi keresések") or row.get("Avg. Monthly Searches")
        competition = row.get("Competition") or row.get("Verseny")
        cpc_low = row.get("Top of page bid (low range)") or row.get("Oldaltetőre vonatkozó ajánlat (alsó tartomány)")
        cpc_high = row.get("Top of page bid (high range)") or row.get("Oldaltetőre vonatkozó ajánlat (felső tartomány)")
        
        gkp_metrics[kw] = {
            "exact_monthly_searches": avg_vol,
            "gkp_competition": competition,
            "cpc_low_range": cpc_low,
            "cpc_high_range": cpc_high
        }

    print(f"[+] Loaded exact metrics for {len(gkp_metrics)} keywords from Google Keyword Planner.")

    # Merge with Master CSV
    if os.path.exists(master_csv_path):
        merged_rows = []
        with open(master_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames)
            for extra in ["Exact_Monthly_Searches", "GKP_Competition", "CPC_Low", "CPC_High"]:
                if extra not in fieldnames:
                    fieldnames.append(extra)

            for row in reader:
                kw = row["Keyword"].strip().lower()
                metrics = gkp_metrics.get(kw, {})
                row["Exact_Monthly_Searches"] = metrics.get("exact_monthly_searches", "N/A")
                row["GKP_Competition"] = metrics.get("gkp_competition", "N/A")
                row["CPC_Low"] = metrics.get("cpc_low_range", "N/A")
                row["CPC_High"] = metrics.get("cpc_high_range", "N/A")
                merged_rows.append(row)

        with open(output_merged_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged_rows)
        print(f"[SUCCESS] Merged exact volume data saved to: {output_merged_path}")


def generate_google_ads_yaml_template(output_path: str):
    """Generates the YAML template for programmatic Google Ads API access."""
    template = """# Google Ads API Credentials Template
# Place your credentials from Google Cloud Console & Google Ads Manager Account (MCC)
developer_token: "INSERT_DEVELOPER_TOKEN_HERE"
client_id: "INSERT_OAUTH_CLIENT_ID_HERE.apps.googleusercontent.com"
client_secret: "INSERT_OAUTH_CLIENT_SECRET_HERE"
refresh_token: "INSERT_REFRESH_TOKEN_HERE"
login_customer_id: "INSERT_10_DIGIT_MCC_ID_WITHOUT_HYPHENS"
use_proto_plus: True
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"[+] Created Google Ads API configuration template at: {output_path}")


if __name__ == "__main__":
    cge_dir = "H:\\Youtube agent\\cge_engine"
    master_csv = os.path.join(cge_dir, "verified_keywords_master.csv")
    export_keywords_for_keyword_planner(master_csv, cge_dir)
    generate_google_ads_yaml_template(os.path.join(cge_dir, "google-ads.yaml.template"))
