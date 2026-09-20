"""Read-only AI analytics agent.

The LLM is asked to generate SQL, but execution is restricted to SELECT/WITH
queries. Add a BigQuery dry-run and table allow-list before production use.
"""
import os
import re
from google.cloud import bigquery

FORBIDDEN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|MERGE|TRUNCATE|GRANT|REVOKE)\b", re.I)

def validate_sql(sql: str) -> str:
    query = sql.strip().rstrip(";")
    if not re.match(r"^(SELECT|WITH)\b", query, re.I):
        raise ValueError("Only SELECT/WITH queries are allowed.")
    if FORBIDDEN.search(query):
        raise ValueError("Potentially mutating SQL was rejected.")
    return query

def run_query(sql: str):
    sql = validate_sql(sql)
    client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
    job_config = bigquery.QueryJobConfig(use_query_cache=True)
    return client.query(sql, job_config=job_config).result().to_dataframe()

def explain(question: str, sql: str, result):
    """Return a deterministic fallback explanation.

    Replace this with an LLM call in production. Keeping the execution layer
    separate makes the safety boundary testable.
    """
    if result.empty:
        return "The query returned no rows."
    return f"Question: {question}\nRows analysed: {len(result)}\nColumns: {', '.join(result.columns)}"
