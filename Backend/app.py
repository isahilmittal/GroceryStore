from flask import Flask, jsonify, request, send_from_directory
from sql_connection import sql_connection
import query
import os
from flask_cors import CORS

UI_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Ui'))

app = Flask(__name__, static_folder=UI_FOLDER, static_url_path='/ui')
CORS(app)

# Serve index.html
@app.route('/')
def home():
    return send_from_directory(UI_FOLDER, "index.html")

# Serve static files (CSS, JS, images)
@app.route('/ui/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(UI_FOLDER, filename)

@app.route('/')
def products():
    return send_from_directory(UI_FOLDER, "products.html")

@app.route('/')
def dashboard():
    return send_from_directory(UI_FOLDER, "dashboard.html")


# Fetch all products
@app.route('/products', methods=['GET'])
def fetch_products():
    connection = sql_connection()
    products = query.get_products(connection) 
    connection.close()
    return jsonify(products), 200

# Products on home

@app.route('/products_home', methods=['GET'])
def fetch_products_home():
    connection = sql_connection()
    products = query.get_products_home(connection) 
    connection.close()
    return jsonify(products), 200


# Add a new product
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    product_name = data.get("product_name")
    unit = data.get("unit")
    price = data.get("price")

    if not (product_name and unit and price):
        return jsonify({"error": "Missing fields"}), 400

    connection = sql_connection()
    response = query.add_product(connection, product_name, unit, price)
    connection.close()
    
    return jsonify(response), 201

# Fetch Store name
@app.route('/get_store_name', methods=['GET'])
def fetch_store_name():
    connection = sql_connection()
    seller = query.get_store_name(connection)
    connection.close()
    return jsonify(seller),200


@app.route('/monthlyrevenue', methods=['GET'])
def fetch_monthly_revenue():
    connection = sql_connection()
    revenue = query.fetch_monthly_revenue(connection)
    connection.close()
    return jsonify(revenue),200




# Fetch order history
@app.route('/orderss', methods=['GET'])
def get_orders():
    connection = sql_connection()
    orders = query.get_orders(connection)
    connection.close()
    
    return jsonify(orders)

@app.route("/orders", methods=["GET"])
def fetch_orders():
    try:
        orders = get_orders()  # Fetch orders from the database
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
