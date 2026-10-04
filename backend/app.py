from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_db_connection, init_db
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Smart Restaurant API is running"
    })


@app.route("/api/menu", methods=["GET"])
def get_menu():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu")

    menu = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(menu)


@app.route("/api/order", methods=["POST"])
def place_order():

    data = request.get_json()

    customer_name = data.get("customer_name")
    items = data.get("items")
    total = data.get("total")

    if not customer_name or not items or total is None:
        return jsonify({
            "error": "Missing order information"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders
        (customer_name, items, total)
        VALUES (%s, %s, %s)
        """,
        (
            customer_name,
            json.dumps(items),
            total
        )
    )

    conn.commit()

    order_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order_id
    }), 201


@app.route("/api/orders", methods=["GET"])
def get_orders():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )