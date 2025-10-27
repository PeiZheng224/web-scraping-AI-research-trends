"""
Web Scraping Mini-Project - Scraper Code
COMPSS 211

BBC News Scraper

Remember to:
1. Check robots.txt before scraping
2. Add delays between requests
3. Handle errors gracefully
4. Document your code
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime
import os

# ---------- Config ----------
base = "https://www.bbc.com"
query = "Taiwan"
headers = {"User-Agent": "peizheng, pei_zheng@berkeley.edu"}
records = []
page = 1
MAX_RECORDS = 60
DELAY = 1.2

# ---------- Skip obvious non-article paths ----------
SKIP_PATHS = [
    "/live", "/sport/", "/reel/", "/sounds/", "/iplayer/",
    "/weather/", "/topics/", "/programmes/", "/cbbc/", "/cbeebies/",
    "/newsletters/", "/bbcverify/", "/in_pictures/"
]

def is_valid_article(link):
    """Skip links that belong to clearly non-article sections."""
    return not any(skip in link for skip in SKIP_PATHS)

# ---------- Helper: parse one article ----------
def parse_article(url):
    """Visit an article page and extract description, image, and published time."""
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("   [skip]", e)
        return None, None, None

    soup = BeautifulSoup(r.text, "html.parser")

    # description (first few paragraphs)
    paragraphs = [p.get_text(strip=True) for p in soup.select("article p")]
    description = "\n".join(paragraphs[:6]) if paragraphs else None

    # image
    img = soup.find("meta", property="og:image")
    img_url = img.get("content") if img else None

    # published time
    t = soup.find("meta", property="article:published_time")
    published_time = t.get("content") if t else None

    return description, img_url, published_time

# ---------- Main scraping loop ----------
while len(records) < MAX_RECORDS:
    url = f"{base}/search?q={query}&page={page}"
    print(f"Scraping page {page}: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Request error:", e)
        break

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select('a[href*="/news"]')
    if not items:
        print("No more results found.")
        break

    for a in items:
        link = a["href"].strip()
        if not link.startswith("http"):
            link = base + link
        if not is_valid_article(link):
            continue

        title = a.get_text(strip=True)
        if not title:
            continue

        # summary (from search page)
        p = a.find_next("p")
        summary = p.get_text(strip=True) if p else None

        # detail page
        description, img_url, published_time = parse_article(link)

        records.append({
            "title": title,
            "url": link,
            "summary": summary,
            "description": description,
            "image_url": img_url,
            "published_time": published_time,
            "source": "BBC News",
            "scraped_at": datetime.now().isoformat(timespec="seconds")
        })

        print(f"  ✓ collected {len(records)}")
        if len(records) >= MAX_RECORDS:
            break
        time.sleep(DELAY)

    page += 1
    time.sleep(DELAY)

# ---------- Save CSV ----------
out = f"data/bbc_Taiwan_{datetime.now().strftime('%Y%m%d')}.csv"
pd.DataFrame(records).to_csv(out, index=False, encoding="utf-8-sig")
print(f"✅ Saved {len(records)} records to {out}")
