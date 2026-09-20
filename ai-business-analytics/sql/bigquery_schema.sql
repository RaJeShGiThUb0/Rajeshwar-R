CREATE SCHEMA IF NOT EXISTS `business_analytics`;

CREATE TABLE IF NOT EXISTS `business_analytics.fact_orders`
(
  order_id STRING NOT NULL,
  order_date DATE NOT NULL,
  customer_id STRING,
  product_id STRING,
  region STRING,
  quantity INT64,
  unit_price NUMERIC,
  unit_cost NUMERIC,
  revenue NUMERIC,
  profit NUMERIC,
  ingested_at TIMESTAMP
)
PARTITION BY order_date
CLUSTER BY region, product_id;

CREATE TABLE IF NOT EXISTS `business_analytics.dim_customer`
(
  customer_id STRING NOT NULL,
  customer_name STRING,
  segment STRING,
  region STRING
);

CREATE TABLE IF NOT EXISTS `business_analytics.dim_product`
(
  product_id STRING NOT NULL,
  product_name STRING,
  category STRING
);
