import requests
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")

print(f"🌍 API_KEY: {API_KEY}, CITY: {CITY}")  # <-- Debug print

DB_CONFIG = {
    "dbname": "weatherdb",
    "user": "rajnishpalsingh",          # <-- use the correct macOS DB user
    "password": "Rajnish123", # <-- use "" if no password set
    "host": "localhost",
    "port": "5432"
}

def fetch_weather():
    print("🌤️ Fetching weather data...")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        print("❌ Failed to fetch data:", res.status_code, res.text)
        return None
    data = res.json()
    return {
        "city": CITY,
        "temperature": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "description": data['weather'][0]['description']
    }

def insert_weather(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Connected to PostgreSQL")
        cur.execute("""
            INSERT INTO weather_data (city, temperature, humidity, description)
            VALUES (%s, %s, %s, %s)
        """, (data['city'], data['temperature'], data['humidity'], data['description']))
        conn.commit()
        print("✅ Data inserted successfully")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error inserting data:", e)

if __name__ == "__main__":
    weather = fetch_weather()
    if weather:
        print("✅ Weather fetched:", weather)
        insert_weather(weather)

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    return {
        "city": city,
        "temperature": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "description": data['weather'][0]['description']
    }

def insert_weather(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_data (city, temperature, humidity, description)
        VALUES (%s, %s, %s, %s)
    """, (data['city'], data['temperature'], data['humidity'], data['description']))
    conn.commit()
    cur.close()
    conn.close()
