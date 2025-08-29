from flask import Blueprint, jsonify, request
from models.user import UserModel
import hashlib
from flask import Blueprint, request, jsonify
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"message": "user_id and password required"}), 400

    user = UserModel.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Compare hashed password
    hashed_input = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if hashed_input != user.get("password"):
        return jsonify({"message": "Invalid password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user["user_id"]))
    return jsonify({"message": "Login successful", "access_token": access_token})



@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())   # convert back to int
    user = UserModel.get_by_id(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.pop("password", None)  # don't return password
    return jsonify({"user": user})  

@users_bp.route('/', methods=['GET'])
def show_users():
    from routes.main import show_table_content
    return show_table_content('users')



@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")   # take password from request
    role = data.get("role", "user")   # default = user if not provided

    if not (email and username and password):
        return jsonify({"error": "email, username, and password are required"}), 400

    user_id = UserModel.create_user(username, email, password, role)
    return jsonify({"user_id": user_id, "role": role}), 201



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