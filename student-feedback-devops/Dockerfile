FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \    apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .
RUN mkdir -p /data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
