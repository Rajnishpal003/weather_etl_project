import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get DB URL (should be full Render DB URL)
DB_URL = os.getenv("DB_URL")

# Set Streamlit page config
st.set_page_config(page_title="🌦️ Weather Dashboard", layout="wide")
st.title("🌤️ Real-Time Weather Dashboard")

# Styling
st.markdown("""
<style>
h1 {
    text-align: center;
    font-size: 48px;
    color: #2E86AB;
}
.css-18e3th9 {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# City selector
CITIES = ["London", "New York", "Delhi", "Tokyo", "Berlin", "Mumbai", "Paris"]
selected_city = st.selectbox("🌍 Select City", CITIES, index=0)

# Load data from DB
def load_data(city):
    try:
        engine = create_engine(DB_URL)
        query = """
        SELECT * FROM weather_data
        WHERE city = %s
        ORDER BY timestamp DESC
        LIMIT 100
        """
        df = pd.read_sql(query, engine, params=(city,))
        return df
    except Exception as e:
        st.error(f"❌ Failed to fetch data from DB: {e}")
        return pd.DataFrame()

# Fetch weather data
df = load_data(selected_city)

if df.empty:
    st.warning("No weather data available for this city yet.")
else:
    latest = df.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature (°C)", f"{latest['temperature']}°")
    col2.metric("💧 Humidity (%)", f"{latest['humidity']}%")
    col3.metric("🌥️ Condition", latest['description'].capitalize())

    st.markdown("---")

    df_view = df.drop(columns=["id"])

    st.subheader("📋 Recent Weather Records")
    st.dataframe(df_view, use_container_width=True)

    st.subheader("📈 Temperature Over Time")
    st.line_chart(df.set_index("timestamp")["temperature"])

    st.subheader("💧 Humidity Over Time")
    st.bar_chart(df.set_index("timestamp")["humidity"])

# Insert new weather data
if st.button("🔁 Fetch New Weather Data"):
    try:
        from weather import fetch_weather, insert_weather
        data = fetch_weather(selected_city)
        if data:
            insert_weather(data)
            st.success(f"✅ New weather data inserted for {selected_city}")
            st.rerun()
        else:
            st.error("❌ Failed to fetch weather data.")
    except Exception as e:
        st.error(f"❌ Error during data fetch/insert: {e}")
