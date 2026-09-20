# Architecture decisions

## Bronze
Raw files/API payloads are retained in Cloud Storage. This preserves replayability and provides an audit boundary.

## Silver
PySpark standardises data types, removes duplicate business keys, handles invalid records and derives row-level revenue/profit.

## Gold
BigQuery stores a star schema. Orders are partitioned by date and clustered by common filter dimensions to reduce scanned data.

## Orchestration
Airflow/Cloud Composer coordinates ingestion, transformation and validation. The DAG is intentionally simple enough to explain in an interview.

## AI
Natural-language questions are translated into SQL. SQL is validated before execution. The analytics identity should have read-only access to the warehouse.

## Client value
The same platform can support a retailer, D2C brand, distributor or other SMB by changing source connectors and dimensions while keeping the core architecture intact.
