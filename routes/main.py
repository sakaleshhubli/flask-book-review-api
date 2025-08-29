from flask import Blueprint, jsonify
from collections import OrderedDict
from utils.database import get_connection
from flask_jwt_extended import JWTManager

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    response = OrderedDict([
        ("message", "Welcome to the Book Review API Home Page."),
        ("instructions", "To view available books, visit /tables")
    ])
    return jsonify(response), 200

@main_bp.route("/tables", methods=['GET'])
def get_tables():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_names = [table[0] for table in tables]
    return jsonify({"tables": table_names}), 200

@main_bp.route("/tables/<table_name>", methods=['GET'])
def show_table_content(table_name):
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM `{table_name}`;")
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify({table_name: rows}), 200


app.config["JWT_SECRET_KEY"] = "super_secret_key_here"  
jwt = JWTManager(app)


@main_bp.route('/login', methods=['GET'])
def home():
