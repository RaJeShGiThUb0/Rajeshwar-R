# Power BI setup

## Recommended semantic model

Connect Power BI to BigQuery and expose:

- fact_orders
- dim_customer
- dim_product
- monthly KPI view

Create measures for:

- Revenue = SUM(fact_orders[revenue])
- Profit = SUM(fact_orders[profit])
- Orders = DISTINCTCOUNT(fact_orders[order_id])
- AOV = DIVIDE([Revenue], [Orders])
- Profit Margin = DIVIDE([Profit], [Revenue])

Suggested report pages:

1. Executive Overview
2. Product Performance
3. Customer & Retention
4. Regional Performance

Keep transformations in BigQuery rather than hiding business logic inside Power BI.
