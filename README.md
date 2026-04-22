# MLB Leaders Scraping & Dashboard Project

## 🚀 MLB Data Pipeline

End-to-end data pipeline for collecting, processing, and analyzing MLB data using Python.

This project demonstrates a small-scale ETL workflow:
- Extract: scrape MLB data using Selenium  
- Transform: clean and process data with Pandas (handling missing values, type conversion, filtering)  
- Load: store structured data in SQLite with indexed tables  
- Query: run SQL queries with joins and aggregations  
- Visualize: display insights using a Streamlit dashboard and Plotly  

Tech stack: Python, Pandas, Selenium, SQLite, SQL, Streamlit  

The goal is to simulate a real-world data workflow, from raw data ingestion to analysis and visualization.

## Why This Project Matters

This project demonstrates how to build a simple but complete data pipeline:
from raw data ingestion to structured storage and downstream analytics.

It reflects real-world data engineering tasks such as:
- handling imperfect data
- designing a data flow
- working with databases and queries
- connecting data pipelines to user-facing applications

## Project Structure

mlb-data-pipeline/
│
│
│
├── data/
│ └── raw/
│ └── leaders.csv
│
├── scripts/
│ ├── scrape_mlb.py # Selenium scraping
│ ├── import_db.py # CSV → SQLite
│ └── query_db.py # SQL queries (JOIN)
│
├── dashboard/
│ └── streamlit_app.py # Interactive dashboard
│
├── mlb.db # SQLite database
├── requirements.txt
└── README.md
│
│
│

### 1️⃣ Web Scraping (Selenium)

- Retrieves MLB leader data  
- Extracts structured information  
- Saves raw data to CSV  

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

## Future Improvements

- Add pipeline scheduling (Airflow or Prefect)
- Replace SQLite with PostgreSQL
- Containerize with Docker
- Add automated tests for data transformations
- Store data in cloud storage (e.g., AWS S3)
