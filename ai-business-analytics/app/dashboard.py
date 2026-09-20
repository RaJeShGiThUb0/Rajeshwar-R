"""Business analytics dashboard with local demo and optional live AI."""
from pathlib import Path
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AI Business Analytics", page_icon="📊", layout="wide")
ROOT = Path(__file__).parents[1]
df = pd.read_csv(ROOT / "data/sample/orders.csv", parse_dates=["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"]
df["profit"] = df["quantity"] * (df["unit_price"] - df["unit_cost"])

st.title("📊 AI-Powered Business Analytics")
st.caption("Synthetic retail data • PySpark/BigQuery architecture • optional natural-language AI")

c1,c2,c3,c4=st.columns(4)
c1.metric("Revenue",f"₹{df.revenue.sum():,.0f}")
c2.metric("Profit",f"₹{df.profit.sum():,.0f}")
c3.metric("Orders",f"{df.order_id.nunique():,}")
c4.metric("AOV",f"₹{df.revenue.sum()/df.order_id.nunique():,.0f}")

monthly=df.assign(month=df.order_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(revenue=("revenue","sum"),profit=("profit","sum"))
st.subheader("Revenue & Profit Trend")
st.line_chart(monthly.set_index("month")[["revenue","profit"]])

a,b=st.columns(2)
with a:
    st.subheader("Top Products")
    st.dataframe(df.groupby("product_id",as_index=False)["revenue"].sum().sort_values("revenue",ascending=False),use_container_width=True,hide_index=True)
with b:
    st.subheader("Regional Performance")
    st.dataframe(df.groupby("region",as_index=False).agg(revenue=("revenue","sum"),profit=("profit","sum")).sort_values("revenue",ascending=False),use_container_width=True,hide_index=True)

st.subheader("🤖 Ask the data")
question=st.text_input("Try: Why did revenue increase from June to August?")
if question:
    if os.getenv("OPENAI_API_KEY") and os.getenv("GCP_PROJECT_ID"):
        try:
            from app.ai_agent import ask
            with st.spinner("Generating SQL and analysing BigQuery..."):
                result=ask(question)
            st.markdown("**Business answer**")
            st.write(result["answer"])
            with st.expander("Generated SQL"):
                st.code(result["sql"],language="sql")
            st.dataframe(result["data"],use_container_width=True)
        except Exception as exc:
            st.error(f"Live AI analysis failed: {exc}")
    else:
        st.warning("Set OPENAI_API_KEY and GCP_PROJECT_ID to enable live BigQuery AI analysis.")
        st.info("The local dashboard works without cloud credentials.")
