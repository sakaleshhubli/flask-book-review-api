from flask import Flask, jsonify, redirect, request
import mysql.connector
from collections import OrderedDict

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='speed',
        database='flaskapi'
    )

@app.route('/', methods=['GET'])
def home():
    response = OrderedDict([
        ("message", "Welcome to the Book Review API Home Page."),
        ("instructions", "To view available books, visit /tables")
    ])
    return jsonify(response), 200

@app.route("/tables", methods=['GET'])
def get_tables():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_names = [table[0] for table in tables]
    return jsonify({"tables": table_names}), 200

@app.route("/tables/<table_name>", methods=['GET'])
def show_table_content(table_name):
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM `{table_name}`;")
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify({table_name: rows}), 200

@app.route("/books", methods=['GET'])
def show_books():
    return redirect('/tables/books')
    
@app.route("/users", methods=['GET'])
def show_users():
    return redirect('/tables/users')

@app.route("/reviews", methods=['GET'])
def show_reviews():
    return redirect('/tables/reviews')

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (email, username) VALUES (%s, %s)", (email, username))
    con.commit()
    cursor.close()
    con.close()
    return jsonify({"message": "User created", "user_id": cursor.lastrowid}), 201


if __name__ == "__main__":
    print("Connecting to DB")
    app.run(debug=True)
