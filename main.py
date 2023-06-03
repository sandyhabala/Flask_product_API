import os
import json
from datetime import timedelta
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
app.permanent_session_lifetime = timedelta(minutes=10)

# secret key for session
app.secret_key = "secretkey"

# Initialize MySQL
mysql = MySQL(app)


# register user
@app.route("/signup", methods=['POST'])
def signup():
    try:
        # Extract data from the request
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        # Check if both username and password are provided
        if not username or not password:
            return Response(json.dumps({'error': "Please fill up all fields"}), mimetype="application/json", status=400)

        # Check if the user already exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username, ))
        foundUser = cursor.fetchone()
        
        if foundUser:
            return Response(json.dumps({'error': "User already exists"}), mimetype="application/json", status=409)
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        cursor.connection.commit()
        cursor.close()

        return Response(json.dumps({'message': 'User created successfully'}), mimetype="application/json", status=201)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json", status=400)
    
    
# login user
@app.route('/login', methods=['POST'])
def login():
    # Extract data from the request
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if both username and password are provided
    if not username or not password:
        return Response(json.dumps({'error': "Please fill up all fields"}), mimetype="application/json", status=400)
    
    # Check if the user exists in the database and validate the password
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Set session variables to indicate the user is logged in
        session['loggedIn'] = True
        session['username'] = user['username']
        return Response(json.dumps({'message': 'Login successful'}), mimetype="application/json", status=201)
    else:
        return Response(json.dumps({'message': 'Invalid username or password'}), mimetype="application/json", status=401)


# Add Product to Database
@app.route("/addProduct", methods=['POST'])
def addProduct():
    try:
        
         # Check if the user is logged in
        if 'loggedIn' not in session or not session['loggedIn']:
            return Response(json.dumps({'error': 'Unauthorized'}), mimetype="application/json", status=401)
        
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
        
         # Check if the user is logged in
        if 'loggedIn' not in session or not session['loggedIn']:
            return Response(json.dumps({'error': 'Unauthorized'}), mimetype="application/json", status=401)
        
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


# Delete a Product
@app.route('/product/<int:product_id>', methods=['DELETE'])
def deleteProduct(product_id):
    try:
        
         # Check if the user is logged in
        if 'loggedIn' not in session or not session['loggedIn']:
            return Response(json.dumps({'error': 'Unauthorized'}), mimetype="application/json", status=401)
        
        # Delete the product from the database
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id, ))
        mysql.connection.commit()
        cursor.close()
        
        return Response(json.dumps({'message': 'Product deleted successfully'}), mimetype="application/json", status=200)
    
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), mimetype="application/json", status=400)


if __name__ == '__main__':
    app.run(debug=True)
