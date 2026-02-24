import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://www.espn.com/mlb/worldseries/history/winners"

st.set_page_config(page_title="MLB World Series Dashboard", layout="wide") 
st.title("MLB World Series Dashboard")
st.markdown("This dashboard scrapes and visualizes MLB World Series winners data.")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
  tables = pd.read_html(DATA_URL, header=None)
  df = tables[0].copy()

  # Force column names (table header is not detected reliably)
  df.columns = ["Season", "Winner", "Loser", "Series"]

  df["Season"] = pd.to_numeric(df["Season"], errors="coerce")
  df = df.dropna(subset=["Season"])
  df["Season"] = df["Season"].astype(int)

  for c in ["Winner", "Loser", "Series"]:
    df[c] = df[c].astype(str).str.strip()

  return df

df = load_data()

st.subheader("Dataset preview")
st.dataframe(df.head(20), use_container_width=True)

min_year, max_year = int(df["Season"].min()), int(df["Season"].max())

st.sidebar.header("Filters")
start = max(min_year, max_year - 30)
year_range = st.sidebar.slider("Season range", min_year, max_year, (start, max_year))

filtered = df[(df["Season"] >= year_range[0]) & (df["Season"] <= year_range[1])].copy()

st.subheader("Filtered results")
st.write(f"Seasons: {year_range[0]}–{year_range[1]} | Rows: {len(filtered)}")
st.dataframe(filtered, use_container_width=True)

titles = (
  filtered.groupby("Winner", as_index=False)
  .size()
  .rename(columns={"size": "Titles"})
  .sort_values("Titles", ascending=False)
)

st.subheader("Championships by Team (selected range)")

fig = px.bar(
  titles.head(15),
  x="Winner",
  y="Titles",
  title="Top Teams by World Series Titles",
  labels={"Winner": "Team", "Titles": "Titles"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Notes / Cleaning Summary")
st.markdown(
  "- Scraped the winners table from ESPN\n"
  "- Assigned column names because the table header was not detected\n"
  "- Converted Season to integer and removed invalid rows\n"
  "- Added interactive filtering and aggregated titles by winner"
)