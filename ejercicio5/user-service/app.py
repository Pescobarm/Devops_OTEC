from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/users')
def users():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO users (name) VALUES ('Alice');")
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)
