from flask import Flask, request, jsonify
import redis
import os
import json

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)

@app.route('/products', methods=['GET'])
def get_products():
    keys = r.keys("product:*")
    products = [json.loads(r.get(k)) for k in keys]
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    r.set(f"product:{data['id']}", json.dumps(data))
    return jsonify({"message": "Producto creado"}), 201
