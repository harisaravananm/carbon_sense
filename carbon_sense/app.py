# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from forecast import forecast_energy
from emissions import estimate_emissions
from streamlit_autorefresh import st_autorefresh

# Refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="datarefresh")

# --- App Title ---
st.title("⚡ CarbonSense: Energy & Emission Forecasting")
st.subheader("AI-powered forecast for energy usage and carbon emissions")

# --- Load data ---
data_path = "carbon_sense/energy.csv"

def load_recent_energy_data(filepath, hours_back=48):
    try:
        df = pd.read_csv(filepath)
        df['ds'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['ds', 'energy_kwh'])  # Remove bad rows
        df['y'] = df['energy_kwh']
        now = df['ds'].max()
        df = df[df['ds'] >= now - pd.Timedelta(hours=hours_back)]
        if df.shape[0] < 2:
            raise ValueError("Not enough data to forecast.")
        return df[['ds', 'y']]
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        return pd.DataFrame(columns=['ds', 'y'])

# Load recent data
df = load_recent_energy_data(data_path)

if df.empty:
    st.warning("Not enough recent data to forecast. Please wait for more data to accumulate.")
else:
    forecast = forecast_energy(df)

    # --- Display energy forecast ---
    st.write("### 🔮 Forecasted Energy Usage (next 48 hours)")
    fig, ax = plt.subplots()
    ax.plot(forecast['ds'], forecast['yhat'], label='Forecast (kWh)')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3)
    ax.set_xlabel("Time")
    ax.set_ylabel("Energy (kWh)")
    ax.set_title("Forecasted Energy Usage with Confidence Interval")
    ax.legend(loc='upper left', framealpha=0.8)
    ax.grid(True, linestyle='--', alpha=0.6)

    # Format x-axis dates with 12-hour AM/PM format
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I %p'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    # --- Emission estimation ---
    st.write("### 🌍 Estimated CO₂ Emissions")
    source = st.selectbox("Select energy source", ["grid", "solar", "wind", "coal"])

    forecast['co2_emissions_kg'] = forecast['yhat'].apply(lambda x: estimate_emissions(x, source))
    total_emissions = forecast['co2_emissions_kg'].sum()

    st.metric("Estimated total CO₂ emissions (next 48h)", f"{total_emissions:.2f} kg")


