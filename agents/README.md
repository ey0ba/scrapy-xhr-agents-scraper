# FIR Agents Scraper (Scrapy + XHR)

Scrapes real estate agent profiles from the Fortune International Realty agents directory and exports structured data to JSON and CSV.

This project demonstrates scraping:
- Directory listings
- Individual profile pages
- JavaScript-delivered data (XHR / embedded JSON)
- Clean structured output using Scrapy pipelines

---

## What it collects

For each agent:
- Name  
- Role / title  
- Profile URL  
- Profile image URL  
- Phone number  
- Social links (if available)  
- Bio (cleaned)  
- Source URLs  

---

## Output

The scraper exports:

- `agents.json`
- `agents.csv`

(Generated via Scrapy Feed Exports or pipelines.)

---

## Tech stack

- Python 3.x  
- Scrapy  
- XPath / CSS selectors  
- Requests-style headers & throttling  

---

## Project structure

scrapy-xhr-agents-scraper/
├── scrapy.cfg
├── README.md
├── agents/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── fir_agents.py
│       └── __init__.py
├── agents.json
├── agents.csv
└── requirements.txt


---

## Setup
Setup
1) Create a virtual environment (optional but recommended)

python -m venv .venv
source .venv/bin/activate


2) Install dependencies

pip install -r requirements.txt


## Run

Run the spider directly with Scrapy:

scrapy crawl fir_agents -O agents.json
scrapy crawl fir_agents -O agents.csv



## Notes on data quality

Notes on data quality

Roles are normalized (e.g., "Realtor-associate" → "Realtor Associate").

Repeated boilerplate marketing text is removed from bios.

Some phone numbers appear to be office numbers shared across multiple agents.

Missing emails are stored as null when not present on the page.

Social links are often company-level accounts rather than agent-specific.

## Example record

{
  "name": "Ana Diazgranados",
  "role": "Realtor Associate",
  "profile_url": "https://fir.com/agent/ana-diazgranados",
  "image_url": "https://media-production.lp-cdn.com/media/wmn6mmgbzrdmfr8lp5fo",
  "phone": "(305) 400-6393",
  "email": null,
  "socials": {
    "instagram": "https://www.instagram.com/fortuneinternationalrealty/"
  },
  "bio": "As a long-time Miami resident, Ana has an intimate knowledge of the South Florida real estate market...",
  "source_url": "https://fir.com/agents"
}

---

## Disclaimer

This project is for educational and portfolio purposes only.
Please respect the website’s terms of service and robots.txt policies.
Do not use this scraper for commercial or abusive purposes.

## Author

Eyob Assefa Betiru
Python Web Scraping | Scrapy | XHR / JSON Parsing | Data Extraction
