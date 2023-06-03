import os
from flask import Flask, request, session
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


if __name__ == '__main__':
    app.run(debug=True)
