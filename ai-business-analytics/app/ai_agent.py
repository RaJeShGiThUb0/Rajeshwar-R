"""Natural-language analytics agent with a strict read-only SQL boundary."""
import os,re
from google.cloud import bigquery
FORBIDDEN=re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|MERGE|TRUNCATE|GRANT|REVOKE|CALL|EXPORT)\b",re.I)
SCHEMA_CONTEXT="Tables: business_analytics.fact_orders(order_id,order_date,customer_id,product_id,region,quantity,unit_price,unit_cost,revenue,profit,ingested_at); business_analytics.dim_customer(customer_id,customer_name,segment,region); business_analytics.dim_product(product_id,product_name,category)"
def validate_sql(sql:str)->str:
    q=sql.strip().strip("`").rstrip(";").strip()
    if not re.match(r"^(SELECT|WITH)\b",q,re.I): raise ValueError("Only SELECT/WITH queries are allowed.")
    if FORBIDDEN.search(q): raise ValueError("Potentially mutating SQL was rejected.")
    return q
def generate_sql(question:str)->str:
    from openai import OpenAI
    c=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    p=f"You are a senior analytics engineer. Generate ONE BigQuery Standard SQL query answering the business question. Return SQL only. Never mutate data. Use only these tables: {SCHEMA_CONTEXT}. Business question: {question}"
    r=c.responses.create(model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),input=p)
    return validate_sql(r.output_text)
def run_query(sql:str,project=None):
    c=bigquery.Client(project=project or os.getenv("GCP_PROJECT_ID"))
    job=bigquery.QueryJobConfig(use_query_cache=True,maximum_bytes_billed=10000000000)
    return c.query(validate_sql(sql),job_config=job).result().to_dataframe()
def explain(question:str,sql:str,result)->str:
    if result.empty:return "No matching data was found."
    from openai import OpenAI
    c=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    p=f"Explain this analytics result to a business user. Do not invent facts. Question: {question}. SQL: {sql}. Result: {result.head(20).to_json(orient="records")}"
    return c.responses.create(model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),input=p).output_text.strip()
def ask(question:str):
    sql=generate_sql(question); data=run_query(sql)
    return {"sql":sql,"data":data,"answer":explain(question,sql,data)}
