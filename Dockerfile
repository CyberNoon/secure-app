# 1. Obraz bazowy - gotowy Python
FROM python:3.11-slim

# 2. Folder wewnątrz kontenera, w którym będziemy pracować
WORKDIR /app

# 3. Kopiujemy plik z listą bibliotek
COPY requirements.txt .

# 4. Instalujemy biblioteki
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiujemy całą resztę kodu z Twojego komputera do kontenera
COPY . .

# 6. Komenda startowa
CMD ["python", "-u", "app.py"]
