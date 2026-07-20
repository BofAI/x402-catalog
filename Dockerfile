FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt
COPY providers/ ./providers/
COPY scripts/ ./scripts/
COPY schemas/ ./schemas/

RUN python3 scripts/validate.py \
    && python3 scripts/build.py \
    && mkdir -p /app/public \
    && mv /app/dist /app/public/api \
    && chown -R nobody:nogroup /app/public

USER nobody

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/status.json', timeout=3).read()" || exit 1

CMD ["python3", "scripts/serve.py", "--host", "0.0.0.0", "--port", "8080", "--directory", "/app/public"]
