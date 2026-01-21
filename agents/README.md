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

