# Web Scraping Mini-Project — arXiv "AI" Research Trends

**Author:** Pei Zheng · UC Berkeley · **Date:** October 2025

A web scraper and analysis pipeline that collects recent AI-related research papers from [arXiv](https://arxiv.org/search/) and explores trends in topics, research categories, and author collaboration.

## Overview

This project scrapes the arXiv search results for the keyword **"AI"** (no API — direct HTML parsing), saves the records to CSV, and analyzes them in a Jupyter notebook. It covers the full pipeline: ethical scraping, data cleaning, exploratory analysis, and visualization.

- **Data source:** `https://arxiv.org/search/` (HTML scraping with BeautifulSoup)
- **Records collected:** 60 papers
- **Fields per record:** `title`, `authors`, `abstract`, `categories`, `submission_date`
- **Goal:** Surface patterns in recent arXiv publications tagged "AI"

## Repository Structure

```
hw4-web-scraping-mini-project/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── scraper.py                   # arXiv HTML scraper (pagination + per-paper enrichment)
├── analysis.ipynb               # Full analysis: cleaning, EDA, visualizations, findings
├── data/
│   ├── arxiv_AI_20251026.csv    # Raw scraped data (60 records, timestamped)
│   └── cleaned_data.csv         # Cleaned dataset
└── starter_code.py              # Original assignment template
```

## How It Works

### 1. Scraping (`scraper.py`)

The scraper extracts each result block from the arXiv search page (title, authors, abstract). Because the search page does not reliably expose categories and submission dates, the scraper also visits each paper's `/abs/` detail page to enrich those fields. It paginates through multiple result pages until the target record count is reached.

Ethical scraping practices built in:

- Checks `robots.txt` and sends a descriptive `User-Agent` identifying the author
- Applies a **1.2-second delay** between requests
- Handles errors gracefully (timeouts, missing fields)
- Collects only public metadata for research/educational use

### 2. Analysis (`analysis.ipynb`)

The notebook loads the scraped CSV, cleans it (drops duplicate titles, normalizes text), then runs exploratory analysis and produces three visualizations.

## Key Findings

1. **Title themes:** The most frequent title words are *models, learning, language, text, based* — pointing to a heavy focus on large language models, NLP, and text-based ML systems.
2. **Research categories:** The dominant categories are Artificial Intelligence (cs.AI), Machine Learning (cs.LG), and Computation and Language (cs.CL), reflecting strong overlap between AI, ML, and LLM research.
3. **Collaboration size:** Most papers have 3–6 authors, with a few large 10+ author collaborations — suggesting compact, often cross-institutional research teams rather than large consortia.

## Visualizations

The notebook produces:

1. A word cloud of the most frequent words in paper titles
2. A bar chart of the top 10 research categories
3. A distribution of author counts per paper

## Data Dictionary

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `title` | string | Paper title | "Real Deep Research for AI, Robotics and Beyond" |
| `authors` | string | Authors, `;`-separated | Anna Mészáros; Patrik Reizinger; Ferenc Huszár |
| `abstract` | string | Abstract text | "With the rapid growth of research in AI and robotics…" |
| `categories` | string | arXiv subject categories | Computation and Language (cs.CL); Artificial Intelligence (cs.AI) |
| `submission_date` | date | Submission date | 23 Oct 2025 |

## Technical Challenges

- **Pagination:** The initial scraper only read the first results page and fell short of 60 records. Solved by adding automatic pagination across result pages.
- **Missing metadata:** Categories and submission dates were empty when read from the search page alone. Solved by visiting each paper's `/abs/` page to extract those fields directly from the article metadata.

## Setup & Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper (produces a timestamped CSV in data/)
python scraper.py

# Open the analysis notebook
jupyter notebook analysis.ipynb
```

## Limitations & Future Work

The dataset covers only 60 papers from a single snapshot, so it is not enough to generalize broad trends. A larger, longitudinal dataset spanning multiple months or years would enable time-series analysis of topic evolution and collaboration networks. Future work could add metadata such as citation counts, institutional affiliations, and geography to reveal deeper patterns in global AI research.

## References

- Data source: https://arxiv.org/search/
- Date of collection: October 26, 2025
- Built with `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `seaborn`, and `wordcloud`
