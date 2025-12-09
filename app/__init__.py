# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Secret key for session management
    app.config['SECRET_KEY'] = 'e6b8dcc547ba2b86d71ee45ffbcf7c68a9870599a8f2454af4d820a48e5dd42a'
    
    # Import and register blueprints AFTER app creation to avoid circular imports
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app