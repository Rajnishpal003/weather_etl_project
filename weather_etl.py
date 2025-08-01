import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env (for local dev only)
load_dotenv()

# Get config from environment
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def fetch_weather(city):
    print(f"🌤️ Fetching weather for {city}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code != 200:
        print(f"❌ Failed to fetch data: {res.status_code} - {res.text}")
        return None

    data = res.json()
    return {
        "city": city,
        "temperature": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "description": data['weather'][0]['description'],
        "timestamp": datetime.utcnow()  # include timestamp for accurate insertion
    }

def insert_weather(data):
    print("⏳ Inserting:", data)
    try:
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
        print("❌ DB Insert Error:", e)

# Run manually for testing
if __name__ == "__main__":
    test_city = os.getenv("CITY", "London")
    weather = fetch_weather(test_city)
    if weather:
        insert_weather(weather)
