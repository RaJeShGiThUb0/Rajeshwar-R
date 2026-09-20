SELECT
  DATE_TRUNC(order_date, MONTH) AS month,
  SUM(revenue) AS revenue,
  SUM(profit) AS profit,
  COUNT(DISTINCT order_id) AS orders,
  SAFE_DIVIDE(SUM(revenue), COUNT(DISTINCT order_id)) AS aov
FROM `business_analytics.fact_orders`
GROUP BY month
ORDER BY month;
