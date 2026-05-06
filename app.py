import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# Pobieranie sekretów z Environment Variables
DB_USER = os.getenv('DB_USER', 'Nieznany')
APP_SECRET = os.getenv('MY_APP_SECRET', 'Brak klucza!')

@app.route('/')
def hello():
    try:
        # Połączenie
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'database-secure'),
            database=os.getenv('DB_NAME', 'postgres'),
            user=DB_USER,
            password=os.getenv('DB_PASS', 'secret')
        )
        cur = conn.cursor()
        
        # Wyciąganie wersji bazy
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        
        # Wyciąganie danych z naszej nowej tabeli
        cur.execute('SELECT content FROM secrets;')
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Budowanie odpowiedzi HTML
        secrets_html = "".join([f"<li>{row[0]}</li>" for row in rows])
        
        return (f"<h1>Panel Administratora</h1>"
                f"<p><b>Zalogowany jako:</b> {DB_USER}</p>"
                f"<p><b>Klucz z Env:</b> {APP_SECRET}</p>"
                f"<hr>"
                f"<h3>Dane wyciągnięte z tabeli SQL:</h3>"
                f"<ul>{secrets_html}</ul>"
                f"<hr>"
                f"<small>Status bazy: {db_version}</small>")
    
    except Exception as e:
        return f"<h1>Błąd</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
