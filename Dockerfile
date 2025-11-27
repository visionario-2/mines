FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD ["bash", "-lc", "python bot_worker.py & uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
