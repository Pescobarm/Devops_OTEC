from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "testdb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def index():
    return "¡Web App con Flask y PostgreSQL en Docker!"

@app.route('/crear', methods=['POST'])
def crear():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visitas (id SERIAL PRIMARY KEY, mensaje TEXT);")
    cur.execute("INSERT INTO visitas (mensaje) VALUES ('Hola desde Flask!');")
    conn.commit()
    cur.close()
    conn.close()
    return "Registro insertado"

@app.route('/ver')
def ver():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM visitas;")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return {"resultados": filas}
