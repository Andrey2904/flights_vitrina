import sys
import psycopg2
import pandas as pd

# Проверка аргумента
if len(sys.argv) < 2 or sys.argv[1] not in ('hour', 'day'):
    print("⚠️ Укажи параметр при запуске: 'hour' или 'day'")
    print("Пример: python vitrina.py 'hour'")
    sys.exit(1)

period = sys.argv[1]

# SQL-запросы
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

conn = psycopg2.connect(
    dbname="opensky",
    user="postgres",
    password="Mto53609",
    host="localhost",  
    port="5432"
)


df = pd.read_sql(queries[period], conn)
print(f"\n📊 Кол-во рейсов по странам за последний {period.upper()}:")
print(df)

conn.close()
