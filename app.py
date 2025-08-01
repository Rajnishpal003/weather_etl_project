import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Database URL for SQLAlchemy
DB_URL = os.getenv("DB_URL")

# City options
CITIES = ["London", "New York", "Delhi", "Tokyo", "Berlin", "Mumbai", "Paris"]
selected_city = st.selectbox("🌍 Select City", CITIES, index=0)

# Streamlit page config
st.set_page_config(page_title="🌦️ Weather Dashboard", layout="wide")
st.title("🌤️ Real-Time Weather Dashboard")

# Load data
def load_data(city):
    try:
        engine = create_engine(DB_URL)
        query = "SELECT * FROM weather_data WHERE city = %s ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql(query, engine, params=(city,))
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

# Render UI
df = load_data(selected_city)

if df.empty:
    st.warning("No weather data available for this city.")
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

# Fetch new weather data
if st.button("🔁 Fetch New Weather Data"):
    from weather_etl import fetch_weather, insert_weather
    data = fetch_weather(selected_city)
    st.write("📦 New data fetched:", data)
    if data:
        insert_weather(data)
        st.success("✅ New data inserted successfully!")
        st.rerun()
    else:
        st.error("⚠️ Failed to fetch new data.")

# Optional: DB health check
try:
    import psycopg2
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM weather_data")
    count = cur.fetchone()[0]
    st.info(f"🗃️ Total records in weather_data: {count}")
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"❌ Could not connect to DB: {e}")
