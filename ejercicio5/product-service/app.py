from flask import Flask, jsonify
import redis
import os
import json

app = Flask(__name__)

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)

@app.route('/products')
def products():
    if r.exists("products"):
        return jsonify({"fuente": "cache", "data": json.loads(r.get("products"))})
    
    productos = [{"id": 1, "nombre": "Laptop"}, {"id": 2, "nombre": "Teclado"}]
    r.set("products", json.dumps(productos), ex=30)
    return jsonify({"fuente": "servidor", "data": productos})
