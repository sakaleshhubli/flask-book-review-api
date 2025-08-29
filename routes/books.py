from flask import Blueprint, jsonify, request
from models.book import BookModel
from utils.auth import check_admin

books_bp = Blueprint('books', __name__, url_prefix='/books')



@books_bp.route('/', methods=['GET'])
def show_books():
    from routes.main import show_table_content
    return show_table_content('books')

@books_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()
    
    if 'user_id' not in data or not check_admin(data['user_id']):
        return jsonify({"error": "Admin access required"}), 403
    
    title = data.get('title')
    author = data.get('author')
    
    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400
    
    book_id = BookModel.create_book(
        title, author, 
        data.get('isbn'), 
        data.get('published_year'), 
        data.get('average_rating')
    )
    
    return jsonify({"message": "Book added successfully", "book_id": book_id}), 201

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    
    if 'user_id' not in data or not check_admin(data['user_id']):
        return jsonify({"error": "Admin access required"}), 403
    
    if BookModel.update_book(
        book_id, 
        data.get('title'), 
        data.get('author'), 
        data.get('isbn'), 
        data.get('published_year'), 
        data.get('average_rating')
    ):
        return jsonify({"message": "Book updated successfully"}), 200
    return jsonify({"error": "Book not found"}), 404

@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    data = request.get_json() or {}
    
    if 'user_id' not in data or not check_admin(data['user_id']):
        return jsonify({"error": "Admin access required"}), 403
    
    if BookModel.delete_book(book_id):
        return jsonify({"message": "Book deleted successfully"}), 200
    return jsonify({"error": "Book not found"}), 404
