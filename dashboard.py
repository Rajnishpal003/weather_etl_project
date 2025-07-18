import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine


# City options
CITIES = ["London", "New York", "Delhi", "Tokyo", "Berlin", "Mumbai", "Paris"]

# Select a city from dropdown
selected_city = st.selectbox("🌍 Select City", CITIES, index=0)

# DB config
DB_CONFIG = {
    "dbname": "weatherdb",
    "user": "rajnishpalsingh",
    "password": "Rajnish123",
    "host": "localhost",
    "port": "5432"
}


# Load data
def load_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()
    return df

# App UI
st.set_page_config(page_title="🌦️ Weather Dashboard", layout="wide")
st.title("🌤️ Real-Time Weather Dashboard")

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

df = load_data()

if df.empty:
    st.warning("No weather data available yet.")
else:
    # Display summary cards
    latest = df.iloc[0]
    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temperature (°C)", f"{latest['temperature']}°")
    col2.metric("💧 Humidity (%)", f"{latest['humidity']}%")
    col3.metric("🌥️ Condition", latest['description'].capitalize())

    st.markdown("---")

    # Hide ID column
    df_view = df.drop(columns=["id"])

    # Display table and charts
    st.subheader("📋 Recent Weather Records")
    st.dataframe(df_view, use_container_width=True)

    st.subheader("📈 Temperature Over Time")
    st.line_chart(df.set_index("timestamp")["temperature"])

    st.subheader("💧 Humidity Over Time")
    st.bar_chart(df.set_index("timestamp")["humidity"])

# Fetch new weather

if st.button("🔁 Fetch New Weather Data"):
    from weather_etl import fetch_weather, insert_weather
    data = fetch_weather(selected_city)
    if data:
        insert_weather(data)
        st.success("✅ New data inserted for " + selected_city)
        st.rerun()



def load_data(city):
    engine = create_engine(f"postgresql+psycopg2://rajnishpalsingh:Rajnish123@localhost:5432/weatherdb")
    query = f"SELECT * FROM weather_data WHERE city = '{city}' ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, engine)
    return df
