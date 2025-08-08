from flask import Blueprint, jsonify, request
from models.review import ReviewModel

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/', methods=['GET'])
def show_reviews():
    from routes.main import show_table_content
    return show_table_content('reviews')

@reviews_bp.route('/', methods=['POST'])
def add_review():
    data = request.get_json()
    
    review_id = ReviewModel.create_review(
        data['user_id'],
        data['book_id'], 
        data['rating'],
        data.get('comment', ''),
        data.get('anonymous', False)
    )
    
    return jsonify({"message": "Review created successfully", "review_id": review_id}), 201

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    
    if ReviewModel.update_review(
        review_id, 
        data.get('rating'), 
        data.get('comment'), 
        data.get('anonymous')
    ):
        return jsonify({"message": "Review updated successfully"}), 200
    return jsonify({"error": "Review not found"}), 404

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    if ReviewModel.delete_review(review_id):
        return jsonify({"message": "Review deleted successfully"}), 200
    return jsonify({"error": "Review not found"}), 404
