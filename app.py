import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="Blockchain adoption", page_icon="💠", layout="wide")

DATA_DIR = Path("data")

def load_csv(name, default_df):
    try:
        p = DATA_DIR / name
        if p.exists():
            return pd.read_csv(p)
        else:
            return default_df.copy()
    except Exception:
        return default_df.copy()

def metric_card(label, value, helptext=""):
    with st.container(border=True):
        st.markdown(f"**{label}**")
        st.markdown(f"<h2 style='margin-top:-6px;'>{value}</h2>", unsafe_allow_html=True)
        if helptext:
            st.caption(helptext)

# Default datasets
df_internet_default = pd.DataFrame({
    "year": [1985, 1990, 1995, 2000, 2005],
    "users_millions_est": [1, 10, 100, 500, 1100]
})
df_blockchain_default = pd.DataFrame({
    "year": [2009, 2015, 2020, 2025],
    "users_millions_est": [0.1, 5, 50, 250]
})

start = datetime.today().date() - timedelta(days=179)
df_tx_default = pd.DataFrame({
    "date": pd.date_range(start, periods=180, freq="D"),
    "btc_daily_tx": [300000 + (i % 50) * 1000 for i in range(180)],
    "swift_daily_msgs": [35000000 + (i % 50) * 100000 for i in range(180)],
})

# Load actual CSVs if available
df_internet = load_csv("adoption_internet.csv", df_internet_default)
df_blockchain = load_csv("adoption_blockchain.csv", df_blockchain_default)
df_tx = load_csv("transactions_comparison.csv", df_tx_default)
if "date" in df_tx.columns:
    df_tx["date"] = pd.to_datetime(df_tx["date"])

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Adoption", "💸 Transactions", "⚖️ Risks"])

# Pages
if page == "🏠 Home":
    st.title("Blockchain adoption")
    metric_card("Years since Bitcoin genesis", f"{datetime.now().year - 2009}+")
    metric_card("Avg daily BTC tx (30d)", f"{int(df_tx.tail(30)['btc_daily_tx'].mean()):,}")

elif page == "📈 Adoption":
    st.subheader("Internet vs Blockchain Adoption")
    di = df_internet.copy(); db = df_blockchain.copy()
    di['series'] = 'Internet'; db['series'] = 'Blockchain'
    df_all = pd.concat([di, db])
    chart = alt.Chart(df_all).mark_line(point=True).encode(
        x="year:O", y="users_millions_est:Q", color="series:N",
        tooltip=["series","year","users_millions_est"]
    )
    st.altair_chart(chart, use_container_width=True)
    st.caption("Comparison of user adoption trends.")

elif page == "💸 Transactions":
    st.subheader("BTC vs SWIFT Transactions")
    t = df_tx.copy().sort_values("date")
    t["btc_ma7"] = t["btc_daily_tx"].rolling(7).mean()
    chart = alt.Chart(t).mark_line().encode(
        x="date:T", y="btc_ma7:Q"
    )
    st.altair_chart(chart, use_container_width=True)
    st.caption("7-day average of BTC transactions.")

elif page == "⚖️ Risks":
    st.subheader("Risks vs Opportunities")
    df_risk = pd.read_csv(DATA_DIR / "risks_opportunities.csv")
    heat = df_risk.melt(id_vars="factor", var_name="dimension", value_name="score")
    heat = heat.replace({"opportunity_score":"Opportunity","risk_score":"Risk"})
    heat_chart = alt.Chart(heat).mark_rect().encode(
        x="dimension:N", y="factor:N", color="score:Q",
        tooltip=["factor","dimension","score"]
    )
    st.altair_chart(heat_chart, use_container_width=True)
    st.caption("Heatmap of risk vs opportunity scores.")
