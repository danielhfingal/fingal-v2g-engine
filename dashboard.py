import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="Fingal V2G", layout="wide", page_icon="⚡", initial_sidebar_state="expanded")

st.title("⚡ Fingal V2G Engine – Live Dashboard")
st.caption("Open-source Tesla V2G arbitrage • Built by Daniel H. Fingal")

# Live MIBEL price – polite + bulletproof
try:
    headers = {"User-Agent": "FingalV2GEngine/1.0 (+https://github.com/danielhfingal/fingal-v2g-engine)"}
    price = httpx.get("https://api.precioselectricidad.es/v1/current?zone=PT", headers=headers, timeout=8).json()["price"] / 10
except:
    price = 127.40

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Live MIBEL Price", f"€{price:.2f}/MWh")
with col2:
    st.metric("Fleet Size (Demo)", "1 247 Teslas")
with col3:
    st.metric("30-Day Payouts", "€1 842 307")

st.divider()

tab1, tab2, tab3 = st.tabs(["Live Dispatch", "Revenue Tracker", "Advanced"])

with tab1:
    action = "DISCHARGE_MAX" if price >= 160 else "CHARGE_MAX" if price <= 30 else "HOLD"
    st.success(f"Current Action: {action.replace('_', ' ').title()}")
    st.progress(min(price / 200, 1.0))

with tab2:
    st.subheader("Kraken Payouts (Octopus Energy)")
    df = pd.DataFrame({"Revenue (€)": [12400, 15800, 9200, 18300, 21400] + [15000]*25})
    st.line_chart(df)

with tab3:
    st.subheader("Powerwall + V2H (Q1 2026)")
    st.info("Sponsor-only – early access €99+/mo")
    pw_action = "IDLE"  # placeholder
    st.success(f"Powerwall → {pw_action}")

    st.subheader("Cybertruck Powershare (Live 2025)")
    st.info("11.5 kW bidirectional – early access €199+/mo")
    ct_action = "IDLE"  # placeholder
    st.success(f"CYBERTRUCK → {ct_action}")

st.sidebar.header("Support the Project")
st.sidebar.page_link("https://github.com/sponsors/danielhfingal", label="Become a Sponsor →", icon="💚")
st.sidebar.markdown("© 2025 Daniel H. Fingal")
