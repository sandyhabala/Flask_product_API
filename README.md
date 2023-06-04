# Flask_product_API

# Flask Project Setup Documentation

This documentation provides instructions for setting up a Flask project. It includes information about the system structure, authentication and authorization, and installing the required modules.

Installation and Setup

To set up the Flask project and run it locally, follow these steps:

1. Install Python: Make sure you have Python installed on your system. You can download it from the official Python website: https://www.python.org/downloads/

2. Clone the project: Clone the project repository to your local machine or download the provided code.

$ git clone https://github.com/sandyhabala/Flask_product_API.git

3. Set up a virtual environment (optional): It is recommended to set up a virtual environment to keep the project dependencies isolated. Navigate to the project directory in your terminal and run the following commands:

$ python -m venv vert      # Create a new virtual environment

$ vert\Scripts\activate     # Activate the virtual environment (Windows)

4. Install modules that is needed

$ pip install flask

$ pip install Flask-MySQLdb

$ pip install dotenv

5. Set up the database: Create a MySQL database and configure the connection settings in the .env file. Make sure to set the following environment variables:

Add your database connection

MYSQL_HOST=your_host
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database

# How to use the system API

1. Sign up for an account by sending a POST request to /signup with the username and password in the request body.

2. Log in by sending a POST request to /login with the username and password in the request body.

3. Add a new product by sending a POST request to /addProduct with the product details in the request body.

4. Retrieve all products by sending a GET request to /products.

5. Search for products by sending a GET request to /product?q=<category>.

6. Update a product by sending a PUT request to /product/<product_id> with the updated details in the request body.

7. Delete a product by sending a DELETE request to /product/<product_id>.

## Created By

- Sandy Habala
