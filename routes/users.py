from flask import Blueprint, jsonify, request
from models.user import UserModel

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def show_users():
    from routes.main import show_table_content
    return show_table_content('users')

@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    
    user_id = UserModel.create_user(username, email)
    return jsonify({"message": "User created", "user_id": user_id}), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    if UserModel.update_user(user_id, username, email):
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if UserModel.delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404