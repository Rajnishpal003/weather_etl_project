# app.py
import streamlit as st
import pandas as pd

from weather import fetch_weather, insert_weather, fetch_all_weather

st.set_page_config(page_title="Weather ETL Dashboard", layout="centered")
st.title("🌤️ Weather ETL Dashboard")

st.markdown("Click the button below to fetch live weather data and store it in your Render PostgreSQL database.")

if st.button("🔁 Fetch New Weather Data"):
    try:
        city = "London"  # Can be dynamic if needed
        weather = fetch_weather(city)
        if weather:
            insert_weather(weather)
            st.success(f"✅ Weather data for {city} inserted.")
        else:
            st.error("❌ Failed to fetch weather data.")
    except Exception as e:
        st.error(f"❌ Error during data fetch/insert: {e}")

# Show graph from database
st.markdown("### 📊 Historical Weather Trends")

try:
    df = fetch_all_weather()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure it's datetime
        df = df.sort_values(by="timestamp")

        st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])
        st.dataframe(df.tail(10))  # optional
    else:
        st.warning("⚠️ No data available to display. Fetch some first.")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
