# HW 4: Web Scraping Mini-Project

## Assignment Overview

In this assignment, you will practice web scraping skills by collecting data from a website of your choice, saving it in a structured format, and performing basic analysis on the collected data. This project will demonstrate your ability to:

1. Navigate website structure and extract relevant data
2. Handle web scraping ethically and responsibly
3. Clean and structure scraped data
4. Perform basic data analysis and visualization
5. Document your process clearly

## Assignment Requirements

### Core Tasks (Required)

1. **Choose a Website to Scrape**
   - Select from our suggested sites (see `example_sites.md`) OR
   - Choose your own site (must be approved - check robots.txt first!)
   
2. **Collect Data**
   - Scrape at least 50 items/records
   - Extract at least 3 different data fields per item
   - Handle errors gracefully (timeouts, missing data, etc.)

3. **Save Your Data**
   - Save as CSV or JSON format in the `data/` folder
   - Include a timestamp in your filename
   - Create a data dictionary explaining each field

4. **Analyze Your Data**
   - Compute basic statistics (mean, median, counts, etc.)
   - Create at least 2 visualizations
   - Write 2-3 paragraphs interpreting your findings

5. **Document Your Process**
   - Comment your code thoroughly
   - Explain your scraping strategy
   - Note any challenges and how you solved them
   - Cite the website and respect their terms of service

### Ethical Considerations

- **ALWAYS** check and respect robots.txt
- Add delays between requests (at least 1 second)
- Include a descriptive User-Agent header
- Do not overwhelm the server with requests
- Respect the website's terms of service
- Give proper attribution to data sources

## Repository Structure

```
web-scraping-mini-project/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── example_sites.md         # Suggested websites to scrape
├── starter_code.py         # Template code to get you started
├── analysis_template.ipynb # Jupyter notebook template
├── scraper.py              # YOUR scraping code goes here
├── analysis.ipynb          # YOUR analysis goes here
├── data/                   # Folder for scraped data
│   └── .gitkeep
└── outputs/                # Folder for visualizations
    └── .gitkeep
```

## Getting Started

1. **Clone this repository** through GitHub Classroom

2. **Set up your environment:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Review the starter files:**
   - Look at `starter_code.py` for a scraping template
   - Check `example_sites.md` for website suggestions
   - Review `analysis_template.ipynb` for analysis structure

4. **Start coding:**
   - Copy `starter_code.py` to `scraper.py` and modify it
   - Copy `analysis_template.ipynb` to `analysis.ipynb` for your analysis

## Submission Requirements

Your submission should include:

1. **Code Files:**
   - `scraper.py` - Your web scraping code
   - `analysis.ipynb` - Your data analysis notebook

2. **Data Files:**
   - Your scraped data in `data/` folder (CSV or JSON)

3. **Output Files:**
   - At least 2 visualizations in `outputs/` folder
   - Brief written analysis (in the notebook)

4. **Documentation:**
   - Well-commented code
   - Clear explanation of your process
   - Any assumptions or limitations noted

## Tips for Success

1. **Start Simple:** Begin with a basic scraper and gradually add features
2. **Test Often:** Scrape a few items first before attempting the full dataset
3. **Handle Errors:** Use try-except blocks for robust code
4. **Be Patient:** Add delays and be respectful of the website
5. **Document Everything:** Your future self will thank you

## Need Help?

- Review the Week 7 lecture materials on web scraping
- Use your AI coding journal to document any LLM assistance
- Post questions in the course forum
- Attend office hours

## Deadline

This assignment is due **one week from assignment date** via GitHub Classroom.

Good luck with your web scraping project!