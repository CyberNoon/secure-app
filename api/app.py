# api/app.py
import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'database-secure')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'secret')
APP_SECRET = os.getenv('MY_APP_SECRET', 'Brak klucza!')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def hello():
    try:
        # Próba połączenia z odizolowaną bazą PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        
        # Wyciąganie wersji bazy i danych z tabeli
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        
        cur.execute('SELECT content FROM secrets;')
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
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
        return f"<h1>Panel Administratora (Błąd Bazy)</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
