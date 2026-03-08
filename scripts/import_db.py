from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("mlb.db")
LEADERS_CSV = Path("data/raw/leaders.csv")


def main() -> None:
  if not LEADERS_CSV.exists():
    raise FileNotFoundError("leaders.csv not found. Run scripts/scrape_mlb.py first.")

  df = pd.read_csv(LEADERS_CSV)

  # basic cleaning / type normalization
  df["year"] = pd.to_numeric(df["year"], errors="coerce")
  df = df.dropna(subset=["year"])
  df["year"] = df["year"].astype(int)

  for c in ["league", "category", "statistic", "player", "team", "value"]:
    df[c] = df[c].astype(str).str.strip()

  conn = sqlite3.connect(DB_PATH)
  try:
    df.to_sql("leaders", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_leaders_year_league ON leaders(year, league);")
    conn.commit()
  finally:
    conn.close()

  print(f"Imported {len(df)} rows into {DB_PATH} (table: leaders)")

if __name__ == "__main__":
  main()