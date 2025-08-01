import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get DB URL from environment
DB_URL = os.getenv("DB_URL")

# Define SQL for creating the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    description TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
"""

# Create the table
engine = create_engine(DB_URL)

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    print("✅ Table 'weather_data' created or already exists.")
