FROM python:3.10.12-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY models /app/models
COPY api /app/api

EXPOSE 8000

CMD uvicorn --reload api.app:app --host 0.0.0.0 --port $PORT
