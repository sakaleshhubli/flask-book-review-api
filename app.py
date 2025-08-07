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

def check_admin(user_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    
    if result and result[0] == 'admin':  # if user exists and is only admin
        return True
    return False

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

@app.route('/addreview', methods=['POST'])
def add_reviews():
    data = request.get_json()
    
    user_id = data['user_id']
    book_id = data['book_id']
    rating = data['rating']
    comment = data.get('comment', '') 
    anonymous = data.get('anonymous', False)
    
    con = get_connection()
    cursor = con.cursor()
    
    
    cursor.execute("""
        INSERT INTO reviews (user_id, book_id, rating, comment, anonymous) 
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, book_id, rating, comment, anonymous))
    
    con.commit()
    review_id = cursor.lastrowid
    cursor.close()
    con.close()
    
    return jsonify({
        "message": "Review created successfully", 
        "review_id": review_id
    }), 201

@app.route('/addbook', methods=['POST'])
def add_book():
    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400

    user_id = data['user_id']

    if not check_admin(user_id):
        return jsonify({"error": "Admin access required"}), 403
    
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    average_rating = data.get('average_rating')
    published_year = data.get('published_year')
    
    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400
    
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("""
        INSERT INTO books (title, author, isbn, published_year, average_rating) 
        VALUES (%s, %s, %s, %s, %s)
    """, (title, author, isbn, published_year, average_rating))
    
    con.commit()
    book_id = cursor.lastrowid
    cursor.close()
    con.close()
    
    return jsonify({
        "message": "Book added successfully", 
        "book_id": book_id
    }), 201

if __name__ == "__main__":
    print("Connecting to DB")
    app.run()