from flask import Flask
import psycopg2
import redis
import os
import json

app = Flask(__name__)

# Variables de entorno
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Conexiones
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def index():
    return "Flask + PostgreSQL + Redis App en Docker"

@app.route("/visitas")
def visitas():
    if r.exists("visitas"):
        visitas = json.loads(r.get("visitas"))
        return {"fuente": "redis (cache)", "visitas": visitas}

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visitas (id SERIAL PRIMARY KEY);")
    cur.execute("INSERT INTO visitas DEFAULT VALUES;")
    cur.execute("SELECT COUNT(*) FROM visitas;")
    visitas = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    r.set("visitas", json.dumps(visitas), ex=10)  # Cachea por 10 segundos

    return {"fuente": "postgresql (db)", "visitas": visitas}
