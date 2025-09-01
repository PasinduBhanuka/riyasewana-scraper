# Riyasewana.com Vehicle Listings Scraper (Python)

Scrapes vehicle listings from **riyasewana.com** into a clean Excel file (one row per listing).  
Built for learning and personal research; please **respect the website’s Terms of Service** and **avoid heavy scraping**.

## Features
- upload your personal user-agent
- Search by keyword (e.g., `Aqua`, `Honda Fit`, `Hilux`).
- Choose how many results to collect.
- Exports to `.xlsx` with columns: Title, Date, Time, Location, Contact, Make, Model, YOM, Mileage(km), Gear, Fuel Type, Options, Engine(cc), Price, Details, Link.
- Simple CLI flags or interactive prompts.
- Polite scraping: optional delay between requests and custom User-Agent.

> **Note:** Site structure can change. If selectors break, open an issue or a PR with a fix.

## Quick Start

### 1) Prerequisites
- Python 3.9+ (3.10–3.12 recommended)
- `pip`

### 2) Installation
```bash
git clone https://github.com/<your-username>/riyasewana-scraper.git
cd riyasewana-scraper
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
