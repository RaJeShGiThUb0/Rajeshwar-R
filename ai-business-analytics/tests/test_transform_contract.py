def test_business_columns():
    required = {"order_id", "order_date", "quantity", "unit_price", "unit_cost"}
    sample_header = {"order_id", "order_date", "customer_id", "product_id", "region", "quantity", "unit_price", "unit_cost"}
    assert required.issubset(sample_header)
