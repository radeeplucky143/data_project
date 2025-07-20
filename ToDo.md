## Data Pipeline – End-to-End Commands

### 1. Project Setup

```bash
# Install dependencies from Pipfile, including dev tools
pipenv install --dev
```

### 2. Data Placement

- Place source data in the `data/` directory:
    - `unity_golf_club.csv`
    - `us_softball_league.tsv`
    - `companies.csv`

### 3. Run ETL (clean, merge, output results)

```bash
pipenv run python -m src.etl
# Outputs:
#   results/master_membership.csv
#   results/suspect_records.csv
```

### 4. Generate Metrics

```bash
pipenv run python -m src.metric
# Outputs:
#   results/metrics_report.md
```

### 5. Ingest Clean Data to SQLite Database

```bash
pipenv run python -m src.db_model
# Outputs:
#   membership.db (SQLite file with 'members' and 'suspect_records' tables)
```

### 6. Run Test Suite

```bash
pipenv run pytest
```

### 7. Review Output Files

- **Clean membership/candidate data:** `results/master_membership.csv`
- **Suspects (bad data):**          `results/suspect_records.csv`
- **Metrics, leaderboards, KPIs:**   `results/metrics_report.md`
- **Database:**                      `membership.db` (in project root)

## Optional: Explore Database with SQLite CLI

```bash
sqlite3 membership.db
# At the sqlite prompt:
.tables
.schema members
SELECT COUNT(*) FROM members;
SELECT * FROM members LIMIT 5;
SELECT * FROM suspect_records LIMIT 5;
.quit
```

Or, use a GUI tool like [DB Browser for SQLite](https://sqlitebrowser.org/).

## Handy Housekeeping

```bash
# Remove existing database to re-ingest from scratch:
rm membership.db

# Re-run ETL/metrics after changing source data or code
pipenv run python -m src.etl
pipenv run python -m src.metrics
```