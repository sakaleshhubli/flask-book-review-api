from flask import Flask
from routes.main import main_bp
from routes.users import users_bp
from routes.books import books_bp
from routes.reviews import reviews_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super_secret_key_here"
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(reviews_bp)

if __name__ == "__main__":
    print("Connecting to DB")
    app.run(debug = True)