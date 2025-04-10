FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY main.py /app/main.py
COPY vitrina.py /app/vitrina.py
COPY map.py /app/map.py
COPY map_app.py /app/map_app.py
COPY .env.example /app/.env.example
COPY clear_maps.py /app/clear_maps.py

WORKDIR /app
EXPOSE 8501


CMD ["python", "main.py"]
