"""
IPL player statistics scraper.

Run:
    python scraper.py

Optional:
    python scraper.py --season "2024" --team "Mumbai Indians"

The exact season/team names are read from the Howstat dropdowns.
Using visible text instead of absolute XPath makes the scraper much
less likely to break when the site's HTML layout changes.
"""

import argparse
import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.howstat.com/cricket/Statistics/IPL/PlayerList.asp"
OUTPUT = Path(__file__).parent / "data" / "ipl_data.csv"

COLUMNS = [
    "Player Name", "Matches", "Runs", "Batting Avg", "Wickets", "Bowling Avg"
]


def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def clean_number(value):
    value = value.replace(",", "").strip()
    try:
        return float(value)
    except ValueError:
        return 0.0


def scrape(season=None, team=None):
    driver = make_driver()
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)

        selects = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "select"))
        )
        if len(selects) < 2:
            raise RuntimeError("Could not find the season and team dropdowns.")

        season_select = Select(selects[0])
        team_select = Select(selects[1])

        # If values are not supplied, preserve the first useful options.
        # Passing visible text is safer than absolute XPath.
        if season:
            season_select.select_by_visible_text(season)
        elif len(season_select.options) > 1:
            season_select.select_by_index(len(season_select.options) - 1)

        time.sleep(1)

        if team:
            team_select = Select(
                wait.until(EC.presence_of_element_located((By.NAME, "cboTeam")))
            )
            team_select.select_by_visible_text(team)
        elif len(team_select.options) > 1:
            team_select.select_by_index(1)

        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="TableLined")

        if table is None:
            raise RuntimeError("Statistics table was not found on Howstat.")

        records = []
        for row in table.find_all("tr")[1:]:
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
            if len(cells) >= 6:
                records.append(cells[:6])

        if not records:
            raise RuntimeError("No player records were found.")

        df = pd.DataFrame(records, columns=COLUMNS)

        for col in COLUMNS[1:]:
            df[col] = df[col].map(clean_number)

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUTPUT, index=False)

        # Also create a useful ranking file.
        top3 = df.sort_values("Runs", ascending=False).head(3)
        top3.to_csv(OUTPUT.parent / "top_3_run_scorers.csv", index=False)

        print(f"Saved {len(df)} players to {OUTPUT}")
        print("\nTop 3 run scorers:")
        print(top3[["Player Name", "Runs", "Batting Avg"]].to_string(index=False))

    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", default=None)
    parser.add_argument("--team", default=None)
    args = parser.parse_args()
    scrape(args.season, args.team)
