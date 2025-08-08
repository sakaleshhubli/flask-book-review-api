from flask import Flask, jsonify, redirect, request
import mysql.connector
from collections import OrderedDict

app = Flask(__name__)


#enter your database details
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='****', 
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

# Update methods
@app.route('/updateuser/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE user_id = %s", 
                   (username, email, user_id))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "User not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/updatebook/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    
    if 'user_id' not in data or not check_admin(data['user_id']):
        return jsonify({"error": "Admin access required"}), 403
    
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_year = data.get('published_year')
    average_rating = data.get('average_rating')
    
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("""
        UPDATE books SET title = %s, author = %s, isbn = %s, 
        published_year = %s, average_rating = %s WHERE book_id = %s
    """, (title, author, isbn, published_year, average_rating, book_id))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "Book not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/updatereview/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    anonymous = data.get('anonymous')
    
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("""
        UPDATE reviews SET rating = %s, comment = %s, anonymous = %s 
        WHERE review_id = %s
    """, (rating, comment, anonymous, review_id))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "Review not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "Review updated successfully"}), 200

# Delete methods
@app.route('/deleteuser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "User not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/deletebook/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    data = request.get_json() or {}
    
    if 'user_id' not in data or not check_admin(data['user_id']):
        return jsonify({"error": "Admin access required"}), 403
    
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "Book not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "Book deleted successfully"}), 200

@app.route('/deletereview/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
    con.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        con.close()
        return jsonify({"error": "Review not found"}), 404
    
    cursor.close()
    con.close()
    return jsonify({"message": "Review deleted successfully"}), 200

if __name__ == "__main__":
    print("Connecting to DB")

    app.run()
