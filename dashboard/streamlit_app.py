from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path("mlb.db")


@st.cache_data(show_spinner=False)
def load_leaders() -> pd.DataFrame:
  conn = sqlite3.connect(DB_PATH)
  try:
      df = pd.read_sql_query("SELECT * FROM leaders;", conn)
  finally:
      conn.close()

  df["year"] = pd.to_numeric(df["year"], errors="coerce")
  df = df.dropna(subset=["year"])
  df["year"] = df["year"].astype(int)

  for c in ["league", "category", "statistic", "player", "team", "value"]:
      df[c] = df[c].astype(str).str.strip()

  df["value_num"] = pd.to_numeric(df["value"], errors="coerce")
  return df


st.set_page_config(page_title="MLB Leaders Dashboard", layout="wide")
st.title("MLB Leaders Dashboard (Baseball Almanac)")
st.caption("Selenium → CSV → SQLite → CLI JOIN → Streamlit dashboard")

if not DB_PATH.exists():
  st.error("mlb.db not found. Run: python scripts/import_db.py")
  st.stop()

df = load_leaders()

min_year, max_year = int(df["year"].min()), int(df["year"].max())

st.sidebar.header("Filters")
year_range = st.sidebar.slider("Year range", min_year, max_year, (max(max_year - 5, min_year), max_year))
league = st.sidebar.selectbox("League", ["AL", "NL"])
category = st.sidebar.selectbox("Category", sorted(df["category"].unique()))

filtered = df[
  (df["year"].between(year_range[0], year_range[1]))
  & (df["league"] == league)
  & (df["category"] == category)
].copy()

st.subheader("Preview (filtered)")
st.write(f"Rows: {len(filtered)}")
st.dataframe(filtered.head(30), use_container_width=True)

# 1) Bar chart — Top teams by leader rows
st.subheader("1) Top Teams by Leader Count")
top_teams = (
  filtered.groupby("team", as_index=False)
  .size()
  .rename(columns={"size": "leader_count"})
  .sort_values("leader_count", ascending=False)
  .head(10)
)
fig1 = px.bar(
  top_teams,
  x="team",
  y="leader_count",
  title=f"Top 10 Teams by Leader Rows — {league} / {category}",
  labels={"team": "Team", "leader_count": "Leader rows"},
)
st.plotly_chart(fig1, use_container_width=True)

# 2) Line chart — Trend by year
st.subheader("2) Leader Rows Over Time")
trend = (
  filtered.groupby("year", as_index=False)
  .size()
  .rename(columns={"size": "leader_rows"})
  .sort_values("year")
)
fig2 = px.line(
  trend,
  x="year",
  y="leader_rows",
  title=f"Leader Rows by Year — {league} / {category}",
  labels={"year": "Year", "leader_rows": "Rows"},
)
st.plotly_chart(fig2, use_container_width=True)

# 3) Scatter — Numeric values over time for a chosen statistic
st.subheader("3) Statistic Value Over Time (numeric only)")
stats = sorted(filtered["statistic"].unique())
stat_choice = st.selectbox("Statistic", stats)

stat_df = filtered[filtered["statistic"] == stat_choice].copy()
stat_df = stat_df.dropna(subset=["value_num"]).sort_values("year")

if stat_df.empty:
  st.info("No numeric values available for this statistic with the current filters.")
else:
    fig3 = px.scatter(
      stat_df,
      x="year",
      y="value_num",
      hover_data=["player", "team", "value"],
      title=f"{stat_choice} — {league} / {category}",
      labels={"value_num": "Value"},
    )
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Cleaning / Pipeline Summary")
st.markdown(
    """
- Scraped year pages using Selenium and saved raw CSV (`data/raw/leaders.csv`).
- Normalized types and imported data into SQLite (`mlb.db`) as the `leaders` table.
- Added a CLI query program that performs a JOIN and filters by year/league.
- Built this Streamlit dashboard with interactive filters and three visualizations.
"""
)