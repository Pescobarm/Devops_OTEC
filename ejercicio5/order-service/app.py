from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, user_id INT, product_id INT);")
    cur.execute("SELECT * FROM orders;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (user_id, product_id) VALUES (%s, %s);", (user_id, product_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Orden registrada"}), 201
