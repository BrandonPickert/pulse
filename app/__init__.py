from flask import Flask
from app.routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pulse-workout-tracker-secret-key'
    
    app.register_blueprint(main_bp)
    
    return app
