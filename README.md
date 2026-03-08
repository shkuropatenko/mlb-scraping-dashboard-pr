# MLB Leaders Scraping & Dashboard Project

## Overview

This project demonstrates a complete end-to-end data pipeline built with Python:

Selenium → CSV → SQLite → CLI Queries (JOIN) → Streamlit Dashboard

The data is scraped from the Baseball Almanac website, cleaned and structured, stored in a SQLite database, queried via command line, and visualized in an interactive dashboard.

---

## Project Structure

mlb-scraping-dashboard-pr/

├── data/  
│ └── raw/  
│ └── leaders.csv

├── scripts/  
│ ├── scrape_mlb.py # Selenium web scraping  
│ ├── import_db.py # CSV → SQLite  
│ └── query_db.py # CLI query with JOIN

├── dashboard/  
│ └── streamlit_app.py # Interactive dashboard

├── mlb.db # SQLite database  
├── requirements.txt  
└── README.md

---

## 1️⃣ Web Scraping (Selenium)

File: `scripts/scrape_mlb.py`

- Uses Selenium to retrieve MLB leader data
- Extracts structured information
- Saves raw data as CSV:

data/raw/leaders.csv

Run:

`python scripts/scrape_mlb.py`

## 2️⃣ Data Cleaning & SQLite Import

File: `scripts/import_db.py`

- Loads CSV using Pandas
- Converts numeric fields
- Cleans whitespace
- Drops malformed rows
- Imports cleaned data into SQLite (`mlb.db`)
- Creates an index for performance

Run:

`python scripts/import_db.py`

## 3️⃣ Database Query Program (JOIN)

File: `scripts/query_db.py`

- Uses SQL JOIN between tables
- Allows filtering by:
  - year
  - league (AL / NL)

Example:

`python scripts/query_db.py --year 2024 --league AL`

## 4️⃣ Interactive Dashboard (Streamlit)

File: `dashboard/streamlit_app.py`

The dashboard reads directly from SQLite and provides:

- Sidebar filters:
  - Year range
  - League
  - Category
- Three interactive visualizations:
  1. Top Teams by Leader Count (Bar chart)
  2. Leader Trends Over Time (Line chart)
  3. Statistic Value Over Time (Scatter chart)

Run:

`streamlit run dashboard/streamlit_app.py`

## Technologies Used

- Python
- Selenium
- Pandas
- SQLite
- Plotly
- Streamlit

---

## Data Pipeline Summary

1. Scraped MLB data using Selenium
2. Saved raw structured CSV
3. Cleaned and normalized dataset
4. Stored data in SQLite
5. Queried with JOIN using CLI
6. Built interactive dashboard

---

## Installation

Create virtual environment (recommended):

- python -m venv .venv
- .venv\Scripts\activate (Windows)
- source .venv/bin/activate (Mac/Linux)

Install dependencies:

`pip install -r requirements.txt`

## Reproducibility

To fully reproduce the project:

1. Install dependencies
2. Run scraping script
3. Import data into SQLite
4. Run dashboard

All required files and dependencies are included.

---

## Screenshot

![Dashboard Screenshot](dashboard_screenshot.png)
