# companysale

This repository collects discounted sale items from configured websites and publishes a React dashboard to GitHub Pages.

## What it contains

- `scraper/`: Python scraper logic and parsers
- `config/sites.yaml`: scrape targets
- `frontend/sales-frontend/`: React/Vite dashboard application
- `.github/workflows/jekyll-gh-pages.yml`: GitHub Actions deployment workflow

## How it works

1. The scraper fetches site HTML and parses discounted items.
2. Scraped JSON is written to `frontend/sales-frontend/public/data/sale_data.json`.
3. The React app builds with Vite and reads `./data/sale_data.json`.
4. GitHub Pages deploys the built dashboard from `frontend/sales-frontend/dist`.

## Local development

```bash
cd scraper
python -m pip install -r requirements.txt
python scraper.py

cd ../frontend/sales-frontend
npm install
npm run dev
```

## Deployment

Push to `main` and GitHub Actions will:
- install Python dependencies
- scrape the target site
- build the frontend
- deploy the dashboard to GitHub Pages
