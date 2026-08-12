# Bay Area Job Search Agent

A fully free, zero-API-key AI job search agent that scrapes **Indeed + LinkedIn** for Bay Area tech jobs and guides you via a conversational chat interface.

## Features

- Chat-based intake: describe your role, skills, experience level, job type
- Scrapes **Indeed** and **LinkedIn** (headless Chrome, anti-detection headers)
- NLTK-powered keyword extraction and relevance scoring
- Job cards with source badges, salary, and direct links
- Filter by source (Indeed / LinkedIn), remote jobs, or listings with salary
- Graceful fallback to Indeed-only if LinkedIn blocks the scraper

## Setup

```bash
cd bay_area_job_agent
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5050** in your browser.

## Usage

Type naturally in the chat, for example:
- *"Senior Python backend engineer, 5 years experience, open to remote"*
- *"Data scientist with ML and SQL skills, hybrid roles"*
- *"Frontend React developer at a startup"*

The agent will search both sites (~20-40 seconds) and display ranked results.

## Notes

- No API keys required — 100% free
- LinkedIn occasionally blocks headless scrapers; agent falls back to Indeed automatically
- Chrome must be installed (ChromeDriver is auto-managed by webdriver-manager)
