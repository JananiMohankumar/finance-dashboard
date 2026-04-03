import os
from flask import Flask, jsonify
from config import Config
from extensions import mongo, jwt, bcrypt, cors
from routes.auth import auth_bp
from routes.users import users_bp
from routes.records import records_bp
from routes.dashboard import dashboard_bp
from dotenv import load_dotenv

# Application Factory pattern: Allows us to create different instances of the app (like for testing)
def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Finance API"})

    # Global error handlers so the API doesn't just crash with HTML pages
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal Server Error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
