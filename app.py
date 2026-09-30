import streamlit as st
import pandas as pd
import numpy as np

# Page Layout Configuration
st.set_page_config(
    page_title="Maritime Weather & Risk Intelligence",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 AI-Powered Maritime Risk Intelligence Dashboard")
st.markdown("Real-time weather risk assessment and port approach monitoring for global bulk shipping corridors.")

# Load the AI predictions dataset safely
@st.cache_data
def load_data():
    try:
        return pd.read_csv("bay_of_bengal_risk_predictions.csv")
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Prediction data not found! Please run your `train_model.py` script first.")
else:
    # --- TOP METRICS ROW ---
    col1, col2, col3, col4 = st.columns(4)
    
    avg_risk = df['predicted_risk_score'].mean()
    max_risk = df['predicted_risk_score'].max()
    high_risk_count = len(df[df['predicted_risk_score'] > 50])
    max_wave = df['swh'].max()

    col1.metric("Average Corridor Risk", f"{avg_risk:.1f} / 100")
    col2.metric("Peak Risk Score", f"{max_risk:.1f} / 100")
    col3.metric("High-Risk Grid Zones", f"{high_risk_count} zones")
    col4.metric("Max Wave Height Recorded", f"{max_wave:.2f} m")

    st.markdown("---")

    # --- PORT RISK ALERTS SECTION ---
    st.subheader("🚨 Port Approach Weather Alerts")
    
    target_ports = {
        "Paradip": (20.26, 86.68),
        "Vizag": (17.68, 83.21),
        "Gangavaram": (17.59, 83.25),
        "Haldia": (22.03, 88.06),
        "Dhamra": (21.08, 86.97),
        "Gopalpur": (19.26, 84.90),
    }

    alert_cols = st.columns(3)
    idx = 0

    for port_name, (port_lat, port_lon) in target_ports.items():
        nearby = df[
            (df['latitude'].between(port_lat - 1.0, port_lat + 1.0)) & 
            (df['longitude'].between(port_lon - 1.0, port_lon + 1.0))
        ]
        
        with alert_cols[idx % 3]:
            if not nearby.empty:
                p_risk = nearby['predicted_risk_score'].mean()
                p_wave = nearby['swh'].max()
                p_wind = nearby['wind_speed'].max()

                if p_risk >= 50.0:
                    st.error(f"**🔴 {port_name} Port**\n\n* **Risk:** {p_risk:.1f}/100\n* **Waves:** {p_wave:.2f}m\n* **Wind:** {p_wind:.1f} m/s\n* **Status:** High Hazard Warning")
                else:
                    st.success(f"**🟢 {port_name} Port**\n\n* **Risk:** {p_risk:.1f}/100\n* **Waves:** {p_wave:.2f}m\n* **Wind:** {p_wind:.1f} m/s\n* **Status:** Clear Conditions")
            else:
                st.info(f"**🔵 {port_name} Port**\n\nNo active telemetry data mapped.")
        idx += 1

    st.markdown("---")

    # --- DATA TABLE EXPLORER ---
    st.subheader("📊 Live AI Prediction Telemetry Table")
    st.markdown("Filter or search through all coordinates, environmental parameters, and AI-calculated risk scores.")
    
    # Search/Filter UI options
    risk_filter = st.slider("Filter by Minimum Risk Score", 0.0, 100.0, 0.0)
    filtered_df = df[df['predicted_risk_score'] >= risk_filter]

    st.dataframe(
        filtered_df[['valid_time', 'latitude', 'longitude', 'wind_speed', 'msl', 'sst', 'swh', 'predicted_risk_score']],
        use_container_width=True
    )