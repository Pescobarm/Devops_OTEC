from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);")
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s);", (data["name"],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuario creado"}), 201
