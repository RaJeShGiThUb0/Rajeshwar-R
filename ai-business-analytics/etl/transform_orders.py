"""PySpark transformation for orders.

Cleans nulls, normalises types, removes duplicate order IDs and creates
business-friendly revenue/profit columns.
"""
from pyspark.sql import SparkSession, functions as F

def build_silver(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("business-analytics-silver").getOrCreate()
    df = spark.read.option("header", True).csv(input_path)

    clean = (
        df.select(
            "order_id", "order_date", "customer_id", "product_id",
            "region", "quantity", "unit_price", "unit_cost"
        )
        .withColumn("order_date", F.to_date("order_date"))
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("unit_price", F.col("unit_price").cast("double"))
        .withColumn("unit_cost", F.col("unit_cost").cast("double"))
        .dropDuplicates(["order_id"])
        .filter(F.col("order_id").isNotNull())
        .withColumn("revenue", F.col("quantity") * F.col("unit_price"))
        .withColumn("profit", F.col("quantity") * (F.col("unit_price") - F.col("unit_cost")))
        .withColumn("ingested_at", F.current_timestamp())
    )
    clean.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    build_silver("data/sample/orders.csv", "data/silver/orders")
