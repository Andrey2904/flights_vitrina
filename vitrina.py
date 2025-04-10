import sys
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

if len(sys.argv) < 2 or sys.argv[1] not in ('hour', 'day'):
    print("⚠️ Укажи параметр при запуске: 'hour' или 'day'")
    print("Пример: python vitrina.py 'hour'")
    sys.exit(1)

period = sys.argv[1]

queries = {
    "hour": """
        SELECT country, COUNT(*) AS flight_count
        FROM flights
        WHERE timestamp >= NOW() - INTERVAL '1 hour'
        GROUP BY country
        ORDER BY flight_count DESC;
    """,
    "day": """
        SELECT country, COUNT(*) AS flight_count
        FROM flights
        WHERE timestamp >= NOW() - INTERVAL '1 day'
        GROUP BY country
        ORDER BY flight_count DESC;
    """
}

print("Подключаюсь к БД:")
print(f"{os.getenv('DB_USER')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "opensky"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)


df = pd.read_sql(queries[period], conn)
print(f"\n📊 Кол-во рейсов по странам за последний {period.upper()}:")
print(df)

conn.close()
