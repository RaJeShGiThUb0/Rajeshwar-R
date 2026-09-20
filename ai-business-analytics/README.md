# AI-Powered Business Analytics Platform

A production-style portfolio project that turns CSV, REST API, and relational database data into a BigQuery analytics warehouse, Power BI-ready marts, and an AI analytics agent.

## Architecture

```
CSV / REST API / PostgreSQL
          |
       Python ETL
          |
   Cloud Storage (Bronze)
          |
      PySpark
          |
   BigQuery Silver/Gold
          |
   Power BI / Streamlit
          |
   AI Analytics Agent
          |
"Why did revenue fall in August?"
```

## What this demonstrates

- Python ingestion from files, APIs, and databases
- PySpark cleansing, deduplication and incremental processing
- BigQuery dimensional modelling, partitioning and clustering
- Airflow orchestration
- SQL analytics marts and KPI calculations
- AI-generated SQL with validation and read-only execution
- Business-facing analytics dashboard
- Tests, configuration, logging and data quality checks

## Project structure

```
ai-business-analytics/
├── app/                    # Streamlit dashboard + AI agent
├── data/sample/            # Small synthetic demo dataset
├── dags/                   # Airflow DAG
├── etl/                    # Python ingestion + PySpark transformation
├── sql/                    # BigQuery DDL and analytical queries
├── tests/                  # Unit tests
├── docs/                   # Architecture and Power BI setup
├── .env.example
├── requirements.txt
└── README.md
```

## Local demo

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run ai-business-analytics/app/dashboard.py
```

The dashboard can run against the included synthetic CSV for a zero-cloud demo.

## GCP deployment

1. Create a GCP project and enable BigQuery, Cloud Storage and Composer.
2. Create a bucket for the bronze layer.
3. Create the BigQuery datasets using `sql/bigquery_schema.sql`.
4. Configure service-account credentials through environment variables or Workload Identity.
5. Upload the DAG to Cloud Composer.
6. Configure Power BI to read the curated BigQuery tables.
7. Configure the AI provider key for the read-only analytics agent.

## AI safety design

The analytics agent is deliberately read-only. It:
1. accepts a business question;
2. asks the LLM for SQL;
3. validates the SQL against an allow-list of read-only statements;
4. executes only SELECT queries against the analytics dataset;
5. returns a concise business explanation with the queried metrics.

Never expose production credentials to the LLM and never allow INSERT, UPDATE, DELETE, DROP, ALTER or arbitrary DDL.

## Example questions

- Why did revenue decrease last month?
- Which products have the highest revenue growth?
- What regions have declining customer retention?
- Which customer segment has the highest average order value?
