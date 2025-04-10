# ✈️ Flights Vitrina

Проект был реализован как тестовое задание.  
В задаче требовалось использовать данные с FlightRadar24 или аналогов, но большинство из них предоставляют данные только по подписке.  
Вместо этого был выбран бесплатный источник — [OpenSky Network](https://opensky-network.org), который позволяет получать данные о полётах в реальном времени.

❗ Обратите внимание: OpenSky **не предоставляет** информации о модели самолёта и авиакомпании, поэтому витрина построена **по странам происхождения самолётов**.

---

## 📚 Описание проекта

Скрипт для сбора, хранения и анализа данных о самолётах, пересекающих акваторию Чёрного моря.  
Используются: OpenSky API, PostgreSQL, Docker, Streamlit и Folium.

---

## 📁 Структура проекта

- `main.py` — собирает данные с OpenSky и сохраняет в PostgreSQL
- `vitrina.py` — формирует отчёт по странам за последний `час` или `день`
- `map.py` — строит карту траекторий по стране за последний час
- `map_app.py` — интерактивный Streamlit-дэшборд для отображения карт
- `clear_maps.py` — CLI-инструмент для удаления сохранённых HTML-карт
- `requirements.txt` — зависимости
- `Dockerfile` + `docker-compose.yml` — для развёртывания в контейнерах
- `.env.example` — пример настроек подключения к БД

---
## 🚀 Быстрый старт (без Docker)

### 1. Клонировать проект

```bash
git clone https://github.com/Andrey2904/flights_vitrina.git
cd flights_vitrina
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# или
source venv/bin/activate  # Linux/macOS
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить подключение к базе данных

Скопируйте  .env.example в .env:

```bash
copy .env.example .env  # Windows
# или
cp .env.example .env    # Linux/macOS
```

Заполните файл .env своими данными подключения к PostgreSQL:
```bash
DB_NAME=opensky
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 📥 Загрузка данных
Для загрузки данных о самолётах в PostgreSQL:

```bash
python main.py
```

### 📊 Построение витрины

Вывод количества самолётов по странам:

```bash
python vitrina.py hour
python vitrina.py day
```

### 🗺️ Построение карты (по стране за последний час)

```bash
python map.py 'Russian Federation'
```
HTML-карта будет сохранена в папке maps/ с меткой времени.

### 🌐 Интерактивный дашборд
```bash
streamlit run map_app.py

```
### 🧹 Очистка сохранённых карт
```bash
python clear_maps.py
```


### 🐳 Запуск через Docker

### 📦 Сборка
``` bash
docker-compose build

```

### 🔄 Загрузка данных
``` bash
docker-compose run --rm app python main.py

```

### 📈 Отчёт
``` bash
docker-compose run --rm app python vitrina.py hour

```
### 🗺️ Карта
``` bash
docker-compose run --rm app python map.py "Russian Federation"

```

### 🌍 Streamlit-дэшборд
``` bash
docker-compose run --rm -p 8501:8501 app streamlit run map_app.py
```



### 📄 Лицензия
Проект использует открытые данные OpenSky Network и создан в образовательных/тестовых целях.

https://github.com/openskynetwork/opensky-api