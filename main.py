from opensky_api import OpenSkyApi
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os



load_dotenv()

bbox = (41.0, 47.5, 27.0, 41.5)


api = OpenSkyApi()
states = api.get_states(bbox=bbox)
date = datetime.now()

data = []
for s in states.states:
    icao24 = s.icao24.lower()
    callsign = s.callsign.strip() if s.callsign else ''
    origin_country = s.origin_country
    data.append((
        icao24, callsign, origin_country, date
    ))


conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "opensky"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    icao24 TEXT,
    callsign TEXT,
    country TEXT,
    timestamp TIMESTAMP
)
""")


execute_values(cursor, """
    INSERT INTO flights (
        icao24, callsign, country, timestamp
    ) VALUES %s
""", data)

conn.commit()
cursor.close()
conn.close()
print("✅ Данные успешно записаны в PostgreSQL")
