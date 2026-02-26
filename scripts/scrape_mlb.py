from __future__ import annotations

import csv
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

YEAR_MENU_URL = "https://www.baseball-almanac.com/yearmenu.shtml"


@dataclass(frozen=True)
class LeaderRow:
  year: int
  league: str       # AL / NL
  category: str     # hitting / pitching
  statistic: str
  player: str
  team: str
  value: str


def make_driver() -> webdriver.Chrome:
  opts = Options()
  opts.add_argument("--headless=new")
  opts.add_argument("--disable-gpu")
  opts.add_argument("--no-sandbox")
  opts.add_argument("--window-size=1400,900")
  opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
  )
  service = Service(ChromeDriverManager().install())
  return webdriver.Chrome(service=service, options=opts)


def year_url(year: int, league: str) -> str:
  suffix = "a" if league.upper() == "AL" else "n"
  return f"https://www.baseball-almanac.com/yearly/yr{year}{suffix}.shtml"


def parse_leaders_from_body_text(body_text: str, year: int, league: str) -> list[LeaderRow]:
  lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]

  def collect_block(start_pat: str, end_pat: str, category: str) -> list[LeaderRow]:
    start_i = next((i for i, ln in enumerate(lines) if re.search(start_pat, ln)), None)
    if start_i is None:
        return []

    out: list[LeaderRow] = []
    i = start_i

    while i < len(lines) and "Statistic Name Team" not in lines[i]:
        i += 1
    i += 1

    while i < len(lines):
      ln = lines[i]
      if re.search(end_pat, ln):
        break

      if "Top 25" in ln:
        ln = ln.replace("Top 25", "").strip()

      m = re.match(
        r"^(?P<stat>.+?)\s+"
        r"(?P<player>[A-Z][a-zA-Z\.\-']+\s+[A-Z][a-zA-Z\.\-']+)\s+"
        r"(?P<team>.+?)\s+"
        r"(?P<value>[-\.\d]+)$",
        ln,
      )
      if m:
        out.append(
          LeaderRow(
            year=year,
            league=league,
            category=category,
            statistic=m.group("stat").strip(),
            player=m.group("player").strip(),
            team=m.group("team").strip(),
            value=m.group("value").strip(),
            )
          )
      i += 1

    return out

  hitting = collect_block(r"Player Review", r"Pitcher Review", "hitting")
  pitching = collect_block(r"Pitcher Review", r"Team Standings", "pitching")
  return hitting + pitching


def write_csv(rows: Iterable[LeaderRow], path: Path) -> None:
  with path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["year", "league", "category", "statistic", "player", "team", "value"])
    for r in rows:
      w.writerow([r.year, r.league, r.category, r.statistic, r.player, r.team, r.value])


def main() -> None:
  years = list(range(2015, 2025))  # keep it reasonable
  leagues = ["AL", "NL"]

  driver = make_driver()
  all_rows: list[LeaderRow] = []

  try:
    for year in years:
      for league in leagues:
        url = year_url(year, league)
        driver.get(url)
        time.sleep(0.8)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        rows = parse_leaders_from_body_text(body_text, year=year, league=league)
        all_rows.extend(rows)

    out_path = RAW_DIR / "leaders.csv"
    write_csv(all_rows, out_path)
    print(f"Saved {len(all_rows)} rows -> {out_path}")
  finally:
    driver.quit()


if __name__ == "__main__":
  main()