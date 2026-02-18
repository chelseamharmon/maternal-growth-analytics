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

