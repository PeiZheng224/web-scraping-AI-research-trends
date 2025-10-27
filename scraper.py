"""
Web Scraping Mini-Project - Starter Code
COMPSS 211

arXiv HTML scraper

Remember to:
1. Check robots.txt before scraping
2. Add delays between requests
3. Handle errors gracefully
4. Document your code
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import argparse
import os
import re
from urllib.parse import urlencode

# ----------- Config -----------
HEADERS = {"User-Agent": "peizheng, pei_zheng@berkeley.edu"}
DELAY = 1.2
BASE = "https://arxiv.org/search/"

# ----------- Helper Functions -----------
def parse_item(div):
    """Extract title, authors, abstract, categories, submission_date from one result block."""
    # Title
    title_el = div.select_one("p.title")
    title = title_el.get_text(strip=True) if title_el else None

    # Authors
    authors_el = div.select("p.authors a")
    authors = "; ".join(a.get_text(strip=True) for a in authors_el) if authors_el else None

    # Abstract
    abs_el = div.select_one("span.abstract-full, span.abstract-short")
    abstract = abs_el.get_text(" ", strip=True) if abs_el else None
    if abstract:
        abstract = re.sub(r"^Abstract:\s*", "", abstract)

    # Categories & submission date (from the meta line on search page; may be missing)
    meta = div.select_one("p.is-size-7")
    categories = None
    submission_date = None
    if meta:
        meta_text = meta.get_text(" ", strip=True)
        m_cat = re.search(r"Subjects?:\s*(.+?)(?:\(|$)", meta_text)
        if m_cat:
            categories = m_cat.group(1).strip()
        m_date = re.search(r"Submitted\s+(?:on\s+)?(\d{1,2}\s+\w+\s+\d{4})", meta_text)
        if m_date:
            submission_date = m_date.group(1)

    # Get the absolute URL of the paper's /abs/ page for enrichment (kept internal; not saved to CSV)
    abs_a = div.select_one("p.list-title a[href*='/abs/'], a[href*='/abs/']")
    url_abs = abs_a["href"].strip() if abs_a and abs_a.has_attr("href") else None
    if url_abs and not url_abs.startswith("http"):
        url_abs = "https://arxiv.org" + url_abs

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "categories": categories,
        "submission_date": submission_date,
        "_url_abs": url_abs,  # internal use only
    }

def enrich_from_abs(url_abs):
    """
    Visit the arXiv /abs/ page to fetch categories and submission date.
    Returns (categories, submission_date) or (None, None) on failure.
    """
    if not url_abs:
        return None, None
    try:
        resp = requests.get(url_abs, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print("   [skip abs page]", e)
        return None, None

    s2 = BeautifulSoup(resp.text, "html.parser")

    # Categories: prefer the 'Subjects' cell (older/newer templates both handled)
    categories = None
    # common pattern
    cat_cell = s2.select_one("td.tablecell.subjects")
    if cat_cell:
        txt = cat_cell.get_text(" ", strip=True)
        categories = re.sub(r"^Subjects:\s*", "", txt).strip() if txt else None
    if not categories:
        # fallback: try to find any element containing 'Subjects:'
        meta_text = s2.get_text(" ", strip=True)
        m = re.search(r"Subjects:\s*(.+?)(?:\s{2,}|\Z)", meta_text)
        if m:
            categories = m.group(1).strip()

    # Submission date: from submission history box
    submission_date = None
    hist = s2.select_one("div.submission-history")
    if hist:
        # pick the first date in the history
        mdate = re.search(r"(\d{1,2}\s+\w+\s+\d{4})", hist.get_text(" ", strip=True))
        if mdate:
            submission_date = mdate.group(1)

    return categories, submission_date

def scrape_arxiv(query: str, max_records: int):
    """Scrape arXiv search HTML results until reaching max_records."""
    session = requests.Session()
    session.headers.update(HEADERS)

    records = []
    start = 0
    page_size = 100  # you asked for size=100; we will still stop at max_records

    while len(records) < max_records:
        params = {
            "query": query,
            "searchtype": "all",
            "abstracts": "show",
            "order": "-announced_date_first",
            "size": page_size,
            "start": start
        }
        url = BASE + "?" + urlencode(params)
        print(f"Scraping: {url}")

        try:
            r = session.get(url, timeout=20)
            r.raise_for_status()
        except Exception as e:
            print("Request error:", e)
            break

        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.select("li.arxiv-result, div.arxiv-result")
        if not results:
            print("No more results found.")
            break

        added = 0
        for div in results:
            rec = parse_item(div)

            # ✅ If categories / submission_date missing, visit /abs/ to enrich
            if (not rec.get("categories")) or (not rec.get("submission_date")):
                cats, subd = enrich_from_abs(rec.get("_url_abs"))
                # merge only if found
                if not rec.get("categories") and cats:
                    rec["categories"] = cats
                if not rec.get("submission_date") and subd:
                    rec["submission_date"] = subd
                # polite delay between detail requests
                time.sleep(DELAY)

            # drop internal key before saving
            rec.pop("_url_abs", None)

            if rec["title"]:
                records.append(rec)
                added += 1
                print(f"  ✓ collected {len(records)}")
                if len(records) >= max_records:
                    break

        # Stop if this page yielded nothing new (safety)
        if added == 0:
            print("No valid items parsed on this page.")
            break

        start += page_size
        time.sleep(DELAY)  # polite delay between pages

    return records[:max_records]

# ----------- CLI -----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="AI", help="Search keyword")
    parser.add_argument("--max_records", type=int, default=60, help="Number of papers to collect")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)
    rows = scrape_arxiv(args.query, args.max_records)

    out = f"data/arxiv_{args.query.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.csv"
    pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\n✅ Saved {len(rows)} records to {out}")
