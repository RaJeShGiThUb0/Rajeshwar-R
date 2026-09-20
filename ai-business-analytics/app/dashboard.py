"""Business analytics dashboard."""
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Business Analytics", layout="wide")
st.title("AI-Powered Business Analytics")

sample = Path(__file__).parents[1] / "data/sample/orders.csv"
df = pd.read_csv(sample, parse_dates=["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"]
df["profit"] = df["quantity"] * (df["unit_price"] - df["unit_cost"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"₹{df.revenue.sum():,.0f}")
c2.metric("Profit", f"₹{df.profit.sum():,.0f}")
c3.metric("Orders", f"{df.order_id.nunique():,}")
c4.metric("AOV", f"₹{df.revenue.sum()/df.order_id.nunique():,.0f}")

monthly = df.assign(month=df.order_date.dt.to_period("M").astype(str)).groupby("month", as_index=False).agg(
    revenue=("revenue", "sum"), profit=("profit", "sum")
)
st.subheader("Revenue & Profit Trend")
st.line_chart(monthly.set_index("month")[["revenue", "profit"]])

st.subheader("Top Products")
st.dataframe(
    df.groupby("product_id", as_index=False)["revenue"].sum()
      .sort_values("revenue", ascending=False),
    use_container_width=True,
)

st.subheader("Ask the data")
question = st.text_input("Example: Why did revenue fall last month?")
if question:
    st.info("AI SQL generation is wired to the read-only execution layer in app/ai_agent.py. Configure BigQuery and an LLM provider to enable live natural-language analysis.")
