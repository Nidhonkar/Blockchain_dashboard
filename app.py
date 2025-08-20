import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="Blockchain adoption", page_icon="₿", layout="wide")

# ---------- Styles (neon/glass) ----------
st.markdown("""
<style>
.big-title { font-size: 42px; font-weight: 800; letter-spacing: .5px; }
.hero { padding: 18px 22px; border-radius: 18px;
  background: linear-gradient(135deg, rgba(247,147,26,.18), rgba(37,99,235,.14));
  border: 1px solid rgba(255,255,255,.08); }
.card { padding: 14px 16px; border-radius: 16px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
.kpi { font-size: 36px; font-weight: 800; }
.caption { color: #cbd5e1; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path("data")

def load_csv(name, default_df):
    try:
        p = DATA_DIR / name
        if p.exists():
            return pd.read_csv(p)
        return default_df.copy()
    except Exception:
        return default_df.copy()

# ---------- Defaults ----------
df_internet_default = pd.DataFrame({
    "year":[1985,1990,1995,2000,2005],
    "users_millions_est":[1,10,100,500,1100]
})
df_blockchain_default = pd.DataFrame({
    "year":[2009,2015,2020,2025],
    "users_millions_est":[0.2,5,50,280]
})
start = datetime.today().date() - timedelta(days=179)
df_tx_default = pd.DataFrame({
    "date": pd.date_range(start, periods=180, freq="D"),
    "btc_daily_tx":[300000 + (i%60)*1200 for i in range(180)],
    "swift_daily_msgs":[35000000 + (i%60)*120000 for i in range(180)]
})
df_fees_default = pd.DataFrame({
    "corridor":["UAE→India","UAE→Philippines","KSA→Pakistan","US→Mexico","EU→Morocco"],
    "traditional_fee_pct":[6.5,7.2,6.8,5.9,6.1],
    "blockchain_fee_pct":[2.2,2.5,2.3,1.8,2.1]
})
df_token_default = pd.DataFrame({
    "asset_class":["Real Estate","Art","Bonds","Equity","Commodities"],
    "tokenized_value_usd_bn_est":[3.2,0.6,5.1,4.0,2.3]
})
df_risk_default = pd.DataFrame({
    "factor":["Transparency","Financial Inclusion","Cost Efficiency","Speed/Settlement","Volatility","Regulatory Clarity","Scams/Fraud","Security"],
    "opportunity_score":[9,8,8,8,3,5,4,7],
    "risk_score":[2,3,3,2,8,6,7,4]
})
df_cbdc_default = pd.DataFrame({
    "country":["China","EU","UAE","India","Brazil","Singapore"],
    "project":["e‑CNY","Digital Euro","mBridge/Aber","Digital Rupee","Drex","Ubin/Orchid"],
    "status":["Pilot","Preparation","Pilot","Pilot","Pilot","Experimentation"]
})

# ---------- Load CSV or defaults ----------
df_internet = load_csv("adoption_internet.csv", df_internet_default)
df_blockchain = load_csv("adoption_blockchain.csv", df_blockchain_default)
df_tx = load_csv("transactions_comparison.csv", df_tx_default); 
if "date" in df_tx.columns: df_tx["date"]=pd.to_datetime(df_tx["date"])
df_fees = load_csv("remittance_fees.csv", df_fees_default)
df_token = load_csv("tokenization_assets.csv", df_token_default)
df_risk  = load_csv("risks_opportunities.csv", df_risk_default)
df_cbdc  = load_csv("cbdc_projects.csv", df_cbdc_default)

# ---------- Sidebar ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home","📈 Adoption","💸 Transactions & Costs","🧱 Tokenization","⚖️ Risks","🔭 CBDC Outlook"])
presentation = st.sidebar.checkbox("Presentation Mode (simplify visuals)", value=True)
if presentation: alt.themes.enable("none")

# ---------- Home ----------
if page == "🏠 Home":
    st.markdown('<div class="hero"><div class="big-title">₿ Blockchain adoption</div><div class="caption">Crypto‑styled dashboard with neon glass cards and curated metrics.</div></div>', unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><div>⛓️ Years since Bitcoin genesis</div><div class="kpi">%s+</div><div class="caption">Bitcoin launched in 2009 — the “email” moment for blockchain.</div></div>' % (datetime.now().year-2009), unsafe_allow_html=True)
    with c2:
        last30 = int(df_tx.tail(30)["btc_daily_tx"].mean())
        st.markdown(f'<div class="card"><div>₿ Avg daily BTC tx (30d)</div><div class="kpi">{last30:,}</div><div class="caption">Rolling activity snapshot (illustrative).</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card"><div>🏦 CBDC projects in table</div><div class="kpi">{len(df_cbdc)}</div><div class="caption">Sample list; swap with BIS/IMF tracker.</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Inside the dashboard**")
    st.markdown("- 📈 Adoption curves & indexed view  \n- 💸 BTC vs SWIFT trends + fee savings  \n- 🧱 Tokenization scenarios  \n- ⚖️ Risk heatmap  \n- 🔭 CBDC filter")

# ---------- Adoption ----------
elif page == "📈 Adoption":
    st.header("📈 Adoption — Internet vs Blockchain")

    col1,col2 = st.columns(2)
    with col1:
        chart_inet = alt.Chart(df_internet).mark_area(opacity=0.7, color="#3b82f6").encode(
            x=alt.X("year:O", title="Year"), y=alt.Y("users_millions_est:Q", title="Users (M)"),
            tooltip=["year","users_millions_est"]
        ).properties(title="Internet adoption (est.)", height=320)
        st.altair_chart(chart_inet, use_container_width=True)
        st.caption("Internet users scaled on open standards (TCP/IP/HTTP), unlocking a layered innovation stack.")

    with col2:
        chart_bc = alt.Chart(df_blockchain).mark_area(opacity=0.8, color="#F7931A").encode(
            x=alt.X("year:O", title="Year"), y=alt.Y("users_millions_est:Q", title="Users (M)"),
            tooltip=["year","users_millions_est"]
        ).properties(title="Blockchain/Crypto adoption (est.)", height=320)
        st.altair_chart(chart_bc, use_container_width=True)
        st.caption("Blockchain growth shows early S‑curve traits as wallets, exchanges and L2s mature.")

    st.markdown("### Indexed adoption (start year = 100)")
    di = df_internet.copy(); db = df_blockchain.copy()
    di["index"] = 100*di["users_millions_est"]/di["users_millions_est"].iloc[0]
    db["index"] = 100*db["users_millions_est"]/db["users_millions_est"].iloc[0]
    di["series"]="Internet"; db["series"]="Blockchain"
    d = pd.concat([di[["year","index","series"]], db[["year","index","series"]]])
    chart_idx = alt.Chart(d).mark_line(point=True).encode(
        x="year:O", y=alt.Y("index:Q", title="Index (start=100)"),
        color=alt.Color("series:N", legend=alt.Legend(title="")),
        tooltip=["series","year","index"]
    ).properties(height=320)
    st.altair_chart(chart_idx, use_container_width=True)
    st.caption("Indexing normalizes scale and highlights **shape** similarities between eras.")

# ---------- Transactions & Costs ----------
elif page == "💸 Transactions & Costs":
    st.header("💸 Transactions & Costs")

    t = df_tx.copy().sort_values("date")
    t["btc_ma7"] = t["btc_daily_tx"].rolling(7).mean()
    t["swift_ma7"] = t["swift_daily_msgs"].rolling(7).mean()

    st.markdown("#### ₿ BTC transactions — daily vs 7‑day average")
    st.line_chart(t.set_index("date")[["btc_daily_tx","btc_ma7"]])
    st.caption("Daily BTC transactions are choppy; the MA7 smooths the line for trend spotting.")

    st.markdown("#### 📨 SWIFT messages — daily vs 7‑day average")
    st.line_chart(t.set_index("date")[["swift_daily_msgs","swift_ma7"]])
    st.caption("SWIFT runs at global banking scale. The chart frames **architecture differences** rather than absolute parity.")

    st.markdown("---")
    st.markdown("#### Remittance fee savings (illustrative)")
    amt = st.number_input("Transfer amount (USD)", min_value=100, step=100, value=1000)
    pick = st.selectbox("Corridor", df_fees["corridor"])
    row = df_fees[df_fees["corridor"] == pick].iloc[0]
    trad_cost = amt*(row["traditional_fee_pct"]/100); chain_cost = amt*(row["blockchain_fee_pct"]/100)
    st.success(f"Traditional ≈ **${trad_cost:,.2f}**  |  On‑chain ≈ **${chain_cost:,.2f}**  →  **Save ${trad_cost-chain_cost:,.2f}**")
    st.bar_chart(df_fees.set_index("corridor")[["traditional_fee_pct","blockchain_fee_pct"]])
    st.caption("Popular corridors can benefit most from lower fees and faster finality.")

# ---------- Tokenization ----------
elif page == "🧱 Tokenization":
    st.header("🧱 Tokenization — real‑world assets on‑chain")
    st.bar_chart(df_token.set_index("asset_class"))
    st.caption("Illustrative split of tokenized value by asset class.")

    st.markdown("### Scenario: 3‑year growth (what‑if)")
    g = st.slider("Growth over 3 years (%)", 0, 200, 60, step=5)
    proj = df_token.copy(); proj["projected"] = proj["tokenized_value_usd_bn_est"]*(1+g/100)
    st.markdown(f"**Projected total**: ${proj['projected'].sum():,.1f} bn")
    st.bar_chart(proj.set_index("asset_class")[["tokenized_value_usd_bn_est","projected"]])
    st.caption("Use scenario sliders to discuss upside/downside in stakeholder meetings.")

# ---------- Risks ----------
elif page == "⚖️ Risks":
    st.header("⚖️ Risks vs Opportunities")
    heat = df_risk.melt(id_vars="factor", var_name="dimension", value_name="score")
    heat = heat.replace({"opportunity_score":"Opportunity","risk_score":"Risk"})
    heat_chart = alt.Chart(heat).mark_rect().encode(
        x=alt.X("dimension:N", title=""),
        y=alt.Y("factor:N", sort="-x", title=""),
        color=alt.Color("score:Q", scale=alt.Scale(scheme="oranges")),
        tooltip=["factor","dimension","score"]
    ).properties(height=320)
    st.altair_chart(heat_chart, use_container_width=True)
    st.caption("Darker orange = higher score. Compare perceived opportunities vs risks factor‑by‑factor.")

# ---------- CBDC Outlook ----------
elif page == "🔭 CBDC Outlook":
    st.header("🔭 CBDC Outlook — sample tracker")
    status = st.multiselect("Filter by status", sorted(df_cbdc["status"].unique()), default=list(df_cbdc["status"].unique()))
    f = df_cbdc[df_cbdc["status"].isin(status)]
    colA,colB = st.columns(2)
    with colA: st.metric("Projects listed", len(f))
    with colB: st.metric("Unique countries", f["country"].nunique())
    st.dataframe(f, use_container_width=True)
    st.caption("Replace with official trackers (BIS/IMF/central banks) before publishing.")
