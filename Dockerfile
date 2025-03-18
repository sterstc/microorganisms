FROM python:3.10.12-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY models /app/models
COPY api /app/api
COPY flask_app.py /app/flask_app.py
COPY templates /app/templates
COPY static /app/static

EXPOSE 8000

CMD uvicorn api.app:app --host 0.0.0.0 --port $PORT
