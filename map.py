import sys
import os
import psycopg2
from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import folium
import hashlib
from dotenv import load_dotenv

load_dotenv()

def get_color_from_icao(icao24):
    hash_val = hashlib.md5(icao24.encode()).hexdigest()
    return f"#{hash_val[:6]}"

if len(sys.argv) < 2:
    print("❗ Укажи страну как аргумент, например: python map.py 'Russian Federation'")
    sys.exit(1)

country = sys.argv[1]


conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "opensky"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
)
cursor = conn.cursor()


cursor.execute("""
    SELECT DISTINCT icao24 
    FROM flights 
    WHERE country = %s AND timestamp >= NOW() - INTERVAL '1 hour'
""", (country,))
icao_list = [row[0] for row in cursor.fetchall()]

if not icao_list:
    print("⚠️ Нет актуальных самолётов за последний час по стране:", country)
    sys.exit(0)

m = folium.Map(location=[45.0, 35.0], zoom_start=5)
api = OpenSkyApi()

for icao in icao_list:
    print(f"📡 Обрабатывается: {icao}")
    try:
        flight_track = api.get_track_by_aircraft(icao, 0)
        if flight_track and flight_track.path:
            route = [(wp[1], wp[2]) for wp in flight_track.path if wp[1] and wp[2]]
            if len(route) >= 2:
                color = get_color_from_icao(icao)
                folium.PolyLine(route, color=color, weight=2.5, opacity=1, tooltip=icao).add_to(m)
                folium.Marker(route[0], popup=f"Начало {icao}", icon=folium.Icon(color="blue")).add_to(m)
                folium.Marker(route[-1], popup=f"Конец {icao}", icon=folium.Icon(color="red")).add_to(m)
    except Exception as e:
        print(f"❌ Ошибка при обработке {icao}: {e}")


os.makedirs("maps", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"flight_routes_{country.lower().replace(' ', '_')}_{timestamp}.html"
output_file = os.path.join("maps", filename)
m.save(output_file)

print(f"✅ Карта сохранена: {output_file}")