from opensky_api import OpenSkyApi
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

# Прямоугольник над Чёрным морем
bbox = (41.0, 47.5, 27.0, 41.5)

# Получаем данные
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

# Подключение к БД
conn = psycopg2.connect(
    dbname="opensky",
    user="postgres",
    password="Mto53609",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Создание таблицы, если нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    icao24 TEXT,
    callsign TEXT,
    country TEXT,
    timestamp TIMESTAMP
)
""")

# Вставка данных
execute_values(cursor, """
    INSERT INTO flights (
        icao24, callsign, country, timestamp
    ) VALUES %s
""", data)

conn.commit()
cursor.close()
conn.close()
print("✅ Данные успешно записаны в PostgreSQL")
