FROM apache/airflow:2.9.0-python3.10


USER root

# Устанавливаем системные зависимости, если нужно (например, для pandas/numpy/scipy)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libatlas-base-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY --chown=airflow:airflow requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
