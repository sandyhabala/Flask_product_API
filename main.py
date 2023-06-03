import os
import json
from flask import Flask, request, session, Response
from dotenv import load_dotenv
from flask_mysqldb import MySQL


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Initialize MySQL
mysql = MySQL(app)

# Add Product to Database
@app.route("/addProduct", methods=['POST'])
def addProduct():
    try:
        # Extract data from the request
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'description' not in data or 'category' not in data:
            return Response(json.dumps({'error': 'Invalid request data'}), mimetype="application/json", status=400)

        # Check if all required fields are provided
        name = data['name']
        price = data['price']
        description = data['description']
        category = data['category']

        if not name or not price or not description or not category:
            return Response(json.dumps({'error': 'Please fill up all fields'}), mimetype="application/json", status=400)

        # Insert the new product into the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (name, price, description, category) VALUES (%s, %s,%s, %s)", 
                        (name, price, description, category))
        cursor.connection.commit()
        cursor.close()

        return Response(json.dumps({'message': 'Product created successfully'}), mimetype="application/json", status=201)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json", status=400)


# Get All Products from Database
@app.route("/products", methods=['GET'])
def products():
    try:
        # Fetch all products from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        
        # Check if there are no products available
        if not products:
            Response(json.dumps({"error": "No products available"}), mimetype="application/json", status=404)
        
        return Response(json.dumps(products), mimetype="application/json", status=200)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json", status=400)

# Update a Product
@app.route('/product/<int:product_id>', methods=['PUT'])
def updateProduct(product_id):
    try:
        # Extract data from the request
        name = request.json['name']
        price = request.json['price']
        description = request.json['description']
        category = request.json['category']
            
        # Update the product in the database
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE products SET name = %s, price=%s, description = %s, category = %s WHERE id = %s",
                            (name, price, description, category, product_id))
        mysql.connection.commit()
        cursor.close()
        return Response(json.dumps({'message': 'Product updated successfully'}), mimetype="application/json", status=200)
        
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json", status=400)


if __name__ == '__main__':
    app.run(debug=True)
