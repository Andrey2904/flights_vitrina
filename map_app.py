import streamlit as st
import os

st.set_page_config(page_title="Карта полётов", layout="wide")
st.title("🌍 Визуализация траекторий самолётов")


map_dir = "maps"
maps = [f for f in os.listdir(map_dir) if f.endswith(".html")]

if not maps:
    st.warning("❗ Пока нет готовых карт. Сначала сгенерируй карту через map.py.")
else:
    selected = st.selectbox("Выбери карту по стране:", sorted(maps, reverse=True))
    st.subheader(f"Карта: {selected}")
    
    with open(os.path.join(map_dir, selected), "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(html, height=650, scrolling=True)
