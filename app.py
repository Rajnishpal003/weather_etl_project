import streamlit as st
import pandas as pd
import requests
import psycopg2
from datetime import datetime
import os

# Streamlit config
st.set_page_config(page_title="Weather ETL Dashboard", layout="centered")
st.title("🌦️ Weather ETL Dashboard")

# ENV VARS for production/deployment
API_KEY = os.getenv("API_KEY")  # from OpenWeather
CITY = os.getenv("CITY", "London")  # Default

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# --- Weather fetcher ---
def fetch_weather(city):
    try:
        st.write(f"🌤️ Fetching weather for **{city}**...")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timestamp": datetime.now()
        }
    except Exception as e:
        st.error(f"❌ Failed to fetch weather: {e}")
        return None

# --- Insert to Render DB ---
def insert_weather(data):
    try:
        st.write(f"⏳ Inserting data into DB: {data}")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather_data (city, temperature, humidity, description, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['city'], data['temperature'], data['humidity'], data['description'], data['timestamp']))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"✅ Weather data for {data['city']} inserted.")
    except Exception as e:
        st.error(f"❌ DB Insert Error: {e}")

# --- Fetch from Render DB ---
def fetch_all_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT city, temperature, humidity, description, timestamp
            FROM weather_data
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        df = pd.DataFrame(rows, columns=["City", "Temperature (°C)", "Humidity (%)", "Description", "Timestamp"])
        return df.sort_values("Timestamp")
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return pd.DataFrame()

# --- UI ---
if st.button("📥 Fetch Weather Data"):
    weather = fetch_weather(CITY)
    if weather:
        insert_weather(weather)

st.subheader("📊 Historical Weather Trends")
data = fetch_all_data()

if not data.empty:
    st.line_chart(data.set_index("Timestamp")[["Temperature (°C)", "Humidity (%)"]])
    st.dataframe(data)
else:
    st.warning("⚠️ No data available to display. Fetch some first.")
