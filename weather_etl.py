import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load .env
load_dotenv()

# Config from .env
API_KEY = os.getenv("API_KEY")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Fetch weather from API
def fetch_weather(city):
    print(f"🌤️ Fetching weather for {city}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

# Insert weather into DB
def insert_weather(data):
    try:
        print(f"⏳ Inserting: {data}")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather_data (city, temperature, humidity, description, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['city'],
            data['temperature'],
            data['humidity'],
            data['description'],
            data['timestamp']
        ))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Data inserted successfully.")
    except Exception as e:
        print(f"❌ DB Insert Error: {e}")

# Run manually
if __name__ == "__main__":
    city = os.getenv("CITY", "London")
    data = fetch_weather(city)
    if data:
        insert_weather(data)
