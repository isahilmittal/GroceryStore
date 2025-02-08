
from sql_connection import sql_connection

# Function to get all products
def get_products(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []
    

def get_products_home(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

def get_store_name(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT store_name, owner_name FROM sellers")
        store_name = cursor.fetchone()
        cursor.close()
        return store_name
    except Exception as e:
        print(f"Error fetching Stoere Name: {e}")
        return {}
    
def fetch_monthly_revenue(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM orders WHERE MONTH(date_time) = MONTH(CURDATE())")
        mrevenue = cursor.fetchall() # Access the first element of the tuple
        cursor.close()
        return mrevenue 
    except Exception as e:
        print(f"Error fetching monthly revenue: {e}")
        return 0

    

# Function to add a new product
def add_product(connection, product_name, unit, price):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO products (product_name, Unit, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, unit, price))
        connection.commit()
        cursor.close()
        return {"message": "Product added successfully"}
    except Exception as e:
        print(f"Error adding product: {e}")
        return {"error": str(e)}

# Function to update product price
def update_product_price(connection, product_id, new_price):
    try:
        cursor = connection.cursor()
        query = "UPDATE products SET price = %s WHERE product_id = %s"
        cursor.execute(query, (new_price, product_id))
        connection.commit()
        cursor.close()
        return {"message": "Price updated successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Function to delete a product
def delete_product(connection, product_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()
        cursor.close()
        return {"message": "Product deleted successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Function to get seller details
def get_seller_details(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT store_name, owner_name, email, phone, address FROM sellers LIMIT 1"
        cursor.execute(query)
        seller = cursor.fetchone()
        cursor.close()
        return seller
    except Exception as e:
        print(f"Error fetching seller details: {e}")
        return {}

# Function to get order history


def get_orders(connection):
    try:
        cursor = connection.cursor()
        query = 'SELECT order_id, amount, customer_name, date_time FROM orders ORDER BY order_id DESC LIMIT 10'
        cursor.execute(query)
        orders = [
            {"order_id": row[0], "amount": row[1], "customer_name": row[2], "date_time": row[3]}
            for row in cursor.fetchall()
            
        ]
        return orders
        
    except Exception as e:
        print(f"Error fetching order history: {e}")
        return {}
    
    cursor.close()






def search_products(query,connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT product_id, product_name, price FROM products WHERE product_name LIKE %s", ("%" + query + "%",))
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_order(customer_name, products, total_amount,connection):
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO orders (customer_name, amount, date_time) VALUES (%s, %s, NOW())", (customer_name, total_amount))
    order_id = cursor.lastrowid
    
    for product in products:
        cursor.execute("INSERT INTO orders_details (order_id, product_id, quantity, amount) VALUES (%s, %s, %s, %s)",
                       (order_id, product['product_id'], product['quantity'], product['amount']))
    
    cursor.commit()
    cursor.close()
    return order_id



