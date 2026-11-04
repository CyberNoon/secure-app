# api/Dockerfile
FROM python:3.11-slim

WORKDIR /app


RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# Najpierw kopiujemy i instalujemy zależności (wykorzystanie cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu i zmiana uprawnień na nie-root użytkownika ze względów bezpieczeństwa
RUN useradd -m -r -s /bin/false apiuser
COPY --chown=apiuser:apiuser . .

USER apiuser
EXPOSE 5000

CMD ["python", "-u", "app.py"]
