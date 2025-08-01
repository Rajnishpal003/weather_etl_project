import os
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get config from .env
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
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
        "description": data['weather'][0]['description']
    }

def insert_weather(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather_data (city, temperature, humidity, description)
            VALUES (%s, %s, %s, %s)
        """, (data['city'], data['temperature'], data['humidity'], data['description']))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Data inserted successfully.")
    except Exception as e:
        print("❌ Error inserting data:", e)

# Optional: Script mode (for testing locally)
if __name__ == "__main__":
    test_city = os.getenv("CITY", "London")
    weather = fetch_weather(test_city)
    if weather:
        insert_weather(weather)
