# Maternal Growth & Retention Analytics

End-to-end healthcare growth analytics simulation using PostgreSQL, Python, and SQL.

## Overview

This project simulates a maternal health enrollment funnel and patient retention analytics workflow, modeling how healthcare startups track:

- Patient acquisition
- Risk segmentation
- Enrollment conversion
- Cohort retention
- Operational KPIs

## Tech Stack

- PostgreSQL (OLTP simulation)
- SQL (analytics layer)
- Python (data generation + ETL)
- SQLAlchemy
- Pandas

## Project Structure

- `sql/ddl` – schema definitions
- `sql/analytics` – funnel + retention queries
- `src/` – data generation & ETL scripts
- `notebooks/` – exploratory analysis
- `data/` – optional exports

## How to Run

1. Start PostgreSQL
2. Run DDL:

```bash
psql -d maternal_growth -f sql/ddl/01_create_tables.sql

## Quickstart (Local)

### 1. Create/activate venv and install deps
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``` 

### 2. Create database tables
```bash
psql -d maternal_growth -f sql/ddl/01_create_tables.sql
psql -d maternal_growth -f sql/ddl/02_core_tables.sql
psql -d maternal_growth -f sql/ddl/03_seed_channels.sql
```

### 3. Load synthetic data
```bash
python src/load_patients.py
python src/load_lifecycle_and_events.py
```

### 4. Run analytics queries
```bash
psql -d maternal_growth -f sql/analytics/01_funnel_conversion_by_channel.sql
psql -d maternal_growth -f sql/analytics/02_weekly_cohort_retention.sql
```


