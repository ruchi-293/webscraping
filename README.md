<<<<<<< HEAD
# IPL Player Analytics Dashboard

A resume-ready **web scraping + data analytics + Flask dashboard** project.

### Project flow

```text
Howstat IPL statistics
        ↓
Selenium + BeautifulSoup
        ↓
Pandas cleaning
        ↓
CSV dataset
        ↓
Flask API
        ↓
Interactive single-page dashboard
```

## Features

- IPL player statistics scraping
- Selenium browser automation
- BeautifulSoup table extraction
- Pandas data cleaning
- Top run scorer and wicket taker
- Top-10 runs and wickets charts
- Searchable player table
- Batting-average insight
- Bowling-average insight
- Responsive single-page UI
- CSV output for portfolio/data-analysis work

## Folder structure

```text
ipl-cricket-analytics-dashboard/
├── app.py
├── scraper.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── README.md
├── .gitignore
├── data/
│   ├── ipl_data.csv
│   └── top_3_run_scorers.csv
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── .github/
    └── workflows/
        └── update-data.yml
```

## Run locally on Windows

Open PowerShell inside this folder:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Update the IPL data

First try:

```powershell
python scraper.py
```

For a specific season/team:

```powershell
python scraper.py --season "2024" --team "Mumbai Indians"
```

The scraper updates:

```text
data/ipl_data.csv
data/top_3_run_scorers.csv
```

Then refresh the dashboard.

> Note: the Howstat page can change its dropdown/table structure. This project intentionally avoids absolute XPaths, but if Howstat changes its HTML completely, the selectors in `scraper.py` may need a small update.

## GitHub

```powershell
git init
git add .
git commit -m "Create IPL analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ipl-cricket-analytics-dashboard.git
git push -u origin main
```

## Deployment

### Render — recommended for the Flask version

1. Push this folder to GitHub.
2. Create a new **Web Service** on Render.
3. Connect your GitHub repository.
4. Build command:

```text
pip install -r requirements.txt
```

5. Start command:

```text
gunicorn app:app
```

6. Deploy.

### GitHub Pages

GitHub Pages can host the static HTML/CSS/JS but **cannot run Flask or Selenium**. For a live Flask dashboard, use Render, Railway, PythonAnywhere, or another Python host.

## Resume description

**IPL Player Analytics Dashboard | Python, Selenium, BeautifulSoup, Pandas, Flask**

Built an automated IPL statistics pipeline using Selenium and BeautifulSoup to collect player performance data, cleaned and analyzed the dataset with Pandas, and developed a responsive Flask dashboard with player search, performance charts, and data-driven batting/bowling insights.

## Good interview points

- Why Selenium? → The target page uses dynamic form controls and browser interaction.
- Why BeautifulSoup? → Efficiently parses the final HTML table.
- Why Pandas? → Cleaning, numeric conversion, sorting, ranking and analysis.
- Why Flask? → Lightweight Python backend for serving the dashboard and JSON APIs.
- Why CSV? → Simple, portable dataset that is easy to inspect and version-control.
- What is the pipeline? → Scrape → clean → store → API → visualize → insight.

## Important data note

The included CSV is a small demo dataset so the dashboard works immediately after cloning. Run `python scraper.py` to replace it with the current data returned by the source website.
=======
# webscraping
IPL Data Scraper – Developed a Python-based web scraping project to extract IPL match data, including teams, players, scores, results, and match details. Used BeautifulSoup/Selenium to collect and organize data for analysis.
>>>>>>> 3dbe13170471a5ebe9672ef2708439195cc27e91
